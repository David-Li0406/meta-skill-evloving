"""
MCP Server Template - Basic server with tools, resources, and prompts.

Usage:
    python mcp_server.py                    # stdio transport (default)
    python mcp_server.py --http             # streamable-http transport
    uvicorn mcp_server:app --reload         # as ASGI app

Replace with your own tools, resources, and prompts.
"""

import argparse
import contextlib
from dataclasses import dataclass
from typing import Optional

from mcp.server.fastmcp import Context, FastMCP


# ============================================================================
# Application Context (for shared resources like database)
# ============================================================================

@dataclass
class AppContext:
    """Application context passed to tools via lifespan."""
    # Add your shared resources here, e.g.:
    # db: Database
    # config: dict
    pass


@contextlib.asynccontextmanager
async def app_lifespan(server: FastMCP):
    """
    Manage application lifecycle.

    Initialize resources on startup, clean up on shutdown.
    """
    # Startup: Initialize resources
    # db = await Database.connect()
    # config = load_config()

    try:
        yield AppContext()  # Pass to tools via ctx.request_context.lifespan_context
    finally:
        # Shutdown: Clean up resources
        # await db.disconnect()
        pass


# ============================================================================
# MCP Server Instance
# ============================================================================

mcp = FastMCP(
    name="My MCP Server",
    lifespan=app_lifespan,
    stateless_http=True,  # Recommended for production
    json_response=True,   # Return JSON instead of SSE
)

# Configure HTTP path (when mounted in Starlette/FastAPI)
mcp.settings.streamable_http_path = "/"


# ============================================================================
# Tools - Actions and computations
# ============================================================================

@mcp.tool()
def hello(name: str = "World") -> dict:
    """
    Say hello to someone.

    Args:
        name: The name to greet (default: World)

    Returns:
        A greeting message
    """
    return {
        "message": f"Hello, {name}!",
        "success": True,
    }


@mcp.tool()
def add_numbers(a: int, b: int) -> dict:
    """
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of the two numbers
    """
    return {
        "result": a + b,
        "operation": f"{a} + {b}",
    }


@mcp.tool()
async def process_with_progress(items: list[str], ctx: Context) -> dict:
    """
    Process items with progress reporting.

    Args:
        items: List of items to process
        ctx: MCP context (automatically injected)

    Returns:
        Processing results
    """
    total = len(items)
    await ctx.info(f"Starting to process {total} items")

    results = []
    for i, item in enumerate(items):
        # Report progress
        await ctx.report_progress(
            progress=(i + 1) / total,
            total=1.0,
            message=f"Processing {i + 1}/{total}: {item}",
        )

        # Process item
        results.append(f"Processed: {item}")
        await ctx.debug(f"Completed: {item}")

    await ctx.info("Processing complete")
    return {
        "success": True,
        "processed": len(results),
        "results": results,
    }


# ============================================================================
# Resources - Read-only data access
# ============================================================================

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting as a resource."""
    return f"Hello, {name}! Welcome to the MCP server."


@mcp.resource("config://app")
def get_app_config() -> str:
    """Get application configuration."""
    import json
    return json.dumps({
        "name": "My MCP Server",
        "version": "1.0.0",
        "features": ["tools", "resources", "prompts"],
    })


# ============================================================================
# Prompts - Reusable prompt templates
# ============================================================================

@mcp.prompt()
def assistant_prompt(name: str = "User") -> str:
    """
    Generate a system prompt for the assistant.

    Args:
        name: User's name for personalization
    """
    return f"""You are a helpful assistant for {name}.

Available tools:
- hello: Greet someone
- add_numbers: Add two numbers
- process_with_progress: Process items with progress updates

Be helpful, concise, and friendly."""


@mcp.prompt()
def help_prompt() -> str:
    """Generate help information for users."""
    return """Welcome! Here's what I can help you with:

**Greetings**
- Say "hello" to get a greeting
- Customize with a name: "hello John"

**Math**
- "add 5 and 3" - Add numbers together

**Processing**
- "process these items: a, b, c" - Process a list

Just ask what you need!"""


# ============================================================================
# ASGI App (for mounting in Starlette/FastAPI)
# ============================================================================

@contextlib.asynccontextmanager
async def asgi_lifespan(app):
    """Lifespan manager for ASGI mounting."""
    async with mcp.session_manager.run():
        yield


# Create ASGI app for uvicorn/mounting
from starlette.applications import Starlette
from starlette.routing import Mount

app = Starlette(
    routes=[
        Mount("/", app=mcp.streamable_http_app()),
    ],
    lifespan=asgi_lifespan,
)


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Server")
    parser.add_argument("--http", action="store_true", help="Use HTTP transport")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP")
    args = parser.parse_args()

    if args.http:
        mcp.run(transport="streamable-http", port=args.port)
    else:
        mcp.run()  # stdio transport (default)
