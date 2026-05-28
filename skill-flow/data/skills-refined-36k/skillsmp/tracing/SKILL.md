---
name: tracing
description: "WHAT: OpenTelemetry tracing with useTracer hook for spans and distributed traces. WHEN: tracking user actions, monitoring async operations, debugging production issues. KEYWORDS: tracing, OpenTelemetry, OTEL, spans, useTracer, createEventSpan, withSpan, startSpan, SPAN_KEYS, attributes."
---

# OpenTelemetry Tracing Patterns

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns


## Core Principles

**Use OpenTelemetry spans to track operations and create distributed traces.** Choose the appropriate span type based on operation characteristics: createEventSpan for instant events, withSpan for async operations, startSpan for manual control, and useCustomTrace for long-running user flows.

**Why**: Distributed tracing enables debugging complex async flows in production, tracks performance bottlenecks, and provides visibility into user interactions across the app.

## When to Use This Skill

Use these patterns when:

- Tracking user interactions (button clicks, navigation, form submissions)
- Monitoring async operations (API calls, data processing, GraphQL queries)
- Creating traces for multi-step user flows (checkout, modals)
- Recording instant events without duration (state changes, errors)
- Debugging production issues with distributed traces
- Measuring operation performance and latency
- Testing tracing instrumentation

## Span Types Decision Matrix

### createEventSpan - Instant Events

**Use for**: Operations with no meaningful duration

```typescript
import { useTracer, SPAN_KEYS } from '@libs/tracing';

const MyComponent = () => {
  const { createEventSpan } = useTracer();

  const handleButtonClick = () => {
    createEventSpan(SPAN_KEYS.USER_ACTION, 'button_click', {
      button_id: 'submit',
      screen: 'checkout',
      action: 'submit_order',
    });
  };

  const handleStateChange = (newState: string) => {
    createEventSpan(SPAN_KEYS.STATE_CHANGE, 'order_state_change', {
      old_state: currentState,
      new_state: newState,
      order_id: orderId,
    });
    setCurrentState(newState);
  };

  return (
    <Button onPress={handleButtonClick}>Submit</Button>
  );
};
```

**Key patterns:**
- Span created and immediately ended (no duration)
- Used for button clicks, state changes, error events
- Attributes capture context (button_id, screen, action)
- Returns span (usually ignored)

**Why**: Instant events don't block execution and provide visibility into user actions without measuring duration.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/programs/screens/programs-home/hooks/useProgramsHomeAnalytics.ts:29`

### withSpan - Async Operations with Duration

**Use for**: Async operations where you want automatic span lifecycle management

```typescript
import { useTracer, SPAN_KEYS } from '@libs/tracing';
import { SpanStatusCode } from '@opentelemetry/api';

export const useCheckout = () => {
  const { withSpan } = useTracer();

  const processPayment = async (paymentData: PaymentData) => {
    return await withSpan(
      SPAN_KEYS.API_REQUEST,
      async (span) => {
        span.setAttributes({
          operation: 'process_payment',
          payment_method: paymentData.method,
          amount: paymentData.total,
        });

        const result = await paymentService.process(paymentData);

        span.setAttribute('transaction_id', result.transactionId);
        span.setStatus({ code: SpanStatusCode.OK });

        return result;
      },
      'process_payment' // Optional custom span name
    );
  };

  return { processPayment };
};
```

**Key patterns:**
- Automatic span lifecycle: created, callback executed, span ended
- Automatic error handling: error thrown → span status set to ERROR
- Callback receives span for setting attributes
- Span ended in finally block (guaranteed cleanup)

**Why**: withSpan handles all span lifecycle management automatically, including error handling and cleanup. Use for most async operations.

**Production Example**: `git-resources/shared-mobile-modules/src/features/country-selection/CountrySelection.tsx:82`

### startSpan - Manual Control

**Use for**: Complex operations requiring fine-grained control over span lifecycle

```typescript
import { useTracer, SPAN_KEYS } from '@libs/tracing';
import { SpanStatusCode } from '@opentelemetry/api';

export const useComplexOperation = () => {
  const { startSpan } = useTracer();

  const performComplexOperation = async () => {
    const span = startSpan(SPAN_KEYS.DATA_PROCESSING, 'complex_operation');

    try {
      // Step 1: Validate input
      span.addEvent('validation_start');
      await validateInput();
      span.addEvent('validation_complete');

      // Step 2: Process data
      span.setAttribute('processing_stage', 'data_transformation');
      const processed = await transformData();
      span.setAttribute('records_processed', processed.length);

      // Step 3: Save results
      span.setAttribute('processing_stage', 'save_results');
      await saveResults(processed);

      span.setStatus({ code: SpanStatusCode.OK });
      return processed;
    } catch (error) {
      span.recordException(error as Error);
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: (error as Error).message,
      });
      throw error;
    } finally {
      span.end(); // CRITICAL: Always end span
    }
  };

  return { performComplexOperation };
};
```

**Key patterns:**
- Manual span creation with startSpan()
- Incremental attribute updates as operation progresses
- span.addEvent() for operation milestones
- span.recordException() for errors
- span.end() in finally block (CRITICAL)

**Why**: Manual control allows tracking multi-step operations with detailed progress. You control exactly when span ends.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/tracing/getTracer.ts:85`

### useCustomTrace - Long-Running User Flows

**Use for**: Multi-step user interactions spanning multiple renders

```typescript
import { useCustomTrace } from '@libs/tracing';
import { SPAN_KEYS } from '@libs/tracing';

export const CheckoutFlow = () => {
  const [startTrace, endTrace] = useCustomTrace(SPAN_KEYS.CHECKOUT_FLOW);

  useEffect(() => {
    // Start trace when checkout flow opens
    startTrace({
      user_id: userId,
      cart_total: cartTotal,
      items_count: cartItems.length,
    });

    return () => {
      // Auto-cleanup on unmount
      endTrace();
    };
  }, []);

  const handlePaymentComplete = (transactionId: string) => {
    // Add attributes before ending
    endTrace({
      transaction_id: transactionId,
      payment_method: selectedPaymentMethod,
      completion_status: 'success',
    });
    navigation.navigate('OrderConfirmation');
  };

  const handleCancel = () => {
    endTrace({
      completion_status: 'cancelled',
      step: currentStep,
    });
    navigation.goBack();
  };

  return (
    <View>
      <PaymentForm onComplete={handlePaymentComplete} />
      <Button onPress={handleCancel}>Cancel</Button>
    </View>
  );
};
```

**Key patterns:**
- Returns tuple: [start, end]
- Automatically prevents nested spans (ends previous if start called again)
- Automatic cleanup on unmount via useEffect
- Start adds initial attributes, end adds final attributes
- Tracks user flows: checkout, modals, multi-step forms

**Why**: Tracks user interactions that span multiple renders and component lifecycles. Auto-cleanup prevents memory leaks.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/tracing/useCustomTrace.ts:1`

## SPAN_KEYS and Naming Conventions

### Use SPAN_KEYS Constants

Always use predefined SPAN_KEYS to enforce low cardinality:

```typescript
import { SPAN_KEYS } from '@libs/tracing';

// ✅ Correct - Use constants
createEventSpan(SPAN_KEYS.USER_ACTION, 'button_click');
withSpan(SPAN_KEYS.API_REQUEST, async (span) => { /* ... */ });
startSpan(SPAN_KEYS.DATA_PROCESSING, 'transform_data');

// ❌ Wrong - String literals create high cardinality
createEventSpan('user_action', 'button_click'); // Don't use string literals
```

**Available SPAN_KEYS:**

```typescript
export const SPAN_KEYS = {
  SESSION: 'session',
  AUTH_GUARD: 'auth_guard',
  SESSION_BACKGROUND: 'session_background',
  SESSION_FOREGROUND: 'session_foreground',
  FETCH: 'fetch',
  GRAPHQL_OPERATION: 'graphql.operation',
  ERROR_BOUNDARY: 'error_boundary',
  USER_ACTION: 'user_action',
  TRACING_PROVIDER: 'tracing_provider',
  STATE_CHANGE: 'state_change',
  API_REQUEST: 'api_request',
  DATA_PROCESSING: 'data_processing',
  CHECKOUT_FLOW: 'checkout_flow',
} as const;
```

**Why**: Constants ensure low cardinality (limited number of unique span keys). High cardinality overwhelms tracing backends.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/tracing/spanKeys.ts:1`

### Span Naming Patterns

**Hierarchical naming with snake_case:**

```typescript
// ✅ Correct - Descriptive hierarchy
createEventSpan(SPAN_KEYS.USER_ACTION, 'button_click_submit');
createEventSpan(SPAN_KEYS.API_REQUEST, 'fetch_user_profile');
createEventSpan(SPAN_KEYS.DATA_PROCESSING, 'transform_order_data');

