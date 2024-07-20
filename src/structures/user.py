# Handles user
from src.fileio.encryption import Encryptor
from src.fileio.file_handler import CredentialHandler
from src.auth.linkedin_handler import initialize_linkedin_api


class UserManager:
    def __init__(self):
        self.file_handler = CredentialHandler()
        self.encryptor = Encryptor("71X-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")  # Initialize the encryptor
        self.user_data = self._load_user_data()

    # Loads user data from file and decrypts sensitive information
    def _load_user_data(self):
        data = self.file_handler.read_credentials()
        print(data)
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

    # Retrieves LinkedIn credentials from user data
    def get_linkedin_credentials(self):
        username = self.user_data['linkedin_username']
        password = self.user_data['linkedin_password']
        return username, password

    # Tests LinkedIn credentials by attempting to initialize the API
    def test_linkedin_credentials(self):
        username, password = self.get_linkedin_credentials()
        try:
            return initialize_linkedin_api(username, password)
        except Exception as e:
            print(e)
            return False
