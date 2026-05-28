---
name: error-handling
description: "WHAT: Error boundaries with fallback UI and OpenTelemetry span recording. WHEN: isolating component errors, handling GraphQL failures, implementing retry logic. KEYWORDS: ErrorBoundary, error handling, fallback UI, OpenTelemetry, recordException, retry, GraphQL, errorPolicy, scope."
---

# Error Handling & Recovery Patterns

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns


## Core Principles

**Use ErrorBoundary components to isolate errors and prevent app crashes.** Integrate OpenTelemetry spans to track errors in distributed tracing and provide user-friendly fallback UI with recovery actions.

**Why**: Proper error handling prevents entire app crashes, improves user experience with actionable error messages, and enables debugging production issues through distributed tracing.

## When to Use This Skill

Use these patterns when:

- Wrapping feature components to isolate errors
- Integrating error tracking with OpenTelemetry
- Creating fallback UI for error states
- Handling GraphQL query/mutation errors
- Implementing retry logic for transient failures
- Testing error boundaries and error handling paths
- Tracking errors in production with distributed tracing

## ErrorBoundary Component

### Component-Level Boundaries

Wrap features with ErrorBoundary to isolate errors and prevent app-wide crashes:

```typescript
import { ErrorBoundary } from '@libs/error-boundary';

export const RecipeListScreen = () => {
  return (
    <ErrorBoundary
      scope={{
        moduleName: 'RecipeList',
        attributes: {
          squad: 'cookbook',
          feature: 'recipe-list',
        },
      }}
      fallback={(error, componentStack, resetError) => (
        <ErrorFallback error={error} onRetry={resetError} />
      )}
    >
      <RecipeListContent />
    </ErrorBoundary>
  );
};
```

**Key patterns:**
- `scope.moduleName`: Identifies where error occurred (required)
- `scope.attributes`: Additional context for debugging (optional)
- `fallback`: Custom error UI with retry functionality
- Automatic OpenTelemetry span creation with `recordException()`

**Why**: Component-level boundaries prevent one failing component from crashing the entire app. Errors are isolated, logged to OpenTelemetry, and users see helpful recovery UI.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/comms/screens/inbox/InboxScreen.tsx:1`

### Screen-Level Boundaries

Wrap entire app or navigation stacks with top-level ErrorBoundary:

```typescript
import { ErrorBoundary } from '@libs/error-boundary';

export const ScreenEntryProvider: React.FC<PropsWithChildren> = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ApolloProvider client={apolloClient}>
        <SafeAreaProvider>
          <AppWithTranslation>
            <ZestProvider>
              <ErrorBoundary scope={{ moduleName: 'App' }}>
                {children}
              </ErrorBoundary>
            </ZestProvider>
          </AppWithTranslation>
        </SafeAreaProvider>
      </ApolloProvider>
    </QueryClientProvider>
  );
};
```

**Why**: Top-level boundaries catch errors that escape component boundaries, ensuring the app never shows a blank white screen.

**Production Example**: `git-resources/shared-mobile-modules/src/entry-providers/providers.tsx:140`

### Error Scope Configuration

Always provide scope information for debugging:

```typescript
<ErrorBoundary
  scope={{
    moduleName: 'Checkout',
    attributes: {
      screenName: 'PaymentScreen',
      feature: 'payment-processing',
      userId: user.id,
      cartId: cart.id,
      squad: 'conversions',
    },
  }}
  onError={(error, componentStack) => {
    // Optional: Custom error handling
    logError(error, { moduleName: 'Checkout', componentStack });
  }}
>
  <PaymentForm />
</ErrorBoundary>
```

**Key patterns:**
- `moduleName`: Required identifier (e.g., 'Checkout', 'RecipeList')
- `attributes`: OpenTelemetry attributes for filtering/grouping errors
- `onError`: Optional callback for custom error handling

**Why**: Rich scope data helps identify error sources in production logs and enables filtering errors by team, feature, or screen.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/error-boundary/ErrorBoundary.tsx:76`

## OpenTelemetry Integration

### Span Recording with Exceptions

Always use try-catch-finally pattern with spans:

