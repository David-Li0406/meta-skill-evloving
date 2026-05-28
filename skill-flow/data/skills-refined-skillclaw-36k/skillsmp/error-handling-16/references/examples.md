# Error Handling - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating error handling patterns.

## Example 1: ErrorBoundary Core Implementation

**File**: `libs/error-boundary/ErrorBoundary.tsx`

This is the complete ErrorBoundary component implementation that all features use.

```typescript
import type { Attributes } from '@opentelemetry/api';
import React, { Component } from 'react';
import RNRestart from 'react-native-restart';

import {
  SPAN_KEYS,
  type TracerUtilsResult,
  useTracer,
  SessionManager,
} from '@libs/tracing';

import { DefaultErrorFallback } from './fallback-ui/DefaultErrorFallback';

export type FallbackRender = (props: {
  error: Error;
  componentStack: string;
  resetError: () => void;
}) => React.ReactElement;

/**
 * Configuration object that defines the scope and context for error boundary reporting.
 */
export type ErrorBoundaryScope = {
  /** The name of the module or scope or component where the error boundary is placed */
  moduleName: string;
  /** Optional OpenTelemetry attributes for enhanced tracing and observability */
  attributes?: Attributes;
};

export type ErrorBoundaryProps = {
  scope: ErrorBoundaryScope;
  children?: React.ReactNode | (() => React.ReactNode);
  fallback?: React.ReactElement | FallbackRender;
  onError?: (error: Error, componentStack: string) => void;
  onMount?: () => void;
  onReset?: (error: Error | null, componentStack: string | null) => void;
  onUnmount?: (error: Error | null, componentStack: string | null) => void;
  beforeCapture?: (
    scope: ErrorBoundaryScope,
    error: Error | null,
    componentStack: string | null
  ) => void;
  tracer: TracerUtilsResult;
};

export type ErrorBoundaryState = {
  error: Error | null;
  componentStack: string | null;
};

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      error: null,
      componentStack: null,
    };
  }

  componentDidMount() {
    const { onMount } = this.props;
    if (onMount) {
      onMount();
    }
  }

  componentDidCatch(error: Error, info: { componentStack: string }) {
    const { scope, beforeCapture, onError } = this.props;
    const { startSpan } = this.props.tracer;

    // Do something before errors are captured
    if (beforeCapture) {
      beforeCapture(scope, error, info.componentStack);
    }

    // Catch errors in any components below and re-render with error message
    this.setState({
      error,
      componentStack: info.componentStack,
    });

    // Do something after errors are captured
    if (onError) {
      onError(error, info.componentStack);
    }

    const name = `ErrorBoundary ${scope.moduleName}`;
    // Log to Honeycomb
    const span = startSpan(SPAN_KEYS.ERROR_BOUNDARY, name, {
      attributes: {
        componentStack: info.componentStack,
        ...this.getAttributes(scope),
      },
    });
    span.recordException(error);
    span.end();
    SessionManager.getInstance().setSessionHasErrorBoundaryEvent();
  }

  getAttributes(scope: ErrorBoundaryScope): Attributes {
    const mergedAttributes = {
      ...scope.attributes,
    };

    // Append module name to attributes
    mergedAttributes['module.name'] = scope.moduleName;

    return mergedAttributes;
  }

  componentWillUnmount() {
    const { onUnmount } = this.props;
    const { error, componentStack } = this.state;

    if (onUnmount) {
      onUnmount(error, componentStack);
    }
  }

  resetError = () => {
    const { onReset } = this.props;
    const { error, componentStack } = this.state;

    // Reset the error back to null
    this.setState({
      error: null,
      componentStack: null,
    });

    // Do something after the error is reset
    if (onReset) {
      onReset(error, componentStack);
    }

    // Reload JS Bundle
    RNRestart.restart();
  };

  render() {
    const { children, fallback } = this.props;
    const { error, componentStack } = this.state;

    if (error && componentStack) {
      if (typeof fallback === 'function') {
        return fallback({ error, componentStack, resetError: this.resetError });
      }

      return (
        fallback || (
          <DefaultErrorFallback
            error={error}
            errorInfo={{ componentStack }}
            resetError={this.resetError}
          />
        )
      );
    }

    return typeof children === 'function' ? children() : children;
  }
}

type ErrorBoundaryRootProps = Omit<ErrorBoundaryProps, 'tracer'>;

export const ErrorBoundaryRoot = (props: ErrorBoundaryRootProps) => {
  const tracer = useTracer();

  return <ErrorBoundary {...props} tracer={tracer} />;
};
```

