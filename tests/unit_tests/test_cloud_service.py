import io

import pytest

from app.api.dependencies import cloud_service


class TestCloudService:
    @pytest.mark.asyncio
    async def test_upload_photo(self):
        service = cloud_service()
        file = io.BytesIO(b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01")
        url = await service.upload_image("test_id", file)
        assert url
