from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from datetime import datetime # Import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    
    # Required attributes
    body = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    
    # DateTime attributes with default values
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Add serialization rules if using SQLAlchemy-serializer (optional but helpful)
    # serialize_rules = () 

    def __repr__(self):
        return f'<Message {self.id}: {self.username}>'