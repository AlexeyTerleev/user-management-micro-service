import pytest


@pytest.mark.usefixtures("empty_users_repo", "empty_groups_repo")
class TestAuth:
    @pytest.mark.asyncio
    async def test_refresh(self, test_app, user_tokens):
        payload = {"refresh_token": user_tokens["refresh_token"]}
        response = await test_app.post("auth/refresh-token", json=payload)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_reset_password(self, test_app, user_tokens):
        headers = {"Authorization": f"Bearer {user_tokens['access_token']}"}
        response = await test_app.post("auth/reset-password", headers=headers)
        assert response.status_code == 200
