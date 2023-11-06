import redis.asyncio as redis

from app.config import settings


class async_session_maker:
    def __init__(self):
        self.session = redis.Redis(
            host=settings.redis.REDIS_HOST,
            port=settings.redis.REDIS_PORT,
            password=settings.redis.REDIS_PASS,
        )

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.aclose()
