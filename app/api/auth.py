from typing import Annotated
from app.api.dependencies import auth_service
from app.schemas.users import (
    TokenSchema,
    UserOutSchema,
    UserRegisterSchema,
)
from app.services.auth import AuthService
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

router = APIRouter(prefix="/auth", tags=["Authorization"],)


@router.post("/singup", response_model=UserOutSchema)
async def auth_singup(
    new_user: UserRegisterSchema,
    auth_service: Annotated[AuthService, Depends(auth_service)],
):
    try:
        user = await auth_service.singup(new_user)
        return user
    except AuthService.DataIsUsedException as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"This {e.data_type} is already used"
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
    except AuthService.UserNotFoundException as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"User with [{e.username}] not found"
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