// Pattern: {domain}_{component}_{operation}
createEventSpan(SPAN_KEYS.USER_ACTION, 'checkout_payment_submit');
//                                       ^domain  ^component ^operation

// ❌ Wrong - Dynamic values in span name
createEventSpan(SPAN_KEYS.USER_ACTION, `button_click_${buttonId}`); // High cardinality!
createEventSpan(SPAN_KEYS.API_REQUEST, `fetch_user_${userId}`); // High cardinality!
```

**Put dynamic data in attributes, NOT span names:**

```typescript
// ✅ Correct - Dynamic data in attributes
createEventSpan(SPAN_KEYS.USER_ACTION, 'button_click', {
  button_id: buttonId, // Dynamic value here
  screen: screenName,
  user_id: userId,
});

// ✅ Correct - TracingProvider span naming
const spanName = `${moduleType}_${moduleName}`;
// screen_checkout, component_cart, feature_payment
```

**Why**: Span names should have low cardinality (limited unique values). Dynamic data creates high cardinality and overwhelms tracing systems.

## Vital Attributes

### Auto-Injected Attributes

useTracer automatically injects vital attributes to every span:

```typescript
export const useTracer = (tracerName: string = TRACER_KEYS.REACT_APP) => {
  const tracingContext = useTracingContext();
  const vitalAttributesFromHook = useVitalAttributes();

  const allAttributes = {
    ...contextAttributes,
    ...vitalAttributesFromHook, // Auto-injected: country, locale, customerID
  };

  return getTracer(tracerName, span, allAttributes);
};
```

**Vital attributes included:**
- `country` - User's country code (from AppConfig)
- `locale` - User's locale (from AppConfig)
- `customer.id` - Customer ID if authenticated

**Why**: Vital attributes enable filtering traces by country, locale, or customer without manual injection in every span.

### TracingProvider Context Attributes

Wrap components with TracingProvider to add context attributes:

```typescript
import { TracingProvider } from '@libs/tracing';

export const CheckoutScreen = () => {
  return (
    <TracingProvider
      moduleType="screen"
      moduleName="checkout"
      squad="conversions-mobile"
      attributes={{
        checkout_step: 'payment',
        cart_total: cartTotal,
      }}
    >
      <CheckoutFlow />
    </TracingProvider>
  );
};
```

**Attributes added by TracingProvider:**
- `squad` - Team attribution
- `module.name` - Component/screen/feature name
- `module.type` - screen | stack | component | feature
- `screen.name` / `component.name` / etc. - Dynamic based on moduleType
- Custom attributes from props

**Why**: TracingProvider cascades context attributes to all child spans. Set once, available everywhere.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/tracing/TracingProvider.tsx:1`

### Attribute Naming Conventions

**Use hierarchical snake_case naming:**

```typescript
span.setAttributes({
  // ✅ Correct - Hierarchical naming
  'http.request.method': 'POST',
  'http.request.url': url,
  'http.response.status_code': 200,
  'user.id': userId,
  'user.subscription.plan': 'premium',
  'cart.items.count': items.length,
  'cart.total.amount': total,
  'payment.method': 'credit_card',
  'payment.transaction.id': transactionId,
});

// ❌ Wrong - Flat naming
span.setAttributes({
  method: 'POST', // Not hierarchical
  userId: userId, // camelCase instead of snake_case
  'items-count': items.length, // Hyphens instead of underscores
});
```

**Semantic Conventions:**
- Use OpenTelemetry semantic conventions for HTTP, Database, etc.
- Format: `{namespace}.{component}.{attribute}` in snake_case
- Examples: `http.request.method`, `db.operation`, `user.id`

**Why**: Hierarchical naming enables filtering and grouping in tracing UIs. Semantic conventions ensure consistency.

## Cardinality Management

### High Cardinality Problem

**Cardinality**: Number of unique values for a dimension

```typescript
// ❌ High Cardinality - BAD
// Each unique user_id creates a new span name
// 10,000 users = 10,000 unique span names
createEventSpan(SPAN_KEYS.USER_ACTION, `user_${userId}_action`);

// ❌ High Cardinality - BAD
// Each unique transaction creates a new span name
withSpan(SPAN_KEYS.API_REQUEST, async () => {
  // ...
}, `transaction_${transactionId}`);

// ✅ Low Cardinality - GOOD
// Single span name, dynamic data in attributes
createEventSpan(SPAN_KEYS.USER_ACTION, 'user_action', {
  user_id: userId, // High cardinality data in attributes
  action_type: 'button_click',
});
```

