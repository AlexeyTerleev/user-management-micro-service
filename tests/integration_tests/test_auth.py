import pytest


@pytest.mark.usefixtures("empty_users_repo", "empty_groups_repo")
class TestAuth:
    @pytest.mark.asyncio
    async def test_refresh(self, test_app, user_tokens):
        payload = {"refresh_token": user_tokens["refresh_token"]}
        response = await test_app.post("auth/refresh-token", json=payload)
        assert response.status_code == 200

