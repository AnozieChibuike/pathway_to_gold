from flask_mail import Message
from app import mail, app
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SENDER_MAIL = os.getenv("EMAIL_FROM")
DEFAULT_SENDER_NAME = os.getenv("EMAIL_NAME")


def send_mail(
    subject: str,
    recipient: str,
    html: str = None,
    body: str = None,
    sender: tuple = (DEFAULT_SENDER_NAME,DEFAULT_SENDER_MAIL),
):
    try:
        msg = Message(subject, recipients=[recipient])
        msg.body = body
        msg.html = html
        msg.sender = (DEFAULT_SENDER_NAME,DEFAULT_SENDER_MAIL)
        mail.send(msg)
        return "Email sent", 200, True
    except Exception as e:
        return "Email not sent {}".format(e), 400, False
