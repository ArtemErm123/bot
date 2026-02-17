import uuid
from contextvars import ContextVar

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.logging import configure_logging
from app.core.settings import get_settings
from app.schemas.common import ProblemDetails

trace_id_ctx: ContextVar[str | None] = ContextVar("trace_id", default=None)
settings = get_settings()


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

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
