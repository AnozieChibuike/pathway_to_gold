from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.baseModel import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")

class Users(BaseModel):
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(120), index=True, unique=True)
    bio = db.Column(db.String(500), default="")
    password_hash = db.Column(db.String(1024))
    image_url = db.Column(db.String(500))
    email_verified = db.Column(db.Boolean, default=False)
    account_verified = db.Column(db.Boolean, default=False)
    pin = db.Column(db.String(4))
    bank_accounts = db.relationship('BankAccount', backref='user', lazy=True)
    balance = db.Column(db.Float, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

