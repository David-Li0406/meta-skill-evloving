# Tracing - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating OpenTelemetry tracing patterns.

## Example 1: useTracer Core Hook

**File**: `libs/tracing/useTracer.ts`

This is the core React hook that provides OpenTelemetry tracing utilities with automatic vital attributes injection.

```typescript
import { useMemo } from 'react';

import { TRACER_KEYS } from './constants';
import { getTracer } from './getTracer';
import type { TracerUtilsResult } from './types';
import { useTracingContext } from './TracingProvider';
import { useVitalAttributes } from './useVitalAttributes';

/**
 * Hook that provides OpenTelemetry tracing utilities.
 *
 * Automatically injects vital attributes (country, locale, customerID) into all spans.
 * Combines context attributes from TracingProvider with vital attributes.
 *
 * @param tracerName - Optional tracer name, defaults to REACT_APP
 * @returns TracerUtilsResult with startSpan, withSpan, createEventSpan
 */
export const useTracer = (
  tracerName: string = TRACER_KEYS.REACT_APP
): TracerUtilsResult => {
  const tracingContext = useTracingContext();
  const contextAttributes = tracingContext?.attributes;
  const span = tracingContext?.span;

  // Get vital attributes (country, locale, customerID) from separate hook
  const vitalAttributesFromHook = useVitalAttributes();

  const tracerUtils = useMemo(() => {
    // Combine context attributes with vital attributes
    const allAttributes = {
      ...contextAttributes,
      ...vitalAttributesFromHook,
    };

    return getTracer(tracerName, span, allAttributes);
  }, [tracerName, span, contextAttributes, vitalAttributesFromHook]);

  return tracerUtils;
};
```

**Key patterns demonstrated:**
- useMemo to prevent re-creation on every render
- useTracingContext() provides parent span and context attributes
- useVitalAttributes() provides country, locale, customerID automatically
- Combines context + vital attributes for all spans
- Returns TracerUtilsResult: { tracer, startSpan, withSpan, createEventSpan }

## Example 2: getTracer Core Implementation

**File**: `libs/tracing/getTracer.ts`

This provides the core tracing utilities: startSpan, withSpan, createEventSpan.

```typescript
import type { Attributes, Span, Tracer } from '@opentelemetry/api';
import { SpanStatusCode, context, trace } from '@opentelemetry/api';

import { SessionManager } from './SessionManager';
import type { SpanKey, SpanOptions, TracerUtilsResult } from './types';

/**
 * Core tracer implementation providing span creation utilities.
 *
 * @param tracerName - Name of the tracer (e.g., 'react-app')
 * @param contextSpan - Parent span from TracingProvider or session span
 * @param contextAttributes - Attributes to add to all spans (vital + context)
 * @returns TracerUtilsResult with startSpan, withSpan, createEventSpan
 */
export const getTracer = (
  tracerName: string = TRACER_KEYS.REACT_APP,
  contextSpan: Span = SessionManager.getInstance().getSessionSpan(),
  contextAttributes?: Attributes
): TracerUtilsResult => {
  const tracer: Tracer = getTracerProvider().getTracer(tracerName);

  /**
   * Creates and starts a new span with parent context.
   *
   * @param key - Span key from SPAN_KEYS constants (for filtering)
   * @param name - Optional span name (defaults to key)
   * @param options - Span options (attributes, kind, etc.)
   * @param parentSpan - Optional parent span (defaults to contextSpan)
   * @returns Active span
   */
  const startSpan = (
    key: SpanKey,
    name?: string,
    options?: SpanOptions,
    parentSpan?: Span
  ): Span => {
    const parent = parentSpan || contextSpan;
    const parentContext = trace.setSpan(context.active(), parent);

    const finalOptions = {
      ...options,
      attributes: {
        ...contextAttributes, // Vital + context attributes
        ...options?.attributes, // Span-specific attributes
      },
    };

    const span = tracer.startSpan(name || key, finalOptions, parentContext);
    span.setAttribute('span.key', key); // For filtering by key

    return span;
  };

  /**
   * Executes async callback within a span, automatically handling lifecycle.
   *
   * - Creates span
   * - Executes callback with span
   * - Sets status to OK on success
   * - Sets status to ERROR on failure
   * - Ends span in finally block
   *
   * @param key - Span key from SPAN_KEYS
   * @param callback - Async function receiving span
   * @param name - Optional span name
   * @param options - Span options
   * @param parentSpan - Optional parent span
   * @returns Callback result
   */
  const withSpan = async <T>(
    key: SpanKey,
    callback: (span: Span) => Promise<T>,
    name?: string,
    options?: SpanOptions,
    parentSpan?: Span
  ): Promise<T> => {
    const span = startSpan(key, name, options, parentSpan);
    try {
      const result = await callback(span);
      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: error instanceof Error ? error.message : 'Unknown error',
      });
      throw error; // Re-throw for caller
    } finally {
      span.end(); // CRITICAL: Always end span
    }
  };

  /**
   * Creates an instant event span (no duration).
   *
   * Immediately ends span after creation. Used for events like button clicks,
   * state changes, error events.
   *
   * @param key - Span key from SPAN_KEYS
   * @param name - Optional span name
   * @param attributes - Span attributes
   * @param parentSpan - Optional parent span
   * @returns Ended span
   */
  const createEventSpan = (
    key: SpanKey,
    name?: string,
    attributes?: Attributes,
    parentSpan?: Span
  ): Span => {
    const span = startSpan(key, name, { attributes }, parentSpan);
    span.end(); // Immediately end (instant event)
    return span;
  };

  return {
    tracer,
    startSpan,
    withSpan,
    createEventSpan,
  };
};
```

