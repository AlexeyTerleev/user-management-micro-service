from fastapi import APIRouter, Depends
from typing import Annotated

from app.schemas.users import UserSchema
from app.utils.oauth_bearer import get_current_user
from app.services.users import UsersService
from app.api.dependencies import users_service


router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("/me")
async def auth_login(
    user: Annotated[UserSchema, Depends(get_current_user)],
    ):
    try:
        return user
    except Exception as e:
        raise e
    

@router.patch("/me")
async def auth_login(
    user: Annotated[UserSchema, Depends(get_current_user)],
    ):
    return user


@router.delete("/me")
async def auth_login(
    user: Annotated[UserSchema, Depends(get_current_user)],
    users_service: Annotated[UsersService, Depends(users_service)],
    ):
    try:
        await users_service.delete_user(user.id)
        return {"status": "deleted"}
    except Exception as e:
        raise e