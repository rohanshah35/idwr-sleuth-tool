# Email functionality
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Functionality to send email
def send_email(sender_email, sender_password, recipient_email, subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)


sender_email = ""
sender_password = ""
recipient_email = ""
subject = ""
body = ""

send_email(sender_email, sender_password, recipient_email, subject, body)