**Key patterns demonstrated:**
- startSpan creates span with parent context from SessionManager
- Merges context attributes (vital + TracingProvider) with span-specific attributes
- span.setAttribute('span.key', key) enables filtering by span key
- withSpan automatically handles try-catch-finally lifecycle
- withSpan sets status to OK on success, ERROR on failure
- createEventSpan immediately ends span (instant events)

## Example 3: useCustomTrace for Long-Running Flows

**File**: `libs/tracing/useCustomTrace.ts`

This hook manages long-running user interactions spanning multiple renders, with automatic cleanup.

```typescript
import type { Span } from '@opentelemetry/api';
import { useCallback, useEffect, useRef } from 'react';

import type { CustomTraceAttributes, SpanKey, SpanOptions } from './types';
import { useTracer } from './useTracer';

/**
 * Hook for long-running user interactions with state-dependent completion.
 *
 * Use cases:
 * - Multi-step checkout flows
 * - Modal interactions
 * - Multi-screen navigation flows
 * - Form submissions with multiple steps
 *
 * Features:
 * - Prevents nested spans (ends previous if start called again)
 * - Automatic cleanup on unmount
 * - Add attributes at start and end
 *
 * @param spanKey - Span key from SPAN_KEYS
 * @returns Tuple [start, end] for explicit control
 */
export const useCustomTrace = (spanKey: SpanKey) => {
  const { startSpan } = useTracer();
  const lastActiveSpan = useRef<{ span: Span; name: string } | null>(null);

  /**
   * Starts a new custom trace.
   *
   * If a span is already active, ends it before starting new one.
   * Prevents nested spans and memory leaks.
   *
   * @param attributes - Initial attributes to set on span
   * @param options - Span options
   * @returns Started span
   */
  const start = useCallback(
    (attributes?: CustomTraceAttributes, options?: SpanOptions) => {
      if (lastActiveSpan.current) {
        // Prevents nested spans by ending previous span
        lastActiveSpan.current.span.end();
      }

      const readableSpanName = getReadableSpanName(spanKey);
      const span = startSpan(spanKey, readableSpanName, options);
      lastActiveSpan.current = { span, name: readableSpanName };

      if (attributes) {
        span.setAttributes(attributes);
      }

      return span;
    },
    [startSpan, spanKey]
  );

  /**
   * Ends the active custom trace.
   *
   * @param attributes - Final attributes to add before ending
   */
  const end = useCallback((attributes?: CustomTraceAttributes) => {
    if (lastActiveSpan.current) {
      if (attributes) {
        // Add final attributes before ending
        Object.entries(attributes).forEach(([key, value]) => {
          lastActiveSpan.current?.span.setAttribute(key, value);
        });
      }
      lastActiveSpan.current.span.end();
    }
    lastActiveSpan.current = null;
  }, []);

  // Ensure any active custom trace span is properly ended on unmount
  useEffect(() => {
    return () => {
      end(); // Auto-cleanup on unmount
    };
  }, [end]);

  return [start, end] as const;
};

/**
 * Converts span key to human-readable name.
 *
 * Example: 'checkout_flow' → 'Checkout Flow'
 */
const getReadableSpanName = (spanKey: SpanKey): string => {
  return spanKey
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};
```

