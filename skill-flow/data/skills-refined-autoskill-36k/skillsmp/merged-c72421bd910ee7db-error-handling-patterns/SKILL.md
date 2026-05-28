---
name: error-handling-patterns
description: Master error handling patterns across languages including exceptions, Result types, error propagation, and graceful degradation to build resilient applications. Use when implementing error handling, designing APIs, or improving application reliability.
---

# Error Handling Patterns

Build resilient applications with robust error handling strategies that gracefully handle failures and provide excellent debugging experiences.

## When to Use This Skill

- Implementing error handling in new features
- Designing error-resilient APIs
- Debugging production issues
- Improving application reliability
- Creating better error messages for users and developers
- Implementing retry and circuit breaker patterns
- Handling async/concurrent errors
- Building fault-tolerant distributed systems

## Core Concepts

### 1. Error Handling Philosophies

| Approach        | Use When                                      |
|-----------------|-----------------------------------------------|
| Exceptions      | Unexpected errors, exceptional conditions     |
| Result Types    | Expected errors, validation failures          |
| Error Codes     | C-style APIs, legacy integration              |

### 2. Error Categories

**Recoverable Errors:**
- Network timeouts
- Missing files
- Invalid user input
- API rate limits

**Unrecoverable Errors:**
- Out of memory
- Stack overflow
- Programming bugs (null pointer, etc.)

## Language-Specific Patterns

### Python Error Handling

**Custom Exception Hierarchy:**

```python
class ApplicationError(Exception):
    """Base exception for all application errors."""
    def __init__(self, message: str, code: str = None, details: dict = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}
        self.timestamp = datetime.utcnow()

class ValidationError(ApplicationError):
    """Raised when validation fails."""
    pass

class NotFoundError(ApplicationError):
    """Raised when resource not found."""
    pass
```

**Retry with Exponential Backoff:**

```python
import time
from functools import wraps
from typing import TypeVar, Callable

T = TypeVar('T')

def retry(max_attempts: int = 3, backoff_factor: float = 2.0, exceptions: tuple = (Exception,)):
    """Retry decorator with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(backoff_factor ** attempt)
                        continue
                    raise
            raise last_exception
        return wrapper
    return decorator
```

### TypeScript/JavaScript Error Handling

**Custom Error Classes:**

```typescript
class ApplicationError extends Error {
  constructor(message: string, public code: string, public statusCode: number = 500) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends ApplicationError {
  constructor(message: string) {
    super(message, "VALIDATION_ERROR", 400);
  }
}
```

**Result Type Pattern:**

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

function Ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}
```

### .NET Exception Patterns

**Custom Exception Hierarchy:**

```csharp
public class ApplicationException : Exception
{
    public string Code { get; }
    public ApplicationException(string message, string code) : base(message)
    {
        Code = code;
    }
}

public class ValidationException : ApplicationException
{
    public ValidationException(string message) : base(message, "VALIDATION_ERROR") { }
}
```

## Universal Patterns

### Circuit Breaker

Prevent cascading failures in distributed systems.

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: timedelta = timedelta(seconds=60)):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def call(self, func: Callable[[], T]) -> T:
        if self.state == CircuitState.OPEN:
            raise Exception("Circuit breaker is OPEN")
        try:
            result = func()
            self.on_success()
            return result
        except Exception:
            self.on_failure()
            raise
```

### Graceful Degradation

Provide fallback functionality when errors occur.

```python
def with_fallback(primary: Callable[[], T], fallback: Callable[[], T]) -> T:
    """Try primary function, fall back to fallback on error."""
    try:
        return primary()
    except Exception:
        return fallback()
```

## Best Practices

1. **Fail Fast**: Validate input early, fail quickly.
2. **Preserve Context**: Include stack traces, metadata, timestamps.
3. **Meaningful Messages**: Explain what happened and how to fix it.
4. **Log Appropriately**: Error = log, expected failure = don't spam logs.
5. **Handle at Right Level**: Catch where you can meaningfully handle.
6. **Clean Up Resources**: Use try-finally, context managers.
7. **Don't Swallow Errors**: Log or re-throw, don't silently ignore.
8. **Type-Safe Errors**: Use typed errors when possible.

## Common Pitfalls

- **Catching Too Broadly**: `except Exception` hides bugs.
- **Empty Catch Blocks**: Silently swallowing errors.
- **Poor Error Messages**: "Error occurred" is not helpful.
- **Ignoring Async Errors**: Unhandled promise rejections.