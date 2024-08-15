import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailHandler:
    def __init__(self, email_address, password):
        self._email_address = email_address
        self._password = password
        self._imap_server = None
        self._smtp_server = None

        def get_email_address(self):
            return self._email_address

    def set_email_address(self, email_address):
        self._email_address = email_address

    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def get_imap_server(self):
        return self._imap_server

    def set_imap_server(self, imap_server):
        self._imap_server = imap_server

    def get_smtp_server(self):
        return self._smtp_server

    def set_smtp_server(self, smtp_server):
        self._smtp_server = smtp_server


    def initialize_imap(self):
        try:
            self._imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
            self._imap_server.login(self._email_address, self._password)
        except imaplib.IMAP4.error:
            raise Exception("Invalid email credentials for IMAP, please try again.")

    def initialize_smtp(self):
        try:
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(self._email_address, self._password)
            self._smtp_server = smtp_server  # Only store if login is successful
        except smtplib.SMTPAuthenticationError:
            raise Exception("Invalid email credentials for SMTP, please try again.")

    def send_email(self, recipient_email, subject, body):
        if not self._smtp_server:
            self.initialize_smtp()

        message = MIMEMultipart()
        message['From'] = self._email_address
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        text = message.as_string()
        self._smtp_server.sendmail(self._email_address, recipient_email, text)

    def search_mailbox_for_unseen_emails_from_clients(self, clients):
        if not self._imap_server:
            self.initialize_imap()

        clients_with_new_mail = []

        for client in clients:
            client_email = client.get_email()
            if not client_email:
                print(f"Skipping client {client.get_name()} - No email provided.")
                continue
            unseen_mail_from_client = self.search_mailbox_for_unseen(client_email)
            if unseen_mail_from_client:
                clients_with_new_mail.append(client)
                print(f"New message detected from {client.get_name()}")

        return clients_with_new_mail

    def search_mailbox(self, sender_email):
        if not self._imap_server:
            self.initialize_imap()

        self._imap_server.select('INBOX')
        _, message_numbers = self._imap_server.search(None, f'FROM "{sender_email}"')
        return message_numbers[0].split()

    def search_mailbox_for_unseen(self, sender_email):
        if not self._imap_server:
            self.initialize_imap()

        self._imap_server.select('INBOX')
        _, message_numbers = self._imap_server.search(None, f'UNSEEN FROM "{sender_email}"')
        return message_numbers[0].split()

    def get_email_content(self, email_id):
        if not self._imap_server:
            self.initialize_imap()

        _, msg_data = self._imap_server.fetch(email_id, '(RFC822)')
        email_body = msg_data[0][1]
        email_message = email.message_from_bytes(email_body)

        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    return email_message, part.get_payload(decode=True).decode()
        else:
            return email_message, email_message.get_payload(decode=True).decode()

    def close_connections(self):
        if self._imap_server:
            try:
                self._imap_server.logout()
            except:
                pass  # Ignore errors during IMAP logout
        if self._smtp_server:
            try:
                self._smtp_server.quit()
            except:
                pass  # Ignore errors during SMTP quit
