# Analytics - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating analytics patterns.

## Example 1: useAnalyticsTracker Core Implementation

**File**: `libs/analytics/useAnalyticsTracker.ts`

This is the core analytics hook that all feature-specific hooks use.

```typescript
import { isEmpty } from 'lodash';
import { useCallback } from 'react';

import { AppConfigDataAccess } from '@data-access/native';

import type {
  AnalyticsEventDestination,
  AnalyticsEntity,
  EventContextEntity,
  EventSpecificationsEntity,
} from '@libs/native-modules/analytics-tracker';
import {
  AnalyticsEvent,
  OpenScreenEvent,
  SharedModulesAnalyticsTracker,
  SnowplowAnalyticsEvent,
} from '@libs/native-modules/analytics-tracker';

import { DEFAULT_ANALYTICS_KEYS } from './constants';
import { useAnalyticsContext } from './context/AnalyticsProvider';
import type { DefaultAnalyticsParams } from './types';
import { Tribe } from './types';

const ANALYTICS_LOGGING = {
  enabled: __DEV__,
  includeParameters: true,
} as const;

export const useAnalyticsTracker = () => {
  const { data: contextData, providedFields } = useAnalyticsContext();
  const { data: brand } = AppConfigDataAccess.queries.useBrandState();

  /**
   * Tracks a generic analytics event with smart required fields based on context.
   * If a field is provided in context, it becomes optional in params.
   * If a field is missing from both context and params, an error is thrown.
   */
  const trackAnalyticsEvent = useCallback(
    async ({
      defaultParams = {},
      destinations,
      parameters,
    }: {
      defaultParams?: Partial<DefaultAnalyticsParams>;
      destinations: AnalyticsEventDestination[];
      parameters?: object;
    }) => {
      try {
        // All fields in DefaultAnalyticsParams are required
        const missingFields = DEFAULT_ANALYTICS_KEYS.filter(
          (field) =>
            !(
              (providedFields.has(field) &&
                contextData.defaultParams?.[field] != null) ||
              (field in defaultParams && defaultParams[field] != null)
            )
        );

        if (!isEmpty(missingFields)) {
          console.log(
            '🔴 Analytics Error: Missing required fields, eventName:',
            defaultParams.eventName,
            { missingFields }
          );

          throw new Error(
            `🔴 Analytics Error: Missing required fields: ${missingFields.join(', ')}`
          );
        }

        // Merge context and provided parameters
        const finalDefaultParams: DefaultAnalyticsParams = {
          eventName:
            defaultParams.eventName ??
            contextData.defaultParams?.eventName ??
            'unknown_event',
          eventCategory:
            defaultParams.eventCategory ??
            contextData.defaultParams?.eventCategory ??
            'unknown_category',
          eventAction:
            defaultParams.eventAction ??
            contextData.defaultParams?.eventAction ??
            'unknown_action',
          eventLabel:
            defaultParams.eventLabel ??
            contextData.defaultParams?.eventLabel ??
            'unknown_label',
          screenName:
            defaultParams.screenName ??
            contextData.defaultParams?.screenName ??
            'unknown_screen',
          tribe:
            defaultParams.tribe ??
            contextData.defaultParams?.tribe ??
            Tribe.AppFoundation,
        };

        const finalParameters = {
          brand: brand ?? 'unknown_brand', // Auto-inject brand for all analytics events
          ...contextData.parameters,
          ...parameters,
        };

        const event = new AnalyticsEvent({
          defaultParams: {
            eventName: finalDefaultParams.eventName,
            eventCategory: finalDefaultParams.eventCategory,
            eventAction: finalDefaultParams.eventAction,
            eventLabel: finalDefaultParams.eventLabel,
            screenName: finalDefaultParams.screenName,
            tribe: finalDefaultParams.tribe.toString(),
          },
          destinations,
          parameters: finalParameters,
        });

        await SharedModulesAnalyticsTracker.trackAnalyticsEvent(event);

        // Log successful event firing conditionally based on environment
        if (ANALYTICS_LOGGING.enabled) {
          console.log(
            `🟢 Analytics Event Successfully Fired - Name: ${finalDefaultParams.eventName} from Screen: ${finalDefaultParams.screenName}`,
            JSON.stringify(
              {
                eventType: 'AnalyticsEvent',
                defaultParams: finalDefaultParams,
                destinations,
                parameters: finalParameters,
                timestamp: new Date().toISOString(),
              },
              null,
              2
            )
          );
        }
      } catch (error) {
        // Re-throw analytics errors to make them visible to developers
        if (
          error instanceof Error &&
          error.message.includes('Analytics Error')
        ) {
          throw error;
        }
        console.error('Error tracking analytics event:', error);
      }
    },
    [contextData, providedFields, brand]
  );

  return {
    trackAnalyticsEvent,
  };
};
```

