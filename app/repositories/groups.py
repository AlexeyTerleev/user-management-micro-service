from app.models.groups import Groups
from app.utils.repository import SQLAlchemyRepository

 
from sqlalchemy import delete, insert, select, update, asc
from sqlalchemy.orm import selectinload
from app.db.db import db_async_session_maker


class GroupsRepository(SQLAlchemyRepository):
    model = Groups

    async def create_one(self, values: dict):
        async with db_async_session_maker() as session:
            stmt = insert(self.model).options(selectinload(self.model.users)).values(**values).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one().to_read_model()