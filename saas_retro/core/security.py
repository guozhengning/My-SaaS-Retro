from __future__ import annotations

from datetime import UTC, datetime, timedelta
import hashlib
import hmac
from dataclasses import dataclass

import jwt

from saas_retro.config import get_settings


@dataclass(frozen=True)
class TokenPayload:
    user_id: int
    school_id: int | None
    role: str
    exp: int


def is_password_hashed(stored_password: str) -> bool:
    return stored_password.startswith("sha256$")


def verify_password(plain_password: str, stored_password: str) -> bool:
    if not stored_password:
        return False

    if stored_password.startswith("sha256$"):
        _, hashed_value = stored_password.split("$", 1)
        sha256_value = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return hmac.compare_digest(sha256_value, hashed_value)

    if hmac.compare_digest(plain_password, stored_password):
        return True

    sha256_value = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return hmac.compare_digest(sha256_value, stored_password)


def needs_password_rehash(stored_password: str) -> bool:
    return bool(stored_password) and not is_password_hashed(stored_password)


def hash_password(plain_password: str) -> str:
    hashed_value = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return f"sha256${hashed_value}"


def build_access_token(*, user_id: int, school_id: int | None, role: str) -> tuple[str, int]:
    settings = get_settings()
    expires_delta = timedelta(minutes=settings.auth_access_token_expire_minutes)
    expire_at = datetime.now(UTC) + expires_delta
    payload = {
        "user_id": user_id,
        "school_id": school_id,
        "role": role,
        "exp": expire_at,
    }
    token = jwt.encode(
        payload,
        settings.auth_secret_key,
        algorithm=settings.auth_algorithm,
    )
    return token, int(expires_delta.total_seconds())


def decode_access_token(token: str) -> TokenPayload:
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.auth_secret_key,
            algorithms=[settings.auth_algorithm],
        )
        return TokenPayload(
            user_id=int(payload["user_id"]),
            school_id=payload.get("school_id"),
            role=str(payload["role"]),
            exp=int(payload["exp"]),
        )
    except jwt.PyJWTError as exc:
        raise ValueError("Invalid token") from exc
