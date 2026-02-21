"""FastMCP server instance."""
from fastmcp import FastMCP

mcp = FastMCP("graph-starter-kit")

# Register tools and resources
from src.mcp.tools import chat_tool  # noqa: F401, E402
from src.mcp.resources import thread_resource  # noqa: F401, E402
