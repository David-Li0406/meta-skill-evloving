---
name: nodes-code-reference
description: "Code execution nodes reference (PythonCode, Shell). Use when asking 'PythonCode', 'code node', 'Shell node', 'execute code', or 'script execution'."
---

# Code Execution Nodes Reference

Complete reference for code execution nodes.

> **Skill Metadata**
> Category: `nodes`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`pythoncode-best-practices`](../../01-core-sdk/pythoncode-best-practices.md), [`nodes-quick-index`](nodes-quick-index.md)
> Related Subagents: `pattern-expert` (code patterns)

## Quick Reference

```python
from kailash.nodes.code import (
    PythonCodeNode,  # Use sparingly!
    MCPToolNode,
    ScriptRunnerNode
)
```

## PythonCode Node

### PythonCodeNode
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.nodes.code import PythonCodeNode

def custom_logic(input_data):
    """Custom business logic."""
    result = input_data * 2
    return {"result": result}

workflow = WorkflowBuilder()

# Option 1: from_function (recommended)
workflow.add_node("PythonCodeNode", "custom",
    PythonCodeNode.from_function(custom_logic).config
)

# Option 2: code string (use sparingly)
workflow.add_node("PythonCodeNode", "code", {
    "code": "result = input_data * 2",
    "input_data": 10
})
```

## MCP Tool Node

### MCPToolNode
```python
workflow.add_node("MCPToolNode", "mcp_tool", {
    "mcp_server": "weather",
    "tool_name": "get_weather",
    "parameters": {"city": "NYC"}
})
```

## When to Use PythonCodeNode

**✅ Appropriate uses:**
- Ollama/local LLM integration
- Complex custom business logic
- Temporary prototyping

**❌ Avoid for:**
- File I/O (use CSVReaderNode, etc.)
- HTTP requests (use HTTPRequestNode)
- Database queries (use AsyncSQLDatabaseNode)
- Data transformation (use FilterNode, DataTransformer)

## Related Skills

- **PythonCode Best Practices**: [`pythoncode-best-practices`](../../01-core-sdk/pythoncode-best-practices.md)
- **Node Index**: [`nodes-quick-index`](nodes-quick-index.md)

## Documentation

- **Code Nodes**: [`sdk-users/2-core-concepts/nodes/07-code-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/07-code-nodes.md)
- **PythonCode Patterns**: [`sdk-users/2-core-concepts/nodes/11-pythoncode-node-patterns.md`](../../../../sdk-users/2-core-concepts/nodes/11-pythoncode-node-patterns.md)

<!-- Trigger Keywords: PythonCode, code node, Shell node, execute code, script execution, PythonCodeNode -->