**Key patterns demonstrated:**
- Class component with `componentDidCatch` to catch React errors
- Creates OpenTelemetry span with scope context
- `span.recordException(error)` for distributed tracing
- Marks session with error flag via `SessionManager`
- Provides `resetError` that calls `RNRestart.restart()`
- Lifecycle callbacks: `onMount`, `beforeCapture`, `onError`, `onReset`, `onUnmount`
- Renders fallback UI or DefaultErrorFallback
- ErrorBoundaryRoot HOC injects tracer via hook

## Example 2: Screen-Level ErrorBoundary Usage

**File**: `entry-providers/providers.tsx`

This example shows top-level ErrorBoundary wrapping the entire app.

```typescript
import { QueryClientProvider } from '@tanstack/react-query';
import type { PropsWithChildren } from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { ErrorBoundary } from '@libs/error-boundary';
import { ApolloProviderWrapper } from '@libs/graphql/providers/ApolloProviderWrapper';
import { AppWithTranslation } from '@libs/localization';
import { queryClient } from '@libs/query';
import { ZestProvider } from '@libs/zest';

/**
 * ScreenEntryProvider provides essential context for full-screen components.
 */
export const ScreenEntryProvider: React.FC<PropsWithChildren> = ({
  children,
}) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ApolloProviderWrapper>
        <SafeAreaProvider>
          <AppWithTranslation>
            <ZestProvider>
              <ErrorBoundary scope={{ moduleName: 'App' }}>
                {children}
              </ErrorBoundary>
            </ZestProvider>
          </AppWithTranslation>
        </SafeAreaProvider>
      </ApolloProviderWrapper>
    </QueryClientProvider>
  );
};
```

**Key patterns demonstrated:**
- Top-level ErrorBoundary with `moduleName: 'App'`
- Catches errors that escape component-level boundaries
- Wraps entire provider tree
- Ensures app never shows blank white screen

## Example 3: Development vs Production Fallback UI

**File**: `libs/error-boundary/fallback-ui/DefaultErrorFallback.tsx`

This example shows conditional fallback UI based on environment.

```typescript
import type { ErrorInfo } from 'react';

import { DevErrorFallback } from './DevErrorFallback';
import { ProductionErrorFallback } from './ProductionErrorFallback';

interface DefaultErrorFallbackProps {
  error: Error;
  errorInfo: ErrorInfo | null;
  resetError: () => void;
}

/**
 * Renders the Default Error Boundary Fallback UI.
 * DEV ENV: This component is used to display the error message and stack trace
 * PROD ENV: This component is used to display a generic error message
 */
export const DefaultErrorFallback = ({
  error,
  errorInfo,
  resetError,
}: DefaultErrorFallbackProps) => {
  if (__DEV__) {
    return (
      <DevErrorFallback
        error={error}
        componentStack={`${errorInfo?.componentStack ?? ''}`.trim()}
        resetError={resetError}
      />
    );
  }

  return (
    <ProductionErrorFallback scope="default-error" resetError={resetError} />
  );
};
```

**Key patterns demonstrated:**
- `__DEV__` flag to detect development environment
- `DevErrorFallback` shows full error message and stack trace
- `ProductionErrorFallback` shows generic user-friendly message
- Both provide `resetError` action

## Example 4: OpenTelemetry Span with Exception Recording

**File**: `libs/networking-client/client/useFetch.ts`

This example shows complete OpenTelemetry integration with error handling for network requests.

