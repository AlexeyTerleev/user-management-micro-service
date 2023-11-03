import re
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from app.utils.roles import Role


class UserSchema(BaseModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    role: Role
    img_path: str | None

    @field_validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    model_config = ConfigDict(from_attributes=True)

class UserDatabaseSchema(UserSchema):
    id: UUID
    group_id: UUID
    hashed_password: str
    blocked: bool
    created_at: datetime
    modified_at: datetime


class GroupSchema(BaseModel):
    name: str
    
    model_config = ConfigDict(from_attributes=True)