import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

from database import DB

class User:
	def __init__(self, id, username, number, password):
		self.id = id
		self.username = username
		self.number = number
		self.password = password

	def create(self):
		with DB() as db:
			values = (self.username, self.number, self.password)
			db.execute('''
				INSERT INTO users (username, number, password)
				VALUES (?, ?, ?)''', values)
			return self

	@staticmethod
	def find_by_number(number):
		if not number:
			return None
		with DB() as db:
			row = db.execute(
				'SELECT * FROM users WHERE number = ?',
				(number,)
			).fetchone()
			if row:
				return User(*row)

	@staticmethod
	def find_by_username(username):
		if not username:
			return None
		with DB() as db:
			row = db.execute(
				'SELECT * FROM users WHERE username = ?',
				(username,)
			).fetchone()
			if row:
				return User(*row)

	@staticmethod
	def hash_password(password):
		return generate_password_hash(password)

	def verify_password(self, submit_password):
		return check_password_hash(self.password, submit_password)
'''
	@staticmethod
	def hash_password(password):
		return hashlib.sha256(password.encode('utf-8')).hexdigest()


	def verify_password(self, username, password):
		return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()
			
'''
