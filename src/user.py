# user.py
from linkedin_api import Linkedin


class User:
    def __init__(self, username, password_hash):
        self.linkedin_api = None
        self.username = username
        self.password_hash = password_hash
        self.is_logged_in = False

    def logout(self):
        self.is_logged_in = False

    def change_password(self, new_encrypted_password):
        self.password_hash = new_encrypted_password

    def initialize_linkedin_api(self, username, password):
        self.linkedin_api = Linkedin(username, password)
        print("Linkedin API initialized")
        print(self.linkedin_api.get_user_profile())

    def __str__(self):
        return f"User: {self.username} (logged in: {self.is_logged_in})"