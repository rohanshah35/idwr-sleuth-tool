# Handles home page functionality
from src.app.login import prompt_for_credentials


# Main home page workflow
def home(user_manager):
    logged_in_prompts(user_manager)

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

# Displays jobs, user makes selection
def select_job():

    return 0

# User create job
def create_job(job):

    return 0

# User deletes jobs
def delete_job(job):

    return 0

# User account settings
def account_settings():

    return 0