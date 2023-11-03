import pytest


class TestGroupsService:
    @pytest.mark.asyncio
    async def test_send_reset_password_url(self, email_service):
        response = await email_service.send_reset_password_url(
            "test@gmail.com", "test_url"
        )
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
