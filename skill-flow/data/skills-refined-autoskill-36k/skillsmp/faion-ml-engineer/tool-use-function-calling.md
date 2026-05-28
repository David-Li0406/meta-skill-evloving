---
id: tool-use-function-calling
name: "Tool Use / Function Calling"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Tool Use / Function Calling

## Overview

Tool use enables LLMs to interact with external systems by calling functions, APIs, or executing code. This extends LLM capabilities beyond text generation to perform real-world actions like searching the web, querying databases, or controlling applications.

## When to Use

- Accessing real-time data (weather, stocks, news)
- Performing calculations with precision
- Interacting with databases or APIs
- Executing code safely
- Building AI agents
- Multi-step task automation

## Key Concepts

### Tool Use Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  User   │────▶│  LLM    │────▶│ Execute │────▶│   LLM   │
│ Request │     │ Decides │     │  Tool   │     │ Response│
└─────────┘     │ Tool    │     └─────────┘     └─────────┘
                └─────────┘           │
                     ▲                │
                     └────────────────┘
                      Tool Result
```

### Supported Providers

| Provider | Feature Name | Max Tools |
|----------|--------------|-----------|
| OpenAI | Function Calling | 128 |
| Anthropic | Tool Use | 64 |
| Google | Function Calling | 64 |
| Ollama | Tools | Varies |

## Implementation

### OpenAI Function Calling

```python
from openai import OpenAI
import json
from typing import List, Dict, Callable

client = OpenAI()

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and country, e.g., 'London, UK'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Search the product database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["electronics", "clothing", "books", "all"]
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Tool implementations
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Mock weather function."""
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "condition": "sunny"
    }

def search_database(query: str, category: str = "all", max_results: int = 5) -> list:
    """Mock database search."""
    return [
        {"name": f"Product {i}", "price": 10 * i, "category": category}
        for i in range(1, min(max_results + 1, 6))
    ]

TOOL_REGISTRY = {
    "get_weather": get_weather,
    "search_database": search_database
}

def chat_with_tools(messages: List[Dict]) -> str:
    """Chat with tool use capability."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # or "none", "required", or specific tool
    )

    message = response.choices[0].message

    # Check if tool call is needed
    if message.tool_calls:
        # Add assistant message with tool calls
        messages.append(message)

        # Execute each tool call
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Execute the function
            if function_name in TOOL_REGISTRY:
                result = TOOL_REGISTRY[function_name](**arguments)
            else:
                result = {"error": f"Unknown function: {function_name}"}

            # Add tool result
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        # Get final response
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )

        return final_response.choices[0].message.content

    return message.content

# Usage
messages = [{"role": "user", "content": "What's the weather in Paris?"}]
response = chat_with_tools(messages)
print(response)
```

### Anthropic Tool Use

```python
from anthropic import Anthropic

client = Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country, e.g., 'London, UK'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    }
]

def chat_with_claude_tools(user_message: str) -> str:
    """Chat with Claude using tools."""
    messages = [{"role": "user", "content": user_message}]

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # Process tool use
    while response.stop_reason == "tool_use":
        # Extract tool use blocks
        tool_use_block = next(
            block for block in response.content
            if block.type == "tool_use"
        )

        # Execute tool
        tool_result = TOOL_REGISTRY[tool_use_block.name](**tool_use_block.input)

        # Continue conversation
        messages = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": json.dumps(tool_result)
                }]
            }
        ]

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

    # Get text response
    return next(
        block.text for block in response.content
        if hasattr(block, "text")
    )
```

### Parallel Tool Calls

```python
def execute_parallel_tools(tool_calls: list) -> list:
    """Execute multiple tool calls in parallel."""
    import concurrent.futures

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if function_name in TOOL_REGISTRY:
                future = executor.submit(
                    TOOL_REGISTRY[function_name],
                    **arguments
                )
                futures[future] = tool_call.id

        for future in concurrent.futures.as_completed(futures):
            tool_call_id = futures[future]
            try:
                result = future.result()
            except Exception as e:
                result = {"error": str(e)}

            results.append({
                "tool_call_id": tool_call_id,
                "content": json.dumps(result)
            })

    return results
```

### Tool Definition Generator

```python
from typing import Callable, get_type_hints
import inspect

def generate_tool_definition(func: Callable) -> dict:
    """Generate OpenAI tool definition from Python function."""
    sig = inspect.signature(func)
    hints = get_type_hints(func)
    doc = inspect.getdoc(func) or ""

    # Parse docstring for parameter descriptions
    param_descriptions = {}
    for line in doc.split("\n"):
        if ":" in line and line.strip().startswith(":param"):
            parts = line.split(":", 2)
            if len(parts) >= 3:
                param_name = parts[1].replace("param", "").strip()
                param_descriptions[param_name] = parts[2].strip()

    # Build properties
    properties = {}
    required = []

    for name, param in sig.parameters.items():
        if name in ["self", "cls"]:
            continue

        param_type = hints.get(name, str)

        # Map Python types to JSON schema types
        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object"
        }

        properties[name] = {
            "type": type_map.get(param_type, "string"),
            "description": param_descriptions.get(name, "")
        }

        if param.default == inspect.Parameter.empty:
            required.append(name)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": doc.split("\n")[0] if doc else "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

