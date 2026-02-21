"""PostgreSQL checkpointer for LangGraph."""
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from src.core.settings import get_settings

_pool: AsyncConnectionPool | None = None
_checkpointer: AsyncPostgresSaver | None = None


async def get_checkpointer() -> AsyncPostgresSaver:
    """Get or create the PostgreSQL checkpointer using a persistent connection pool."""
    global _pool, _checkpointer
    if _checkpointer is None:
        settings = get_settings()
        conn_string = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
        _pool = AsyncConnectionPool(
            conninfo=conn_string,
            max_size=10,
            open=False,
            kwargs={"autocommit": True, "prepare_threshold": 0},
        )
        await _pool.open()
        _checkpointer = AsyncPostgresSaver(_pool)
        await _checkpointer.setup()
    return _checkpointer
