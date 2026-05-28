---
name: agentic-ai
description: Helps build AI agents using Azure AI Foundry with tool calling capabilities. Use this skill when creating agents, configuring tool definitions, implementing the agent loop, or integrating agents with Azure Functions and MCP servers.
---

# Agentic AI Development Skill

## Overview

This skill helps you build **AI agents** that can reason, plan, and execute actions using tools. We focus on the **single-agent pattern** using Azure AI Foundry.

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Agent Loop                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────┐     ┌──────────────┐     ┌─────────────────────┐ │
│   │  User   │────▶│  AI Model    │────▶│  Tool Execution     │ │
│   │  Query  │     │  (Reasoning) │     │  (Azure Functions)  │ │
│   └─────────┘     └──────────────┘     └─────────────────────┘ │
│        ▲                │                        │              │
│        │                ▼                        ▼              │
│        │         ┌──────────────┐     ┌─────────────────────┐ │
│        └─────────│  Response    │◀────│  Tool Results       │ │
│                  │  Generation  │     │                     │ │
│                  └──────────────┘     └─────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Tool Definition Schema

Tools tell the AI what actions it can take:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "analyze_data",
            "description": "Analyze a list of numbers and return statistics including count, sum, mean, min, and max.",
            "parameters": {
                "type": "object",
                "properties": {
                    "values": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "List of numbers to analyze"
                    }
                },
                "required": ["values"]
            }
        }
    }
]
```

## Agent Implementation with Azure AI Foundry

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize client
client = AIProjectClient(
    credential=DefaultAzureCredential(),
    subscription_id="your-subscription",
    resource_group_name="your-rg",
    project_name="your-project"
)

# Create agent with tools
agent = client.agents.create_agent(
    model="gpt-4o",
    name="data-analyst",
    instructions="You are a data analysis assistant. Use your tools to analyze data when asked.",
    tools=tools
)

# Create thread and run
thread = client.agents.create_thread()
message = client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Analyze these sales figures: [100, 250, 175, 300, 225]"
)

run = client.agents.create_and_process_run(
    thread_id=thread.id,
    assistant_id=agent.id
)
```

## Tool Execution Pattern

When the AI decides to call a tool:

```python
def process_tool_calls(run, client, thread_id):
    """Process tool calls from the agent."""
    if run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        
        tool_outputs = []
        for call in tool_calls:
            # Get function name and arguments
            function_name = call.function.name
            arguments = json.loads(call.function.arguments)
            
            # Execute the tool
            if function_name == "analyze_data":
                result = analyze_data(arguments["values"])
            elif function_name == "search_database":
                result = search_database(arguments["query"])
            else:
                result = {"error": f"Unknown function: {function_name}"}
            
            tool_outputs.append({
                "tool_call_id": call.id,
                "output": json.dumps(result)
            })
        
        # Submit results back to the agent
        run = client.agents.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    
    return run
```

## Writing Good Tool Descriptions

The AI uses descriptions to decide **when** to use a tool. Be specific:

### Good ✅
```python
"description": "Search the product database for items matching the query. Returns product name, price, and availability. Use when the user asks about products, inventory, or wants to find specific items."
```

### Bad ❌
```python
"description": "Searches things"  # Too vague
```

## Single Agent vs Multi-Agent

| Aspect | Single Agent | Multi-Agent |
|--------|--------------|-------------|
| **Complexity** | Lower | Higher |
| **Use Case** | One brain + many tools | Specialized roles |
| **Coordination** | None needed | Requires orchestration |
| **Debugging** | Easier | More complex |
| **When to Use** | Most tasks | Parallel work, debate, specialization |

**Start with single agent.** Graduate to multi-agent only when needed.

## Agent Loop Best Practices

1. **Clear Instructions**: Tell the agent its role and constraints
2. **Descriptive Tools**: Help the AI understand when to use each tool
3. **Error Handling**: Tools should return error info, not throw exceptions
4. **Iteration Limits**: Set max iterations to prevent infinite loops
5. **Logging**: Log tool calls and results for debugging

## Connecting to External Tools

### Via HTTP (Azure Functions)
```python
def call_azure_function(function_url: str, data: dict) -> dict:
    """Call an Azure Function as a tool."""
    response = requests.post(
        function_url,
        json=data,
        headers={"x-functions-key": os.environ["FUNCTION_KEY"]}
    )
    return response.json()
```

### Via MCP (Model Context Protocol)
```python
# MCP tools are auto-discovered by compatible clients
# See the mcp-server skill for implementation details
```

## Debugging Agents

1. **Print tool calls**: Log what the AI is trying to do
2. **Check tool definitions**: Ensure schemas are valid JSON
3. **Test tools independently**: Call tools directly before agent integration
4. **Review instructions**: Vague instructions lead to vague behavior
5. **Inspect thread history**: See the full conversation context
