from system.database import Database

class Device:
    def __init__(self, d_name, d_type, ip, port):
        self.id = None
        self.device_name = d_name
        self.device_type = d_type
        self.ip_address = ip
        self.protocol_port = port
        self.registration_date = None

    @staticmethod
    def get_by_id(d_id):
        query = "SELECT * FROM device WHERE id = %s"
        with Database() as db:
            data = db.execute_query(query, (d_id,), fetch_one=True)
            if data:
                id, device_name, device_type, ip_address, protocol_port, registration_date = data
                device = Device(device_name, device_type, ip_address, protocol_port)
                device.id = id
                device.registration_date = registration_date
                return device
        return None

    @staticmethod
    def get_by_ip(ip, port):
        query = "SELECT * FROM device WHERE ip_address = %s AND protocol_port = %s"
        with Database() as db:
            data = db.execute_query(query, (ip, port,), fetch_one=True)
            if data:
                id, device_name, device_type, ip_address, protocol_port, registration_date = data
                device = Device(device_name, device_type, ip_address, protocol_port)
                device.id = id
                device.registration_date = registration_date
                return device
        return None

    @staticmethod
    def get_all_devices():
        query = "SELECT * FROM device"
        with Database() as db:
            data = db.execute_query(query, (), fetch_one=False)
            devices = []
            for row in data:
                id, device_name, device_type, ip_address, protocol_port, registration_date = row
                device = Device(device_name, device_type, ip_address, protocol_port)
                device.id = id
                device.registration_date = registration_date
                devices.append(device)
            return devices
        return None

    def create(self):
        query = "INSERT INTO device (device_name, type_id, ip_address, protocol_port) VALUES (%s, %s, %s, %s) RETURNING id, registration_date"
        with Database() as db:
            data = db.execute_query(query, (self.device_name, self.device_type, self.ip_address, self.protocol_port,), fetch_one=True)
            if data:
                self.id, self.registration_date = data
                db.connection.commit()
                return self.id
        return None  

    def delete(self):
        query = "DELETE FROM device WHERE id = %s RETURNING id"
        with Database() as db:
            data = db.execute_query(query, (self.id,), fetch_one=True)
            if data:
                deleted_id = data[0]
                db.connection.commit()
                return deleted_id
        return None

class DeviceType:
    def __init__(self, type_name):
        self.id = None
        self.name = type_name

    @staticmethod
    def get_all():
        query = "SELECT * FROM type1"
        with Database() as db:
            data = db.execute_query(query, (), fetch_one=False)
            types = []
            for row in data:
                id, type_name = row
                d_type = DeviceType(type_name)
                d_type.id = id
                types.append(d_type)
            return types
        return None
