import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(
    receiver_email: str,
    subject: str,
    body: str,
):
    """
    Send Email Alert
    """

    if not EMAIL or not EMAIL_PASSWORD:
        return {
            "success": False,
            "message": "Email credentials not configured."
        }

    try:
        msg = MIMEMultipart()

        msg["From"] = EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
        )

        server.starttls()

        server.login(
            EMAIL,
            EMAIL_PASSWORD,
        )

        server.send_message(msg)

        server.quit()

        return {
            "success": True,
            "message": "Email sent successfully."
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }