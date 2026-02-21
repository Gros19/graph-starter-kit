"""Abstract LLM provider base classes."""
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from datetime import datetime

from pydantic import BaseModel, Field


class GenerationConfig(BaseModel):
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    stop_sequences: list[str] = Field(default_factory=list)


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMResponseMetadata(BaseModel):
    model: str
    provider: str
    finish_reason: str = "stop"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LLMResponse(BaseModel):
    content: str
    usage: TokenUsage = Field(default_factory=TokenUsage)
    metadata: LLMResponseMetadata


class StreamChunk(BaseModel):
    content: str
    delta_tokens: int = 0
    finish_reason: str | None = None


class LLMProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str: ...

    @property
    @abstractmethod
    def model_name(self) -> str: ...

    @abstractmethod
    async def generate(self, prompt: str, config: GenerationConfig | None = None) -> LLMResponse: ...

    @abstractmethod
    async def stream_generate(
        self, prompt: str, config: GenerationConfig | None = None
    ) -> AsyncGenerator[StreamChunk, None]: ...

    @abstractmethod
    async def estimate_tokens(self, text: str) -> int: ...
