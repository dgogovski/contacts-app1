from flask import Flask
from flask import redirect, render_template, request
from contact import Contact
from contacts_db import Database
from user import User
from users_db import DB

app = Flask(__name__)
database = Database()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    values = [
        None,
        request.form['username'],
        request.form['number'],
        User.hash_password(request.form['password'])
    ]
    User(*values).create()
    return redirect('/')


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    auth = request.form['auth']
    password = request.form['password']
    user = User.find_by_username(auth)

    if user:
        if user.verify_password(password) is True:
            return redirect('/contacts')
        else:
            return redirect('/login')
    else:
        return redirect('/register')


@app.route('/contacts', methods=['GET'])
def display_contacts():
    return render_template('contacts.html', contacts=database.get_contacts())


@app.route('/contacts/create', methods=['GET'])
def create_contact_get():
    return render_template('create_contact.html')


@app.route('/contacts/create', methods=['POST'])
def create_contact_post():
    database.add_contact(Contact(request.form['Name'], request.form['Number'], request.form['Note']))
    return redirect('/contacts')


@app.route('/contacts/<int:contact_id>', methods=['GET'])
def display_contact(contact_id):
    contact = database.get_contact_by_id(contact_id)

    if contact is None:
        return 'Error'
    return render_template('contact.html', contact=contact)


@app.route('/contacts/<int:contact_id>', methods=['POST'])
def update_contact(contact_id):
    contact = database.get_contact_by_id(contact_id)

    try:
        if request.form['Update_button'] is not None:
            database.update_contact(contact_id, request.form['Name'], request.form['Number'], request.form['Note'])
            return redirect('/contacts/' + str(contact.id))
    except KeyError:
        try:
            if request.form['Delete_button'] is not None:
                try:
                    database.delete_contact(contact_id)
                    return redirect('/contacts')
                except:
                    return 'Error deleting contact'
        except KeyError:
            return 'KeyError: no element request.form[\'Delete_button\']'


if __name__ == "__main__":
    app.run()
