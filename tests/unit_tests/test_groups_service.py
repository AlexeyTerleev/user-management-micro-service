import asyncio
import pytest
import pytest_asyncio

from app.api.dependencies import groups_service
from app.services.groups import GroupsService
from app.schemas.groups import GroupCreateSchema

@pytest_asyncio.fixture
async def group():
    service = groups_service()
    group_schema = GroupCreateSchema(name="group")
    group = await service.create_group(group_schema)
    return group


@pytest.mark.usefixtures("empty_users_repo", "empty_groups_repo")
class TestGroupsService:

    @pytest.mark.asyncio
    async def test_get_group_by_name(self, group):
        service = groups_service()
        getted = await service.get_group_by_name(group.name)
        assert group == getted

    @pytest.mark.asyncio
    async def test_get_group_by_id(self, group):
        service = groups_service()
        getted = await service.get_group_by_id(group.id)
        assert group == getted

    @pytest.mark.asyncio
    async def test_get_or_create_group(self):
        service = groups_service()
        name = "test_group"

        created = await service.get_or_create_group(name)
        getted = await service.get_or_create_group(name)

        assert created == getted

    @pytest.mark.asyncio
    async def test_update_group(self):
        service = groups_service()
        old_name, new_name = "old_test_group", "new_test_group"
        group = GroupCreateSchema(name=old_name)

        created = await service.create_group(group)
        not_updated = await service.update_group(created, old_name)
        updated = await service.update_group(created, new_name)

        old_group = await service.get_group_by_name(old_name)
        new_group = await service.get_group_by_name(new_name)

        assert old_group == not_updated
        assert new_group == updated

    @pytest.mark.asyncio
    async def test_delete_group_by_id(self, group):
        service = groups_service()
        await service.delete_group_by_id(group.id)
        with pytest.raises(GroupsService.GroupNotFoundException):
            empty = await service.get_group_by_name(group.name)

    @pytest.mark.asyncio
    async def test_delete_group_by_id_if_empty(self, group):
        service = groups_service()
        await service.delete_group_by_id_if_empty(group.id)
        with pytest.raises(GroupsService.GroupNotFoundException):
            empty = await service.get_group_by_name(group.name)