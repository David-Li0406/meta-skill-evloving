# JavaScript/TypeScript Error Handling Patterns

## Table of Contents

1. [Custom Error Classes](#custom-error-classes)
2. [Async Error Handling](#async-error-handling)
3. [Promise Error Handling](#promise-error-handling)
4. [Error Boundaries (React)](#error-boundaries-react)
5. [Express.js Error Middleware](#expressjs-error-middleware)
6. [NestJS Exception Filters](#nestjs-exception-filters)
7. [Error Aggregation](#error-aggregation)
8. [TypeScript Type-Safe Errors](#typescript-type-safe-errors)

## Custom Error Classes

### Basic Custom Error

```typescript
class ApplicationError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public isOperational: boolean = true,
    public context?: Record<string, any>
  ) {
    super(message);
    this.name = this.constructor.name;

    // Maintains proper stack trace for where error was thrown (V8 only)
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      code: this.code,
      statusCode: this.statusCode,
      context: this.context
    };
  }
}
```

### Domain-Specific Error Hierarchy

```typescript
// Base application error
class ApplicationError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Validation errors
class ValidationError extends ApplicationError {
  constructor(
    message: string,
    public fields: Record<string, string>
  ) {
    super(message, 'VALIDATION_ERROR', 400);
  }
}

// Resource not found
class NotFoundError extends ApplicationError {
  constructor(resource: string, identifier: string) {
    super(
      `${resource} not found: ${identifier}`,
      'NOT_FOUND',
      404
    );
  }
}

// Authentication errors
class AuthenticationError extends ApplicationError {
  constructor(message: string = 'Authentication failed') {
    super(message, 'AUTHENTICATION_ERROR', 401);
  }
}

// Authorization errors
class AuthorizationError extends ApplicationError {
  constructor(message: string = 'Access denied') {
    super(message, 'AUTHORIZATION_ERROR', 403);
  }
}

// Business logic errors
class BusinessRuleError extends ApplicationError {
  constructor(message: string, code: string) {
    super(message, code, 422);
  }
}

// External service errors
class ExternalServiceError extends ApplicationError {
  constructor(
    service: string,
    message: string,
    public originalError?: Error
  ) {
    super(
      `${service} error: ${message}`,
      'EXTERNAL_SERVICE_ERROR',
      503
    );
  }
}

// Usage examples
throw new ValidationError('Invalid input', {
  email: 'Invalid email format',
  age: 'Must be at least 18'
});

throw new NotFoundError('User', userId);

throw new AuthenticationError('Invalid credentials');

throw new BusinessRuleError(
  'Cannot delete order with pending shipment',
  'ORDER_HAS_PENDING_SHIPMENT'
);
```

## Async Error Handling

### Async/Await Pattern

```typescript
async function fetchUserData(userId: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${userId}`);

    if (!response.ok) {
      throw new NotFoundError('User', userId);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    // Re-throw known errors
    if (error instanceof ApplicationError) {
      throw error;
    }

    // Wrap unknown errors
    logger.error('Failed to fetch user data', { userId, error });
    throw new ExternalServiceError(
      'User API',
      'Failed to fetch user data',
      error as Error
    );
  }
}
```

### Async Error Wrapper

```typescript
function asyncHandler<T extends any[]>(
  fn: (...args: T) => Promise<any>
) {
  return async (...args: T) => {
    try {
      return await fn(...args);
    } catch (error) {
      // Centralized error handling
      handleError(error);
      throw error;
    }
  };
}

// Usage
const fetchData = asyncHandler(async (id: string) => {
  const response = await fetch(`/api/data/${id}`);
  return response.json();
});
```

### Parallel Operations Error Handling

```typescript
async function fetchMultipleUsers(userIds: string[]): Promise<User[]> {
  try {
    // Promise.all - fails fast on first error
    const users = await Promise.all(
      userIds.map(id => fetchUserData(id))
    );
    return users;
  } catch (error) {
    logger.error('Failed to fetch users', { userIds, error });
    throw error;
  }
}

async function fetchMultipleUsersWithPartialSuccess(
  userIds: string[]
): Promise<{ users: User[], errors: Error[] }> {
  // Promise.allSettled - waits for all, collects errors
  const results = await Promise.allSettled(
    userIds.map(id => fetchUserData(id))
  );

  const users: User[] = [];
  const errors: Error[] = [];

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      users.push(result.value);
    } else {
      logger.warn('Failed to fetch user', {
        userId: userIds[index],
        error: result.reason
      });
      errors.push(result.reason);
    }
  });

  return { users, errors };
}
```

## Promise Error Handling

### Basic Promise Chain

```typescript
fetchUserData(userId)
  .then(user => processUser(user))
  .then(result => saveResult(result))
  .catch(error => {
    if (error instanceof NotFoundError) {
      return createDefaultUser(userId);
    }
    throw error;
  })
  .finally(() => {
    cleanup();
  });
```

### Promise with Retry

```typescript
function retryPromise<T>(
  operation: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  return operation().catch(error => {
    if (maxRetries === 0) {
      throw error;
    }

    return new Promise<T>((resolve, reject) => {
      setTimeout(() => {
        retryPromise(operation, maxRetries - 1, delay * 2)
          .then(resolve)
          .catch(reject);
      }, delay);
    });
  });
}

// Usage
retryPromise(() => fetchUserData(userId), 3)
  .then(user => console.log('User fetched:', user))
  .catch(error => console.error('Failed after retries:', error));
```

### Promise Timeout

```typescript
function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number
): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(
        () => reject(new Error(`Operation timed out after ${timeoutMs}ms`)),
        timeoutMs
      )
    )
  ]);
}