**Key patterns demonstrated:**
- useRef to track active span across renders
- Prevents nested spans by ending previous span if start called again
- Automatic cleanup on unmount via useEffect
- Returns tuple [start, end] for explicit control
- start() adds initial attributes, end() adds final attributes
- Used for multi-step user flows: checkout, modals, navigation

## Example 4: TracingProvider for Context Attributes

**File**: `libs/tracing/TracingProvider.tsx`

This provider cascades context attributes through the component tree and creates a parent span.

```typescript
import type { Attributes, Span } from '@opentelemetry/api';
import { createContext, useContext, useMemo } from 'react';

import type { Squad } from '@libs/governance';

import { SPAN_KEYS } from './spanKeys';
import { useTracer } from './useTracer';

interface TracingContextValue {
  span: Span;
  attributes: Attributes;
}

type TracingProviderProps = {
  children: React.ReactNode;
  moduleName: string;
  moduleType: 'screen' | 'stack' | 'component' | 'feature';
  squad: Squad;
  attributes?: Attributes;
};

const TracingContext = createContext<TracingContextValue | null>(null);

/**
 * Provider that cascades context attributes to all child spans.
 *
 * Use cases:
 * - Wrap screens to add screen name and squad
 * - Wrap navigation stacks to add stack context
 * - Wrap feature components to add feature name
 *
 * Features:
 * - Merges parent attributes with own attributes
 * - Creates event span as parent for all child spans
 * - Adds module metadata: module.name, module.type, screen.name, etc.
 *
 * @param moduleName - Name of the module (e.g., 'checkout', 'cart')
 * @param moduleType - Type of module: screen | stack | component | feature
 * @param squad - Team attribution (e.g., 'conversions-mobile')
 * @param attributes - Additional custom attributes
 */
export const TracingProvider: React.FC<TracingProviderProps> = (props) => {
  const { createEventSpan } = useTracer();
  const parentSpan = useTracingContext()?.span;
  const parentAttributes = useTracingContext()?.attributes;

  const mergedAttributes = useMemo(() => {
    return {
      ...parentAttributes, // Inherit parent attributes
      ...props.attributes, // Own attributes override parent
      squad: props.squad,
      ['module.name']: props.moduleName,
      ['module.type']: props.moduleType,
      [`${props.moduleType}.name`]: props.moduleName,
      // Creates: screen.name, component.name, feature.name, stack.name
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const contextSpan = useMemo(() => {
    const spanName = `${props.moduleType}_${props.moduleName}`;
    // screen_checkout, component_cart, feature_payment

    return createEventSpan(
      SPAN_KEYS.TRACING_PROVIDER,
      spanName,
      mergedAttributes,
      parentSpan
    );
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <TracingContext.Provider
      value={{ span: contextSpan, attributes: mergedAttributes }}
    >
      {props.children}
    </TracingContext.Provider>
  );
};

export const useTracingContext = (): TracingContextValue | null => {
  const context = useContext(TracingContext);
  return context;
};
```

**Key patterns demonstrated:**
- Merges parent attributes with own attributes (child overrides)
- Creates event span as parent for all child spans
- Adds module metadata: `module.name`, `module.type`, `screen.name`, etc.
- Span name pattern: `${moduleType}_${moduleName}` (screen_checkout)
- useContext hook to access parent TracingProvider context
- useMemo to prevent re-creation on every render

## Example 5: withSpan Usage in Event Handler

**File**: `features/country-selection/CountrySelection.tsx`

This example shows using withSpan in an event handler for user interactions.

