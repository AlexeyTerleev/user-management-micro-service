import asyncio
import pytest
import pytest_asyncio
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import auth_service

from app.schemas.users import UserRegisterSchema

@pytest_asyncio.fixture
async def user():
    service = auth_service()
    user_schema = UserRegisterSchema(
        name="name",
        surname="surname",
        username="username",
        phone_number="+375299292242",
        email="email@email.com",
        role="USER",
        password="password",
        group_name="group",
    )
    user = await service.singup(user_schema)
    return user


@pytest.mark.usefixtures("empty_users_repo", "empty_groups_repo")
class TestAuthService:

    @pytest.mark.asyncio
    async def test_login(self, user):
        service = auth_service()
        form = OAuth2PasswordRequestForm(username="username", password="password")
        tokens = await service.login(form)
        assert tokens is not None