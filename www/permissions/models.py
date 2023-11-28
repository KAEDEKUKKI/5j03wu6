from system.database import Database

class Groups:
    def __init__(self, group_name):
        self.id = None
        self.group_name = group_name

    @staticmethod
    def get_by_name(group_name):
        query = "SELECT id, group_name FROM groups WHERE group_name = %s"
        with Database() as db:
            data = db.execute_query(query, (group_name,), fetch_one=True)
            if data:
                id, group_name = data
                group = Groups(group_name)
                group.id = id
                return group
        return None

    @staticmethod
    def get_all_group():
        query = "SELECT * FROM groups"
        with Database() as db:
            data = db.execute_query(query, (), fetch_one=False)
            groups = []
            for row in data:
                id, group_name = row
                group = Groups(group_name)
                group.id = id
                devices.append(device)
            return groups
        return None

    def create(self):
        query = "INSERT INTO groups (group_name) VALUES (%s) RETURNING id"
        with Database() as db:
            data = db.execute_query(query, (self.group_name,), fetch_one=True)
            if data:
                self.id = data
                db.connection.commit()
                return self.id
        return None

class UserGroup:
    def __init__(self, user_id, group_id, read_p, write_p, delete_p):
        self.id = None
        self.user_id = user_id
        self.group_id = group_id
        self.read_p = read_p
        self.write_p = write_p
        self.delete_p = delete_p

    @staticmethod
    def get_by_user_group(user_id, group_id):
        query = "SELECT * FROM group1 WHERE user_id = %s AND group_id = %s"
        with Database() as db:
            data = db.execute_query(query, (user_id, group_id), fetch_one=True)
            if data:
                id, user_id, group_id, read_p, write_p, delete_p = data
                user_group = UserGroup(user_id, group_id, read_p, write_p, delete_p)
                user_group.id = id
                return user_group
        return None

    @staticmethod
    def is_admin(user_id):
        query = "SELECT * FROM group1 WHERE user_id = %s AND group_id = 1"
        with Database() as db:
            data = db.execute_query(query, (user_id,), fetch_one=True)
            if data:
                return True
        return False

    @staticmethod
    def get_all_user_groups():
        query = "SELECT * FROM group1"
        with Database() as db:
            data = db.execute_query(query, (), fetch_one=False)
            user_groups = []
            for row in data:
                id, user_id, group_id, read_p, write_p, delete_p = row
                user_group = UserGroup(user_id, group_id, read_p, write_p, delete_p)
                user_group.id = id
                user_groups.append(user_group)
            return user_groups
        return None

    def create(self):
        query = "INSERT INTO group1 (user_id, group_id, read_p, write_p, delete_p) VALUES (%s, %s, %s, %s, %s) RETURNING id"
        with Database() as db:
            data = db.execute_query(query, (self.user_id, self.group_id, self.read_p, self.write_p, self.delete_p), fetch_one=True)
            if data:
                self.id = data
                db.connection.commit()
                return self.id
        return None

    def delete(self):
        query = "DELETE FROM group1 WHERE id = %s"
        with Database() as db:
            db.execute_query(query, (self.id,))
            db.connection.commit()

class UserDevice:
    def __init__(self, user_id, device_id):
        self.id = None
        self.user_id = user_id
        self.device_id = device_id
        self.read_p = True
        self.write_p = True
        self.delete_p = False

    @staticmethod
    def get_by_user_device(user_id, device_id):
        query = "SELECT * FROM group2 WHERE user_id = %s AND device_id = %s"
        with Database() as db:
            data = db.execute_query(query, (user_id, device_id), fetch_one=True)
            if data:
                id, user_id, device_id, read_p, write_p, delete_p = data
                user_device = UserDevice(user_id, device_id, read_p, write_p, delete_p)
                user_device.id = id
                return user_device
        return None

    @staticmethod
    def get_all_user_devices():
        query = "SELECT * FROM group2"
        with Database() as db:
            data = db.execute_query(query, (), fetch_one=False)
            user_devices = []
            for row in data:
                id, user_id, device_id, read_p, write_p, delete_p = row
                user_device = UserDevice(user_id, device_id, read_p, write_p, delete_p)
                user_device.id = id
                user_devices.append(user_device)
            return user_devices
        return None

    @staticmethod
    def select_devices(user_id):
        query = """
        SELECT ud.user_id, ud.device_id, d.device_name
        FROM user_device_permissions ud
        JOIN devices d ON ud.device_id = d.device_id
        WHERE ud.user_id = %s
        AND ud.read_permission = 1;
        """
        with Database() as db:
            data = db.execute_query(query, (), fetch_one=False)
            user_devices = []
            for row in data:
                user_id, device_id, device_name = row
                user_device.id = id
                user_devices.append(user_device)
            return user_devices
        return None

    def create(self):
        query = "INSERT INTO group2 (user_id, device_id, read_p, write_p, delete_p) VALUES (%s, %s, %s, %s, %s) RETURNING id"
        with Database() as db:
            data = db.execute_query(query, (self.user_id, self.device_id, self.read_p, self.write_p, self.delete_p), fetch_one=True)
            if data:
                self.id = data
                db.connection.commit()
                return self.id
        return None

    def delete(self):
        query = "DELETE FROM group2 WHERE id = %s"
        with Database() as db:
            db.execute_query(query, (self.id,))
            db.connection.commit()

class GroupDevice:
    def __init__(self, group_id, device_id, read_p, write_p, delete_p):
        self.id = None
        self.group_id = group_id
        self.device_id = device_id
        self.read_p = read_p
        self.write_p = write_p
        self.delete_p = delete_p

    @staticmethod
    def get_by_group_device(group_id, device_id):
        query = "SELECT * FROM group3 WHERE group_id = %s AND device_id = %s"
        with Database() as db:
            data = db.execute_query(query, (group_id, device_id), fetch_one=True)
            if data:
                id, group_id, device_id, read_p, write_p, delete_p = data
                group_device = GroupDevice(group_id, device_id, read_p, write_p, delete_p)
                group_device.id = id
                return group_device
        return None

    @staticmethod
    def get_all_group_devices():
        query = "SELECT * FROM group3"
        with Database() as db:
            data = db.execute_query(query, (), fetch_one=False)
            group_devices = []
            for row in data:
                id, group_id, device_id, read_p, write_p, delete_p = row
                group_device = GroupDevice(group_id, device_id, read_p, write_p, delete_p)
                group_device.id = id
                group_devices.append(group_device)
            return group_devices
        return None

    def create(self):
        query = "INSERT INTO group3 (group_id, device_id, read_p, write_p, delete_p) VALUES (%s, %s, %s, %s, %s) RETURNING id"
        with Database() as db:
            data = db.execute_query(query, (self.group_id, self.device_id, self.read_p, self.write_p, self.delete_p), fetch_one=True)
            if data:
                self.id = data
                db.connection.commit()
                return self.id
        return None

    def delete(self):
        query = "DELETE FROM group3 WHERE id = %s"
        with Database() as db:
            db.execute_query(query, (self.id,))
            db.connection.commit()
