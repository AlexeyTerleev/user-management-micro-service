from uuid import UUID

from app.schemas.groups import GroupOutSchema
from app.schemas.users import UserRegisterSchema, UserOutSchema, UserCreateSchema
from app.services.users import UsersService
from app.services.groups import GroupsService
from app.utils.auth import get_hashed_password, verify_password, create_access_token, create_refresh_token




class AuthService:

    class DataIsUsedException(Exception):
        def __init__(self, data_type: str, *args: object) -> None:
            self.data_type = data_type
            super().__init__(*args)

    class UserNotFoundException(Exception):
        def __init__(self, username: str, *args: object) -> None:
            self.username = username
            super().__init__(*args)
    
    class IncorrectPasswordException(Exception):
        ...

    def __init__(self, users_service: UsersService, groups_service: GroupsService):
        self.users_service: UsersService = users_service
        self.groups_service: GroupsService = groups_service

    async def check_if_data_is_used(self, idtf):
        return (await self.users_service.get_user_by_idtf(idtf)) is not None

    async def singup(self, new_user: UserRegisterSchema) -> UserOutSchema:
        for idtf in ["username", "phone_number", "email"]:
            if await self.check_if_data_is_used(new_user.dict()[idtf]):
                raise AuthService.DataIsUsedException(data_type=idtf)

        group = await self.groups_service.get_or_create_group(new_user.group_name)

        new_user_dict = new_user.dict()
        new_user_dict["hashed_password"] = get_hashed_password(new_user_dict.pop("password"))
        new_user_dict["img_path"] = str(new_user_dict["img_path"])
        new_user_dict["group_id"] = group.id

        user = await self.users_service.create_user(UserCreateSchema(**new_user_dict))

        return UserOutSchema(group=GroupOutSchema(**group.dict()), **user.dict())
    
    async def login(self, form_data):
        user = await self.users_service.get_user_by_idtf(form_data.username)
        if user is None:
            raise AuthService.UserNotFoundException(username=form_data.username)
        if not verify_password(form_data.password, user.hashed_password):
            raise AuthService.IncorrectPasswordException
        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }

