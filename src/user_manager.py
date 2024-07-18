# user_manager.py
from file_handler import FileHandler
from utils import validate_input
from encryption import Encryptor
from user import User


class UserManager:
    def __init__(self):
        self.file_handler = FileHandler('users.json')
        self.encryptor = Encryptor(
            "71X-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        self.users = {}
        self._load_users()

    def _load_users(self):
        stored_users = self.file_handler.read_users()
        for username, encrypted_password in stored_users.items():
            self.users[username] = User(username, encrypted_password)

    def login(self, username, password):
        if username in self.users:
            stored_encrypted_password = self.users[username].password_hash
            try:
                decrypted_password = self.encryptor.decrypt(stored_encrypted_password)
                if password == decrypted_password:
                    print("Logged in!")
                    self.users[username].initialize_linkedin_api(username, password)
                    return True
            except Exception as e:
                print(e)
        return False

    def register(self, username, password):
        if not validate_input(username) or not validate_input(password):
            return False
        if username in self.users:
            return False

        encrypted_password = self.encryptor.encrypt(password)
        self.users[username] = User(username, encrypted_password)
        self._save_users()
        self.login(username, password)
        return True

    def _save_users(self):
        users_data = {username: user.password_hash for username, user in self.users.items()}
        self.file_handler.write_users(users_data)

    def logout(self, username):
        if username in self.users:
            self.users[username].logout()

    def change_password(self, username, new_password):
        if username in self.users:
            encrypted_password = self.encryptor.encrypt(new_password)
            self.users[username].change_password(encrypted_password)
            self._save_users()
            return True
        return False
