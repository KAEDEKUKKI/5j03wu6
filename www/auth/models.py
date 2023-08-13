import psycopg2
from config import DBParams
import hashlib

db_params={
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
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = False

    @classmethod
    def get_user_by_id(cls, id):
        try:
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()
    
            select_query = """
            SELECT * FROM "users" WHERE email = %s
            """
            cursor.execute(select_query, (email,))
            user_data = cursor.fetchone()
    
            cursor.close()
            conn.close()

            if user_data and user_data[4] == hashlib.sha256(password.encode('utf-8')).hexdigest():
                id, first_name, last_name, email, passwd, start_time = user_data
                user = cls(first_name, last_name, email)
                user.id = id
                user.start_time = start_time
                user.is_authenticated = True
                user.is_active = True
                return user
            else:
                print("WRONG PASSWORD")
                return None
        except (Exception, psycopg2.Error) as error:
            print("Error getting user:", error)
            return None

    @classmethod
    def get_user_by_email(cls, email, password):
        try:
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()
    
            select_query = """
            SELECT * FROM "users" WHERE email = %s
            """
            cursor.execute(select_query, (email,))
            user_data = cursor.fetchone()
    
            cursor.close()
            conn.close()

            if user_data and user_data[4] == hashlib.sha256(password.encode('utf-8')).hexdigest():
                id, first_name, last_name, email, passwd, start_time = user_data
                user = cls(first_name, last_name, email)
                user.id = id
                user.start_time = start_time
                user.is_authenticated = True
                user.is_active = True
                return user
            else:
                print("WRONG PASSWORD")
                return None
        except (Exception, psycopg2.Error) as error:
            print("Error getting user:", error)
            return None

    def get_id(self):
        return str(self.id)

    def create(self):
        try:
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()

            insert_query = """
            INSERT INTO "users" (first_name, last_name, email, passwd)
            VALUES (%s, %s, %s, %s)
            RETURNING id, start_time
            """
            cursor.execute(insert_query, (self.first_name, self.last_name, self.email, self.passwd))
            user_data = cursor.fetchone()

            conn.commit()
            cursor.close()
            conn.close()

            if user_data:
                self.id, self.start_time = user_data

            return self.id
        except (Exception, psycopg2.Error) as error:
            print("Error creating user:", error)
            return None

    def set_password(self, password, ck_passwd):
        if password == ck_passwd:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            self.passwd = hashed_password