```typescript
import { useTracer } from '@libs/observability';
import { SpanStatusCode } from '@opentelemetry/api';

export const useCheckoutFlow = () => {
  const { startSpan } = useTracer();

  const processPayment = async (paymentData: PaymentData) => {
    const span = startSpan('checkout.processPayment', {
      attributes: {
        'payment.method': paymentData.method,
        'cart.total': paymentData.total,
        'payment.currency': paymentData.currency,
      },
    });

    try {
      const result = await paymentService.process(paymentData);
      span.setStatus({ code: SpanStatusCode.OK });
      span.setAttributes({
        'payment.transaction_id': result.transactionId,
        'payment.status': 'success',
      });
      return result;
    } catch (error) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: (error as Error).message,
      });
      span.recordException(error as Error);
      span.setAttributes({
        'payment.status': 'failed',
        'error.type': (error as Error).name,
      });
      throw error; // Re-throw for caller to handle
    } finally {
      span.end(); // ALWAYS end span
    }
  };

  return { processPayment };
};
```

**Key patterns:**
- `startSpan()` with descriptive name (`checkout.processPayment`)
- `setStatus()` with OK or ERROR
- `recordException()` for detailed error tracking
- `span.end()` in finally block (CRITICAL)
- Attributes for request context and results

**Why**: Distributed tracing enables debugging complex async flows in production. Always ending spans in finally blocks prevents memory leaks.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/networking-client/client/useFetch.ts:89`

### Automatic GraphQL Tracing

GraphQL operations automatically create spans via tracingLink:

```typescript
// Automatic instrumentation in Apollo Client setup
import { tracingLink } from '@libs/graphql/links/tracing';

const apolloClient = new ApolloClient({
  link: ApolloLink.from([
    tracingLink, // Automatically creates spans for all GraphQL operations
    httpLink,
  ]),
  cache: inMemoryCache,
});
```

**How tracingLink works:**
- Creates span for each GraphQL operation: `QUERY GetRecipes`, `MUTATION CreateOrder`
- Adds operation type, name, variables (sanitized)
- Records GraphQL errors with `recordException()`
- Sets span attributes: response status, error count, error messages
- Automatically ends span on completion

**Why**: Consistent telemetry for all GraphQL operations without manual instrumentation. Errors are automatically tracked in OpenTelemetry.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/graphql/links/tracing.ts:115`

## Fallback UI Patterns

### User-Friendly Error Messages

Provide clear, actionable error messages based on error type:

```typescript
export const ErrorFallback = ({ error, onRetry }: ErrorFallbackProps) => {
  const styles = useZestStyles(stylesConfig);

  // Network errors
  if (error.networkError || error.message.includes('Network request failed')) {
    return (
      <View style={styles.container}>
        <Icon icon="WifiOff24" />
        <Text type="headline-md">No Internet Connection</Text>
        <Text type="body-md">Please check your connection and try again.</Text>
        <Button onPress={onRetry}>Retry</Button>
      </View>
    );
  }

  // Authentication errors
  if (error.message.includes('unauthorized') || error.message.includes('401')) {
    return (
      <View style={styles.container}>
        <Icon icon="LockOutline24" />
        <Text type="headline-md">Session Expired</Text>
        <Text type="body-md">Your session has expired. Please sign in again.</Text>
        <Button onPress={handleReauth}>Sign In Again</Button>
      </View>
    );
  }

  // Generic errors
  return (
    <View style={styles.container}>
      <Icon icon="ErrorOutline24" />
      <Text type="headline-md">Something Went Wrong</Text>
      <Text type="body-md">We encountered an unexpected error.</Text>
      <Button onPress={onRetry}>Try Again</Button>
    </View>
  );
};
```

**Key patterns:**
- Detect error type from error properties or message
- Show appropriate icon and message for each error type
- Always provide action (Retry, Sign In Again)
- Never show technical stack traces to users

**Why**: User-friendly messages improve UX and guide users toward recovery actions. Technical errors confuse non-technical users.

### Development vs Production Fallbacks

Show different UI in development vs production:

```typescript
export const DefaultErrorFallback = ({
  error,
  errorInfo,
  resetError,
}: DefaultErrorFallbackProps) => {
  if (__DEV__) {
    return (
      <DevErrorFallback
        error={error}
        componentStack={errorInfo?.componentStack ?? ''}
        resetError={resetError}
      />
    );
  }

  return (
    <ProductionErrorFallback scope="default-error" resetError={resetError} />
  );
};
```

**Development fallback:**
- Shows full error message and stack trace
- Displays component stack for debugging
- Helpful for developers during development

**Production fallback:**
- Shows generic user-friendly message
- Hides technical details
- Provides retry action

