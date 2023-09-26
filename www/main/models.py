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
class Groups:
    def __init__(self, group_name):
        self.id = None
        self.group_name = group_name

    @staticmethod
    def _get_connection():
        return psycopg2.connect(**db_params)
    @classmethod
    def get_group_data(cls, query, params):
        try:
            with cls._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchone()
        except (Exception, psycopg2.Error) as error:
            print("Error fetching user data:", error)
            return None
    @classmethod
    def get_group_by_name(cls, group_name):
        query = "SELECT id, group_name FROM groups WHERE group_name = %s"
        try:
            group_data = cls.get_group_data(query, (group_name,))
            if group_data:
                id,group_name = group_data
                group = cls(group_name)
                group.id = id
                print("GG")
                return group
        except (Exception, psycopg2.Error) as error:
            print("Error getting group by name::", error)
            return None

    @classmethod
    def create(self, group_name):
        query = "INSERT INTO groups (group_name) VALUES (%s)RETURNING id"
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (group_name,))
                    group_data = cursor.fetchone()
                    conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("EError creating group:", error)
            return None

    

# # 示例用法：
# # 获取用户的userid和group_id
# user_id = input("Enter user ID: ")
# group_id = input("Enter group ID: ")