```typescript
import { SpanKind, SpanStatusCode } from '@opentelemetry/api';
import {
  ATTR_HTTP_REQUEST_METHOD,
  ATTR_HTTP_RESPONSE_STATUS_CODE,
  ATTR_URL_FULL,
} from '@opentelemetry/semantic-conventions';

import { useNetworkTracer, SPAN_KEYS } from '@libs/tracing';

import { isFetchError } from './errors';
import { fetchClient } from './fetchClient';

export const useFetch = (baseUrl?: string): FetchFunction<Response> => {
  const { startSpan } = useNetworkTracer();

  return useCallback(
    async (
      path: string,
      queryKey: QueryKey,
      options: RequestOptions = {},
      authRequestOptions: AuthRequestOptions = {},
      requestID?: string
    ): Promise<Response> => {
      const name = baseUrl
        ? 'CustomFetch'
        : `${options.method ?? 'GET'} ${requestID}`;
      const span = startSpan(SPAN_KEYS.FETCH, name, {
        kind: SpanKind.CLIENT,
      });

      try {
        const headers = {
          'X-Request-Id': uuid.v4(),
          'User-Agent': getUserAgent(),
          ...options.headers,
        };

        const url = actualBaseUrl + path + `?${queryString}`;

        span.setAttributes({
          [ATTR_HTTP_REQUEST_METHOD]: options.method ?? 'GET',
          [ATTR_URL_FULL]: url,
          'fetch.query_key': JSON.stringify(queryKey),
        });

        const response = await fetchClient(
          path,
          queryKey,
          { ...options, headers },
          authRequestOptions,
          requestID
        );

        setResponseAttributes(span, response);

        return response;
      } catch (error) {
        if (isFetchError(error)) {
          if (error.response) {
            setResponseAttributes(span, error.response);
          } else {
            // API call timed out
            span.setAttribute(
              'availability-error-type',
              'backend-service-timeout'
            );
          }
        }
        span.recordException(error as Error);
        span.setStatus({
          code: SpanStatusCode.ERROR,
          message: (error as Error).message,
        });

        throw error;
      } finally {
        span.end();
      }
    },
    [baseUrl, startSpan]
  );
};

const setResponseAttributes = (span: Span, response: Response) => {
  span.setAttributes({
    [ATTR_HTTP_RESPONSE_STATUS_CODE]: response.status,
    'http.response.status_text': response.statusText,
    'fetch.ok': response.ok,
  });

  if (response.status >= 500) {
    span.setAttribute('availability-error-type', 'backend-service-error');
  }
};
```

**Key patterns demonstrated:**
- `startSpan()` with `SpanKind.CLIENT` for network requests
- Request attributes set before operation
- Response attributes set after success
- `span.recordException()` for error tracking
- `span.setStatus()` with ERROR code
- Special handling for timeout vs response errors
- `span.end()` in finally block (CRITICAL)
- useCallback with dependencies

## Example 5: GraphQL Tracing Link

**File**: `libs/graphql/links/tracing.ts`

This example shows automatic OpenTelemetry tracing for all GraphQL operations.