```typescript
import type { Span } from '@opentelemetry/api';
import { useCallback } from 'react';

import { useTracer, SPAN_KEYS, TracingProvider } from '@libs/tracing';

export const CountrySelection = ({ route, navigation }: CountrySelectionScreenProps) => {
  const { withSpan } = useTracer();

  const onSelectCountry = useCallback(
    (params: CountryList) => {
      withSpan(SPAN_KEYS.ON_SELECT_COUNTRY, async (span: Span) => {
        // Set attributes for debugging
        span.setAttributes({
          locale: params.locale,
          country: params.country,
        });

        // Track analytics event
        trackCountrySelection(data?.locale || null, params.locale);

        // Update country in native config
        await updateCountry(params);

        // Navigate back if possible
        if (navigation.canGoBack()) {
          navigation.goBack();
        }
      });
    },
    [withSpan, trackCountrySelection, updateCountry, navigation, data?.locale]
  );

  return (
    <TracingProvider
      moduleType="screen"
      moduleName="country_selection"
      squad="conversions-mobile"
    >
      <FlatList
        data={countryList}
        renderItem={({ item }) => (
          <CountryItem item={item} onPress={() => onSelectCountry(item)} />
        )}
        testID="country-selection"
      />
    </TracingProvider>
  );
};
```

**Key patterns demonstrated:**
- withSpan in event handler for user interactions
- span.setAttributes() to add context (locale, country)
- Combining analytics tracking + tracing
- TracingProvider wraps screen for context attributes
- Async operations within span callback (updateCountry, navigation)
- useCallback with all dependencies

## Example 6: Combining Analytics + Tracing

**File**: `modules/programs/screens/programs-home/hooks/useProgramsHomeAnalytics.ts`

This example demonstrates combining analytics tracking with OpenTelemetry tracing.

```typescript
import { useEffect } from 'react';

import { useAnalyticsTracker, Tribe } from '@libs/analytics';
import { AnalyticsEventDestination } from '@libs/native-modules/analytics-tracker';
import { useTracer, SPAN_KEYS } from '@libs/tracing';

import type { CustomWebViewProps } from '@components/webview';

const EVENT_BASE = {
  screenName: 'Programs home',
  tribe: Tribe.ShoppingExperience,
};

/**
 * Hook combining analytics tracking with OpenTelemetry tracing.
 *
 * - Tracks pageView analytics event on mount
 * - Creates event spans for WebView messages
 * - Error handling with tracing
 */
export const useProgramsHomeAnalytics = () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();
  const { createEventSpan } = useTracer();

  // Track screen view on mount
  useEffect(() => {
    trackAnalyticsEvent({
      defaultParams: {
        eventName: 'ProgramsHome_ScreenShow',
        eventAction: 'pageView',
        eventLabel: 'RNSM | Programs | Programs home Screen',
        screenName: EVENT_BASE.screenName,
        tribe: EVENT_BASE.tribe,
      },
      destinations: [AnalyticsEventDestination.Firebase],
      parameters: {},
    });
  }, [trackAnalyticsEvent]);

  /**
   * Handles WebView messages and creates event spans for tracking.
   */
  const trackMealSelectionsSaved: CustomWebViewProps['onMessageCallback'] = (
    event
  ) => {
    try {
      const { type, payload = {} } = JSON.parse(event.nativeEvent.data);

      if (type === 'track' && payload?.event_name === 'SelectMeals_Submit') {
        // Create event span for user action
        createEventSpan(SPAN_KEYS.USER_ACTION, 'select_meals_submit', payload);
      }
    } catch (error) {
      // Create event span for error
      createEventSpan(
        SPAN_KEYS.WEBVIEW_MESSAGE_ERROR,
        'webview_error_message',
        {
          error: error instanceof Error ? error.message : String(error),
        }
      );
    }

    return { shouldContinue: true };
  };

  return { trackMealSelectionsSaved };
};
```

**Key patterns demonstrated:**
- Combining useAnalyticsTracker + useTracer
- createEventSpan for instant events (button click, WebView message)
- Error handling with createEventSpan
- WebView message parsing with tracing
- Analytics event on mount with useEffect

## Example 7: SPAN_KEYS Constants

**File**: `libs/tracing/spanKeys.ts`

