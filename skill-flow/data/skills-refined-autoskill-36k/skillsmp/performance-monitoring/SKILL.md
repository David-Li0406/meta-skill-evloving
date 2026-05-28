---
name: performance-monitoring
description: "WHAT: Performance hooks for TTR, TTI, and custom metrics with dual native + OTEL tracking. WHEN: measuring render time, tracking interactivity readiness, monitoring async operations. KEYWORDS: performance, TTR, TTI, useTimeToRender, useTimeToInteractivity, usePerformanceTracker, metrics, onLayout."
---

# Performance Monitoring Patterns

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns


## Core Principles

**Use performance monitoring hooks to track render time, interactivity, and custom metrics.** Choose useTimeToRender for visual rendering performance, useTimeToInteractivity for user readiness, and usePerformanceTracker for custom operations with dual native + OTEL tracking.

**Why**: Performance monitoring identifies bottlenecks, tracks user experience metrics, and enables proactive optimization. Measuring Time To Render (TTR) and Time To Interactivity (TTI) provides insights into actual user experience beyond traditional metrics.

## When to Use This Skill

Use these patterns when:

- Measuring screen render performance (TTR)
- Tracking when UI becomes interactive (TTI)
- Monitoring async operations with custom metrics
- Recording performance context (user info, operation complexity)
- Debugging slow screens or interactions
- Optimizing user experience metrics
- Testing performance instrumentation

## Performance Hook Decision Matrix

### useTimeToRender - Visual Rendering Performance

**Use for**: Measuring when UI is visually rendered

```typescript
import { useTimeToRender } from '@libs/observability';

const ProductDetailsScreen = ({ productId }: Props) => {
  const { measureTTROnLayout } = useTimeToRender({
    traceName: 'ProductDetails',
    autoStart: true, // Starts on mount
  });

  return (
    <ScrollView onLayout={measureTTROnLayout}>
      <ProductInfo productId={productId} />
      <AddToCartButton />
    </ScrollView>
  );
};
```

**Key patterns:**
- Attach `measureTTROnLayout` to root View/ScrollView `onLayout` prop
- `onLayout` fires after View has been measured and rendered
- `autoStart: true` captures full render cycle from mount
- Automatically stops when layout completes
- Provides debug logging in `__DEV__` mode
- Trace name suffixed with `_ttr` internally

**Why**: TTR accurately measures when UI is visually rendered, providing actual user-facing performance metrics rather than code execution time. Uses `onLayout` because it fires after the View has been measured and laid out.

**Production Example**: `git-resources/shared-mobile-modules/src/features/country-selection/CountrySelection.tsx:29`

### useTimeToInteractivity - User Readiness

**Use for**: Measuring when users can actually interact with UI

```typescript
import { useTimeToInteractivity } from '@libs/observability';

const CheckoutScreen = () => {
  useTimeToInteractivity({
    traceName: 'Checkout',
    autoStart: true,
  });

  return (
    <View>
      <PaymentForm />
      <SubmitButton />
    </View>
  );
};
```

**Key patterns:**
- No callback needed (fully automatic)
- Uses `InteractionManager.runAfterInteractions()`
- Measures when JS thread is ready for user interaction
- `autoStart: true` starts on mount
- Automatically stops when interactions complete
- Trace name suffixed with `_tti` internally

**Why**: TTI measures when users can actually interact with the UI, which may happen after initial render due to animations, data loading, or JavaScript execution. InteractionManager waits for all interactions (animations, gestures) to complete.

**Production Example**: `git-resources/shared-mobile-modules/src/features/country-selection/CountrySelection.tsx:32`

### usePerformanceTracker - Custom Operations

**Use for**: Tracking async operations, data loading, or custom metrics with dual native + OTEL tracking

```typescript
import { usePerformanceTracker } from '@libs/observability';
import { SPAN_KEYS } from '@libs/tracing';

const useDataLoader = () => {
  const { startTrace, stopTrace, recordUserInfo, incrementMetric } =
    usePerformanceTracker(SPAN_KEYS.DATA_PROCESSING, 'DataLoad');

  const loadData = async () => {
    startTrace();

    try {
      const result = await fetchData();

      // Record context
      recordUserInfo({
        dataSource: 'api',
        cacheHit: false,
      });

      // Record metrics
      incrementMetric({
        metricName: 'items_loaded',
        value: result.length,
      });

      stopTrace();
      return result;
    } catch (error) {
      stopTrace();
      throw error;
    }
  };

  return { loadData };
};
```

