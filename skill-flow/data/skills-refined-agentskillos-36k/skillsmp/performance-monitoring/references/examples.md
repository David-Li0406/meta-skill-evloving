# Performance Monitoring - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating performance monitoring patterns.

## Example 1: usePerformanceTracker Core Implementation

**File**: `libs/observability/usePerformanceTracker.ts`

This is the core performance tracking hook providing dual native + OTEL tracking.

```typescript
import type { Span } from '@opentelemetry/api';
import { useRef } from 'react';

import { SharedModulesPerformanceTracker } from '@libs/native-modules/performance-tracker';
import { useTracer, type SpanKey } from '@libs/tracing';

interface UsePerformanceTrackerOptions {
  /**
   * Whether to use OpenTelemetry (OTEL) tracing.
   * @default true
   */
  useOTEL: boolean;
}

/**
 * A hook that provides performance tracking functionality using both native PerformanceTracker
 * and OpenTelemetry (OTEL) tracing.
 *
 * @param spanKey - The span key to categorize the type of operation being traced.
 * @param traceName - The name of the trace to be used in both native and OTEL tracing.
 * @param options - Configuration options for the performance tracker.
 *
 * @remarks
 * By default, this hook enables OTEL tracing for all users. This provides out-of-the-box
 * observability with minimal setup required.
 *
 * However, it also offers the flexibility to opt-out of OTEL tracing. This can be useful in scenarios where:
 * 1. You want full control over the tracing implementation.
 * 2. You're using this hook in conjunction with more specific tracing hooks like `useTimeToRender`
 *    or `useTimeToInteractivity`, which may implement their own custom OTEL tracing with more
 *    accurate tracer names.
 *
 * To opt-out of OTEL tracing, pass `{ useOTEL: false }` in the options parameter.
 *
 * @example
 * // Using default behavior (OTEL tracing enabled)
 * const tracker = usePerformanceTracker(SPAN_KEYS.USER_ACTION, 'MyComponent');
 *
 * // Opting out of OTEL tracing
 * const trackerWithoutOTEL = usePerformanceTracker(SPAN_KEYS.USER_ACTION, 'MyComponent', { useOTEL: false });
 */
export const usePerformanceTracker = (
  spanKey: SpanKey,
  traceName: string,
  options: UsePerformanceTrackerOptions = { useOTEL: true }
) => {
  const { start, stop, record, incrementMetric } =
    SharedModulesPerformanceTracker;
  const { startSpan } = useTracer(traceName);
  const spanRef = useRef<Span | null>(null);

  const { useOTEL } = options;

  return {
    startTrace: () => {
      start(traceName);
      if (useOTEL) {
        spanRef.current = startSpan(spanKey, traceName, {
          attributes: {
            event_type: 'performance_tracker',
          },
        });
      }
    },
    stopTrace: () => {
      stop(traceName);
      if (useOTEL && spanRef.current) {
        spanRef.current.end();
        spanRef.current = null;
      }
    },
    recordUserInfo: (userInfo: object) => {
      record({ traceName, userInfo });
      if (useOTEL && spanRef.current) {
        spanRef.current.setAttributes(
          userInfo as Record<string, string | number | boolean>
        );
      }
    },
    incrementMetric: ({
      metricName,
      value,
    }: {
      metricName: string;
      value: number;
    }) => {
      incrementMetric({ traceName, metricName, value });
      if (useOTEL && spanRef.current) {
        spanRef.current.setAttribute(metricName, value);
      }
    },
  };
};
```

**Key patterns demonstrated:**
- useRef to track active OTEL span across renders
- Dual tracking: SharedModulesPerformanceTracker (native) + OTEL span
- `useOTEL` option to disable OTEL tracking (avoid duplicates)
- startTrace: starts native trace + optionally creates OTEL span
- stopTrace: stops native trace + optionally ends OTEL span
- recordUserInfo: adds attributes to both native and OTEL
- incrementMetric: records counters in both native and OTEL
- spanRef.current stores active span for attribute updates

## Example 2: useTimeToRender Core Implementation

**File**: `libs/observability/useTimeToRender.ts`

This hook measures "time to render" using the onLayout event.

