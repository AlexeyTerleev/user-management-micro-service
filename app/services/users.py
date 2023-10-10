from uuid import UUID

from app.utils.repository import AbstractRepository
from app.utils.auth import get_hashed_password
from app.schemas.users import UserCreateSchema


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def get_user(self, filter_by):
        user = await self.users_repo.find_one(filter_by)
        return user
    
    async def create_user(self, new_user: UserCreateSchema):
        user = await self.users_repo.create_one(
            {
                "hashed_password": get_hashed_password(new_user.password),
                "name": new_user.name,
                "surname": new_user.surname,
                "username": new_user.username,
                "phone_number": new_user.phone_number,
                "email": new_user.email,
                "role": new_user.role,
                "group_id": new_user.group_id,
                "img_path": str(new_user.img_path), 
            }
        )
        return user
    
    async def delete_user(self, id: UUID):
        await self.users_repo.delete({"id": id})