**Key patterns:**
- Manual `startTrace()` and `stopTrace()` calls
- `recordUserInfo()` adds context attributes
- `incrementMetric()` tracks counters
- Dual tracking: native PerformanceTracker + OTEL spans
- Always stop trace in finally or catch block

**Why**: Provides flexible tracking for operations that don't fit TTR or TTI patterns. Dual tracking enables both native platform monitoring and distributed tracing.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/observability/usePerformanceTracker.ts:1`

### Opting Out of OTEL Tracking

**Use `{ useOTEL: false }` when combining with TTR/TTI to avoid duplicate spans:**

```typescript
const ProductScreen = () => {
  // TTR creates OTEL span
  const { measureTTROnLayout } = useTimeToRender({
    traceName: 'ProductScreen',
  });

  // TTI creates OTEL span
  useTimeToInteractivity({ traceName: 'ProductScreen' });

  // Disable OTEL to avoid duplicate spans
  const { recordUserInfo } = usePerformanceTracker(
    SPAN_KEYS.DATA_PROCESSING,
    'ProductScreen_Load',
    { useOTEL: false } // Native tracking only
  );

  const { data } = useQuery({
    queryKey: ['product'],
    queryFn: fetchProduct,
    onSuccess: (product) => {
      recordUserInfo({
        productId: product.id,
        variantCount: product.variants.length,
      });
    },
  });

  return <ScrollView onLayout={measureTTROnLayout}>...</ScrollView>;
};
```

**Why**: TTR and TTI already create OTEL spans. Using `useOTEL: false` in usePerformanceTracker avoids creating duplicate spans while still recording native metrics and attributes.

## Combining Performance Hooks

### Complete Screen Instrumentation

```typescript
import {
  useTimeToRender,
  useTimeToInteractivity,
  usePerformanceTracker,
} from '@libs/observability';
import { SPAN_KEYS } from '@libs/tracing';
import { useQuery } from '@tanstack/react-query';

const ProductDetailsScreen = ({ productId }: Props) => {
  // Measure visual render time
  const { measureTTROnLayout } = useTimeToRender({
    traceName: 'ProductDetails',
    autoStart: true,
  });

  // Measure interactivity readiness
  useTimeToInteractivity({
    traceName: 'ProductDetails',
    autoStart: true,
  });

  // Track data loading metrics (OTEL disabled to avoid duplicates)
  const { recordUserInfo, incrementMetric } = usePerformanceTracker(
    SPAN_KEYS.DATA_PROCESSING,
    'ProductDetails_DataLoad',
    { useOTEL: false }
  );

  const { data, isLoading } = useQuery({
    queryKey: ['product', productId],
    queryFn: () => fetchProduct(productId),
    onSuccess: (product) => {
      recordUserInfo({
        productId: product.id,
        hasImages: product.images.length > 0,
      });
      incrementMetric({
        metricName: 'variant_count',
        value: product.variants.length,
      });
    },
  });

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <ScrollView onLayout={measureTTROnLayout}>
      <ProductInfo product={data} />
      <AddToCartButton />
    </ScrollView>
  );
};
```

**Key patterns:**
- TTR measures UI render time
- TTI measures when UI becomes interactive
- usePerformanceTracker with `useOTEL: false` adds custom metrics
- All hooks use same base trace name: 'ProductDetails'
- TTR attached to root container's onLayout
- recordUserInfo adds context on data load success

**Why**: Combining multiple performance hooks provides comprehensive visibility into different aspects of user experience: visual render, interactivity, and data loading.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/programs/screens/programs-home/ProgramsHome.tsx:44`

## Recording Performance Metrics

### Add Context with recordUserInfo

```typescript
const { recordUserInfo } = usePerformanceTracker(
  SPAN_KEYS.DATA_PROCESSING,
  'CartLoad',
  { useOTEL: false }
);

