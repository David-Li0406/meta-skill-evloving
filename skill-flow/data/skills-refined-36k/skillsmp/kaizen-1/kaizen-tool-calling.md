# Kaizen Tool Calling (v0.2.0+)

Autonomous tool execution with approval workflows for AI agents.

## Overview

Tool Calling enables agents to execute external tools automatically:
- **12 Builtin Tools** - File, HTTP, bash, web operations
- **Custom Tools** - Register your own tools
- **MCP Integration** - Connect to MCP servers
- **Approval Workflows** - Danger-level based safety

**Version:** Kaizen v0.2.0+

---

## Quick Start

```python
from kaizen.core.base_agent import BaseAgent

# 1. Tools auto-configured via MCP
agent = MyAgent(
    config=config,
    signature=signature,
    tools="all"  # Enable 12 builtin tools via MCP
)

# 2. Execute tool
result = await agent.execute_tool("read_file", {"path": "data.txt"})

# 3. OR configure custom MCP servers
mcp_servers = [{
    "name": "kaizen_builtin",
    "command": "python",
    "args": ["-m", "kaizen.mcp.builtin_server"],
    "transport": "stdio"
}]
agent = MyAgent(
    config=config,
    signature=signature,
    custom_mcp_servers=mcp_servers
)
```

---

## Builtin Tools

### File Operations (5 tools)

```python
# Read file
content = await agent.execute_tool("read_file", {"path": "data.txt"})

# Write file
await agent.execute_tool("write_file", {
    "path": "output.txt",
    "content": "Hello World"
})

# Delete file
await agent.execute_tool("delete_file", {"path": "temp.txt"})

# List directory
files = await agent.execute_tool("list_directory", {"path": "."})

# Check existence
exists = await agent.execute_tool("file_exists", {"path": "data.txt"})
```

### HTTP Operations (4 tools)

```python
# GET request
response = await agent.execute_tool("http_get", {
    "url": "https://api.example.com/data"
})

# POST request
response = await agent.execute_tool("http_post", {
    "url": "https://api.example.com/create",
    "data": {"name": "John"}
})

# PUT and DELETE also available
```

### Bash Operations (1 tool)

```python
# Execute bash command
result = await agent.execute_tool("bash_command", {
    "command": "ls -la",
    "timeout": 10
})
```

### Web Operations (2 tools)

```python
# Fetch URL content
content = await agent.execute_tool("fetch_url", {
    "url": "https://example.com"
})

# Extract links
links = await agent.execute_tool("extract_links", {
    "url": "https://example.com"
})
```

---

## Tool Discovery

```python
# Discover all tools
tools = await agent.discover_tools()

# Discover by category
file_tools = await agent.discover_tools(category="file")
http_tools = await agent.discover_tools(category="http")

# Tool structure
# {
#     "name": "read_file",
#     "description": "Read file contents",
#     "category": "file",
#     "danger_level": "SAFE",
#     "parameters": {...}
# }
```

---

## Tool Chaining

Execute multiple tools in sequence:

```python
# Chain tools together
results = await agent.execute_tool_chain([
    {
        "tool_name": "read_file",
        "params": {"path": "input.txt"}
    },
    {
        "tool_name": "http_post",
        "params": {
            "url": "https://api.example.com/process",
            "data": "${previous.content}"  # Use previous result
        }
    },
    {
        "tool_name": "write_file",
        "params": {
            "path": "output.txt",
            "content": "${previous.response}"
        }
    }
])

# Results contain all outputs
# [
#     {"content": "file contents"},
#     {"response": "API response"},
#     {"success": true}
# ]
```

---

## Danger Levels

Tools have safety levels that determine approval requirements:

| Level | Description | Approval Required | Examples |
|-------|-------------|-------------------|----------|
| `SAFE` | Read-only, no side effects | No | read_file, http_get, fetch_url |
| `LOW` | Minor modifications | No | write_file (non-critical) |
| `MEDIUM` | Significant changes | Yes (auto-approve in dev) | http_post, http_put |
| `HIGH` | Risky operations | Yes | delete_file, bash_command |
| `CRITICAL` | Destructive operations | Yes (manual only) | System commands |

### Approval Workflow

