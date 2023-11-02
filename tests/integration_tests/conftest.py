import pytest_asyncio
from httpx import AsyncClient

from app.main import app


@pytest_asyncio.fixture(scope="module")
async def test_app():
    async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
        yield ac


@pytest_asyncio.fixture
async def create_user(test_app):
    payload = {
        "name": "username",
        "surname": "username",
        "username": "username",
        "phone_number": "+111111111111",
        "email": "username@example.com",
        "role": "USER",
        "img_path": "https://username.com/",
        "password": "password",
        "group_name": "group",
    }
    response = await test_app.post("auth/singup", json=payload)
    return response.json()


@pytest_asyncio.fixture
async def create_admin(test_app):
    payload = {
        "name": "admin",
        "surname": "admin",
        "username": "admin",
        "phone_number": "+211111111111",
        "email": "admin@example.com",
        "role": "ADMIN",
        "img_path": "https://admin.com/",
        "password": "password",
        "group_name": "group",
    }
    response = await test_app.post("auth/singup", json=payload)
    return response.json()


@pytest_asyncio.fixture
async def user_tokens(test_app, create_user):
    payload = {"username": "username", "password": "password"}
    response = await test_app.post("auth/login", data=payload)
    return response.json()


@pytest_asyncio.fixture
async def admin_tokens(test_app, create_admin):
    payload = {"username": "admin", "password": "password"}
    response = await test_app.post("auth/login", data=payload)
    return response.json()