# Usage
def calculate_mortgage(
    principal: float,
    annual_rate: float,
    years: int
) -> dict:
    """Calculate monthly mortgage payment.

    :param principal: Loan amount in dollars
    :param annual_rate: Annual interest rate (e.g., 0.05 for 5%)
    :param years: Loan term in years
    """
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
              ((1 + monthly_rate)**num_payments - 1)
    return {"monthly_payment": round(payment, 2)}

tool_def = generate_tool_definition(calculate_mortgage)
print(json.dumps(tool_def, indent=2))
```

### Tool Router

```python
from dataclasses import dataclass
from typing import Dict, List, Callable, Any
import re

@dataclass
class Tool:
    name: str
    description: str
    function: Callable
    parameters: dict
    examples: List[str] = None  # Example queries this tool handles

class ToolRouter:
    """Route queries to appropriate tools."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        """Register a tool."""
        self.tools[tool.name] = tool

    def get_tool_definitions(self) -> List[dict]:
        """Get OpenAI tool definitions."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools.values()
        ]

    def execute(self, query: str) -> Dict[str, Any]:
        """Execute query with tool routing."""
        messages = [{"role": "user", "content": query}]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.get_tool_definitions(),
            tool_choice="auto"
        )

        message = response.choices[0].message
        result = {"query": query, "tool_calls": [], "final_response": None}

        # Handle tool calls
        while message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if tool_name in self.tools:
                    tool_result = self.tools[tool_name].function(**arguments)
                else:
                    tool_result = {"error": f"Unknown tool: {tool_name}"}

                result["tool_calls"].append({
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": tool_result
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result)
                })

            # Get next response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.get_tool_definitions()
            )
            message = response.choices[0].message

        result["final_response"] = message.content
        return result

# Usage
router = ToolRouter(client)

router.register(Tool(
    name="get_weather",
    description="Get weather for a location",
    function=get_weather,
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
        },
        "required": ["location"]
    }
))

result = router.execute("What's the weather in Tokyo?")
```

### Code Execution Tool

```python
import subprocess
import tempfile
import os

def execute_python(code: str, timeout: int = 30) -> dict:
    """Safely execute Python code in a sandbox."""
    # Create temporary file
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        delete=False
    ) as f:
        f.write(code)
        temp_path = f.name

    try:
        # Execute with timeout
        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {"error": f"Execution timed out after {timeout} seconds"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        os.unlink(temp_path)

# Tool definition for code execution
CODE_EXECUTION_TOOL = {
    "type": "function",
    "function": {
        "name": "execute_python",
        "description": "Execute Python code and return the output. Use for calculations, data processing, or generating results.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute"
                }
            },
            "required": ["code"]
        }
    }
}
```

### Agentic Tool Loop

```python
from typing import Optional
import logging

