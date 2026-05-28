# Error Handling

Error codes, formats, and recovery patterns for the chat API.

---

## Error Response Format

All errors follow a consistent structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "field": "optional_field_name",
    "details": {}
  }
}
```

### Schema

```python
from pydantic import BaseModel
from typing import Optional, Any


class ErrorDetail(BaseModel):
    code: str
    message: str
    field: Optional[str] = None
    details: Optional[dict[str, Any]] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
```

---

## Error Codes by Step

### Step 1: Validation Errors (400)

| Code | Message | When |
|------|---------|------|
| `VALIDATION_ERROR` | Field-specific message | Any validation failure |
| `MESSAGE_REQUIRED` | Message is required | Empty/missing message |
| `MESSAGE_TOO_LONG` | Message exceeds maximum length | > 100,000 chars |
| `INVALID_CONVERSATION_ID` | Invalid conversation_id format | Bad UUID format |
| `INVALID_MODEL` | Model not supported | Unknown model name |

```python
# Example responses
{
  "error": {
    "code": "MESSAGE_REQUIRED",
    "message": "Message is required",
    "field": "message"
  }
}

{
  "error": {
    "code": "INVALID_MODEL",
    "message": "Model 'gpt-5' is not supported",
    "field": "model",
    "details": {
      "allowed_models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
    }
  }
}
```

### Step 2: Authentication Errors (401, 403)

| Code | Status | Message | When |
|------|--------|---------|------|
| `AUTHENTICATION_REQUIRED` | 401 | Authentication required | No token |
| `INVALID_TOKEN_FORMAT` | 401 | Invalid authorization header format | Not "Bearer <token>" |
| `TOKEN_EXPIRED` | 401 | Authentication token expired | JWT expired |
| `INVALID_TOKEN` | 401 | Invalid authentication token | Bad signature/format |
| `TOKEN_MISSING_CLAIMS` | 401 | Token missing required claims | No sub/email |
| `FORBIDDEN` | 403 | Cannot access another user's chat | user_id mismatch |

```python
# 401 responses include WWW-Authenticate header
{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Authentication token expired"
  }
}

# 403 response
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Cannot access another user's chat"
  }
}
```

### Step 3: Resolution Errors (404)

| Code | Status | Message | When |
|------|--------|---------|------|
| `CONVERSATION_NOT_FOUND` | 404 | Conversation not found | ID doesn't exist or not owned |

```python
{
  "error": {
    "code": "CONVERSATION_NOT_FOUND",
    "message": "Conversation not found"
  }
}
```

**Security note**: Always return 404 (not 403) when conversation exists but belongs to another user. This prevents enumeration attacks.

### Step 4: Agent Errors (503)

| Code | Status | Message | When |
|------|--------|---------|------|
| `AGENT_UNAVAILABLE` | 503 | Agent temporarily unavailable | Agent call failed |
| `AGENT_TIMEOUT` | 503 | Agent request timed out | Timeout exceeded |
| `RATE_LIMITED` | 429 | Too many requests | Rate limit hit |
| `CONTENT_FILTERED` | 400 | Content policy violation | Blocked content |

```python
{
  "error": {
    "code": "AGENT_UNAVAILABLE",
    "message": "Agent temporarily unavailable. Please retry.",
    "details": {
      "retry_after": 5
    }
  }
}

{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Please wait before retrying.",
    "details": {
      "retry_after": 60
    }
  }
}
```

### Step 5: Unexpected Errors (500)

| Code | Status | Message | When |
|------|--------|---------|------|
| `INTERNAL_ERROR` | 500 | An unexpected error occurred | Unhandled exception |
| `DATABASE_ERROR` | 503 | Database temporarily unavailable | DB connection failed |

```python
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred"
  }
}
```

---

## Implementation

### Custom Exception Classes

```python
# exceptions.py
from fastapi import HTTPException, status


