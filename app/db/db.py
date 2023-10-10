from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.db.postgres_user}:{settings.db.postgres_pass}@{settings.db.postgres_host}:{settings.db.postgres_port}/{settings.db.postgres_name}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
