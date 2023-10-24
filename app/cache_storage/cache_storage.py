import redis.asyncio as redis
from app.config import settings

class async_session_maker:

    def __init__(self):
        self.session = redis.Redis(host=settings.redis.host, port=settings.redis.port, password=settings.redis.password)

    async def __aenter__(self):
        return self.session
 
    async def __aexit__(self, exc_type, exc, tb):
        await self.session.aclose()