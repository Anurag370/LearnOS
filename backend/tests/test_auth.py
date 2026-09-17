AUTH_PREFIX = "/api/v1/auth"


async def test_register_success(client):
    response = await client.post(
        f"{AUTH_PREFIX}/register",
        json={"email": "student@example.com", "password": "password123"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "student@example.com"
    assert data["role"] == "STUDENT"
    assert isinstance(data["id"], int)


async def test_register_duplicate_email(client, user_token):
    await user_token("dup@example.com")

    response = await client.post(
        f"{AUTH_PREFIX}/register",
        json={"email": "dup@example.com", "password": "password123"},
    )

    assert response.status_code == 409


async def test_register_rejects_short_password(client):
    response = await client.post(
        f"{AUTH_PREFIX}/register",
        json={"email": "short@example.com", "password": "short"},
    )

    assert response.status_code == 422


async def test_login_returns_token(client, user_token):
    token = await user_token("login@example.com")

    assert isinstance(token, str)
    assert token


async def test_login_wrong_password(client, user_token):
    await user_token("wrongpass@example.com")

    response = await client.post(
        f"{AUTH_PREFIX}/login",
        json={"email": "wrongpass@example.com", "password": "not-the-password"},
    )

    assert response.status_code == 401


async def test_login_unknown_email(client):
    response = await client.post(
        f"{AUTH_PREFIX}/login",
        json={"email": "nobody@example.com", "password": "password123"},
    )

    assert response.status_code == 401


async def test_me_returns_authenticated_user(client, user_token):
    token = await user_token("me@example.com")

    response = await client.get(f"{AUTH_PREFIX}/me", headers=_auth(token))

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["role"] == "STUDENT"


async def test_me_rejects_invalid_token(client):
    response = await client.get(f"{AUTH_PREFIX}/me", headers=_auth("not-a-real-token"))

    assert response.status_code == 401


async def test_me_requires_token(client):
    response = await client.get(f"{AUTH_PREFIX}/me")

    assert response.status_code == 401


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}