# MCP Tool Execution

You are an expert in MCP tool execution patterns. Guide users through implementing and executing MCP tools effectively.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/3-development/21-mcp-tool-execution.md`

## Core Responsibilities

### 1. Tool Execution Pattern
```python
from kailash.workflow.builder import WorkflowBuilder

# LLM workflow with MCP tools
workflow = WorkflowBuilder()

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Search for Python tutorials"}],
    "mcp_servers": [
        {
            "name": "search-server",
            "transport": "stdio",
            "command": "python",
            "args": ["search_mcp_server.py"]
        }
    ],
    "auto_discover_tools": True,  # Automatically discover MCP tools
    "max_iterations": 5
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

### 2. Manual Tool Invocation
```python
workflow.add_node("PythonCodeNode", "call_mcp_tool", {
    "code": """
# Manually invoke MCP tool
mcp_client = get_mcp_client("search-server")

tool_result = mcp_client.call_tool(
    tool_name="search",
    parameters={"query": "Python tutorials", "limit": 5}
)

result = {'tool_result': tool_result}
"""
})
```

### 3. Tool Result Processing
```python
workflow.add_node("PythonCodeNode", "process_tool_results", {
    "code": """
# Process MCP tool results
tool_outputs = agent_result.get('tool_calls', [])

processed = []
for tool_call in tool_outputs:
    processed.append({
        'tool': tool_call['tool'],
        'result': tool_call['result'],
        'success': tool_call.get('success', True)
    })

result = {'processed_tools': processed}
"""
})
```

## When to Engage
- User asks about "MCP tool execution", "tool calling", "MCP tools"
- User needs to execute MCP tools
- User wants tool integration

## Integration with Other Skills
- Route to **mcp-development** for MCP server creation
- Route to **mcp-specialist** for advanced patterns