const { data } = useQuery({
  queryKey: ['cart'],
  queryFn: fetchCart,
  onSuccess: (cart) => {
    recordUserInfo({
      userId: user.id,
      itemCount: cart.items.length,
      totalValue: cart.total,
      cacheHit: cart.fromCache,
      hasPromoCode: !!cart.promoCode,
    });
  },
});
```

**Key patterns:**
- Record context after operation completes
- Include relevant business metrics
- Use descriptive attribute names
- Record both success and error cases

**Why**: Adding context to performance traces enables filtering and analysis by user segment, data source, or operation complexity. Helps identify patterns in performance issues.

### Track Counters with incrementMetric

```typescript
const { startTrace, stopTrace, incrementMetric } = usePerformanceTracker(
  SPAN_KEYS.DATA_PROCESSING,
  'ImageLoad'
);

const loadImages = async (urls: string[]) => {
  startTrace();

  let successCount = 0;
  let errorCount = 0;

  for (const url of urls) {
    try {
      await loadImage(url);
      successCount++;
    } catch {
      errorCount++;
    }
  }

  incrementMetric({ metricName: 'images_loaded', value: successCount });
  incrementMetric({ metricName: 'images_failed', value: errorCount });

  stopTrace();
};
```

**Key patterns:**
- Track operation counts
- Separate success and error counters
- Record metrics before stopping trace
- Use snake_case naming

**Why**: Metrics provide quantitative data about operation complexity and success rates. Helps understand performance in context of operation scale.

## Development Mode Logging

Performance hooks automatically log metrics in development mode:

```typescript
const MyScreen = () => {
  const { measureTTROnLayout } = useTimeToRender({
    traceName: 'MyScreen',
  });

  useTimeToInteractivity({ traceName: 'MyScreen' });

  return <View onLayout={measureTTROnLayout}>...</View>;
};

// Console output in __DEV__:
// #DEBUG [MyScreen] Time To Render: 234.56 ms
// #DEBUG [MyScreen] Time To Interactivity: 456.78 ms
```

**Key patterns:**
- Automatic logging with `#DEBUG` prefix
- Shows trace name and milliseconds
- Only logs in development mode (`__DEV__`)
- No manual logging needed

**Why**: Immediate feedback during development enables quick performance regression detection without opening profiler tools.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/observability/useTimeToRender.ts:54`

## When to Use TTR vs TTI

### Use TTR When:

- Measuring **visual rendering performance**
- Optimizing **initial paint time**
- Testing **layout performance**
- Debugging **slow render cycles**

```typescript
// ✅ Good use case: Measuring screen render
const { measureTTROnLayout } = useTimeToRender({
  traceName: 'ProductList',
});

return (
  <FlatList
    onLayout={measureTTROnLayout}
    data={products}
    renderItem={renderProduct}
  />
);
```

### Use TTI When:

- Measuring **actual user experience**
- Tracking when users can **interact with UI**
- Optimizing **responsiveness after mount**
- Understanding **render-to-interactive gap**

```typescript
// ✅ Good use case: Measuring when UI is ready
useTimeToInteractivity({ traceName: 'Checkout' });

// UI might render immediately, but TTI waits for:
// - Animations to complete
// - Data to load
// - JS thread to be idle
```

### Use Both When:

- Comprehensive performance monitoring
- Understanding render-to-interactive gap
- Debugging slow interactivity issues
- Optimizing both render and interaction

```typescript
// ✅ Complete monitoring
const { measureTTROnLayout } = useTimeToRender({
  traceName: 'ProductDetails',
});
useTimeToInteractivity({ traceName: 'ProductDetails' });

