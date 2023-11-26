import psycopg2
from config import DBParams

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
    def _get_data(cls, query, params):
        try:
            with cls._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchone()
        except (Exception, psycopg2.Error) as error:
            print("Error fetching data:", error)
            return None
    @classmethod
    def get_group_by_name(cls, group_name):
        query = "SELECT id, group_name FROM groups WHERE group_name = %s"
        try:
            group_data = cls._get_data(query, (group_name,))
            if group_data:
                id,group_name = group_data
                group = cls(group_name)
                group.id = id
                return group
        except (Exception, psycopg2.Error) as error:
            print("Error getting group by name:", error)
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
                    return group_data
        except (Exception, psycopg2.Error) as error:
            print("EError creating group:", error)
            return None
    @classmethod
    def delete(cls, group_id):
        query = "DELETE FROM groups WHERE id = %s"
        try:
            with cls._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (group_id,))
                    conn.commit()
                    print("Group deleted successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error deleting group:", error)

            
    @classmethod
    def get_all_group_names(cls):
        query = "SELECT id, group_name FROM groups"
        try:
            with cls._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    group_data = cursor.fetchall()
                    group_names = [{"id": id, "group_name": group_name} for id, group_name in group_data]
                    return group_names
        except (Exception, psycopg2.Error) as error:
            print("Error fetching all group names:", error)
            return []

    @classmethod
    def get_id_by_name(cls, group_name):
        query = "SELECT id FROM groups WHERE group_name = %s"
        try:
            with cls._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (group_name,))
                    result = cursor.fetchone()
                    return result[0] if result else None
        except (Exception, psycopg2.Error) as error:
            print("Error getting group id by name:", error)
            return None
class Groups1:   #group_user
    def __init__(self, group_id, user_id):
        self.id = None
        self.group_id= group_id
        self.user_id= user_id
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
    def create(cls, group_id, user_id):
        query = "INSERT INTO group1 (group_id, user_id) VALUES (%s, %s) RETURNING id"
        try:
            with cls._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (group_id, user_id,))
                    group_data = cursor.fetchone()
                    conn.commit()
                if group_data:
                    id = group_data[0]
                    new_group = cls(group_id, user_id)
                    new_group.id = id
                    return new_group
        except (Exception, psycopg2.Error) as error:
            print("Error creating group1:", error)
            return None
    # @classmethod
    # def get_group_by_ids(cls,  group_id, user_id,):
    #     query = "SELECT id, group_id, user_id FROM group1 WHERE group_id = %s AND user_id = %s"
    #     try:
    #         user_group_data = cls.get_group_data(query, (group_id, user_id,))
    #         if user_group_data:
    #             id, group_id, user_id = user_group_data
    #             user_group = cls(group_id, user_id)
    #             user_group.id = id
    #             return group1
    #     except (Exception, psycopg2.Error) as error:
    #         print("Error getting user group by IDs:", error)
    #         return None
    @classmethod
    def delete(cls, group_id, user_id):
        query = "DELETE FROM group1 WHERE group_id = %s AND user_id = %s"
        try:
            with cls._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (group_id, user_id))
                    conn.commit()
            return True
        except (Exception, psycopg2.Error) as error:
            print("删除group1时出错:", error)
            return False
    @classmethod
    def get_all_info(cls):
        query = "SELECT id, group_id, user_id FROM group1"
        try:
            with cls._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    group_data = cursor.fetchall()
                    return [{"id": id, "group_id": group_id, "user_id": user_id} for id, group_id, user_id in group_data]
        except (Exception, psycopg2.Error) as error:
            print("Error fetching all group1 data:", error)
            return []

    @classmethod
    def get_all_users_names(cls):
        query = "SELECT id, first_name, last_name FROM users"
        try:
            with cls._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    user_data = cursor.fetchall()
                    users = [{"id": id, "first_name": first_name, "last_name": last_name} for id, first_name, last_name in user_data]
                    return users
        except (Exception, psycopg2.Error) as error:
            print("Error fetching all users names:", error)
            return []