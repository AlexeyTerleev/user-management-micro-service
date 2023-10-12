from app.repositories.groups import GroupsRepository
from app.repositories.users import UsersRepository
from app.services.groups import GroupsService
from app.services.users import UsersService


def users_service():
    return UsersService(UsersRepository)


def groups_service():
    return GroupsService(GroupsRepository)
