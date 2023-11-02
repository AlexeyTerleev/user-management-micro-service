import asyncio
import pytest
import pytest_asyncio
from contextlib import nullcontext as does_not_raise

from app.services.email import EmailService
from app.schemas.groups import GroupCreateSchema

@pytest_asyncio.fixture
async def email_service():
    return EmailService()

class TestGroupsService:

    @pytest.mark.asyncio
    async def test_send_reset_password_url(self, email_service):
        response = await email_service.send_reset_password_url("test@gmail.com", "test_url")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200