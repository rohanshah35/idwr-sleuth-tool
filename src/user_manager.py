# user_manager.py
from file_handler import FileHandler
from utils import validate_input
from encryption import Encryptor
from user import User


class UserManager:
    def __init__(self):
        # Initialize FileHandler for user data persistence
        self.file_handler = FileHandler('users.json')
        # Initialize Encryptor with a secret key
        self.encryptor = Encryptor(
            "71X-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        # Dictionary to store user objects
        self.users = {}
        # Load existing users from file
        self._load_users()

    def _load_users(self):
        # Retrieve stored user data
        stored_users = self.file_handler.read_users()
        for username, user_data in stored_users.items():
            # If user_data is a dictionary (new format)
            password_hash = user_data.get('password_hash')
            remember_me = user_data.get('remember_me', False)
            # Create User object and add to users dictionary
            self.users[username] = User(username, password_hash, remember_me)

    def login_to_linkedin(self, user):
        decrypted_password = self.encryptor.decrypt(user.password_hash)
        return user.initialize_linkedin_api(user.username, decrypted_password)

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
                    self.login_to_linkedin(user)  # Pass the User object, not just the username
                    self._save_users()  # Save after updating remember_me
                    return True
            except Exception as e:
                print(e)
        return False

    def register(self, username, password):
        # Validate input and check if username already exists
        if not validate_input(username) or not validate_input(password):
            return False
        if username in self.users:
            return False

        # Encrypt password and create new User object
        encrypted_password = self.encryptor.encrypt(password)
        self.users[username] = User(username, encrypted_password)
        self._save_users()
        # Log in the newly registered user
        return self.login(username, password)

    def _save_users(self):
        # Prepare user data for saving
        users_data = {username: {
            'password_hash': user.password_hash,
            'remember_me': user.remember_me
        } for username, user in self.users.items()}
        # Write user data to file
        self.file_handler.write_users(users_data)

    def logout(self, user):
        user.logout()
        user.set_remember_me(False)
        self._save_users()  # Save changes after logout

    def change_password(self, user, new_password):
        # Encrypt new password and update user object
        encrypted_password = self.encryptor.encrypt(new_password)
        user.change_password(encrypted_password)
        self._save_users()
        return True

    def get_remembered_user(self):
        # Return the User object, not just the username
        for user in self.users.values():
            if user.remember_me:
                return user
        return None
