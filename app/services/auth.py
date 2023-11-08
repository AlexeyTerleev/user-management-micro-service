from datetime import datetime

import jwt

from app.config import settings
from app.schemas.users import (
    TokenPayload,
    TokenSchema,
    UserOutSchema,
    UserRegisterSchema,
)
from app.services.cache import CacheService
from app.services.groups import GroupsService
from app.services.users import UsersService
from app.utils.auth import create_access_token, create_refresh_token, verify_password


class AuthService:
    class IncorrectPasswordException(Exception):
        ...

    def __init__(
        self,
        users_service: UsersService,
        groups_service: GroupsService,
        cache_service: CacheService,
    ):
        self.users_service: UsersService = users_service
        self.groups_service: GroupsService = groups_service
        self.cache_service: CacheService = cache_service

    async def singup(self, new_user: UserRegisterSchema) -> UserOutSchema:
        group = await self.groups_service.get_or_create_group(new_user.group_name)
        user = await self.users_service.create_user(new_user, group.id)
        return user

    async def login(self, form_data) -> TokenSchema:
        user = await self.users_service.get_user_by_idtf(form_data.username)
        if not verify_password(form_data.password, user.hashed_password):
            raise AuthService.IncorrectPasswordException
        return TokenSchema(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh_tokens(self, refresh_token) -> TokenSchema:
        payload = jwt.decode(
            refresh_token,
            settings.auth.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.auth.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise jwt.ExpiredSignatureError
        if await self.cache_service.token_in_blackist(refresh_token):
            raise jwt.ExpiredSignatureError
        await self.cache_service.blacklist_token(refresh_token)
        return TokenSchema(
            access_token=create_access_token(token_data.sub),
            refresh_token=create_refresh_token(token_data.sub),
        )
