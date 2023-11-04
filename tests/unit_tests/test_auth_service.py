from contextlib import nullcontext as does_not_raise

import pytest
import pytest_asyncio
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import auth_service, cache_service
from app.schemas.users import TokenSchema, UserRegisterSchema
from app.services.auth import AuthService
from app.services.users import UsersService


@pytest.mark.usefixtures("empty_users_repo", "empty_groups_repo")
class TestAuthService:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "login, password, expectation",
        [
            ("username", "password", does_not_raise()),
            ("+375299292242", "password", does_not_raise()),
            ("email@email.com", "password", does_not_raise()),
            (
                "wrong_username",
                "password",
                pytest.raises(UsersService.UserNotFoundException),
            ),
            (
                "+111111111111",
                "password",
                pytest.raises(UsersService.UserNotFoundException),
            ),
            (
                "wrong_email@email.com",
                "password",
                pytest.raises(UsersService.UserNotFoundException),
            ),
            (
                "username",
                "wrong_password",
                pytest.raises(AuthService.IncorrectPasswordException),
            ),
        ],
    )
    async def test_login(self, auth_user_singup, login, password, expectation):
        service = auth_service()
        with expectation:
            tokens = await service.login(
                OAuth2PasswordRequestForm(
                    username=login,
                    password=password,
                )
            )
            assert tokens is not None

    @pytest.mark.asyncio
    async def test_refresh_tokens(self, tokens):
        service = auth_service()
        refreshed_tokens = await service.refresh_tokens(tokens.refresh_token)

        assert refreshed_tokens is not None

        service = cache_service()
        await service.cache_repo.srem("token_blacklist", tokens.refresh_token)
