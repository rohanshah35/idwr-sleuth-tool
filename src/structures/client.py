# Client data structure

from datetime import date


class Client:
    def __init__(self, name, description, company, linkedin, email, anonymous=None, linkedin_name=None, date_created=None, has_responded=None):
        self.__name = name
        self.__description = description
        self.__company = company
        self.__linkedin = linkedin
        self.__email = email
        self.__message_thread = []
        self.__last_sender = None
        self.__anonymous = anonymous
        self.__linkedin_name = linkedin_name
        self.__date_created = date.today() if not date_created else date_created
        self.__has_responded = has_responded

    # Getters
    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_company(self):
        return self.__company

    def get_linkedin(self):
        return self.__linkedin

    def get_email(self):
        return self.__email

    def get_message_thread(self):
        return self.__message_thread

    def get_last_sender(self):
        return self.__last_sender

    def get_anonymous(self):
        return self.__anonymous

    def get_linkedin_name(self):
        return self.__linkedin_name

    def get_date_created(self):
        return self.__date_created

    def get_date_created_iso(self):
        return self.__date_created.isoformat()

    def get_has_responded(self):
        return self.__has_responded

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_company(self, company):
        self.__company = company

    def set_linkedin(self, linkedin):
        self.__linkedin = linkedin

    def set_email(self, email):
        self.__email = email

    def set_message_thread(self, message_thread):
        self.__message_thread = message_thread

    def set_last_sender(self, last_sender):
        self.__last_sender = last_sender

    def set_anonymous(self, anonymous):
        self.__anonymous = anonymous

    def set_linkedin_name(self, linkedin_name):
        self.__linkedin_name = linkedin_name

    def set_date_created(self, date_created):
        self.__date_created = date_created

    def set_has_responded(self, has_responded):
        self.__has_responded = has_responded

    # Conversation loading
    def load_linkedin_conversation(self, linkedin_handler):
        uncleaned_message_thread = linkedin_handler.get_conversation_text(self.get_name())
        for i, message in enumerate(uncleaned_message_thread, 0):
            self.__message_thread.append(self.__message_to_dict(i, message))

    # Serialization methods
    def __message_to_dict(self, index, message):
        split_sender_and_message_body = message.split(':', 1)
        message = {}
        try:
            message_body = split_sender_and_message_body[1]
            self.__last_sender = split_sender_and_message_body[0]
        except IndexError:
            message_body = split_sender_and_message_body[0]

        message["id"] = index
        message["sender"] = self.__last_sender
        message["body"] = message_body
        return message

    def to_dict(self):
        return {
            "name": self.__name,
            "description": self.__description,
            "company": self.__company,
            "email": self.__email,
            "linkedin": self.__linkedin,
            "message_thread": self.__message_thread,
            "anonymous": self.__anonymous,
            "linkedin_name": self.__linkedin_name,
            "date_created": self.__date_created.isoformat(),
            "has_responded": self.__has_responded
        }

    def __str__(self):
        return f"Client(name={self.__name}, email={self.__email})"

    @classmethod
    def from_dict(cls, data):
        date_created = date.fromisoformat(data["date_created"])

        client = cls(
            data["name"],
            data["description"],
            data["company"],
            data["linkedin"],
            data["email"],
            data["anonymous"],
            data["linkedin_name"],
            date_created,
            data["has_responded"]
        )
        client.set_message_thread(data.get("message_thread", []))
        return client