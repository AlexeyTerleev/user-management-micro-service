from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.db import Base
from app.schemas.users import UserDatabaseSchema
from app.utils.roles import Role
from sqlalchemy_utils import URLType


class Users(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hashed_password: Mapped[str]
    name: Mapped[str]
    surname: Mapped[str]
    username: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    role: Mapped[Role]
    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"))
    img_path: Mapped[str]
    blocked: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.current_timestamp()
    )

    def to_read_model(self) -> UserDatabaseSchema:
        return UserDatabaseSchema(
            id=self.id,
            hashed_password=self.hashed_password,
            name=self.name,
            surname=self.surname,
            username=self.username,
            phone_number=self.phone_number,
            email=self.email,
            role=self.role,
            group_id=self.group_id,
            img_path=self.img_path,
            blocked=self.blocked,
            created_at=self.created_at,
            modified_at=self.modified_at,
        )
