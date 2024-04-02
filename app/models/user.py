from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.baseModel import BaseModel
import os
from dotenv import load_dotenv
from lib.utils.tokens import *

load_dotenv()

base_url = os.getenv("BASE_URL")


class Users(BaseModel):
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(120), index=True, unique=True)
    bio = db.Column(db.String(500), default="")
    phone = db.Column(db.String(11), nullable=False, unique=True)
    password_hash = db.Column(db.String(1024))
    image_url = db.Column(db.String(500))
    email_verified = db.Column(db.Boolean, default=False)
    account_verified = db.Column(db.Boolean, default=False)
    pin = db.Column(db.String(4))
    bank_accounts = db.relationship("BankAccount", backref="user", lazy=True)
    balance = db.Column(db.Float, default=0)
    otp_token = db.Column(db.String(50))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_otp(self, otp: str):
        if not self.otp_token:
            return "User has not requested OTP", False, 400
        data, code, status = verify_token(self.otp_token)
        if not status:
            return data, False, code
        payload = data["payload"]
        print(payload)
        if payload["otp"] != otp:
            return "Invalid OTP", False, 400
        self.otp_token = None
        self.email_verified = True
        self.save()
        return "OTP verified", True, 200

    def __repr__(self):
        return f"<User {self.username}>"
