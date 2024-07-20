# Handles home page functionality
from src.app.login import prompt_for_credentials
from src.fileio.file_handler import JobHandler
from src.structures.job import Job

job_name = None
job_description = None
job_list = []


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
        print("3. Create job")
        print("4. Exit")
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            if user_manager.test_linkedin_credentials():
                print("LinkedIn credentials are valid.")
            else:
                print("LinkedIn credentials are invalid or there was an error.")
        elif choice == '2':
            prompt_for_credentials(user_manager)
        elif choice == '3':
            create_job()
        elif choice == '4':
            print("Exiting credential management.")
            break
        else:
            print("Invalid choice. Please try again.")


# Displays jobs, user makes selection
def select_job():
    return 0


# User create job
def create_job():
    print("Submit -1 to go back")
    prompt_for_job_name()
    job = Job(job_name, job_description)
    job_list.append(job)
    job_manager = JobHandler(job_name)
    job_manager.write_jobs()

# Prompts for job name
def prompt_for_job_name():
    global job_name
    name = input("Enter job name: ")
    if name == "-1":
        prompt_for_job_name()
        return
    job_name = name
    prompt_for_job_desc()

# Prompts for job description
def prompt_for_job_desc():
    global job_description
    description = input("Enter job description: ")
    if description == "-1":
        prompt_for_job_name()
        return
    job_description = description


# User deletes jobs
def delete_job(job):
    return 0


# User account settings
def account_settings():
    return 0