```python
# HIGH/CRITICAL tools trigger approval
result = await agent.execute_tool("delete_file", {"path": "data.txt"})
# Prompts: "Approve tool execution: delete_file?" [Yes/No]
```

---

## Custom Tools

### Register Custom Tool

```python
from kaizen.tools import Tool, ToolParameter

# 1. Define tool
def my_custom_tool(param1: str, param2: int) -> dict:
    # Tool logic here
    return {"result": f"Processed {param1} with {param2}"}

# 2. Create Tool object
custom_tool = Tool(
    name="my_custom_tool",
    description="Processes data with custom logic",
    function=my_custom_tool,
    parameters=[
        ToolParameter(
            name="param1",
            type="string",
            description="First parameter",
            required=True
        ),
        ToolParameter(
            name="param2",
            type="integer",
            description="Second parameter",
            required=True
        )
    ],
    category="custom",
    danger_level="LOW"
)

# 3. Register
registry.register_tool(custom_tool)

# 4. Use
result = await agent.execute_tool("my_custom_tool", {
    "param1": "data",
    "param2": 42
})
```

---

## MCP Server Integration

Connect to MCP servers for additional tools:

```python
# 1. Define MCP servers
mcp_servers = [
    {
        "name": "filesystem",
        "command": "mcp-server-filesystem",
        "args": ["--root", "/data"]
    },
    {
        "name": "git",
        "command": "mcp-server-git",
        "args": ["--repo", "/repo"]
    }
]

# 2. Enable for agent
agent = MyAgent(
    config=config,
    signature=signature,
    tools="all"  # Enable 12 builtin tools via MCP
    mcp_servers=mcp_servers  # Add MCP tools
)

# 3. MCP tools automatically available
result = await agent.execute_tool("git_status", {})
```

---

## Autonomous Agents with Tools

Agents can autonomously call tools during execution:

```python
from kaizen.agents import ReActAgent

# ReActAgent uses tools autonomously
agent = ReActAgent(
    config=config,
    tools="all"  # Enable 12 builtin tools via MCP
)

# Agent automatically:
# 1. Reasons about task
# 2. Calls appropriate tools
# 3. Iterates until objective met
result = agent.solve("Find all Python files and count lines of code")

# Behind the scenes:
# - Calls list_directory to find files
# - Calls read_file for each Python file
# - Processes and returns result
```

---

## Complete Example

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature, InputField, OutputField
# Tools auto-configured via MCP

from dataclasses import dataclass

class DataProcessingSignature(Signature):
    source_file: str = InputField(description="Source file path")
    result: str = OutputField(description="Processing result")

@dataclass
class DataConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"

class DataProcessingAgent(BaseAgent):
    def __init__(self, config: DataConfig):
        super().__init__(
            config=config,
            signature=DataProcessingSignature(),
            tools="all"  # Enable 12 builtin tools via MCP
        )

    async def process_data(self, source_file: str) -> dict:
        # 1. Read source file
        content = await self.execute_tool("read_file", {
            "path": source_file
        })

        # 2. Process with LLM
        result = self.run(source_file=source_file, content=content["content"])

        # 3. Send to API
        api_response = await self.execute_tool("http_post", {
            "url": "https://api.example.com/process",
            "data": result
        })

        # 4. Save result
        await self.execute_tool("write_file", {
            "path": "result.txt",
            "content": api_response["response"]
        })

        return result

# Usage
async def main():

    # 12 builtin tools enabled via MCP

    agent = DataProcessingAgent(DataConfig(), registry)
    result = await agent.process_data("input.txt")
```

---

## Best Practices

### 1. Use Tool Discovery

```python
# ✅ GOOD - Discover available tools
tools = await agent.discover_tools(category="file")
for tool in tools:
    print(f"Available: {tool['name']}")

# ❌ BAD - Assume tool exists
await agent.execute_tool("unknown_tool", {})
```

### 2. Handle Tool Errors

```python
# ✅ GOOD - Error handling
try:
    result = await agent.execute_tool("read_file", {"path": "data.txt"})
except FileNotFoundError:
    # Handle missing file
    result = {"content": ""}
```

### 3. Set Appropriate Danger Levels

```python
# ✅ GOOD - Safe for read operations
tool = Tool(name="read_config", danger_level="SAFE", ...)

