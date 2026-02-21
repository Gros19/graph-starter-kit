"""Chat workflow unit tests."""
import pytest
from unittest.mock import AsyncMock, patch
from langchain_core.messages import HumanMessage, AIMessage

from src.workflows.assistants.chat.state import ChatState


def test_chat_state_structure():
    """ChatState should accept messages and thread_id."""
    state: ChatState = {"messages": [HumanMessage(content="Hello")], "thread_id": "test-1"}
    assert state["thread_id"] == "test-1"
    assert len(state["messages"]) == 1


@pytest.mark.asyncio
async def test_call_model_node(mock_llm):
    """call_model node should return AI message."""
    with patch("src.workflows.assistants.chat.nodes.create_llm_provider", return_value=mock_llm):
        from src.workflows.assistants.chat.nodes import call_model
        state: ChatState = {
            "messages": [HumanMessage(content="Hello")],
            "thread_id": "test-1",
        }
        result = await call_model(state)
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], AIMessage)