**Key patterns demonstrated:**
- Merges context and provided parameters with priority: params > context > defaults
- Validates all required fields are present (from context OR params)
- Auto-injects brand from native config
- Logs events in development only
- Throws on missing required fields for developer visibility
- Uses useCallback with context dependencies

## Example 2: Feature-Specific Analytics Hook

**File**: `modules/store/hooks/analytics/useCategoryNavigationAnalytics.ts`

This example shows a feature-specific hook that encapsulates category navigation tracking.

```typescript
import { useCallback } from 'react';

import { useAnalyticsContext, useAnalyticsTracker } from '@libs/analytics';
import { AnalyticsEventDestination } from '@libs/native-modules/analytics-tracker';

import type { Category } from '@modules/store/zustand-store/navigation/types';

export const useCategoryNavigationAnalytics = () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();
  const { data: analyticsContext } = useAnalyticsContext();

  const { hfWeek } =
    (analyticsContext?.parameters as { hfWeek?: string }) || {};

  const trackParentCategoryClick = useCallback(
    (category: Category, position: number) => {
      trackAnalyticsEvent({
        defaultParams: {
          eventName: 'SelectMeals_ParentCategoryClick',
          eventCategory: 'BrowseCategory',
          eventAction: 'clickParentCategory',
          eventLabel: `${hfWeek}|${category.id}|${position}`,
        },
        parameters: {
          parent_category: category.id,
          position,
          number_of_available_items_in_parent_category: category.itemCount,
        },
        destinations: [AnalyticsEventDestination.Firebase],
      });
    },
    [hfWeek, trackAnalyticsEvent]
  );

  const trackSubCategoryClick = useCallback(
    (
      subCategoryId: string,
      position: number,
      parent: string,
      action: string,
      itemCount: number
    ) => {
      trackAnalyticsEvent({
        defaultParams: {
          eventName: 'SelectMeals_SubCategoryClick',
          eventCategory: 'BrowseCategory',
          eventAction: 'clickSubCategory',
          eventLabel: `${hfWeek}|${parent}|${subCategoryId}|${position}`,
        },
        parameters: {
          browse_category: parent,
          browse_subcategory: subCategoryId,
          free_category: '',
          position,
          parent_position: '',
          number_of_available_items_in_sub_category: itemCount,
          action,
        },
        destinations: [AnalyticsEventDestination.Firebase],
      });
    },
    [hfWeek, trackAnalyticsEvent]
  );

  return {
    trackParentCategoryClick,
    trackSubCategoryClick,
  };
};
```

**Key patterns demonstrated:**
- Feature-specific hook encapsulates category navigation tracking
- Extracts context parameters (hfWeek) from AnalyticsProvider
- Uses useCallback with proper dependencies
- Returns object with tracking functions
- Event naming: `SelectMeals_ParentCategoryClick` (feature_action)
- Parameter naming: snake_case (`parent_category`, `number_of_available_items_in_parent_category`)

## Example 3: AnalyticsProvider Context Implementation

**File**: `libs/analytics/context/AnalyticsProvider.tsx`

This example shows how AnalyticsProvider cascades context through the component tree.

