"""FastAPI application entry point with FastMCP mounted."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.settings import get_settings
from src.infrastructure.logging.setup import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup/shutdown events."""
    settings = get_settings()
    import structlog
    logger = structlog.get_logger()
    logger.info("Starting graph-starter-kit", debug=settings.debug, log_level=settings.log_level)
    yield
    logger.info("Shutting down graph-starter-kit")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Graph Starter Kit",
        description="FastAPI + FastMCP + LangGraph starter kit",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from src.api.middleware.exception_handler import register_exception_handlers
    register_exception_handlers(app)

    from src.api.routers.assistants.chat import router as chat_router
    app.include_router(chat_router, prefix="/v1")

    from src.mcp.server import mcp
    app.mount("/mcp", mcp.http_app(path="/"))

    return app


app = create_app()
