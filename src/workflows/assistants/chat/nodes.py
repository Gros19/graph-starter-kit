"""Chat workflow nodes."""
import structlog
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.core.settings import get_settings
from src.infrastructure.llm_provider.factory import create_llm_provider
from src.workflows.assistants.chat.state import ChatState

logger = structlog.get_logger()


def _messages_to_prompt(messages: list) -> str:
    """Convert message history to a single prompt string."""
    parts = []
    for msg in messages:
        if isinstance(msg, SystemMessage):
            parts.append(f"System: {msg.content}")
        elif isinstance(msg, HumanMessage):
            parts.append(f"Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            parts.append(f"Assistant: {msg.content}")
        else:
            parts.append(str(msg.content))
    parts.append("Assistant:")
    return "\n".join(parts)


async def call_model(state: ChatState) -> dict:
    """Call LLM with the full conversation history."""
    settings = get_settings()
    llm = create_llm_provider()

    messages = state["messages"]
    prompt = _messages_to_prompt(messages)

    logger.info("Calling LLM", thread_id=state.get("thread_id"), model=llm.model_name)

    from src.infrastructure.llm_provider.base import GenerationConfig
    config = GenerationConfig(
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )
    response = await llm.generate(prompt, config)

    return {"messages": [AIMessage(content=response.content)]}
