from datetime import timedelta, datetime, timezone

import jwt
from jwt import InvalidTokenError

from configs.app_config import TOKEN_SECRET_KEY, TOKEN_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from services.security.exceptions import credentials_exception


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creates and returns a new access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """Returns decoded token, otherwise raises credentials_exception"""
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception
    return payload
