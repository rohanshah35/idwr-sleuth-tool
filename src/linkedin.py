# LinkedIn functionality

from linkedin_api import Linkedin


def initialize_linkedin_api(username, password):
    print("authorizing details on linkedin.py..")
    while True:
        try:
            linkedin_api = Linkedin(username, password)
            print("linkedin.py api initialized")
            return linkedin_api
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
