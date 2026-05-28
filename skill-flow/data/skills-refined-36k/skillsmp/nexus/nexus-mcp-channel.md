---
skill: nexus-mcp-channel
description: MCP (Model Context Protocol) tool exposure and AI agent integration patterns
priority: HIGH
tags: [nexus, mcp, ai-agents, tool-discovery, integration]
---

# Nexus MCP Channel

AI agent integration via Model Context Protocol (MCP).

## What is MCP?

MCP (Model Context Protocol) exposes workflows as discoverable tools for AI agents like Claude, ChatGPT, and custom agents.

## Basic MCP Integration

```python
from nexus import Nexus
from kailash.workflow.builder import WorkflowBuilder

# Enable MCP channel
app = Nexus(mcp_port=3001)

# Workflows automatically become MCP tools
workflow = WorkflowBuilder()
workflow.add_node("HTTPRequestNode", "fetch", {
    "url": "https://api.github.com/users/{{username}}",
    "method": "GET"
})

app.register("github-lookup", workflow.build())
app.start()

# Now discoverable by AI agents on localhost:3001
```

## Tool Metadata for AI Discovery

```python
# Add metadata for better AI understanding
workflow = WorkflowBuilder()

workflow.add_metadata({
    "name": "github_user_lookup",
    "description": "Look up GitHub user information by username",
    "parameters": {
        "username": {
            "type": "string",
            "description": "GitHub username to look up",
            "required": True
        }
    },
    "returns": {
        "type": "object",
        "description": "GitHub user profile information including name, bio, repos, followers"
    }
})

workflow.add_node("HTTPRequestNode", "fetch", {
    "url": "https://api.github.com/users/{{username}}",
    "method": "GET"
})

app.register("github-lookup", workflow.build())
```

## MCP Client Usage

```python
import mcp_client

# Connect to Nexus MCP server
client = mcp_client.connect("http://localhost:3001")

# Discover available tools
tools = client.list_tools()
print(f"Available tools: {[t['name'] for t in tools]}")

# Execute tool
result = client.call_tool("github-lookup", {
    "username": "octocat"
})

print(result)
```

## MCP Configuration

```python
app = Nexus(
    mcp_port=3001,
    mcp_host="0.0.0.0"
)

# Fine-tune MCP behavior
app.mcp.tool_caching = True        # Cache tool results
app.mcp.batch_operations = True    # Batch tool calls
app.mcp.async_execution = True     # Async execution
app.mcp.timeout = 30               # Execution timeout
```

## AI Agent Structured Output

```python
# Format output for AI agents
workflow.add_node("PythonCodeNode", "format_for_ai", {
    "code": """
def format_for_agents(data):
    user = data.get('user', {})

    # Structured data for AI consumption
    return {
        'tool_name': 'github_user_lookup',
        'success': True,
        'data': {
            'username': user.get('login'),
            'display_name': user.get('name'),
            'description': user.get('bio'),
            'metrics': {
                'repositories': user.get('public_repos', 0),
                'followers': user.get('followers', 0)
            },
            'profile_url': f"https://github.com/{user.get('login', '')}",
            'avatar_url': user.get('avatar_url')
        },
        'metadata': {
            'retrieved_at': __import__('datetime').datetime.now().isoformat(),
            'source': 'github_api'
        }
    }

result = format_for_agents(user_data)
"""
})
```

## Tool Discovery

MCP tools are automatically discoverable:

```json
{
  "tools": [
    {
      "name": "github-lookup",
      "description": "Look up GitHub user information",
      "input_schema": {
        "type": "object",
        "properties": {
          "username": {
            "type": "string",
            "description": "GitHub username"
          }
        },
        "required": ["username"]
      }
    }
  ]
}
```

## Best Practices

1. **Add Rich Descriptions** for AI understanding
2. **Structure Outputs** for easy parsing
3. **Include Metadata** for context
4. **Use Clear Parameter Names**
5. **Provide Examples** in descriptions
6. **Handle Errors Gracefully**

## Key Takeaways

- Workflows automatically become MCP tools
- AI agents discover and execute tools
- Add metadata for better AI integration
- Structure outputs for easy parsing
- MCP enables agentic workflows

## Related Skills

- [nexus-multi-channel](#) - MCP, API, CLI overview
- [nexus-api-patterns](#) - REST API usage
- [nexus-enterprise-features](#) - Auth for MCP
