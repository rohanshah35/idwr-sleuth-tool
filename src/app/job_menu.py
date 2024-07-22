from src.app.login import login

client_name = None
client_description = None
client_email = None
client_linkedin = None

def job_menu(job, user_manager):
    job_prompts(job, user_manager)


def job_prompts(job, user_manager):
    while True:
        print("\n Current job: " + job.get_name())
        print("\nPlease select an option:")
        print("1. Select client")
        print("2. Create client")
        print("3. Delete client")
        print("4. Back to home")
        choice = input("Enter your choice(1-4): ")
        if choice == '1':
            select_client(job, user_manager)
        elif choice == '2':
            create_client(job, user_manager)
        elif choice == '3':
            delete_client(job, user_manager)
        elif choice == '4':
            back_to_home(user_manager)
        else:
            print("Invalid choice. Please try again.")


def select_client(job, user_manager):
    clients = job.get_clients()
    if not clients:
        print("No clients found for this job.")
        return None

    print("\nAvailable clients:")
    for i, client in enumerate(clients, 1):
        print(f"{i}. {client.get_name()} - {client.get_email()}")

    while True:
        try:
            choice = int(input("Enter the number of the client you want to select (0 to go back): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(clients):
                selected_client = clients[choice - 1]
                print(f"\nSelected client: {selected_client.get_name()}")
                print(f"Description: {selected_client.description}")
                print(f"Email: {selected_client.get_email()}")
                print(f"LinkedIn: {selected_client.linkedin}")
                return selected_client
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


def create_client(job, user_manager):
    global client_name, client_description, client_email, client_linkedin
    print("Submit -1 to go back")
    prompt_for_client_name()


def delete_client(job, user_manager):
    return 0


def back_to_home(user_manager):
    from src.app.home import home
    home(user_manager)
