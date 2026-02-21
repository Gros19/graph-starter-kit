"""LLM provider factory."""
from src.core.constants.enums import AIProvider
from src.core.settings import get_settings
from src.domain.exceptions import ConfigurationError
from src.infrastructure.llm_provider.base import LLMProvider


def create_llm_provider(
    provider_name: str | None = None,
    model: str | None = None,
) -> LLMProvider:
    """Create an LLM provider instance."""
    settings = get_settings()
    provider = provider_name or settings.default_ai_provider
    model = model or settings.default_model

    if provider == AIProvider.ANTHROPIC:
        from src.infrastructure.llm_provider.anthropic_adapter import AnthropicAdapter
        if not settings.anthropic_api_key:
            raise ConfigurationError("ANTHROPIC_API_KEY is not set")
        return AnthropicAdapter(api_key=settings.anthropic_api_key, model=model)

    elif provider == AIProvider.OPENAI:
        from src.infrastructure.llm_provider.openai_adapter import OpenAIAdapter
        if not settings.openai_api_key:
            raise ConfigurationError("OPENAI_API_KEY is not set")
        return OpenAIAdapter(api_key=settings.openai_api_key, model=model)

    elif provider == AIProvider.GOOGLE:
        from src.infrastructure.llm_provider.gemini_adapter import GeminiAdapter
        if not settings.google_ai_api_key:
            raise ConfigurationError("GOOGLE_AI_API_KEY is not set")
        return GeminiAdapter(api_key=settings.google_ai_api_key, model=model)

    else:
        raise ConfigurationError(f"Unsupported provider: {provider}")
