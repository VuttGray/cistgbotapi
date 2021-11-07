from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from cistgbotapi.hashing import Hash
from cistgbotapi._token import create_access_token
from cistgbotapi import database, models

router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    print(f'User: {user}')
    if not user or not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
