from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError

from cistgbotapi import schemas
from cistgbotapi.config import settings


class ApiConfig:
    def __init__(self, **kwargs):
        self.secret_key = kwargs.pop('secret_key')
        self.algorithm = kwargs.pop('algorithm')
        self.access_token_expire_minutes = kwargs.pop('access_token_expire_minutes', 30)


conf: ApiConfig = ApiConfig(**settings.default.tgbotapi)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire_period = expires_delta if expires_delta else timedelta(minutes=conf.access_token_expire_minutes)
    to_encode.update({"exp": datetime.utcnow() + expire_period})
    encoded_jwt = jwt.encode(to_encode, conf.secret_key, algorithm=conf.algorithm)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, conf.secret_key, algorithms=[conf.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data