This defines SPAN_KEYS constants and naming conventions for low cardinality.

```typescript
/**
 * Span key constants for low cardinality enforcement.
 *
 * Always use SPAN_KEYS constants instead of string literals.
 * This ensures low cardinality (limited unique values).
 *
 * High cardinality (many unique values) overwhelms tracing backends.
 */
export const SPAN_KEYS = {
  // Session spans
  SESSION: 'session',
  AUTH_GUARD: 'auth_guard',
  SESSION_BACKGROUND: 'session_background',
  SESSION_FOREGROUND: 'session_foreground',

  // User action spans
  USER_ACTION: 'user_action',
  ON_SELECT_COUNTRY: 'button_click_select_country',

  // Network spans
  FETCH: 'fetch',
  GRAPHQL_OPERATION: 'graphql.operation',

  // Error spans
  ERROR_BOUNDARY: 'error_boundary',
  WEBVIEW_LOADING_ERROR: 'webview_loading_error',
  WEBVIEW_MESSAGE_ERROR: 'webview_message_error',

  // Provider spans
  TRACING_PROVIDER: 'tracing_provider',

  // State spans
  STATE_CHANGE: 'state_change',
  TRANSLATION_MISSING: 'translation_missing',

  // Data spans
  API_REQUEST: 'api_request',
  DATA_PROCESSING: 'data_processing',

  // Flow spans
  CHECKOUT_FLOW: 'checkout_flow',
} as const;

export type GeneralSpanKeys = (typeof SPAN_KEYS)[keyof typeof SPAN_KEYS];

/**
 * Type-safe span naming patterns.
 *
 * Pattern: {domain}_{component}_{operation} in snake_case
 *
 * Examples:
 * - ui_button_click
 * - api_graphql_query
 * - data_cache_update
 * - background_sync_job
 */
export type UIOperations = `ui_${('interaction' | 'rendering' | 'navigation')}_${string}`;
export type APIOperations = `api_${('request' | 'response' | 'graphql')}_${string}`;
export type DataOperations = `data_${('query' | 'update' | 'transform' | 'cache')}_${string}`;
export type BackgroundOperations = `background_${('job' | 'sync')}_${string}`;

export type SpanKey =
  | GeneralSpanKeys
  | UIOperations
  | APIOperations
  | DataOperations
  | BackgroundOperations;
```

**Key patterns demonstrated:**
- Predefined keys for common operations
- Type-safe span naming with union types
- Naming pattern: `{domain}_{component}_{operation}` in snake_case
- Hierarchical organization: ui_, api_, data_, background_
- Low cardinality enforcement via constants
- TypeScript types for compile-time validation

## Example 8: Testing Tracing

**File**: `libs/tracing/getTracer.spec.ts`

This example shows comprehensive testing of tracing utilities.

