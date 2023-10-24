from typing import Annotated
from app.api.dependencies import auth_service
from app.schemas.users import (
    TokenSchema,
    UserOutSchema,
    UserRegisterSchema,
)
from app.utils.oauth_bearer import refresh_oauth
from app.services.auth import AuthService
from app.services.users import UsersService
from app.utils.oauth_bearer import get_current_unblocked_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from pydantic import EmailStr
import jwt


router = APIRouter(prefix="/auth", tags=["Authorization"],)


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
                detail=f"{e.idtf} [{e.value}] is already used"
            )
    except HTTPException as e:
        raise e
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
                detail=f"User with {e.idtf} [{e.value}] not found"
            )
    except AuthService.IncorrectPasswordException as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Incorrect password"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    

@router.post("/refresh-token", response_model=TokenSchema)
async def auth_refresh_token(
    refresh_token: str,
    auth_service: Annotated[AuthService, Depends(auth_service)],
):
    try:
        tokens = await auth_service.refresh_tokens(refresh_token)
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


@router.post("/reset-password", response_model=TokenSchema)
async def auth_reset_password(
    email: EmailStr,
    auth_service: Annotated[AuthService, Depends(auth_service)],
):
    try:
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
