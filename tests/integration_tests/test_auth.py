import asyncio
import pytest
import pytest_asyncio



@pytest.mark.usefixtures("empty_users_repo", "empty_groups_repo")
class TestAuth:

    @pytest.mark.asyncio
    async def test_refresh(self, test_app, tokens):
        payload = {"refresh_token": tokens["refresh_token"]}
        response = await test_app.post("auth/refresh-token", json=payload)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_reset_password(self, test_app, tokens):
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        response = await test_app.post("auth/reset-password", headers=headers)
        assert response.status_code == 200