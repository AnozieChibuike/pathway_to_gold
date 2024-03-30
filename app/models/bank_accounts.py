from app import db
from app.models.baseModel import BaseModel

class BankAccount(BaseModel):
    account_number = db.Column(db.String(10),nullable=False)
    bank_code = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50))
    user_id = db.Column(db.String(126), db.ForeignKey('users.id'), nullable=False)