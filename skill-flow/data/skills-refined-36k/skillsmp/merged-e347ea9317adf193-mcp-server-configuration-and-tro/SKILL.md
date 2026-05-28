---
name: mcp-server-configuration-and-troubleshooting
description: Use this skill when you need to create, configure, and troubleshoot Model Context Protocol (MCP) server connections for OpenAI Agents SDK.
---

# MCP Server Configuration and Troubleshooting Skill

This skill helps create, configure, and troubleshoot Model Context Protocol (MCP) server connections in OpenAI Agents SDK, addressing both hosted and SSE configurations as well as common connection issues.

## Purpose
- Create and configure MCP server connections (both hosted and SSE)
- Diagnose and resolve common MCP connection problems
- Provide systematic troubleshooting steps for authentication, network, and configuration issues

## Common Issues Addressed
1. **Connection failures** - Network timeouts, unreachable servers
2. **Authentication errors** - Token issues, invalid credentials
3. **Tool discovery problems** - Tools not appearing, listing failures
4. **Communication errors** - Request/response failures
5. **Performance issues** - Slow responses, timeouts
6. **Configuration problems** - Incorrect parameters, headers

## Troubleshooting Approach
1. **Identify the transport method** in use (Hosted, HTTP, SSE, stdio)
2. **Check basic connectivity** to the MCP server
3. **Verify authentication** credentials and tokens
4. **Validate server configuration** parameters
5. **Test tool listing** functionality
6. **Examine error messages** for specific details
7. **Review logs** for additional diagnostic information

## MCP Server Configuration

### Hosted MCP Server Configuration
- **tool_config** (Mcp object/dict): The MCP tool config, which includes the server URL and other settings
- **on_approval_request** (function): Optional function for handling approval requests for sensitive operations

### MCPServerSse Configuration
- **params** (MCPServerSseParams): Connection parameters for the server
  - **url** (str): SSE endpoint URL for the MCP server
  - **headers** (dict[str, str], optional): HTTP headers to include with requests
  - **timeout** (timedelta | float, optional): The timeout for the HTTP request (default: 5 seconds)
  - **sse_read_timeout** (timedelta | float, optional): The timeout for the SSE connection (default: 5 minutes)
  - **cache_tools_list** (bool): Whether to cache the list of available tools (default: False)

## Diagnostic Commands
- Test server reachability
- Validate authentication tokens
- Check tool listing endpoints
- Verify headers and parameters
- Review timeout configurations

## Resolution Strategies
- Update authentication credentials
- Adjust timeout values
- Fix network configuration
- Correct server parameters
- Implement retry mechanisms
- Add proper error handling

## Usage Context
Use this skill when:
- Working with servers that implement HTTP with Server-Sent Events transport
- Connecting to publicly accessible MCP servers
- Needing real-time event streaming from the MCP server
- Using OpenAI's infrastructure for tool execution

## Basic Example for Hosted MCP Server
```python
import asyncio
from agents import Agent, HostedMCPTool, Runner

async def main() -> None:
    agent = Agent(
        name="Assistant",
        tools=[
            HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "example-server",
                    "server_url": "https://example.com/mcp",
                    "require_approval": "never",
                }
            )
        ],
    )

    result = await Runner.run(agent, "What is the status of the server?")
    print(result.final_output)

asyncio.run(main())
```

## Basic Example for MCPServerSse
```python
import asyncio
from agents import Agent, Runner, MCPServerSse

async def main() -> None:
    async with MCPServerSse(
        name="SSE Example Server",
        params={
            "url": "http://localhost:8000/sse",
            "headers": {"X-Workspace": "demo-workspace"},
        },
        cache_tools_list=True,
    ) as server:
        agent = Agent(
            name="Assistant",
            mcp_servers=[server],
        )
        result = await Runner.run(agent, "What's the weather in Tokyo?")
        print(result.final_output)

asyncio.run(main())
```