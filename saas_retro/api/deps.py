from __future__ import annotations

from collections.abc import Generator
from collections.abc import Callable

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from saas_retro.db import get_session
from saas_retro.db.enums import UserRole
from saas_retro.db.models.organization import User
from saas_retro.core.security import TokenPayload, decode_access_token


def get_db_session() -> Generator[Session, None, None]:
    session = get_session()
    try:
        yield session
    finally:
        session.close()


def get_bearer_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return token


def get_token_payload(token: str = Depends(get_bearer_token)) -> TokenPayload:
    try:
        return decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


def get_current_user(
    payload: TokenPayload = Depends(get_token_payload),
    session: Session = Depends(get_db_session),
) -> User:
    stmt = select(User).where(User.id == payload.user_id, User.is_deleted.is_(False))
    user = session.execute(stmt).scalar_one_or_none()
    if user is None or user.status != "active":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_roles(*roles: UserRole | str) -> Callable[[User], User]:
    allowed_roles = {str(role) for role in roles}

    def _role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return current_user

    return _role_checker
