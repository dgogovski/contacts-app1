from flask import Flask
from flask import redirect, render_template, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from contact import Contact
from database2 import Database2
from user import User

app = Flask(__name__)
app.debug = True
auth = HTTPBasicAuth()
database = Database2()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registration', methods=['GET', 'POST'])
def register():
	if request.method=='GET':
		return render_template('registration.html')
	elif request.method=='POST':
		values = (
			None,
			request.form['username'],
			request.form['number'],
			User.hash_password(request.form['password'])
		)
		User(*values).create()
	return redirect('/')

@app.route('/authentication', methods=['GET', 'POST'])
def authenticate():
	authenticate.checked_password=0
	if request.method=='GET':
		return render_template('authentication.html')
	elif request.method=='POST':
		auth = request.form['auth']
		password = User.hash_password(request.form['password'])
		username = User.find_by_username(auth)
		number = User.find_by_number(auth)
		if username:
			if username.verify_password(password)==False:
				authenticate.checked_password=0
			else:
				authenticate.checked_password=1
		elif number:
			if number.verify_password(password)==False:
				authenticate.checked_password=0
			else:
				authenticate.checked_password=1
		
	return redirect('/identification')

@app.route('/identification')
def identificate():
	if authenticate.checked_password==0:
		return redirect('/authentication')
	if authenticate.checked_password==1:
		return redirect('/contacts')
	
	

@app.route('/contacts', methods=['GET'])
def displayContacts():
	return render_template('contacts.html', contacts=database.get_contacts())


@app.route('/contacts/create', methods=['GET'])
def createContact_GET():
	return render_template('create_contact.html')


@app.route('/contacts/create', methods=['POST'])
def createContact_POST():
	database.add_contact(Contact(request.form['Name'], request.form['Number'], request.form['Note']))
	return redirect('/contacts')


@app.route('/contacts/<int:contact_id>', methods=['GET'])
def displayContact(contact_id):
	contact = Database.get_contact_by_id(database, contact_id)

	if contact is None:
		return 'Error'
	return render_template('contact.html', contact=contact)


@app.route('/contacts/<int:contact_id>', methods=['POST'])
def updateContact(contact_id):
	contact = Database.get_contact_by_id(database, contact_id)

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
