from httpx import AsyncClient


async def login_user(client: AsyncClient) -> str:
    user_token = await client.post(
        "/api/v1/auth/token",
        data={"username": "tester", "password": "testpass"},
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    return user_token.json()["access_token"]


async def test_create_post(client):
    user_token = await login_user(client)

    result = await client.post(
        "/api/v1/posts/create",
        json={"text": "test"},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert result.status_code == 201
    assert result.json()["status"] is True


async def test_get_post(client):
    user_token = await login_user(client)

    result = await client.get(
        "/api/v1/posts/get",
        params={"post_id": 1},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert result.status_code == 200
    assert result.json() == {"id": 1, "text": "test", "author_id": 1}


async def test_get_all_posts(client):
    user_token = await login_user(client)

    result = await client.get(
        "/api/v1/posts/all",
        params={"post_id": 1},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert result.status_code == 200
    assert result.json()[0] == {"id": 1, "text": "test", "author_id": 1}


async def test_update_post(client):
    user_token = await login_user(client)

    result_update = await client.put(
        "/api/v1/posts/update",
        json={"post_id": 1, "data": {"text": "test2"}},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    result_get = await client.get(
        "/api/v1/posts/get",
        params={"post_id": 1},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert result_update.status_code == 200
    assert result_update.json()["status"] is True
    assert result_get.status_code == 200
    assert result_get.json() == {"id": 1, "text": "test2", "author_id": 1}


async def test_delete_post(client):
    user_token = await login_user(client)

    result_delete = await client.delete(
        "/api/v1/posts/delete",
        params={"post_id": 1},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    result_get = await client.get(
        "/api/v1/posts/get",
        params={"post_id": 1},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert result_delete.status_code == 200
    assert result_delete.json()["status"] is True
    assert result_get.status_code == 404
