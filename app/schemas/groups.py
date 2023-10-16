from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GroupSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class GroupCreateSchema(GroupSchema):
    ...


class GroupDatabaseSchema(GroupSchema):
    id: UUID
    created_at: datetime


class GroupOutSchema(GroupSchema):
    id: UUID
    created_at: datetime
