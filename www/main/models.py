from system.database import Database

class Deivce:
    def __init__(self, d_name, d_type, ip):
        self.id = None
        self.device_name = d_name
        self.device_type = d_type
        self.ip_address = ip
        self.registration_date = None
    