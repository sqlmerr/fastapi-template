from conftest import client


def test_register():
    result = client.post(
        "/api/v1/auth/register/", json={"username": "tester", "password": "testpass"}
    )

    assert result.status_code == 201
