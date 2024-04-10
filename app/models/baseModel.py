from app import db
from datetime import datetime
import uuid
import pytz # type: ignore[import-untyped]
from flask import abort
from sqlalchemy.orm import Mapped
import typing

class BaseModel(db.Model): # type: ignore[name-defined]
    """
    BaseModel class
    Args:
        id: Random id for each table
        created_at: Represents the time each class was created
        updated_at: Represents the time each class was updated
    """
    __abstract__ = True
    id: Mapped[str] = db.Column(db.String(126), primary_key=True, unique=True, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, nullable=False)
    updated_at: Mapped[datetime] = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(pytz.timezone('Africa/Lagos'))
        self.updated_at = datetime.now(pytz.timezone('Africa/Lagos'))

    def save(self) -> None:
        """
        Saves the current session into the database
        """
        self.updated_at = datetime.now(pytz.timezone('Africa/Lagos'))
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        """
        Deletes the current session from the database
        """
        db.session.delete(self)
        db.session.commit()
    def close(self) -> None:
        db.session.remove()
    
    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the object.
        """
        attributes = {}
        for column in self.__table__.columns:
            attribute_name = column.name
            attribute_value = getattr(self, attribute_name)
            attributes[attribute_name] = attribute_value
        return attributes
    
    @classmethod
    def all(cls):
        """
        Retrieves all objects of the current model
        """
        return cls.query.all()
    
    @classmethod
    def get(cls,**kwargs):
        """
        Retrieve an object by its id or name or email or username.
        Returns the object if found, None otherwise.
        Usage:
            cls.get(name=<name>)
        """
        id = kwargs.get('id')
        email = kwargs.get('email')
        username = kwargs.get('username')
        phone = kwargs.get('phone') 
        if id:
            return cls.query.get(id)
        if email:
            return cls.query.filter_by(email=email).first()
        if username:
            return cls.query.filter_by(username=username).first()
        if phone:
            return cls.query.filter_by(phone=phone).first()
        return None
        
        
    @classmethod
    def get_or_404(cls,**kwargs):
        """
        Retrieve an object by its id or name or email or username.
        Returns the object if found, None otherwise.
        Usage:
            cls.get(name=<name>)
        """
        id = kwargs.get('id')
        email = kwargs.get('email')
        username = kwargs.get('username')
        phone = kwargs.get('phone') 
        if id:
            return cls.query.get(id) or abort(404, description="User with given ID not found")
        if email:
            return cls.query.filter_by(email=email).first() or abort(404, description="User with given email not found")
        if username:
            return cls.query.filter_by(username=username).first() or abort(404,description="User with given username not found")
        if phone:
            return cls.query.filter_by(phone=phone).first() or abort(404, description="User with given phone number not found")