import getpass

from encryption import Encryptor
from file_handler import FileHandler
from linkedin import initialize_linkedin_api
from utils import validate_input


class UserManager:
    def __init__(self):
        self.file_handler = FileHandler('linkedin_user.json')
        self.encryptor = Encryptor("71X-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")  # Initialize the encryptor
        self.user_data = self._load_user_data()

    # Loads user data from file and decrypts sensitive information
    def _load_user_data(self):
        data = self.file_handler.read_users()
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
        self.file_handler.write_users(encrypted_data)

    # Prompts user for credentials and saves them if valid
    def prompt_for_credentials(self):
        print("Please enter your LinkedIn credentials:")
        linkedin_username = input("LinkedIn Username: ")
        linkedin_password = input("LinkedIn Password: ")
        email = input("Email address: ")
        email_password = input("Email Password: ")

        if validate_input(linkedin_username) and validate_input(linkedin_password) and \
                validate_input(email) and validate_input(email_password):
            self.user_data = {
                'linkedin_username': linkedin_username,
                'linkedin_password': linkedin_password,
                'email': email,
                'email_password': email_password
            }
            self.save_user_data()
            print("Credentials saved successfully!")
        else:
            print("Invalid input. Please try again.")

    # Displays menu for logged-in user and handles their choices
    def logged_in_prompts(self):
        while True:
            print("\nCurrent credentials:")
            print(f"LinkedIn Username: {self.user_data.get('linkedin_username', 'Not set')}")
            print(f"Email: {self.user_data.get('email', 'Not set')}")
            print("\nPlease select an option:")
            print("1. Test LinkedIn credentials")
            print("2. Change credentials")
            print("3. Exit")

            choice = input("Enter your choice (1-3): ")

            if choice == '1':
                if self.test_linkedin_credentials():
                    print("LinkedIn credentials are valid.")
                else:
                    print("LinkedIn credentials are invalid or there was an error.")
            elif choice == '2':
                self.prompt_for_credentials()
            elif choice == '3':
                print("Exiting credential management.")
                break
            else:
                print("Invalid choice. Please try again.")

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