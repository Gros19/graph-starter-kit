"""Chat assistant router."""
import structlog
from fastapi import APIRouter
from langchain_core.messages import HumanMessage

from src.api.schemas.chat import ChatRequest, ChatResponse
from src.domain.exceptions import WorkflowError
from src.workflows.assistants.chat.graph import get_chat_graph

router = APIRouter(prefix="/assistants/chat", tags=["chat"])
logger = structlog.get_logger()


@router.post("/run", response_model=ChatResponse)
async def run_chat(request: ChatRequest) -> ChatResponse:
    """Run a chat turn."""
    logger.info("Chat request", thread_id=request.thread_id)

    try:
        graph = await get_chat_graph()
        config = {"configurable": {"thread_id": request.thread_id}}
        result = await graph.ainvoke(
            {"messages": [HumanMessage(content=request.message)], "thread_id": request.thread_id},
            config=config,
        )
    except Exception as e:
        raise WorkflowError(f"Chat failed: {e}", thread_id=request.thread_id) from e

    messages = result.get("messages", [])
    reply = messages[-1].content if messages else ""

    return ChatResponse(thread_id=request.thread_id, reply=reply)


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
