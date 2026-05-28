# MCP Tools Usage Guide

This document provides detailed information about using the `@mcp.tool()` decorator to define tools in your MCP server.

## Overview

Tools are functions that can be called remotely by MCP clients. They perform actions and return results, forming the primary way external systems interact with your server.

## Basic Tool Definition

### Simple Tool
```python
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
```

### Tool with Multiple Parameters
```python
@mcp.tool()
def calculate_area(width: float, height: float, unit: str = "meters") -> dict:
    """Calculate area with units."""
    area = width * height
    return {
        "area": area,
        "unit": unit,
        "width": width,
        "height": height
    }
```

### Tool with Complex Return Types
```python
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class SearchResult:
    id: str
    title: str
    score: float
    metadata: Dict[str, any]

@mcp.tool()
def search_documents(query: str, limit: int = 10) -> List[SearchResult]:
    """Search for documents and return structured results."""
    results = perform_search(query, limit)
    return [
        SearchResult(id=r["id"], title=r["title"], score=r["score"], metadata=r["meta"])
        for r in results
    ]
```

## Asynchronous Tools

### Async Tool
```python
@mcp.tool()
async def fetch_data_async(url: str) -> str:
    """Fetch data from a URL asynchronously."""
    import aiohttp

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### Async Tool with Context
```python
from mcp_use.server import Context

@mcp.tool()
async def intelligent_search(query: str, ctx: Context) -> str:
    """Search tool that leverages context for LLM assistance."""
    # Use context to get LLM assistance
    refined_result = await ctx.sample(
        messages=f"Refine this search query: {query}",
        max_tokens=100,
        temperature=0.7
    )

    refined_query = refined_result.content.text

    # Log progress
    await ctx.log('info', f'Searching with refined query: {refined_query}')

    # Perform search
    results = await async_search(refined_query)
    return format_results(results)
```

## Tool Parameters

### Tool Decorator Parameters
```python
@mcp.tool(
    name="custom-tool-name",     # Optional custom name (defaults to function name)
    title="Custom Tool Title",   # Optional human-readable title
    description="Description of what this tool does",  # Optional description
    icons=[{"type": "image/png", "uri": "icon.png"}]     # Optional icons
)
def custom_tool(parameter: str) -> str:
    """Tool with custom parameters."""
    return f"Custom tool result: {parameter}"
```

## State Management Patterns

### Tool with Internal State
```python
from threading import Lock
from collections import defaultdict

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.lock = Lock()

    def create_session(self, user_id: str) -> str:
        import uuid
        session_id = str(uuid.uuid4())
        with self.lock:
            self.sessions[session_id] = {
                "user_id": user_id,
                "created_at": __import__('datetime').datetime.now(),
                "active": True
            }
        return session_id

    def get_session(self, session_id: str):
        with self.lock:
            return self.sessions.get(session_id)

session_manager = SessionManager()

@mcp.tool()
def create_user_session(user_id: str) -> str:
    """Create a new user session."""
    return session_manager.create_session(user_id)

@mcp.tool()
def get_session_info(session_id: str) -> dict:
    """Get information about a session."""
    session = session_manager.get_session(session_id)
    if not session:
        raise ValueError(f"Session {session_id} not found")
    return session
```

## Resource Management Patterns

### Tool with Resource Cleanup
```python
from contextlib import contextmanager
import tempfile
import os

@contextmanager
def temporary_file(suffix: str = ""):
    """Context manager for temporary files that ensures cleanup."""
    temp_fd, temp_path = tempfile.mkstemp(suffix=suffix)
    try:
        os.close(temp_fd)  # Close the file descriptor
        yield temp_path
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@mcp.tool()
def process_document_content(content: str) -> str:
    """Process document content using temporary file."""
    with temporary_file(suffix=".txt") as temp_path:
        # Write content to temporary file
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Process the file
        result = process_document_file(temp_path)

        # File is automatically cleaned up
        return result
```

## Async Patterns

### Tool with Concurrent Operations
```python
import asyncio

@mcp.tool()
async def fetch_multiple_sources(urls: list[str]) -> list[dict]:
    """Fetch data from multiple sources concurrently."""
    async def fetch_single(url: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return {
                        "url": url,
                        "status": response.status,
                        "data": await response.text()
                    }
        except Exception as e:
            return {
                "url": url,
                "error": str(e)
            }

    # Execute all requests concurrently
    results = await asyncio.gather(*[fetch_single(url) for url in urls])
    return results
```

## Best Practices

### For Tools
- Always provide clear docstrings explaining what the tool does
- Validate input parameters
- Handle errors gracefully
- Use appropriate return types
- Consider async functions for I/O-bound operations
- Implement proper authentication and authorization
- Apply rate limiting where appropriate
- Use structured logging for observability
- Include comprehensive error handling