**Why high cardinality is bad:**
- Overwhelms tracing backends (Honeycomb, Datadog)
- Increases costs (charged per unique span name)
- Degrades query performance
- Makes traces unusable

**Rule**: Span names should have **low cardinality** (< 100 unique values). Attributes can have **high cardinality**.

### Safe vs Unsafe Values

**Low cardinality (safe in span names):**
- Operation types: 'fetch', 'update', 'delete'
- Screen names: 'checkout', 'cart', 'profile'
- Action types: 'button_click', 'navigation', 'state_change'
- Fixed enum values

**High cardinality (only in attributes):**
- User IDs
- Transaction IDs
- Timestamps
- URLs with query params
- Error messages
- Any user-generated content

## Error Handling in Spans

### withSpan Auto-Handling

withSpan automatically handles errors:

```typescript
const fetchData = async () => {
  return await withSpan(SPAN_KEYS.API_REQUEST, async (span) => {
    span.setAttribute('endpoint', '/api/users');

    const response = await fetch('/api/users');

    // If error thrown, withSpan:
    // 1. Sets span status to ERROR
    // 2. Ends span
    // 3. Re-throws error

    span.setAttribute('status_code', response.status);
    return response.json();
  });
};
```

**Why**: withSpan handles span lifecycle in error cases automatically. No manual error handling needed.

### startSpan Manual Error Handling

startSpan requires manual error handling:

```typescript
const processData = async () => {
  const span = startSpan(SPAN_KEYS.DATA_PROCESSING, 'process_data');

  try {
    const result = await transform();
    span.setStatus({ code: SpanStatusCode.OK });
    return result;
  } catch (error) {
    span.recordException(error as Error); // Record exception details
    span.setStatus({
      code: SpanStatusCode.ERROR,
      message: (error as Error).message,
    });
    throw error; // Re-throw for caller
  } finally {
    span.end(); // CRITICAL: Always end span
  }
};
```

**Key patterns:**
- span.recordException() for error details
- span.setStatus() with ERROR code
- span.end() in finally block (CRITICAL)
- Re-throw error for caller to handle

**Why**: Manual error handling gives full control over error reporting and span attributes during failures.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/networking-client/client/useFetch.ts:89`

## TracingProvider for Context

### Provider Hierarchy

TracingProvider cascades context attributes:

```typescript
// Top-level provider
<TracingProvider
  moduleType="stack"
  moduleName="checkout_stack"
  squad="conversions-mobile"
>
  {/* Screen-level provider inherits stack attributes */}
  <TracingProvider
    moduleType="screen"
    moduleName="payment_screen"
    attributes={{
      checkout_step: 'payment',
    }}
  >
    {/* Component-level provider inherits all parent attributes */}
    <TracingProvider
      moduleType="component"
      moduleName="credit_card_form"
      attributes={{
        form_type: 'credit_card',
      }}
    >
      <CreditCardForm />
    </TracingProvider>
  </TracingProvider>
</TracingProvider>
```

**Attributes cascade:**
- `squad`: 'conversions-mobile' (from stack)
- `module.name`: 'credit_card_form' (from component)
- `module.type`: 'component' (from component)
- `stack.name`: 'checkout_stack' (from stack)
- `screen.name`: 'payment_screen' (from screen)
- `component.name`: 'credit_card_form' (from component)
- `checkout_step`: 'payment' (from screen)
- `form_type`: 'credit_card' (from component)

**Why**: Cascading context eliminates repetitive attribute setting. Set attributes once at provider level, available in all child spans.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/tracing/TracingProvider.tsx:24`

### Provider Span Creation

TracingProvider automatically creates an event span:

```typescript
const contextSpan = useMemo(() => {
  const spanName = `${props.moduleType}_${props.moduleName}`;
  // screen_checkout, component_cart, feature_payment

  return createEventSpan(
    SPAN_KEYS.TRACING_PROVIDER,
    spanName,
    mergedAttributes,
    parentSpan
  );
}, []);
```

**Why**: Provider span serves as parent for all child spans, creating hierarchical trace structure.

## Testing Tracing

### Mock useTracer

