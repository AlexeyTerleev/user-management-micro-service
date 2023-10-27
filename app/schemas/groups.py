from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel


class GroupSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class GroupCreateSchema(GroupSchema):
    ...


class GroupOutSchema(GroupSchema):
    id: UUID
    created_at: datetime


class GroupDatabaseSchema(GroupSchema):
    id: UUID
    users: "List[UserDatabaseSchema]"
    created_at: datetime


from app.schemas.users import UserDatabaseSchema
GroupDatabaseSchema.update_forward_refs()