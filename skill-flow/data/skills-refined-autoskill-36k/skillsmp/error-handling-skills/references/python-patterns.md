# Python Error Handling Patterns

## Table of Contents

1. [Exception Basics](#exception-basics)
2. [Custom Exception Classes](#custom-exception-classes)
3. [Context Managers](#context-managers)
4. [Decorators for Error Handling](#decorators-for-error-handling)
5. [Exception Chaining](#exception-chaining)
6. [FastAPI Error Handling](#fastapi-error-handling)
7. [Django Error Handling](#django-error-handling)
8. [Async Exception Handling](#async-exception-handling)

## Exception Basics

### Try-Except-Finally

```python
def read_file(path: str) -> str:
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise
    except PermissionError:
        logger.error(f"Permission denied: {path}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error reading file: {path}", exc_info=True)
        raise
    finally:
        logger.debug(f"Finished reading file: {path}")
```

### Try-Except-Else

```python
def divide(a: int, b: int) -> float:
    try:
        result = a / b
    except ZeroDivisionError:
        logger.error("Division by zero")
        raise ValueError("Cannot divide by zero")
    else:
        # Executes only if no exception occurred
        logger.info(f"Division successful: {a} / {b} = {result}")
        return result
```

### Multiple Exception Handling

```python
def process_data(data: dict) -> None:
    try:
        validate(data)
        save_to_db(data)
    except (ValueError, TypeError) as e:
        # Handle multiple exception types the same way
        logger.error(f"Validation error: {e}")
        raise ValidationError(str(e)) from e
    except DatabaseError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        raise
```

## Custom Exception Classes

### Basic Custom Exception

```python
class ApplicationError(Exception):
    """Base exception for application errors"""

    def __init__(self, message: str, code: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code

    def to_dict(self) -> dict:
        return {
            'message': self.message,
            'code': self.code,
            'status_code': self.status_code
        }
```

### Exception Hierarchy

```python
from typing import Dict, Optional, Any

class ApplicationError(Exception):
    """Base exception for all application errors"""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 500,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.context = context or {}

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"

    def to_dict(self) -> dict:
        return {
            'message': self.message,
            'code': self.code,
            'context': self.context
        }


class ValidationError(ApplicationError):
    """Validation failed"""

    def __init__(self, message: str, fields: Dict[str, str]):
        super().__init__(
            message=message,
            code='VALIDATION_ERROR',
            status_code=400,
            context={'fields': fields}
        )
        self.fields = fields


class NotFoundError(ApplicationError):
    """Resource not found"""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            code='NOT_FOUND',
            status_code=404,
            context={'resource': resource, 'identifier': identifier}
        )


class AuthenticationError(ApplicationError):
    """Authentication failed"""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            code='AUTHENTICATION_ERROR',
            status_code=401
        )


class AuthorizationError(ApplicationError):
    """Authorization failed"""

    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            code='AUTHORIZATION_ERROR',
            status_code=403
        )


class DatabaseError(ApplicationError):
    """Database operation failed"""

    def __init__(self, operation: str, original_error: Exception):
        super().__init__(
            message=f"Database operation failed: {operation}",
            code='DATABASE_ERROR',
            status_code=503,
            context={'operation': operation}
        )
        self.original_error = original_error


class ExternalServiceError(ApplicationError):
    """External service call failed"""

    def __init__(self, service: str, message: str):
        super().__init__(
            message=f"{service} error: {message}",
            code='EXTERNAL_SERVICE_ERROR',
            status_code=503,
            context={'service': service}
        )


# Usage examples
raise ValidationError('Invalid input', {
    'email': 'Invalid email format',
    'age': 'Must be at least 18'
})

raise NotFoundError('User', user_id)

raise AuthenticationError('Invalid credentials')
```

## Context Managers

### Basic Context Manager

```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def database_transaction(db) -> Generator:
    """Context manager for database transactions"""
    try:
        yield db
        db.commit()
        logger.info("Transaction committed")
    except Exception as e:
        db.rollback()
        logger.error(f"Transaction rolled back: {e}", exc_info=True)
        raise DatabaseError('transaction', e) from e
    finally:
        db.close()

# Usage
with database_transaction(db) as conn:
    conn.execute("INSERT INTO users ...")
```

### Class-Based Context Manager

```python
from typing import Optional

class FileHandler:
    """Context manager for file operations"""

    def __init__(self, path: str, mode: str = 'r'):
        self.path = path
        self.mode = mode
        self.file: Optional[Any] = None

    def __enter__(self):
        try:
            self.file = open(self.path, self.mode)
            logger.debug(f"Opened file: {self.path}")
            return self.file
        except IOError as e:
            logger.error(f"Failed to open file: {self.path}", exc_info=True)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
            logger.debug(f"Closed file: {self.path}")

        if exc_type is not None:
            logger.error(f"Error in file operation: {exc_val}")

        # Return False to propagate exceptions
        return False

# Usage
with FileHandler('data.txt', 'r') as f:
    data = f.read()
```

### Suppress Exceptions

```python
from contextlib import suppress

# Suppress specific exceptions
with suppress(FileNotFoundError):
    os.remove('temp.txt')  # No error if file doesn't exist

# Multiple exceptions
with suppress(ValueError, TypeError):
    data = int(input("Enter a number: "))
```

## Decorators for Error Handling

### Basic Error Handler Decorator

```python
from functools import wraps
from typing import Callable, Any

def handle_errors(func: Callable) -> Callable:
    """Decorator to handle errors in functions"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except ApplicationError:
            # Re-raise application errors
            raise
        except Exception as e:
            logger.error(
                f"Error in {func.__name__}",
                exc_info=True,
                extra={'args': args, 'kwargs': kwargs}
            )
            raise ApplicationError(
                f"Operation failed: {func.__name__}",
                'OPERATION_ERROR'
            ) from e

    return wrapper

# Usage
@handle_errors
def process_user(user_id: str) -> User:
    return fetch_user(user_id)
```

### Retry Decorator

```python
import time
from functools import wraps
from typing import Callable, Type, Tuple

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """Retry decorator with exponential backoff"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts",
                            exc_info=True
                        )
                        raise

                    logger.warning(
                        f"{func.__name__} attempt {attempt + 1}/{max_attempts} failed, "
                        f"retrying in {current_delay}s",
                        extra={'error': str(e)}
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator

# Usage
@retry(max_attempts=3, delay=1.0, exceptions=(ConnectionError, TimeoutError))
def fetch_from_api(url: str) -> dict:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

### Async Retry Decorator

```python
import asyncio
from functools import wraps
from typing import Callable, Type, Tuple

def async_retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """Async retry decorator with exponential backoff"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts",
                            exc_info=True
                        )
                        raise

                    logger.warning(
                        f"{func.__name__} attempt {attempt + 1}/{max_attempts} failed"
                    )
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator

# Usage
@async_retry(max_attempts=3, exceptions=(aiohttp.ClientError,))
async def fetch_async(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

## Exception Chaining

### Explicit Exception Chaining

```python
def fetch_user(user_id: str) -> User:
    try:
        result = db.query("SELECT * FROM users WHERE id = ?", user_id)
        return User(**result)
    except DatabaseConnectionError as e:
        # Chain exceptions with 'from'
        raise DatabaseError('fetch_user', e) from e
    except KeyError as e:
        # Transform to domain exception
        raise ValidationError(
            'Invalid user data structure',
            {'user_id': 'User data incomplete'}
        ) from e
```

### Suppress Exception Context

```python
def process_data(data: dict) -> None:
    try:
        validate(data)
    except ValueError as e:
        # Suppress original exception from context
        raise ValidationError(
            'Data validation failed',
            {'data': str(e)}
        ) from None  # Hides original traceback
```

### Accessing Exception Chain

```python
try:
    operation()
except Exception as e:
    # Access the exception chain
    current = e
    while current:
        logger.error(f"Exception: {type(current).__name__}: {current}")
        current = current.__cause__ or current.__context__
```

## FastAPI Error Handling

### Exception Handlers

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(ApplicationError)
async def application_error_handler(
    request: Request,
    exc: ApplicationError
) -> JSONResponse:
    """Handle application errors"""

    logger.error(
        "Application error",
        extra={
            'error': exc,
            'path': request.url.path,
            'method': request.method
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': {
                'message': exc.message,
                'code': exc.code,
                **exc.context
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors"""

    errors = {}
    for error in exc.errors():
        field = '.'.join(str(loc) for loc in error['loc'])
        errors[field] = error['msg']

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'error': {
                'message': 'Validation failed',
                'code': 'VALIDATION_ERROR',
                'fields': errors
            }
        }
    )


@app.exception_handler(Exception)
async def generic_error_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected errors"""

    logger.error(
        "Unexpected error",
        exc_info=True,
        extra={
            'path': request.url.path,
            'method': request.method
        }
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'error': {
                'message': 'An unexpected error occurred',
                'code': 'INTERNAL_SERVER_ERROR'
            }
        }
    )
```

### Dependency Error Handling

```python
from fastapi import Depends, HTTPException

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Dependency that raises HTTPException"""
    try:
        payload = decode_token(token)
        user = await get_user(payload['sub'])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## Django Error Handling

### Custom Exception Middleware

```python
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(MiddlewareMixin):
    """Middleware to handle exceptions"""

    def process_exception(self, request, exception):
        # Log the exception
        logger.error(
            "Django exception",
            exc_info=True,
            extra={
                'path': request.path,
                'method': request.method,
                'user': getattr(request.user, 'id', None)
            }
        )

        # Handle application errors
        if isinstance(exception, ApplicationError):
            return JsonResponse(
                {
                    'error': {
                        'message': exception.message,
                        'code': exception.code
                    }
                },
                status=exception.status_code
            )

        # Handle validation errors
        if isinstance(exception, ValidationError):
            return JsonResponse(
                {
                    'error': {
                        'message': 'Validation failed',
                        'code': 'VALIDATION_ERROR',
                        'fields': exception.fields
                    }
                },
                status=400
            )

        # Unknown errors
        return JsonResponse(
            {
                'error': {
                    'message': 'An unexpected error occurred',
                    'code': 'INTERNAL_SERVER_ERROR'
                }
            },
            status=500
        )
```

### Django REST Framework Exception Handler

```python
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """Custom exception handler for DRF"""

    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    # Log the exception
    logger.error(
        "DRF exception",
        exc_info=True,
        extra={
            'view': context['view'].__class__.__name__,
            'request': context['request'].path
        }
    )

    # Handle application errors
    if isinstance(exc, ApplicationError):
        return Response(
            {
                'error': {
                    'message': exc.message,
                    'code': exc.code
                }
            },
            status=exc.status_code
        )

    # Return DRF's response if available
    if response is not None:
        return response

    # Handle unexpected errors
    return Response(
        {
            'error': {
                'message': 'An unexpected error occurred',
                'code': 'INTERNAL_SERVER_ERROR'
            }
        },
        status=500
    )

# In settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.exceptions.custom_exception_handler'
}
```

## Async Exception Handling

### Basic Async Error Handling

```python
async def fetch_user_async(user_id: str) -> User:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'/api/users/{user_id}') as response:
                if response.status == 404:
                    raise NotFoundError('User', user_id)
                response.raise_for_status()
                data = await response.json()
                return User(**data)
    except aiohttp.ClientError as e:
        logger.error(f"Failed to fetch user: {user_id}", exc_info=True)
        raise ExternalServiceError('User API', str(e)) from e
```

### Gather with Error Handling

```python
async def fetch_multiple_users(user_ids: list[str]) -> list[User]:
    """Fetch multiple users, fail fast on first error"""
    tasks = [fetch_user_async(uid) for uid in user_ids]
    try:
        users = await asyncio.gather(*tasks)
        return users
    except Exception as e:
        logger.error("Failed to fetch users", exc_info=True)
        raise

async def fetch_multiple_users_partial(
    user_ids: list[str]
) -> tuple[list[User], list[Exception]]:
    """Fetch multiple users, collect all errors"""
    tasks = [fetch_user_async(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    users = []
    errors = []

    for result in results:
        if isinstance(result, Exception):
            errors.append(result)
        else:
            users.append(result)

    return users, errors
```

## Best Practices Summary

1. **Use exception hierarchy**: Create a base exception and inherit from it
2. **Chain exceptions**: Use `from` to preserve exception context
3. **Context managers**: Use `with` statements for resource management
4. **Decorators**: Use decorators for cross-cutting error handling
5. **Log with exc_info**: Always use `exc_info=True` to capture stack traces
6. **Don't catch Exception**: Catch specific exceptions when possible
7. **Clean up resources**: Use `finally` or context managers
8. **Custom error messages**: Provide clear, actionable error messages
9. **Test error paths**: Write tests for all exception scenarios
10. **Document exceptions**: Document which exceptions functions can raise
