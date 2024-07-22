# General utility
import re

# Validates LinkedIn credentials
def linkedin_validator(input_string):

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', input_string)

    if match == None:
        return False

    return True

# Validates email credentials
def email_validator(input_string):

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', input_string)

    if match == None:
        return False

    return True
