from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from cistgbotapi.hashing import Hash
from cistgbotapi.schemas import User
from cistgbotapi import models
from cistgbotapi.database import add_record_in_db


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def get(user_name: str, db: Session):
    user = db.query(models.User).filter(models.User.name == user_name or models.User.email == user_name).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with name {user_name} does not exist")
    return user


def create(request: User, db: Session):
    new_record = models.User(name=request.name,
                             email=request.email,
                             tg_chat_id=request.tg_chat_id,
                             password=Hash.bcrypt(request.password))
    return add_record_in_db(new_record, db)
