"""Chat workflow graph assembly."""
from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from src.workflows.assistants.chat.nodes import call_model
from src.workflows.assistants.chat.state import ChatState


def build_chat_graph() -> StateGraph:
    """Build the chat StateGraph (not compiled)."""
    builder = StateGraph(ChatState)
    builder.add_node("call_model", call_model)
    builder.add_edge(START, "call_model")
    builder.add_edge("call_model", END)
    return builder


async def get_chat_graph():
    """Get compiled chat graph with PostgreSQL checkpointer."""
    from src.workflows.shared.checkpointer import get_checkpointer
    checkpointer = await get_checkpointer()
    builder = build_chat_graph()
    return builder.compile(checkpointer=checkpointer)
