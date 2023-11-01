import asyncio
import pytest
import pytest_asyncio
from uuid import UUID

from app.api.dependencies import users_service, groups_service
from app.services.users import UsersService
from app.schemas.users import UserRegisterSchema, UserUpdateSchema
from app.schemas.groups import GroupCreateSchema


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
        )
    ]
    for user_schema in user_schemas:
        await service.create_user(user_schema, group.id)


@pytest.mark.usefixtures("empty_users_repo", "empty_groups_repo")
class TestUsersService:

    @pytest.mark.asyncio
    async def test_get_group_by_username(self, user):
        service = users_service()
        getted = await service.get_user_by_username(user.username)
        assert user == getted

    @pytest.mark.asyncio
    async def test_get_group_by_phone_number(self, user):
        service = users_service()
        getted = await service.get_user_by_phone_number(user.phone_number)
        assert user == getted

    @pytest.mark.asyncio
    async def test_get_group_by_email(self, user):
        service = users_service()
        getted = await service.get_user_by_email(user.email)
        assert user == getted
    
    @pytest.mark.asyncio
    async def test_get_group_by_id(self, user):
        service = users_service()
        getted = await service.get_user_by_id(user.id)
        assert user == getted

    @pytest.mark.asyncio
    async def test_get_group_by_idtf(self, user):
        service = users_service()
        getted = await service.get_user_by_username(user.username)
        assert user == getted

    @pytest.mark.asyncio
    async def test_update_user(self, user):
        service = users_service()
        new_name = "new_name"
        new_values = UserUpdateSchema(name=new_name)
        updated = await service.update_user(user, new_values)
        assert updated.id == user.id
        assert updated.name == new_name

    @pytest.mark.asyncio
    async def test_delete_user_by_id(self, user):
        service = users_service()
        await service.delete_user_by_id(user.id)
        with pytest.raises(UsersService.UserNotFoundException):
            empty = await service.get_user_by_id(user.id)
        
    @pytest.mark.asyncio
    async def test_get_users(self, users):
        service = users_service()
        getted = await service.get_users()
        assert len(getted) == 3
