from datetime import datetime
from fastapi import status, HTTPException, Response
from sqlalchemy.orm import Session

from cistgbotapi import schemas
from cistgbotapi import models
from cistgbotapi.database import add_record_in_db


def __get_query(message_id: int, db: Session) -> models.Message:
    message = db.query(models.Message).filter(models.Message.id == message_id)
    if not message.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Message with id {message_id} does not exist")
    return message


def get_all(db: Session):
    messages = db.query(models.Message).all()
    return messages


def get_to_sent(db: Session):
    messages = db.query(models.Message).filter(models.Message.sent == None).all()
    return messages


def create(data: schemas.Message | models.Message,
           db: Session):
    if isinstance(data, models.Message):
        new_record = data
    else:
        new_record = models.Message(recipient_name=data.recipient_name,
                                    message=data.message,
                                    created=datetime.now())
    return add_record_in_db(new_record, db)


def get(message_id: int,
        db: Session):
    return __get_query(message_id, db).first()


def sent(message_id: int,
         db: Session):
    message = __get_query(message_id, db)
    message.update({'sent': datetime.now()})
    db.commit()


def update(message_id: int,
           data: schemas.Message,
           db: Session):
    message = __get_query(message_id, db)
    message.update(data.dict())
    db.commit()
    return message.first()


def delete(message_id: int,
           db: Session):
    message = __get_query(message_id, db)
    message.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
