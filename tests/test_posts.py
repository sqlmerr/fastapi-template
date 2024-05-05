from typing import Any

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


async def get_user(client: AsyncClient, access_token: str) -> dict[str, Any]:
    user = await client.get(
        "/api/v1/auth/profile",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )

    return user.json()


async def test_create_post(client):
    user_token = await login_user(client)

    result = await client.post(
        "/api/v1/posts/",
        json={"text": "test"},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert result.status_code == 201
    assert result.json()["status"] is True


async def test_get_post(client):
    user_token = await login_user(client)
    user = await get_user(client, user_token)

    posts = await client.get(
        "/api/v1/posts/",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    post_id = posts.json()[0]["id"]

    result = await client.get(
        f"/api/v1/posts/{post_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert result.status_code == 200
    assert result.json() == {"id": post_id, "text": "test", "author_id": user["id"]}


async def test_get_all_posts(client):
    user_token = await login_user(client)
    user = await get_user(client, user_token)

    result = await client.get(
        "/api/v1/posts/",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    first_post = result.json()[0]

    assert result.status_code == 200
    assert first_post["text"] == "test"
    assert first_post["author_id"] == user["id"]


async def test_update_post(client):
    user_token = await login_user(client)
    user = await get_user(client, user_token)

    posts = await client.get(
        "/api/v1/posts/",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    post_id = posts.json()[0]["id"]

    result_update = await client.put(
        "/api/v1/posts/",
        json={"id": post_id, "text": "test2"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    result_get = await client.get(
        f"/api/v1/posts/{post_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert result_update.status_code == 200
    assert result_update.json()["status"] is True
    assert result_get.status_code == 200
    assert result_get.json() == {
        "id": post_id,
        "text": "test2",
        "author_id": user["id"],
    }


async def test_delete_post(client):
    user_token = await login_user(client)

    posts = await client.get(
        "/api/v1/posts/",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    post_id = posts.json()[0]["id"]

    result_delete = await client.delete(
        "/api/v1/posts/",
        params={"post_id": post_id},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    result_get = await client.get(
        f"/api/v1/posts/{post_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert result_delete.status_code == 200
    assert result_delete.json()["status"] is True
    assert result_get.status_code == 404
