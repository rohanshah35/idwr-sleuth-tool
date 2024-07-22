import json

from src.structures.client import Client


class Job:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.clients = []

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_clients(self):
        return self.clients

    def add_client(self, client):
        self.clients.append(client)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "clients": [client.to_dict() for client in self.clients]
        }

    @classmethod
    def from_dict(cls, data):
        job = cls(data['name'], data['description'])
        for client_data in data.get('clients', []):
            try:
                client = Client.from_dict(client_data)
                job.add_client(client)
            except Exception as e:
                print(f"Error creating client from data: {client_data}")
                print(f"Error: {str(e)}")
        return job
