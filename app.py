from flask import Flask
from flask import redirect, render_template, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from contact import Contact
from database import Database

app = Flask(__name__)
auth = HTTPBasicAuth()
database = Database()


@app.route('/')
def home():
    return redirect('/contacts')


@app.route('/contacts', methods=['GET'])
def contacts_get():
    return render_template('contacts.html', contacts=database.get_contacts())


@app.route('/contacts/create', methods=['GET'])
def create_contact_get():
    return render_template('create_contact.html')


@app.route('/contacts/create', methods=['POST'])
def create_contact_post():
    database.add_contact(Contact(request.form['Name'], request.form['Number'], request.form['Note']))
    return redirect('/contacts')


@app.route('/contacts/<int:contact_id>', methods=['GET', 'POST'])
def contact_view(contact_id):
    contact = Database.get_contact_by_id(database, contact_id)

    if request.method == 'GET':
        if contact is None:
            return 'Error'
        return render_template('contact.html', contact=contact)
    elif request.method == 'POST':
        if request.form['Update_button'] is not None:
            database.update_contact(contact_id, request.form['Name'], request.form['Number'], request.form['Note'])
            return redirect('/contacts/' + str(contact.id))
        if request.form['Delete_button'] is not None:
            return 'hi'
            # database.delete_contact(contact_id)
            return redirect('/contacts')
    return 'hello'

# # https://pythonise.com/series/learning-flask/flask-http-methods
# @app.route('/contacts/<int:contact_id>', methods=['PUT'])
# def contact_update(contact_id):
#     if database.get_contact_by_id(contact_id) in database.get_contacts():
#         database.update_contact(contact_id, 'test', 'test', 'test')
#         return redirect('/contacts/3')
        # return make_response(jsonify({"message": "Collection replaced"}), 200)
    # if request.POST['submit'] == 'Update button':
    #     database.update_contact(contact_id, request.form['Name'], request.form['Number'], request.form['Note'])
    #     # return redirect('/contacts/<int:contact_id>')
    #     return redirect('/contacts/11')
    # elif request.POST['submit'] == 'Delete button':
    #     database.delete_contact(contact_id)
    #     return redirect('/contacts/12')
    # return redirect('/contacts/13')

if __name__ == "__main__":
    app.run()
