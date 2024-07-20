# Run application
from login import Login
from user_manager import UserManager


def main():
    user_manager = UserManager()

    login = Login(user_manager)
    login.login()


if __name__ == "__main__":
    main()
