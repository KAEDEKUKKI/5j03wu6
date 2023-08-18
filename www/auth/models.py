import psycopg2
from config import DBParams
from passlib.hash import bcrypt_sha256

db_params = {
    'dbname': DBParams.dbname,
    'user': DBParams.user,
    'password': DBParams.password,
    'host': DBParams.host,
    'port': DBParams.port,
}

class Users:
    def __init__(self, first_name, last_name, email):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.passwd = ''
        self.start_time = None

    @staticmethod
    def _get_connection():
        return psycopg2.connect(**db_params)

    @classmethod
    def _get_user_data(cls, query, params):
        try:
            with cls._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchone()
        except (Exception, psycopg2.Error) as error:
            print("Error fetching user data:", error)
            return None

    @classmethod
    def get_user_by_id(cls, user_id):
        query = "SELECT id, first_name, last_name, email, start_time FROM users WHERE id = %s"
        try:
            user_data = cls._get_user_data(query, (user_id,))
            if user_data:
                id, first_name, last_name, email, start_time = user_data
                user = cls(first_name, last_name, email)
                user.id = id
                user.start_time = start_time
                return user
        except (Exception, psycopg2.Error) as error:
            print("Error getting user by ID:", error)
        return None

    @classmethod
    def get_user_by_email(cls, email):
        query = "SELECT id, first_name, last_name, email, start_time FROM users WHERE email = %s"
        try:
            user_data = cls._get_user_data(query, (email,))
            if user_data:
                id, first_name, last_name, email, start_time = user_data
                user = cls(first_name, last_name, email)
                user.id = id
                user.start_time = start_time
                return user
        except (Exception, psycopg2.Error) as error:
            print("Error getting user by email:", error)
        return None

    def check_password(self, password):
        query = "SELECT passwd FROM users WHERE id = %s"
        stored_password = self._get_user_data(query, (self.id,))

        if stored_password:
            return bcrypt_sha256.verify(password, stored_password[0])
        else:
            return False

    def set_password(self, password, ck_passwd):
        if password == ck_passwd:
            self.passwd = bcrypt_sha256.hash(password)

    def create(self):
        query = "INSERT INTO users (first_name, last_name, email, passwd) VALUES (%s, %s, %s, %s) RETURNING id, start_time"
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (self.first_name, self.last_name, self.email, self.passwd))
                    user_data = cursor.fetchone()
                    conn.commit()

                    if user_data:
                        self.id, self.start_time = user_data

                        #user_db_name = self.email.replace('@', '_').replace('.', '_')

                        #create_db_query = f"CREATE DATABASE {user_db_name}"
                        #cursor.execute(create_db_query)

                        #conn.commit()

                        return self.id
        except (Exception, psycopg2.Error) as error:
            print("Error creating user:", error)
            return None

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        # Add your own authentication logic if needed
        # Here, we assume that the user is authenticated if id is not None
        return self.id is not None

    @property
    def is_active(self):
        # Add your own account activity logic if needed
        # Here, we assume that the user is always active
        return True

    @property
    def is_anonymous(self):
        # Add your own anonymous user logic if needed
        # Here, we assume that the user is not anonymous
        return False

#class DatabaseManager:
#    def __init__(self, dbname):
#        self.db_params = {
#            'dbname': dbname,
#            'user': DBParams.user,
#            'password': DBParams.password,
#            'host': DBParams.host,
#            'port': DBParams.port,
#        }
#
#    def create_tables(self, email):
#        query = f"""
#            CREATE TABLE IF NOT EXISTS groups (
#                id SERIAL PRIMARY KEY,
#                name VARCHAR(255) NOT NULL
#            );
#            
#            CREATE TABLE IF NOT EXISTS device (
#                id SERIAL PRIMARY KEY,
#                name VARCHAR(255) NOT NULL,
#                group_id INT REFERENCES groups(id)
#            );
#        """
#        with psycopg2.connect(**self.db_params, dbname=db_name) as conn:
#            with conn.cursor() as cursor:
#                cursor.execute(query)
#                conn.commit()
#
#    def initialize_user_data(self, email):
#        self.create_tables(email)
