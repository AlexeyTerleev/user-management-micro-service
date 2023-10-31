from app.config import settings
from app.db.db import Base, async_session_maker, engine, DATABASE_URL

from app.models.groups import GroupDatabaseSchema
from app.models.users import UserDatabaseSchema

from app.schemas.groups import GroupCreateSchema, GroupDatabaseSchema

from app.api.dependencies import groups_service
import asyncio
import pytest
import pytest_asyncio

pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def empty_groups_repo():
    service = groups_service()
    await service.groups_repo.delete_all({})


@pytest.mark.usefixtures("empty_groups_repo")
class TestGroupService:

    @pytest.mark.asyncio
    async def test_get_group_by_name(self):
        service = groups_service()
        name = "test_group"
        group = GroupCreateSchema(name=name)

        created = await service.create_group(group)
        getted = await service.get_group_by_name(name)

        assert created == getted

    @pytest.mark.asyncio
    async def test_get_group_by_id(self):
        service = groups_service()
        name = "test_group"
        group = GroupCreateSchema(name=name)

        created = await service.create_group(group)
        getted = await service.get_group_by_id(created.id)

        assert created == getted

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
    
        print(created)
        print(updated)

        old_group = await service.get_group_by_name(old_name)
        new_group = await service.get_group_by_name(new_name)

        assert old_group == not_updated
        assert new_group == updated

    @pytest.mark.asyncio
    async def test_delete_group_by_id(self):
        service = groups_service()
        name = "test_group"
        group = GroupCreateSchema(name=name)

        created = await service.create_group(group)
        await service.delete_group_by_id(created.id)
        getted = await service.get_group_by_name(name)

        assert getted is None

    @pytest.mark.asyncio
    async def test_delete_group_by_id_if_empty(self):
        service = groups_service()
        name = "test_group"
        group = GroupCreateSchema(name=name)

        created = await service.create_group(group)
        await service.delete_group_by_id_if_empty(created.id)
        getted = await service.get_group_by_name(name)

        assert getted is None