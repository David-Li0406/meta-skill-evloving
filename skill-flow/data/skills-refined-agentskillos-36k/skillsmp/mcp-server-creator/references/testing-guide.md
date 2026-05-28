# MCP Server Testing Guide

This document provides comprehensive guidance on testing MCP servers using the official Python SDK.

## Overview

The Python SDK provides a `Client` class for testing MCP servers with an in-memory transport. This makes it easy to write tests without network overhead. The Client class simulates the real MCP protocol interactions but runs entirely in memory, making tests fast and isolated.

### Install the dependencies
```bash
# Using pip
pip install inline-snapshot pytest anyio

# Using uv
uv add inline-snapshot pytest anyio
```

The `pytest` framework is used for testing, and `inline-snapshot` is a library that allows you to take snapshots of the output of your tests. This makes it easier to create tests for your server - you don't need to use it, but it's recommended for best practices.

## Basic Test Setup

### Example Server to Test

```python title="calculator_server.py"
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def multiply(x: float, y: float) -> float:
    """Multiply two numbers."""
    return x * y
```

### Basic Test Example

```python title="test_calculator_server.py"
import pytest
from inline_snapshot import snapshot
from mcp import Client
from mcp.types import CallToolResult, TextContent

from server import app


@pytest.fixture
def anyio_backend():
    # When using `trio`, `anyio_backend` should be set as `"trio"`.
    return "asyncio"

@pytest.fixture
async def client():
    # The `client` fixture creates a connected client that can be reused across multiple tests.
    async with Client(app, raise_exceptions=True) as c:
        yield c

@pytest.mark.anyio
async def test_call_add_tool(client: Client):
    result = await client.call_tool("add", {"a": 1, "b": 2})
    assert result == snapshot(
        CallToolResult(
            content=[TextContent(type="text", text="3")],
            structuredContent={"result": 3},
        )
    )

@pytest.mark.anyio
async def test_call_multiply_tool(client: Client):
    result = await client.call_tool("multiply", {"a": 5, "b": 3})
    assert result == snapshot(
        CallToolResult(
            content=[TextContent(type="text", text="15")],
            structuredContent={"result": 15},
        )
    )
```
