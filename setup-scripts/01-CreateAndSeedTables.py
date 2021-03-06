import psycopg2
import sys

table_creation_succeeded = True
user_creation_succeeded = True

conn_string = "host='localhost' dbname='ChoreExplore' user='cxp' password='choresarereallyfun'"

def execute_commands(commands):
	conn = None
	
	try:
		print ("Connecting to database using" + conn_string)

		conn = psycopg2.connect(conn_string)

		cursor = conn.cursor()

		for command in commands:
			cursor.execute(command)
			conn.commit()

		cursor.close()

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		if conn:
			conn.rollback()
		return False

	finally:
		if conn:
			conn.close()
		
	return True

def create_tables():

	""" Create necessary tables in the database """

	commands = [
		"""
		CREATE TABLE roles
		(
			id INT PRIMARY KEY,
			name VARCHAR(255) NOT NULL
		)
		""",
		"""
		CREATE TABLE users
		(
			id INT PRIMARY KEY,
			role_id INT REFERENCES roles(id),
			username VARCHAR(255) NOT NULL,
			password VARCHAR(255) NOT NULL,
			first_name VARCHAR(255) NOT NULL,
			middle_name VARCHAR(255),
			last_name VARCHAR(255),
			email_address VARCHAR(255),
			date_of_birth date
		)
		""",
		"""
		CREATE TABLE chores
		(
			id INT PRIMARY KEY,
			due_date date,
			name VARCHAR(255),
			description VARCHAR(255),
			points INT NOT NULL
		)
		""",
		"""
		CREATE TABLE rewards
		(
			id INT PRIMARY KEY,
			name VARCHAR(255) NOT NULL,
			description VARCHAR(255) NOT NULL,
			points INT NOT NULL
		)
		"""
	]

	if(execute_commands(commands)):
		return True

	return False

def seed_roles():

	""" Seed the default roles """

	commands = [
		"""
		INSERT INTO roles
			(id, name)
			VALUES
			(0, 'Administrator')
		""",
		"""
		INSERT INTO roles
			(id, name)
			VALUES
			(1, 'Standard')
		"""
	]

	if(execute_commands(commands)):
		return True

	return False

def seed_admin_user():

	""" Seed the admin user """

	commands = [
		"""
		INSERT INTO users
			(id, role_id, username, password, first_name, middle_name, last_name, email_address, date_of_birth)
			VALUES
			(0, 0, 'administrator', 'password', 'first', 'middle', 'last', 'test@email.com', TO_DATE('01 Jan 1945', 'DD Mon YYYY'))
		"""
	]

	if(execute_commands(commands)):
		return True

	return False

if __name__ == '__main__':
	
	if(create_tables()):
		print("Tables created. Seeding roles and admin user...")
		if(seed_roles() and seed_admin_user()):
			print("Roles and admin user seeded.")
	else:
		print("Failed.")