**Why**: Developers need detailed error info for debugging. Users need simple, actionable messages without technical jargon.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/error-boundary/fallback-ui/DefaultErrorFallback.tsx:1`

## GraphQL Error Handling

### Error Policy Configuration

Use `errorPolicy` to control how GraphQL errors are handled:

```typescript
export const useGetProductDetails = (productId: string) => {
  const { data, loading, error } = useQuery(GetProductDetailsDocument, {
    variables: { productId },
    errorPolicy: 'all', // Return partial data + errors
  });

  const hasErrors = error?.graphQLErrors.length > 0;
  const hasNetworkError = error?.networkError != null;

  return {
    product: data?.product || null,
    loading: loading && !data,
    hasErrors,
    hasNetworkError,
  };
};
```

**ErrorPolicy options:**
- `none` (default): Throw on any GraphQL error, no data returned
- `ignore`: Ignore errors entirely, return data only
- `all`: Return partial data + errors (RECOMMENDED)

**Why**: `errorPolicy: 'all'` enables graceful degradation. Show partial data when available instead of blank error screen.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/product-details/queries.ts:26`

### Error Type Discrimination

Handle different GraphQL error types appropriately:

```typescript
export const handleGraphQLError = (error: ApolloError) => {
  // Authentication errors (401)
  const authError = error.graphQLErrors.find(
    (err) => err.extensions?.code === 'UNAUTHENTICATED'
  );
  if (authError) {
    return {
      type: 'auth' as const,
      message: 'Please sign in again',
      action: 'reauth',
    };
  }

  // Validation errors (400)
  const validationError = error.graphQLErrors.find(
    (err) => err.extensions?.code === 'BAD_USER_INPUT'
  );
  if (validationError) {
    return {
      type: 'validation' as const,
      message: validationError.message,
      fields: validationError.extensions?.fields as Record<string, string>,
    };
  }

  // Network errors (no response)
  if (error.networkError) {
    return {
      type: 'network' as const,
      message: 'Connection failed. Please check your internet.',
      action: 'retry',
    };
  }

  // Generic errors
  return {
    type: 'unknown' as const,
    message: 'Something went wrong. Please try again.',
    action: 'retry',
  };
};
```

**Key error types:**
- `UNAUTHENTICATED`: Session expired, need re-auth
- `BAD_USER_INPUT`: Validation errors with field details
- `networkError`: Connection failures
- Generic: Unknown server errors

**Why**: Specific error handling enables appropriate user feedback and recovery actions.

## Retry Strategies

### TanStack Query Retry Configuration

Configure automatic retry for transient errors:

```typescript
export const useLoadRecipes = () => {
  const { data, error, refetch, isRefetching } = useQuery({
    queryKey: ['recipes'],
    queryFn: fetchRecipes,
    retry: 3, // Retry 3 times
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000), // Exponential backoff
  });

  return {
    recipes: data ?? [],
    error,
    refetch,
    isRefetching,
  };
};
```

**Retry patterns:**
- `retry: 3`: Retry up to 3 times
- `retryDelay`: Exponential backoff (1s, 2s, 4s, max 30s)
- Automatic for temporary network failures
- No retry for 4xx errors (client errors)

**Why**: Automatic retry handles temporary network issues without user intervention. Exponential backoff prevents overwhelming servers.

### Manual Retry Hook

Provide manual retry for user-initiated actions:

```typescript
export const useManualRetry = (onRetry: () => Promise<void>) => {
  const [isRetrying, setIsRetrying] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

  const retry = useCallback(async () => {
    setIsRetrying(true);
    setRetryCount((prev) => prev + 1);

    try {
      await onRetry();
    } catch (error) {
      console.error('Retry failed:', error);
    } finally {
      setIsRetrying(false);
    }
  }, [onRetry]);

  return { retry, isRetrying, retryCount };
};

// Usage
const ErrorScreen = ({ error, refetch }) => {
  const { retry, isRetrying } = useManualRetry(refetch);

  return (
    <View>
      <Text>Error: {error.message}</Text>
      <Button onPress={retry} loading={isRetrying}>
        Retry
      </Button>
    </View>
  );
};
```

**Why**: Users can manually retry after fixing issues (e.g., enabling wifi). Visual loading state shows retry in progress.

## Error Boundary Lifecycle

### Lifecycle Callbacks

Use lifecycle callbacks for custom error handling:

```typescript
<ErrorBoundary
  scope={{ moduleName: 'Checkout' }}
  onMount={() => {
    // Component mounted successfully
    console.log('Checkout error boundary mounted');
  }}
  beforeCapture={(scope, error, componentStack) => {
    // Before error is captured
    console.log('About to capture error in:', scope.moduleName);
  }}
  onError={(error, componentStack) => {
    // After error is captured
    logErrorToAnalytics(error, { moduleName: 'Checkout' });
  }}
  onReset={(error, componentStack) => {
    // After error is reset (before app restart)
    console.log('Resetting error boundary');
  }}
  onUnmount={(error, componentStack) => {
    // Component unmounting
    if (error) {
      console.log('Unmounting with active error');
    }
  }}
>
  <CheckoutFlow />
</ErrorBoundary>
```

