# OpenTelemetry JavaScript API Reference

**Version**: 2.0.1

## Official Documentation

- **API**: https://opentelemetry.io/docs/languages/js/api/
- **SDK**: https://opentelemetry.io/docs/languages/js/instrumentation/
- **Tracing**: https://opentelemetry.io/docs/concepts/signals/traces/

## Core API

### Tracer

Get tracer instance for creating spans.

```typescript
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('my-service', '1.0.0');
```

### Span

Represent a unit of work or operation.

```typescript
const span = tracer.startSpan('operation-name', {
  attributes: {
    'user.id': userId,
    'operation.type': 'read',
  },
  kind: SpanKind.CLIENT,
});

// Do work

span.end();
```

**Span Methods**:
- `setAttribute(key, value)` - Add single attribute
- `setAttributes(attributes)` - Add multiple attributes
- `addEvent(name, attributes?)` - Add event to span
- `setStatus({ code, message? })` - Set span status
- `recordException(exception)` - Record exception
- `updateName(name)` - Update span name
- `end(endTime?)` - End span
- `isRecording()` - Check if span is recording

### SpanKind

```typescript
import { SpanKind } from '@opentelemetry/api';

SpanKind.INTERNAL;  // Default, internal operation
SpanKind.SERVER;    // Server-side request handler
SpanKind.CLIENT;    // Client-side request
SpanKind.PRODUCER;  // Message producer
SpanKind.CONSUMER;  // Message consumer
```

### SpanStatusCode

```typescript
import { SpanStatusCode } from '@opentelemetry/api';

span.setStatus({ code: SpanStatusCode.OK });
span.setStatus({ code: SpanStatusCode.ERROR, message: 'Failed' });
span.setStatus({ code: SpanStatusCode.UNSET }); // Default
```

## Context Management

### Active Context

```typescript
import { context, trace } from '@opentelemetry/api';

// Get active span
const activeSpan = trace.getActiveSpan();

// Set active span
context.with(trace.setSpan(context.active(), span), () => {
  // Code here has `span` as active span
});
```

### Context Propagation

```typescript
// Extract context from carrier
const ctx = propagation.extract(context.active(), carrier);

// Inject context into carrier
propagation.inject(context.active(), carrier);
```

## Span Creation Patterns

### Start Active Span

Most common pattern - automatically sets span as active.

```typescript
tracer.startActiveSpan('operation', (span) => {
  try {
    // Do work
    span.setAttribute('result', 'success');
  } catch (error) {
    span.recordException(error);
    span.setStatus({ code: SpanStatusCode.ERROR });
  } finally {
    span.end();
  }
});

// Async version
await tracer.startActiveSpan('async-operation', async (span) => {
  try {
    const result = await fetchData();
    span.setAttribute('result.count', result.length);
    return result;
  } catch (error) {
    span.recordException(error);
    span.setStatus({ code: SpanStatusCode.ERROR });
    throw error;
  } finally {
    span.end();
  }
});
```

### Start Span (Manual)

Manual span management without setting active.

```typescript
const span = tracer.startSpan('operation', {
  attributes: {
    'http.method': 'GET',
    'http.url': '/api/data',
  },
  kind: SpanKind.CLIENT,
  startTime: Date.now(),
});

try {
  // Do work
} finally {
  span.end();
}
```

### Nested Spans

```typescript
tracer.startActiveSpan('parent', (parentSpan) => {
  tracer.startActiveSpan('child', (childSpan) => {
    // childSpan is child of parentSpan
    childSpan.end();
  });
  parentSpan.end();
});
```

## Attributes

### Standard Attributes

```typescript
span.setAttributes({
  // HTTP
  'http.method': 'GET',
  'http.url': '/api/data',
  'http.status_code': 200,
  'http.route': '/api/:id',

  // Database
  'db.system': 'postgresql',
  'db.statement': 'SELECT * FROM users',
  'db.name': 'mydb',

  // User
  'user.id': userId,
  'user.email': userEmail,

  // Custom
  'app.feature': 'checkout',
  'app.version': '1.0.0',
});
```

### Attribute Types

```typescript
span.setAttribute('string.attr', 'value');
span.setAttribute('number.attr', 42);
span.setAttribute('boolean.attr', true);
span.setAttribute('array.attr', ['a', 'b', 'c']);
```

### Cardinality Management

```typescript
// ❌ High cardinality (avoid)
span.setAttribute('user.email', email); // Unique per user
span.setAttribute('request.id', uuid); // Unique per request

// ✅ Low cardinality (prefer)
span.setAttribute('user.type', 'premium'); // Limited values
span.setAttribute('http.method', 'GET'); // Fixed set
span.setAttribute('error.type', 'NetworkError'); // Error categories
```

## Events

### Adding Events

```typescript
span.addEvent('user.action', {
  'action.type': 'click',
  'element.id': 'submit-button',
});

span.addEvent('cache.miss', {
  'cache.key': 'user:123',
});

span.addEvent('validation.failed', {
  'field': 'email',
  'reason': 'invalid format',
});
```

