import json
from datetime import date

from src.structures.client import Client


class Project:
    def __init__(self, name, description, date_created=None):
        self.name = name
        self.description = description
        if not date_created:
            self.date_created = date.today()
        else:
            self.date_created = date_created
        self.clients = []

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_clients(self):
        return self.clients

    def get_date_created(self):
        return self.date_created

    def get_date_created_iso(self):
        return self.date_created.isoformat()

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
            return True
        return False

    def update_client(self, old_name, updated_client):
        for i, client in enumerate(self.clients):
            if client.get_name() == old_name:
                self.clients[i] = updated_client
                break

    def remove_client_by_name(self, client_name):
        for client in self.clients:
            if client.get_name() == client_name:
                self.clients.remove(client)
                return True
        return False

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "date_created": self.date_created.isoformat(),
            "clients": [client.to_dict() for client in self.clients]
        }

    def get_all_client_names(self):
        return [client.get_name() for client in self.clients]

    @classmethod
    def from_dict(cls, data):
        # split_date = data['date_created'].split('-')
        # date_created = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
        date_created = date.fromisoformat(data['date_created'])
        project = cls(data['name'], data['description'], date_created)
        for client_data in data.get('clients', []):
            try:
                client = Client.from_dict(client_data)
                project.add_client(client)
            except Exception as e:
                print(f"Error creating client from data: {client_data}")
                print(f"Error: {str(e)}")
        return project
