"""Chat API schemas."""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    thread_id: str = Field(..., description="Conversation thread ID")
    message: str = Field(..., min_length=1, description="User message")


class ChatResponse(BaseModel):
    thread_id: str
    reply: str
    model: str | None = None
