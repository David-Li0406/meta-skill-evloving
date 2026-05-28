---
id: logging-patterns
name: "Logging Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Logging Patterns

## Overview

Logging provides visibility into application behavior for debugging, monitoring, and auditing. Effective logging balances information capture with performance and storage considerations, using structured formats for machine processing.

## When to Use

- Production monitoring and alerting
- Debugging issues in deployed applications
- Audit trails for compliance
- Performance analysis
- Security incident investigation

## Key Principles

- **Structured logging**: Use JSON for machine parsing
- **Appropriate levels**: Debug, info, warning, error, critical
- **Meaningful context**: Include relevant data without sensitive info
- **Performance awareness**: Don't log excessively in hot paths
- **Correlation**: Track requests across services

## Best Practices

### Logging Configuration

```python
# Python logging configuration

import logging
import logging.config
import json
from datetime import datetime
from typing import Any

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(timestamp)s %(level)s %(name)s %(message)s"
        },
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json" if ENVIRONMENT == "production" else "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "/var/log/app/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["console", "file"],
            "level": "INFO"
        },
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        },
        "sqlalchemy.engine": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### Structured Logging with structlog

```python
import structlog
from contextvars import ContextVar
from typing import Optional
import uuid

# Context variables for request tracking
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar("user_id", default=None)

def add_context(logger, method_name, event_dict):
    """Add request context to all log entries."""
    event_dict["request_id"] = request_id_var.get()
    event_dict["user_id"] = user_id_var.get()
    return event_dict

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        add_context,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage
logger.info(
    "Order processed",
    order_id="ord-123",
    total=99.99,
    items_count=3
)
# Output:
# {"timestamp": "2024-01-15T10:30:00Z", "level": "info", "event": "Order processed",
#  "order_id": "ord-123", "total": 99.99, "items_count": 3,
#  "request_id": "req-abc", "user_id": "user-xyz"}
```

### Log Levels Guide

```python
import logging

logger = logging.getLogger(__name__)

# DEBUG: Detailed information for diagnosing problems
# Use for: Development, troubleshooting specific issues
logger.debug(
    "Processing item",
    extra={"item_id": item.id, "step": "validation", "data": item.to_dict()}
)

# INFO: Confirmation that things are working as expected
# Use for: Request handling, business events, state changes
logger.info(
    "User registered",
    extra={"user_id": user.id, "email_domain": user.email.split("@")[1]}
)

# WARNING: Something unexpected but not necessarily wrong
# Use for: Deprecated API usage, recoverable errors, approaching limits
logger.warning(
    "Rate limit approaching",
    extra={"user_id": user.id, "current": 95, "limit": 100}
)

# ERROR: An error occurred that should be investigated
# Use for: Exceptions, failed operations, integration failures
logger.error(
    "Payment processing failed",
    extra={"order_id": order.id, "error_code": e.code},
    exc_info=True
)

# CRITICAL: Application cannot continue
# Use for: System failures, data corruption, security breaches
logger.critical(
    "Database connection lost",
    extra={"host": db_host, "last_error": str(e)},
    exc_info=True
)
```

### Request Logging Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import structlog
import time
import uuid

logger = structlog.get_logger()

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_var.set(request_id)

        # Extract user ID from auth (if available)
        user_id = getattr(request.state, "user_id", None)
        user_id_var.set(user_id)

        # Log request start
        start_time = time.perf_counter()
        logger.info(
            "Request started",
            method=request.method,
            path=request.url.path,
            query=str(request.query_params),
            client_ip=request.client.host,
            user_agent=request.headers.get("User-Agent"),
        )

        try:
            response = await call_next(request)

            # Log request completion
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.info(
                "Request completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                "Request failed",
                method=request.method,
                path=request.url.path,
                duration_ms=round(duration_ms, 2),
                error=str(e),
                exc_info=True,
            )
            raise

app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)
```

### Business Event Logging

```python
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime
import structlog

logger = structlog.get_logger()

class EventType(Enum):
    # User events
    USER_REGISTERED = "user.registered"
    USER_LOGGED_IN = "user.logged_in"
    USER_LOGGED_OUT = "user.logged_out"
    USER_PASSWORD_CHANGED = "user.password_changed"

    # Order events
    ORDER_CREATED = "order.created"
    ORDER_PAID = "order.paid"
    ORDER_SHIPPED = "order.shipped"
    ORDER_DELIVERED = "order.delivered"
    ORDER_CANCELLED = "order.cancelled"

    # Payment events
    PAYMENT_INITIATED = "payment.initiated"
    PAYMENT_COMPLETED = "payment.completed"
    PAYMENT_FAILED = "payment.failed"
    PAYMENT_REFUNDED = "payment.refunded"


@dataclass
class BusinessEvent:
    event_type: EventType
    entity_type: str
    entity_id: str
    data: dict
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


def log_business_event(event: BusinessEvent):
    """Log a business event for audit and analytics."""
    logger.info(
        event.event_type.value,
        entity_type=event.entity_type,
        entity_id=event.entity_id,
        timestamp=event.timestamp.isoformat(),
        **event.data
    )


# Usage
def complete_order(order: Order):
    # Business logic
    order.status = "completed"
    save(order)

    # Log business event
    log_business_event(BusinessEvent(
        event_type=EventType.ORDER_PAID,
        entity_type="order",
        entity_id=order.id,
        data={
            "customer_id": order.customer_id,
            "total": float(order.total),
            "items_count": len(order.items),
            "payment_method": order.payment_method,
        }
    ))
```

### Sensitive Data Handling

