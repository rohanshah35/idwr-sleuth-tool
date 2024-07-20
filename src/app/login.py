# Handles login page functionality
from src.utils.utils import validate_input
from src.structures.user import UserManager

linkedin_username = None
linkedin_password = None
email = None
email_password = None

# Main login workflow
def login(user_manager):
    print("Welcome to IDWR Sleuth Tool!")
    if user_manager.user_data:
        print("Existing credentials found.")
        print()
    else:
        print("No existing credentials found.")
        print()
        prompt_for_credentials(user_manager)
    print("LinkedIn credentials and email are set.")

# Prompt for LinkedIn username
def prompt_for_linkedin_username():
    global linkedin_username
    username = input("LinkedIn username: ")
    if username == "-1":
        prompt_for_linkedin_username()
        return
    linkedin_username = username
    prompt_for_linkedin_password()

# Prompt for LinkedIn password
def prompt_for_linkedin_password():
    global linkedin_password
    password = input("LinkedIn password: ")
    if password == "-1":
        prompt_for_linkedin_username()
        return
    linkedin_password = password
    prompt_for_email()

# Prompt for email
def prompt_for_email():
    global email
    email_address = input("Email address: ")
    if email_address == "-1":
        prompt_for_linkedin_password()
        return
    email = email_address
    prompt_for_email_password()

# Prompt for email password
def prompt_for_email_password():
    global email_password
    password = input("Email password: ")
    if password == "-1":
        prompt_for_email()
        return
    email_password = password

# Prompts user for credentials and saves them if valid
def prompt_for_credentials(user_manager):
    while True:
        print("Please enter your LinkedIn credentials, or submit -1 to go back a step")
        prompt_for_linkedin_username()

        if validate_input(linkedin_username) and validate_input(linkedin_password) and \
                validate_input(email) and validate_input(email_password):
            user_manager.user_data = {
                'linkedin_username': linkedin_username,
                'linkedin_password': linkedin_password,
                'email': email,
                'email_password': email_password
            }
            user_manager.save_user_data()
            print("Credentials saved successfully!")
            break
        else:
            print("Invalid input. Please try again.")

# Displays menu for logged-in user and handles their choices
def logged_in_prompts(user_manager):
    while True:
        print("\nCurrent credentials:")
        print(f"LinkedIn Username: {user_manager.user_data.get('linkedin_username', 'Not set')}")
        print(f"Email: {user_manager.user_data.get('email', 'Not set')}")
        print("\nPlease select an option:")
        print("1. Test LinkedIn credentials")
        print("2. Change credentials")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            if user_manager.test_linkedin_credentials():
                print("LinkedIn credentials are valid.")
            else:
                print("LinkedIn credentials are invalid or there was an error.")
        elif choice == '2':
            prompt_for_credentials(user_manager)
        elif choice == '3':
            print("Exiting credential management.")
            break
        else:
            print("Invalid choice. Please try again.")
