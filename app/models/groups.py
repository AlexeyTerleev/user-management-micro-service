from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from uuid import UUID, uuid4
from datetime import datetime

from app.db.db import Base
from app.schemas.groups import GroupSchema


class Groups(Base):
    __tablename__ = "groups"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def to_read_model(self) -> GroupSchema:
        return GroupSchema(id=self.id, name=self.name, created_at=self.created_at,)
