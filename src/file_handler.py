# Handles file I/O

import json


# Handles reading and writing user data to a file
class FileHandler:

    # Initialize with a filename
    def __init__(self, filename):
        self.filename = filename

    # Read users from the file
    def read_users(self):
        users = {}
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    user_data = json.loads(line.strip())
                    users.update(user_data)
        except FileNotFoundError:
            pass
        return users

    # Write users to the file
    def write_users(self, users):
        with open(self.filename, 'w') as f:
            json.dump(users, f)
            f.write('\n')