```typescript
import { useEffect, useCallback, useRef } from 'react';
import type { LayoutChangeEvent } from 'react-native';

import { usePerformanceTracker } from './usePerformanceTracker';

interface UseTimeToRenderProps {
  /**
   * @context The trace name to use for the performance tracker.
   * This will be suffixed with "_ttr" to create a unique trace ID.
   */
  traceName: string;
  autoStart?: boolean;
}

/**
 * @context Measures "time to render" using onLayout.
 * Will start a performance trace on mount and stop when the View's layout finishes.
 */
export const useTimeToRender = ({
  traceName,
  autoStart = true,
}: UseTimeToRenderProps) => {
  const { startTrace, stopTrace } = usePerformanceTracker(
    'ui_rendering_screen_ttr',
    traceName
  );
  const startTimeRef = useRef<number | null>(null);

  useEffect(() => {
    if (autoStart) {
      startTrace();

      // Log the start time for debugging purposes
      if (__DEV__) {
        const now = performance.now();
        startTimeRef.current = now;
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /**
   * @context We expose this callback to be passed into the screen's
   * View container's onLayout prop.
   */
  const onLayout = useCallback(
    (_: LayoutChangeEvent) => {
      stopTrace();

      if (__DEV__) {
        const now = performance.now();

        if (startTimeRef.current !== null) {
          console.log(
            `#DEBUG [${traceName}] Time To Render: ${(
              now - startTimeRef.current
            ).toFixed(2)} ms`
          );
          startTimeRef.current = null;
        }
      }
    },
    [stopTrace, traceName]
  );

  return { measureTTROnLayout: onLayout };
};
```

**Key patterns demonstrated:**
- Uses usePerformanceTracker internally with span key 'ui_rendering_screen_ttr'
- autoStart defaults to true - starts trace on mount
- startTimeRef tracks start time for dev logging
- onLayout callback stops trace when View layout completes
- Development logging with `#DEBUG` prefix and milliseconds
- useCallback with dependencies for stable callback reference
- Returns measureTTROnLayout to attach to View's onLayout prop

## Example 3: useTimeToInteractivity Core Implementation

**File**: `libs/observability/useTimeToInteractivity.ts`

This hook measures "time to interactivity" using InteractionManager.

```typescript
import { useEffect, useRef } from 'react';
import { InteractionManager } from 'react-native';

import { usePerformanceTracker } from './usePerformanceTracker';

interface UseTimeToInteractivityProps {
  /**
   * @context The trace name to use for the performance tracker.
   * This will be suffixed with "_tti" to create a unique trace ID.
   */
  traceName: string;
  autoStart?: boolean;
}

/**
 * @context Measures "time to interactivity" using `InteractionManager`.
 * Will start a performance trace on mount and stop after interactions complete.
 */
export const useTimeToInteractivity = ({
  traceName,
  autoStart = true,
}: UseTimeToInteractivityProps) => {
  const { startTrace, stopTrace } = usePerformanceTracker(
    'ui_interaction_screen_tti',
    traceName
  );
  const startTimeRef = useRef<number | null>(null);

  useEffect(() => {
    if (autoStart) {
      startTrace();

      // Log the start time for debugging purposes
      if (__DEV__) {
        const now = performance.now();
        startTimeRef.current = now;
      }
    }

    const interactionHandle = InteractionManager.runAfterInteractions(() => {
      stopTrace();

      if (__DEV__) {
        const now = performance.now();

        if (startTimeRef.current !== null) {
          console.log(
            `#DEBUG [${traceName}] Time To Interactivity: ${(
              now - startTimeRef.current
            ).toFixed(2)} ms`
          );
          startTimeRef.current = null;
        }
      }
    });

    return () => {
      interactionHandle.cancel();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
};
```

**Key patterns demonstrated:**
- Uses usePerformanceTracker internally with span key 'ui_interaction_screen_tti'
- InteractionManager.runAfterInteractions() waits for all interactions to complete
- autoStart defaults to true - starts trace on mount
- stopTrace called after all interactions complete
- Development logging with `#DEBUG` prefix
- Cleanup: interactionHandle.cancel() on unmount
- No callback needed (fully automatic)

