# Project data structure

from datetime import date
from src.structures.client import Client


class Project:
    def __init__(self, name, description, date_created=None):
        self.__name = name
        self.__description = description
        self.__date_created = date.today() if not date_created else date_created
        self.__clients = []

    # Getters
    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_clients(self):
        return self.__clients

    def get_date_created(self):
        return self.__date_created

    def get_date_created_iso(self):
        return self.__date_created.isoformat()

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_date_created(self, date_created):
        self.__date_created = date_created

    # Client management methods
    def add_client(self, client):
        self.__clients.append(client)

    def remove_client(self, client):
        if client in self.__clients:
            self.__clients.remove(client)
            return True
        return False

    def update_client(self, old_name, updated_client):
        for i, client in enumerate(self.__clients):
            if client.get_name() == old_name:
                self.__clients[i] = updated_client
                break

    def remove_client_by_name(self, client_name):
        for client in self.__clients:
            if client.get_name() == client_name:
                self.__clients.remove(client)
                return True
        return False

    def get_all_client_names(self):
        return [client.get_name() for client in self.__clients]

    # Serialization methods
    def to_dict(self):
        return {
            "name": self.__name,
            "description": self.__description,
            "date_created": self.__date_created.isoformat(),
            "clients": [client.to_dict() for client in self.__clients]
        }

    @classmethod
    def from_dict(cls, data):
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