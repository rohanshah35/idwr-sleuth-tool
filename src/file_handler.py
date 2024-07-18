# file_handler.py
import json

# this class handles reading and writing user data to a file
class FileHandler:
    # initialize with a filename
    def __init__(self, filename):
        self.filename = filename

    # read users from the file
    def read_users(self):
        users = {}
        try:
            # open the file and read line by line
            with open(self.filename, 'r') as f:
                for line in f:
                    # parse each line as json and add to users dictionary
                    user_data = json.loads(line.strip())
                    users.update(user_data)
        except FileNotFoundError:
            # if file doesn't exist, just return an empty dictionary
            pass
        return users

    # write users to the file
    def write_users(self, users):
        # open the file and write the users dictionary as json
        with open(self.filename, 'w') as f:
            json.dump(users, f)
            f.write('\n')