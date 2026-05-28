# Tool Use (Function Calling) Guide

## Basic Concept

Tool Use allows Claude to call external functions, enabling:
- Database queries
- API calls
- Computational operations
- System integrations

## Basic Example

```python
import anthropic

client = anthropic.Anthropic()

# Define tools
tools = [
    {
        "name": "get_weather",
        "description": "Get weather information for a specified city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g.: New York"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["city"]
        }
    }
]

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather like in New York today?"}]
)
```

## Handling Tool Use Response

```python
# Check if tool call is needed
if message.stop_reason == "tool_use":
    for block in message.content:
        if block.type == "tool_use":
            tool_name = block.name
            tool_input = block.input
            tool_use_id = block.id
            
            # Execute the actual tool call
            result = execute_tool(tool_name, tool_input)
            
            # Return result to Claude
            follow_up = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                tools=tools,
                messages=[
                    {"role": "user", "content": "What's the weather like in New York today?"},
                    {"role": "assistant", "content": message.content},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use_id,
                                "content": result
                            }
                        ]
                    }
                ]
            )
```

## Tool Choice Control

```python
# Auto decide (default)
tool_choice = {"type": "auto"}

# Force specific tool
tool_choice = {"type": "tool", "name": "get_weather"}

# Force any tool
tool_choice = {"type": "any"}

# Disable tools
tool_choice = {"type": "none"}

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    tool_choice=tool_choice,
    messages=[...]
)
```

## Disable Parallel Tool Calls

```python
tool_choice = {
    "type": "auto",
    "disable_parallel_tool_use": True  # Only call one tool at a time
}
```

## Multiple Tool Definitions

```python
tools = [
    {
        "name": "search_database",
        "description": "Search records in the database",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "default": 10}
            },
            "required": ["query"]
        }
    },
    {
        "name": "send_email",
        "description": "Send an email",
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["to", "subject", "body"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"]
        }
    }
]
```

## Complete Agentic Loop

```python
def run_agent(user_message, tools, max_iterations=10):
    messages = [{"role": "user", "content": user_message}]
    
    for _ in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )
        
        # If no tool needed, return final response
        if response.stop_reason == "end_turn":
            return response.content
        
        # Handle tool calls
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            
            messages.append({"role": "user", "content": tool_results})
    
    return "Max iterations reached"
```

## Built-in Tools

### Web Search Tool

```python
tools = [
    {
        "type": "web_search_20250305",
        "name": "web_search"
    }
]
```

### Code Execution Tool

```python
tools = [
    {
        "type": "code_execution_20250522",
        "name": "code_execution"
    }
]
```

### Computer Use Tool

```python
tools = [
    {
        "type": "computer_20250124",
        "name": "computer",
        "display_width_px": 1920,
        "display_height_px": 1080
    }
]
```

## Best Practices

1. **Clear tool descriptions** - Explain tool purpose and parameters in detail
2. **Use JSON Schema** - Define strict input formats
3. **Error handling** - Report errors in tool_result
4. **Limit iterations** - Prevent infinite loops
5. **Validate tool input** - Verify parameters before execution

## Response Structure

```json
{
    "id": "msg_xxx",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "tool_use",
            "id": "toolu_xxx",
            "name": "get_weather",
            "input": {"city": "New York"}
        }
    ],
    "stop_reason": "tool_use"
}
```