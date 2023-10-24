from uuid import UUID

from app.schemas.groups import GroupCreateSchema, GroupDatabaseSchema, GroupOutSchema
from app.utils.repository import AbstractDBRepository


class GroupsService:
    def __init__(self, groups_repo: AbstractDBRepository):
        self.groups_repo: AbstractDBRepository = groups_repo()

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
    
    async def update_group(self, current_group: GroupOutSchema, new_group_name: str | None) -> UUID:
        if new_group_name and new_group_name != current_group.name:
            new_group = await self.get_or_create_group(new_group_name)
        else:
            new_group = current_group
        return new_group
        
    async def delete_group_by_id(self, id: UUID) -> GroupDatabaseSchema:
        group = await self.groups_repo.delete_all({"id": id})
        return group
    
    async def delete_group_by_id_if_empty(self, id: UUID) -> GroupDatabaseSchema:
        group = await self.get_group_by_id(id)
        if not group.users:
            await self.delete_group_by_id(id)
        return group