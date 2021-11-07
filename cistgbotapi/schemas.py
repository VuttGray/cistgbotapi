from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    tg_chat_id: int
    password: str


class Message(BaseModel):
    recipient_name: str
    message: str
    created: Optional[datetime]
    sent: Optional[datetime]
    last_attempted: Optional[datetime]
    attempts: Optional[int]


class ShortMessages(BaseModel):
    message: str
    created: Optional[datetime]

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowMessage(BaseModel):
    id: int
    created: Optional[datetime]
    sent: Optional[datetime]
    message: str
    recipient_name: str
    recipient: ShowUser

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
