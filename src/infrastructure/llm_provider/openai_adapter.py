"""OpenAI adapter."""
from collections.abc import AsyncGenerator

from openai import AsyncOpenAI

from src.infrastructure.llm_provider.base import (
    GenerationConfig,
    LLMProvider,
    LLMResponse,
    LLMResponseMetadata,
    StreamChunk,
    TokenUsage,
)


class OpenAIAdapter(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def model_name(self) -> str:
        return self._model

    async def generate(self, prompt: str, config: GenerationConfig | None = None) -> LLMResponse:
        config = config or GenerationConfig()
        response = await self._client.chat.completions.create(
            model=self._model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content or ""
        usage = response.usage
        return LLMResponse(
            content=content,
            usage=TokenUsage(
                prompt_tokens=usage.prompt_tokens if usage else 0,
                completion_tokens=usage.completion_tokens if usage else 0,
                total_tokens=usage.total_tokens if usage else 0,
            ),
            metadata=LLMResponseMetadata(
                model=self._model,
                provider=self.provider_name,
                finish_reason=response.choices[0].finish_reason or "stop",
            ),
        )

    async def stream_generate(
        self, prompt: str, config: GenerationConfig | None = None
    ) -> AsyncGenerator[StreamChunk, None]:
        config = config or GenerationConfig()
        stream = await self._client.chat.completions.create(
            model=self._model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                yield StreamChunk(content=delta)

    async def estimate_tokens(self, text: str) -> int:
        return len(text) // 4
