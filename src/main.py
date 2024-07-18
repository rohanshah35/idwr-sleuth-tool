# main.py
from user_manager import UserManager


def display_logged_out_menu():
    print("select an option:")
    print("1. login\n2. register (these credentials will be used to login to linkedin)\n3. exit")
    return input("enter your choice: ")


def display_logged_in_menu(username):
    print(f"\nwelcome, {username}!")
    print("1. log in to Linkedin\n2. change password\n3. logout (this will toggle remember-me feature)\n4. exit")
    return input("enter your choice: ")


def main():
    logged_in_to_linkedin = False
    user_manager = UserManager()
    current_user = user_manager.get_remembered_user()

    # If there's a remembered user, log them in automatically
    if current_user:
        print(f"Remembered user found: {current_user.username}")
        print("Automatic login successful!")
    else:
        print("No remembered user found.")

    # main program loop
    while True:
        if current_user is None:
            choice = display_logged_out_menu()

            if choice == '1':  # login
                username = input("enter username: ")
                password = input("enter password: ")
                if user_manager.login(username, password):
                    current_user = user_manager.users[username]
                    print("login successful!")
                else:
                    print("invalid credentials.")
            elif choice == '2':  # register
                username = input("enter new username: ")
                password = input("enter new password: ")
                if user_manager.register(username, password):
                    current_user = user_manager.users[username]
                    print("registration successful!")
                else:
                    print("username already exists or invalid input.")
            elif choice == '3':  # exit
                print("goodbye!")
                break
            else:
                print("invalid choice. please try again.")

        elif current_user and not logged_in_to_linkedin:
            choice = display_logged_in_menu(current_user.username)

            if choice == '1':  # login to Linkedin
                logged_in_to_linkedin = user_manager.login_to_linkedin(current_user)
            elif choice == '2':  # change password
                new_password = input("enter new password: ")
                if user_manager.change_password(current_user.username, new_password):
                    print("password changed successfully!")
                else:
                    print("failed to change password.")
            elif choice == '3':  # logout
                user_manager.logout(current_user)
                print(f"logged out successfully. goodbye, {current_user.username}!")
                current_user = None
            elif choice == '4':  # exit
                print(f"goodbye, {current_user.username}!")
                break
            else:
                print("invalid choice. please try again.")
        elif logged_in_to_linkedin:
            print(f"logged in to linkedin, {current_user.username}!")
            input("coming soon.......")
            break


if __name__ == "__main__":
    main()
