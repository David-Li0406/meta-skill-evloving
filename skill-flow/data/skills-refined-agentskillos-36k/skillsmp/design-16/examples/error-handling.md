# Pattern: Error Handling

> Standard patterns for handling, propagating, and recovering from errors.

---

## When to Use This Pattern

- Building service boundaries (API handlers, background jobs)
- Implementing retry logic and circuit breakers
- Designing error responses for APIs
- Adding observability to error flows

**Do NOT use when:**
- Simple scripts with fail-fast behavior
- Errors that should crash the process (unrecoverable)

---

## The Pattern

### TypeScript/JavaScript

```typescript
// errors.ts - Define error hierarchy
export class AppError extends Error {
  public readonly code: string;
  public readonly statusCode: number;
  public readonly isOperational: boolean;
  public readonly context?: Record<string, unknown>;

  constructor(
    message: string,
    code: string,
    statusCode: number = 500,
    isOperational: boolean = true,
    context?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    this.context = context;
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      code: this.code,
      statusCode: this.statusCode,
      ...(process.env.NODE_ENV !== 'production' && { stack: this.stack }),
    };
  }
}

// Specific error types
export class ValidationError extends AppError {
  constructor(message: string, context?: Record<string, unknown>) {
    super(message, 'VALIDATION_ERROR', 400, true, context);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', 404, true, { resource, id });
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(message, 'UNAUTHORIZED', 401, true);
  }
}

export class ForbiddenError extends AppError {
  constructor(message: string = 'Forbidden') {
    super(message, 'FORBIDDEN', 403, true);
  }
}

export class ConflictError extends AppError {
  constructor(message: string, context?: Record<string, unknown>) {
    super(message, 'CONFLICT', 409, true, context);
  }
}

export class RateLimitError extends AppError {
  public readonly retryAfter?: number;

  constructor(message: string = 'Rate limit exceeded', retryAfter?: number) {
    super(message, 'RATE_LIMIT', 429, true);
    this.retryAfter = retryAfter;
  }
}

export class ExternalServiceError extends AppError {
  public readonly service: string;

  constructor(service: string, message: string, context?: Record<string, unknown>) {
    super(message, 'EXTERNAL_SERVICE_ERROR', 502, true, context);
    this.service = service;
  }
}

// error-handler.ts - Express middleware
import { Request, Response, NextFunction } from 'express';
import { AppError } from './errors';
import { logger } from './logger';

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log the error
  logger.error('Request error', {
    error: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method,
    requestId: req.headers['x-request-id'],
  });

  // Handle known errors
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      error: {
        code: error.code,
        message: error.message,
        ...(error.context && { details: error.context }),
      },
    });
  }

  // Handle unknown errors (don't leak details in production)
  const message = process.env.NODE_ENV === 'production'
    ? 'Internal server error'
    : error.message;

  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message,
    },
  });
}

// Async wrapper for Express routes
export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// result.ts - Result type for explicit error handling
export type Result<T, E = AppError> =
  | { success: true; data: T }
  | { success: false; error: E };

export function ok<T>(data: T): Result<T, never> {
  return { success: true, data };
}

export function err<E>(error: E): Result<never, E> {
  return { success: false, error };
}

// Usage example
async function getUser(id: string): Promise<Result<User>> {
  try {
    const user = await db.users.findById(id);
    if (!user) {
      return err(new NotFoundError('User', id));
    }
    return ok(user);
  } catch (e) {
    return err(new AppError('Database error', 'DB_ERROR', 500, true, { originalError: e.message }));
  }
}
```

### Python

```python
# errors.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import traceback
import logging

logger = logging.getLogger(__name__)

@dataclass
class AppError(Exception):
    message: str
    code: str
    status_code: int = 500
    is_operational: bool = True
    context: Optional[Dict[str, Any]] = field(default_factory=dict)

    def __str__(self):
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        return {
            'code': self.code,
            'message': self.message,
            **(self.context if self.context else {})
        }

class ValidationError(AppError):
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(
            message=message,
            code='VALIDATION_ERROR',
            status_code=400,
            context=context
        )

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(
            message=f'{resource} not found: {id}',
            code='NOT_FOUND',
            status_code=404,
            context={'resource': resource, 'id': id}
        )

class UnauthorizedError(AppError):
    def __init__(self, message: str = 'Unauthorized'):
        super().__init__(
            message=message,
            code='UNAUTHORIZED',
            status_code=401
        )

class ExternalServiceError(AppError):
    def __init__(self, service: str, message: str, context: Optional[Dict] = None):
        super().__init__(
            message=message,
            code='EXTERNAL_SERVICE_ERROR',
            status_code=502,
            context={'service': service, **(context or {})}
        )

# error_handler.py - Flask/FastAPI middleware
from flask import jsonify, request
from functools import wraps

def error_handler(app):
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        logger.error(
            f"App error: {error.message}",
            extra={
                'code': error.code,
                'path': request.path,
                'method': request.method,
            }
        )
        return jsonify({'error': error.to_dict()}), error.status_code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        logger.exception("Unexpected error")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error'
            }
        }), 500

# result.py - Result type
from typing import TypeVar, Generic, Union
from dataclasses import dataclass

T = TypeVar('T')
E = TypeVar('E', bound=Exception)

@dataclass
class Ok(Generic[T]):
    value: T

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False

@dataclass
class Err(Generic[E]):
    error: E

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def is_err(self) -> bool:
        return True

Result = Union[Ok[T], Err[E]]

def ok(value: T) -> Ok[T]:
    return Ok(value)

def err(error: E) -> Err[E]:
    return Err(error)

# Usage
async def get_user(id: str) -> Result[User, AppError]:
    try:
        user = await db.users.find_by_id(id)
        if not user:
            return err(NotFoundError('User', id))
        return ok(user)
    except Exception as e:
        return err(AppError(
            message='Database error',
            code='DB_ERROR',
            context={'original': str(e)}
        ))
```

