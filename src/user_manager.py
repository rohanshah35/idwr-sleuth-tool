from file_handler import FileHandler
from utils import validate_input
from encryption import Encryptor


class UserManager:
    def __init__(self):
        self.file_handler = FileHandler('users.json')
        self.encryptor = Encryptor("71X-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")

    def login(self, username, password):
        users = self.file_handler.read_users()
        if username in users:
            stored_password = self.encryptor.decrypt(users[username])
            return stored_password == password
        return False

    def register(self, username, password):
        if not validate_input(username) or not validate_input(password):
            return False

        users = self.file_handler.read_users()
        if username in users:
            return False

        encrypted_password = self.encryptor.encrypt(password)
        users[username] = encrypted_password
        self.file_handler.write_users(users)
        return True