```typescript
import { SpanStatusCode } from '@opentelemetry/api';
import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';

import { mockTracerProvider } from 'jest-utils';

import { getTracer } from './getTracer';
import { SPAN_KEYS } from './spanKeys';

describe('getTracer', () => {
  const mockSpanExporter = mockTracerProvider();

  beforeEach(() => {
    mockSpanExporter.reset();
  });

  describe('createEventSpan', () => {
    it('creates instant event span with no duration', () => {
      const { createEventSpan } = getTracer();

      const span = createEventSpan(SPAN_KEYS.USER_ACTION, 'button_click', {
        button_id: 'submit',
        screen: 'checkout',
      });

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(1);

      const recordedSpan = spans[0] as ReadableSpan;
      expect(recordedSpan.name).toBe('button_click');
      expect(recordedSpan.attributes).toEqual(
        expect.objectContaining({
          'span.key': 'user_action',
          button_id: 'submit',
          screen: 'checkout',
        })
      );

      // Verify span was immediately ended (duration close to 0)
      const duration = recordedSpan.duration[0]; // seconds part
      expect(duration).toBeLessThan(1);
    });
  });

  describe('withSpan', () => {
    it('creates span with duration and sets status to OK on success', async () => {
      const { withSpan } = getTracer();

      const result = await withSpan(
        SPAN_KEYS.API_REQUEST,
        async (span) => {
          span.setAttribute('endpoint', '/api/users');
          return { data: 'success' };
        },
        'fetch_users'
      );

      expect(result).toEqual({ data: 'success' });

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(1);

      const recordedSpan = spans[0] as ReadableSpan;
      expect(recordedSpan.name).toBe('fetch_users');
      expect(recordedSpan.status.code).toBe(SpanStatusCode.OK);
      expect(recordedSpan.attributes).toEqual(
        expect.objectContaining({
          'span.key': 'api_request',
          endpoint: '/api/users',
        })
      );
    });

    it('sets status to ERROR and re-throws on failure', async () => {
      const { withSpan } = getTracer();

      await expect(
        withSpan(
          SPAN_KEYS.API_REQUEST,
          async (span) => {
            span.setAttribute('endpoint', '/api/users');
            throw new Error('Network error');
          },
          'fetch_users'
        )
      ).rejects.toThrow('Network error');

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(1);

      const recordedSpan = spans[0] as ReadableSpan;
      expect(recordedSpan.status.code).toBe(SpanStatusCode.ERROR);
      expect(recordedSpan.status.message).toBe('Network error');
    });

    it('always ends span even if callback throws', async () => {
      const { withSpan } = getTracer();

      try {
        await withSpan(SPAN_KEYS.API_REQUEST, async () => {
          throw new Error('Error');
        });
      } catch {
        // Expected error
      }

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(1); // Span was ended despite error
    });
  });

  describe('startSpan', () => {
    it('creates span with manual lifecycle control', () => {
      const { startSpan } = getTracer();

      const span = startSpan(SPAN_KEYS.DATA_PROCESSING, 'transform_data', {
        attributes: {
          operation: 'transform',
          items_count: 100,
        },
      });

      // Manually add attributes
      span.setAttribute('processing_stage', 'validation');

      // Manually end span
      span.end();

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(1);

      const recordedSpan = spans[0] as ReadableSpan;
      expect(recordedSpan.name).toBe('transform_data');
      expect(recordedSpan.attributes).toEqual(
        expect.objectContaining({
          'span.key': 'data_processing',
          operation: 'transform',
          items_count: 100,
          processing_stage: 'validation',
        })
      );
    });
  });

  describe('context attributes', () => {
    it('merges context attributes with span attributes', () => {
      const contextAttributes = {
        country: 'US',
        locale: 'en-US',
        'customer.id': '123',
      };

      const { createEventSpan } = getTracer(
        'test-tracer',
        undefined,
        contextAttributes
      );

      createEventSpan(SPAN_KEYS.USER_ACTION, 'button_click', {
        button_id: 'submit',
      });

      const spans = mockSpanExporter.getFinishedSpans();
      const recordedSpan = spans[0] as ReadableSpan;

      expect(recordedSpan.attributes).toEqual(
        expect.objectContaining({
          country: 'US',
          locale: 'en-US',
          'customer.id': '123',
          button_id: 'submit',
        })
      );
    });
  });
});
```

**Key patterns demonstrated:**
- mockTracerProvider() for OTEL span testing
- getFinishedSpans() to retrieve recorded spans
- Verify span name, attributes, status, duration
- Test createEventSpan: instant event with no duration
- Test withSpan: automatic lifecycle, error handling, always ends span
- Test startSpan: manual control, incremental attributes
- Test context attributes merging
- expect.objectContaining() for partial matching

## Summary

The YourCompany codebase consistently follows these tracing patterns:

1. **useTracer hook** provides createEventSpan, withSpan, startSpan
2. **useCustomTrace** for long-running user flows with auto-cleanup
3. **TracingProvider** cascades context attributes through component tree
4. **SPAN_KEYS constants** enforce low cardinality
5. **Vital attributes** auto-injected: country, locale, customerID
6. **Hierarchical attribute naming**: snake_case with namespaces (http.request.method)
7. **Dynamic data in attributes**, never in span names
8. **withSpan for most async operations** (automatic lifecycle)
9. **startSpan for complex operations** (manual control, incremental attributes)
10. **Comprehensive testing** with mockTracerProvider

These patterns ensure consistent, performant distributed tracing with low cardinality and rich context throughout the app.
