# Run application
import sys
import os

# For VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.login import login
from src.app.home import home
from src.structures.user import UserManager


def main():
    user = UserManager()
    login(user)


if __name__ == "__main__":
    main()
