
import pytest
import pytest_asyncio
import asyncio

from app.api.dependencies import groups_service, users_service


@pytest_asyncio.fixture
async def empty_groups_repo():
    service = groups_service()
    await service.groups_repo.delete_all({})


@pytest_asyncio.fixture
async def empty_users_repo():
    service = users_service()
    await service.users_repo.delete_all({})