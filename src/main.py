# Main application

from user_manager import UserManager


def main():
    user_manager = UserManager()

    if user_manager.user_data:
        print("Existing credentials found.")
        user_manager.logged_in_prompts()
    else:
        print("No existing credentials found.")
        user_manager.prompt_for_credentials()
        user_manager.logged_in_prompts()

    print("LinkedIn credentials and email are set.")


if __name__ == "__main__":
    main()