class ChatAPIError(HTTPException):
    """Base exception for chat API errors."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        field: str | None = None,
        details: dict | None = None,
        headers: dict | None = None
    ):
        self.code = code
        self.field = field
        self.details = details
        super().__init__(
            status_code=status_code,
            detail={
                "error": {
                    "code": code,
                    "message": message,
                    **({"field": field} if field else {}),
                    **({"details": details} if details else {})
                }
            },
            headers=headers
        )


class ValidationError(ChatAPIError):
    def __init__(self, message: str, field: str | None = None, details: dict | None = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="VALIDATION_ERROR",
            message=message,
            field=field,
            details=details
        )


class AuthenticationError(ChatAPIError):
    def __init__(self, code: str, message: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=code,
            message=message,
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenError(ChatAPIError):
    def __init__(self, message: str = "Cannot access another user's chat"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            message=message
        )


class NotFoundError(ChatAPIError):
    def __init__(self, resource: str = "Conversation"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code=f"{resource.upper()}_NOT_FOUND",
            message=f"{resource} not found"
        )


class AgentError(ChatAPIError):
    def __init__(self, message: str = "Agent temporarily unavailable", retry_after: int | None = None):
        details = {"retry_after": retry_after} if retry_after else None
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="AGENT_UNAVAILABLE",
            message=message,
            details=details
        )


class RateLimitError(ChatAPIError):
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="RATE_LIMITED",
            message="Too many requests. Please wait before retrying.",
            details={"retry_after": retry_after},
            headers={"Retry-After": str(retry_after)}
        )
```

### Exception Handlers

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Convert Pydantic validation errors to our format."""
    errors = exc.errors()
    first_error = errors[0] if errors else {}

    field_path = ".".join(str(loc) for loc in first_error.get("loc", [])[1:])  # Skip 'body'
    message = first_error.get("msg", "Validation failed")

    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": message,
                "field": field_path if field_path else None
            }
        }
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors."""
    # Log the actual error for debugging
    logger.error(f"Database error: {exc}")

    return JSONResponse(
        status_code=503,
        content={
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Database temporarily unavailable"
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch-all for unexpected errors."""
    # Log for debugging
    logger.exception(f"Unexpected error: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )
```

---

## Client-Side Error Handling

### Retry Strategy

```typescript
interface RetryConfig {
  maxRetries: number;
  baseDelay: number;
  maxDelay: number;
}

const defaultRetryConfig: RetryConfig = {
  maxRetries: 3,
  baseDelay: 1000,
  maxDelay: 30000
};

function shouldRetry(status: number, code: string): boolean {
  // Retry on server errors and rate limits
  if (status === 429) return true;
  if (status === 503) return true;
  if (status >= 500) return true;

  // Don't retry client errors
  return false;
}

async function chatWithRetry(
  request: ChatRequest,
  config: RetryConfig = defaultRetryConfig
): Promise<ChatResponse> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < config.maxRetries; attempt++) {
    try {
      return await chat(request);
    } catch (error) {
      lastError = error;

      if (!shouldRetry(error.status, error.code)) {
        throw error;
      }

      // Calculate delay with exponential backoff
      const delay = Math.min(
        config.baseDelay * Math.pow(2, attempt),
        config.maxDelay
      );

      // Use server-provided retry-after if available
      const retryAfter = error.details?.retry_after;
      const actualDelay = retryAfter ? retryAfter * 1000 : delay;

      await sleep(actualDelay);
    }
  }

  throw lastError;
}
```

### Error Display Mapping

```typescript
const errorMessages: Record<string, string> = {
  'VALIDATION_ERROR': 'Please check your input and try again.',
  'AUTHENTICATION_REQUIRED': 'Please sign in to continue.',
  'TOKEN_EXPIRED': 'Your session has expired. Please sign in again.',
  'FORBIDDEN': 'You don\'t have permission to access this resource.',
  'CONVERSATION_NOT_FOUND': 'This conversation no longer exists.',
  'AGENT_UNAVAILABLE': 'The AI is temporarily unavailable. Retrying...',
  'RATE_LIMITED': 'Too many requests. Please wait a moment.',
  'INTERNAL_ERROR': 'Something went wrong. Please try again later.'
};

function getDisplayMessage(error: ErrorResponse): string {
  return errorMessages[error.error.code] || error.error.message;
}
```

---

## Logging Errors

```python
# middleware/logging.py
import logging
import time
from fastapi import Request

logger = logging.getLogger("chat_api")


async def log_request_middleware(request: Request, call_next):
    """Log all requests with timing and error details."""
    start_time = time.time()
    request_id = request.headers.get("X-Request-ID", str(uuid4()))

    # Add request_id to context
    logger.info(f"[{request_id}] → {request.method} {request.url.path}")

    response = await call_next(request)

    duration = time.time() - start_time

    # Log based on status
    if response.status_code >= 500:
        logger.error(
            f"[{request_id}] ← {response.status_code} ({duration:.2f}s)"
        )
    elif response.status_code >= 400:
        logger.warning(
            f"[{request_id}] ← {response.status_code} ({duration:.2f}s)"
        )
    else:
        logger.info(
            f"[{request_id}] ← {response.status_code} ({duration:.2f}s)"
        )

    # Add request_id to response headers
    response.headers["X-Request-ID"] = request_id

    return response
```

---

## Error Recovery Patterns

### Conversation State Recovery

If agent fails after user message was persisted:

```python
async def execute_agent_with_recovery(
    session: Session,
    agent: AgentRunner,
    conversation_id: str,
    user_id: str,
    message: str,
    model: str
) -> ChatResponse:
    """Execute agent with rollback on failure."""

    # Check for incomplete message pair (user message without response)
    messages = get_messages(session, conversation_id, user_id)
    if messages and messages[-1].role == "user":
        # Previous request failed after persisting user message
        # Don't add duplicate user message
        last_user_message = messages[-1].content
        if last_user_message == message:
            # Retry the same message - use existing
            pass
        else:
            # New message - add it
            add_message(session, conversation_id, user_id, "user", message)
    else:
        # Normal case - add user message
        add_message(session, conversation_id, user_id, "user", message)

    # Build context and call agent
    # ...
```

### Graceful Degradation

```python
async def chat_with_fallback(
    session: Session,
    primary_agent: AgentRunner,
    fallback_agent: AgentRunner,
    ...
) -> ChatResponse:
    """Try primary agent, fall back to secondary."""

    try:
        return await execute_agent(session, primary_agent, ...)
    except AgentError:
        logger.warning("Primary agent failed, trying fallback")
        try:
            return await execute_agent(session, fallback_agent, ...)
        except AgentError:
            raise AgentError("All agents unavailable")
```
