from typing import Annotated

import jwt
import aio_pika
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.config import settings
from app.api.dependencies import auth_service
from app.schemas.users import (
    RefreshTokenSchema,
    TokenSchema,
    UserOutSchema,
    UserRegisterSchema,
)
from app.services.auth import AuthService
from app.services.rabbit_mq import RabbitMQService
from app.services.users import UsersService
from app.utils.oauth_bearer import get_current_unblocked_user

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)


@router.post("/singup", response_model=UserOutSchema)
async def auth_singup(
    new_user: UserRegisterSchema,
    auth_service: Annotated[AuthService, Depends(auth_service)],
):
    try:
        user = await auth_service.singup(new_user)
        return user
    except UsersService.UserExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e.idtf} [{e.value}] is already used",
        )
    except Exception as e:
        raise e


@router.post("/login", response_model=TokenSchema)
async def auth_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(auth_service)],
):
    try:
        tokens = await auth_service.login(form_data)
        return tokens
    except UsersService.UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with {e.idtf} [{e.value}] not found",
        )
    except AuthService.IncorrectPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Incorrect password"
        )
    except Exception as e:
        raise e


@router.post("/refresh-token", response_model=TokenSchema)
async def auth_refresh_token(
    refresh_token: RefreshTokenSchema,
    auth_service: Annotated[AuthService, Depends(auth_service)],
):
    try:
        tokens = await auth_service.refresh_tokens(refresh_token.refresh_token)
        return tokens
    except jwt.exceptions.DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise e


@router.post("/reset-password", status_code=204)
async def auth_reset_password(
    user: Annotated[UserOutSchema, Depends(get_current_unblocked_user)],
    rabbit_mq_service: Annotated[RabbitMQService, Depends(RabbitMQService)],
):
    url = "reset_password_url"
    try:
        await rabbit_mq_service.send_reset_password_message(user.email, url)
    except Exception as e:
        raise e
