"""Anthropic Claude adapter."""
from collections.abc import AsyncGenerator

import anthropic

from src.infrastructure.llm_provider.base import (
    GenerationConfig,
    LLMProvider,
    LLMResponse,
    LLMResponseMetadata,
    StreamChunk,
    TokenUsage,
)


class AnthropicAdapter(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-5-haiku-20241022") -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model

    @property
    def provider_name(self) -> str:
        return "anthropic"

    @property
    def model_name(self) -> str:
        return self._model

    async def generate(self, prompt: str, config: GenerationConfig | None = None) -> LLMResponse:
        config = config or GenerationConfig()
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.content[0].text if response.content else ""
        return LLMResponse(
            content=content,
            usage=TokenUsage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            ),
            metadata=LLMResponseMetadata(
                model=self._model,
                provider=self.provider_name,
                finish_reason=response.stop_reason or "stop",
            ),
        )

    async def stream_generate(
        self, prompt: str, config: GenerationConfig | None = None
    ) -> AsyncGenerator[StreamChunk, None]:
        config = config or GenerationConfig()
        async with self._client.messages.stream(
            model=self._model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            async for text in stream.text_stream:
                yield StreamChunk(content=text)

    async def estimate_tokens(self, text: str) -> int:
        return len(text) // 4