**Lifecycle order:**
1. `onMount()` - Component mounted
2. Error occurs in children
3. `beforeCapture()` - Before capturing error
4. Error state set
5. `onError()` - After error captured
6. User clicks retry
7. `onReset()` - Before app restart
8. `RNRestart.restart()` - App restarts

**Why**: Lifecycle callbacks enable analytics tracking, custom logging, and cleanup before app restart.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/error-boundary/ErrorBoundary.tsx:60`

### Reset Error Strategy

ErrorBoundary provides `resetError` that restarts the app:

```typescript
const resetError = () => {
  // Reset error state
  this.setState({
    error: null,
    componentStack: null,
  });

  // Call onReset callback
  if (onReset) {
    onReset(error, componentStack);
  }

  // Reload JS Bundle
  RNRestart.restart();
};
```

**Why**: `RNRestart.restart()` ensures a clean slate after errors. State is cleared and app reloads.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/error-boundary/ErrorBoundary.tsx:130`

## Testing Error Handling

### Test Error Boundaries

Verify ErrorBoundary catches errors and shows fallback:

```typescript
import { render, screen } from '@testing-library/react-native';
import { useEffect } from 'react';

const ThrowError = ({ shouldThrow = true }) => {
  useEffect(() => {
    if (shouldThrow) {
      throw new Error('Test error');
    }
  }, [shouldThrow]);

  return null;
};

describe('ErrorBoundary', () => {
  it('renders fallback when error occurs', () => {
    render(
      <ErrorBoundary
        scope={{ moduleName: 'Test' }}
        fallback={(error) => <Text>Error: {error.message}</Text>}
      >
        <ThrowError />
      </ErrorBoundary>
    );

    expect(screen.getByText('Error: Test error')).toBeTruthy();
  });

  it('calls onError callback', () => {
    const onError = jest.fn();

    render(
      <ErrorBoundary scope={{ moduleName: 'Test' }} onError={onError}>
        <ThrowError />
      </ErrorBoundary>
    );

    expect(onError).toHaveBeenCalledWith(
      expect.objectContaining({ message: 'Test error' }),
      expect.any(String) // componentStack
    );
  });
});
```

**Key patterns:**
- Use `useEffect` to throw errors (componentDidCatch catches lifecycle errors)
- Verify fallback UI is rendered
- Verify `onError` callback is called with error and componentStack

**Why**: Testing ensures error boundaries work correctly and capture all error details.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/error-boundary/ErrorBoundary.test.tsx:1`

### Test OpenTelemetry Spans

Verify spans are created with correct attributes:

```typescript
import { mockTracerProvider } from 'jest-utils';

describe('ErrorBoundary OTEL Tracing', () => {
  const mockSpanExporter = mockTracerProvider();

  beforeEach(() => {
    mockSpanExporter.reset();
  });

  it('creates span when error occurs', () => {
    render(
      <ErrorBoundary
        scope={{
          moduleName: 'TestModule',
          attributes: {
            feature: 'checkout',
            userId: '123',
          },
        }}
      >
        <ThrowError />
      </ErrorBoundary>
    );

    const spans = mockSpanExporter.getFinishedSpans();
    expect(spans.length).toBe(1);

    const span = spans[0];
    expect(span.name).toBe('ErrorBoundary TestModule');
    expect(span.attributes).toEqual(
      expect.objectContaining({
        'module.name': 'TestModule',
        feature: 'checkout',
        userId: '123',
        componentStack: expect.any(String),
      })
    );
  });
});
```

**Why**: Testing OTEL integration ensures errors are properly tracked in distributed tracing.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/error-boundary/ErrorBoundary.test.tsx:92`

### Test Retry Logic

Verify retry behavior with mock failures:

```typescript
test('retries failed queries with exponential backoff', async () => {
  const mockFetch = jest
    .fn()
    .mockRejectedValueOnce(new Error('Network error'))
    .mockRejectedValueOnce(new Error('Network error'))
    .mockResolvedValueOnce({ data: mockRecipes });

  const { result } = renderHook(() =>
    useQuery({
      queryKey: ['recipes'],
      queryFn: mockFetch,
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    })
  );

  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(mockFetch).toHaveBeenCalledTimes(3); // 2 failures + 1 success
  expect(result.current.data).toEqual({ data: mockRecipes });
});
```