// Metrics show:
// - TTR: 200ms (UI rendered quickly)
// - TTI: 800ms (animations + data loading delayed interactivity)
// Gap of 600ms indicates optimization opportunity
```

## Common Mistakes to Avoid

❌ **Don't use TTR for non-UI operations**:

```typescript
// ❌ Wrong - TTR only measures layout completion
const DataProcessingScreen = () => {
  const { measureTTROnLayout } = useTimeToRender({
    traceName: 'DataProcessing',
  });

  // UI renders immediately, but data is still loading
  return (
    <View onLayout={measureTTROnLayout}>
      <DataList data={slowlyLoadingData} />
    </View>
  );
};
```

✅ **Do use appropriate metrics for each operation**:

```typescript
// ✅ Correct - Separate metrics for UI and data
const DataProcessingScreen = () => {
  // TTR measures UI render time
  const { measureTTROnLayout } = useTimeToRender({
    traceName: 'DataProcessing',
  });

  // Custom tracker measures data loading time
  const { startTrace, stopTrace } = usePerformanceTracker(
    SPAN_KEYS.DATA_PROCESSING,
    'DataProcessing_DataLoad',
    { useOTEL: false }
  );

  const { data, isLoading } = useQuery({
    queryKey: ['data'],
    queryFn: async () => {
      startTrace();
      try {
        const result = await fetchData();
        stopTrace();
        return result;
      } catch (error) {
        stopTrace();
        throw error;
      }
    },
  });

  return (
    <View onLayout={measureTTROnLayout}>
      {isLoading ? <LoadingSpinner /> : <DataList data={data} />}
    </View>
  );
};
```

❌ **Don't create multiple trackers for same operation**:

```typescript
// ❌ Wrong - Creates 3 separate traces
const MyScreen = () => {
  const tracker1 = usePerformanceTracker(SPAN_KEYS.SESSION, 'MyScreen');
  const tracker2 = usePerformanceTracker(SPAN_KEYS.SESSION, 'MyScreen');
  const { measureTTROnLayout } = useTimeToRender({ traceName: 'MyScreen' });

  useEffect(() => {
    tracker1.startTrace();
    tracker2.startTrace(); // Duplicate!
  }, []);
};
```

✅ **Do use appropriate hooks for specific measurements**:

```typescript
// ✅ Correct - One hook per measurement type
const MyScreen = () => {
  // TTR for render performance
  const { measureTTROnLayout } = useTimeToRender({ traceName: 'MyScreen' });

  // TTI for interactivity
  useTimeToInteractivity({ traceName: 'MyScreen' });

  // Custom tracker only for additional metrics (OTEL disabled)
  const { recordUserInfo } = usePerformanceTracker(
    SPAN_KEYS.DATA_PROCESSING,
    'MyScreen_Load',
    { useOTEL: false } // Avoid duplicate OTEL spans
  );
};
```

❌ **Don't start traces without stopping them**:

```typescript
// ❌ Wrong - Memory leak, never stopped
const MyComponent = () => {
  const { startTrace } = usePerformanceTracker(
    SPAN_KEYS.DATA_PROCESSING,
    'MyComponent'
  );

  useEffect(() => {
    startTrace();
    // Never stopped - memory leak!
  }, []);
};
```

✅ **Do always stop traces**:

```typescript
// ✅ Correct - Always stop after operation
const MyComponent = () => {
  const { startTrace, stopTrace } = usePerformanceTracker(
    SPAN_KEYS.DATA_PROCESSING,
    'MyComponent'
  );

  useEffect(() => {
    startTrace();

    const loadData = async () => {
      try {
        await fetchData();
      } finally {
        stopTrace(); // Always stopped
      }
    };

    loadData();
  }, []);
};
```

❌ **Don't apply onLayout to conditional components**:

```typescript
// ❌ Wrong - onLayout never fires if content not shown
const MyScreen = () => {
  const { measureTTROnLayout } = useTimeToRender({ traceName: 'MyScreen' });
  const [showContent, setShowContent] = useState(false);

  return (
    <View>
      {showContent && <View onLayout={measureTTROnLayout}>...</View>}
    </View>
  );
};
```

✅ **Do apply onLayout to root container**:

```typescript
// ✅ Correct - Root container always renders
const MyScreen = () => {
  const { measureTTROnLayout } = useTimeToRender({ traceName: 'MyScreen' });
  const [showContent, setShowContent] = useState(false);

  return (
    <View onLayout={measureTTROnLayout}>
      {showContent && <View>...</View>}
    </View>
  );
};
```

❌ **Don't use native PerformanceTracker directly**:

```typescript
// ❌ Wrong - Missing OTEL integration and cleanup
import { SharedModulesPerformanceTracker } from '@libs/native-modules/performance-tracker';

const MyComponent = () => {
  useEffect(() => {
    SharedModulesPerformanceTracker.start('MyTrace'); // Don't do this
    // Missing: OTEL span, cleanup, error handling
  }, []);
};
```

✅ **Do always use React hooks**:

```typescript
// ✅ Correct - Proper React integration
import { usePerformanceTracker } from '@libs/observability';

const MyComponent = () => {
  const { startTrace, stopTrace } = usePerformanceTracker(
    SPAN_KEYS.DATA_PROCESSING,
    'MyTrace'
  );
  // Provides: OTEL integration, cleanup, error handling
};
```

## Testing Performance Monitoring

### Mock Performance Hooks

```typescript
import { render, waitFor } from '@testing-library/react-native';
import { ProductDetailsScreen } from './ProductDetailsScreen';

