from app import db
from app.models.baseModel import BaseModel
from sqlalchemy.orm import Mapped

class BankAccount(BaseModel):
    account_number: Mapped[str] = db.Column(db.String(10),nullable=False)
    account_name: Mapped[str] = db.Column(db.String(50), nullable=False, default='')
    bank_code: Mapped[str] = db.Column(db.String(50), nullable=False)
    bank_name: Mapped[str] = db.Column(db.String(50))
    user_id: Mapped[str] = db.Column(db.String(126), db.ForeignKey('users.id'), nullable=False)