from uuid import UUID

from app.utils.repository import AbstractRepository
from app.schemas.groups import GroupRegisterSchema


class GroupsService:
    def __init__(self, groups_repo: AbstractRepository):
        self.groups_repo: AbstractRepository = groups_repo()

    async def get_group(self, name: str):
        group = await self.groups_repo.find_one({"name": name})
        return group
    
    async def create_group(self, new_group: GroupRegisterSchema):
        group = await self.groups_repo.create_one(
            {
                "name": new_group.name 
            }
        )
        return group
    
    async def get_or_create_group(self, name: str):
        try:
            group = await self.get_group(name)
        except ValueError:
            group = await self.create_group(GroupRegisterSchema(name=name))
        return group
    
    async def delete_group(self, id: UUID):
        group = await self.groups_repo.delete(
            {"id": id}
        )
        return group