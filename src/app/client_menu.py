from src.app.job_menu import job_menu
from src.utils.utils import clear_console


def client_menu(client, job, user_manager):
    linkedin_handler = user_manager.linkedin_handler
    email_handler = user_manager.email_handler

    clear_console()

    client_prompts(client, job, user_manager, linkedin_handler, email_handler)


def client_prompts(client, job, user_manager, linkedin_handler, email_handler):
    while True:
        print("\nCurrent client: " + client.get_name())
        print("\nPlease select an option:")
        print("1. LinkedIn conversation")
        print("2. Send LinkedIn message")
        print("3. Email conversation")
        print("4. Send email message")
        print()
        print("5. Back to job menu")
        choice = input("Enter your choice(1-4): ")
        if choice == '1':
            clear_console()
            view_linkedin_conversation(client, linkedin_handler)
            clear_console()
        elif choice == '2':
            clear_console()
            send_linkedin_message(client, linkedin_handler)
            clear_console()
        elif choice == '3':
            clear_console()
            view_email_conversation(client, email_handler)
            clear_console()
        elif choice == '4':
            clear_console()
            send_email_message(client, email_handler)
            clear_console()
        elif choice == '5':
            clear_console()
            back_to_job_menu(job, user_manager)
            clear_console()
        else:
            print("Invalid choice. Please try again.")
            clear_console()


def view_linkedin_conversation(client, linkedin_handler):
    print(linkedin_handler.get_conversation_text(client.linkedin))


def send_linkedin_message(client, linkedin_handler):
    print("Enter your message")
    message = input(" ")

    print(linkedin_handler.send_linkedin_message(client.linkedin, message))


# Not sure what to do here for logic, one could have multiple email threads with one client, should we display them all and ask them to choose?
def view_email_conversation(client, email_handler):
    message_ids = email_handler.search_mailbox(client.get_email())
    for email_id in message_ids:
        email_content, email_body = email_handler.get_email_content(email_id)
        print(f"Subject: {email_content['Subject']}")
        print(f"From: {email_content['From']}")
        print(f"Date: {email_content['Date']}")
        print("Content:")
        print(email_body)
        print("--------------------")


def send_email_message(client, email_handler):
    print("Enter the email subject:")
    subject = input(" ")

    print("Enter the email body:")
    body = input(" ")

    email_handler.send_email(client.email, subject, body)


def back_to_job_menu(job, user_manager):
    job_menu(job, user_manager)
