---
skill: nexus-multi-channel
description: Understand Nexus's revolutionary multi-channel architecture - single workflow, three interfaces (API/CLI/MCP)
priority: HIGH
tags: [nexus, multi-channel, api, cli, mcp, architecture]
---

# Nexus Multi-Channel Architecture

Register once, deploy to API + CLI + MCP automatically.

## Core Innovation

Traditional platforms require separate implementations for each interface. Nexus automatically generates all three:

```python
from nexus import Nexus
from kailash.workflow.builder import WorkflowBuilder

app = Nexus()

# Build once
workflow = WorkflowBuilder()
workflow.add_node("HTTPRequestNode", "fetch", {
    "url": "https://api.github.com/users/{{username}}",
    "method": "GET"
})

# Register once
app.register("github-user", workflow.build())

# Now available as:
# 1. REST API: POST /workflows/github-user/execute
# 2. CLI: nexus run github-user --username octocat
# 3. MCP: AI agents discover as "github-user" tool
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│                    Nexus Core                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   API    │  │   CLI    │  │   MCP    │     │
│  │ Channel  │  │ Channel  │  │ Channel  │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       └──────────────┴──────────────┘           │
│         Session Manager & Event Router          │
│  ┌─────────────────────────────────────────────┐│
│  │        Enterprise Gateway                   ││
│  └─────────────────────────────────────────────┘│
├─────────────────────────────────────────────────┤
│               Kailash SDK                       │
│         Workflows │ Nodes │ Runtime             │
└─────────────────────────────────────────────────┘
```

## API Channel

**Automatic REST Endpoints**:
```bash
# Execute workflow
curl -X POST http://localhost:8000/workflows/github-user/execute \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"username": "octocat"}}'

# Get workflow schema
curl http://localhost:8000/workflows/github-user/schema

# Get OpenAPI docs
curl http://localhost:8000/docs

# Health check
curl http://localhost:8000/health
```

**Configuration**:
```python
app = Nexus(
    api_port=8000,
    enable_auth=True,
    rate_limit=1000
)

# Fine-tune API behavior
app.api.response_compression = True
app.api.request_timeout = 30
app.api.max_concurrent_requests = 100
```

## CLI Channel

**Automatic Commands**:
```bash
# Execute workflow
nexus run github-user --username octocat

# List available workflows
nexus list

# Get workflow info
nexus info github-user

# Help
nexus --help
```

**Configuration**:
```python
# Configure CLI behavior
app.cli.interactive = True          # Enable prompts
app.cli.auto_complete = True        # Tab completion
app.cli.progress_bars = True        # Progress indicators
app.cli.colored_output = True       # Colors
```

## MCP Channel

**AI Agent Integration**:
```python
# Workflows automatically become MCP tools
app = Nexus(mcp_port=3001)

# Add metadata for AI discovery
workflow = WorkflowBuilder()
workflow.add_metadata({
    "name": "github_user_lookup",
    "description": "Look up GitHub user by username",
    "parameters": {
        "username": {
            "type": "string",
            "description": "GitHub username",
            "required": True
        }
    }
})

app.register("github-lookup", workflow.build())
```

**MCP Usage**:
```python
import mcp_client

client = mcp_client.connect("http://localhost:3001")
result = client.call_tool("github-lookup", {"username": "octocat"})
```

**Configuration**:
```python
app.mcp.tool_caching = True        # Cache tool results
app.mcp.batch_operations = True    # Batch calls
app.mcp.async_execution = True     # Async execution
```

## Cross-Channel Parameter Consistency

**Same inputs work across all channels**:

```python
# API Request
{
  "inputs": {
    "username": "octocat",
    "include_repos": true
  }
}

# CLI Command
nexus run github-user --username octocat --include-repos true

# MCP Call
client.call_tool("github-user", {
  "username": "octocat",
  "include_repos": true
})
```

## Unified Sessions

Sessions work across all channels:

```python
# Create session in API
response = requests.post(
    "http://localhost:8000/workflows/process/execute",
    json={"inputs": {"step": 1}},
    headers={"X-Session-ID": "session-123"}
)

# Continue in CLI (same session)
# nexus run process --session session-123 --step 2

# Complete in MCP (full state preserved)
result = client.call_tool("process", {
    "step": 3,
    "session_id": "session-123"
})
```

## Testing All Channels

```python
import requests
import subprocess

class MultiChannelTester:
    def test_api(self, workflow_name, inputs):
        response = requests.post(
            f"http://localhost:8000/workflows/{workflow_name}/execute",
            json={"inputs": inputs}
        )
        return response.json()

    def test_cli(self, workflow_name, params):
        cmd = ["nexus", "run", workflow_name] + params
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout

    def test_mcp(self, tool_name, parameters):
        client = mcp_client.connect("http://localhost:3001")
        return client.call_tool(tool_name, parameters)

tester = MultiChannelTester()
tester.test_api("github-user", {"username": "octocat"})
tester.test_cli("github-user", ["--username", "octocat"])
tester.test_mcp("github-user", {"username": "octocat"})
```

## Best Practices

### 1. Channel-Agnostic Design
Design workflows that work well across all channels:

```python
workflow.add_node("PythonCodeNode", "universal_output", {
    "code": """
result = {
    'data': process(input_data),        # Core logic
    'api_response': format_json(data),  # For API
    'cli_display': format_text(data),   # For CLI
    'mcp_result': format_tool(data)     # For MCP
}
"""
})
```

### 2. Progressive Enhancement
Start simple, add channel-specific features as needed:

```python
app = Nexus()
app.register("workflow", workflow.build())

# Add API features
app.api.enable_docs = True
app.api.enable_metrics = True

# Add CLI features
app.cli.enable_autocomplete = True
app.cli.enable_history = True

# Add MCP features
app.mcp.enable_tool_discovery = True
```

### 3. Consistent Error Handling
Handle errors uniformly across channels:

```python
workflow.add_node("PythonCodeNode", "error_handler", {
    "code": """
if 'error' in data:
    result = {
        'api_error': {'status': 'error', 'message': data['error']},
        'cli_error': f"Error: {data['error']}",
        'mcp_error': {'error': True, 'details': data['error']}
    }
"""
})
```

## Key Takeaways

- Single registration creates three interfaces automatically
- Same parameters work across all channels
- Unified session management across channels
- Test all channels during development
- Channel-specific optimizations available
- Progressive enhancement from simple to complex

## Related Skills

- [nexus-api-patterns](#) - Deep dive into API usage
- [nexus-cli-patterns](#) - CLI command patterns
- [nexus-mcp-channel](#) - MCP integration details
- [nexus-sessions](#) - Session management guide
