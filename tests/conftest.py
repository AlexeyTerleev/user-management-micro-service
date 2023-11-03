import asyncio

import pytest
import pytest_asyncio
from faker import Faker

from app.api.dependencies import groups_service, users_service
from app.config import settings
from app.db.db import Base, engine
from app.models.groups import GroupDatabaseSchema
from app.models.users import UserDatabaseSchema

pytest_plugins = ("pytest_asyncio",)


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


@pytest_asyncio.fixture
async def empty_users_repo():
    service = users_service()
    await service.users_repo.delete_all({})


async def creation_payload():
    faker = Faker()
    payload = {
        "name": faker.first_name(),
        "surname": faker.last_name(),
        "username": faker.user_name(),
        "phone_number": f"+375{faker.msisdn()[4:]}",
        "email": faker.email(),
        "img_path": faker.url(),
        "password": faker.password(),
        "group_name": faker.random_element(elements=('group_1', 'group_2', 'group_3'))
    }
    return payload

@pytest_asyncio.fixture
async def user_creation_payload():
    payload = await creation_payload()
    payload["role"] = "USER"
    return payload

@pytest_asyncio.fixture
async def admin_creation_payload():
    payload = await creation_payload()
    payload["role"] = "ADMIN"
    return payload
