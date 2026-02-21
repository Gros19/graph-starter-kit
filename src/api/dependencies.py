"""FastAPI dependencies."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.llm_provider.base import LLMProvider
from src.infrastructure.llm_provider.factory import create_llm_provider
from src.infrastructure.persistence.database import get_db_session


def get_llm_provider() -> LLMProvider:
    """Dependency for LLM provider."""
    return create_llm_provider()


LLMProviderDep = Annotated[LLMProvider, Depends(get_llm_provider)]
DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
