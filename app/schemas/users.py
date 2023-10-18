import re
from datetime import datetime
from uuid import UUID

import app.schemas.groups as groups_schemas
from app.utils.roles import Role
from pydantic import BaseModel, EmailStr, HttpUrl, field_validator


class UserSchema(BaseModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    role: Role
    img_path: str

    @field_validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    class Config:
        from_attributes = True


class UserRegisterSchema(UserSchema):
    password: str
    group_name: str
    img_path: HttpUrl

class UserCreateSchema(UserSchema):
    hashed_password: str
    group_id: UUID
    img_path: str


class UserUpdateSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    role: Role | None = None
    img_path: HttpUrl | None = None
    password: str | None = None
    group_name: str | None = None

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
    img_path: str | None = None
    hashed_password: str | None = None
    group_id: UUID | None = None

    @field_validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


class UserDatabaseSchema(UserSchema):
    id: UUID
    group_id: UUID
    hashed_password: str
    blocked: bool
    created_at: datetime
    modified_at: datetime


class UserOutSchema(UserSchema):
    id: UUID
    group: groups_schemas.GroupOutSchema
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

    class Config:
        from_attributes = True


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

    class Config:
        from_attributes = True
