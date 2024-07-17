import json


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def read_users(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def write_users(self, users):
        with open(self.filename, 'w') as f:
            json.dump(users, f)
