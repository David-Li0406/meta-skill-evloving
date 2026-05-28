---
name: python-result-pattern
description: >
  Implement the Result[T] = Union[Success[T], Failure] pattern for explicit, type-safe error handling
  in Python. Use this skill when writing service methods that can fail, adding new error codes, 
  refactoring try/except blocks, or implementing Railway-Oriented Programming patterns. This pattern
  replaces exceptions for control flow, making errors explicit in function signatures.
version: 1.0.0
tags:
  - python
  - error-handling
  - functional-programming
  - type-safety
  - services
  - result-pattern
author: context-harness
---

# Python Result Pattern

A comprehensive guide for implementing the Result pattern in context-harness Python services. This pattern provides explicit, type-safe error handling without relying on exceptions for control flow.

## Overview

The Result pattern is a functional programming approach where functions that can fail return a discriminated union type (`Result[T]`) that is either:
- `Success[T]` - contains the success value
- `Failure` - contains error information (message, code, details)

This approach:
- Makes errors explicit in function signatures
- Forces callers to handle both success and failure cases
- Eliminates hidden control flow via exceptions
- Provides structured error information with standardized codes
- Enables type-safe error propagation

## When to Use This Skill

Activate this skill when:

- **Implementing new service methods** that can fail (I/O, validation, external calls)
- **Adding error handling** to existing code
- **Working with files in** `src/context_harness/services/`
- **Adding new error codes** to the `ErrorCode` enum
- **Refactoring try/except blocks** to Result pattern
- **Writing tests** for service methods that return Results
- **Chaining multiple operations** that can fail

## Core Components

### 1. Result Type Definition

Located in `src/context_harness/primitives/result.py`:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Generic, Optional, TypeVar, Union

T = TypeVar("T")

@dataclass(frozen=True)
class Success(Generic[T]):
    """Successful operation result."""
    value: T
    message: Optional[str] = None

@dataclass(frozen=True)
class Failure:
    """Failed operation result."""
    error: str
    code: ErrorCode
    details: Optional[Dict[str, Any]] = None

# The Result type alias
Result = Union[Success[T], Failure]
```

### 2. ErrorCode Enum

Standardized error codes for categorization:

```python
class ErrorCode(Enum):
    # General errors
    NOT_FOUND = "not_found"
    ALREADY_EXISTS = "already_exists"
    VALIDATION_ERROR = "validation_error"
    PERMISSION_DENIED = "permission_denied"
    UNKNOWN = "unknown"

    # Authentication errors
    AUTH_REQUIRED = "auth_required"
    AUTH_FAILED = "auth_failed"
    AUTH_EXPIRED = "auth_expired"
    AUTH_CANCELLED = "auth_cancelled"
    TOKEN_EXPIRED = "token_expired"
    TOKEN_REFRESH_FAILED = "token_refresh_failed"

    # Network errors
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"

    # Configuration errors
    CONFIG_INVALID = "config_invalid"
    CONFIG_MISSING = "config_missing"

    # Skill errors
    SKILL_NOT_FOUND = "skill_not_found"
    SKILL_INVALID = "skill_invalid"
    SKILL_INSTALL_FAILED = "skill_install_failed"

    # Session errors
    SESSION_NOT_FOUND = "session_not_found"
    SESSION_CORRUPTED = "session_corrupted"

    # MCP errors
    MCP_SERVER_NOT_FOUND = "mcp_server_not_found"
    MCP_CONFIG_ERROR = "mcp_config_error"
```

### 3. Factory Functions

Helper functions for creating Results:

```python
def success(value: T, message: Optional[str] = None) -> Success[T]:
    """Create a Success result."""
    return Success(value=value, message=message)

def failure(
    error: str,
    code: ErrorCode = ErrorCode.UNKNOWN,
    details: Optional[Dict[str, Any]] = None,
) -> Failure:
    """Create a Failure result."""
    return Failure(error=error, code=code, details=details)

def is_success(result: Result[T]) -> bool:
    """Check if a result is a Success."""
    return isinstance(result, Success)

def is_failure(result: Result[T]) -> bool:
    """Check if a result is a Failure."""
    return isinstance(result, Failure)
```

## Implementation Guide

### Step 1: Define Function Signature

Always declare the return type as `Result[T]` where `T` is your success value type:

```python
from context_harness.primitives import (
    ErrorCode,
    Failure,
    Result,
    Success,
)

def load_config(path: Path) -> Result[Dict[str, Any]]:
    """Load configuration from file.
    
    Returns:
        Result containing config dict or Failure
    """
    ...
```

### Step 2: Handle All Failure Cases

Return `Failure` with appropriate error code for each failure case:

```python
def load_config(path: Path) -> Result[Dict[str, Any]]:
    if not path.exists():
        return Failure(
            error=f"Configuration file not found: {path}",
            code=ErrorCode.CONFIG_MISSING,
            details={"path": str(path)},
        )
    
    try:
        with open(path) as f:
            data = json.load(f)
        return Success(value=data)
    except json.JSONDecodeError as e:
        return Failure(
            error=f"Invalid JSON: {e}",
            code=ErrorCode.CONFIG_INVALID,
            details={"path": str(path), "error": str(e)},
        )
    except PermissionError:
        return Failure(
            error=f"Permission denied: {path}",
            code=ErrorCode.PERMISSION_DENIED,
            details={"path": str(path)},
        )
