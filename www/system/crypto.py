import hashlib
import random
import bcrypt 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class MyCrypto:
    def __init__(self):
        self.hash_size = 32
        self.x = self.hash("5j03wu6")

    def generate_random_data(self):
        return [random.getrandbits(8) for _ in range(self.hash_size)]

    def hash(self, msg):
        if isinstance(msg, str):
            return hashlib.sha256(msg.encode()).digest()
        return hashlib.sha256(msg).digest()

    def aes_encrypt(self, data, key):
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return ciphertext

    def aes_decrypt(self, encrypted_data, key):
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        return decrypted_data

    def bcrypt(self, data):
        dataBytes = data.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(dataBytes, salt)

    def bcrypt_verify(self, data, hash_data):
        dataBytes = data.encode('utf-8')
        return bcrypt.checkpw(dataBytes, hash_data)