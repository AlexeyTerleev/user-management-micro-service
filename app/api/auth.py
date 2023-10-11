import re
from typing import Annotated

from app.api.dependencies import groups_service, users_service
from app.schemas.users import UserCreateSchema, UserRegisterSchema
from app.services.groups import GroupsService
from app.services.users import UsersService
from app.utils.auth import create_access_token, create_refresh_token, verify_password
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

router = APIRouter(prefix="/auth", tags=["Authorization"],)


@router.post("/singup")
async def auth_singup(
    new_user: UserRegisterSchema,
    users_service: Annotated[UsersService, Depends(users_service)],
    groups_service: Annotated[GroupsService, Depends(groups_service)],
):
    try:
        if await users_service.get_user({"username": new_user.username}) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with username [{new_user.username}] is already exist",
            )
        if (
            await users_service.get_user({"phone_number": new_user.phone_number})
            is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with phone number [{new_user.phone_number}] is already exist",
            )
        if await users_service.get_user({"email": new_user.email}) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email [{new_user.email}] is already exist",
            )
        group = await groups_service.get_or_create_group(new_user.group_name)
        user = await users_service.create_user(
            UserCreateSchema(group_id=group.id, **dict(new_user))
        )
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
        filter_name = get_filter_name(form_data.username)
        user = await users_service.get_user({filter_name: form_data.username})

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with {filter_name.replace('_', ' ')} [{form_data.username}] not found",
            )
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )
        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


def get_filter_name(filter_value):
    filter_name = "username"
    if is_phone_number(filter_value):
        filter_name = "phone_number"
    elif is_email(filter_value):
        filter_name = "email"
    return filter_name


def is_phone_number(filter_value: str) -> bool:
    regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
    return bool(re.match(regex, filter_value))


def is_email(filter_value: str) -> bool:
    regex = r"^[^@]+@[^@]+\.[^@]+$"
    return bool(re.match(regex, filter_value))
