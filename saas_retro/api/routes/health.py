from __future__ import annotations

from fastapi import APIRouter

from saas_retro.api.schemas.common import ApiResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ApiResponse[dict[str, str]])
def health_check() -> ApiResponse[dict[str, str]]:
    return ApiResponse.ok({"status": "ok"})


@router.get("/api/v1/ping", response_model=ApiResponse[dict[str, str]])
def ping() -> ApiResponse[dict[str, str]]:
    return ApiResponse.ok({"message": "pong"})
