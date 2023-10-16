from app.repositories.groups import GroupsRepository
from app.repositories.users import UsersRepository
from app.services.groups import GroupsService
from app.services.users import UsersService
from app.services.auth import AuthService


def users_service():
    return UsersService(UsersRepository)


def groups_service():
    return GroupsService(GroupsRepository)

def auth_service():
    return AuthService(UsersService(UsersRepository), GroupsService(GroupsRepository))
