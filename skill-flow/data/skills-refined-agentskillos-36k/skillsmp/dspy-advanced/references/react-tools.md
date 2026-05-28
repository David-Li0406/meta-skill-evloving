# DSPy ReAct Agents and Tools

ReAct combines reasoning and action, enabling agents to use tools to answer complex questions. This guide covers ReAct agent patterns and tool integration.

## Table of Contents

- [ReAct Overview](#react-overview)
- [Basic ReAct Agent](#basic-react-agent)
- [Tool Definition](#tool-definition)
- [Multi-Tool Coordination](#multi-tool-coordination)
- [Tool Error Handling](#tool-error-handling)
- [Best Practices](#best-practices)

## ReAct Overview

### What is ReAct?

ReAct (Reasoning + Acting) is an agent pattern that combines language model reasoning with the ability to use external tools. It follows a loop of:
1. **Reason**: Analyze the current state and decide on next action
2. **Act**: Call a tool or provide the final answer
3. **Observe**: Update state with tool results

### Why Use ReAct?

- **Complex tasks**: Questions requiring multiple steps and tools
- **External knowledge**: Access to APIs, databases, search engines
- **Dynamic reasoning**: Adapt to intermediate results
- **Traceability**: Full trajectory of tool calls for debugging

## Basic ReAct Agent

### Simple ReAct with Single Tool

```python
import dspy

# Define tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # In a real implementation, this would call a weather API
    return f"The weather in {city} is sunny and 75°F"

# Create ReAct agent
react = dspy.ReAct(
    signature="question -> answer",
    tools=[get_weather],
    max_iters=5
)

# Use agent
result = react(question="What's the weather like in Tokyo?")
print(result.answer)
print("Tool calls made:", result.trajectory)
```

**Key components:**
- `signature`: Input/output structure for the agent
- `tools`: List of available tool functions
- `max_iters`: Maximum number of reasoning/action cycles

### ReAct with Multiple Tools

```python
# Define tools
def evaluate_math(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return dspy.PythonInterpreter({}).execute(expression)

def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    results = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')(query, k=3)
    return [x['text'] for x in results]

# Create ReAct agent
react = dspy.ReAct(
    "question -> answer: float",
    tools=[evaluate_math, search_wikipedia],
    max_iters=5
)

# Use agent
pred = react(question="What is 9362158 divided by the year of birth of David Gregory of Kinnairdy castle?")
print(pred.answer)
```

## Tool Definition

### Tool Function Requirements

Tools are Python functions with:
1. **Type hints**: Parameter and return types
2. **Docstrings**: Clear description of what the tool does
3. **Valid inputs**: Should accept the types hinted
4. **Return values**: Should return the hinted type

### Tool Example: Calculator

```python
def calculate(expression: str) -> float:
    """
    Calculate the result of a mathematical expression.

    Args:
        expression: A mathematical expression as a string (e.g., "2+2", "10*5")

    Returns:
        float: The result of the calculation
    """
    try:
        import ast
        import operator

        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
        }

        node = ast.parse(expression, mode='eval').body

        def eval_node(n):
            if isinstance(n, ast.Num):
                return n.n
            elif isinstance(n, ast.BinOp):
                left = eval_node(n.left)
                right = eval_node(n.right)
                return ops[type(n.op)](left, right)
            else:
                raise ValueError(f"Unsupported operation: {type(n)}")

        return float(eval_node(node))
    except Exception as e:
        return float('nan')
```

### Tool Example: API Caller

```python
import requests

def get_stock_price(symbol: str) -> str:
    """
    Get the current stock price for a given symbol.

    Args:
        symbol: Stock symbol (e.g., "AAPL", "GOOGL")

    Returns:
        str: Current stock price as a string
    """
    try:
        response = requests.get(f"https://api.example.com/stock/{symbol}")
        data = response.json()
        return str(data.get('price', 'N/A'))
    except Exception as e:
        return f"Error: {str(e)}"
```

## Multi-Tool Coordination

### Sequential Tool Usage

ReAct automatically handles sequential tool usage:

```python
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for '{query}'"

def summarize(text: str) -> str:
    """Summarize the given text."""
    return f"Summary of: {text[:50]}..."

react = dspy.ReAct(
    "task -> summary",
    tools=[search_web, summarize],
    max_iters=5
)

result = react(task="Summarize the latest news about AI")
# ReAct will:
# 1. Call search_web with "latest news about AI"
# 2. Call summarize with search results
# 3. Return final summary
```

### Conditional Tool Selection

ReAct reasons about which tool to use based on context:

```python
def check_email(user: str) -> str:
    """Check if user has unread emails."""
    return f"{user} has 5 unread emails"

def check_calendar(user: str) -> str:
    """Check user's calendar for today."""
    return f"{user} has 3 meetings today"

react = dspy.ReAct(
    "user -> status",
    tools=[check_email, check_calendar],
    max_iters=5
)

result = react(user="Alice")
# ReAct will reason about which tool(s) to call
```

### Tool Output as Input

Tools can use outputs from previous tool calls:

```python
def get_city_name(user: str) -> str:
    """Get the city where the user is located."""
    return "San Francisco"

def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: 72°F, sunny"

react = dspy.ReAct(
    "user -> weather_report",
    tools=[get_city_name, get_weather],
    max_iters=5
)

result = react(user="Alice")
# ReAct will:
# 1. Call get_city_name("Alice") → "San Francisco"
# 2. Call get_weather("San Francisco") → "Weather in San Francisco: 72°F, sunny"
```

## Tool Error Handling

### Graceful Error Handling

Tools should handle errors gracefully:

```python
def robust_search(query: str) -> str:
    """Search with error handling."""
    try:
        results = search_api(query)
        return results[0]['text']
    except IndexError:
        return "No results found"
    except Exception as e:
        return f"Search error: {str(e)}"
```

### Tool Validation

Validate tool inputs before processing:

```python
def validated_calculate(expression: str) -> float:
    """Calculate with input validation."""
    # Validate input
    if not isinstance(expression, str):
        raise TypeError("Expression must be a string")

    if len(expression) > 100:
        raise ValueError("Expression too long")

    # Process input
    result = calculate(expression)

    # Validate output
    if isinstance(result, float) and not (result != result):  # Check for NaN
        return result
    else:
        raise ValueError("Invalid calculation result")
```

## Best Practices

### 1. Clear Tool Names

```python
# Good: Descriptive name
def get_weather_forecast(city: str) -> str:
    pass

# Bad: Vague name
def get_info(location: str) -> str:
    pass
```

### 2. Comprehensive Docstrings

```python
# Good: Detailed docstring
def calculate_expression(expr: str) -> float:
    """
    Calculate a mathematical expression.

    Supports basic operations: +, -, *, /
    Example: "2+2" returns 4.0

    Args:
        expr: Mathematical expression as string

    Returns:
        float: Calculation result

    Raises:
        ValueError: For invalid expressions
    """
    pass

# Bad: Minimal docstring
def calculate(expr: str) -> float:
    """Calculate."""
    pass
```

### 3. Type Hints for All Parameters

```python
# Good: All parameters have type hints
def query_database(table: str, limit: int = 10) -> list[dict]:
    pass

# Bad: Missing type hints
def query_database(table, limit=10):
    pass
```

### 4. Handle All Exceptions

```python
# Good: Handle all exceptions
def safe_api_call(endpoint: str) -> str:
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"API error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Bad: Not handling exceptions
def unsafe_api_call(endpoint: str) -> str:
    response = requests.get(endpoint)
    return response.text
```

### 5. Return Meaningful Error Messages

```python
# Good: Meaningful error messages
def divide_numbers(a: float, b: float) -> float:
    if b == 0:
        raise ValueError(f"Cannot divide by zero: {a} / {b}")
    return a / b

# Bad: Generic error messages
def divide_numbers(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Error")
    return a / b
```

## Common Issues and Solutions

### Issue: Tool Not Found

**Problem**: ReAct doesn't recognize the tool

**Solution**:
1. Check tool is in the `tools` list
2. Verify tool is defined before creating ReAct agent
3. Check tool name is unique

### Issue: Wrong Tool Arguments

**Problem**: ReAct passes incorrect arguments to tool

**Solution**:
1. Check type hints match expected types
2. Verify tool accepts all arguments from reasoning
3. Add default values for optional parameters

### Issue: Tool Returns Wrong Type

**Problem**: Tool returns type different from hint

**Solution**:
1. Verify return type matches hint
2. Add type conversion if needed
3. Return consistent types (always str or always dict)

### Issue: Too Many Tool Calls

**Problem**: ReAct calls tools excessively

**Solution**:
1. Reduce `max_iters` parameter
2. Improve tool docstrings for better reasoning
3. Add validation to prevent redundant calls
