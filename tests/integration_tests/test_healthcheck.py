import pytest


class TestHealthcheck:
    @pytest.mark.asyncio
    async def test_healthcheck(self, test_app):
        response = await test_app.get("healthcheck")
        assert response.status_code == 204
