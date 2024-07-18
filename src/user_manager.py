# ?

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

    # Retrieve stored user data
    def _load_users(self):
        stored_users = self.file_handler.read_users()
        for username, user_data in stored_users.items():
            # If user_data is a dictionary (new format)
            password_hash = user_data.get('password_hash')
            remember_me = user_data.get('remember_me', False)
            # Create User object and add to users dictionary
            self.users[username] = User(username, password_hash, remember_me)

    # Login to LinkedIn
    def login_to_linkedin(self, user):
        decrypted_password = self.encryptor.decrypt(user.password_hash)
        return user.initialize_linkedin_api(user.username, decrypted_password)

    # Login
    def login(self, username, password):
        if username in self.users:
            user = self.users[username]
            stored_encrypted_password = user.password_hash
            try:
                decrypted_password = self.encryptor.decrypt(stored_encrypted_password)
                if password == decrypted_password:
                    print("logged in!")
                    while True:
                        remember_me = input("\nremember credentials? y/n: ")
                        if remember_me.lower() == "y":
                            user.set_remember_me(True)
                            break
                        elif remember_me.lower() == "n":
                            user.set_remember_me(False)
                            break
                        else:
                            print("invalid input")
                    self.login_to_linkedin(user)
                    self._save_users()
                    return True
            except Exception as e:
                print(e)
        return False

    # Register
    def register(self, username, password):
        if not validate_input(username) or not validate_input(password):
            return False
        if username in self.users:
            return False

        encrypted_password = self.encryptor.encrypt(password)
        self.users[username] = User(username, encrypted_password)
        self._save_users()
        return self.login(username, password)

    # Save users
    def _save_users(self):
        users_data = {username: {
            'password_hash': user.password_hash,
            'remember_me': user.remember_me
        } for username, user in self.users.items()}
        self.file_handler.write_users(users_data)

    # Logout
    def logout(self, user):
        user.logout()
        user.set_remember_me(False)
        self._save_users()

    # Change password
    def change_password(self, user, new_password):
        encrypted_password = self.encryptor.encrypt(new_password)
        user.change_password(encrypted_password)
        self._save_users()
        return True

    # Get remembered user
    def get_remembered_user(self):
        for user in self.users.values():
            if user.remember_me:
                return user
        return None