## Exception Handling

### Record Exception

```typescript
try {
  // Code that might throw
} catch (error) {
  span.recordException(error);
  span.setStatus({
    code: SpanStatusCode.ERROR,
    message: error.message,
  });
}
```

### Exception with Attributes

```typescript
span.recordException(error, {
  'exception.escaped': true,
  'exception.handled': false,
});
```

## React Native Patterns

### Custom Hook

```typescript
import { useCallback } from 'react';
import { trace, SpanStatusCode } from '@opentelemetry/api';

export const useTracer = () => {
  const tracer = trace.getTracer('my-app');

  const createEventSpan = useCallback((name: string, attributes: Record<string, any>) => {
    const span = tracer.startSpan(name, {
      attributes,
      kind: SpanKind.INTERNAL,
    });
    span.end();
  }, [tracer]);

  const withSpan = useCallback(async <T,>(
    name: string,
    fn: () => Promise<T>,
    attributes?: Record<string, any>
  ): Promise<T> => {
    return tracer.startActiveSpan(name, async (span) => {
      try {
        if (attributes) {
          span.setAttributes(attributes);
        }
        const result = await fn();
        span.setStatus({ code: SpanStatusCode.OK });
        return result;
      } catch (error) {
        span.recordException(error as Error);
        span.setStatus({ code: SpanStatusCode.ERROR });
        throw error;
      } finally {
        span.end();
      }
    });
  }, [tracer]);

  return { createEventSpan, withSpan, tracer };
};
```

### Usage in Components

```typescript
const { createEventSpan, withSpan } = useTracer();

const handleSubmit = async () => {
  createEventSpan('user.submit_form', {
    'form.type': 'checkout',
    'user.id': userId,
  });

  await withSpan('checkout.process', async () => {
    await processCheckout();
  }, {
    'cart.items': cartItems.length,
    'payment.method': 'credit_card',
  });
};
```

## Span Lifecycle

### Manual Span Management

```typescript
const span = tracer.startSpan('operation');

// Set initial attributes
span.setAttributes({
  'operation.type': 'fetch',
});

// Add event
span.addEvent('request.sent');

// Update attributes
span.setAttribute('response.size', data.length);

// Add another event
span.addEvent('response.received');

// Set final status
span.setStatus({ code: SpanStatusCode.OK });

// End span
span.end();
```

### Automatic Span Management

```typescript
await tracer.startActiveSpan('operation', async (span) => {
  // Span automatically ends after callback
  await doWork();
  // No need to call span.end()
});
```

## Testing

### Mock Tracer

```typescript
const mockSpan = {
  setAttribute: jest.fn(),
  setAttributes: jest.fn(),
  addEvent: jest.fn(),
  setStatus: jest.fn(),
  recordException: jest.fn(),
  end: jest.fn(),
  isRecording: jest.fn(() => true),
};

const mockTracer = {
  startSpan: jest.fn(() => mockSpan),
  startActiveSpan: jest.fn((name, fn) => fn(mockSpan)),
};

jest.mock('@opentelemetry/api', () => ({
  trace: {
    getTracer: jest.fn(() => mockTracer),
  },
  SpanStatusCode: {
    OK: 1,
    ERROR: 2,
  },
}));
```

### Verify Span Calls

```typescript
it('creates span with attributes', () => {
  const { createEventSpan } = useTracer();

  createEventSpan('user.action', { type: 'click' });

  expect(mockTracer.startSpan).toHaveBeenCalledWith('user.action', {
    attributes: { type: 'click' },
    kind: expect.any(Number),
  });
  expect(mockSpan.end).toHaveBeenCalled();
});
```

## Best Practices

### Span Naming

```typescript
// ✅ Good - descriptive, hierarchical
'api.fetch_user'
'database.query'
'navigation.screen_view'
'user.button_click'

// ❌ Bad - vague, inconsistent
'fetch'
'query'
'click'
'action'
```

### Attribute Keys

```typescript
// ✅ Good - namespaced, dot-separated
'user.id'
'http.method'
'db.statement'
'app.feature'

// ❌ Bad - no namespace, inconsistent
'userId'
'method'
'SQL'
'feature_name'
```

### Performance Considerations

```typescript
// Only create spans for significant operations
if (span.isRecording()) {
  // Add expensive attributes only if recording
  span.setAttribute('expensive.data', computeExpensiveData());
}

// Use single setAttributes for multiple values
span.setAttributes({
  attr1: value1,
  attr2: value2,
  attr3: value3,
});
```

## Key Considerations

- Always end spans (use `finally` or `startActiveSpan`)
- Keep attribute cardinality low (avoid unique IDs)
- Use semantic conventions for standard attributes
- Record exceptions with `recordException()`
- Set span status appropriately (OK, ERROR)
- Use `startActiveSpan` for automatic context propagation
- Namespace custom attributes (e.g., `app.feature`)
- Add events for significant milestones
- Test with mocked tracer to avoid overhead
- Only record vital attributes to reduce overhead
