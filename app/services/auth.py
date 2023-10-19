from app.schemas.groups import GroupOutSchema
from app.schemas.users import UserRegisterSchema, UserOutSchema
from app.services.users import UsersService
from app.services.groups import GroupsService
from app.utils.auth import verify_password, create_access_token, create_refresh_token



class AuthService:
    
    class IncorrectPasswordException(Exception):
        ...

    def __init__(self, users_service: UsersService, groups_service: GroupsService):
        self.users_service: UsersService = users_service
        self.groups_service: GroupsService = groups_service

    async def singup(self, new_user: UserRegisterSchema) -> UserOutSchema:
        group = await self.groups_service.get_or_create_group(new_user.group_name)
        user = await self.users_service.create_user(new_user, group.id)
        return user
    
    async def login(self, form_data):
        user = await self.users_service.get_user_by_idtf(form_data.username)
        if not verify_password(form_data.password, user.hashed_password):
            raise AuthService.IncorrectPasswordException
        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }


# {
#   "name": "name",
#   "surname": "surname",
#   "username": "username",
#   "phone_number": "+375299292242",
#   "email": "user@example.com",
#   "role": "USER",
#   "img_path": "https://example.com/",
#   "password": "password",
#   "group_name": "string"
# }