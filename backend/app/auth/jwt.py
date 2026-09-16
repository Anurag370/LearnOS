from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings

ACCESS_TOKEN_EXPIRES_MINUTES = 60

def create_access_token(user_id:int, expires_delta:timedelta | None = None,) -> str:

    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta

    payload = {"sub": str(user_id), "exp": expire}

    return jwt.encode(payload, settings.secret_key, algorithm = settings.jwt_algorithm)

def decode_access_token(token: str):

    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])