```typescript
import { ApolloLink } from '@apollo/client';
import type { FetchResult, Operation } from '@apollo/client';
import { Observable } from '@apollo/client/utilities';
import { SpanKind, SpanStatusCode } from '@opentelemetry/api';
import {
  ATTR_HTTP_REQUEST_METHOD,
  ATTR_URL_FULL,
} from '@opentelemetry/semantic-conventions';

import { getTracer, SPAN_KEYS } from '@libs/tracing';

/**
 * Sanitizes variables to remove sensitive data before recording in spans
 */
const sanitizeVariables = (
  variables: Record<string, unknown> | undefined
): Record<string, unknown> | undefined => {
  if (!variables) {
    return undefined;
  }

  const sanitized = { ...variables };
  const sensitiveKeys = ['password', 'token', 'secret', 'authorization'];

  Object.keys(sanitized).forEach((key) => {
    if (
      sensitiveKeys.some((sensitive) => key.toLowerCase().includes(sensitive))
    ) {
      sanitized[key] = '[REDACTED]';
    }
  });

  return sanitized;
};

/**
 * Apollo Link that adds OpenTelemetry tracing to GraphQL operations
 */
export const tracingLink = new ApolloLink((operation: Operation, forward) => {
  const { startSpan } = getTracer();

  // Extract operation details
  const operationName = operation.operationName || 'unknown';
  const operationType =
    operation.query.definitions[0]?.kind === 'OperationDefinition'
      ? operation.query.definitions[0].operation
      : 'unknown';

  const context = operation.getContext();
  const uri = typeof context?.uri === 'string' ? context.uri : '';
  const method = (
    typeof context?.fetchOptions?.method === 'string'
      ? context.fetchOptions.method
      : 'POST'
  ).toUpperCase();

  // Create span name: "QUERY GetStoreInitialData"
  const spanName = `${operationType.toUpperCase()} ${operationName}`;

  const span = startSpan(SPAN_KEYS.GRAPHQL_OPERATION, spanName, {
    kind: SpanKind.CLIENT,
  });

  const requestAttributes = {
    [ATTR_HTTP_REQUEST_METHOD]: method,
    [ATTR_URL_FULL]: uri,
    'graphql.operation.type': operationType,
    'graphql.operation.name': operationName,
    'graphql.variables': JSON.stringify(sanitizeVariables(operation.variables)),
  };

  span.setAttributes(requestAttributes);

  // Forward the operation and handle the response
  return new Observable<FetchResult>((observer) => {
    const subscription = forward(operation).subscribe({
      next: (result) => {
        const nextContext = operation.getContext();
        const maybeResponse = nextContext?.response;

        if (isResponseLike(maybeResponse)) {
          setResponseAttributes(span, maybeResponse);
        }

        if (result.errors && result.errors.length > 0) {
          span.setAttributes({
            'graphql.errors.count': result.errors.length,
            'graphql.errors.messages': JSON.stringify(
              result.errors.map((error) => error.message)
            ),
          });
          span.setStatus({
            code: SpanStatusCode.ERROR,
            message: `GraphQL operation returned ${result.errors.length} error(s)`,
          });
        } else {
          span.setStatus({ code: SpanStatusCode.OK });
        }

        span.setAttributes({
          'graphql.response.has_data': !!result.data,
          'graphql.response.has_errors': !!(
            result.errors && result.errors.length > 0
          ),
        });

        observer.next(result);
      },
      error: (error) => {
        const errorContext = operation.getContext();
        const maybeResponse = errorContext?.response;
        if (isResponseLike(maybeResponse)) {
          setResponseAttributes(span, maybeResponse);
        } else {
          span.setAttribute(
            'availability-error-type',
            'backend-service-timeout'
          );
        }

        span.recordException(error);
        span.setStatus({
          code: SpanStatusCode.ERROR,
          message: error.message || 'GraphQL operation failed',
        });

        span.end();
        observer.error(error);
      },
      complete: () => {
        span.end();
        observer.complete();
      },
    });

    return () => {
      subscription.unsubscribe();
    };
  });
});
```

**Key patterns demonstrated:**
- ApolloLink for automatic GraphQL tracing
- Span name: `QUERY OperationName` or `MUTATION OperationName`
- Sanitizes sensitive variables (password, token, secret)
- Records GraphQL errors with count and messages
- Sets span status based on errors vs success
- Handles network errors vs GraphQL errors
- Always ends span in complete/error handlers
- Observable pattern for async operations

## Example 6: GraphQL errorPolicy Usage

**File**: `data-access/graphql/product-details/queries.ts`

This example shows using `errorPolicy: 'all'` for graceful degradation.

```typescript
import type { QueryHookOptions } from '@apollo/client';
import { useQuery } from '@apollo/client';

import type {
  GetShoppableProductDetailsQuery,
  GetShoppableProductDetailsQueryVariables,
} from '@data-access/graphql';
import {
  GetShoppableProductDetailsDocument,
} from '@data-access/graphql';

export const useGetShoppableProductDetailsQuery = (
  options: QueryHookOptions<
    GetShoppableProductDetailsQuery,
    GetShoppableProductDetailsQueryVariables
  >
) => {
  return useQuery(GetShoppableProductDetailsDocument, {
    ...options,
    errorPolicy: 'ignore', // Ignore errors, return data only
    fetchPolicy: 'cache-and-network',
    notifyOnNetworkStatusChange: false,
  });
};
```

**Key patterns demonstrated:**
- `errorPolicy: 'ignore'` silently ignores GraphQL errors
- `fetchPolicy: 'cache-and-network'` ensures fresh data
- `notifyOnNetworkStatusChange: false` prevents re-renders
- Use `errorPolicy: 'all'` for most cases (partial data + errors)

**Alternative pattern (recommended):**
```typescript
useQuery(GetProductDetailsDocument, {
  errorPolicy: 'all', // Return partial data + errors
});
```

## Example 7: Testing ErrorBoundary

**File**: `libs/error-boundary/ErrorBoundary.test.tsx`

This example shows comprehensive ErrorBoundary testing.

