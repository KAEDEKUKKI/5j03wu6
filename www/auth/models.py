from system.database import Database
from system.crypto import MyCrypto

class Users():
    def __init__(self, first_name, last_name, email):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.passwd = None
        self.start_time = None

    @staticmethod
    def get_by_id(user_id):
        query = "SELECT id, first_name, last_name, email, start_time FROM users WHERE id = %s"
        with Database() as db:
            user_data = db.execute_query(query, (user_id,), fetch_one=True)
            if user_data:
                id, first_name, last_name, email, start_time = user_data
                user = Users(first_name, last_name, email)
                user.id = id
                user.start_time = start_time
                return user
        return None

    @staticmethod
    def get_by_email(email):
        query = "SELECT id, first_name, last_name, email, start_time FROM users WHERE email = %s"
        with Database() as db:
            user_data = db.execute_query(query, (email,), fetch_one=True)
            if user_data:
                id, first_name, last_name, email, start_time = user_data
                user = Users(first_name, last_name, email)
                user.id = id
                user.start_time = start_time
                return user
        return None

    def check_password(self, password):
        query = "SELECT passwd FROM users WHERE id = %s"
        with Database() as db:
            stored_password = db.execute_query(query, (self.id,), fetch_one=True)
            if stored_password:
                crypto = MyCrypto()
                stored_password_str = stored_password[0]

                # Check if the stored password is in the correct bcrypt format
                if len(stored_password_str) == 60 and stored_password_str.startswith("$2b$"):
                    return crypto.bcrypt_verify(password, stored_password_str.encode('utf-8'))
                else:
                    print("Stored password is not in the correct bcrypt format.")
        return False

    def set_password(self, password, ck_passwd):
        if password == ck_passwd:
            crypto = MyCrypto()
            self.passwd = crypto.bcrypt(password).decode('utf-8')

    def create(self):
        query = "INSERT INTO users (first_name, last_name, email, passwd) VALUES (%s, %s, %s, %s) RETURNING id, start_time"
        with Database() as db:
            user_data = db.execute_query(query, (self.first_name, self.last_name, self.email, self.passwd,), fetch_one=True)
            if user_data:
                self.id, self.start_time = user_data
                db.connection.commit()
                return self.id
        return None

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return self.id is not None

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False