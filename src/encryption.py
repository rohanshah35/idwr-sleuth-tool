# encryption.py
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# this function creates a key from a password
def generate_key(password):
    # convert password to bytes
    password = password.encode()
    # set a fixed salt (not recommended for real use)
    salt = b'salt_'
    # create a key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    # generate and return the key
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


# this class handles encryption and decryption
class Encryptor:
    # initialize with a password
    def __init__(self, password):
        self.fernet = Fernet(generate_key(password))

    # encrypt a string
    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    # decrypt a string
    def decrypt(self, data: str) -> str:
        return self.fernet.decrypt(data.encode()).decode()
