from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from cistgbotapi.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    recipient_name = Column(String, ForeignKey('users.name'))
    message = Column(String)
    created = Column(DateTime)
    sent = Column(DateTime, nullable=True)
    last_attempted = Column(DateTime, nullable=True)
    attempts = Column(Integer, default=0)

    recipient = relationship("User", back_populates="messages")


class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True)
    password = Column(String)
    tg_chat_id = Column(Integer, nullable=True)

    messages = relationship("Message", back_populates="recipient")