```

### Step 3: Check Results with isinstance

Use `isinstance` for type-safe result checking:

```python
def use_config(path: Path) -> Result[bool]:
    # Call function that returns Result
    result = load_config(path)
    
    # Check for failure first (early return pattern)
    if isinstance(result, Failure):
        return result  # Propagate failure as-is
    
    # Type narrowing: result is now Success[Dict[str, Any]]
    config = result.value
    
    # Use the config...
    return Success(value=True, message="Config loaded successfully")
```

### Step 4: Chain Multiple Operations

For operations that depend on each other:

```python
def install_skill(skill_name: str, project_path: Path) -> Result[Skill]:
    # Step 1: Get skill info
    info_result = self.get_info(skill_name)
    if isinstance(info_result, Failure):
        return info_result  # Propagate failure
    
    skill = info_result.value
    
    # Step 2: Validate destination
    skill_dest = project_path / ".opencode" / "skill" / skill_name
    if skill_dest.exists():
        return Failure(
            error=f"Skill '{skill_name}' already installed",
            code=ErrorCode.ALREADY_EXISTS,
            details={"path": str(skill_dest)},
        )
    
    # Step 3: Fetch files
    if not self.github.fetch_directory(...):
        return Failure(
            error=f"Failed to install skill '{skill_name}'",
            code=ErrorCode.SKILL_INSTALL_FAILED,
        )
    
    # Step 4: Return success
    return Success(
        value=installed_skill,
        message=f"Skill '{skill_name}' installed successfully",
    )
```

## Testing Patterns

### Testing Success Cases

```python
def test_load_existing_config(self, tmp_path: Path) -> None:
    """Should load valid opencode.json."""
    config_data = {"$schema": "https://opencode.ai/config.json"}
    config_path = tmp_path / "opencode.json"
    config_path.write_text(json.dumps(config_data))

    service = ConfigService()
    result = service.load(tmp_path)

    assert isinstance(result, Success)
    assert result.value is not None
```

### Testing Failure Cases

```python
def test_load_missing_config(self, tmp_path: Path) -> None:
    """Should return Failure for missing config."""
    service = ConfigService()
    result = service.load(tmp_path)

    assert isinstance(result, Failure)
    assert result.code == ErrorCode.CONFIG_MISSING
```

### Testing Error Codes

```python
def test_load_invalid_json(self, tmp_path: Path) -> None:
    """Should return Failure for invalid JSON."""
    config_path = tmp_path / "opencode.json"
    config_path.write_text("{ invalid json }")

    service = ConfigService()
    result = service.load(tmp_path)

    assert isinstance(result, Failure)
    assert result.code == ErrorCode.CONFIG_INVALID
    assert "path" in result.details
```

## Best Practices

### DO ✅

1. **Always type annotate** with `Result[T]`
2. **Use specific ErrorCodes** - add new ones if needed
3. **Include details dict** with context for debugging
4. **Return early on failure** - don't nest deeply
5. **Propagate failures unchanged** when appropriate
6. **Use frozen dataclasses** for immutability
7. **Add success messages** for user feedback

### DON'T ❌

1. **Don't use exceptions** for expected failure cases
2. **Don't ignore the result** - always check
3. **Don't use generic UNKNOWN** when a specific code applies
4. **Don't mutate results** - they're frozen
5. **Don't catch and re-raise as Failure** without adding value

## Adding New Error Codes

When you need a new error code:

1. Add to `ErrorCode` enum in `src/context_harness/primitives/result.py`
2. Group with related codes (auth, network, config, etc.)
3. Use snake_case with descriptive names
4. Update this skill document

```python
class ErrorCode(Enum):
    # Your new domain errors
    PLUGIN_NOT_FOUND = "plugin_not_found"
    PLUGIN_LOAD_FAILED = "plugin_load_failed"
```

## Template for New Service Methods

```python
def your_method(self, param: str) -> Result[YourReturnType]:
    """One-line description.
    
    Args:
        param: Description of parameter
        
    Returns:
        Result containing YourReturnType or Failure
    """
    # Validation
    if not param:
        return Failure(
            error="Parameter cannot be empty",
            code=ErrorCode.VALIDATION_ERROR,
        )
    
    # Operation that might fail
    try:
        result = some_operation(param)
    except SomeExpectedException as e:
        return Failure(
            error=f"Operation failed: {e}",
            code=ErrorCode.SPECIFIC_CODE,
            details={"param": param},
        )
    
    # Chain dependent operations
    dependent_result = self.other_method(result)
    if isinstance(dependent_result, Failure):
        return dependent_result
    
    # Success
    return Success(
        value=dependent_result.value,
        message="Operation completed successfully",
    )
```

## References

- [Railway Oriented Programming](https://fsharpforfunandprofit.com/rop/) - Original concept
- [Result Pattern in Python](https://returns.readthedocs.io/) - Returns library (similar concept)
- [src/context_harness/primitives/result.py](../../../src/context_harness/primitives/result.py) - Implementation

---

_Skill version 1.0.0 | Last updated: 2025-12-30_
