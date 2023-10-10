from pydantic import BaseModel, EmailStr, HttpUrl, field_validator
from uuid import UUID
from datetime import datetime
from app.utils.roles import Role
import re




class UserSchema(BaseModel):
    id: UUID
    hashed_password: str
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    role: Role
    group_id: UUID
    img_path: HttpUrl
    blocked: bool
    created_at: datetime
    modified_at: datetime


    @field_validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    class Config:
        from_attributes = True


class UserRegisterSchema(BaseModel):
    password: str
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    role: Role
    group_name: str
    img_path: HttpUrl

    @field_validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    password: str
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    role: Role
    group_id: UUID
    img_path: HttpUrl

    @field_validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v
    class Config:
        from_attributes = True


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