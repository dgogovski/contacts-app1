import sqlite3

DB_NAME = 'contacts.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''
	CREATE TABLE IF NOT EXISTS users
	(
		user_id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT UNIQUE NOT NULL,
		number TEXT UNIQUE NOT NULL,
		password TEXT NOT NULL
	)		
''')

conn.cursor().execute('''
	CREATE TABLE IF NOT EXISTS contacts
	(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT UNIQUE NOT NULL,
		number TEXT UNIQUE NOT NULL,
		password TEXT NOT NULL
	)		
''')

conn.commit()


class DB:
	def __enter__(self):
		self.conn = sqlite3.connect(DB_NAME)
		return self.conn.cursor()

	def __exit__(self, db_type, value, traceback):
		self.conn.commit()
