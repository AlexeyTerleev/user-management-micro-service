from datetime import datetime
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from pydantic import ValidationError

from app.api.dependencies import users_service
from app.config import settings
from app.schemas.users import TokenPayload, UserOutSchema
from app.services.users import UsersService

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="./auth/login", scheme_name="JWT")


async def get_current_user(
    users_service: Annotated[UsersService, Depends(users_service)],
    token: Annotated[str, Depends(reuseable_oauth)],
) -> UserOutSchema:
    try:
        payload = jwt.decode(
            token, settings.auth.jwt_secret_key, algorithms=[settings.auth.algorithm]
        )
        token_data = TokenPayload(**payload)
    except (jwt.exceptions.DecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = await users_service.get_user_by_id(token_data.sub)
    except Exception as e:
        raise e
    return user


async def get_current_unblocked_user(
    current_user: Annotated[UserOutSchema, Depends(get_current_user)]
) -> UserOutSchema:
    if current_user.blocked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user is blocked"
        )
    return current_user
