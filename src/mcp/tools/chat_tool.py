"""Chat MCP tool — wrapper around the chat workflow."""
import structlog
from langchain_core.messages import HumanMessage

from src.mcp.server import mcp

logger = structlog.get_logger()


@mcp.tool()
async def chat(thread_id: str, message: str) -> str:
    """
    Send a message in a conversation thread and get a reply.

    Args:
        thread_id: Unique identifier for the conversation thread.
                   Use the same ID to continue a conversation.
        message: The user's message text.

    Returns:
        The AI assistant's reply.
    """
    from src.workflows.assistants.chat.graph import get_chat_graph

    logger.info("MCP chat tool called", thread_id=thread_id)
    graph = await get_chat_graph()
    config = {"configurable": {"thread_id": thread_id}}
    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=message)], "thread_id": thread_id},
        config=config,
    )
    messages = result.get("messages", [])
    return messages[-1].content if messages else ""