// Usage
withTimeout(fetchUserData(userId), 5000)
  .then(user => console.log('User:', user))
  .catch(error => console.error('Timeout or error:', error));
```

## Error Boundaries (React)

### Class Component Error Boundary

```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to monitoring service
    logger.error('React Error Boundary caught error', {
      error,
      componentStack: errorInfo.componentStack
    });

    // Call custom error handler
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h1>Something went wrong</h1>
          <p>Please refresh the page or contact support.</p>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
```

### Async Error Boundary (React 18+)

```typescript
import { useEffect, useState } from 'react';

function useAsyncError() {
  const [, setError] = useState();

  return (error: Error) => {
    setError(() => {
      throw error;
    });
  };
}

function AsyncComponent() {
  const throwAsyncError = useAsyncError();

  useEffect(() => {
    fetchData()
      .catch(error => {
        // This will be caught by Error Boundary
        throwAsyncError(error);
      });
  }, []);

  return <div>Loading...</div>;
}
```

## Express.js Error Middleware

### Centralized Error Handler

```typescript
import { Request, Response, NextFunction } from 'express';

// Error handling middleware (must be last)
function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log error with context
  logger.error('Express error handler', {
    error: err,
    method: req.method,
    path: req.path,
    query: req.query,
    body: sanitizeForLogging(req.body),
    userId: req.user?.id,
    requestId: req.id
  });

  // Handle known application errors
  if (err instanceof ApplicationError) {
    return res.status(err.statusCode).json({
      error: {
        message: err.message,
        code: err.code,
        ...(err instanceof ValidationError && { fields: err.fields })
      },
      requestId: req.id
    });
  }

  // Handle JWT errors
  if (err.name === 'JsonWebTokenError') {
    return res.status(401).json({
      error: {
        message: 'Invalid authentication token',
        code: 'INVALID_TOKEN'
      },
      requestId: req.id
    });
  }

  // Handle validation errors (express-validator)
  if (err.name === 'ValidationError') {
    return res.status(400).json({
      error: {
        message: 'Validation failed',
        code: 'VALIDATION_ERROR',
        details: err.errors
      },
      requestId: req.id
    });
  }

  // Unknown errors - don't expose details
  res.status(500).json({
    error: {
      message: 'An unexpected error occurred',
      code: 'INTERNAL_SERVER_ERROR'
    },
    requestId: req.id
  });
}

// Async route handler wrapper
function asyncHandler(fn: Function) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Usage
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await fetchUserData(req.params.id);
  res.json(user);
}));

// Error middleware (must be last)
app.use(errorHandler);
```

### 404 Handler

```typescript
app.use((req: Request, res: Response) => {
  res.status(404).json({
    error: {
      message: 'Route not found',
      code: 'NOT_FOUND',
      path: req.path
    }
  });
});
```

## NestJS Exception Filters

### Global Exception Filter

```typescript
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus
} from '@nestjs/common';
import { Request, Response } from 'express';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message = 'Internal server error';
    let code = 'INTERNAL_SERVER_ERROR';

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const exceptionResponse = exception.getResponse();

      if (typeof exceptionResponse === 'object') {
        message = (exceptionResponse as any).message || message;
        code = (exceptionResponse as any).code || code;
      } else {
        message = exceptionResponse;
      }
    } else if (exception instanceof ApplicationError) {
      status = exception.statusCode;
      message = exception.message;
      code = exception.code;
    }

    // Log error
    logger.error('NestJS exception filter', {
      exception,
      method: request.method,
      path: request.url,
      status,
      userId: (request as any).user?.id
    });

    // Send response
    response.status(status).json({
      error: {
        message,
        code,
        timestamp: new Date().toISOString(),
        path: request.url
      }
    });
  }
}

