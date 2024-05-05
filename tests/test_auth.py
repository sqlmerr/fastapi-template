async def test_register(client):
    result = await client.post(
        "/api/v1/auth/register", json={"username": "tester", "password": "testpass"}
    )

    assert result.status_code == 201


async def test_login(client):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    result_login_not_found = await client.post(
        "/api/v1/auth/token",
        data={"username": "not_tester", "password": "password"},
        headers=headers,
    )

    result_login_unauthorized = await client.post(
        "/api/v1/auth/token",
        data={"username": "tester", "password": "some_password"},
        headers=headers,
    )

    result_login = await client.post(
        "/api/v1/auth/token",
        data={"username": "tester", "password": "testpass"},
        headers=headers,
    )

    assert result_login_not_found.status_code == 404
    assert result_login_unauthorized.status_code == 401
    assert result_login.status_code == 200
    assert result_login.json()["token_type"].lower() == "bearer"

    result_profile = await client.get(
        "/api/v1/auth/profile",
        headers={"Authorization": f"Bearer {result_login.json()['access_token']}"},
    )
    profile_json = result_profile.json()

    assert result_profile.status_code == 200
    assert profile_json["username"] == "tester"
    assert profile_json["disabled"] is False
