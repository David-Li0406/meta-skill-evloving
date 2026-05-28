# Logging Patterns with structlog

Enterprise-grade logging using structlog with JSON and colored console output.

## Overview

All logs include:
- **Structured data**: Key-value pairs, not just strings
- **Conversation ID**: Track requests across services
- **Timestamps**: ISO format with timezone
- **Log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Context**: Logger name, function, line number

## Configuration

### core/logging.py

```python
import logging
import sys
import structlog
from structlog.types import EventDict
from core.config import settings
from middleware.conversation import get_conversation_id

def add_conversation_id(logger, method_name, event_dict: EventDict) -> EventDict:
    """Add conversation_id to all log entries."""
    conversation_id = get_conversation_id()
    if conversation_id:
        event_dict["conversation_id"] = conversation_id
    return event_dict

def configure_logging() -> None:
    """Configure structlog based on environment."""
    
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        add_conversation_id,  # ← Add conversation ID
    ]
    
    if settings.LOG_JSON:
        # Production: JSON logs
        structlog.configure(
            processors=shared_processors + [
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # Development: Colored console
        structlog.configure(
            processors=shared_processors + [
                structlog.processors.format_exc_info,
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
    
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )

def get_logger(name: str):
    """Get configured logger."""
    if not structlog.is_configured():
        configure_logging()
    return structlog.get_logger(name)
```

## Usage in Code

### Basic Logging

```python
from core.logging import get_logger

logger = get_logger(__name__)

# Simple message
logger.info("User logged in")

# With structured data
logger.info("User logged in", user_id=123, email="user@example.com")

# Different levels
logger.debug("Debug info", data={"key": "value"})
logger.warning("Warning message", reason="Invalid token")
logger.error("Error occurred", error=str(e), traceback=True)
```

### Output Examples

**Development (Colored Console)**:
```
2024-01-22 14:30:45 [info     ] User logged in        conversation_id=abc-123 user_id=123 email=user@example.com
2024-01-22 14:30:46 [warning  ] Warning message       conversation_id=abc-123 reason=Invalid token
```

**Production (JSON)**:
```json
{"event": "User logged in", "level": "info", "timestamp": "2024-01-22T14:30:45.123Z", "conversation_id": "abc-123", "user_id": 123, "email": "user@example.com", "logger": "api.routes.auth"}
{"event": "Warning message", "level": "warning", "timestamp": "2024-01-22T14:30:46.456Z", "conversation_id": "abc-123", "reason": "Invalid token", "logger": "api.routes.auth"}
```

## Request/Response Logging Middleware

Log all API requests and responses automatically.

### middleware/request_logging.py

```python
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from core.logging import get_logger

logger = get_logger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(
            "HTTP request",
            method=request.method,
            path=request.url.path,
            query=str(request.url.query),
            client=request.client.host if request.client else None,
        )
        
        # Process request
        response: Response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            "HTTP response",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2),
        )
        
        return response
```

### Register in app.py

```python
from middleware.request_logging import RequestLoggingMiddleware

app.add_middleware(RequestLoggingMiddleware)
```

## Service Layer Logging

### Log Business Operations

```python
# services/user/profile.py
from core.logging import get_logger

logger = get_logger(__name__)

class UserProfileService:
    async def create(self, db, data):
        logger.info("Creating user profile", email=data.email)
        
        try:
            # Business logic
            user = User(**data.model_dump())
            db.add(user)
            await db.commit()
            
            logger.info("User profile created", user_id=user.id, email=user.email)
            return user
            
        except Exception as e:
            logger.error(
                "Failed to create user profile",
                email=data.email,
                error=str(e),
                exc_info=True,  # Include traceback
            )
            raise
```

## Database Query Logging

### Option 1: SQLAlchemy Echo (Development)

```python
# core/config.py
DB_ECHO: bool = True  # Logs all SQL queries
```

```python
# core/db.py
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,  # Logs SQL
)
```

### Option 2: Manual Query Logging

```python
from sqlalchemy import select
from core.logging import get_logger

logger = get_logger(__name__)

async def get_user_by_email(db, email: str):
    logger.debug("Querying user by email", email=email)
    
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    logger.debug(
        "User query result",
        email=email,
        found=user is not None,
        user_id=user.id if user else None,
    )
    
    return user
```

## External API Call Logging

Automatically logged in `core/httpx.py`:

```python
logger.info(
    "External API request",
    method=method,
    url=url,
    conversation_id=get_conversation_id(),  # Propagate conversation ID
)

response = await client.request(method, url, **kwargs)

logger.info(
    "External API response",
    method=method,
    url=url,
    status_code=response.status_code,
    duration_ms=...,
)
```

## Error Logging Best Practices

### 1. Include Context

```python
logger.error(
    "Database connection failed",
    database_url=settings.DATABASE_URL,
    error=str(e),
    exc_info=True,  # Include full traceback
)
```

### 2. Use Appropriate Levels

- **DEBUG**: Detailed diagnostic info (disabled in production)
- **INFO**: Normal operations (user login, API calls)
- **WARNING**: Unusual but recoverable (rate limit reached)
- **ERROR**: Operation failed (database error)
- **CRITICAL**: System failure (service down)

### 3. Don't Log Sensitive Data

```python
# ❌ Bad
logger.info("User login", password=password, api_key=api_key)

# ✅ Good
logger.info("User login", email=email, user_id=user_id)
```

## Log Aggregation

### JSON Logs for ELK/Splunk

Set in production:
```bash
LOG_JSON=true
```

All logs will be JSON, easily parseable by log aggregators:

```json
{
  "event": "User profile created",
  "timestamp": "2024-01-22T14:30:45.123Z",
  "level": "info",
  "conversation_id": "abc-123",
  "user_id": 456,
  "email": "user@example.com",
  "logger": "services.user.profile",
  "func": "create",
  "lineno": 25
}
```

Query by `conversation_id` to trace entire request flow.

## Conversation ID Tracking

Conversation ID is automatically:
1. Generated or extracted in `ConversationMiddleware`
2. Stored in context vars
3. Added to all logs via `add_conversation_id` processor
4. Propagated to external API calls

This enables end-to-end request tracing across services.

## Performance Considerations

- **Async logging**: structlog is synchronous but fast
- **Sampling**: In high-traffic scenarios, sample DEBUG logs
- **Buffering**: Consider async log handlers for production

## Testing

Test logs in tests:

```python
import pytest
from core.logging import get_logger

def test_logging(caplog):
    logger = get_logger(__name__)
    
    logger.info("Test message", data="value")
    
    assert "Test message" in caplog.text
    assert "data" in caplog.text
```

## Next Steps

- [Observability Patterns](observability-patterns.md) - Metrics & tracing
- [Error Handling Workflow](error-handling-workflow.md) - Systematic debugging
- [Configuration Patterns](configuration-patterns.md) - Log level management
