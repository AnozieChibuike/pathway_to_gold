from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.baseModel import BaseModel
import os
from dotenv import load_dotenv
from lib.utils.tokens import *
from sqlalchemy.orm import Mapped
import pyotp

load_dotenv()

base_url = os.getenv("BASE_URL")


class Users(BaseModel):
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    fullname: Mapped[str] = db.Column(db.String(50), nullable=False)
    email: Mapped[str] = db.Column(db.String(120), index=True, unique=True)
    username: Mapped[str] = db.Column(db.String(120), index=True, unique=True)
    bio: Mapped[str] = db.Column(db.String(500), default="")
    phone: Mapped[str] = db.Column(db.String(11), nullable=False, unique=True)
    password_hash: Mapped[str] = db.Column(db.String(1024))
    image_url: Mapped[str] = db.Column(db.String(500))
    email_verified: Mapped[bool] = db.Column(db.Boolean, default=False)
    phone_verified: Mapped[bool] = db.Column(db.Boolean, default=False)
    account_verified: Mapped[bool] = db.Column(db.Boolean, default=False)
    pin: Mapped[str] = db.Column(db.String(4))
    bank_accounts = db.relationship("BankAccount", backref="user", lazy=True, cascade='all, delete-orphan', passive_deletes=True)
    balance: Mapped[float] = db.Column(db.Float, default=0)
    otp_token: Mapped[str] = db.Column(db.String(126))
    totp_secret: Mapped[str] = db.Column(db.String(126), default=pyotp.random_base32())

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def verify_otp(self, otp: str) -> tuple[str, bool, int]:
        if not self.otp_token:
            return "User has not requested OTP", False, 400
        data, code, status = verify_token(self.otp_token)
        if not status:
            return data['reason'], False, code
        payload = data["payload"]
        if payload["otp"] != otp:
            return "Invalid OTP", False, 400
        self.otp_token = ''
        self.email_verified = True
        self.save()
        return "OTP verified", True, 200

    def __repr__(self):
        return f"<User {self.username}>"
