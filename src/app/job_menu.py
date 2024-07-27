from src.fileio.file_handler import JobHandler
from src.structures.client import Client
from src.utils.utils import clear_console

client_name = None
client_description = None
client_email = None
client_linkedin = None


def job_menu(job, user_manager):
    clear_console()

    job_prompts(job, user_manager)


def job_prompts(job, user_manager):
    while True:
        print("\nCurrent job: " + job.get_name())
        print("\nPlease select an option:")
        print("1. Select client")
        print("2. Create client")
        print("3. Delete client")
        print()
        print("4. Back to home menu")
        choice = input("Enter your choice(1-4): ")
        if choice == '1':
            clear_console()
            select_client(job, user_manager)
            clear_console()
        elif choice == '2':
            clear_console()
            create_client(job, user_manager)
            clear_console()
        elif choice == '3':
            clear_console()
            delete_client(job, user_manager)
            clear_console()
        elif choice == '4':
            clear_console()
            back_to_home(user_manager)
        else:
            print("Invalid choice. Please try again.")
            clear_console()


def select_client(job, user_manager):
    from src.app.client_menu import client_menu
    clients = job.get_clients()
    if not clients:
        print("No clients found for this job.")
        return None

    print("0. Return to job menu")

    print("\nAvailable clients:")
    for i, client in enumerate(clients, 1):
        print(f"{i}. {client.get_name()} - {client.get_email()}")

    while True:
        try:
            choice = int(input("Enter the number of the client you want to select (0 to go back): "))
            if choice == 0:
                return job_menu(job, user_manager)
            if 1 <= choice <= len(clients):
                print(clients)
                selected_client = clients[choice-1]
                print(f"\nSelected client: {selected_client.get_name()}")
                print(f"Description: {selected_client.description}")
                print(f"Email: {selected_client.get_email()}")
                print(f"LinkedIn: {selected_client.linkedin}")
                client_menu(selected_client, job, user_manager)
            else:
                print("Invalid choice. Please try again.")
                clear_console()
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


def create_client(job, user_manager):
    print("Submit -1 to go back")
    prompt_for_client_name()
    client = Client(client_name, client_description, client_linkedin, client_email)
    job.add_client(client)
    job_manager = JobHandler(job)
    job_manager.write_job()


def prompt_for_client_name():
    global client_name
    name = input("Enter client's name: ")
    if name == "-1":
        prompt_for_client_name()
        return
    client_name = name
    prompt_for_client_desc()


def prompt_for_client_desc():
    global client_description
    description = input("Enter client's description: ")
    if description == "-1":
        prompt_for_client_name()
        return
    client_description = description
    prompt_for_client_linkedin()


def prompt_for_client_linkedin():
    global client_linkedin
    linkedin = input("Enter linkedin profile URL (or leave blank): ")
    if linkedin == "-1":
        prompt_for_client_desc()
        return
    client_linkedin = linkedin
    prompt_for_client_email()


def prompt_for_client_email():
    global client_email
    email = input("Enter client email (or leave blank): ")
    if email == "-1":
        prompt_for_client_linkedin()
        return
    client_email = email


def delete_client(job, user_manager):
    client_names = job.get_all_client_names()
    if not client_names:
        print("No clients found for this job.")
        return

    print("0. Return to job menu")

    print("\nAvailable clients:")
    for i, client in enumerate(client_names, 1):
        print(f"{i}. {client}")

    while True:
        try:
            choice = int(input("Enter the number of the client you want to delete: "))
            if choice == 0:
                job_menu(job, user_manager)
            if 1 <= choice <= len(client_names):
                selected_client_name = client_names[choice - 1]
                job.remove_client_by_name(selected_client_name)
                job_manager = JobHandler(job)
                job_manager.write_job()
                print(f"\nSelected client has been deleted: {selected_client_name}")
                break
            else:
                print("Invalid choice. Please try again.")
                clear_console()
        except ValueError:
            print("Please enter a valid number.")


def back_to_home(user_manager):
    from src.app.home import home
    home(user_manager)
