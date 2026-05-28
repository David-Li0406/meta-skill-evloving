---
name: mcp-server
description: Helps build MCP (Model Context Protocol) servers that expose tools to AI agents like GitHub Copilot. Use this skill when creating MCP tools, configuring MCP clients, debugging MCP connections, or integrating with VS Code Copilot Agent Mode.
---

# MCP Server Development Skill

## Overview

The **Model Context Protocol (MCP)** is an open standard for connecting AI agents to external tools. This skill helps you build MCP servers using Azure Functions.

## Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  AI Agent       │     │  MCP Server          │     │  Your Logic     │
│  (Copilot)      │────▶│  (Azure Functions)   │────▶│  (Python)       │
│                 │◀────│  SSE Transport       │◀────│                 │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

## Creating an MCP Tool

### Tool Definition Pattern

```python
import json
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Define tool properties (JSON schema for parameters)
tool_properties = json.dumps([
    {
        "propertyName": "query",
        "propertyType": "string",
        "description": "The search query to execute"
    },
    {
        "propertyName": "limit",
        "propertyType": "number",
        "description": "Maximum number of results (default: 10)"
    }
])

@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="search_data",
    description="Search the database for records matching the query. Use when the user asks to find or search for specific data.",
    toolProperties=tool_properties
)
def search_data(context) -> str:
    """Search tool implementation."""
    content = json.loads(context)
    query = content["arguments"].get("query", "")
    limit = content["arguments"].get("limit", 10)
    
    # Your search logic here
    results = perform_search(query, limit)
    
    return json.dumps({
        "results": results,
        "count": len(results),
        "query": query
    })
```

### Tool Property Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text input | `"hello world"` |
| `number` | Integer or float | `42`, `3.14` |
| `boolean` | True/false | `true`, `false` |
| `array` | JSON array (as string) | `"[1, 2, 3]"` |
| `object` | JSON object (as string) | `'{"key": "value"}'` |

## VS Code MCP Configuration

### Local Development (.vscode/mcp.json)

```json
{
    "servers": {
        "my-mcp-server": {
            "type": "http",
            "url": "http://localhost:7071/runtime/webhooks/mcp"
        }
    }
}
```

### Production (with authentication)

```json
{
    "servers": {
        "my-mcp-server-prod": {
            "type": "http",
            "url": "https://my-app.azurewebsites.net/runtime/webhooks/mcp",
            "headers": {
                "x-functions-key": "${MCP_FUNCTION_KEY}"
            }
        }
    }
}
```

## Testing MCP Tools

### Via VS Code Copilot
1. Press `F1` → **MCP: List Servers**
2. Verify your server is connected
3. Open Copilot Chat → Switch to **Agent Mode**
4. Your tools appear in the tools panel

### Test Prompts

| Tool | Test Prompt |
|------|-------------|
| `hello_mcp` | "Say hello" |
| `analyze_data` | "Analyze [1, 2, 3, 4, 5]" |
| `search_data` | "Search for Python tutorials" |

## Writing Good Tool Descriptions

The `description` field is **critical** — it's how Copilot decides when to use your tool.

### Good Descriptions ✅

```python
description="Analyze a list of numbers and return statistics including count, sum, mean, min, and max. Use when the user asks for data analysis or statistics."
```

### Poor Descriptions ❌

```python
description="Analyzes data"  # Too vague
```

## Common Patterns

### Tool with No Parameters

```python
@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="get_status",
    description="Get the current system status",
    toolProperties="[]"  # Empty array for no parameters
)
def get_status(context) -> str:
    return json.dumps({"status": "healthy"})
```

### Tool with Optional Parameters

```python
# Mark as optional in description
tool_properties = json.dumps([{
    "propertyName": "format",
    "propertyType": "string",
    "description": "Output format: 'json' or 'text' (optional, default: json)"
}])
```

### Error Handling

```python
def my_tool(context) -> str:
    try:
        content = json.loads(context)
        # ... tool logic ...
        return json.dumps({"status": "success", "data": result})
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON input"})
    except KeyError as e:
        return json.dumps({"error": f"Missing required parameter: {e}"})
    except Exception as e:
        logging.error(f"Tool error: {e}")
        return json.dumps({"error": str(e)})
```

## Debugging Tips

1. **Check func start output** — Tools should be listed
2. **View logs** — `logging.info()` appears in terminal
3. **Test JSON parsing** — Context comes as JSON string
4. **Verify MCP config** — `F1` → **MCP: List Servers**
5. **Restart Copilot** — After config changes
