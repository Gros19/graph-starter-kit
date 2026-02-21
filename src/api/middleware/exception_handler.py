"""Global exception handlers."""
import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import BaseAPIException

logger = structlog.get_logger()


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers."""

    @app.exception_handler(BaseAPIException)
    async def handle_api_exception(request: Request, exc: BaseAPIException) -> JSONResponse:
        logger.warning(
            "API exception",
            path=request.url.path,
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception) -> JSONResponse:
        logger.error("Unhandled exception", path=request.url.path, error=str(exc), exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "INTERNAL_ERROR", "message": "An unexpected error occurred"},
        )
