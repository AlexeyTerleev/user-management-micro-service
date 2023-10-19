from typing import Annotated, List
from uuid import UUID

from app.api.dependencies import groups_service, users_service
from app.schemas.users import (
    UserOutSchema,
    UserUpdateSchema,
)
from app.services.groups import GroupsService
from app.services.users import UsersService
from app.utils.oauth_bearer import get_current_unblocked_user
from app.utils.roles import Role
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
        group = await groups_service.get_group_by_id(user.group.id)
        if not group.users:
            await groups_service.delete_group(group.id)
        return updated_user
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
    groups_service: Annotated[GroupsService, Depends(groups_service)],
):
    try:
        await users_service.delete_user_by_id(user.id)
        group = await groups_service.get_group_by_id(user.group.id)
        if not group.users:
            await groups_service.delete_group(group.id)
    except Exception as e:
        raise e
    

@router.get("s", response_model=List[UserOutSchema])
async def users_get(
    user: Annotated[UserOutSchema, Depends(get_current_unblocked_user)],
    users_service: Annotated[UsersService, Depends(users_service)],
    filter_by_name: str = None, filter_by_surname: str = None, 
    sotred_by: str = None, order_by: str = None
):
    try:
        if user.role == Role.admin:
            group_id = None
        elif user.role == Role.moderator:
            group_id = user.group.id  
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Permission denied",
            )
        users = await users_service.get_users(
            filter_by_name, filter_by_surname, group_id, sotred_by, order_by,
        )
        return users
    except Exception as e:
        raise e
    

@router.get("/", response_model=UserOutSchema)
async def users_get(
    user_id: UUID,
    user: Annotated[UserOutSchema, Depends(get_current_unblocked_user)],
    users_service: Annotated[UsersService, Depends(users_service)],
):
    try:
        aim_user = await users_service.get_user_by_id(user_id)
        if user.role == Role.user or (user.role == Role.moderator and user.group.id != aim_user.group.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Permission denied",
            )
        return aim_user
    except UsersService.UserNotFoundException as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"User with id: [{user_id}] not found"
            )
    
    except Exception as e:
        raise e
    

@router.patch("/", response_model=UserOutSchema)
async def users_get(
    user_id: UUID,
    new_values: UserUpdateSchema,
    user: Annotated[UserOutSchema, Depends(get_current_unblocked_user)],
    users_service: Annotated[UsersService, Depends(users_service)],
    groups_service: Annotated[GroupsService, Depends(groups_service)],
):
    try:
        if user.role != Role.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Permission denied",
            )
        aim_user = await users_service.get_user_by_id(user_id)
        updated_group = await groups_service.update_group(aim_user.group, new_values.group_name)
        updated_user = await users_service.update_user(aim_user, new_values, updated_group)
        group = await groups_service.get_group_by_id(user.group.id)
        if not group.users:
            await groups_service.delete_group(group.id)
        return updated_user
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
    
# bug not working singup (creates user but throw exception)
# export logic of deletion group if the group is empty