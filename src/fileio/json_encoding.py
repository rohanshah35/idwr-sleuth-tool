import json

from src.structures.client import Client
from src.structures.job import Job


class JobEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Job, Client)):
            return obj.to_dict()
        return super().default(obj)


def job_decoder(dct):
    if 'clients' in dct:
        return Job.from_dict(dct)
    elif 'linkedin' in dct:
        return Client.from_dict(dct)
    return dct