```typescript
import React, {
  useContext,
  createContext,
  useMemo,
  useState,
  useCallback,
} from 'react';

import { getValidDefaultAnalyticsKeys } from '../constants';

import type { AnalyticsContextData, ContextWithMeta } from './types';

// Context with metadata about which fields are provided
const AnalyticsContext = createContext<ContextWithMeta>({
  data: {},
  providedFields: new Set(),
  setGlobalParameters: () => {
    console.warn('setGlobalParameters called outside of AnalyticsProvider');
  },
});

export const useAnalyticsContext = (): ContextWithMeta =>
  useContext(AnalyticsContext);

export const AnalyticsProvider: React.FC<
  React.PropsWithChildren<AnalyticsContextData>
> = ({ children, defaultParams = {}, parameters }) => {
  const parent = useAnalyticsContext();

  const [globalDynamicParameters, setGlobalDynamicParameters] =
    useState<object>({});

  const setGlobalParameters = useCallback(
    (newParameters: object) => {
      // Update this provider's dynamic parameters
      setGlobalDynamicParameters((prev) => ({
        ...prev,
        ...newParameters,
      }));

      // Bubble up to parent provider if it exists
      if (parent.setGlobalParameters) {
        parent.setGlobalParameters(newParameters);
      }
    },
    [parent]
  );

  const value = useMemo(() => {
    const mergedDefaultParams = {
      ...parent.data.defaultParams,
      ...defaultParams,
    };

    const mergedParameters = {
      ...parent.data.parameters,
      ...parameters,
      ...globalDynamicParameters, // Global Dynamic parameters have highest priority
    };

    // Track which default analytics fields are provided by this provider
    const defaultFieldsProvidedHere =
      getValidDefaultAnalyticsKeys(defaultParams);
    const providedFields = new Set([
      ...parent.providedFields,
      ...defaultFieldsProvidedHere,
    ]);

    return {
      data: {
        defaultParams: mergedDefaultParams,
        parameters: mergedParameters,
      },
      providedFields,
      setGlobalParameters,
    };
  }, [
    parent,
    defaultParams,
    parameters,
    globalDynamicParameters,
    setGlobalParameters,
  ]);

  return (
    <AnalyticsContext.Provider value={value}>
      {children}
    </AnalyticsContext.Provider>
  );
};
```

**Key patterns demonstrated:**
- Merges parent and child `defaultParams` (child overrides)
- Merges parent and child `parameters` (child overrides)
- `globalDynamicParameters` have highest priority
- Tracks which fields are provided (`providedFields` Set)
- `setGlobalParameters` bubbles up to parent providers
- useMemo prevents unnecessary re-renders

## Example 4: Cart Analytics with Event Factories

**File**: `modules/store/screens/cart/hooks/use-cart-analytics/useCartAnalytics.ts`

This example demonstrates using event factory functions.

```typescript
import { useCallback } from 'react';

import { AppConfigDataAccess } from '@data-access/native';

import { useAnalyticsTracker } from '@libs/analytics';

import { useScreenName } from '@operations/analytics/hooks';

import {
  OrderSummaryEditableSummaryDrawerCloseEvent,
  OrderSummaryEditableSummaryDrawerOpenEvent,
  ShoppingActionsCartScrollEvent,
} from '../../analytic-events';
import { useDataContext } from '../../providers/data';

const useDeliveryData = () => {
  const { delivery, subscriptionId } = useDataContext();
  const flags = delivery?.flags;

  return {
    hfWeek: delivery?.id,
    subscriptionId,
    isNextEditableDelivery: flags?.isNextEditableDelivery,
  };
};

export const useCartAnalytics = () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();
  const { data } = AppConfigDataAccess.queries.useCurrentCountryState();

  const country = data?.country;
  const screenName = useScreenName();
  const { hfWeek, subscriptionId, isNextEditableDelivery } = useDeliveryData();

  const trackCartOpen = useCallback(() => {
    const event = OrderSummaryEditableSummaryDrawerOpenEvent({
      hfWeek,
      subscriptionId,
      screenName,
      countryCode: country,
    }).createAnalyticsEvent();

    trackAnalyticsEvent(event);
  }, [trackAnalyticsEvent, hfWeek, subscriptionId, screenName, country]);

  const trackCartClose = useCallback(() => {
    const event = OrderSummaryEditableSummaryDrawerCloseEvent({
      hfWeek: hfWeek,
      screenName: screenName,
    }).createAnalyticsEvent();

    trackAnalyticsEvent(event);
  }, [trackAnalyticsEvent, hfWeek, screenName]);

  const trackCartScroll = useCallback(
    (isTotalPriceShown: boolean) => {
      const event = ShoppingActionsCartScrollEvent({
        hfWeek,
        subscriptionId,
        screenName,
        isTotalPriceShown,
        isNextEditableDelivery,
      }).createAnalyticsEvent();

      trackAnalyticsEvent(event);
    },
    [
      trackAnalyticsEvent,
      hfWeek,
      subscriptionId,
      isNextEditableDelivery,
      screenName,
    ]
  );

  return { trackCartOpen, trackCartClose, trackCartScroll };
};
```

