"""Pytest fixtures."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from src.infrastructure.llm_provider.base import GenerationConfig, LLMProvider, LLMResponse, LLMResponseMetadata, TokenUsage


class MockLLMProvider(LLMProvider):
    def __init__(self, response_text: str = "Hello! How can I help you?") -> None:
        self._response = response_text

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def model_name(self) -> str:
        return "mock-model"

    async def generate(self, prompt: str, config: GenerationConfig | None = None) -> LLMResponse:
        return LLMResponse(
            content=self._response,
            usage=TokenUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20),
            metadata=LLMResponseMetadata(model="mock-model", provider="mock"),
        )

    async def stream_generate(self, prompt: str, config: GenerationConfig | None = None):
        from src.infrastructure.llm_provider.base import StreamChunk
        yield StreamChunk(content=self._response)

    async def estimate_tokens(self, text: str) -> int:
        return len(text) // 4


@pytest.fixture
def mock_llm():
    return MockLLMProvider()
