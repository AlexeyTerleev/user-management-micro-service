import re
from typing import Annotated

from app.api.dependencies import groups_service, users_service
from app.schemas.groups import GroupOutSchema
from app.schemas.users import (
    TokenSchema,
    UserCreateSchema,
    UserOutSchema,
    UserRegisterSchema,
)
from app.services.groups import GroupsService
from app.services.users import UsersService
from app.utils.auth import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

router = APIRouter(prefix="/auth", tags=["Authorization"],)


@router.post("/singup", response_model=UserOutSchema)
async def auth_singup(
    new_user: UserRegisterSchema,
    users_service: Annotated[UsersService, Depends(users_service)],
    groups_service: Annotated[GroupsService, Depends(groups_service)],
):
    try:
        if await users_service.get_user_by_username(new_user.username) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with username [{new_user.username}] is already exist",
            )
        if (
            await users_service.get_user_by_phone_number(new_user.phone_number)
            is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with phone number [{new_user.phone_number}] is already exist",
            )
        if await users_service.get_user_by_email(new_user.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email [{new_user.email}] is already exist",
            )

        group = await groups_service.get_or_create_group(new_user.group_name)

        new_user_dict = new_user.dict()
        new_user_dict["hashed_password"] = get_hashed_password(
            new_user_dict.pop("password")
        )
        new_user_dict["img_path"] = str(new_user_dict["img_path"])
        new_user_dict["group_id"] = group.id

        user = await users_service.create_user(UserCreateSchema(**new_user_dict))

        return UserOutSchema(group=GroupOutSchema(**group.dict()), **user.dict())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.post("/login", response_model=TokenSchema)
async def auth_login(
    users_service: Annotated[UsersService, Depends(users_service)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        if is_phone_number(form_data.username):
            username_type = "phone number"
            user = await users_service.get_user_by_phone_number(form_data.username)
        elif is_email(form_data.username):
            username_type = "email"
            user = await users_service.get_user_by_email(form_data.username)
        else:
            username_type = "username"
            user = await users_service.get_user_by_username(form_data.username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with {username_type} [{form_data.username}] not found",
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


def is_phone_number(filter_value: str) -> bool:
    regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
    return bool(re.match(regex, filter_value))


def is_email(filter_value: str) -> bool:
    regex = r"^[^@]+@[^@]+\.[^@]+$"
    return bool(re.match(regex, filter_value))