// Mock all performance hooks
jest.mock('@libs/observability', () => ({
  useTimeToRender: jest.fn(() => ({
    measureTTROnLayout: jest.fn(),
  })),
  useTimeToInteractivity: jest.fn(),
  usePerformanceTracker: jest.fn(() => ({
    startTrace: jest.fn(),
    stopTrace: jest.fn(),
    recordUserInfo: jest.fn(),
    incrementMetric: jest.fn(),
  })),
}));

// Mock data fetching
jest.mock('@data-access/products', () => ({
  fetchProduct: jest.fn(() =>
    Promise.resolve({
      id: '123',
      name: 'Test Product',
      variants: [{}, {}],
    })
  ),
}));

describe('ProductDetailsScreen', () => {
  it('should render without creating performance traces', async () => {
    const { getByText } = render(<ProductDetailsScreen productId="123" />);

    await waitFor(() => {
      expect(getByText('Test Product')).toBeDefined();
    });

    // Test passes without creating actual traces
  });

  it('should call recordUserInfo with product data', async () => {
    const mockRecordUserInfo = jest.fn();
    const { usePerformanceTracker } = require('@libs/observability');

    usePerformanceTracker.mockReturnValue({
      recordUserInfo: mockRecordUserInfo,
      startTrace: jest.fn(),
      stopTrace: jest.fn(),
      incrementMetric: jest.fn(),
    });

    render(<ProductDetailsScreen productId="123" />);

    await waitFor(() => {
      expect(mockRecordUserInfo).toHaveBeenCalledWith({
        productId: '123',
        variantCount: 2,
      });
    });
  });
});
```

**Key patterns:**
- Mock `useTimeToRender`, `useTimeToInteractivity`, `usePerformanceTracker`
- Return mock functions for all methods
- Verify hooks are called correctly
- Verify attributes passed to recordUserInfo
- Mock data dependencies to control test data

**Why**: Mocking performance hooks prevents actual traces from being created during tests while still allowing you to verify that components integrate correctly with the performance monitoring system.

**Production Example**: `git-resources/shared-mobile-modules/src/features/country-selection/CountrySelection.spec.tsx:24`

### Test Native + OTEL Integration

```typescript
import { renderHook } from '@testing-library/react-native';
import { mockTracerProvider } from 'jest-utils';
import { SharedModulesPerformanceTracker } from '@libs/native-modules/performance-tracker';
import { usePerformanceTracker } from '@libs/observability';
import { SPAN_KEYS } from '@libs/tracing';

describe('usePerformanceTracker', () => {
  const mockSpanExporter = mockTracerProvider();

  beforeEach(() => {
    mockSpanExporter.reset();
    jest.clearAllMocks();
  });

  it('should start native trace and OTEL span', () => {
    const mockStart = jest.spyOn(SharedModulesPerformanceTracker, 'start');

    const { result } = renderHook(() =>
      usePerformanceTracker(SPAN_KEYS.SESSION, 'testTrace')
    );

    result.current.startTrace();

    // Verify native trace started
    expect(mockStart).toHaveBeenCalledWith('testTrace');

    // Verify no finished spans yet
    const spans = mockSpanExporter.getFinishedSpans();
    expect(spans.length).toBe(0); // Span not finished yet
  });

  it('should stop native trace and OTEL span', () => {
    const mockStop = jest.spyOn(SharedModulesPerformanceTracker, 'stop');

    const { result } = renderHook(() =>
      usePerformanceTracker(SPAN_KEYS.SESSION, 'testTrace')
    );

    result.current.startTrace();
    result.current.stopTrace();

    // Verify native trace stopped
    expect(mockStop).toHaveBeenCalledWith('testTrace');

    // Verify OTEL span finished
    const spans = mockSpanExporter.getFinishedSpans();
    expect(spans.length).toBe(1);
    expect(spans[0].name).toBe('testTrace');
    expect(spans[0].attributes).toEqual(
      expect.objectContaining({
        event_type: 'performance_tracker',
      })
    );
  });

  it('should record user info in native trace and OTEL span', () => {
    const mockRecord = jest.spyOn(SharedModulesPerformanceTracker, 'record');

    const { result } = renderHook(() =>
      usePerformanceTracker(SPAN_KEYS.SESSION, 'testTrace')
    );

    const userInfo = { userId: '123', country: 'US' };

    result.current.startTrace();
    result.current.recordUserInfo(userInfo);
    result.current.stopTrace();

    // Verify native record called
    expect(mockRecord).toHaveBeenCalledWith({
      traceName: 'testTrace',
      userInfo,
    });

    // Verify OTEL span attributes
    const spans = mockSpanExporter.getFinishedSpans();
    expect(spans[0].attributes).toEqual(
      expect.objectContaining({
        userId: '123',
        country: 'US',
      })
    );
  });
});
```

**Key patterns:**
- mockTracerProvider() for OTEL span testing
- Spy on SharedModulesPerformanceTracker methods
- Verify both native and OTEL calls
- getFinishedSpans() to retrieve recorded spans
- Test with `useOTEL: true` (default)

**Why**: Testing both native and OTEL integration ensures dual tracking works correctly and attributes are synced.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/observability/usePerformanceTracker.spec.ts:1`

