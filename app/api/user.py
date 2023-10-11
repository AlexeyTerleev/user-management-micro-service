from fastapi import APIRouter, Depends
from typing import Annotated

from app.schemas.users import UserSchema, UserUpdateSchema
from app.utils.oauth_bearer import get_current_unblocked_user
from app.services.users import UsersService
from app.api.dependencies import users_service


router = APIRouter(prefix="/user", tags=["User"],)


@router.get("/me")
async def me_get(user: Annotated[UserSchema, Depends(get_current_unblocked_user)],):
    try:
        return user
    except Exception as e:
        raise e


@router.patch("/me")
async def me_patch(
    new_values: UserUpdateSchema,
    user: Annotated[UserSchema, Depends(get_current_unblocked_user)],
    users_service: Annotated[UsersService, Depends(users_service)],
):
    try:
        update_data = new_values.dict(exclude_unset=True)
        update_user = user.copy(update=update_data)
        update_user_dict = update_user.dict()
        update_user_dict["img_path"] = str(update_user_dict["img_path"])
        updated_user = await users_service.update_user(user.id, update_user_dict)
        return updated_user
    except Exception as e:
        raise e

@router.delete("/me")
async def me_delete(
    user: Annotated[UserSchema, Depends(get_current_unblocked_user)],
    users_service: Annotated[UsersService, Depends(users_service)],
):
    try:
        await users_service.delete_user(user.id)
        return {"status": "deleted"}
    except Exception as e:
        raise e
