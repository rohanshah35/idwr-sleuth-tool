import json

from src.structures.client import Client
from src.structures.project import Project


class ProjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Project, Client)):
            return obj.to_dict()
        return super().default(obj)


def project_decoder(dct):
    if 'clients' in dct:
        return Project.from_dict(dct)
    elif 'linkedin' in dct:
        return Client.from_dict(dct)
    return dct
