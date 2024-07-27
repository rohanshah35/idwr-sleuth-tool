import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailHandler:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.imap_server = None
        self.smtp_server = None

    def initialize_imap(self):
        try:
            self.imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
            self.imap_server.login(self.email_address, self.password)
            print("successfully logged in")
        except imaplib.IMAP4.error:
            raise Exception("Invalid email credentials for IMAP, please try again.")

    def initialize_smtp(self):
        try:
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(self.email_address, self.password)
            self.smtp_server = smtp_server  # Only store if login is successful
        except smtplib.SMTPAuthenticationError:
            raise Exception("Invalid email credentials for SMTP, please try again.")

    def send_email(self, recipient_email, subject, body):
        if not self.smtp_server:
            self.initialize_smtp()

        message = MIMEMultipart()
        message['From'] = self.email_address
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        text = message.as_string()
        self.smtp_server.sendmail(self.email_address, recipient_email, text)

    def search_mailbox(self, sender_email):
        if not self.imap_server:
            self.initialize_imap()

        self.imap_server.select('INBOX')
        _, message_numbers = self.imap_server.search(None, f'FROM "{sender_email}"')
        return message_numbers[0].split()

    def get_email_content(self, email_id):
        if not self.imap_server:
            self.initialize_imap()

        _, msg_data = self.imap_server.fetch(email_id, '(RFC822)')
        email_body = msg_data[0][1]
        email_message = email.message_from_bytes(email_body)

        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    return email_message, part.get_payload(decode=True).decode()
        else:
            return email_message, email_message.get_payload(decode=True).decode()

    def close_connections(self):
        if self.imap_server:
            try:
                self.imap_server.logout()
            except:
                pass  # Ignore errors during IMAP logout
        if self.smtp_server:
            try:
                self.smtp_server.quit()
            except:
                pass  # Ignore errors during SMTP quit



if __name__ == "__main__":
    email_address = '@gmail.com'
    password = ''
    sender_email = ""

    try:
        email_handler = EmailHandler(email_address, password)

        print("Initializing email connections...")
        email_handler.initialize_imap()
        email_handler.initialize_smtp()
        print("Email connections successful")

        # Search for emails from the specified sender
        message_ids = email_handler.search_mailbox(sender_email)

        for email_id in message_ids:
            email_content, email_body = email_handler.get_email_content(email_id)
            print(f"Subject: {email_content['Subject']}")
            print(f"From: {email_content['From']}")
            print(f"Date: {email_content['Date']}")
            print("Content:")
            print(email_body)
            print("--------------------")

        # Example: Send an email
        email_handler.send_email('recipient@example.com', 'Test Subject', 'This is a test email.')
        print("Email sent successfully")

    except Exception as e:
        print(f"Error: {str(e)}")
