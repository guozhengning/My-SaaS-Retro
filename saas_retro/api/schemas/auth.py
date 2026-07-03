from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class AuthLoginRequest(BaseModel):
    login_id: str
    password: str


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    school_id: int | None
    role: str
    login_id: str
    name: str
    phone: str | None
    status: str


class AuthLoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: CurrentUserResponse
