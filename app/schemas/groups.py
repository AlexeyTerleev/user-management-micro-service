from datetime import datetime
from typing import List
from uuid import UUID

from app.schemas.base import GroupSchema, UserDatabaseSchema


class GroupCreateSchema(GroupSchema):
    ...


class GroupOutSchema(GroupSchema):
    id: UUID
    created_at: datetime


class GroupDatabaseSchema(GroupSchema):
    id: UUID
    users: List[UserDatabaseSchema]
    created_at: datetime
