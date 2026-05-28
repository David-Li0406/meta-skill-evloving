# Error Handling - API Reference

API reference for error handling patterns including ErrorBoundary, error tracking, and recovery strategies.

## Official Documentation

- **React Error Boundaries**: https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary
- **OpenTelemetry**: https://opentelemetry.io/docs/instrumentation/js/
- **GraphQL Error Handling**: https://www.apollographql.com/docs/react/data/error-handling/

## ErrorBoundary Component

### Basic Implementation

```typescript
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback: (error: Error, resetError: () => void) => ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.props.onError?.(error, errorInfo);
  }

  resetError = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      return this.props.fallback(this.state.error, this.resetError);
    }

    return this.props.children;
  }
}
```

### With OpenTelemetry Integration

```typescript
import { Span } from '@opentelemetry/api';

componentDidCatch(error: Error, errorInfo: ErrorInfo) {
  // Record error in span
  if (this.span) {
    this.span.recordException(error);
    this.span.setAttributes({
      'error.type': error.name,
      'error.message': error.message,
      'component.stack': errorInfo.componentStack,
    });
  }

  this.props.onError?.(error, errorInfo);
}
```

## GraphQL Error Handling

### Error Policy Configuration

```typescript
import { useQuery } from '@apollo/client';

const { data, error } = useQuery(GET_USER, {
  errorPolicy: 'all', // Return both data and errors
});

if (error) {
  // Handle GraphQL errors
  error.graphQLErrors.forEach((err) => {
    console.error('GraphQL Error:', err.message);
  });

  if (error.networkError) {
    console.error('Network Error:', error.networkError);
  }
}
```

### Error Policy Options

```typescript
type ErrorPolicy =
  | 'none'         // Treat GraphQL errors as runtime errors
  | 'ignore'       // Ignore GraphQL errors, return data
  | 'all';         // Return both data and errors
```

## React Query Error Handling

### With onError Callback

```typescript
import { useQuery } from 'react-query';

const { data, error, isError } = useQuery(
  ['user', userId],
  () => fetchUser(userId),
  {
    onError: (error: Error) => {
      console.error('Query failed:', error);
      trackError(error);
    },
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  }
);
```

## Retry Strategies

### Exponential Backoff

```typescript
const retry = async <T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;

      const delay = Math.min(1000 * 2 ** i, 30000);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw new Error('Max retries exceeded');
};
```

### With Condition

```typescript
const retryIf = async <T>(
  fn: () => Promise<T>,
  shouldRetry: (error: Error) => boolean,
  maxRetries: number = 3
): Promise<T> => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1 || !shouldRetry(error as Error)) {
        throw error;
      }

      await new Promise(resolve => setTimeout(resolve, 1000 * 2 ** i));
    }
  }

  throw new Error('Max retries exceeded');
};

// Usage
await retryIf(
  () => fetchData(),
  (error) => error.message.includes('timeout'),
  3
);
```

## Error Types

### Custom Error Classes

```typescript
class NetworkError extends Error {
  constructor(message: string, public statusCode?: number) {
    super(message);
    this.name = 'NetworkError';
  }
}

class ValidationError extends Error {
  constructor(message: string, public field?: string) {
    super(message);
    this.name = 'ValidationError';
  }
}
```

### Type Guards

```typescript
function isNetworkError(error: unknown): error is NetworkError {
  return error instanceof NetworkError;
}

function isValidationError(error: unknown): error is ValidationError {
  return error instanceof ValidationError;
}

// Usage
catch (error) {
  if (isNetworkError(error)) {
    handleNetworkError(error);
  } else if (isValidationError(error)) {
    handleValidationError(error);
  }
}
```

## Fallback UI Components

### Basic Fallback

```typescript
interface ErrorFallbackProps {
  error: Error;
  resetError: () => void;
}

export const ErrorFallback: React.FC<ErrorFallbackProps> = ({
  error,
  resetError,
}) => (
  <div data-testid="error-fallback">
    <h1>Something went wrong</h1>
    <pre>{error.message}</pre>
    <button onClick={resetError}>Try again</button>
  </div>
);
```

### With Recovery Actions

```typescript
export const ErrorFallbackWithActions: React.FC<ErrorFallbackProps> = ({
  error,
  resetError,
}) => {
  const handleReload = () => {
    window.location.reload();
  };

  const handleGoHome = () => {
    window.location.href = '/';
  };

  return (
    <div data-testid="error-fallback">
      <h1>Oops! Something went wrong</h1>
      <p>{error.message}</p>
      <div>
        <button onClick={resetError}>Try Again</button>
        <button onClick={handleReload}>Reload Page</button>
        <button onClick={handleGoHome}>Go Home</button>
      </div>
    </div>
  );
};
```

## Error Tracking

### With Analytics

```typescript
const trackError = (error: Error, context?: Record<string, any>) => {
  analytics.track('Error_Occurred', {
    error_message: error.message,
    error_stack: error.stack,
    error_name: error.name,
    ...context,
  });
};
```

### With Sentry

```typescript
import * as Sentry from '@sentry/react';

Sentry.captureException(error, {
  tags: {
    feature: 'checkout',
    component: 'PaymentForm',
  },
  extra: {
    userId: user.id,
    formData: sanitizedFormData,
  },
});
```

## Testing Patterns

### Testing ErrorBoundary

```typescript
it('renders fallback on error', () => {
  const ThrowError = () => {
    throw new Error('Test error');
  };

  render(
    <ErrorBoundary fallback={(error) => <div>{error.message}</div>}>
      <ThrowError />
    </ErrorBoundary>
  );

  expect(screen.getByText('Test error')).toBeInTheDocument();
});
```

### Testing Error Handling

```typescript
it('handles query error', async () => {
  const mockError = new Error('API Error');
  jest.spyOn(console, 'error').mockImplementation();

  server.use(
    rest.get('/api/user', (req, res, ctx) => {
      return res(ctx.status(500), ctx.json({ message: 'Server error' }));
    })
  );

  render(<UserComponent />);

  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument();
  });
});
```

## Best Practices

1. **Isolate errors** - Use ErrorBoundary to prevent app crashes
2. **Provide context** - Include relevant information in error tracking
3. **User-friendly messages** - Don't show technical errors to users
4. **Recovery actions** - Give users ways to recover from errors
5. **Retry transient failures** - Implement exponential backoff
6. **Log comprehensively** - Track errors for debugging
7. **Test error paths** - Ensure error handling works correctly
