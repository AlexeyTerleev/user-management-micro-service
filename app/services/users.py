from uuid import UUID

from app.schemas.users import UserCreateSchema, UserUpgradeSchema
from app.utils.auth import get_hashed_password
from app.utils.repository import AbstractRepository
import re


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def get_user_by_idtf(self, idtf):
        if is_phone_number(idtf):
            return await self.get_user_by_phone_number(idtf)
        elif is_email(idtf):
            return await self.get_user_by_email(idtf)
        else:
            return await self.get_user_by_username(idtf)

    async def get_user_by_id(self, id):
        user = await self.users_repo.find_one({"id": id})
        return user

    async def get_user_by_username(self, username):
        user = await self.users_repo.find_one({"username": username})
        return user

    async def get_user_by_phone_number(self, phone_number):
        user = await self.users_repo.find_one({"phone_number": phone_number})
        return user

    async def get_user_by_email(self, email):
        user = await self.users_repo.find_one({"email": email})
        return user

    async def create_user(self, new_user: UserCreateSchema):
        user = await self.users_repo.create_one(new_user.dict())
        return user

    async def update_user(self, id: UUID, new_values: UserUpgradeSchema):
        upated_user = await self.users_repo.update_all(
            {"id": id}, new_values.dict(exclude_unset=True)
        )
        return upated_user

    async def delete_user_by_id(self, id: UUID):
        await self.users_repo.delete_all({"id": id})


def is_phone_number(filter_value: str) -> bool:
    regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
    return bool(re.match(regex, filter_value))


def is_email(filter_value: str) -> bool:
    regex = r"^[^@]+@[^@]+\.[^@]+$"
    return bool(re.match(regex, filter_value))