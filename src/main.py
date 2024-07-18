# main.py
from user_manager import UserManager


def display_logged_out_menu():
    print("\n1. Login\n2. Register\n3. Exit")
    return input("Enter your choice: ")


def display_logged_in_menu(username):
    print(f"\nWelcome, {username}!")
    print("1. Logout\n2. Change Password\n3. Exit")
    return input("Enter your choice: ")


def main():
    user_manager = UserManager()
    current_user = None

    while True:
        if current_user is None:
            choice = display_logged_out_menu()

            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                if user_manager.login(username, password):
                    current_user = username
                    print("Login successful!")
                else:
                    print("Invalid credentials.")
            elif choice == '2':
                username = input("Enter new username: ")
                password = input("Enter new password: ")
                if user_manager.register(username, password):
                    print("Registration successful!")
                else:
                    print("Username already exists or invalid input.")
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

        else:
            choice = display_logged_in_menu(current_user)

            if choice == '1':
                user_manager.logout(current_user)
                print(f"Logged out successfully. Goodbye, {current_user}!")
                current_user = None
            elif choice == '2':
                new_password = input("Enter new password: ")
                if user_manager.change_password(current_user, new_password):
                    print("Password changed successfully!")
                else:
                    print("Failed to change password.")
            elif choice == '3':
                print(f"Goodbye, {current_user}!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
