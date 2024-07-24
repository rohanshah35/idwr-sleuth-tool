from src.app.job_menu import job_menu
from src.utils.utils import clear_console


def client_menu(client, job, user_manager):
    clear_console()

    client_prompts(client, job, user_manager)


def client_prompts(client, job, user_manager):
    while True:
        print("\nCurrent client: " + client.get_name())
        print("\nPlease select an option:")
        print("1. LinkedIn conversation")
        print("2. Send LinkedIn message")
        print("3. Email conversation")
        print("4. Send email message")
        print()
        print("4. Back to job menu")
        choice = input("Enter your choice(1-4): ")
        if choice == '1':
            clear_console()
            view_linkedin_conversation(client)
            clear_console()
        elif choice == '2':
            clear_console()
            send_linkedin_message(client)
            clear_console()
        elif choice == '3':
            clear_console()
            view_email_conversation(client)
            clear_console()
        elif choice == '4':
            clear_console()
            send_email_message(client)
            clear_console()
        elif choice == '5':
            clear_console()
            back_to_job_menu(job, user_manager)
            clear_console()
        else:
            print("Invalid choice. Please try again.")
            clear_console()


def view_linkedin_conversation():
    return 0


def send_linkedin_message():
    return 0


def view_email_conversation():
    return 0


def send_email_message():
    return 0


def back_to_job_menu(job, user_manager):
    job_menu(job, user_manager)