**Key patterns demonstrated:**
- Custom hook extracts delivery data from context
- Event factory functions create event objects
- `.createAnalyticsEvent()` method returns event config
- useCallback with all dependencies
- Data from multiple sources: native data, context, navigation

## Example 5: Event Factory Implementation

**File**: `modules/store/screens/cart/analytic-events/ShoppingActionsCartScrollEvent.ts`

This example shows event factory pattern for reusable event creation.

```typescript
import { Tribe } from '@libs/analytics';
import type { TrackingEvent } from '@libs/analytics';
import { AnalyticsEventDestination } from '@libs/native-modules/analytics-tracker';

interface Props {
  hfWeek: string;
  subscriptionId: string;
  screenName: string;
  isTotalPriceShown: boolean;
  isNextEditableDelivery: boolean;
}

export const ShoppingActionsCartScrollEvent = ({
  hfWeek,
  subscriptionId,
  screenName,
  isTotalPriceShown,
  isNextEditableDelivery,
}: Props): TrackingEvent => {
  const legacyParams = {
    eventCategory: 'StoreFront|OrderSummary',
    eventAction: 'EndofCartScrolled',
    eventLabel: `${hfWeek}|${subscriptionId}`,
  };

  return {
    createAnalyticsEvent: () => {
      return {
        defaultParams: {
          ...legacyParams,
          eventName: 'ShoppingActionsCart_Scroll',
          screenName: screenName,
          tribe: Tribe.CustomerOrderManagement,
        },
        parameters: {
          isTotalPriceShown: isTotalPriceShown ? 'yes' : 'no',
          weekType: isNextEditableDelivery ? 'currentWeek' : 'futureWeek',
        },
        destinations: [AnalyticsEventDestination.Firebase],
      };
    },
  };
};
```

**Key patterns demonstrated:**
- Type-safe event factory with Props interface
- Returns `TrackingEvent` with `createAnalyticsEvent` method
- Legacy params support for backward compatibility
- Tribe assignment: `Tribe.CustomerOrderManagement`
- Boolean conversion to strings for parameters
- Descriptive event name: `ShoppingActionsCart_Scroll`

## Example 6: Testing Analytics Hooks

**File**: `features/app-onboarding/hooks/test/useAnalytics.test.ts`

This example shows comprehensive testing of analytics hooks.

