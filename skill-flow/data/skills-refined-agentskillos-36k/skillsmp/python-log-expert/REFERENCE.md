# Python Logging Reference

This document provides comprehensive reference information for Python logging libraries and best practices.

## Structlog Configuration

### Core Components

#### Processors

Processors transform log entries before they're output. Common processors include:

```python
import structlog

processors = [
    # Filter messages based on log level
    structlog.stdlib.filter_by_level,

    # Add standard library context
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,

    # Format positional arguments
    structlog.stdlib.PositionalArgumentsFormatter(),

    # Add timestamps
    structlog.processors.TimeStamper(fmt="iso"),

    # Add stack information for debugging
    structlog.processors.StackInfoRenderer(),

    # Format exception information
    structlog.processors.format_exc_info,

    # Handle Unicode decoding
    structlog.processors.UnicodeDecoder(),

    # Final output formatting
    structlog.processors.JSONRenderer(),  # or structlog.dev.ConsoleRenderer()
]
```

#### Formatters

**JSON Renderer** (Production):
```python
structlog.processors.JSONRenderer()
```

**Console Renderer** (Development):
```python
structlog.dev.ConsoleRenderer(colors=True)
```

**Custom Formatter**:
```python
def custom_formatter(logger, method_name: str, event_dict: dict) -> str:
    return f"{event_dict['timestamp']} - {event_dict['level']} - {event_dict['event']}"
```

### Context Management

#### Global Context
```python
import structlog

# Bind global context
structlog.contextvars.bind_contextvars(
    service="my-app",
    version="1.0.0",
    environment="production"
)

# Clear global context
structlog.contextvars.clear_contextvars()
```

#### Local Context
```python
import structlog

log = structlog.get_logger()

# Bind context to logger
log = log.bind(user_id=123, request_id="abc-def")

# Or use context manager
with log.bind(user_id=123):
    log.info("User action performed")
```

## Standard Library Logging Integration

### Basic Configuration

```python
import logging
import sys

# Standard logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)
```

### Handler Configuration

**File Handler with Rotation**:
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=10485760,  # 10MB
    backupCount=5
)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(handler)
```

**Syslog Handler**:
```python
import logging.handlers

syslog_handler = logging.handlers.SysLogHandler(address="/dev/log")
syslog_handler.setFormatter(logging.Formatter("%(name)s[%(process)d]: %(levelname)s - %(message)s"))
logging.getLogger().addHandler(syslog_handler)
```

## Log Levels

### Standard Log Levels
- `DEBUG` (10): Detailed information, typically of interest only when diagnosing problems
- `INFO` (20): Confirmation that things are working as expected
- `WARNING` (30): An indication that something unexpected happened
- `ERROR` (40): Due to a more serious problem, the software has not been able to perform some function
- `CRITICAL` (50): A serious error, indicating that the program itself may be unable to continue running

### Log Level Best Practices
```python
# Use appropriate levels
log.debug("Detailed debugging information")  # Development only
log.info("Normal application flow")  # Production
log.warning("Something unexpected but recoverable")  # Production
log.error("Error occurred but application continues")  # Production
log.critical("Critical error, application may fail")  # Production
```

## Performance Considerations

### Lazy Evaluation
```python
# Bad: String formatting happens even if log level filters it out
log.info(f"User {user_id} performed action {action}")

# Good: Lazy evaluation
log.info("User performed action", user_id=user_id, action=action)
```

### Async Logging
```python
import structlog
import asyncio

async def async_log_example():
    log = structlog.get_logger()

    # Use async-compatible logging
    await asyncio.to_thread(log.info, "Async operation completed")
```

### Caching
```python
# Enable logger caching for better performance
structlog.configure(
    cache_logger_on_first_use=True,
    # ... other configuration
)
```

## Exception Handling

### Exception Logging
```python
import structlog

log = structlog.get_logger()

try:
    risky_operation()
except Exception:
    # Log with full traceback
    log.exception("Operation failed")

    # Or log with custom context
    log.error("Operation failed", exc_info=True)
```

### Exception Formatting
```python
import structlog.processors

# Configure exception formatting
structlog.configure(
    processors=[
        # ... other processors
        structlog.processors.format_exc_info,  # Include full traceback
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ]
)
```

## Structured Logging Patterns

### Event Schema
```python
# Consistent event structure
log.info("user_action",
         user_id=123,
         action="login",
         ip_address="192.168.1.1",
         user_agent="Mozilla/5.0...",
         success=True)

log.error("api_error",
          endpoint="/api/v1/users",
          method="POST",
          status_code=500,
          error_message="Database connection failed",
          request_id="req-123")
```

### Correlation IDs
```python
import uuid

# Generate and track correlation IDs
correlation_id = str(uuid.uuid4())
structlog.contextvars.bind_contextvars(correlation_id=correlation_id)

log.info("Request started", correlation_id=correlation_id)
```

## Environment-Specific Configuration

### Development
```python
import structlog

structlog.configure(
    processors=[
        structlog.dev.ConsoleRenderer(colors=True)
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
)
```

### Production
```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

## Testing Logging

### Log Capture for Testing
```python
import structlog
from io import StringIO

def test_logging():
    # Capture log output
    log_stream = StringIO()

    # Configure test logging
    structlog.configure(
        processors=[
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.WriteLoggerFactory(log_stream),
    )

    log = structlog.get_logger()
    log.info("Test message", test_data="value")

    # Assert log content
    log_output = log_stream.getvalue()
    assert "Test message" in log_output
    assert "test_data" in log_output
```

### Log Level Testing
```python
import logging

def test_log_levels():
    # Set high log level for test
    logging.basicConfig(level=logging.WARNING)

    log = structlog.get_logger()

    # This should not appear in output
    log.info("This should be filtered out")

    # This should appear
    log.warning("This should be visible")
```