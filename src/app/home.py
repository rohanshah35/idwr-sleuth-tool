# Handles home page functionality
from src.app.job_menu import job_menu
from src.app.login import prompt_for_credentials, login
from src.fileio.file_handler import JobHandler
from src.structures.client import Client
from src.structures.job import Job
import os

from src.structures.user import UserManager

job_name = None
job_description = None
job_list = []
job_handler = None


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
        print("1. Select job")
        print("2. Create job")
        print("3. Delete job")
        print("4. Account credentials")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            select_job(user_manager)
        elif choice == '2':
            create_job()
        elif choice == '3':
            delete_job()
        elif choice == '4':
            account_credentials(user_manager)
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")


# Displays jobs, user makes selection
def select_job(user_manager):
    job_names = JobHandler.get_all_job_names()
    if not job_names:
        print("No jobs found.")
        return

    print("\nAvailable jobs:")
    for i, name in enumerate(job_names, 1):
        print(f"{i}. {name}")

    while True:
        try:
            choice = int(input("Enter the number of the job you want to select (-1 to go back): "))
            if choice == 0:
                return
            if 1 <= choice <= len(job_names):
                selected_job = JobHandler.load_job(job_names[choice - 1])
                if selected_job:
                    print(f"\nSelected job: {selected_job.get_name()}")
                    print(f"Description: {selected_job.get_description()}")
                    print("Clients:")
                    for client in selected_job.get_clients():
                        print(f"  - {client}")
                job_menu(selected_job, user_manager)
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


# User create job
def create_job():
    global job_handler
    print("Submit -1 to go back")
    prompt_for_job_name()
    job = Job(job_name, job_description)
    client = Client("test", "test", "test@test.com", "test")
    job.add_client(client)
    job_list.append(job)
    job_handler = JobHandler(job)
    job_handler.write_job()


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
def delete_job():
    job_names = JobHandler.get_all_job_names()
    if not job_names:
        print("No jobs found.")
        return

    print("\nAvailable jobs:")
    for i, name in enumerate(job_names, 1):
        print(f"{i}. {name}")

    while True:
        try:
            choice = int(input("Enter the number of the job you want to delete (-1 to go back): "))
            if choice == 0:
                return
            if 1 <= choice <= len(job_names):
                job_name = job_names[choice - 1]
                filename = f'jobs/{job_name}.json'
                try:
                    os.remove(filename)
                    print(f"Job '{job_name}' has been deleted.")
                except OSError as e:
                    print(f"Error deleting job file: {e}")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


# User account credentials (currently empty)
def account_credentials(user_manager):
    print("1. Change credentials")
    print("2. Delete account (wipes all credentials/jobs)")
    while True:
        try:
            choice = int(input("Enter the number of the account credentials (-1 to go back): "))
            if choice == 0:
                return
            if choice == 1:
                prompt_for_credentials(user_manager)
            elif choice == 2:
                user_manager.file_handler.delete_credentials()
                job_names = JobHandler.get_all_job_names()
                for name in job_names:
                    filename = f'jobs/{name}.json'
                    os.remove(filename)
                    print(f"{name} has been deleted.")
                user_manager = UserManager()
                login(user_manager)
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
