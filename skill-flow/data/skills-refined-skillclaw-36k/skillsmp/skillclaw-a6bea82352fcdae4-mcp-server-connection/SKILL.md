---
name: mcp-server-connection
description: Use this skill when you need to create and configure various types of Model Context Protocol (MCP) server connections for OpenAI Agents SDK.
---

# MCP Server Connection Skill

This skill helps create and configure different types of Model Context Protocol (MCP) server connections in OpenAI Agents SDK, including HTTP, Server-Sent Events (SSE), stdio, and hosted servers.

## Purpose
- Create configurations for various MCP server types
- Configure connection parameters, authentication, and headers
- Manage tool discovery and communication with MCP servers

## Supported MCP Server Types
1. **HTTP with SSE**: For real-time event streaming from MCP servers.
2. **Hosted MCP**: For connecting to publicly accessible MCP servers with approval flows.
3. **Stdio**: For local subprocess MCP servers that communicate via standard input/output.
4. **Streamable HTTP**: For managing HTTP connections with direct connection management.

## Common Parameters
- **url** (str): The server endpoint URL.
- **headers** (dict[str, str], optional): HTTP headers to include with requests.
- **timeout** (timedelta | float, optional): The timeout for the HTTP request (default: 5 seconds).
- **cache_tools_list** (bool): Whether to cache the list of available tools (default: False).
- **name** (string | None): A readable name for the server (default: None, auto-generated).
- **max_retry_attempts** (int): Number of times to retry failed tool calls (default: 0).
- **retry_backoff_seconds_base** (float): Base delay for exponential backoff between retries (default: 1.0).

## Usage Context
Use this skill when:
- You need to connect to different types of MCP servers.
- You require real-time communication or local subprocess management.
- You want to handle tool discovery and communication effectively.

## Basic Example
```python
import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerSse, HostedMCPTool, MCPServerStdio, MCPServerStreamableHttp

async def main() -> None:
    # Example for SSE
    async with MCPServerSse(url="http://localhost:8000/sse") as sse_server:
        # Handle SSE server communication

    # Example for Hosted MCP
    hosted_tool = HostedMCPTool(tool_config={"server_url": "http://example.com"})
    
    # Example for Stdio
    async with MCPServerStdio(command="python", args=["server.py"]) as stdio_server:
        # Handle stdio server communication

    # Example for Streamable HTTP
    async with MCPServerStreamableHttp(url="http://localhost:8000/stream") as streamable_http_server:
        # Handle streamable HTTP server communication
```