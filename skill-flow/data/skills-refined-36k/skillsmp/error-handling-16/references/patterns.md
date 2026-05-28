# Error Handling - Implementation Patterns

Implementation patterns and anti-patterns for error handling in React web applications.

## Pattern: Use ErrorBoundary to Isolate Features

Wrap feature components with ErrorBoundary to prevent app-wide crashes.

✅ **Good:**
```typescript
export const RecipeListScreen = () => {
  return (
    <ErrorBoundary
      fallback={(error, resetError) => (
        <ErrorFallback error={error} onRetry={resetError} />
      )}
      onError={(error, errorInfo) => {
        trackError(error, { component: 'RecipeList' });
      }}
    >
      <RecipeListContent />
    </ErrorBoundary>
  );
};
```

❌ **Bad:**
```typescript
// No ErrorBoundary - one error crashes entire app
export const RecipeListScreen = () => {
  return <RecipeListContent />;
};
```

**Why:** ErrorBoundary:
- Prevents full app crashes
- Isolates errors to specific features
- Provides recovery options
- Better user experience
- Enables error tracking

## Pattern: Provide User-Friendly Fallback UI

Show actionable error messages, not technical details.

✅ **Good:**
```typescript
const ErrorFallback = ({ error, resetError }: ErrorFallbackProps) => (
  <div>
    <h1>Something went wrong</h1>
    <p>We're having trouble loading this page. Please try again.</p>
    <button onClick={resetError}>Try Again</button>
    <button onClick={() => window.location.href = '/'}>Go Home</button>
  </div>
);
```

❌ **Bad:**
```typescript
const ErrorFallback = ({ error }: ErrorFallbackProps) => (
  <div>
    <h1>Error</h1>
    {/* Technical details exposed to user */}
    <pre>{error.stack}</pre>
  </div>
);
```

**Why:** User-friendly messages:
- Don't expose technical details
- Provide recovery actions
- Maintain trust
- Clear next steps
- Better UX

## Pattern: Track Errors with Context

Include relevant context when tracking errors.

✅ **Good:**
```typescript
componentDidCatch(error: Error, errorInfo: ErrorInfo) {
  trackError(error, {
    component: 'RecipeList',
    userId: user?.id,
    url: window.location.href,
    timestamp: new Date().toISOString(),
    componentStack: errorInfo.componentStack,
  });
}
```

❌ **Bad:**
```typescript
componentDidCatch(error: Error) {
  // No context - hard to debug
  console.error(error);
}
```

**Why:** Context tracking:
- Easier debugging
- Reproduces issues
- User impact understanding
- Better error reports
- Actionable insights

## Pattern: Use errorPolicy in GraphQL

Configure error handling for GraphQL queries.

✅ **Good:**
```typescript
const { data, error } = useQuery(GET_USER, {
  variables: { id: userId },
  errorPolicy: 'all', // Return both data and errors
});

if (error) {
  // Handle errors gracefully
  if (error.networkError) {
    return <NetworkErrorMessage />;
  }

  if (error.graphQLErrors.length > 0) {
    return <GraphQLErrorMessage errors={error.graphQLErrors} />;
  }
}
```

❌ **Bad:**
```typescript
const { data } = useQuery(GET_USER, {
  variables: { id: userId },
  // No errorPolicy - default behavior may not be what you want
});

// No error handling - crashes if query fails
return <UserProfile user={data.user} />;
```

**Why:** Error policy:
- Explicit error handling
- Partial data support
- Better UX
- Graceful degradation
- Network resilience

## Pattern: Implement Retry with Exponential Backoff

Retry transient failures with increasing delays.

✅ **Good:**
```typescript
const { data, error } = useQuery(
  ['user', userId],
  () => fetchUser(userId),
  {
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  }
);
```

❌ **Bad:**
```typescript
// No retry - fails on first error
const { data, error } = useQuery(
  ['user', userId],
  () => fetchUser(userId)
);

// Or constant retry without backoff
const { data, error } = useQuery(
  ['user', userId],
  () => fetchUser(userId),
  {
    retry: 3,
    retryDelay: 1000, // Same delay every time
  }
);
```

**Why:** Exponential backoff:
- Handles transient failures
- Reduces server load
- Better success rate
- Standard pattern
- Network resilience

## Pattern: Use finally for Cleanup

Always clean up in finally blocks.

✅ **Good:**
```typescript
const fetchData = async () => {
  setLoading(true);

  try {
    const data = await apiCall();
    setData(data);
  } catch (error) {
    setError(error);
    trackError(error);
  } finally {
    setLoading(false); // Always runs
  }
};
```

❌ **Bad:**
```typescript
const fetchData = async () => {
  setLoading(true);

  try {
    const data = await apiCall();
    setData(data);
    setLoading(false); // Doesn't run if error thrown
  } catch (error) {
    setError(error);
    setLoading(false); // Duplicated cleanup
  }
};
```

**Why:** finally blocks:
- Always execute
- Prevent duplicated cleanup
- Cleaner code
- Guaranteed execution
- Standard pattern

## Pattern: Differentiate Error Types

Handle different errors appropriately.

