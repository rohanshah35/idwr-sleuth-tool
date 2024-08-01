# Handles file I/O
import json
import os

from src.fileio.json_encoding import job_decoder, JobEncoder
from src.structures.job import Job


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

    def delete_credentials(self):
        os.remove(self.filename)


class JobHandler:
    def __init__(self, job):
        self.job = job
        self.filename = f'jobs/{job.get_name()}.json'

    def read_job(self):
        try:
            with open(self.filename, 'r') as f:
                return json.loads(f.read(), object_hook=job_decoder)
        except FileNotFoundError:
            print(f"Job file {self.filename} not found.")
            return None

    def write_job(self):
        os.makedirs('jobs', exist_ok=True)
        with open(self.filename, 'w') as f:
            json.dump(self.job, f, cls=JobEncoder)

    @staticmethod
    def get_all_job_names():
        return [f.replace('.json', '') for f in os.listdir('jobs') if f.endswith('.json')]

    @staticmethod
    def load_job(job_name):
        filename = f'jobs/{job_name}.json'
        try:
            with open(filename, 'r') as f:
                json_data = f.read()
                job_data = json.loads(json_data)
                return Job.from_dict(job_data)
        except FileNotFoundError:
            print(f"Job file {filename} not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {filename}: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error loading job from {filename}: {str(e)}")
            return None

    @staticmethod
    def load_jobs_from_directory(directory='jobs'):
        job_list = []
        job_files = [f for f in os.listdir(directory) if f.endswith('.json')]

        for job_file in job_files:
            with open(os.path.join(directory, job_file), 'r') as file:
                job_data = json.load(file)
                job = Job(job_data['name'], job_data['description'])
                job.clients = job_data.get('clients', [])
                job_list.append(job)

        return job_list
