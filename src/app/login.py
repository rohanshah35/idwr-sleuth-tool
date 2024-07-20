# Handles login page functionality
from src.utils.utils import validate_input


class Login:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.linked_in_username = None
        self.linked_in_password = None
        self.email = None
        self.email_password = None

    # Main login workflow
    def login(self):
        print("Welcome to IDWR Sleuth Tool!")
        if self.user_manager.user_data:
            print("Existing credentials found.")
            print()
        else:
            print("No existing credentials found.")
            print()
            self.prompt_for_credentials()
        print("LinkedIn credentials and email are set.")

    # Prompt for LinkedIn username
    def prompt_for_linkedin_username(self):
        username = input("LinkedIn username: ")
        if username == "-1":
            self.prompt_for_linkedin_username()
            return
        self.linked_in_username = username
        self.prompt_for_linkedin_password()

    # Prompt for LinkedIn password
    def prompt_for_linkedin_password(self):
        password = input("LinkedIn password: ")
        if password == "-1":
            self.prompt_for_linkedin_username()
            return
        self.linked_in_password = password
        self.prompt_for_email()

    # Prompt for email
    def prompt_for_email(self):
        email = input("Email address: ")
        if email == "-1":
            self.prompt_for_linkedin_password()
            return
        self.email = email
        self.prompt_for_email_password()

    # Prompt for email password
    def prompt_for_email_password(self):
        email_password = input("Email password: ")
        if email_password == "-1":
            self.prompt_for_email()
            return
        self.email_password = email_password

    # Prompts user for credentials and saves them if valid
    def prompt_for_credentials(self):
        while True:
            print("Please enter your LinkedIn credentials, or submit -1 to go back a step")
            self.prompt_for_linkedin_username()

            if validate_input(self.linked_in_username) and validate_input(self.linked_in_password) and \
                    validate_input(self.email) and validate_input(self.email_password):
                self.user_manager.user_data = {
                    'linkedin_username': self.linked_in_username,
                    'linkedin_password': self.linked_in_password,
                    'email': self.email,
                    'email_password': self.email_password
                }
                self.user_manager.save_user_data()
                print("Credentials saved successfully!")
                break
            else:
                print("Invalid input. Please try again.")

    # Displays menu for logged-in user and handles their choices
    def logged_in_prompts(self):
        while True:
            print("\nCurrent credentials:")
            print(f"LinkedIn Username: {self.user_manager.user_data.get('linkedin_username', 'Not set')}")
            print(f"Email: {self.user_manager.user_data.get('email', 'Not set')}")
            print("\nPlease select an option:")
            print("1. Test LinkedIn credentials")
            print("2. Change credentials")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")
            if choice == '1':
                if self.user_manager.test_linkedin_credentials():
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