```typescript
import { renderHook, act } from '@testing-library/react-native';
import { useTracer } from '@libs/tracing';

jest.mock('@libs/tracing', () => ({
  useTracer: jest.fn(),
  SPAN_KEYS: {
    USER_ACTION: 'user_action',
    API_REQUEST: 'api_request',
  },
}));

describe('useCheckout', () => {
  const mockCreateEventSpan = jest.fn();
  const mockWithSpan = jest.fn((key, callback) => callback({
    setAttributes: jest.fn(),
    setAttribute: jest.fn(),
    setStatus: jest.fn(),
  }));
  const mockStartSpan = jest.fn(() => ({
    setAttributes: jest.fn(),
    setAttribute: jest.fn(),
    setStatus: jest.fn(),
    recordException: jest.fn(),
    end: jest.fn(),
  }));

  beforeEach(() => {
    jest.clearAllMocks();
    (useTracer as jest.Mock).mockReturnValue({
      createEventSpan: mockCreateEventSpan,
      withSpan: mockWithSpan,
      startSpan: mockStartSpan,
    });
  });

  it('creates event span on button click', () => {
    const { result } = renderHook(() => useCheckout());

    act(() => {
      result.current.handleButtonClick();
    });

    expect(mockCreateEventSpan).toHaveBeenCalledWith(
      'user_action',
      'button_click_submit',
      expect.objectContaining({
        button_id: 'submit',
        screen: 'checkout',
      })
    );
  });

  it('uses withSpan for async operation', async () => {
    const { result } = renderHook(() => useCheckout());

    await act(async () => {
      await result.current.processPayment({ method: 'credit_card', total: 100 });
    });

    expect(mockWithSpan).toHaveBeenCalledWith(
      'api_request',
      expect.any(Function),
      'process_payment'
    );
  });
});
```

**Key patterns:**
- Mock useTracer to return mock functions
- Mock SPAN_KEYS with test values
- Mock span methods: setAttributes, setAttribute, setStatus, recordException, end
- Verify span creation with correct key, name, and attributes
- Use act() wrapper for async operations

**Why**: Testing ensures tracing instrumentation works correctly without sending real traces to backend.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/tracing/getTracer.spec.ts:1`

### Test Span Attributes

```typescript
it('sets correct attributes on span', async () => {
  const mockSpan = {
    setAttributes: jest.fn(),
    setAttribute: jest.fn(),
    setStatus: jest.fn(),
  };

  mockWithSpan.mockImplementation((key, callback) => callback(mockSpan));

  const { result } = renderHook(() => useCheckout());

  await act(async () => {
    await result.current.processPayment({ method: 'credit_card', total: 100 });
  });

  expect(mockSpan.setAttributes).toHaveBeenCalledWith({
    operation: 'process_payment',
    payment_method: 'credit_card',
    amount: 100,
  });

  expect(mockSpan.setStatus).toHaveBeenCalledWith({
    code: 0, // SpanStatusCode.OK
  });
});
```

**Why**: Verify correct attributes are set on spans with proper values and timing.

## Common Mistakes to Avoid

❌ **Don't create spans during render**:

```typescript
// ❌ Wrong - Creates span on every render
const MyComponent = () => {
  const { createEventSpan } = useTracer();
  createEventSpan(SPAN_KEYS.USER_ACTION, 'component_render'); // Called on every render!

  return <View />;
};

// ✅ Correct - Create spans in event handlers or effects
const MyComponent = () => {
  const { createEventSpan } = useTracer();

  useEffect(() => {
    createEventSpan(SPAN_KEYS.USER_ACTION, 'component_mount'); // Once on mount
  }, []);

  const handleClick = () => {
    createEventSpan(SPAN_KEYS.USER_ACTION, 'button_click'); // On user action
  };

  return <Button onPress={handleClick} />;
};
```

❌ **Don't forget to end spans**:

```typescript
// ❌ Wrong - Memory leak, span never ends
const span = startSpan(SPAN_KEYS.API_REQUEST, 'fetch_data');
const result = await fetchData();
// Forgot span.end()

// ✅ Correct - Always end span in finally
const span = startSpan(SPAN_KEYS.API_REQUEST, 'fetch_data');
try {
  const result = await fetchData();
  return result;
} finally {
  span.end(); // CRITICAL
}
```

❌ **Don't use dynamic values in span names**:

```typescript
// ❌ Wrong - High cardinality
createEventSpan(SPAN_KEYS.USER_ACTION, `user_${userId}_action`);
withSpan(SPAN_KEYS.API_REQUEST, async () => {}, `fetch_order_${orderId}`);

