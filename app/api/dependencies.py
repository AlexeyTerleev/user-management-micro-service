from app.repositories.users import UsersRepository
from app.repositories.groups import GroupsRepository

from app.services.users import UsersService
from app.services.groups import GroupsService


def users_service():
    return UsersService(UsersRepository)


def groups_service():
    return GroupsService(GroupsRepository)
