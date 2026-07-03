from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from saas_retro.api.routes.auth import router as auth_router
from saas_retro.api.routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="SaaS Retro API",
        version="0.1.0",
        description="Campus SaaS backend API",
    )

    app.include_router(health_router)
    app.include_router(auth_router)

    @app.exception_handler(ValueError)
    async def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"code": 40001, "message": str(exc), "data": {}},
        )

    return app


app = create_app()