✅ **Good:**
```typescript
catch (error) {
  if (isNetworkError(error)) {
    showMessage('Check your internet connection');
  } else if (isValidationError(error)) {
    showFieldError(error.field, error.message);
  } else if (isAuthError(error)) {
    redirectToLogin();
  } else {
    showGenericError();
  }
}
```

❌ **Bad:**
```typescript
catch (error) {
  // All errors handled the same way
  showMessage('Something went wrong');
}
```

**Why:** Error differentiation:
- Appropriate responses
- Better UX
- Actionable messages
- Targeted fixes
- User guidance

## Pattern: Provide resetError Function

Allow users to retry after errors.

✅ **Good:**
```typescript
const ErrorFallback = ({ error, resetError }: Props) => (
  <div>
    <p>Failed to load data</p>
    <button onClick={resetError}>Try Again</button>
  </div>
);

// In ErrorBoundary
resetError = () => {
  this.setState({ hasError: false, error: null });
};
```

❌ **Bad:**
```typescript
const ErrorFallback = ({ error }: Props) => (
  <div>
    <p>Failed to load data</p>
    {/* No way to recover */}
  </div>
);
```

**Why:** Reset capability:
- User recovery
- Better UX
- Avoid page reload
- Second chances
- Transient error handling

## Pattern: Log Errors Comprehensively

Log errors with full context for debugging.

✅ **Good:**
```typescript
const handleError = (error: Error, context: ErrorContext) => {
  console.error('Error occurred:', {
    name: error.name,
    message: error.message,
    stack: error.stack,
    timestamp: new Date().toISOString(),
    url: window.location.href,
    userAgent: navigator.userAgent,
    ...context,
  });

  // Send to error tracking service
  Sentry.captureException(error, { extra: context });
};
```

❌ **Bad:**
```typescript
const handleError = (error: Error) => {
  console.error(error); // Minimal information
};
```

**Why:** Comprehensive logging:
- Easier debugging
- Production issue tracking
- Reproduction steps
- User impact analysis
- Better monitoring

## Pattern: Test Error Boundaries

Test error handling paths.

✅ **Good:**
```typescript
it('renders error fallback on error', () => {
  const ThrowError = () => {
    throw new Error('Test error');
  };

  const { getByText } = render(
    <ErrorBoundary fallback={(error) => <div>{error.message}</div>}>
      <ThrowError />
    </ErrorBoundary>
  );

  expect(getByText('Test error')).toBeInTheDocument();
});

it('calls onError callback', () => {
  const onError = jest.fn();
  const ThrowError = () => {
    throw new Error('Test error');
  };

  render(
    <ErrorBoundary
      fallback={() => <div>Error</div>}
      onError={onError}
    >
      <ThrowError />
    </ErrorBoundary>
  );

  expect(onError).toHaveBeenCalledWith(
    expect.objectContaining({ message: 'Test error' }),
    expect.any(Object)
  );
});
```

❌ **Bad:**
```typescript
// No error boundary tests
it('renders component', () => {
  render(<MyComponent />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

**Why:** Error testing:
- Ensures error handling works
- Prevents regressions
- Validates fallback UI
- Tests recovery
- Better reliability

## Anti-Pattern: Swallowing Errors

Don't catch errors without handling them.

❌ **Bad:**
```typescript
try {
  await riskyOperation();
} catch (error) {
  // Error swallowed - no logging, no user feedback
}
```

✅ **Good:**
```typescript
try {
  await riskyOperation();
} catch (error) {
  console.error('Operation failed:', error);
  trackError(error);
  showErrorMessage('Operation failed. Please try again.');
}
```

## Anti-Pattern: Exposing Technical Details

Don't show stack traces to users.

❌ **Bad:**
```typescript
<ErrorFallback>
  <h1>Error: {error.name}</h1>
  <pre>{error.stack}</pre>
  <p>ComponentStack: {errorInfo.componentStack}</p>
</ErrorFallback>
```

✅ **Good:**
```typescript
<ErrorFallback>
  <h1>Something went wrong</h1>
  <p>We're working to fix this issue.</p>
  <button onClick={resetError}>Try Again</button>
</ErrorFallback>
```

## Anti-Pattern: No Recovery Options

Don't trap users in error states.

❌ **Bad:**
```typescript
<ErrorFallback>
  <p>An error occurred</p>
  {/* No way out */}
</ErrorFallback>
```

✅ **Good:**
```typescript
<ErrorFallback>
  <p>An error occurred</p>
  <button onClick={resetError}>Try Again</button>
  <button onClick={() => navigate('/')}>Go Home</button>
  <button onClick={() => window.location.reload()}>Reload</button>
</ErrorFallback>
```

## Summary

**Key Patterns:**
- Use ErrorBoundary to isolate features
- Provide user-friendly fallback UI
- Track errors with context
- Use errorPolicy in GraphQL
- Implement retry with exponential backoff
- Use finally for cleanup
- Differentiate error types
- Provide resetError function
- Log errors comprehensively
- Test error boundaries

**Anti-Patterns to Avoid:**
- No error boundaries
- Exposing technical details
- Swallowing errors
- No recovery options
- Missing error context
- No retry logic
- Same handling for all errors
- Not testing error paths
