import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl, field_validator

from app.utils.roles import Role
from app.schemas.base import UserSchema
from app.schemas.groups import GroupOutSchema



class UserRegisterSchema(UserSchema):
    password: str
    group_name: str
    img_path: HttpUrl | None = None


class UserCreateSchema(UserSchema):
    hashed_password: str
    group_id: UUID


class UserUpdateSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    role: Role | None = None
    group_name: str | None = None
    img_path: HttpUrl | None = None

    @field_validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


class UserUpgradeSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    role: Role | None = None
    group_id: UUID | None = None
    img_path: str | None = None

    @field_validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

class UserOutSchema(UserSchema):
    id: UUID
    group: GroupOutSchema
    hashed_password: str
    blocked: bool
    created_at: datetime
    modified_at: datetime


class UserIdtfsShema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenSchema(BaseModel):
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

    model_config = ConfigDict(from_attributes=True)
