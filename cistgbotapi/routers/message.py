from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import cistgbotapi.repository.message as rep
from cistgbotapi import oauth2, schemas
from cistgbotapi.database import get_db

router = APIRouter(
    prefix="/message",
    tags=['Messages']
)


@router.get("/", response_model=List[schemas.ShowMessage])
def get_all(db: Session = Depends(get_db),
            current_user: schemas.User = Depends(oauth2.get_current_user)):
    return rep.get_all(db)


@router.get("/{message_id}", response_model=schemas.ShowMessage)
def get(message_id: int, db: Session = Depends(get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    return rep.get(message_id, db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowMessage)
def create(request: schemas.Message, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return rep.create(request, db)


@router.put("/{message_id}", status_code=status.HTTP_202_ACCEPTED)
def update(message_id: int, request: schemas.Message, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return rep.update(message_id, request, db)


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(message_id: int, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return rep.delete(message_id, db)
