"""Thread MCP resource — expose conversation history."""
import structlog

from src.mcp.server import mcp

logger = structlog.get_logger()


@mcp.resource("mcp://threads/{thread_id}")
async def get_thread_messages(thread_id: str) -> str:
    """
    Get the message history for a conversation thread.

    Args:
        thread_id: The thread ID to retrieve messages for.

    Returns:
        Formatted conversation history as text.
    """
    from src.workflows.assistants.chat.graph import get_chat_graph

    graph = await get_chat_graph()
    config = {"configurable": {"thread_id": thread_id}}

    try:
        state = await graph.aget_state(config)
        messages = state.values.get("messages", [])
        if not messages:
            return f"Thread '{thread_id}' has no messages yet."

        lines = [f"Thread: {thread_id}", "=" * 40]
        for msg in messages:
            role = "Human" if msg.__class__.__name__ == "HumanMessage" else "AI"
            content = msg.content if isinstance(msg.content, str) else str(msg.content)
            lines.append(f"{role}: {content}")
        return "\n".join(lines)
    except Exception as e:
        logger.warning("Failed to get thread state", thread_id=thread_id, error=str(e))
        return f"Thread '{thread_id}' not found or empty."
