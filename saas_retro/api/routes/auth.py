from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from saas_retro.api.deps import get_current_user, get_db_session
from saas_retro.api.schemas.auth import AuthLoginRequest, AuthLoginResponse, CurrentUserResponse
from saas_retro.api.schemas.common import ApiResponse
from saas_retro.core.security import build_access_token, verify_password
from saas_retro.db.models.organization import User

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=ApiResponse[AuthLoginResponse])
def login(
    payload: AuthLoginRequest,
    session: Session = Depends(get_db_session),
) -> ApiResponse[AuthLoginResponse]:
    stmt = select(User).where(
        User.login_id == payload.login_id,
        User.is_deleted.is_(False),
        User.status == "active",
    )
    user = session.execute(stmt).scalar_one_or_none()

    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token, expires_in = build_access_token(user_id=user.id, school_id=user.school_id, role=user.role)
    response = AuthLoginResponse(
        access_token=token,
        token_type="Bearer",
        expires_in=expires_in,
        user=CurrentUserResponse.model_validate(user),
    )
    return ApiResponse.ok(response)


@router.get("/me", response_model=ApiResponse[CurrentUserResponse])
def get_me(
    current_user: User = Depends(get_current_user),
) -> ApiResponse[CurrentUserResponse]:
    return ApiResponse.ok(CurrentUserResponse.model_validate(current_user))
