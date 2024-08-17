# Supports email integration

import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailHandler:
    def __init__(self, email_address, password):
        self._email_address = email_address
        self._password = password
        self._imap_server = None
        self._smtp_server = None

    # Getters
    def get_email_address(self):
        return self._email_address

    def get_password(self):
        return self._password

    def get_imap_server(self):
        return self._imap_server

    def get_smtp_server(self):
        return self._smtp_server

    # Setters
    def set_email_address(self, email_address):
        self._email_address = email_address

    def set_password(self, password):
        self._password = password

    def set_imap_server(self, imap_server):
        self._imap_server = imap_server

    def set_smtp_server(self, smtp_server):
        self._smtp_server = smtp_server

    # Initializes the IMAP server and logs in
    def initialize_imap(self):
        try:
            self._imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
            self._imap_server.login(self._email_address, self._password)
        except imaplib.IMAP4.error:
            raise Exception("Invalid email credentials for IMAP, please try again.")

    # Initializes the SMTP server and logs in
    def initialize_smtp(self):
        try:
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(self._email_address, self._password)
            self._smtp_server = smtp_server
        except smtplib.SMTPAuthenticationError:
            raise Exception("Invalid email credentials for SMTP, please try again.")

    # Sends an email to the specified recipient
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

    # Searches for unseen emails from specified clients
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

    # Searches for unseen emails from a specific sender
    def search_mailbox_for_unseen(self, sender_email):
        if not self._imap_server:
            self.initialize_imap()

        self._imap_server.select('INBOX')
        _, message_numbers = self._imap_server.search(None, f'UNSEEN FROM "{sender_email}"')
        return message_numbers[0].split()