// Register in main.ts
app.useGlobalFilters(new AllExceptionsFilter());
```

### Custom HTTP Exception

```typescript
import { HttpException, HttpStatus } from '@nestjs/common';

export class BusinessRuleException extends HttpException {
  constructor(message: string, code: string) {
    super(
      {
        message,
        code,
        statusCode: HttpStatus.UNPROCESSABLE_ENTITY
      },
      HttpStatus.UNPROCESSABLE_ENTITY
    );
  }
}

// Usage
throw new BusinessRuleException(
  'Cannot delete order with pending shipment',
  'ORDER_HAS_PENDING_SHIPMENT'
);
```

## Error Aggregation

### Collecting Multiple Errors

```typescript
class ErrorCollector {
  private errors: Error[] = [];

  add(error: Error): void {
    this.errors.push(error);
  }

  hasErrors(): boolean {
    return this.errors.length > 0;
  }

  getErrors(): Error[] {
    return this.errors;
  }

  throwIfErrors(): void {
    if (this.hasErrors()) {
      throw new AggregateError(
        this.errors,
        `${this.errors.length} error(s) occurred`
      );
    }
  }
}

// Usage
async function processMultipleUsers(userIds: string[]): Promise<void> {
  const collector = new ErrorCollector();

  for (const userId of userIds) {
    try {
      await processUser(userId);
    } catch (error) {
      collector.add(error as Error);
    }
  }

  collector.throwIfErrors();
}
```

### Aggregate Error (Native)

```typescript
try {
  await Promise.any([
    fetch('https://api1.example.com'),
    fetch('https://api2.example.com'),
    fetch('https://api3.example.com')
  ]);
} catch (error) {
  if (error instanceof AggregateError) {
    logger.error('All API calls failed', {
      errors: error.errors
    });
  }
}
```

## TypeScript Type-Safe Errors

### Result Type Pattern

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function divide(a: number, b: number): Result<number> {
  if (b === 0) {
    return { ok: false, error: new Error('Division by zero') };
  }
  return { ok: true, value: a / b };
}

// Usage
const result = divide(10, 2);
if (result.ok) {
  console.log('Result:', result.value);
} else {
  console.error('Error:', result.error);
}
```

### Type Guards for Errors

```typescript
function isApplicationError(error: unknown): error is ApplicationError {
  return error instanceof ApplicationError;
}

function isValidationError(error: unknown): error is ValidationError {
  return error instanceof ValidationError;
}

// Usage
try {
  await operation();
} catch (error) {
  if (isValidationError(error)) {
    // TypeScript knows error.fields exists
    console.log('Validation errors:', error.fields);
  } else if (isApplicationError(error)) {
    // TypeScript knows error.code exists
    console.log('Error code:', error.code);
  } else {
    // Unknown error
    console.error('Unknown error:', error);
  }
}
```

### Discriminated Union Errors

```typescript
type ApiError =
  | { type: 'NETWORK_ERROR'; message: string }
  | { type: 'VALIDATION_ERROR'; fields: Record<string, string> }
  | { type: 'NOT_FOUND'; resource: string; id: string }
  | { type: 'UNAUTHORIZED'; reason: string };

function handleApiError(error: ApiError): void {
  switch (error.type) {
    case 'NETWORK_ERROR':
      console.error('Network error:', error.message);
      break;
    case 'VALIDATION_ERROR':
      console.error('Validation failed:', error.fields);
      break;
    case 'NOT_FOUND':
      console.error(`${error.resource} ${error.id} not found`);
      break;
    case 'UNAUTHORIZED':
      console.error('Unauthorized:', error.reason);
      break;
  }
}
```

## Best Practices Summary

1. **Always extend Error**: Custom errors should extend Error or a subclass
2. **Capture stack traces**: Use `Error.captureStackTrace()` in V8
3. **Type-safe errors**: Use TypeScript to make errors type-safe
4. **Wrap async handlers**: Use wrapper functions to catch async errors
5. **Centralized error handling**: Use error boundaries and middleware
6. **Log with context**: Always include request ID, user ID, and operation
7. **Never expose internals**: Sanitize error messages for users
8. **Test error paths**: Write tests for all error conditions
9. **Monitor errors**: Send errors to monitoring services
10. **Document error codes**: Maintain a list of all error codes and their meanings
