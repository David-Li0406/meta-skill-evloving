---
name: error-handling-patterns
description: Use this skill when implementing error handling, designing APIs, or improving application reliability across various programming languages.
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

| Approach       | Use When                                   |
|----------------|--------------------------------------------|
| Exceptions     | Unexpected errors, exceptional conditions  |
| Result Types   | Expected errors, validation failures       |
| Error Codes    | C-style APIs, legacy integration           |

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

class ExternalServiceError(ApplicationError):
    """Raised when external service fails."""
    def __init__(self, message: str, service: str, **kwargs):
        super().__init__(message, **kwargs)
        self.service = service
```

### C# Error Handling

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
    public ValidationException(string message)
        : base(message, "VALIDATION_ERROR") { }
}

public class NotFoundException : ApplicationException
{
    public NotFoundException(string resource, Guid id)
        : base($"{resource} not found: {id}", "NOT_FOUND") { }
}
```

### TypeScript Result Type Pattern

```typescript
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

function Ok<T>(value: T): Result<T, never> {
    return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
    return { ok: false, error };
}

// Usage
function parseJSON<T>(json: string): Result<T, SyntaxError> {
    try {
        return Ok(JSON.parse(json) as T);
    } catch (error) {
        return Err(error as SyntaxError);
    }
}
```

### Resilience with Polly in .NET

**HTTP Retry with Exponential Backoff:**

```csharp
public IAsyncPolicy<HttpResponseMessage> BuildHttpRetryPolicy(int retryCount = 3)
{
    return HttpPolicyExtensions
        .HandleTransientHttpError()
        .WaitAndRetryAsync(retryCount, retryAttempt => 
            TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));
}
```