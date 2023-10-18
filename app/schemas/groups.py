from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import List


class GroupSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class GroupCreateSchema(GroupSchema):
    ...

class GroupOutSchema(GroupSchema):
    id: UUID
    created_at: datetime

import app.schemas.users as users_schemas
class GroupDatabaseSchema(GroupSchema):
    id: UUID
    users: List[users_schemas.UserDatabaseSchema]
    created_at: datetime

