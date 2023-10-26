import re
from typing import List
from uuid import UUID

from sqlalchemy import asc, desc

from app.schemas.users import (
    UserCreateSchema,
    UserIdtfsShema,
    UserOutSchema,
    UserRegisterSchema,
    UserUpdateSchema,
    UserUpgradeSchema,
)
from app.utils.auth import get_hashed_password
from app.utils.repository import AbstractDBRepository


class UsersService:
    class UserNotFoundException(Exception):
        def __init__(self, idtf: str, value: str, *args: object) -> None:
            self.idtf = idtf
            self.value = value
            super().__init__(*args)

    class UserExistsException(Exception):
        def __init__(self, idtf: str, value: str, *args: object) -> None:
            self.idtf = idtf
            self.value = value
            super().__init__(*args)

    class NothingToUpdateException(Exception):
        ...

    def __init__(self, users_repo: AbstractDBRepository):
        self.users_repo: AbstractDBRepository = users_repo()

    async def get_user_by_idtf(self, idtf):
        if await self.__is_phone_number(idtf):
            user = await self.get_user_by_phone_number(idtf)
        elif await self.__is_email(idtf):
            user = await self.get_user_by_email(idtf)
        else:
            user = await self.get_user_by_username(idtf)
        return user

    async def __is_phone_number(self, filter_value: str) -> bool:
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        return bool(filter_value and re.search(regex, filter_value, re.I))

    async def __is_email(self, filter_value: str) -> bool:
        regex = r"^[^@]+@[^@]+\.[^@]+$"
        return bool(filter_value and re.search(regex, filter_value, re.I))

    async def get_user_by_id(self, id) -> UserOutSchema:
        user = await self.users_repo.find_one({"id": id})
        if not user:
            raise UsersService.UserNotFoundException("id", id)
        return user

    async def get_user_by_username(self, username) -> UserOutSchema:
        user = await self.users_repo.find_one({"username": username})
        if not user:
            raise UsersService.UserNotFoundException("username", username)
        return user

    async def get_user_by_phone_number(self, phone_number) -> UserOutSchema:
        user = await self.users_repo.find_one({"phone_number": phone_number})
        if not user:
            raise UsersService.UserNotFoundException("phone_number", phone_number)
        return user

    async def get_user_by_email(self, email) -> UserOutSchema:
        user = await self.users_repo.find_one({"email": email})
        if not user:
            raise UsersService.UserNotFoundException("email", email)
        return user

    async def create_user(
        self, new_user: UserRegisterSchema, new_user_group_id: int
    ) -> UserOutSchema:
        register_dict = new_user.dict()
        await self.__raise_except_if_user_exists(UserIdtfsShema(**register_dict))
        create_dict = await self.__transform_values(register_dict, new_user_group_id)
        create_user = UserCreateSchema(**create_dict)
        created_user = await self.users_repo.create_one(create_user.dict())
        return created_user

    async def update_user(
        self, current_user: UserOutSchema, new_values: UserUpdateSchema, new_value_group
    ) -> UserOutSchema:
        update_dict = new_values.dict(exclude_unset=True)
        await self.__raise_except_if_user_exists(UserIdtfsShema(**update_dict))
        upgrade_dct = await self.__transform_values(update_dict, new_value_group.id)
        upgrade_dct = await self.__remove_unchaneged_values(current_user, upgrade_dct)
        if not upgrade_dct:
            raise UsersService.NothingToUpdateException
        upgrade_user = UserUpgradeSchema(**upgrade_dct)
        upgraded_user = await self.users_repo.update_all(
            {"id": current_user.id}, upgrade_user.dict(exclude_unset=True)
        )
        return upgraded_user

    async def __raise_except_if_user_exists(self, user_idtfs: UserIdtfsShema) -> None:
        for idtf, value in user_idtfs.dict(exclude_unset=True).items():
            try:
                await self.get_user_by_idtf(value)
            except UsersService.UserNotFoundException:
                continue
            else:
                raise UsersService.UserExistsException(idtf, value)

    async def __transform_values(self, dct: dict, group_id) -> dict:
        if dct.get("password", None):
            dct["hashed_password"] = get_hashed_password(dct.pop("password"))
        if dct.get("img_path", None):
            dct["img_path"] = str(dct["img_path"])
        if group_id:
            dct["group_id"] = group_id
        return dct

    async def __remove_unchaneged_values(
        self, current_user: UserOutSchema, upgrade_dct: dict
    ) -> dict:
        if current_user.group.id == upgrade_dct["group_id"]:
            upgrade_dct.pop("group_id")
        for key, value in current_user.dict().items():
            if value == upgrade_dct.get(key, None):
                upgrade_dct.pop(key)
        return upgrade_dct

    async def delete_user_by_id(self, id: UUID) -> None:
        await self.users_repo.delete_all({"id": id})

    async def get_users(
        self,
        page: int = None,
        limit: int = None,
        filter_by_name: str = None,
        filter_by_surname: str = None,
        filter_by_group_id: str = None,
        sorted_by: str = None,
        order_by: str = None,
    ) -> List[UserOutSchema]:
        filter_by = {
            "name": filter_by_name,
            "surname": filter_by_surname,
            "group_id": filter_by_group_id,
        }
        filter_by = {key: value for key, value in filter_by.items() if value}
        order_func = desc if order_by and order_by == "desc" else asc
        offset = limit * page if page and limit else None
        users = await self.users_repo.find_all(
            filter_by=filter_by,
            sorted_by=sorted_by,
            order_func=order_func,
            limit=limit,
            offset=offset,
        )
        return users
