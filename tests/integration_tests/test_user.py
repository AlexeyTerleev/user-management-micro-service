import io

import pytest


@pytest.mark.usefixtures("empty_users_repo", "empty_groups_repo")
class TestUser:
    @pytest.mark.asyncio
    async def test_me_get(self, test_app, user_tokens):
        headers = {"Authorization": f"Bearer {user_tokens['access_token']}"}
        response = await test_app.get("user/me", headers=headers)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_me_delete(self, test_app, user_tokens):
        headers = {"Authorization": f"Bearer {user_tokens['access_token']}"}
        response = await test_app.delete("user/me", headers=headers)
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_me_patch(self, test_app, user_tokens):
        headers = {"Authorization": f"Bearer {user_tokens['access_token']}"}
        payload = {"name": "new_name"}
        response = await test_app.patch("user/me", headers=headers, json=payload)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_me_photo_patch(self, test_app, user_tokens):
        headers = {"Authorization": f"Bearer {user_tokens['access_token']}"}
        file = io.BytesIO(b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01")
        response = await test_app.patch(
            "user/me/photo", headers=headers, files={"photo": file}
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_users_get(self, test_app, admin_tokens):
        headers = {"Authorization": f"Bearer {admin_tokens['access_token']}"}
        response = await test_app.get("users", headers=headers)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_user_get(self, test_app, admin_tokens, create_user):
        headers = {"Authorization": f"Bearer {admin_tokens['access_token']}"}
        print(create_user)
        response = await test_app.get(f"user/{create_user['id']}", headers=headers)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_user_patch(self, test_app, admin_tokens, create_user):
        headers = {"Authorization": f"Bearer {admin_tokens['access_token']}"}
        print(create_user)
        payload = {"name": "new_name"}
        response = await test_app.patch(
            f"user/{create_user['id']}", headers=headers, json=payload
        )
        assert response.status_code == 200
