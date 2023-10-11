from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class GroupSchema(BaseModel):
    id: UUID
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class GroupRegisterSchema(BaseModel):
    name: str

    class Config:
        form_attribudes = True
