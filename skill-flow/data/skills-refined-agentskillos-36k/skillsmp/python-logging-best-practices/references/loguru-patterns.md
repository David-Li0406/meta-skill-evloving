# Loguru Configuration Patterns

## Basic Setup

```python
from loguru import logger
import sys

# Remove default handler
logger.remove()

# Add custom handlers
logger.add(sys.stderr, level="INFO")
logger.add("app.log", rotation="10 MB")
```

## JSONL Output Pattern

```python
import json

def json_formatter(record) -> str:
    """JSONL formatter - one JSON per line."""
    return json.dumps({
        "timestamp": record["time"].strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "level": record["level"].name.lower(),
        "message": record["message"],
        "extra": record["extra"]
    })

logger.add(sys.stderr, format=json_formatter)
```

## Structured Logging

```python
# Add context to log messages
logger.info(
    "User logged in",
    operation="login",
    status="success",
    user_id=123,
    metrics={"duration_ms": 50}
)
```

## Rotation Options

```python
# Size-based rotation
logger.add("app.log", rotation="10 MB")

# Time-based rotation
logger.add("app.log", rotation="1 day")
logger.add("app.log", rotation="1 week")
logger.add("app.log", rotation="00:00")  # Midnight

# Count-based rotation
logger.add("app.log", rotation="100 records")
```

## Retention Options

```python
# Time-based retention
logger.add("app.log", retention="7 days")
logger.add("app.log", retention="1 month")

# Count-based retention
logger.add("app.log", retention=5)  # Keep 5 old files
```

## Compression

```python
# gzip compression (recommended)
logger.add("app.log", compression="gz")

# Other formats
logger.add("app.log", compression="bz2")
logger.add("app.log", compression="xz")
logger.add("app.log", compression="zip")
```

## Exception Handling

```python
# Log exceptions with traceback
try:
    raise ValueError("Something went wrong")
except ValueError:
    logger.exception("Error occurred")

# Or use opt() for more control
logger.opt(exception=True).error("Error with traceback")
```

## Async Support

```python
# For async applications - use enqueue
logger.add("app.log", enqueue=True)

# Note: For simple startup scripts, enqueue=False (default) is fine
```

## Filtering

```python
# Filter by level
logger.add("errors.log", level="ERROR")

# Filter by function
def my_filter(record):
    return "sensitive" not in record["message"]

logger.add("filtered.log", filter=my_filter)
```

## Best Practices

1. **Always `logger.remove()`** first - Removes default handler
2. **Use rotation** - Prevent unbounded growth
3. **Use retention** - Clean up old logs
4. **Use compression** - Save disk space
5. **Use structured extras** - Add context via kwargs
