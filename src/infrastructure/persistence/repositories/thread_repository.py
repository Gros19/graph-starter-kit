"""Thread repository."""
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.persistence.models.thread import Thread


async def create_thread(session: AsyncSession, title: str | None = None) -> Thread:
    """Create a new thread."""
    thread = Thread(title=title)
    session.add(thread)
    await session.flush()
    return thread


async def get_thread(session: AsyncSession, thread_id: UUID) -> Thread | None:
    """Get a thread by ID."""
    result = await session.execute(select(Thread).where(Thread.id == thread_id))
    return result.scalar_one_or_none()
