from app.models.groups import Groups
from app.utils.repository import SQLAlchemyRepository


class GroupsRepository(SQLAlchemyRepository):
    model = Groups
