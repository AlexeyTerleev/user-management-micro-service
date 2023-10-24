from app.utils.repository import AbstractCacheRepository


class CacheService:
    def __init__(self, cache_repo: AbstractCacheRepository):
        self.cache_repo: AbstractCacheRepository = cache_repo()

    async def token_in_blackist(self, token) -> bool:
        return await self.cache_repo.sismember("token_blacklist", token)
    
    async def blacklist_token(self, token) -> None:
        await self.cache_repo.sadd("token_blacklist", token)