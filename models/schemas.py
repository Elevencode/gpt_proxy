from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    id = Column(String, primary_key=True)
    telegram_id = Column(String, unique=True, index=True, nullable=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    tokens_used = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="user")

class Message(Base):
    __tablename__ = 'Messages'

    id = Column(String, primary_key=True)
    text = Column(String)
    user_id = Column(String, ForeignKey('Users.id'))
    source = Column(String)
    related_message_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    channel_id = Column(String)

    user = relationship("User", back_populates="messages")