from abc import ABC, abstractmethod
from typing import Callable

import boto3
from sqlalchemy import asc, delete, insert, select, update

from app.cache_storage.cache_storage import (
    async_session_maker as cache_async_session_maker,
)
from app.config import settings
from app.db.db import async_session_maker as db_async_session_maker


class AbstractDBRepository(ABC):
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


class SQLAlchemyRepository(AbstractDBRepository):
    model = None

    async def find_all(
        self,
        filter_by: dict,
        sorted_by: str = None,
        order_func: Callable = asc,
        limit: int = None,
        offset: int = None,
    ):
        async with db_async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            if sorted_by:
                stmt = stmt.order_by(order_func(sorted_by))
            if limit:
                stmt = stmt.limit(limit)
            if offset:
                stmt = stmt.offset(offset)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.unique().all()]
            return res

    async def find_one(self, filter_by: dict):
        async with db_async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = res.first()
            return None if res is None else res[0].to_read_model()

    async def create_one(self, values: dict):
        async with db_async_session_maker() as session:
            stmt = insert(self.model).values(**values).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one().to_read_model()

    async def update_all(self, filter_by: dict, new_values: dict):
        async with db_async_session_maker() as session:
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
        async with db_async_session_maker() as session:
            stmt = delete(self.model).filter_by(**filter_by)
            await session.execute(stmt)
            await session.commit()
            return None


class AbstractCacheRepository(ABC):
    @abstractmethod
    async def sismember():
        raise NotImplementedError

    @abstractmethod
    async def sadd():
        raise NotImplementedError
    
    @abstractmethod
    async def srem():
        raise NotImplementedError


class RedisRepository(AbstractCacheRepository):
    async def sismember(self, key, member):
        async with cache_async_session_maker() as session:
            res = await session.sismember(key, member)
        return res

    async def sadd(self, key, value):
        async with cache_async_session_maker() as session:
            await session.sadd(key, value)

    async def srem(self, key, value):
        async with cache_async_session_maker() as session:
            await session.srem(key, value)

class AbstractCloudRepository(ABC):
    @abstractmethod
    async def upload_file():
        raise NotImplementedError


class S3Repository(AbstractCloudRepository):
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.aws.AWS_URL,
            aws_access_key_id=settings.aws.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.aws.AWS_SECRET_ACCESS_KEY,
            region_name=settings.aws.AWS_REGION_NAME,
        )
        self.bucket = settings.aws.s3.S3_BUCKET

    async def upload_file(self, path: str, content: bytes):
        self.client.upload_fileobj(Fileobj=content, Bucket=self.bucket, Key=path)
