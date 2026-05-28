---
name: frontend-error-handling
description: Provides error handling patterns for React applications. This skill should be used when implementing error boundaries, API error interceptors, error tracking, or user-friendly error messages.
---

# Frontend Error Handling

This skill provides patterns for handling errors gracefully in React applications.

## Error Categories

### 1. API Errors

**What**: Errors from failed API requests (network errors, 4xx/5xx responses).

**Handling Strategy**: Use API client interceptors to handle errors globally.

**Implementation** (`src/lib/api-client.ts`):

```typescript
import axios from 'axios';
import { useNotifications } from '@/stores/notifications-store';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const message = error.response.data?.message || 'An error occurred';

      switch (status) {
        case 401:
          // Unauthorized - redirect to login
          window.location.href = '/login';
          break;
        case 403:
          // Forbidden - show permission error
          showNotification({
            type: 'error',
            message: 'You do not have permission to perform this action',
          });
          break;
        case 404:
          // Not found
          showNotification({
            type: 'error',
            message: 'Resource not found',
          });
          break;
        case 500:
          // Server error
          showNotification({
            type: 'error',
            message: 'Server error. Please try again later.',
          });
          break;
        default:
          // Generic error
          showNotification({
            type: 'error',
            message,
          });
      }
    } else if (error.request) {
      // Request made but no response received (network error)
      showNotification({
        type: 'error',
        message: 'Network error. Please check your connection.',
      });
    } else {
      // Something else happened
      showNotification({
        type: 'error',
        message: 'An unexpected error occurred',
      });
    }

    return Promise.reject(error);
  }
);

// Helper to show notifications (integrate with your notification system)
function showNotification(notification: { type: string; message: string }) {
  // Implementation depends on your notification system
  // Could use toast library, custom notification component, etc.
}
```

**Best Practices**:
- Show user-friendly error messages (not technical details)
- Log technical details for debugging
- Handle different status codes appropriately
- Provide actionable feedback when possible

### 2. In-App Errors (Component Errors)

**What**: Errors that occur during rendering, in lifecycle methods, or in event handlers.

**Handling Strategy**: Use Error Boundaries to catch and handle component errors.

**Implementation**:

```typescript
// src/components/ErrorBoundary.tsx
import { Component, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log error to error tracking service
    console.error('Error caught by boundary:', error, errorInfo);
    
    // Call optional error handler
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Render custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4">
          <h1 className="text-2xl font-bold mb-4">Something went wrong</h1>
          <p className="text-muted-foreground mb-4">
            We're sorry for the inconvenience. Please try refreshing the page.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-primary text-primary-foreground rounded"
          >
            Refresh Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

**Usage** - Multiple Error Boundaries:

```typescript
// App-level error boundary (catches critical errors)
function App() {
  return (
    <ErrorBoundary fallback={<CriticalErrorPage />}>
      <Router />
    </ErrorBoundary>
  );
}

// Route-level error boundary (catches route-specific errors)
function DashboardRoute() {
  return (
    <ErrorBoundary fallback={<RouteErrorMessage />}>
      <Dashboard />
    </ErrorBoundary>
  );
}

// Component-level error boundary (catches component-specific errors)
function UserProfile() {
  return (
    <div>
      <h1>User Profile</h1>
      <ErrorBoundary fallback={<div>Failed to load activity feed</div>}>
        <ActivityFeed />
      </ErrorBoundary>
    </div>
  );
}
```

**Best Practices**:
- Use multiple error boundaries at different levels
- Provide specific fallback UI for each boundary
- Don't wrap the entire app in a single boundary
- Error boundaries don't catch:
  - Event handlers (use try-catch)
  - Async code (use try-catch)
  - Server-side rendering errors
  - Errors in the error boundary itself

### 3. Async Errors (Event Handlers, useEffect)

**What**: Errors in event handlers, useEffect, or other async code.

**Handling Strategy**: Use try-catch blocks and handle errors explicitly.

**Example** (Event Handler):

```typescript
function DeleteButton({ itemId }: { itemId: string }) {
  const deleteItem = useDeleteItem();
  const { addNotification } = useNotifications();

  const handleDelete = async () => {
    try {
      await deleteItem.mutateAsync(itemId);
      addNotification({
        type: 'success',
        message: 'Item deleted successfully',
      });
    } catch (error) {
      // Handle error
      addNotification({
        type: 'error',
        message: 'Failed to delete item. Please try again.',
      });
      
      // Log for debugging
      console.error('Delete failed:', error);
    }
  };

  return (
    <button onClick={handleDelete} disabled={deleteItem.isPending}>
      {deleteItem.isPending ? 'Deleting...' : 'Delete'}
    </button>
  );
}
```

**Example** (useEffect):

```typescript
function DataLoader({ userId }: { userId: string }) {
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchUserData(userId);
        // Process data
      } catch (err) {
        setError(err as Error);
        console.error('Failed to load data:', err);
      }
    }

    loadData();
  }, [userId]);

  if (error) {
    return <ErrorMessage error={error} />;
  }

  return <div>{/* Render data */}</div>;
}
```

## Error Tracking

**What**: Monitoring and logging errors that occur in production.

**Recommended Tool**: [Sentry](https://sentry.io/)

**Setup**:

```typescript
// src/lib/sentry.ts
import * as Sentry from '@sentry/react';

