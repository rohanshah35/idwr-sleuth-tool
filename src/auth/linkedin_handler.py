# LinkedIn functionality
from linkedin_api import Linkedin


# Initialize LinkedIn API
def initialize_linkedin_api(username, password):
    try:
        linkedin_api = Linkedin(username, password)
        print("LinkedIn Verified!")
        return linkedin_api
    except Exception as e:
        if e.__str__() == 'CHALLENGE':
            raise Exception("Challenge failed, could be captcha, please try again")
        elif e.__str__() == 'BAD_USERNAME_OR_PASSWORD':
            raise Exception("Invalid LinkedIn credentials, please try again")
        else:
            print(e)
            return False
