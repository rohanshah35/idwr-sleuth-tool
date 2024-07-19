# Run application
from login import login
from user_manager import UserManager


def main():
    user_manager = UserManager()

    login(user_manager)


if __name__ == "__main__":
    main()
