# Python Logging Examples

This document provides practical examples for various logging scenarios.

## Web Application Logging

### Flask application with structlog

```python
from flask import Flask, request
import structlog
import uuid

app = Flask(__name__)

# Configure structlog
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

log = structlog.get_logger()

@app.before_request
def add_request_id():
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)

@app.route("/")
def home():
    log.info("Home page accessed", user_agent=request.headers.get("User-Agent"))
    return "Hello, World!"

@app.route("/error")
def error():
    try:
        raise ValueError("Something went wrong")
    except Exception:
        log.exception("Error occurred in /error endpoint")
        return "Internal Server Error", 500
```

### FastAPI application with context

```python
from fastapi import FastAPI, Request
import structlog
import uuid

app = FastAPI()

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path
    )

    response = await call_next(request)
    return response

@app.get("/")
async def root():
    log = structlog.get_logger()
    log.info("Root endpoint accessed")
    return {"message": "Hello World"}
```

## Database Operation Logging

```python
import structlog
import time
from contextlib import contextmanager

log = structlog.get_logger()

@contextmanager
def log_database_operation(operation: str, table: str):
    start_time = time.time()
    log.info("Database operation started", operation=operation, table=table)

    try:
        yield
        duration = time.time() - start_time
        log.info("Database operation completed",
                operation=operation,
                table=table,
                duration=duration)
    except Exception as e:
        duration = time.time() - start_time
        log.error("Database operation failed",
                 operation=operation,
                 table=table,
                 duration=duration,
                 error=str(e))
        raise

# Usage example
def create_user(user_data):
    with log_database_operation("CREATE", "users"):
        # Database operation here
        time.sleep(0.1)  # Simulate database work
        pass
```

## Background Task Logging

```python
import structlog
import asyncio
from datetime import datetime

log = structlog.get_logger()

async def process_data_batch(batch_id: int, data: list):
    log.info("Starting batch processing", batch_id=batch_id, items_count=len(data))

    success_count = 0
    error_count = 0

    for i, item in enumerate(data):
        try:
            # Process item
            await process_single_item(item)
            success_count += 1

            if i % 100 == 0:
                log.info("Batch processing progress",
                        batch_id=batch_id,
                        processed=i+1,
                        total=len(data))

        except Exception as e:
            error_count += 1
            log.error("Item processing failed",
                     batch_id=batch_id,
                     item_index=i,
                     error=str(e))

    log.info("Batch processing completed",
            batch_id=batch_id,
            success_count=success_count,
            error_count=error_count)

async def process_single_item(item):
    # Simulate processing
    await asyncio.sleep(0.01)
    if item % 10 == 0:  # Simulate occasional errors
        raise ValueError("Random processing error")
```

## Error Analysis and Alerting

```python
import structlog
from collections import defaultdict
import time

log = structlog.get_logger()

class ErrorTracker:
    def __init__(self):
        self.error_counts = defaultdict(int)
        self.last_alert_time = {}

    def track_error(self, error_type: str, error_message: str):
        self.error_counts[error_type] += 1

        # Log the error
        log.error("Error tracked",
                 error_type=error_type,
                 error_message=error_message,
                 count=self.error_counts[error_type])

        # Alert if threshold exceeded
        if self.error_counts[error_type] >= 5:
            current_time = time.time()
            last_alert = self.last_alert_time.get(error_type, 0)

            if current_time - last_alert > 300:  # 5 minutes
                log.critical("High error rate detected",
                           error_type=error_type,
                           count=self.error_counts[error_type])
                self.last_alert_time[error_type] = current_time

# Usage
error_tracker = ErrorTracker()

def risky_operation():
    try:
        # Some operation that might fail
        raise ValueError("Connection timeout")
    except Exception as e:
        error_type = type(e).__name__
        error_tracker.track_error(error_type, str(e))
        raise
```

## Performance Monitoring

```python
import structlog
import time
from functools import wraps

log = structlog.get_logger()

def log_performance(operation_name: str):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                log.info("Performance metric",
                        operation=operation_name,
                        duration=duration,
                        success=True)
                return result
            except Exception as e:
                duration = time.time() - start_time
                log.error("Performance metric",
                         operation=operation_name,
                         duration=duration,
                         success=False,
                         error=str(e))
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                log.info("Performance metric",
                        operation=operation_name,
                        duration=duration,
                        success=True)
                return result
            except Exception as e:
                duration = time.time() - start_time
                log.error("Performance metric",
                         operation=operation_name,
                         duration=duration,
                         success=False,
                         error=str(e))
                raise

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Usage
@log_performance("database_query")
def fetch_user_data(user_id: int):
    time.sleep(0.1)  # Simulate database query
    return {"id": user_id, "name": "John Doe"}
```