## Example 4: Complete Screen with TTR + TTI

**File**: `features/country-selection/CountrySelection.tsx`

This example shows a complete screen using both TTR and TTI hooks.

```typescript
import type { Span } from '@opentelemetry/api';
import { useMemo } from 'react';
import type { ListRenderItemInfo } from 'react-native';
import { FlatList } from 'react-native';

import { AppConfigOperations } from '@operations';

import { AppConfigDataAccess } from '@data-access/native';

import { useTimeToInteractivity, useTimeToRender } from '@libs/observability';
import { SPAN_KEYS, TracingProvider, useTracer } from '@libs/tracing';
import { PlatformStatusBar } from '@libs/utils';

import { useZestStyles } from '@zest/react-native';

import { CountrySelectionItem } from './components/country-selection-item';
import { COUNTRY_SELECTION_TRACE_ID } from './constants';
import { useCountrySelectionAnalytics } from './hooks/useCountrySelectionAnalytics';
import { selectSortedCountryList } from './selector';
import { stylesConfig } from './styles';
import type { CountryList, CountrySelectionScreenProps } from './types';

export const CountrySelection = ({
  route,
  navigation,
}: CountrySelectionScreenProps) => {
  const { withSpan } = useTracer();

  // Performance Observability hooks
  const { measureTTROnLayout } = useTimeToRender({
    traceName: COUNTRY_SELECTION_TRACE_ID, // 'CountrySelection'
  });
  useTimeToInteractivity({ traceName: COUNTRY_SELECTION_TRACE_ID });

  const countryList = useMemo(
    () => selectSortedCountryList(route.params?.countryList || []),
    [route.params?.countryList]
  );

  const styles = useZestStyles(stylesConfig);

  const { trackCountrySelection } = useCountrySelectionAnalytics();

  const { data } = AppConfigDataAccess.queries.useCurrentCountryState();
  const {
    mutate: updateCountry,
    variables: optimisticState,
    isPending,
  } = AppConfigOperations.useMutateCountry();

  const currentCountryState = isPending ? optimisticState : data;

  const onSelectCountry = (params: CountryList) => {
    withSpan(SPAN_KEYS.ON_SELECT_COUNTRY, async (span: Span) => {
      span.setAttributes({
        locale: params.locale,
        country: params.country,
      });
      trackCountrySelection(data?.locale || null, params.locale);
      await updateCountry(params);
      if (navigation.canGoBack()) {
        navigation.goBack();
      }
    });
  };

  const renderItem = ({ item }: ListRenderItemInfo<CountryList>) => (
    <CountrySelectionItem
      country={item.country}
      locale={item.locale}
      onSelectCountry={onSelectCountry}
      selected={currentCountryState?.locale === item.locale}
      isOptimisticSelection={
        isPending && optimisticState.locale === item.locale
      }
    />
  );

  return (
    <TracingProvider
      moduleType="screen"
      moduleName="country_selection"
      squad="conversions-mobile"
    >
      <>
        <PlatformStatusBar />
        <FlatList
          onLayout={measureTTROnLayout}
          data={countryList}
          renderItem={renderItem}
          contentContainerStyle={styles.contentContainerStyle}
          style={styles.containerStyle}
          testID="country-selection"
        />
      </>
    </TracingProvider>
  );
};
```

**Key patterns demonstrated:**
- useTimeToRender + useTimeToInteractivity with same traceName
- measureTTROnLayout attached to FlatList onLayout prop
- TTI fully automatic (no callback needed)
- TracingProvider wraps component for OTEL context
- withSpan for user interaction tracing (separate from TTR/TTI)
- Constants for trace names (COUNTRY_SELECTION_TRACE_ID)

## Example 5: Screen with TTR + TTI + Custom Metrics

**File**: `modules/programs/screens/programs-home/ProgramsHome.tsx`

This example shows comprehensive performance monitoring with TTR, TTI, and custom metrics tracking.

