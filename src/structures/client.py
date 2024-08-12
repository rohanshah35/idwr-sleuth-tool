# Handles client data
from src.auth.linkedin_handler import LinkedInHandler


class Client:
    def __init__(self, name, description, company, linkedin, email, anonymous=None, linkedin_name=None):
        self.name = name
        self.description = description
        self.company = company
        self.linkedin = linkedin
        self.email = email
        self.message_thread = []
        self.last_sender = None
        self.anonymous = anonymous
        self.linkedin_name = linkedin_name

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_company(self):
        return self.company

    def get_linkedin(self):
        return self.linkedin

    def get_email(self):
        return self.email

    def get_anonymous(self):
        return self.anonymous

    def get_linkedin_name(self):
        return self.linkedin_name

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_company(self, company):
        self.company = company

    def set_linkedin(self, linkedin):
        self.linkedin = linkedin

    def set_email(self, email):
        self.email = email

    def set_anonymous(self, anonymous):
        self.anonymous = anonymous

    def set_linkedin_name(self, linkedin_name):
        self.linkedin_name = linkedin_name

    def load_linkedin_conversation(self, linkedin_handler):
        uncleaned_message_thread = linkedin_handler.get_conversation_text(self.get_name())
        for i, message in enumerate(uncleaned_message_thread, 0):
            self.message_thread.append(self.message_to_dict(i, message))

    def message_to_dict(self, index, message):
        split_sender_and_message_body = message.split(':', 1) # splits by : 1 time
        print(split_sender_and_message_body)
        message = {}
        try:
            message_body = split_sender_and_message_body[1]
            self.last_sender = split_sender_and_message_body[0]
        except IndexError:
            message_body = split_sender_and_message_body[0]

        message["id"] = index
        message["sender"] = self.last_sender
        message["body"] = message_body
        return message

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "company": self.company,
            "email": self.email,
            "linkedin": self.linkedin,
            "message_thread": self.message_thread,
            "anonymous": self.anonymous,
            "linkedin_name": self.linkedin_name
        }

    def __str__(self):
        return f"Client(name={self.name}, email={self.email})"

    @classmethod
    def from_dict(cls, data):
        client = cls(data["name"], data["description"], data["company"], data["linkedin"], data["email"], data["anonymous"], data["linkedin_name"])
        client.message_thread = data.get("message_thread", [])
        return client

def main():
    # LinkedIn credentials
    linkedin_username = ""
    linkedin_password = ""

    # Recipient's full name as it appears on LinkedIn
    recipient_name = "Luca Bianchini"
    client = Client("Luca Bianchini", "Bob's name", "flsdjkflsdjf", "kldskfkldsklf")

    try:
        # Create LinkedInHandler instance
        linkedin_handler = LinkedInHandler(linkedin_username, linkedin_password)

        print("Logging in to LinkedIn...")
        if linkedin_handler.login_to_linkedin_headless():
            print("Login successful!")

            print(f"Attempting to view conversation with {recipient_name}...")
            client.load_linkedin_conversation(linkedin_handler)

            #test encoding and decoding
            data = client.to_dict()
            print(data)
            client_from_dict = Client.from_dict(data)
            print(client_from_dict.to_dict())
        else:
            print("Failed to log in to LinkedIn.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if linkedin_handler:
            print("Closing browser...")
            linkedin_handler.quit()

if __name__ == "__main__":
    main()