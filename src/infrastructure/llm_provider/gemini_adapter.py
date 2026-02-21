"""Google Gemini adapter."""
from collections.abc import AsyncGenerator

from google import genai

from src.infrastructure.llm_provider.base import (
    GenerationConfig,
    LLMProvider,
    LLMResponse,
    LLMResponseMetadata,
    StreamChunk,
    TokenUsage,
)


class GeminiAdapter(LLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash") -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model

    @property
    def provider_name(self) -> str:
        return "google"

    @property
    def model_name(self) -> str:
        return self._model

    async def generate(self, prompt: str, config: GenerationConfig | None = None) -> LLMResponse:
        config = config or GenerationConfig()
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
        )
        content = response.text or ""
        return LLMResponse(
            content=content,
            usage=TokenUsage(),
            metadata=LLMResponseMetadata(
                model=self._model,
                provider=self.provider_name,
            ),
        )

    async def stream_generate(
        self, prompt: str, config: GenerationConfig | None = None
    ) -> AsyncGenerator[StreamChunk, None]:
        async for chunk in await self._client.aio.models.generate_content_stream(
            model=self._model,
            contents=prompt,
        ):
            if chunk.text:
                yield StreamChunk(content=chunk.text)

    async def estimate_tokens(self, text: str) -> int:
        return len(text) // 4
