---
title: Write Clear Docstrings for Tool Descriptions
impact: HIGH
impactDescription: LLM uses docstrings to understand tool purpose
tags: tool, docstring, documentation, schema
---

## Write Clear Docstrings for Tool Descriptions

**Impact: HIGH (LLM uses docstrings to understand tool purpose)**

The SDK extracts tool descriptions and argument descriptions from docstrings. Clear docstrings help the LLM choose and use tools correctly.

**Incorrect (missing or poor docstrings):**

```python
from agents import function_tool

@function_tool
def process_data(data, format):  # No types, no docstring
    return str(data)

@function_tool
def fetch_user(user_id: str) -> str:
    # No docstring - LLM doesn't know when to use this
    return f"User {user_id}"
```

**Correct (clear docstrings with Args):**

```python
from agents import function_tool

@function_tool
def fetch_user_profile(user_id: str, include_history: bool = False) -> str:
    """Fetch a user's profile information from the database.
    
    Call this when you need to look up user details like name, email,
    or account status. Use include_history for support inquiries.
    
    Args:
        user_id: The unique identifier of the user (e.g., "usr_123").
        include_history: Whether to include purchase history. Default False.
    
    Returns:
        JSON string with user profile data.
    """
    return '{"name": "John", "email": "john@example.com"}'
```

**Supported docstring formats:**

- Google style (shown above) - recommended
- Sphinx style (`:param name: description`)
- NumPy style

**Disable docstring parsing if needed:**

```python
@function_tool(use_docstring_info=False)
def my_tool(x: str) -> str:
    """This docstring will be ignored."""
    return x
```

Reference: [Tools Documentation - Docstring Parsing](https://openai.github.io/openai-agents-python/tools/#automatic-argument-and-docstring-parsing)