class AgentExecutor:
    """Execute tools in an agentic loop."""

    def __init__(
        self,
        client,
        tools: List[dict],
        tool_registry: Dict[str, Callable],
        model: str = "gpt-4o",
        max_iterations: int = 10
    ):
        self.client = client
        self.tools = tools
        self.tool_registry = tool_registry
        self.model = model
        self.max_iterations = max_iterations
        self.logger = logging.getLogger(__name__)

    def run(self, user_request: str, system_prompt: str = "") -> Dict:
        """Run agent until task complete or max iterations."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_request})

        iteration = 0
        tool_history = []

        while iteration < self.max_iterations:
            self.logger.info(f"Iteration {iteration + 1}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            # No tool calls - task complete
            if not message.tool_calls:
                return {
                    "success": True,
                    "response": message.content,
                    "iterations": iteration + 1,
                    "tool_history": tool_history
                }

            # Execute tool calls
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                self.logger.info(f"Calling {tool_name} with {arguments}")

                if tool_name in self.tool_registry:
                    try:
                        result = self.tool_registry[tool_name](**arguments)
                    except Exception as e:
                        result = {"error": str(e)}
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}

                tool_history.append({
                    "iteration": iteration + 1,
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            iteration += 1

        return {
            "success": False,
            "error": "Max iterations reached",
            "iterations": iteration,
            "tool_history": tool_history
        }

# Usage
agent = AgentExecutor(
    client=client,
    tools=tools,
    tool_registry=TOOL_REGISTRY,
    max_iterations=5
)

result = agent.run(
    user_request="Find the weather in Paris and convert the temperature to Fahrenheit",
    system_prompt="You are a helpful assistant. Use tools when needed."
)
```

### Production Tool Service

```python
from dataclasses import dataclass
from typing import Dict, List, Callable, Any, Optional
from enum import Enum
import logging
import time

class ToolCallPolicy(Enum):
    AUTO = "auto"
    REQUIRED = "required"
    NONE = "none"

@dataclass
class ToolConfig:
    max_tool_calls: int = 10
    timeout_per_tool: int = 30
    parallel_execution: bool = True
    policy: ToolCallPolicy = ToolCallPolicy.AUTO

class ToolService:
    """Production-ready tool calling service."""

    def __init__(
        self,
        client,
        model: str = "gpt-4o",
        config: Optional[ToolConfig] = None
    ):
        self.client = client
        self.model = model
        self.config = config or ToolConfig()
        self.tools: Dict[str, dict] = {}
        self.implementations: Dict[str, Callable] = {}
        self.logger = logging.getLogger(__name__)

    def register_tool(
        self,
        name: str,
        description: str,
        parameters: dict,
        implementation: Callable
    ):
        """Register a tool with its implementation."""
        self.tools[name] = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }
        self.implementations[name] = implementation

    def execute(
        self,
        messages: List[Dict],
        policy: Optional[ToolCallPolicy] = None
    ) -> Dict[str, Any]:
        """Execute a conversation with tool support."""
        policy = policy or self.config.policy
        tool_calls_made = 0
        start_time = time.time()

        tool_choice = {
            ToolCallPolicy.AUTO: "auto",
            ToolCallPolicy.REQUIRED: "required",
            ToolCallPolicy.NONE: "none"
        }[policy]

        while tool_calls_made < self.config.max_tool_calls:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=list(self.tools.values()) if self.tools else None,
                tool_choice=tool_choice if self.tools else None
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return {
                    "success": True,
                    "content": message.content,
                    "tool_calls_made": tool_calls_made,
                    "duration": time.time() - start_time
                }

            messages.append(message)

            # Execute tools
            tool_results = self._execute_tools(message.tool_calls)
            tool_calls_made += len(message.tool_calls)

            for result in tool_results:
                messages.append({
                    "role": "tool",
                    "tool_call_id": result["id"],
                    "content": json.dumps(result["result"])
                })

        return {
            "success": False,
            "error": "Max tool calls exceeded",
            "tool_calls_made": tool_calls_made,
            "duration": time.time() - start_time
        }

    def _execute_tools(self, tool_calls: list) -> List[Dict]:
        """Execute tool calls."""
        if self.config.parallel_execution:
            return self._execute_parallel(tool_calls)
        else:
            return self._execute_sequential(tool_calls)

    def _execute_sequential(self, tool_calls: list) -> List[Dict]:
        """Execute tools sequentially."""
        results = []

        for tool_call in tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            try:
                result = self.implementations[name](**args)
            except Exception as e:
                self.logger.error(f"Tool {name} failed: {e}")
                result = {"error": str(e)}

            results.append({
                "id": tool_call.id,
                "name": name,
                "result": result
            })

        return results

    def _execute_parallel(self, tool_calls: list) -> List[Dict]:
        """Execute tools in parallel."""
        import concurrent.futures

        results = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {}

            for tool_call in tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                future = executor.submit(
                    self._safe_execute,
                    name,
                    args
                )
                futures[future] = tool_call

            for future in concurrent.futures.as_completed(futures):
                tool_call = futures[future]
                result = future.result()

                results.append({
                    "id": tool_call.id,
                    "name": tool_call.function.name,
                    "result": result
                })

        return results

    def _safe_execute(self, name: str, args: dict) -> Any:
        """Safely execute a tool with error handling."""
        try:
            if name not in self.implementations:
                return {"error": f"Unknown tool: {name}"}
            return self.implementations[name](**args)
        except Exception as e:
            self.logger.error(f"Tool {name} error: {e}")
            return {"error": str(e)}
```

## Best Practices

1. **Tool Design**
   - Clear, specific descriptions
   - Well-defined parameter schemas
   - Handle errors gracefully

2. **Security**
   - Validate all inputs
   - Sandbox code execution
   - Limit tool permissions

3. **Performance**
   - Execute independent tools in parallel
   - Set appropriate timeouts
   - Cache frequently used results

4. **Error Handling**
   - Return structured error messages
   - Allow LLM to recover from errors
   - Log all tool executions

5. **Testing**
   - Test tools independently
   - Test tool selection by LLM
   - Test error recovery

## Common Pitfalls

1. **Vague Descriptions** - LLM can't choose the right tool
2. **Missing Parameters** - Function fails with missing args
3. **No Error Handling** - Crashes propagate to user
4. **Infinite Loops** - No iteration limit in agent loops
5. **Security Holes** - Unsafe code execution
6. **No Timeout** - Tools can hang indefinitely

## References

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)