**Why**: Testing retry logic prevents infinite loops and validates backoff strategy.

## Common Mistakes to Avoid

❌ **Don't forget to end spans**:

```typescript
// ❌ Missing span.end() - memory leak
const span = tracer.startSpan('operation');
await doSomething();
// Forgot span.end()

// ✅ Always end span in finally block
const span = tracer.startSpan('operation');
try {
  await doSomething();
} catch (error) {
  span.recordException(error);
  throw error;
} finally {
  span.end(); // CRITICAL
}
```

❌ **Don't show technical errors to users**:

```typescript
// ❌ Technical stack trace confuses users
<Text>{error.stack}</Text>

// ✅ User-friendly message
<Text>Something went wrong. Please try again.</Text>
```

❌ **Don't swallow errors without logging**:

```typescript
// ❌ Silent failure - no logging
try {
  await fetchData();
} catch (error) {
  // Silent failure
}

// ✅ Log errors with context
try {
  await fetchData();
} catch (error) {
  logError(error, { moduleName: 'DataFetcher', operation: 'fetchData' });
  throw error; // Re-throw if caller needs to handle
}
```

❌ **Don't use errorPolicy: 'ignore' blindly**:

```typescript
// ❌ Ignoring all errors silently
useQuery(GetDataDocument, {
  errorPolicy: 'ignore', // Errors disappear
});

// ✅ Use 'all' to get partial data + errors
useQuery(GetDataDocument, {
  errorPolicy: 'all', // Partial data + errors
});
```

✅ **Do provide scope context for errors**:

```typescript
// ✅ Rich context for debugging
<ErrorBoundary
  scope={{
    moduleName: 'Checkout',
    attributes: {
      feature: 'payment',
      squad: 'conversions',
      userId: user.id,
    },
  }}
>
  <CheckoutFlow />
</ErrorBoundary>
```

✅ **Do use component-level boundaries**:

```typescript
// ✅ Isolate errors per feature
<ErrorBoundary scope={{ moduleName: 'RecipeList' }}>
  <RecipeList />
</ErrorBoundary>

<ErrorBoundary scope={{ moduleName: 'Cart' }}>
  <Cart />
</ErrorBoundary>
```

✅ **Do provide retry actions**:

```typescript
// ✅ User can retry after fixing issue
<ErrorFallback
  error={error}
  onRetry={() => {
    refetch();
  }}
/>
```

## Performance Considerations

### Avoid Creating Too Many Spans

Don't create spans for every small operation:

```typescript
// ❌ Too many spans - performance overhead
items.forEach((item) => {
  const span = tracer.startSpan(`process-${item.id}`);
  processItem(item);
  span.end();
});

// ✅ Single span for batch operation
const span = tracer.startSpan('process-items', {
  attributes: {
    'items.count': items.length,
  },
});
try {
  items.forEach(processItem);
  span.setStatus({ code: SpanStatusCode.OK });
} finally {
  span.end();
}
```

**Why**: Too many spans impact performance and create noise in traces. Group related operations.

## Quick Reference

**ErrorBoundary Pattern:**
```typescript
<ErrorBoundary
  scope={{
    moduleName: 'FeatureName',
    attributes: { squad: 'team', feature: 'name' },
  }}
  fallback={(error, componentStack, resetError) => (
    <ErrorFallback error={error} onRetry={resetError} />
  )}
  onError={(error, componentStack) => {
    logError(error, { moduleName: 'FeatureName' });
  }}
>
  <FeatureComponent />
</ErrorBoundary>
```

**OpenTelemetry Span Pattern:**
```typescript
const span = startSpan('operation.name', { attributes: { /* context */ } });
try {
  const result = await operation();
  span.setStatus({ code: SpanStatusCode.OK });
  return result;
} catch (error) {
  span.recordException(error);
  span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
  throw error;
} finally {
  span.end(); // ALWAYS
}
```

**GraphQL Error Handling:**
```typescript
useQuery(Document, {
  errorPolicy: 'all', // Partial data + errors
});
```

**Retry Configuration:**
```typescript
useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  retry: 3,
  retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
});
```

**Key Libraries:**
- React Native 0.75.4
- @opentelemetry/api 2.0.1
- @apollo/client 3.13.6
- @tanstack/react-query 5.59.16
- react-native-restart (for ErrorBoundary reset)

For production examples, see [references/examples.md](references/examples.md).
