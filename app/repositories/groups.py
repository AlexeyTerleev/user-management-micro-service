from sqlalchemy import asc, delete, insert, select, update
from sqlalchemy.orm import selectinload

from app.db.db import async_session_maker
from app.models.groups import Groups
from app.utils.repository import SQLAlchemyRepository


class GroupsRepository(SQLAlchemyRepository):
    model = Groups

    async def create_one(self, values: dict):
        async with async_session_maker() as session:
            stmt = (
                insert(self.model)
                .options(selectinload(self.model.users))
                .values(**values)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one().to_read_model()
