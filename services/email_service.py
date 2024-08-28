# services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings
import logging
from typing import List


def send_email(receiver_email: str, subject: str, body: str):
    message = MIMEMultipart()
    message["From"] = settings.SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SENDER_EMAIL, settings.SENDER_PASSWORD)
            server.sendmail(settings.SENDER_EMAIL, receiver_email, message.as_string())
        logging.info(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        logging.error(f"Failed to send email to {receiver_email}: {e}")

def send_welcome_email(user_email: str, subscribed_channels: List[str]):
    subject = "Welcome to YouTube Channel Summary Service"
    body = f"Welcome to our YouTube Channel Summary Service!\n\n"
    body += "You have successfully subscribed to the following channels:\n"
    for channel in subscribed_channels:
        body += f"- {channel}\n"
    body += "\nYou will receive weekly summaries of the latest videos from these channels every Monday at 9:00 AM.\n"
    body += "\nThank you for using our service!"

    send_email(user_email, subject, body)