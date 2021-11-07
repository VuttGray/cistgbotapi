from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import cistgbotapi.repository.user as rep
from cistgbotapi import schemas, oauth2
from cistgbotapi.database import get_db

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.get("/", response_model=List[schemas.ShowUser])
def get_all(db: Session = Depends(get_db),
            current_user: schemas.User = Depends(oauth2.get_current_user)):
    return rep.get_all(db)


@router.get("/{user_name}", response_model=schemas.ShowUser)
def get(user_name: str, db: Session = Depends(get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    return rep.get(user_name, db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create(request: schemas.User, db: Session = Depends(get_db)):
    return rep.create(request, db)