# ✅ GOOD - High for destructive operations
tool = Tool(name="delete_all", danger_level="CRITICAL", ...)
```

### 4. Use Tool Chaining

```python
# ✅ GOOD - Chain related operations
results = await agent.execute_tool_chain([...])

# ❌ BAD - Individual calls (slower, less atomic)
r1 = await agent.execute_tool("read_file", {})
r2 = await agent.execute_tool("process", {"data": r1})
r3 = await agent.execute_tool("write_file", {"content": r2})
```

---

## Integration

### With Control Protocol

```python
# Combine tool calling with user confirmation
class SafeAgent(BaseAgent):
    async def process(self):
        # Discover dangerous tools
        dangerous = [t for t in await self.discover_tools()
                    if t["danger_level"] in ["HIGH", "CRITICAL"]]

        if dangerous:
            # Ask user for permission
            approved = await self.ask_user_question(
                question=f"Allow {len(dangerous)} dangerous tools?",
                options=["Yes", "No"]
            )

            if approved == "No":
                return {"status": "cancelled"}

        # Proceed with tools
        result = await self.execute_tool("delete_file", {...})
```

### With Multi-Agent

```python
from kaizen.agents.coordination.supervisor_worker import SupervisorWorkerPattern

# Supervisor with tools
supervisor = SupervisorAgent(config, tools="all"  # Enable 12 builtin tools via MCP

# Workers with specialized tools
file_worker = FileAgent(config, tools="all"  # Enable tools via MCP
api_worker = APIAgent(config, tools="all"  # Enable tools via MCP

pattern = SupervisorWorkerPattern(supervisor, [file_worker, api_worker], ...)
```

---

## Testing

```python
import pytest
# Tools auto-configured via MCP, Tool

@pytest.mark.asyncio
async def test_tool_execution():
    # Setup


    # Register mock tool
    def mock_tool(param: str) -> dict:
        return {"result": f"Processed {param}"}

    tool = Tool(
        name="mock_tool",
        function=mock_tool,
        parameters=[...],
        danger_level="SAFE"
    )
    registry.register_tool(tool)

    # Create agent
    agent = MyAgent(config, tools="all"  # Enable 12 builtin tools via MCP

    # Test
    result = await agent.execute_tool("mock_tool", {"param": "test"})
    assert result["result"] == "Processed test"
```

---

## Performance

| Operation | Latency | Notes |
|-----------|---------|-------|
| Tool discovery | <1ms | Cached registry |
| Single tool execution | 10-100ms | Depends on tool |
| Tool chain (3 tools) | 30-300ms | Sequential execution |
| MCP tool call | 50-200ms | IPC overhead |

---

## Troubleshooting

**Issue:** `ToolNotFoundError: Tool 'xyz' not found`

**Fix:** Ensure tool is registered:
```python

# 12 builtin tools enabled via MCP
```

**Issue:** Tool execution hangs

**Fix:** Add timeout:
```python
result = await agent.execute_tool(
    "bash_command",
    {"command": "...", "timeout": 10}
)
```

**Issue:** Approval prompt not showing

**Fix:** Enable control protocol:
```python
agent = MyAgent(config, tools="all"  # Enable 12 builtin tools via MCP
```

---

## Migration

**Before** (Manual tool integration):
```python
# Custom tool integration
import requests

class MyAgent:
    def process(self):
        response = requests.get("https://api.example.com")
        # Manual error handling, logging, etc.
```

**After** (Tool Calling):
```python
# Unified tool calling
agent = MyAgent(config, tools="all"  # Enable 12 builtin tools via MCP
response = await agent.execute_tool("http_get", {
    "url": "https://api.example.com"
})
# Automatic error handling, logging, approval workflows
```

---

## Related

- **[kaizen-control-protocol.md](kaizen-control-protocol.md)** - Interactive approval workflows
- **[kaizen-baseagent-quick.md](kaizen-baseagent-quick.md)** - BaseAgent fundamentals
- **[kaizen-react-pattern.md](kaizen-react-pattern.md)** - Autonomous reasoning + action
- **[BaseAgent Tool Integration](../../../apps/kailash-kaizen/docs/features/baseagent-tool-integration.md)** - Complete guide (667 lines)

---

**Version:** Kaizen v0.2.0+
**Status:** Production-ready ✅
