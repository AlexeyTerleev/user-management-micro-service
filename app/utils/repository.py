from abc import ABC, abstractmethod
from typing import List, Callable

from sqlalchemy import delete, insert, select, update, asc

from app.db.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        raise NotImplementedError

    @abstractmethod
    async def create_one():
        raise NotImplementedError

    @abstractmethod
    async def update_all():
        raise NotImplementedError

    @abstractmethod
    async def delete_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):

    model = None

    async def find_all(self, filter_by: dict, sorted_by: str = None, order_func: Callable = asc):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            if sorted_by:
                stmt = stmt.order_by(order_func(sorted_by))
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def find_one(self, filter_by: dict):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = res.first()
            return None if res is None else res[0].to_read_model()

    async def create_one(self, values: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**values).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one().to_read_model()

    async def update_all(self, filter_by: dict, new_values: dict):
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .filter_by(**filter_by)
                .values(**new_values)
                .returning(self.model)
            )
            updated_user = await session.execute(stmt)
            await session.commit()
            updated_user = updated_user.unique().scalar_one()
            return updated_user.to_read_model()

    async def delete_all(self, filter_by: dict):
        async with async_session_maker() as session:
            stmt = delete(self.model).filter_by(**filter_by)
            await session.execute(stmt)
            await session.commit()
            return None
    
