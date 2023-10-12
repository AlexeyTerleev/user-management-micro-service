from uuid import UUID

from app.schemas.groups import GroupCreateSchema, GroupDatabaseSchema
from app.utils.repository import AbstractRepository


class GroupsService:
    def __init__(self, groups_repo: AbstractRepository):
        self.groups_repo: AbstractRepository = groups_repo()

    async def get_group_by_name(self, name: str) -> GroupDatabaseSchema:
        group = await self.groups_repo.find_one({"name": name})
        return group
    
    async def get_group_by_id(self, id: UUID) -> GroupDatabaseSchema:
        group = await self.groups_repo.find_one({"id": id})
        return group

    async def create_group(self, new_group: GroupCreateSchema) -> GroupDatabaseSchema:
        group = await self.groups_repo.create_one({"name": new_group.name})
        return group

    async def get_or_create_group(self, name: str) -> GroupDatabaseSchema:
        group = await self.get_group_by_name(name)
        if group is None:
            group = await self.create_group(GroupCreateSchema(name=name))
        return group

    async def delete_group(self, id: UUID) -> GroupDatabaseSchema:
        group = await self.groups_repo.delete({"id": id})
        return group
