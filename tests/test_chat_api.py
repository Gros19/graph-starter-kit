"""FastAPI chat endpoint integration tests."""
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

from langchain_core.messages import AIMessage


@pytest.mark.asyncio
async def test_chat_run_endpoint():
    """POST /v1/assistants/chat/run should return reply."""
    mock_graph = AsyncMock()
    mock_graph.ainvoke = AsyncMock(return_value={
        "messages": [AIMessage(content="Hello! How can I help?")],
        "thread_id": "test-1",
    })

    async def mock_get_chat_graph():
        return mock_graph

    with patch("src.api.routers.assistants.chat.get_chat_graph", side_effect=mock_get_chat_graph):
        from app import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/v1/assistants/chat/run",
                json={"thread_id": "test-1", "message": "Hello"},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["thread_id"] == "test-1"
        assert "reply" in data


@pytest.mark.asyncio
async def test_chat_health_endpoint():
    """GET /v1/assistants/chat/health should return ok."""
    from app import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/v1/assistants/chat/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
