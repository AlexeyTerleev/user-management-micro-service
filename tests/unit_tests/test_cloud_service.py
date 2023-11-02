import io

import pytest

from app.api.dependencies import cloud_service


class TestGroupsService:
    @pytest.mark.asyncio
    async def test_send_reset_password_url(self):
        service = cloud_service()
        file = io.BytesIO(b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01")
        url = await service.upload_image("test_id", file)
        assert url