```typescript
import { useRef, useState } from 'react';
import { View, SafeAreaView } from 'react-native';
import type { WebView as RNWebView } from 'react-native-webview';

import { AppConfigDataAccess } from '@data-access/native';
import { useCustomerSubscriptions } from '@data-access/query/customer';

import { FactorFormEntrypoint } from '@features/factor-form-entrypoint';
import { WebView } from '@features/webview';

import { Tribe } from '@libs/analytics';
import { useTimeToInteractivity, useTimeToRender } from '@libs/observability';
import { DefaultScreenProvider } from '@libs/tracing';

import { ProgramsExperienceSwitcher } from '@modules/programs/screens/programs-home/components/programs-experience-switcher/ProgramsExperienceSwitcher';
import { ProgramsReactivationButton } from '@modules/programs/screens/programs-home/components/reactivation-button/ProgramsReactivationButton';

import { Spinner, useZestStyles } from '@zest/react-native';

import { createScreenOptions } from '../../stacks/programs/screenOptions';

import {
  APP_VERSION,
  PROGRAMS_HOME_TRACE_ID,
  SPINNER_TEST_ID,
  WEBVIEW_CONTAINER_TEST_ID,
  WEBVIEW_TEST_ID,
} from './constants';
import { useHasProgramsAndVMSSubscriptions } from './hooks/useHasProgramsAndVMSSubscriptions';
import { useProgramsHomeAnalytics } from './hooks/useProgramsHomeAnalytics';
import { useProgramsWebview } from './hooks/useProgramsWebview';
import { useReloadProgramHome } from './hooks/useReloadProgramHome';
import { useWebViewStateChange } from './hooks/useWebViewStateChange';
import { stylesConfig } from './styles';

const ProgramsHomeWithProvider = () => {
  const webViewRef = useRef<RNWebView>(null);
  const { getDashboardUrl } = useProgramsWebview();
  const { data: brand, isLoading } =
    AppConfigDataAccess.queries.useBrandState();
  const { data: subscriptionsData, isLoading: isLoadingSubscriptions } =
    useCustomerSubscriptions({});

  // Performance monitoring hooks
  const { measureTTROnLayout } = useTimeToRender({
    traceName: PROGRAMS_HOME_TRACE_ID,
  });
  useTimeToInteractivity({ traceName: PROGRAMS_HOME_TRACE_ID });

  const { trackMealSelectionsSaved } = useProgramsHomeAnalytics();

  const { onWebviewStateChanges, canShowReactivationButton } =
    useWebViewStateChange(webViewRef);

  useReloadProgramHome(webViewRef);
  const shouldShowBrandSwitcher = useHasProgramsAndVMSSubscriptions();
  const [activeTabIndex, setActiveTabIndex] = useState(0);

  const styles = useZestStyles(stylesConfig);

  const shouldShowSpinner = !brand || isLoading || isLoadingSubscriptions;
  const dashboardUrl = getDashboardUrl();

  const returnToPrograms = () => {
    setActiveTabIndex(0);
  };

  return (
    <SafeAreaView style={styles.container}>
      {shouldShowBrandSwitcher && (
        <ProgramsExperienceSwitcher
          activeTabIndex={activeTabIndex}
          setActiveTabIndex={setActiveTabIndex}
        />
      )}
      {shouldShowBrandSwitcher && activeTabIndex === 1 ? (
        <FactorFormEntrypoint returnToFactorMeals={returnToPrograms} />
      ) : (
        <View
          style={styles.container}
          onLayout={measureTTROnLayout}
          testID={WEBVIEW_CONTAINER_TEST_ID}
        >
          {shouldShowSpinner ? (
            <View style={styles.spinnerContainer}>
              <Spinner size="lg" testID={SPINNER_TEST_ID} />
            </View>
          ) : (
            <WebView
              ref={webViewRef}
              source={{
                uri: dashboardUrl,
                headers: {
                  Link: `<${dashboardUrl}>; rel=preconnect`,
                },
              }}
              applicationNameForUserAgent={`${brand}-${APP_VERSION}`}
              webviewDebuggingEnabled
              onNavigationStateChange={onWebviewStateChanges}
              cacheEnabled
              cacheMode="LOAD_CACHE_ELSE_NETWORK"
              testID={WEBVIEW_TEST_ID}
              eventLabel={'RNSM | Programs | Webview Screen'}
              tribe={Tribe.RTEExpansion}
              screenName={'Programs home Screen'}
              onMessageCallback={trackMealSelectionsSaved}
            />
          )}
          {!shouldShowSpinner && canShowReactivationButton && (
            <ProgramsReactivationButton
              subscriptions={subscriptionsData?.items || []}
            />
          )}
        </View>
      )}
    </SafeAreaView>
  );
};

export const ProgramsHome = () => {
  return (
    <DefaultScreenProvider
      moduleType="screen"
      moduleName={'programs-webview'}
      squad={'rte-programs'}
    >
      <ProgramsHomeWithProvider />
    </DefaultScreenProvider>
  );
};

export const ProgramsHomeScreenOptions = createScreenOptions({
  headerShown: false,
});
```

