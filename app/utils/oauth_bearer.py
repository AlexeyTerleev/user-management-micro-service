from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Annotated
from pydantic import ValidationError
from datetime import datetime
import jwt 

from app.schemas.users import UserSchema, TokenPayload
from app.services.users import UsersService
from app.api.dependencies import users_service
from app.config import settings


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="./auth/login",
    scheme_name="JWT"
)

async def get_current_user(
        users_service: Annotated[UsersService, Depends(users_service)],
        token: Annotated[str, Depends(reuseable_oauth)],
        ) -> UserSchema:
    try:
        payload = jwt.decode(token, settings.auth.jwt_secret_key, algorithms=[settings.auth.algorithm])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = await users_service.get_user({"id" : token_data.sub})
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user