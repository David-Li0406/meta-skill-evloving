---
name: fastapi-exceptions
description: Use this skill when you need to create custom exceptions, error response schemas, and centralized exception handlers for FastAPI applications.
---

# FastAPI Exceptions & Error Handling

## Overview

This skill covers creating a comprehensive exception handling system with custom exceptions, standardized error responses, and centralized exception handlers.

## Create exceptions.py

Create `src/app/exceptions.py`:

```python
from typing import Any
from uuid import UUID


class AppException(Exception):
    """
    Base exception for all application errors.

    All custom exceptions should inherit from this class.
    Provides consistent error structure across the application.

    Attributes:
        message: Human-readable error description
        error_code: Machine-readable error code (e.g., "NOT_FOUND")
        status_code: HTTP status code
        details: Additional error context
    """

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppException):
    """
    Raised when a requested resource is not found.

    HTTP Status: 404
    """

    def __init__(
        self,
        resource: str,
        id: UUID | str | None = None,
        field: str | None = None,
        value: Any = None,
    ):
        if id is not None:
            message = f"{resource} with id '{id}' not found"
            details = {"resource": resource, "id": str(id)}
        elif field is not None:
            message = f"{resource} with {field}='{value}' not found"
            details = {"resource": resource, "field": field, "value": str(value)}
        else:
            message = f"{resource} not found"
            details = {"resource": resource}

        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=404,
            details=details,
        )


class ConflictError(AppException):
    """
    Raised when an operation conflicts with existing data.

    Examples:
    - Duplicate unique constraint violation
    - Resource already exists
    - Concurrent modification conflict

    HTTP Status: 409
    """

    def __init__(
        self,
        resource: str,
        field: str,
        value: Any,
    ):
        message = f"{resource} with {field}='{value}' already exists"
        details = {"resource": resource, "field": field, "value": str(value)}
        super().__init__(
            message=message,
            error_code="CONFLICT",
            status_code=409,
            details=details,
        )
```