**Key patterns demonstrated:**
- useTimeToRender + useTimeToInteractivity with same trace name
- measureTTROnLayout attached to container View (not WebView)
- Constants for trace IDs (PROGRAMS_HOME_TRACE_ID)
- DefaultScreenProvider wraps component for tracing context
- Conditional rendering with spinner before content loads
- TTR measures when container View layout completes
- TTI measures when all interactions (data loading, animations) complete

## Example 6: Testing usePerformanceTracker

**File**: `libs/observability/usePerformanceTracker.spec.ts`

This example shows comprehensive testing of usePerformanceTracker with both native and OTEL integration.

```typescript
import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';
import { renderHook } from '@testing-library/react-native';

import { mockTracerProvider } from 'jest-utils';

import { SharedModulesPerformanceTracker } from '@libs/native-modules/performance-tracker';
import { SPAN_KEYS } from '@libs/tracing';

import { usePerformanceTracker } from './usePerformanceTracker';

describe('usePerformanceTracker', () => {
  const mockSpanExporter = mockTracerProvider();
  const mockStart = jest.fn();
  const mockStop = jest.fn();
  const mockRecord = jest.fn();
  const mockIncrementMetric = jest.fn();

  beforeEach(() => {
    mockSpanExporter.reset();
    jest.clearAllMocks();
    jest
      .spyOn(SharedModulesPerformanceTracker, 'start')
      .mockImplementation(mockStart);
    jest
      .spyOn(SharedModulesPerformanceTracker, 'stop')
      .mockImplementation(mockStop);
    jest
      .spyOn(SharedModulesPerformanceTracker, 'record')
      .mockImplementation(mockRecord);
    jest
      .spyOn(SharedModulesPerformanceTracker, 'incrementMetric')
      .mockImplementation(mockIncrementMetric);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('with OTEL enabled (default)', () => {
    it('should start a native trace and an OTEL span', () => {
      const { result } = renderHook(() =>
        usePerformanceTracker(SPAN_KEYS.SESSION, 'testTrace')
      );
      result.current.startTrace();

      expect(mockStart).toHaveBeenCalledWith('testTrace');

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(0); // Span not finished yet
    });

    it('should stop a native trace and an OTEL span', () => {
      const { result } = renderHook(() =>
        usePerformanceTracker(SPAN_KEYS.SESSION, 'testTrace')
      );
      result.current.startTrace();
      result.current.stopTrace();

      expect(mockStop).toHaveBeenCalledWith('testTrace');

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(1);

      const span = spans[0] as ReadableSpan;
      expect(span.name).toBe('testTrace');
      expect(span.attributes).toEqual(
        expect.objectContaining({
          event_type: 'performance_tracker',
        })
      );
    });

    it('should record user info and set OTEL span attributes', () => {
      const { result } = renderHook(() =>
        usePerformanceTracker(SPAN_KEYS.SESSION, 'testTrace')
      );
      const userInfo = { id: 1, name: 'John Doe' };
      result.current.startTrace();
      result.current.recordUserInfo(userInfo);
      result.current.stopTrace();

      expect(mockRecord).toHaveBeenCalledWith({
        traceName: 'testTrace',
        userInfo,
      });

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(1);

      const span = spans[0] as ReadableSpan;
      expect(span.attributes).toEqual(
        expect.objectContaining({
          event_type: 'performance_tracker',
          id: 1,
          name: 'John Doe',
        })
      );
    });

    it('should increment a metric and set OTEL span attributes', () => {
      const { result } = renderHook(() =>
        usePerformanceTracker(SPAN_KEYS.SESSION, 'testTrace')
      );
      result.current.startTrace();
      result.current.incrementMetric({ metricName: 'loadTime', value: 200 });
      result.current.stopTrace();

      expect(mockIncrementMetric).toHaveBeenCalledWith({
        traceName: 'testTrace',
        metricName: 'loadTime',
        value: 200,
      });

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(1);

      const span = spans[0] as ReadableSpan;
      expect(span.attributes).toEqual(
        expect.objectContaining({
          event_type: 'performance_tracker',
          loadTime: 200,
        })
      );
    });
  });

  describe('with OTEL disabled', () => {
    const options = { useOTEL: false };

    it('should start only a native trace', () => {
      const { result } = renderHook(() =>
        usePerformanceTracker('session', 'testTrace', options)
      );
      result.current.startTrace();

      expect(mockStart).toHaveBeenCalledWith('testTrace');

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(0); // No OTEL spans should be created
    });

    it('should stop only a native trace', () => {
      const { result } = renderHook(() =>
        usePerformanceTracker('session', 'testTrace', options)
      );
      result.current.startTrace();
      result.current.stopTrace();

      expect(mockStop).toHaveBeenCalledWith('testTrace');

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(0); // No OTEL spans should be created
    });

    it('should record only user info for native trace', () => {
      const { result } = renderHook(() =>
        usePerformanceTracker('session', 'testTrace', options)
      );
      const userInfo = { id: 1, name: 'John Doe' };
      result.current.startTrace();
      result.current.recordUserInfo(userInfo);
      result.current.stopTrace();

      expect(mockRecord).toHaveBeenCalledWith({
        traceName: 'testTrace',
        userInfo,
      });

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(0); // No OTEL spans should be created
    });

    it('should increment only a native metric', () => {
      const { result } = renderHook(() =>
        usePerformanceTracker('session', 'testTrace', options)
      );
      result.current.startTrace();
      result.current.incrementMetric({ metricName: 'loadTime', value: 200 });
      result.current.stopTrace();

      expect(mockIncrementMetric).toHaveBeenCalledWith({
        traceName: 'testTrace',
        metricName: 'loadTime',
        value: 200,
      });

      const spans = mockSpanExporter.getFinishedSpans();
      expect(spans.length).toBe(0); // No OTEL spans should be created
    });
  });
});
```

