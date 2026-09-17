from app.auth.jwt import create_access_token, decode_access_token
from app.auth.security import hash_password, verify_password


def test_password_is_not_stored_as_plaintext():
    password = "password123"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_wrong_password_is_rejected():
    password = "password123"

    hashed = hash_password(password)

    assert not verify_password(
        "wrong-password",
        hashed,
    )


def test_jwt_contains_user_id():
    token = create_access_token(user_id=42)

    payload = decode_access_token(token)

    assert payload["sub"] == "42"


def test_jwt_contains_expiration():
    token = create_access_token(user_id=42)

    payload = decode_access_token(token)

    assert "exp" in payload