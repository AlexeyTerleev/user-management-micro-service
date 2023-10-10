
import jwt
from datetime import datetime
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
import jwt

from app.config import settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_token(key: str, subject: Union[str, Any], expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow()
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.auth.access_token_expire_minutes)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, key, settings.auth.algorithm)
    return encoded_jwt


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return create_token(settings.auth.jwt_secret_key, subject, expires_delta)


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return create_token(settings.auth.jwt_refresh_secret_key, subject, expires_delta)


