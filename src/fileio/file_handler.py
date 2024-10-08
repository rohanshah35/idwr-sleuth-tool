# Handles file I/O

import json
import os

from src.fileio.json_encoding import project_decoder, ProjectEncoder
from src.structures.client import Client
from src.structures.project import Project


# Handles reading and writing user data to a file
class CredentialHandler:

    # Initialize with a filename
    def __init__(self):
        self.filename = 'auth/credentials.json'
        os.makedirs("auth", exist_ok=True)

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

    # Delete the credentials file
    def delete_credentials(self):
        os.remove(self.filename)


class ProjectHandler:
    def __init__(self, project):
        self.project = project
        self.filename = f'projects/{project.get_name()}.json'
        os.makedirs("projects", exist_ok=True)

    # Read project data from the file
    def read_project(self):
        try:
            with open(self.filename, 'r') as f:
                return json.loads(f.read(), object_hook=project_decoder)
        except FileNotFoundError:
            print(f"Project file {self.filename} not found.")
            return None

    # Write project data to the file
    def write_project(self):
        os.makedirs('projects', exist_ok=True)
        with open(self.filename, 'w') as f:
            json.dump(self.project, f, cls=ProjectEncoder)

    # Rename the project file
    def rename_project(self, new_name):
        old_filename = self.filename
        new_filename = f'projects/{new_name}.json'
        if old_filename != new_filename:
            if os.path.exists(new_filename):
                os.remove(new_filename)
            os.rename(old_filename, new_filename)
            self.filename = new_filename

    # Get a list of all project names from the directory
    @staticmethod
    def get_all_project_names():
        os.makedirs("projects", exist_ok=True)
        return [f.replace('.json', '') for f in os.listdir('projects') if f.endswith('.json')]

    # Load a specific project by name
    @staticmethod
    def load_project(project_name):
        os.makedirs("projects", exist_ok=True)
        filename = f'projects/{project_name}.json'
        try:
            with open(filename, 'r') as f:
                json_data = f.read()
                project_data = json.loads(json_data)
                return Project.from_dict(project_data)
        except FileNotFoundError:
            print(f"Project file {filename} not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {filename}: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error loading project from {filename}: {str(e)}")
            return None

    # Load all projects from the directory
    @staticmethod
    def load_projects_from_directory(directory='projects'):
        os.makedirs("projects", exist_ok=True)
        project_list = []
        project_files = [f for f in os.listdir(directory) if f.endswith('.json')]

        for project_file in project_files:
            with open(os.path.join(directory, project_file), 'r') as file:
                project_data = json.load(file)
                project = Project(project_data['name'], project_data['description'])

                for client_dict in project_data.get('clients', []):
                    project.add_client(Client.from_dict(client_dict))

                project_list.append(project)

        return project_list
