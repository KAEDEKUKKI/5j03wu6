import psycopg2
from config import DBParams

class Database:
    def __init__(self):
        self.db_params = {
            'dbname': DBParams.dbname,
            'user': DBParams.user,
            'password': DBParams.password,
            'host': DBParams.host,
            'port': DBParams.port,
        }
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        self.connection = psycopg2.connect(**self.db_params)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None, fetch_one=False):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if fetch_one:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error fetching data:", error)
            return None
