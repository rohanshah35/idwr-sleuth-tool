# Run application
from src.app.login import Login
from src.structures.user import UserManager
import sys
import os

# For VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    user_manager = UserManager()

    login = Login(user_manager)
    login.login()


if __name__ == "__main__":
    main()
