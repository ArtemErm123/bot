from __future__ import annotations

import logging
import uuid
from contextvars import ContextVar
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.reports import router as reports_router
from app.api.routes import router as routes_router
from app.api.v1.router import api_router
from app.core.logging import configure_logging
from app.core.settings import get_settings
from app.schemas.common import ProblemDetails
from app.services.connector_service import ConnectorConfig, ConnectorService, MockConnector, RetryPolicy
from app.services.report_service import ReportService
from app.storage.report_store import ReportStore

logging.basicConfig(level=logging.INFO)

trace_id_ctx: ContextVar[str | None] = ContextVar("trace_id", default=None)
settings = get_settings()

connector_config = ConnectorConfig(
    endpoint="https://mock.local/api/reports",
    token="dev-token",
    timeout_seconds=3,
    retry_policy=RetryPolicy(max_attempts=3, backoff_seconds=0.05),
)
connector_service = ConnectorService(connector=MockConnector(config=connector_config))
report_store = ReportStore()
report_service = ReportService(
    store=report_store,
    connector_service=connector_service,
    artifacts_dir=Path("backend/artifacts"),
)


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        openapi_tags=[
            {"name": "projects", "description": "Project CRUD"},
            {"name": "calculate", "description": "Engineering calculations"},
            {"name": "predict", "description": "Lifetime prediction"},
            {"name": "reports", "description": "Report generation and access"},
        ],
    )

    @app.middleware("http")
    async def trace_id_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
        trace_id = request.headers.get("X-Trace-Id", str(uuid.uuid4()))
        trace_id_ctx.set(trace_id)
        response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id
        return response

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        body = ProblemDetails(
            type="about:blank",
            title="HTTP Error",
            status=exc.status_code,
            detail=str(exc.detail),
            instance=request.url.path,
            trace_id=trace_id_ctx.get(),
        )
        return JSONResponse(status_code=exc.status_code, content=body.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        body = ProblemDetails(
            type="https://example.com/problem/validation-error",
            title="Validation Error",
            status=422,
            detail=str(exc),
            instance=request.url.path,
            trace_id=trace_id_ctx.get(),
        )
        return JSONResponse(status_code=422, content=body.model_dump())

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        body = ProblemDetails(
            type="https://example.com/problem/internal-error",
            title="Internal Server Error",
            status=500,
            detail=str(exc),
            instance=request.url.path,
            trace_id=trace_id_ctx.get(),
        )
        return JSONResponse(status_code=500, content=body.model_dump())

    app.include_router(routes_router, prefix="/api")
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    app.include_router(reports_router)
    app.state.report_service = report_service

    return app


# Final ASGI export used by tests and runtime.
app = create_app()
