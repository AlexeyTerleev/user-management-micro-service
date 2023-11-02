from contextlib import nullcontext as does_not_raise

import pytest
import pytest_asyncio

from app.api.dependencies import groups_service, users_service
from app.schemas.groups import GroupCreateSchema
from app.schemas.users import UserRegisterSchema, UserUpdateSchema
from app.services.users import UsersService


@pytest_asyncio.fixture
async def group():
    service = groups_service()
    group_schema = GroupCreateSchema(name="group")
    group = await service.create_group(group_schema)
    return group


@pytest_asyncio.fixture
async def user(group):
    service = users_service()
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
    user = await service.create_user(user_schema, group.id)
    return user


@pytest_asyncio.fixture
async def users(group):
    service = users_service()
    user_schemas = [
        UserRegisterSchema(
            name="name1",
            surname="surname1",
            username="username1",
            phone_number="+111111111111",
            email="email1@email.com",
            role="USER",
            password="password",
            group_name="group",
        ),
        UserRegisterSchema(
            name="name2",
            surname="surname2",
            username="username2",
            phone_number="+211111111111",
            email="email2@email.com",
            role="MODERATOR",
            password="password",
            group_name="group",
        ),
        UserRegisterSchema(
            name="name3",
            surname="surname3",
            username="username3",
            phone_number="+311111111111",
            email="email3@email.com",
            role="ADMIN",
            password="password",
            group_name="group",
        ),
    ]
    for user_schema in user_schemas:
        await service.create_user(user_schema, group.id)


@pytest.mark.usefixtures("empty_users_repo", "empty_groups_repo")
class TestUsersService:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "username, expectation",
        [
            ("username", does_not_raise()),
            ("wrong_username", pytest.raises(UsersService.UserNotFoundException)),
        ],
    )
    async def test_get_user_by_username(self, user, username, expectation):
        service = users_service()
        with expectation:
            getted = await service.get_user_by_username(username)
            assert user == getted

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "phone_number, expectation",
        [
            ("+375299292242", does_not_raise()),
            ("+111111111111", pytest.raises(UsersService.UserNotFoundException)),
        ],
    )
    async def test_get_user_by_phone_number(self, user, phone_number, expectation):
        service = users_service()
        with expectation:
            getted = await service.get_user_by_phone_number(phone_number)
            assert user == getted

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "email, expectation",
        [
            ("email@email.com", does_not_raise()),
            (
                "wrong_email@email.com",
                pytest.raises(UsersService.UserNotFoundException),
            ),
        ],
    )
    async def test_get_user_by_email(self, user, email, expectation):
        service = users_service()
        with expectation:
            getted = await service.get_user_by_email(email)
            assert user == getted

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, user):
        service = users_service()
        getted = await service.get_user_by_id(user.id)
        assert user == getted

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "idtf, expectation",
        [
            ("username", does_not_raise()),
            ("+375299292242", does_not_raise()),
            ("email@email.com", does_not_raise()),
            ("wrong_username", pytest.raises(UsersService.UserNotFoundException)),
            ("+111111111111", pytest.raises(UsersService.UserNotFoundException)),
            (
                "wrong_email@email.com",
                pytest.raises(UsersService.UserNotFoundException),
            ),
        ],
    )
    async def test_get_user_by_idtf(self, user, idtf, expectation):
        service = users_service()
        with expectation:
            getted = await service.get_user_by_idtf(idtf)
            assert user == getted

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "new_values, expectation",
        [
            (
                UserUpdateSchema(name="new_name", username="new_username"),
                does_not_raise(),
            ),
            (
                UserUpdateSchema(surname="surname"),
                pytest.raises(UsersService.NothingToUpdateException),
            ),
        ],
    )
    async def test_update_user(self, user, new_values, expectation):
        service = users_service()
        with expectation:
            updated = await service.update_user(user, new_values)

            assert updated.id == user.id
            updated_dict, new_values_dict = (
                updated.model_dump(),
                new_values.model_dump(),
            )
            for key, value in new_values_dict.items():
                if value:
                    assert updated_dict[key] == value

    @pytest.mark.asyncio
    async def test_delete_user_by_id(self, user):
        service = users_service()
        await service.delete_user_by_id(user.id)
        with pytest.raises(UsersService.UserNotFoundException):
            empty = await service.get_user_by_id(user.id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "page, limit, filter_by_name, filter_by_surname, filter_by_group_id, sorted_by, ordered_by, res",
        [
            (None, None, "name1", None, None, None, None, "username1"),
            (None, None, None, "surname1", None, None, None, "username1"),
            (0, 1, None, None, None, "name", "desc", "username3"),
            (1, 1, None, None, None, "name", "desc", "username2"),
            (2, 1, None, None, None, "name", "desc", "username1"),
            (0, 1, None, None, None, "name", "asc", "username1"),
            (1, 2, None, None, None, "name", "asc", "username3"),
        ],
    )
    async def test_get_users(
        self,
        users,
        page,
        limit,
        filter_by_name,
        filter_by_surname,
        filter_by_group_id,
        sorted_by,
        ordered_by,
        res,
    ):
        service = users_service()
        getted = await service.get_users(
            page,
            limit,
            filter_by_name,
            filter_by_surname,
            filter_by_group_id,
            sorted_by,
            ordered_by,
        )
        assert getted[0].username == res
