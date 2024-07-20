# Run application
from src.app.login import Login
from user import UserManager


def main():
    user_manager = UserManager()

    login = Login(user_manager)
    login.login()


if __name__ == "__main__":
    main()
