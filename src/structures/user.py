# User data structure

from src.auth.email_handler import EmailHandler
from src.auth.linkedin_handler import LinkedInHandler
from src.fileio.encryption import Encryptor
from src.fileio.file_handler import CredentialHandler


class UserManager:
    def __init__(self):
        self.__file_handler = CredentialHandler()
        self.__encryptor = Encryptor("71X-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        self.__user_data = self.__load_user_data()
        self.__linkedin_username = None
        self.__linkedin_password = None
        self.__email = None
        self.__email_password = None
        self.__linkedin_handler = None
        self.__email_handler = None

    # Getters
    def get_linkedin_username(self):
        return self.__linkedin_username

    def get_linkedin_password(self):
        return self.__linkedin_password

    def get_email(self):
        return self.__email

    def get_email_password(self):
        return self.__email_password

    def get_linkedin_handler(self):
        return self.__linkedin_handler

    def get_email_handler(self):
        return self.__email_handler

    def get_user_data(self):
        return self.__user_data

    def get_file_handler(self):
        return self.__file_handler

    # Setters
    def set_linkedin_username(self, username):
        self.__linkedin_username = username

    def set_linkedin_password(self, password):
        self.__linkedin_password = password

    def set_email(self, email):
        self.__email = email

    def set_email_password(self, password):
        self.__email_password = password

    def set_linkedin_handler(self, handler):
        self.__linkedin_handler = handler

    def set_email_handler(self, handler):
        self.__email_handler = handler

    def set_user_data(self, user_data):
        self.__user_data = user_data

    # Load messaging handlers
    def load_handlers(self):
        if self.__user_data:
            self.__linkedin_handler = LinkedInHandler(self.__user_data['linkedin_email'], self.__user_data['linkedin_password'])
            self.__email_handler = EmailHandler(self.__user_data['email'], self.__user_data['email_password'])

    # Handle user data
    def __load_user_data(self):
        data = self.__file_handler.read_credentials()
        if 'linkedin_password' in data:
            data['linkedin_password'] = self.__encryptor.decrypt(data['linkedin_password'])
        if 'email_password' in data:
            data['email_password'] = self.__encryptor.decrypt(data['email_password'])
        return data

    def save_user_data(self):
        encrypted_data = self.__user_data.copy()
        if 'linkedin_password' in encrypted_data:
            encrypted_data['linkedin_password'] = self.__encryptor.encrypt(encrypted_data['linkedin_password'])
        if 'email_password' in encrypted_data:
            encrypted_data['email_password'] = self.__encryptor.encrypt(encrypted_data['email_password'])
        self.__file_handler.write_credentials(encrypted_data)