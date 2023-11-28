from .crypto import MyCrypto

class Handshake:
    def __init__(self):
        self.hash_size = 32
        self.rr = [[0] * self.hash_size for _ in range(3)]
        self.mm = [[0] * self.hash_size for _ in range(2)]
        self.IDi = bytearray(self.hash_size)
        self.crypto = MyCrypto()

    def session_key(self):
        key = bytes(self.rr[0]) + bytes(self.rr[1]) + bytes(self.rr[2]) + self.crypto.hash(self.IDi + self.crypto.x)
        return self.crypto.aes_encrypt(self.crypto.hash(key), self.mm[1])

    def client_hello(self):
        self.IDi = self.crypto.generate_random_data()
        self.rr[0] = self.crypto.generate_random_data()
        result = bytes(self.IDi) + bytes(self.rr[0])
        encrypt_result = self.crypto.aes_encrypt(result, self.crypto.x)
        return bytes(encrypt_result)

    def certificate(self, receive):
        decrypted_msg = self.crypto.aes_decrypt(receive, self.crypto.x)
        self.mm[0] = decrypted_msg[:self.hash_size]
        self.rr[1] = decrypted_msg[self.hash_size:self.hash_size*2]
        if self.mm[0] == self.crypto.hash(bytes(self.rr[1]) + self.crypto.hash(self.IDi + self.crypto.x) + bytes(self.rr[0])):
            self.crypto.generate_random_data(self.rr[2])
            self.mm[1] = self.crypto.hash(bytes(self.rr[2]) + bytes(self.rr[1]) + self.crypto.hash(self.IDi + self.crypto.x))
            result = bytes(self.mm[1]) + bytes(self.rr[2])
            encrypt_result = self.crypto.aes_encrypt(result, self.mm[0])
            return bytes(encrypt_result)
        return bytes([0] * self.hash_size*2)

    def get_all_variables(self):
        all_variables = (
            f"IDi={self.byte_array_to_string(self.IDi)}\n"
            f"x={self.byte_array_to_string(self.crypto.x)}\n"
        )
        for i, rr_i in enumerate(self.rr):
            all_variables += f"rr[{i}]={self.byte_array_to_string(rr_i)}\n"
        for i, mm_i in enumerate(self.mm):
            all_variables += f"mm[{i}]={self.byte_array_to_string(mm_i)}\n"
        return all_variables

    def byte_array_to_string(self, array):
        return ''.join(f"{byte:02X}" for byte in array)

    def perform_handshake(self, client):
        msg = self.client_hello()
        client.sendall('A'.encode('utf-8') + msg)
        response = client.recv(65)
        if response[0:1] == b'B':
            msg = self.certificate(response[1:])
            client.sendall('C'.encode('utf-8') + msg)
        else:
            client.close()
