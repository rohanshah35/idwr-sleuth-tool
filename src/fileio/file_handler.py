# Handles file I/O
import json


# Handles reading and writing user data to a file
class CredentialHandler:

    # Initialize with a filename
    def __init__(self):
        self.filename = 'auth/credentials.json'

    # Read credentials from the file
    def read_credentials(self):
        credentials = {}
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    user_data = json.loads(line.strip())
                    credentials.update(user_data)
        except FileNotFoundError:
            pass
        return credentials

    # Write credentials to the file
    def write_credentials(self, credentials):
        with open(self.filename, 'w') as f:
            json.dump(credentials, f)
            f.write('\n')

class JobHandler:

    # Initialize with a filename
    def __init__(self, filename):
        self.filename = filename

    # Read job from a file
    def read_jobs(self, job_name):
        people = {}
        try:
            with open(f'jobs/{job_name}', 'r') as f:
                for line in f:
                    user_data = json.loads(line.strip())
                    people.update(user_data)
        except FileNotFoundError:
            pass
        return people

    # Write job to a new file
    def write_jobs(self, job_name):
        with open(f'jobs/{job_name}', 'w') as f:
            json.dump(job_name, f)
            f.write('\n')
