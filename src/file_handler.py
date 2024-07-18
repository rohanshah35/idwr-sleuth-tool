# file_handler.py
import json


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

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

    def write_users(self, users):
        with open(self.filename, 'w') as f:
            json.dump(users, f)
            f.write('\n')
