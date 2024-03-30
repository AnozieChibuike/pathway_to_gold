from flask_mail import Message
from app import mail, app

DEFAULT_SENDER = app.config.get("MAIL_DEFAULT_SENDER")


def send_mail(
    subject: str,
    recipients: list,
    html: str = None,
    body: str = None,
    sender: str = DEFAULT_SENDER,
):
    try:
        msg = Message(subject, recipients=recipients)
        msg.body = body
        msg.html = html
        msg.sender = sender
        mail.send(msg)
        return {"message": "Email sent"}, 200, True
    except Exception as e:
        return {"message": "Email not sent {}".format(e)}, 400, False
