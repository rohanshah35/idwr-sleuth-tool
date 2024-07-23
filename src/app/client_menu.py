from src.app.login import email_handler
from src.utils.utils import clear_console


def client_menu(client):
    clear_console()

    client_prompts(client)


def client_prompts(client):
    while True:
        print("\nCurrent client: " + client.get_name())
        print("\nPlease select an option:")
        print("1. Select conversation")
        print("2. Exit")
        print("3. Send a message")
