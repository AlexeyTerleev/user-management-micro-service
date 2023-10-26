from app.repositories.cache import CacheRepository
from app.repositories.groups import GroupsRepository
from app.repositories.users import UsersRepository
from app.repositories.cloud import CloudRepository

from app.services.auth import AuthService
from app.services.cache import CacheService
from app.services.groups import GroupsService
from app.services.users import UsersService
from app.services.cloud import CloudService


def users_service():
    return UsersService(UsersRepository)


def groups_service():
    return GroupsService(GroupsRepository)


def cache_service():
    return CacheService(CacheRepository)


def auth_service():
    return AuthService(
        UsersService(UsersRepository),
        GroupsService(GroupsRepository),
        CacheService(CacheRepository),
    )

def cloud_service():
    return CloudService(CloudRepository)