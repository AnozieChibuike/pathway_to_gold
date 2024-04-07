import os
from dotenv import load_dotenv
import secrets

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET", secrets.token_hex())
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('EMAIL_SERVER_HOST','smtp.gmail.com')
    MAIL_PORT=465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME=os.getenv('EMAIL_SERVER_USER')
    MAIL_PASSWORD=os.getenv('EMAIL_SERVER_PASSWORD')
    MAIL_DEFAULT_SENDER=os.getenv('EMAIL_FROM')
    MAIL_DEFAULT_SENDER_NAME=os.getenv('EMAIL_NAME')
