from flask_mail import Message # type: ignore[import-untyped]
from app import mail, app
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SENDER_MAIL: str | None = os.getenv("EMAIL_FROM")
DEFAULT_SENDER_NAME: str | None = os.getenv("EMAIL_NAME")


def send_mail(
    subject: str,
    recipient: str,
    html: str | None = '',
    body: str | None = '',
    image =  None
) -> tuple[str,int,bool]:
    try:
        msg: Message = Message(subject, recipients=[recipient])
        msg.body = body
        msg.html = html
        msg.sender = (DEFAULT_SENDER_NAME,DEFAULT_SENDER_MAIL)
        if image:
            with app.open_resource(image) as f:
                msg.attach(image, "image/png")
        mail.send(msg)
        return "Email sent", 200, True
    except Exception as e:
        return "Email not sent {}".format(e), 400, False
