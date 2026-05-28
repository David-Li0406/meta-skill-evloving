"""
Example MCP Server using the official MCP SDK

This is a basic example demonstrating how to create an MCP server using the official SDK.
"""

from mcp.server.fastmcp import FastMCP
from starlette.responses import JSONResponse
from starlette.requests import Request
import os
import psutil
from datetime import datetime

# Create server instance using the official SDK
mcp = FastMCP(
    name=os.getenv("MCP_SERVER_NAME", "example-mcp-server"),
    json_response=True,
    host="127.0.0.1",
    port=8080,
)

@mcp.tool()
def hello_world(name: str = "World") -> str:
    """Simple tool that greets the user."""
    return f"Hello, {name}! This is your MCP server speaking."

@mcp.tool()
def echo(text: str) -> str:
    """Echo back the provided text."""
    return text

@mcp.tool()
def get_system_info() -> dict:
    """Get basic system information."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "timestamp": datetime.now().isoformat()
    }

# Health check endpoint
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    """Health check endpoint for the server."""
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": os.getenv("MCP_SERVER_NAME", "example-mcp-server"),
        "version": "1.0.0",
    })

if __name__ == "__main__":
    # Run the server
    mcp.run(transport=os.getenv("MCP_TRANSPORT", "streamable-http"))
