import asyncio
import pytest
from app.api.dependencies import cache_service




class TestCacheService:

    @pytest.mark.asyncio
    async def test_tocken_not_in_balcklist(self):
        service = cache_service()
        token_in_blacklist = await service.token_in_blackist("test_tocken")
        assert not token_in_blacklist

    @pytest.mark.asyncio
    async def test_balcklist_token(self):
        service = cache_service()
        await service.blacklist_token("test_tocken")
        token_in_blacklist = await service.token_in_blackist("test_tocken")
        assert token_in_blacklist

        await service.cache_repo.srem("token_blacklist", "test_tocken")
        