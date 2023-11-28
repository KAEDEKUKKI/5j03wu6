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
                id, device_name, device_type, ip_address, registration_date = data
                device = Device(device_name, device_type, ip_address)
                device.id = id
                device.registration_date = registration_date
                return device
        return None

    @staticmethod
    def get_by_ip(ip):
        query = "SELECT * FROM device WHERE ip_address = %s"
        with Database() as db:
            data = db.execute_query(query, (ip,), fetch_one=True)
            if data:
                id, device_name, device_type, ip_address, registration_date = data
                device = Device(device_name, device_type, ip_address)
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
                id, device_name, device_type, ip_address, registration_date = row
                device = Device(device_name, device_type, ip_address)
                device.id = id
                device.registration_date = registration_date
                devices.append(device)
            return devices
        return None

    def create(self):
        query = "INSERT INTO device (device_name, device_type, ip_address, protocol_port) VALUES (%s, %s, %s, %s) RETURNING id, registration_date"
        with Database() as db:
            data = db.execute_query(query, (self.device_name, self.device_type, self.ip_address, self.protocol_port,), fetch_one=True)
            if data:
                self.id, self.registration_date = data
                db.connection.commit()
                return self.id
        return None  