```python
import re
from typing import Any
import structlog

# Patterns to mask
SENSITIVE_PATTERNS = [
    (r'\b\d{16}\b', '****-****-****-****'),  # Credit card
    (r'\b\d{3}-\d{2}-\d{4}\b', '***-**-****'),  # SSN
    (r'password["\s:=]+["\']?([^"\'\s]+)', 'password: [REDACTED]'),
    (r'api[_-]?key["\s:=]+["\']?([^"\'\s]+)', 'api_key: [REDACTED]'),
]

SENSITIVE_FIELDS = {'password', 'secret', 'token', 'api_key', 'ssn', 'credit_card'}


def mask_sensitive_string(value: str) -> str:
    """Mask sensitive patterns in strings."""
    for pattern, replacement in SENSITIVE_PATTERNS:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    return value


def mask_sensitive_dict(data: dict) -> dict:
    """Recursively mask sensitive fields in dictionaries."""
    masked = {}
    for key, value in data.items():
        if key.lower() in SENSITIVE_FIELDS:
            masked[key] = "[REDACTED]"
        elif isinstance(value, dict):
            masked[key] = mask_sensitive_dict(value)
        elif isinstance(value, str):
            masked[key] = mask_sensitive_string(value)
        elif isinstance(value, list):
            masked[key] = [
                mask_sensitive_dict(item) if isinstance(item, dict)
                else mask_sensitive_string(item) if isinstance(item, str)
                else item
                for item in value
            ]
        else:
            masked[key] = value
    return masked


def sensitive_data_processor(logger, method_name, event_dict):
    """structlog processor to mask sensitive data."""
    return mask_sensitive_dict(event_dict)


# Add to structlog configuration
structlog.configure(
    processors=[
        # ... other processors
        sensitive_data_processor,
        structlog.processors.JSONRenderer()
    ]
)
```

### Performance Logging

```python
import time
from contextlib import contextmanager
from functools import wraps
import structlog

logger = structlog.get_logger()


@contextmanager
def log_timing(operation: str, **context):
    """Context manager to log operation timing."""
    start = time.perf_counter()
    try:
        yield
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            f"{operation} completed",
            duration_ms=round(duration_ms, 2),
            **context
        )


def log_slow_operations(threshold_ms: float = 100):
    """Decorator to log slow operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration_ms = (time.perf_counter() - start) * 1000

            if duration_ms > threshold_ms:
                logger.warning(
                    "Slow operation detected",
                    function=func.__name__,
                    duration_ms=round(duration_ms, 2),
                    threshold_ms=threshold_ms
                )

            return result
        return wrapper
    return decorator


# Usage
@log_slow_operations(threshold_ms=50)
def process_data(data: list) -> list:
    return [transform(item) for item in data]


with log_timing("database_query", table="users", query_type="select"):
    users = db.query(User).filter(User.active == True).all()
```

### Distributed Tracing Integration

```python
from opentelemetry import trace
from opentelemetry.trace import SpanKind
import structlog

logger = structlog.get_logger()
tracer = trace.get_tracer(__name__)


def add_trace_context(logger, method_name, event_dict):
    """Add OpenTelemetry trace context to logs."""
    span = trace.get_current_span()
    if span.is_recording():
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict


# Add to structlog processors
structlog.configure(
    processors=[
        add_trace_context,
        # ... other processors
    ]
)


# Usage with tracing
async def process_order(order_id: str):
    with tracer.start_as_current_span(
        "process_order",
        kind=SpanKind.INTERNAL,
        attributes={"order_id": order_id}
    ) as span:
        logger.info("Processing order", order_id=order_id)

        # Nested span for specific operation
        with tracer.start_as_current_span("validate_inventory"):
            await validate_inventory(order_id)
            logger.info("Inventory validated", order_id=order_id)

        with tracer.start_as_current_span("charge_payment"):
            await charge_payment(order_id)
            logger.info("Payment charged", order_id=order_id)
```

### TypeScript Logging

```typescript
import pino from 'pino';

// Configure Pino logger
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  redact: {
    paths: ['password', 'token', 'authorization', '*.password', '*.token'],
    censor: '[REDACTED]',
  },
});

// Create child logger with context
const requestLogger = logger.child({
  service: 'api',
  version: process.env.APP_VERSION,
});

// Express middleware
const loggerMiddleware = (req, res, next) => {
  const requestId = req.headers['x-request-id'] || crypto.randomUUID();
  req.log = requestLogger.child({ requestId });

  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    req.log.info({
      method: req.method,
      url: req.url,
      statusCode: res.statusCode,
      duration,
    }, 'Request completed');
  });

  next();
};

// Usage
app.get('/users/:id', async (req, res) => {
  req.log.info({ userId: req.params.id }, 'Fetching user');

  try {
    const user = await getUser(req.params.id);
    res.json(user);
  } catch (error) {
    req.log.error({ error, userId: req.params.id }, 'Failed to fetch user');
    throw error;
  }
});
```

## Anti-patterns

- **Logging sensitive data**: Passwords, tokens, PII
- **Excessive logging**: Logging in hot loops
- **Inconsistent format**: Mixed structured and unstructured logs
- **Missing context**: Logs without request/user context
- **String concatenation**: Building log messages inefficiently
- **Log and throw**: Logging error then re-throwing (duplicate logs)
- **Ignoring log levels**: Using INFO for everything

## References

- [structlog Documentation](https://www.structlog.org/)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [12 Factor App - Logs](https://12factor.net/logs)
- [Pino Logger](https://getpino.io/)
- [OpenTelemetry Logging](https://opentelemetry.io/docs/specs/otel/logs/)
