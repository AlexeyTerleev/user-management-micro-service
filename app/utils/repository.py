from abc import ABC, abstractmethod

from sqlalchemy import insert, select, delete

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
    async def delete():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):

    model = None
    
    async def find_all(self, filter_by: dict):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res
    
    async def find_one(self, filter_by: dict):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = res.first()
            if res is None: 
                raise ValueError
            res = res[0].to_read_model()
            return res
        
    async def create_one(self, values: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**values).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
        
    async def delete(self, filter_by: dict):
        async with async_session_maker() as session:
            stmt = delete(self.model).filter_by(**filter_by)
            await session.execute(stmt)
            await session.commit()
            return None
