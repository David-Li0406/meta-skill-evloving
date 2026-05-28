---
name: fastapi-logging
description: Use this skill when you need to configure structured JSON logging with correlation IDs and request context for a FastAPI application.
---

# FastAPI Logging & Correlation IDs

## Overview

This skill covers setting up structured JSON logging with correlation ID middleware for request tracing across the application.

## Create logging.py

Create `src/app/logging.py`:

```python
import logging
import sys
from typing import Any
from pythonjsonlogger import jsonlogger
from app.config import settings
from app.middleware.correlation_id import get_correlation_id

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter that adds standard fields to all log records.

    Output format:
    {
        "timestamp": "2025-01-05T12:00:00.000Z",
        "level": "INFO",
        "message": "Request completed",
        "logger": "app.api.v1.items",
        "correlation_id": "uuid",
        ...additional fields
    }
    """

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)

        # Standard fields
        log_record["timestamp"] = self.formatTime(record, self.datefmt)
        log_record["level"] = record.levelname
        log_record["logger"] = record.name

        # Remove default fields we're replacing
        log_record.pop("levelname", None)
        log_record.pop("name", None)

        # Add correlation_id from context if available
        correlation_id = get_correlation_id()
        if correlation_id:
            log_record["correlation_id"] = correlation_id

def setup_logging() -> None:
    """
    Configure application logging.

    Call this early in application startup, before creating the FastAPI app.

    Configures:
    - JSON format for production (LOG_JSON_FORMAT=true)
    - Human-readable format for development
    - Log level from settings
    - Suppresses noisy third-party loggers
    """
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    if settings.log_json_format:
        # JSON format for production
        formatter = CustomJsonFormatter()
        handler.setFormatter(formatter)

    root_logger.addHandler(handler)
```