**Key patterns demonstrated:**
- mockTracerProvider() for OTEL span testing
- Spy on SharedModulesPerformanceTracker methods
- Test both native and OTEL calls
- getFinishedSpans() to retrieve recorded spans
- Test with useOTEL: true (default) and useOTEL: false
- Verify attributes are synced between native and OTEL
- renderHook from @testing-library/react-native

## Example 7: Testing Performance Hooks in Component

**File**: `features/country-selection/CountrySelection.spec.tsx`

This example shows testing a component that uses performance monitoring hooks.

```typescript
import type { ReadableSpan } from '@opentelemetry/sdk-trace-base';
import type { RouteProp } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { screen, userEvent, waitFor, act } from '@testing-library/react-native';
import type { ReactNode } from 'react';

import { renderWithProviders, mockTracerProvider } from 'jest-utils';

import { useTimeToInteractivity, useTimeToRender } from '@libs/observability';
import { SystemCountry, Locale } from '@libs/system-country';

import type {
  ProfileStackRoutes as ProfileStackRoutesType,
  ProfileStackParamsList,
} from '@modules/profile/stacks/profile';

import { CountrySelection } from './CountrySelection';
import { useCountrySelectionAnalytics } from './hooks/useCountrySelectionAnalytics';

jest.mock('@libs/localization/appWithTranslations', () => ({
  AppWithTranslation: ({ children }: { children: ReactNode }) => children,
}));

jest.mock('@libs/observability', () => ({
  useTimeToInteractivity: jest.fn(),
  useTimeToRender: jest.fn().mockReturnValue({
    measureTTROnLayout: jest.fn(),
  }),
}));

jest.mock('./hooks/useCountrySelectionAnalytics');

jest.mock('@operations', () => {
  const mockMutate = jest.fn().mockImplementation(() => Promise.resolve());
  return {
    AppConfigOperations: {
      useMutateCountry: jest.fn().mockReturnValue({
        mutate: mockMutate,
        isPending: false,
        error: null,
        variables: null,
      }),
    },
  };
});

describe('<CountrySelection />', () => {
  jest.useFakeTimers();

  const mockSpanExporter = mockTracerProvider();

  beforeEach(() => {
    jest.clearAllMocks();
    mockSpanExporter.reset();
  });

  afterAll(() => {
    jest.useRealTimers();
  });

  let navigation: Partial<NavigationType>;
  let route: Partial<RouteType>;
  const mockTrackCountrySelection = jest.fn();
  const mockGoBack = jest.fn();

  beforeEach(() => {
    (useCountrySelectionAnalytics as jest.Mock).mockReturnValue({
      trackCountrySelection: mockTrackCountrySelection,
    });

    navigation = {
      dispatch: jest.fn(),
      canGoBack: jest.fn().mockReturnValue(true),
      goBack: mockGoBack,
    };

    route = {
      params: {
        countryList: [
          {
            locale: Locale.enUS,
            country: SystemCountry.US,
          },
        ],
      },
    } as unknown as RouteType;
  });

  it('should render', () => {
    renderWithProviders(
      <CountrySelection
        route={route as RouteType}
        navigation={navigation as NavigationType}
      />
    );

    expect(screen.getByTestId('country-selection')).toBeTruthy();
    expect(useTimeToInteractivity).toHaveBeenCalled();
    expect(useTimeToRender).toHaveBeenCalled();
  });

  it('should create tracing span when country is selected', async () => {
    renderWithProviders(
      <CountrySelection
        route={route as RouteType}
        navigation={navigation as NavigationType}
      />
    );

    // Select a country
    await userEvent.press(
      screen.getByTestId('country_selection_container_en-US_US')
    );

    // Run all timers and microtasks to complete async operations
    act(() => {
      jest.runAllTimers();
    });

    // Wait for the async actions to complete
    await waitFor(
      () => {
        expect(mockGoBack).toHaveBeenCalled();
      },
      { timeout: 100 }
    );

    // Verify spans were created
    const spans = mockSpanExporter.getFinishedSpans();
    expect(spans.length).toBeGreaterThan(0);

    // Find the country selection span
    const countrySelectionSpan = spans.find(
      (span) => span.name === 'button_click_select_country'
    ) as ReadableSpan;

    expect(countrySelectionSpan).toBeDefined();
    expect(countrySelectionSpan.attributes).toEqual(
      expect.objectContaining({
        locale: 'en-US',
        country: 'US',
      })
    );
  });
});
```

**Key patterns demonstrated:**
- Mock @libs/observability module
- Mock useTimeToRender to return measureTTROnLayout mock
- Mock useTimeToInteractivity as no-op
- Verify hooks are called on component render
- mockTracerProvider() for OTEL span verification
- userEvent.press() to trigger user interaction
- waitFor() to wait for async operations
- Verify span attributes with expect.objectContaining()

## Summary

The YourCompany codebase consistently follows these performance monitoring patterns:

1. **useTimeToRender** for visual render performance with onLayout callback
2. **useTimeToInteractivity** for user readiness with InteractionManager
3. **usePerformanceTracker** for custom operations with dual native + OTEL tracking
4. **{ useOTEL: false }** option to avoid duplicate OTEL spans
5. **recordUserInfo** for context attributes
6. **incrementMetric** for operation counters
7. **Development logging** with `#DEBUG` prefix in `__DEV__` mode
8. **Trace name constants** for consistency (e.g., COUNTRY_SELECTION_TRACE_ID)
9. **onLayout on root container** for accurate TTR measurement
10. **Comprehensive testing** with mocked hooks and OTEL span verification

These patterns ensure consistent, performant monitoring with comprehensive visibility into render time, interactivity, and custom metrics throughout the app.
