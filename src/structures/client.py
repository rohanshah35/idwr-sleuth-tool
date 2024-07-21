# Handles client data

class Client:
    def __init__(self, name, description, email, linkedin):
        self.name = name
        self.description = description
        self.email = email
        self.linkedin = linkedin

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "email": self.email,
            "linkedin": self.linkedin
        }

    def __str__(self):
        return f"Client(name={self.name}, email={self.email})"

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['description'], data['email'], data['linkedin'])