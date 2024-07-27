# Handles login page functionality
from src.auth.email_handler import EmailHandler
from src.auth.linkedin_handler import LinkedInHandler
from src.utils.utils import linkedin_validator, clear_console

linkedin_username = None
linkedin_password = None
email = None
email_password = None

linkedin_handler = None
email_handler = None


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
        clear_console()


# Prompt for LinkedIn username
def prompt_for_linkedin_username():
    global linkedin_username
    username = input("LinkedIn username: ")
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


# Prompt for email
def prompt_for_email():
    global email
    email_address = input("Email address: ")
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
    global email_handler, linkedin_handler
    while True:
        print("Please enter your LinkedIn credentials, submit -1 to go back a step")
        prompt_for_linkedin_username()

        while True:
            if linkedin_validator(linkedin_username):
                linkedin_handler = LinkedInHandler(linkedin_username, linkedin_password)
                try:
                    if linkedin_handler.login_to_linkedin_headless():
                        break
                except Exception as e:
                    print(e)
                    prompt_for_linkedin_username()
            else:
                print("Invalid LinkedIn credentials, please try again")
                prompt_for_linkedin_username()

        print()
        print("Please enter your email credentials, submit -1 to go back a step")
        prompt_for_email()
        while True:
            try:
                print("Logging in...")
                email_handler = EmailHandler(email, email_password)
                email_handler.initialize_imap()
                email_handler.initialize_smtp()
                print("Email login successful.")
                break
            except Exception as e:
                print(f"Error during email login: {str(e)}")
                print("Please try again.")
                prompt_for_email()

        user_manager.set_linkedin_username(linkedin_username)
        user_manager.set_linkedin_password(linkedin_password)
        user_manager.set_email(email)
        user_manager.set_email_password(email_password)

        user_manager.user_data = {
            'linkedin_username': linkedin_username,
            'linkedin_password': linkedin_password,
            'email': email,
            'email_password': email_password
        }
        user_manager.save_user_data()
        print("Credentials saved successfully!")
        break