```typescript
import { renderHook } from '@testing-library/react-native';
import { act } from 'react';

import { useAnalytics } from '@features/app-onboarding/hooks/useAnalytics';

import { useAnalyticsTracker } from '@libs/analytics';
import { AnalyticsEventDestination } from '@libs/native-modules/analytics-tracker';

jest.mock('@libs/analytics', () => ({
  useAnalyticsTracker: jest.fn(),
  Tribe: { ShoppingExperience: 'ShoppingExperience' },
}));

describe('useAnalytics', () => {
  const mockTrackAnalyticsEvent = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (useAnalyticsTracker as jest.Mock).mockReturnValue({
      trackAnalyticsEvent: mockTrackAnalyticsEvent,
    });
  });

  it('tracks onboarding card view', () => {
    const { result } = renderHook(() => useAnalytics());

    act(() => {
      result.current.trackOnboardingCardView({
        sequenceLen: 3,
        cardIndex: 1,
        cardId: 'welcome card',
      });
    });

    expect(mockTrackAnalyticsEvent).toHaveBeenCalledWith(
      expect.objectContaining({
        defaultParams: expect.objectContaining({
          eventName: 'Onboarding_CardView',
          eventAction: 'cardView',
        }),
        parameters: {
          sequence_len: 3,
          card_index: 1,
          card_id: 'welcome card',
        },
        destinations: [
          AnalyticsEventDestination.Firebase,
          AnalyticsEventDestination.Adjust,
          AnalyticsEventDestination.Statsig,
        ],
      })
    );
  });

  it('tracks onboarding card navigation', () => {
    const { result } = renderHook(() => useAnalytics());

    act(() => {
      result.current.trackOnboardingCardNavigation({
        action: 'swipe',
        label: 'next',
        sequenceLen: 5,
        cardIndex: 2,
        cardId: 'Second card',
      });
    });

    expect(mockTrackAnalyticsEvent).toHaveBeenCalledWith(
      expect.objectContaining({
        defaultParams: expect.objectContaining({
          eventName: 'Onboarding_CardNavigation',
          eventAction: 'swipe',
          eventLabel: 'next',
        }),
        parameters: expect.objectContaining({
          sequence_len: 5,
          card_index: 2,
          card_id: 'Second card',
          interaction: 'swipe',
          navigation_direction: 'next',
        }),
      })
    );
  });

  it('tracks onboarding dismiss', () => {
    const { result } = renderHook(() => useAnalytics());

    act(() => {
      result.current.trackOnboardingDismiss({
        sequenceLen: 4,
        cardIndex: 4,
        cardId: 'Last card',
      });
    });

    expect(mockTrackAnalyticsEvent).toHaveBeenCalledWith(
      expect.objectContaining({
        defaultParams: expect.objectContaining({
          eventName: 'Onboarding_Dismiss',
          eventAction: 'dismiss',
        }),
        parameters: {
          sequence_len: 4,
          card_index: 4,
          card_id: 'Last card',
        },
      })
    );
  });
});
```

**Key patterns demonstrated:**
- Mock `useAnalyticsTracker` from `@libs/analytics`
- Mock `Tribe` enum with string values
- `renderHook` from `@testing-library/react-native`
- `act` wrapper for hook calls
- `expect.objectContaining` for partial matching
- Verify `destinations`, `defaultParams`, and `parameters`
- Multiple test cases for different tracking functions

## Example 7: Tribe Enum Definition

**File**: `libs/analytics/types.ts`

This shows the Tribe enum for team attribution.

```typescript
export type DefaultAnalyticsParams = {
  eventName: string;
  eventCategory: string;
  eventAction: string;
  eventLabel: string;
  screenName: string;
  tribe: Tribe;
};

// Enum for different tribes
export enum Tribe {
  AppFoundation = 'App Foundation',
  Wac = 'WAC',
  Engagement = 'Engagement',
  CustomerOrderManagement = 'Customer Order Management',
  Conversions = 'Conversions',
  Market = 'Market',
  Payments = 'Payments',
  Menu = 'Menu',
  CustomerBenefits = 'Customer Benefits',
  AdTech = 'Ad Tech',
  Communications = 'Communications',
  HabitBuilding = 'Habit Building',
  Culinary = 'Culinary',
  ShoppingExperience = 'Shopping Experience',
  RTEExpansion = 'RTE Expansion',
  ConsumerCore = 'Consumer Core',
}
```

**Key patterns demonstrated:**
- `DefaultAnalyticsParams` type defines all required fields
- `Tribe` enum with human-readable display values
- Every event MUST specify a tribe
- Tribes map to organizational teams for attribution

## Summary

The YourCompany codebase consistently follows these analytics patterns:

1. **Feature-specific hooks** with useCallback for performance
2. **useAnalyticsTracker** core hook with context merging
3. **AnalyticsProvider** for cascading context
4. **Destinations always specified** (Firebase, Adjust, Statsig)
5. **Event naming**: PascalCase with `Feature_Action`
6. **Parameter naming**: snake_case
7. **Tribe assignment** for team attribution
8. **Event factory pattern** for reusable event creation
9. **Context consumption** for dynamic parameters
10. **Comprehensive testing** with mocked trackers

These patterns ensure consistent, performant analytics tracking with team attribution and cross-platform support throughout the app.
