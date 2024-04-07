from flask_mail import Message
from app import mail, app

DEFAULT_SENDER_MAIL = app.config.get("MAIL_DEFAULT_SENDER")
DEFAULT_SENDER_NAME = app.config.get("MAIL_DEFAULT_SENDER_NAME")


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
        msg.sender = sender
        mail.send(msg)
        return "Email sent", 200, True
    except Exception as e:
        return "Email not sent {}".format(e), 400, False
