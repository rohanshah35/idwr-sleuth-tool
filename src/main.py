from user_manager import UserManager


def main():
    user_manager = UserManager()

    while True:
        print("\n1. Login\n2. Register\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if user_manager.login(username, password):
                print(f"Welcome back, {username}!")
            else:
                print("Invalid username or password!")
        elif choice == "2":
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            if user_manager.register(username, password):
                print(f"Registration success, {username}!")
            else:
                print(f"Username {username} already exists!")
        elif choice == "3":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
