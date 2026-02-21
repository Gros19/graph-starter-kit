"""Chat workflow state definition."""
from langgraph.graph import MessagesState


class ChatState(MessagesState):
    """State for the chat workflow."""
    thread_id: str
