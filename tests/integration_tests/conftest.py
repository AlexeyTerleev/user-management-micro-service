import pytest_asyncio
from httpx import AsyncClient

from app.main import app


@pytest_asyncio.fixture(scope="module")
async def test_app():
    async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
        yield ac


@pytest_asyncio.fixture
async def create_user(test_app, user_creation_payload):
    response = await test_app.post("auth/singup", json=user_creation_payload)
    return response.json()


@pytest_asyncio.fixture
async def create_admin(test_app, admin_creation_payload):
    response = await test_app.post("auth/singup", json=admin_creation_payload)
    return response.json()


@pytest_asyncio.fixture
async def user_tokens(test_app, user_creation_payload):
    response = await test_app.post("auth/singup", json=user_creation_payload)
    payload = {
        "username": user_creation_payload["username"],
        "password": user_creation_payload["password"],
    }
    response = await test_app.post("auth/login", data=payload)
    return response.json()


@pytest_asyncio.fixture
async def admin_tokens(test_app, admin_creation_payload):
    response = await test_app.post("auth/singup", json=admin_creation_payload)
    payload = {
        "username": admin_creation_payload["username"],
        "password": admin_creation_payload["password"],
    }
    response = await test_app.post("auth/login", data=payload)
    return response.json()