// ✅ Correct - Dynamic values in attributes
createEventSpan(SPAN_KEYS.USER_ACTION, 'user_action', { user_id: userId });
withSpan(
  SPAN_KEYS.API_REQUEST,
  async (span) => {
    span.setAttribute('order_id', orderId);
  },
  'fetch_order'
);
```

❌ **Don't create too many spans**:

```typescript
// ❌ Wrong - Too granular, performance overhead
items.forEach((item) => {
  withSpan(SPAN_KEYS.DATA_PROCESSING, async (span) => {
    processItem(item);
  }, `process_item_${item.id}`); // Also high cardinality!
});

// ✅ Correct - Single span for batch operation
await withSpan(SPAN_KEYS.DATA_PROCESSING, async (span) => {
  span.setAttribute('items_count', items.length);

  const results = await Promise.all(items.map(processItem));

  span.setAttribute('processed_count', results.length);
  return results;
}, 'process_items_batch');
```

✅ **Do use withSpan for most async operations**:

```typescript
// ✅ Automatic span lifecycle management
const fetchData = async () => {
  return await withSpan(SPAN_KEYS.API_REQUEST, async (span) => {
    span.setAttribute('endpoint', '/api/users');
    return await fetch('/api/users');
  });
};
```

✅ **Do cascade context with TracingProvider**:

```typescript
// ✅ Set context once, available everywhere
<TracingProvider
  moduleType="screen"
  moduleName="checkout"
  squad="conversions-mobile"
  attributes={{ checkout_step: 'payment' }}
>
  <CheckoutFlow />
</TracingProvider>
```

✅ **Do use SPAN_KEYS constants**:

```typescript
// ✅ Low cardinality enforcement
import { SPAN_KEYS } from '@libs/tracing';

createEventSpan(SPAN_KEYS.USER_ACTION, 'button_click');
withSpan(SPAN_KEYS.API_REQUEST, async () => { /* ... */ });
```

## Performance Considerations

### Span Creation Cost

Creating spans has minimal overhead, but avoid creating thousands of spans:

```typescript
// ❌ Avoid - Creates 1000+ spans
for (let i = 0; i < 1000; i++) {
  createEventSpan(SPAN_KEYS.DATA_PROCESSING, 'item_processed');
}

// ✅ Better - Single span with count
createEventSpan(SPAN_KEYS.DATA_PROCESSING, 'items_processed', {
  items_count: 1000,
});
```

**Why**: Each span has serialization and network cost. Batch operations into fewer spans.

### Attribute Size

Keep attribute values small:

```typescript
// ❌ Large attribute values
span.setAttribute('response_body', JSON.stringify(largeResponse)); // 100KB+

// ✅ Small attribute values
span.setAttribute('response_size', largeResponse.length);
span.setAttribute('items_count', largeResponse.items.length);
```

**Why**: Large attributes increase trace size and backend costs.

## Quick Reference

**Span Types:**
```typescript
// Instant event (no duration)
createEventSpan(SPAN_KEYS.USER_ACTION, 'button_click', { button_id: 'submit' });

// Async operation with auto-lifecycle
await withSpan(SPAN_KEYS.API_REQUEST, async (span) => {
  span.setAttribute('endpoint', '/api/users');
  return await fetch('/api/users');
});

// Manual control
const span = startSpan(SPAN_KEYS.DATA_PROCESSING, 'transform_data');
try {
  await transform();
} finally {
  span.end();
}

// Long-running user flow
const [start, end] = useCustomTrace(SPAN_KEYS.CHECKOUT_FLOW);
start({ user_id: userId });
// ... user interactions ...
end({ status: 'success' });
```

**TracingProvider:**
```typescript
<TracingProvider
  moduleType="screen"
  moduleName="checkout"
  squad="conversions-mobile"
  attributes={{ checkout_step: 'payment' }}
>
  <CheckoutFlow />
</TracingProvider>
```

**Testing:**
```typescript
jest.mock('@libs/tracing', () => ({
  useTracer: jest.fn(() => ({
    createEventSpan: jest.fn(),
    withSpan: jest.fn((key, cb) => cb({ setAttributes: jest.fn() })),
    startSpan: jest.fn(() => ({ end: jest.fn() })),
  })),
}));
```

**Key Libraries:**
- @opentelemetry/api 2.0.1
- React Native 0.75.4
- TypeScript 5.1.6

For production examples, see [references/examples.md](references/examples.md).
