import pytest_asyncio
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import auth_service, groups_service, users_service
from app.schemas.groups import GroupCreateSchema
from app.schemas.users import UserRegisterSchema
from app.services.email import EmailService


@pytest_asyncio.fixture
async def email_service():
    return EmailService()


@pytest_asyncio.fixture
async def group():
    service = groups_service()
    group_schema = GroupCreateSchema(name="group_name")
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
        group_name="group_name",
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


@pytest_asyncio.fixture
async def auth_user_singup():
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


@pytest_asyncio.fixture
async def tokens(user):
    service = auth_service()
    form = OAuth2PasswordRequestForm(username="username", password="password")
    tokens = await service.login(form)
    return tokens
