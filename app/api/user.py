from typing import Annotated

from app.api.dependencies import groups_service, users_service
from app.schemas.users import (
    GroupOutSchema,
    UserOutSchema,
    UserUpdateSchema,
)
from app.services.groups import GroupsService
from app.services.users import UsersService
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
        updated_group = await groups_service.update_group(user.group, new_values.group_name)
        updated_user = await users_service.update_user(user, new_values, updated_group)
        return UserOutSchema(group=GroupOutSchema(**updated_group.dict()), **updated_user.dict())
    except UsersService.UserExistsException as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"{e.idtf} [{e.value}] is already used"
            )
    except UsersService.NothingToUpdateException:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"No changes avalible"
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