```typescript
import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';
import { render, screen } from '@testing-library/react-native';
import { useEffect } from 'react';

import { mockTracerProvider } from 'jest-utils';

import { Text } from '@zest/react-native';

import type { ErrorBoundaryProps } from './ErrorBoundary';
import { ErrorBoundaryRoot } from './ErrorBoundary';

jest.mock('react-native-restart', () => ({
  restart: jest.fn(),
}));

describe('ErrorBoundary', () => {
  const mockSpanExporter = mockTracerProvider();
  const mockScope = { moduleName: 'TestModule' };

  beforeEach(() => {
    jest.clearAllMocks();
    mockSpanExporter.reset();
  });

  const ThrowError = () => {
    useEffect(() => {
      throw new Error('Test Error');
    });

    return null;
  };

  it('should render children when no error occurs', () => {
    render(
      <ErrorBoundaryRoot scope={mockScope}>
        <Text>Test Child</Text>
      </ErrorBoundaryRoot>
    );
    expect(screen.getByText('Test Child')).toBeTruthy();
  });

  it('should render fallback UI when an error occurs', () => {
    render(
      <ErrorBoundaryRoot scope={mockScope}>
        <ThrowError />
      </ErrorBoundaryRoot>
    );

    expect(screen.getByTestId('error-boundary')).toBeTruthy();
  });

  it('should call onError when an error occurs', () => {
    const onError = jest.fn();

    render(
      <ErrorBoundaryRoot scope={mockScope} onError={onError}>
        <ThrowError />
      </ErrorBoundaryRoot>
    );

    expect(onError).toHaveBeenCalledWith(expect.any(Error), expect.any(String));
  });

  it('should call beforeCapture before capturing an error', () => {
    const beforeCapture = jest.fn();
    render(
      <ErrorBoundaryRoot scope={mockScope} beforeCapture={beforeCapture}>
        <ThrowError />
      </ErrorBoundaryRoot>
    );

    expect(beforeCapture).toHaveBeenCalledWith(
      mockScope,
      expect.any(Error),
      expect.any(String)
    );
  });

  describe('OTEL Tracing', () => {
    it('should create a span when an error occurs', () => {
      render(
        <ErrorBoundaryRoot scope={mockScope}>
          <ThrowError />
        </ErrorBoundaryRoot>
      );

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(1);
      const span = spans[0] as ReadableSpan;
      expect(span.name).toBe('ErrorBoundary TestModule');
      expect(span.attributes).toEqual(
        expect.objectContaining({
          componentStack: expect.any(String),
          'module.name': 'TestModule',
          'span.key': 'error_boundary',
        })
      );
    });

    it('should include custom attributes in span', () => {
      const customScope = {
        moduleName: 'CustomModule',
        attributes: {
          customAttribute: 'customValue',
          userId: '12345',
        },
      };

      render(
        <ErrorBoundaryRoot scope={customScope}>
          <ThrowError />
        </ErrorBoundaryRoot>
      );

      const spans = mockSpanExporter.getFinishedSpans();
      const span = spans[0] as ReadableSpan;
      expect(span.attributes).toEqual(
        expect.objectContaining({
          'module.name': 'CustomModule',
          customAttribute: 'customValue',
          userId: '12345',
        })
      );
    });
  });
});
```

**Key patterns demonstrated:**
- Mock `react-native-restart` to prevent actual app restart
- `mockTracerProvider()` for OTEL span testing
- `ThrowError` component with `useEffect` to trigger `componentDidCatch`
- Verify fallback UI is rendered
- Verify lifecycle callbacks are called
- Verify OTEL span is created with correct attributes
- `expect.objectContaining()` for partial attribute matching
- Test custom attributes are included in span

## Summary

The YourCompany codebase consistently follows these error handling patterns:

1. **ErrorBoundary components** isolate errors per feature
2. **OpenTelemetry integration** with `span.recordException()` and `span.end()` in finally
3. **RNRestart.restart()** for error recovery after user action
4. **Lifecycle callbacks** for custom error handling and analytics
5. **GraphQL errorPolicy** configuration for partial data rendering
6. **Automatic tracing** via ApolloLink for GraphQL operations
7. **Development vs production fallbacks** for appropriate error display
8. **Comprehensive testing** with mocked trackers and error components
9. **Scope context** with moduleName and attributes for debugging
10. **User-friendly messages** in production, technical details in development

These patterns ensure robust error handling with graceful degradation, comprehensive tracing, and excellent debugging capabilities throughout the app.