### Test OTEL Disabled Mode

```typescript
it('should only start native trace when OTEL disabled', () => {
  const mockStart = jest.spyOn(SharedModulesPerformanceTracker, 'start');

  const { result } = renderHook(() =>
    usePerformanceTracker(SPAN_KEYS.SESSION, 'testTrace', { useOTEL: false })
  );

  result.current.startTrace();

  // Verify native trace started
  expect(mockStart).toHaveBeenCalledWith('testTrace');

  // Verify NO OTEL spans created
  const spans = mockSpanExporter.getFinishedSpans();
  expect(spans.length).toBe(0);
});
```

**Why**: Testing with `useOTEL: false` ensures native-only mode works when avoiding duplicate OTEL spans.

## Performance Considerations

### Minimize onLayout Calls

```typescript
// ❌ Avoid - onLayout on every list item
<FlatList
  data={items}
  renderItem={({ item }) => (
    <View onLayout={measureTTROnLayout}> {/* Called for every item! */}
      <Text>{item.name}</Text>
    </View>
  )}
/>

// ✅ Better - onLayout on FlatList container
<FlatList
  onLayout={measureTTROnLayout} // Called once
  data={items}
  renderItem={({ item }) => (
    <View>
      <Text>{item.name}</Text>
    </View>
  )}
/>
```

**Why**: onLayout callbacks have performance overhead. Apply to root container only.

### Avoid Excessive Metric Recording

```typescript
// ❌ Avoid - Recording metrics in tight loop
items.forEach((item) => {
  incrementMetric({ metricName: 'item_processed', value: 1 });
});

// ✅ Better - Record aggregate metrics
incrementMetric({ metricName: 'items_processed', value: items.length });
```

**Why**: Each metric call has overhead. Batch metrics when possible.

## Quick Reference

**useTimeToRender:**
```typescript
const { measureTTROnLayout } = useTimeToRender({
  traceName: 'ScreenName',
  autoStart: true,
});

<View onLayout={measureTTROnLayout}>...</View>
```

**useTimeToInteractivity:**
```typescript
useTimeToInteractivity({
  traceName: 'ScreenName',
  autoStart: true,
});
```

**usePerformanceTracker:**
```typescript
const { startTrace, stopTrace, recordUserInfo, incrementMetric } =
  usePerformanceTracker(SPAN_KEYS.DATA_PROCESSING, 'TraceName', {
    useOTEL: false, // Optional: disable OTEL to avoid duplicates
  });

startTrace();
recordUserInfo({ userId: '123' });
incrementMetric({ metricName: 'items_loaded', value: 10 });
stopTrace();
```

**Testing:**
```typescript
jest.mock('@libs/observability', () => ({
  useTimeToRender: jest.fn(() => ({ measureTTROnLayout: jest.fn() })),
  useTimeToInteractivity: jest.fn(),
  usePerformanceTracker: jest.fn(() => ({
    startTrace: jest.fn(),
    stopTrace: jest.fn(),
    recordUserInfo: jest.fn(),
    incrementMetric: jest.fn(),
  })),
}));
```

**Key Libraries:**
- React Native 0.75.4
- @opentelemetry/api 2.0.1
- Native PerformanceTracker module

For production examples, see [references/examples.md](references/examples.md).
