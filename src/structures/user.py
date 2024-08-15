# Handles user data
from src.auth.email_handler import EmailHandler
from src.auth.linkedin_handler import LinkedInHandler
from src.fileio.encryption import Encryptor
from src.fileio.file_handler import CredentialHandler


class UserManager:
    def __init__(self):
        self.file_handler = CredentialHandler()
        self.encryptor = Encryptor("71X-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")  # Initialize the encryptor
        self.user_data = self.load_user_data()
        self.linkedin_username = None
        self.linkedin_password = None
        self.email = None
        self.email_password = None
        self.linkedin_handler = None
        self.email_handler = None

    def get_linkedin_username(self):
        return self.linkedin_username

    def set_linkedin_username(self, username):
        self.linkedin_username = username

    def get_linkedin_password(self):
        return self.linkedin_password

    def set_linkedin_password(self, password):
        self.linkedin_password = password

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_email_password(self):
        return self.email_password

    def set_email_password(self, password):
        self.email_password = password

    def load_handlers(self):
        if self.user_data:
            self.linkedin_handler = LinkedInHandler(self.user_data['linkedin_email'], self.user_data['linkedin_password'])
            self.email_handler = EmailHandler(self.user_data['email'], self.user_data['email_password'])

    # Loads user data from file and decrypts sensitive information
    def load_user_data(self):
        data = self.file_handler.read_credentials()
        if 'linkedin_password' in data:
            data['linkedin_password'] = self.encryptor.decrypt(data['linkedin_password'])
        if 'email_password' in data:
            data['email_password'] = self.encryptor.decrypt(data['email_password'])
        return data

    # Encrypts sensitive data and saves user data to file
    def save_user_data(self):
        encrypted_data = self.user_data.copy()
        if 'linkedin_password' in encrypted_data:
            encrypted_data['linkedin_password'] = self.encryptor.encrypt(encrypted_data['linkedin_password'])
        if 'email_password' in encrypted_data:
            encrypted_data['email_password'] = self.encryptor.encrypt(encrypted_data['email_password'])
        self.file_handler.write_credentials(encrypted_data)

