# Handles encryption

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Creates a key from a password
def generate_key(password):
    password = password.encode()
    salt = b'salt_'

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


# Handles encryption and decryption
class Encryptor:

    # Initialize with a password
    def __init__(self, password):
        self.fernet = Fernet(generate_key(password))

    # Encrypt a string
    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    # Decrypt a string
    def decrypt(self, data: str) -> str:
        return self.fernet.decrypt(data.encode()).decode()
