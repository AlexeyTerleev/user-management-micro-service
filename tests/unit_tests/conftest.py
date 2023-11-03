import pytest_asyncio

from app.services.email import EmailService


@pytest_asyncio.fixture
async def email_service():
    return EmailService()