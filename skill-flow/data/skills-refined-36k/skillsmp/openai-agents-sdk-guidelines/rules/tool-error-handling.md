---
title: Handle Tool Errors with failure_error_function
impact: MEDIUM
impactDescription: Graceful error handling for tool failures
tags: tool, error-handling, failure, resilience
---

## Handle Tool Errors with failure_error_function

**Impact: MEDIUM (graceful error handling for tool failures)**

Use `failure_error_function` to provide custom error messages when tools fail, instead of crashing or exposing internal errors.

**Default behavior (generic error message):**

```python
from agents import function_tool

@function_tool
def fetch_data(query: str) -> str:
    """Fetch data from API."""
    raise ConnectionError("API timeout")  # Default handler tells LLM "an error occurred"
```

**Correct (custom error handling):**

```python
from agents import function_tool, RunContextWrapper
from typing import Any

def handle_api_error(ctx: RunContextWrapper[Any], error: Exception) -> str:
    """Provide user-friendly error message to the LLM."""
    if isinstance(error, ConnectionError):
        return "The data service is temporarily unavailable. Please try again later."
    elif isinstance(error, ValueError):
        return f"Invalid input: {error}. Please check the parameters."
    else:
        # Log the actual error for debugging
        print(f"Unexpected error: {error}")
        return "An unexpected error occurred. Please try a different approach."

@function_tool(failure_error_function=handle_api_error)
def fetch_data(query: str) -> str:
    """Fetch data from the API.
    
    Args:
        query: The search query.
    """
    if not query:
        raise ValueError("Query cannot be empty")
    # Simulated API call that might fail
    raise ConnectionError("API timeout")
```

**Re-raise errors for manual handling:**

```python
@function_tool(failure_error_function=None)  # Explicitly None
def critical_operation(data: str) -> str:
    """Operation where you want to handle errors yourself."""
    raise ValueError("Something went wrong")

# Errors will propagate - catch them in your Runner.run() call
try:
    result = await Runner.run(agent, "Do the operation")
except Exception as e:
    # Handle at application level
    pass
```

Reference: [Tools Documentation - Error Handling](https://openai.github.io/openai-agents-python/tools/#handling-errors-in-function-tools)
