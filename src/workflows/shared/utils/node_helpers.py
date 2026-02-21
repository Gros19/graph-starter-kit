"""Common node utilities."""
import structlog

from src.infrastructure.llm_provider.base import GenerationConfig, LLMProvider, LLMResponse
from src.domain.exceptions import LLMProviderError

logger = structlog.get_logger()


async def call_llm_safe(
    llm: LLMProvider,
    prompt: str,
    config: GenerationConfig | None = None,
) -> LLMResponse:
    """Call LLM with error handling."""
    try:
        return await llm.generate(prompt, config)
    except Exception as e:
        logger.error("LLM call failed", provider=llm.provider_name, error=str(e))
        raise LLMProviderError(
            message=f"LLM generation failed: {e}",
            provider=llm.provider_name,
        ) from e
