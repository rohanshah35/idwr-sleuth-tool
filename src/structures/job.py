# Handles job data

class Job:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.clients = []

    def load_job_data(self):

        return 0

    def save_job_data(self):

        return 0

    def get_name(self):

        return self.name

    def get_description(self):

        return self.description

    def get_clients(self):

        return self.clients

    def add_client(self, client):

        self.clients.append(client)