export function initSentry() {
  if (import.meta.env.PROD) {
    Sentry.init({
      dsn: import.meta.env.VITE_SENTRY_DSN,
      environment: import.meta.env.MODE,
      integrations: [
        new Sentry.BrowserTracing(),
        new Sentry.Replay(),
      ],
      tracesSampleRate: 0.1,
      replaysSessionSampleRate: 0.1,
      replaysOnErrorSampleRate: 1.0,
    });
  }
}

// src/main.tsx
import { initSentry } from './lib/sentry';

initSentry();

// ... rest of app initialization
```

**Usage with Error Boundary**:

```typescript
import * as Sentry from '@sentry/react';

<ErrorBoundary
  onError={(error, errorInfo) => {
    Sentry.captureException(error, {
      contexts: {
        react: {
          componentStack: errorInfo.componentStack,
        },
      },
    });
  }}
>
  <App />
</ErrorBoundary>
```

**Manual Error Reporting**:

```typescript
try {
  await riskyOperation();
} catch (error) {
  // Report to Sentry
  Sentry.captureException(error, {
    tags: {
      feature: 'user-profile',
      action: 'update',
    },
    extra: {
      userId: user.id,
    },
  });
  
  // Show user-friendly message
  showNotification({ type: 'error', message: 'Operation failed' });
}
```

## User-Friendly Error Messages

**Principles**:
1. **Be clear and concise** - Explain what went wrong in simple terms
2. **Be actionable** - Tell users what they can do to fix it
3. **Be empathetic** - Acknowledge the frustration
4. **Don't expose technical details** - Keep stack traces and error codes hidden from users

**Examples**:

```typescript
// ❌ BAD: Technical error message
"Error: Network request failed with status 500"

// ✅ GOOD: User-friendly message
"We're having trouble connecting to our servers. Please try again in a moment."

// ❌ BAD: Vague message
"Something went wrong"

// ✅ GOOD: Specific and actionable
"We couldn't save your changes. Please check your internet connection and try again."
```

**Error Message Component**:

```typescript
interface ErrorMessageProps {
  title?: string;
  message: string;
  retry?: () => void;
}

export function ErrorMessage({ title = 'Error', message, retry }: ErrorMessageProps) {
  return (
    <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-4">
      <h3 className="font-semibold text-destructive mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground mb-4">{message}</p>
      {retry && (
        <button
          onClick={retry}
          className="text-sm text-primary hover:underline"
        >
          Try again
        </button>
      )}
    </div>
  );
}
```

## Best Practices

1. **Layer your error handling** - Use error boundaries, API interceptors, and try-catch together
2. **Provide context** - Include relevant information when logging errors
3. **Fail gracefully** - Show fallback UI instead of blank screens
4. **Track errors in production** - Use Sentry or similar tool
5. **Test error states** - Ensure error handling works as expected
6. **Don't silence errors** - Always log errors for debugging
7. **Provide recovery options** - Give users a way to retry or navigate away

## Checklist

- [ ] API client has error interceptor for global error handling
- [ ] Error boundaries are used at multiple levels (app, route, component)
- [ ] Async errors in event handlers and useEffect are caught with try-catch
- [ ] Error tracking is set up (Sentry or similar)
- [ ] Error messages are user-friendly and actionable
- [ ] Fallback UI is provided for all error states
- [ ] Errors are logged for debugging (console.error or error tracking)
- [ ] Users have a way to recover from errors (retry, refresh, navigate)
