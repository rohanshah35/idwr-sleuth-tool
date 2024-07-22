# Handles login page functionality
from src.auth.email_handler import initialize_email
from src.auth.linkedin_handler import initialize_linkedin_api
from src.utils.utils import linkedin_validator, email_validator, clear_console

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
    while True:
        print("Please enter your LinkedIn credentials, submit -1 to go back a step")
        prompt_for_linkedin_username()

        # while True:
        #     if linkedin_validator(linkedin_username):
        #         try:
        #             if initialize_linkedin_api(linkedin_username, linkedin_password):
        #                 break
        #         except Exception as e:
        #             print(e)
        #             prompt_for_linkedin_username()
        #     else:
        #         print("Invalid LinkedIn credentials, please try again")
        #         prompt_for_linkedin_username()

        print()
        print("Please enter your email credentials, submit -1 to go back a step")
        prompt_for_email()

        # while True:
        #     if email_validator(email):
        #         try:
        #             if initialize_email(email, email_password):
        #                 break
        #         except Exception as e:
        #             print(e)
        #             prompt_for_email()
        #     else:
        #         print("Invalid email, please try again")
        #         prompt_for_email()

        user_manager.user_data = {
            'linkedin_username': linkedin_username,
            'linkedin_password': linkedin_password,
            'email': email,
            'email_password': email_password
        }

        user_manager.save_user_data()
        print("Credentials saved successfully!")
        break
