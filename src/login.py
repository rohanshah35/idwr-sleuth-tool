# Handles Login functionality
from utils import validate_input


# Main login workflow
def login(user):
    print("Welcome to IDWR Sleuth Tool!")
    if user.user_data:
        print("Existing credentials found.")
        print()
        logged_in_prompts(user)
    else:
        print("No existing credentials found.")
        print()
        prompt_for_credentials(user)
    print("LinkedIn credentials and email are set.")


# Prompt for LinkedIn username
def prompt_for_linkedin_username():
    username = input("LinkedIn username: ")
    if username == "-1":
        prompt_for_linkedin_username()
    return username


# Prompt for LinkedIn password
def prompt_for_linkedin_password():
    password = input("LinkedIn password: ")
    if password == "-1":
        prompt_for_linkedin_username()
    return password


# Prompt for email
def prompt_for_email():
    email = input("Email address: ")
    if email == "-1":
        prompt_for_linkedin_password()
    return email


# Prompt for email password
def prompt_for_email_password():
    email_password = input("Email password: ")
    if email_password == "-1":
        prompt_for_email()
    return email_password


# Prompts user for credentials and saves them if valid
def prompt_for_credentials(self):
    while True:
        print("Please enter your LinkedIn credentials, or submit -1 to go back a step")
        linkedin_username = prompt_for_linkedin_username()
        linkedin_password = prompt_for_linkedin_password()

        print()

        print("Please enter your email credentials, or submit -1 to go back a step")
        email = prompt_for_email()
        email_password = prompt_for_email_password()

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
            break
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
            prompt_for_credentials(self)
        elif choice == '3':
            print("Exiting credential management.")
            break
        else:
            print("Invalid choice. Please try again.")
