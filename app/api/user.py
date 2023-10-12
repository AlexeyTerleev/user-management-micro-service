from typing import Annotated

from app.api.dependencies import groups_service, users_service
from app.schemas.users import (
    GroupOutSchema,
    UserOutSchema,
    UserUpdateSchema,
    UserUpgradeSchema,
)
from app.services.groups import GroupsService
from app.services.users import UsersService
from app.utils.auth import get_hashed_password
from app.utils.oauth_bearer import get_current_unblocked_user
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

router = APIRouter(prefix="/user", tags=["User"],)


@router.get("/me", response_model=UserOutSchema)
async def me_get(user: Annotated[UserOutSchema, Depends(get_current_unblocked_user)],):
    try:
        return user
    except Exception as e:
        raise e


@router.patch("/me", response_model=UserOutSchema)
async def me_patch(
    new_values: UserUpdateSchema,
    user: Annotated[UserOutSchema, Depends(get_current_unblocked_user)],
    users_service: Annotated[UsersService, Depends(users_service)],
    groups_service: Annotated[GroupsService, Depends(groups_service)],
):
    try:

        if (
            new_values.username is not None
            and await users_service.get_user_by_username(new_values.username)
            is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with username [{new_values.username}] is already exist",
            )
        if (
            new_values.phone_number is not None
            and await users_service.get_user_by_phone_number(new_values.phone_number)
            is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with phone number [{new_values.phone_number}] is already exist",
            )
        if (
            new_values.email is not None
            and await users_service.get_user_by_email(new_values.email) is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email [{new_values.email}] is already exist",
            )

        update_dict = new_values.dict(exclude_unset=True)

        if (
            new_values.group_name is not None
            and new_values.group_name != user.group.name
        ):
            group = await groups_service.get_or_create_group(new_values.group_name)
            update_dict["group_id"] = group.id
        else:
            group = user.group

        update_dict.pop("group_name", None)

        if update_dict.get("password", None) is not None:
            update_dict["hashed_password"] = get_hashed_password(
                update_dict.pop("password")
            )
        if update_dict.get("img_path", None) is not None:
            update_dict["img_path"] = str(update_dict["img_path"])

        for key, value in user.dict().items():
            if value == update_dict.get(key, None):
                update_dict.pop(key)

        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No paramtrs to update",
            )

        updated_user = await users_service.update_user(
            user.id, UserUpgradeSchema(**update_dict)
        )
        return UserOutSchema(
            group=GroupOutSchema(**group.dict()), **updated_user.dict()
        )

    except Exception as e:
        raise e


@router.delete("/me", status_code=204)
async def me_delete(
    user: Annotated[UserOutSchema, Depends(get_current_unblocked_user)],
    users_service: Annotated[UsersService, Depends(users_service)],
):
    try:
        await users_service.delete_user_by_id(user.id)
    except Exception as e:
        raise e