### Error Recovery Pattern

```typescript
// circuit-breaker.ts
interface CircuitBreakerConfig {
  failureThreshold: number;
  resetTimeout: number;
}

class CircuitBreaker {
  private failures = 0;
  private lastFailure: Date | null = null;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  constructor(private config: CircuitBreakerConfig) {}

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (this.shouldReset()) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is open');
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private shouldReset(): boolean {
    if (!this.lastFailure) return false;
    const elapsed = Date.now() - this.lastFailure.getTime();
    return elapsed >= this.config.resetTimeout;
  }

  private onSuccess() {
    this.failures = 0;
    this.state = 'closed';
  }

  private onFailure() {
    this.failures++;
    this.lastFailure = new Date();
    if (this.failures >= this.config.failureThreshold) {
      this.state = 'open';
    }
  }
}

// Usage
const breaker = new CircuitBreaker({ failureThreshold: 5, resetTimeout: 30000 });

async function callExternalService() {
  return breaker.execute(async () => {
    return await externalApi.call();
  });
}
```

---

## Common Mistakes to Avoid

### 1. Swallowing Errors
```typescript
// BAD - error is swallowed, no logging or handling
try {
  await riskyOperation();
} catch (e) {
  // do nothing
}

// GOOD - at minimum, log the error
try {
  await riskyOperation();
} catch (e) {
  logger.warn('Operation failed, using fallback', { error: e.message });
  return fallbackValue;
}
```

### 2. Leaking Internal Details
```typescript
// BAD - exposes stack trace and internal paths
res.status(500).json({ error: error.stack });

// GOOD - sanitize for production
res.status(500).json({
  error: {
    code: 'INTERNAL_ERROR',
    message: 'An unexpected error occurred'
  }
});
```

### 3. Inconsistent Error Formats
```typescript
// BAD - different formats across endpoints
res.json({ error: 'Not found' });  // endpoint 1
res.json({ message: 'Not found', status: 404 });  // endpoint 2
res.json({ err: { msg: 'Not found' } });  // endpoint 3

// GOOD - consistent format everywhere
res.json({ error: { code: 'NOT_FOUND', message: 'Resource not found' } });
```

### 4. Not Distinguishing Operational vs Programming Errors
```typescript
// BAD - treats all errors the same
catch (e) {
  res.status(500).json({ error: e.message });
}

// GOOD - operational errors are expected, programming errors should crash
catch (e) {
  if (e instanceof AppError && e.isOperational) {
    res.status(e.statusCode).json({ error: e.toJSON() });
  } else {
    // Programming error - log and crash (let process manager restart)
    logger.fatal('Unexpected error', { error: e });
    process.exit(1);
  }
}
```

### 5. Catching Too Broadly
```typescript
// BAD - catches everything including programming errors
try {
  const result = processData(data);
  await saveToDb(result);
} catch (e) {
  return defaultValue;
}

// GOOD - only catch expected errors
try {
  await saveToDb(result);
} catch (e) {
  if (e instanceof DatabaseError) {
    return handleDbError(e);
  }
  throw e; // Re-throw unexpected errors
}
```

---

## Validation Commands

```bash
# Verify error classes are properly exported
npx tsc --noEmit src/errors.ts

# Run error handling tests
npm test -- --testPathPattern="error"

# Check for swallowed errors (empty catch blocks)
! grep -rn "catch.*{[[:space:]]*}" src/ || echo "WARNING: Empty catch blocks found"

# Verify consistent error format in responses
grep -rn "res.json\|res.status" src/routes/ | head -20

# Test error responses
curl -s http://localhost:8080/nonexistent | jq '.error.code'
```

---

## Related Conventions

- **Error Codes**: All errors MUST have a unique error code (SCREAMING_SNAKE_CASE)
- **Status Codes**: Map error types to HTTP status codes consistently
- **Logging**: Log all errors with context (request ID, user ID, operation)
- **Recovery**: Operational errors should be recoverable; programming errors should crash
- **Format**: All API error responses MUST follow: `{ error: { code, message, details? } }`

---

## See Also

- [API Client](api-client.md) - Error handling for HTTP clients
- [Config Loading](config-loading.md) - Configuration validation errors
- [Database Patterns](database-patterns.md) - Database error handling
