# User class

from linkedin_api import Linkedin


class User:
    def __init__(self, username, password_hash, remember_me=False):
        self.linkedin_api = None
        self.username = username
        self.password_hash = password_hash
        self.is_logged_in = False
        self.remember_me = remember_me  # Initialize remember_me in the constructor

    # Logout user
    def logout(self):
        self.is_logged_in = False
        self.remember_me = False  # Reset remember_me on logout

    # Change user password
    def change_password(self, new_encrypted_password):
        self.password_hash = new_encrypted_password

    # Change remember me boolean
    def set_remember_me(self, choice):
        self.remember_me = bool(choice)

    # Log into LinkedIn
    def initialize_linkedin_api(self, username, password):
        print("authorizing details on linkedin..")
        while True:
            try:
                self.linkedin_api = Linkedin(username, password)
                print("linkedin api initialized")
                return True
            except Exception as e:
                if e.__str__() == 'CHALLENGE':
                    print("Challenge failed, could be captcha or incorrect credentials")
                    value = input("Press enter to continue trying again or -1 to exit: ")
                    if value == '-1':
                        break
                elif e.__str__() == 'BAD_USERNAME_OR_PASSWORD':
                    raise Exception("Bad username or password, please update your credentials")
                else:
                    return False

    def __str__(self):
        return f"user: {self.username} (logged in: {self.is_logged_in}, remember me: {self.remember_me})"
