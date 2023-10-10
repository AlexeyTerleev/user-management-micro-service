from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import Annotated

from app.schemas.users import UserRegisterSchema,  UserCreateSchema
from app.api.dependencies import users_service, groups_service
from app.services.users import UsersService
from app.services.groups import GroupsService
from app.utils.auth import verify_password, create_access_token, create_refresh_token


router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)


@router.post("/singup")
async def auth_singup(
    new_user: UserRegisterSchema,
    users_service: Annotated[UsersService, Depends(users_service)],
    groups_service: Annotated[GroupsService, Depends(groups_service)]
    ):
    try:
        group = await groups_service.get_or_create_group(new_user.group_name)
        user = await users_service.create_user(UserCreateSchema(group_id=group.id, **dict(new_user)))
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.post("/login")
async def auth_login(
    users_service: Annotated[UsersService, Depends(users_service)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ):
    try:
        try: 
            user = await users_service.get_user({"username" : form_data.username})
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect login"
            )
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )
        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e

