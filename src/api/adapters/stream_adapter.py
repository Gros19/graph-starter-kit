"""LangGraph astream_events → SSE/NDJSON adapter."""
import json
from collections.abc import AsyncGenerator
from typing import Any


async def stream_graph_as_ndjson(
    graph_stream: AsyncGenerator[dict[str, Any], None],
) -> AsyncGenerator[str, None]:
    """Convert LangGraph event stream to NDJSON lines."""
    async for event in graph_stream:
        yield json.dumps(event) + "\n"
