---
name: analytics
description: "WHAT: Event tracking with useAnalyticsTracker and AnalyticsProvider for cross-platform analytics. WHEN: tracking user interactions, feature usage, cross-platform attribution. KEYWORDS: analytics, tracking, Firebase, Adjust, Statsig, useAnalyticsTracker, events, tribe, destinations, snake_case."
---

# Analytics & Event Tracking Patterns

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns


## Core Principles

**Use feature-specific analytics hooks with useCallback for consistent event tracking.** Always specify destinations explicitly and provide complete event context with tribe assignment.

**Why**: Structured analytics enable data-driven decisions, feature performance tracking, and cross-platform attribution without prop drilling or manual parameter management.

## When to Use This Skill

Use these patterns when:

- Tracking user interactions and feature usage
- Need cross-platform analytics (Firebase, Adjust, Statsig)
- Cascading analytics context through component trees
- Tracking screen views and navigation flows
- Need team-specific event attribution (tribe assignment)
- Testing components with analytics
- Building feature-specific analytics abstractions

## Feature-Specific Analytics Hooks

### Basic Hook Structure

Create hooks with useCallback for each feature:

```typescript
// features/store/hooks/useCategoryNavigationAnalytics.ts
import { useCallback } from 'react';
import { useAnalyticsTracker } from '@libs/analytics';
import { AnalyticsEventDestination } from '@libs/native-modules/analytics-tracker';
import { Tribe } from '@libs/analytics/types';

export const useCategoryNavigationAnalytics = () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();

  const trackParentCategoryClick = useCallback(
    (category: Category, position: number) => {
      trackAnalyticsEvent({
        defaultParams: {
          eventName: 'SelectMeals_ParentCategoryClick',
          eventCategory: 'BrowseCategory',
          eventAction: 'clickParentCategory',
          eventLabel: `${category.id}|${position}`,
          screenName: 'Storefront',
          tribe: Tribe.ShoppingExperience,
        },
        parameters: {
          parent_category: category.id,
          position,
          number_of_available_items_in_parent_category: category.itemCount,
        },
        destinations: [AnalyticsEventDestination.Firebase],
      });
    },
    [trackAnalyticsEvent]
  );

  const trackSubCategoryClick = useCallback(
    (subCategoryId: string, position: number, parent: string) => {
      trackAnalyticsEvent({
        defaultParams: {
          eventName: 'SelectMeals_SubCategoryClick',
          eventCategory: 'BrowseCategory',
          eventAction: 'clickSubCategory',
          eventLabel: `${parent}|${subCategoryId}|${position}`,
          screenName: 'Storefront',
          tribe: Tribe.ShoppingExperience,
        },
        parameters: {
          browse_category: parent,
          browse_subcategory: subCategoryId,
          position,
        },
        destinations: [AnalyticsEventDestination.Firebase],
      });
    },
    [trackAnalyticsEvent]
  );

  return {
    trackParentCategoryClick,
    trackSubCategoryClick,
  };
};
```

**Key patterns:**
- Import `useAnalyticsTracker` from `@libs/analytics`
- Wrap tracking functions with `useCallback`
- Include `trackAnalyticsEvent` in dependency array
- Return object with tracking functions

**Why**: useCallback prevents function recreation on every render, improving performance and preventing unnecessary component re-renders.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/hooks/analytics/useCategoryNavigationAnalytics.ts:1`

## Destinations Configuration

### Always Specify Destinations

Every analytics event must explicitly declare which platforms receive it:

```typescript
const DESTINATIONS = [
  AnalyticsEventDestination.Firebase,  // For Firebase Analytics
  AnalyticsEventDestination.Adjust,    // For mobile attribution
  AnalyticsEventDestination.Statsig,   // For feature flags and A/B testing
];

trackAnalyticsEvent({
  defaultParams: { /* ... */ },
  parameters: { /* ... */ },
  destinations: DESTINATIONS,
});
```

**Why**: Explicit destinations prevent sending PII to wrong platforms and enable platform-specific analytics strategies.

### Platform-Specific Destinations

Different events may target different platforms:

```typescript
// Attribution events only to Adjust
const ATTRIBUTION_DESTINATIONS = [AnalyticsEventDestination.Adjust];

// Product events to all platforms
const PRODUCT_DESTINATIONS = [
  AnalyticsEventDestination.Firebase,
  AnalyticsEventDestination.Adjust,
  AnalyticsEventDestination.Statsig,
];

// Screen views only to Firebase
const SCREEN_VIEW_DESTINATIONS = [AnalyticsEventDestination.Firebase];
```

**Why**: Different platforms have different purposes (attribution vs analytics vs experimentation).

## Event Naming Conventions

### Event Names: PascalCase with Feature Prefix

Pattern: `FeatureName_EventType`

```typescript
// ✅ Good event names
'Onboarding_CardView'
'Checkout_PaymentSuccess'
'Recipe_AddToCart'
'Store_FilterApplied'
'ShoppingActionsCart_Scroll'

// ❌ Bad event names
'card_view'            // No feature context, wrong case
'checkout-payment'     // Wrong separator
'RecipeCart'           // Unclear action
```

**Why**: Consistent naming makes events easier to find in analytics dashboards and enables feature-based reporting.

### Event Parameters: snake_case

Use snake_case for all parameter names to match analytics platform conventions:

```typescript
trackAnalyticsEvent({
  defaultParams: {
    eventName: 'Recipe_AddToCart',
    eventCategory: 'recipe',
    eventAction: 'addToCart',
    eventLabel: 'recipe-123',
    screenName: 'RecipeList',
    tribe: Tribe.ShoppingExperience,
  },
  parameters: {
    recipe_id: 'recipe-123',           // snake_case
    recipe_name: 'Chicken Tikka',      // snake_case
    recipe_category: 'indian',         // snake_case
    user_plan_type: 'premium',         // snake_case
    is_total_price_shown: true,        // snake_case
  },
  destinations: DESTINATIONS,
});
```

**Why**: Firebase, Adjust, and Statsig all use snake_case conventions. Consistency prevents parameter mismatches.

## AnalyticsProvider Pattern

### Provider Hierarchy

Use AnalyticsProvider to cascade context through component tree:

```typescript
import { AnalyticsProvider } from '@libs/analytics/context';

<AnalyticsProvider
  defaultParams=\{{
    screenName: 'RecipeList',
    eventCategory: 'recipe',
    eventAction: 'view',
    eventLabel: 'favorites',
    tribe: Tribe.ShoppingExperience,
  }}
  parameters=\{{
    list_type: 'favorites',
    section: 'my_recipes',
  }}
>
  <RecipeListScreen />
</AnalyticsProvider>
```

**Why**: Provider pattern automatically adds context to all child events without manual prop drilling. Components don't need to know about screen context.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/analytics/context/AnalyticsProvider.tsx:1`

### Nested Providers Merge Context

Child providers override parent values:

```typescript
<AnalyticsProvider
  defaultParams=\{{
    screenName: 'Cookbook',
    tribe: Tribe.ShoppingExperience,
  }}
  parameters=\{{
    section: 'recipes',
  }}
>
  <CookbookScreen>
    <AnalyticsProvider
      parameters=\{{
        list_type: 'favorites',  // Adds to parent parameters
        section: 'my_recipes',   // Overrides parent section
      }}
    >
      <RecipeList />
      {/* Events here have: screenName (from parent), tribe (from parent),
          section: 'my_recipes' (overridden), list_type: 'favorites' (added) */}
    </AnalyticsProvider>
  </CookbookScreen>
</AnalyticsProvider>
```

**Merging Rules:**
- `defaultParams` merge (child overrides parent)
- `parameters` merge (child overrides parent)
- `providedFields` accumulate (union of parent and child)

**Why**: Nested providers enable hierarchical context without duplicating parameters or passing props.

### Dynamic Parameters

Update parameters dynamically using setGlobalParameters:

```typescript
import { useAnalyticsContext } from '@libs/analytics';

const FilterComponent = () => {
  const { setGlobalParameters } = useAnalyticsContext();

  useEffect(() => {
    if (selectedCategory) {
      setGlobalParameters({
        selected_category: selectedCategory,
        filter_applied: true,
      });
    }
  }, [selectedCategory, setGlobalParameters]);

  return <FilterUI />;
};
```

**Why**: Dynamic parameters allow context to change based on user interactions without re-rendering providers.

## Default Analytics Params

### Required Fields

Every analytics event requires these fields (provided by context or explicitly):

```typescript
type DefaultAnalyticsParams = {
  eventName: string;      // Event identifier: 'Recipe_AddToCart'
  eventCategory: string;  // Category: 'recipe', 'cart', 'onboarding'
  eventAction: string;    // Action: 'addToCart', 'view', 'click'
  eventLabel: string;     // Label: additional context or identifier
  screenName: string;     // Current screen: 'RecipeList', 'Cart'
  tribe: Tribe;          // Team: Tribe.ShoppingExperience
};
```

**Validation**: useAnalyticsTracker throws error if any required field is missing from both context and params.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/analytics/useAnalyticsTracker.ts:50`

## Tribe Assignment

### Assign Team to Events

Always assign a tribe (team) for organizational tracking:

```typescript
enum Tribe {
  AppFoundation = 'App Foundation',
  ShoppingExperience = 'Shopping Experience',
  CustomerOrderManagement = 'Customer Order Management',
  Conversions = 'Conversions',
  Menu = 'Menu',
  CustomerBenefits = 'Customer Benefits',
  Communications = 'Communications',
  // ... more tribes
}

trackAnalyticsEvent({
  defaultParams: {
    eventName: 'Cart_ItemAdded',
    eventCategory: 'cart',
    eventAction: 'addItem',
    eventLabel: productId,
    screenName: 'Cart',
    tribe: Tribe.CustomerOrderManagement,  // Required
  },
  parameters: { /* ... */ },
  destinations: DESTINATIONS,
});
```

**Why**: Tribe assignment helps teams track their feature performance and enables org-wide analytics reporting.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/analytics/types.ts:10`

## Analytics Event Objects

### Event Factory Pattern

Create reusable event factories for consistency:

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
  return {
    createAnalyticsEvent: () => {
      return {
        defaultParams: {
          eventName: 'ShoppingActionsCart_Scroll',
          eventCategory: 'StoreFront|OrderSummary',
          eventAction: 'EndofCartScrolled',
          eventLabel: `${hfWeek}|${subscriptionId}`,
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

**Usage:**

```typescript
const event = ShoppingActionsCartScrollEvent({
  hfWeek,
  subscriptionId,
  screenName,
  isTotalPriceShown: true,
  isNextEditableDelivery: false,
}).createAnalyticsEvent();

trackAnalyticsEvent(event);
```

**Why**: Event factories encapsulate event creation logic, ensure consistency, and make testing easier.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/screens/cart/analytic-events/ShoppingActionsCartScrollEvent.ts:1`

## Component Integration

### Track User Actions

Track meaningful interactions with useCallback:

```typescript
import { useCallback } from 'react';
import { useCategoryNavigationAnalytics } from '../hooks/useCategoryNavigationAnalytics';

const CategoryCard = ({ category, position }) => {
  const { trackParentCategoryClick } = useCategoryNavigationAnalytics();

  const handlePress = useCallback(() => {
    trackParentCategoryClick(category, position);
    navigate('CategoryDetails', { categoryId: category.id });
  }, [category, position, trackParentCategoryClick, navigate]);

  return (
    <TouchableOpacity onPress={handlePress}>
      <Text>{category.name}</Text>
    </TouchableOpacity>
  );
};
```

**Why**: Tracking in event handlers ensures events fire only when users interact, not on every render.

### Track Effects

Track component lifecycle events:

```typescript
import { useEffect } from 'react';

const RecipeCard = ({ recipe }) => {
  const { trackRecipeView } = useRecipeAnalytics();

  useEffect(() => {
    trackRecipeView({ recipe_id: recipe.id });
  }, [trackRecipeView, recipe.id]);

  return <Card>{/* content */}</Card>;
};
```

**Why**: useEffect ensures view tracking happens once per mount, not on every render.

## Context Consumption

### Access Analytics Context

```typescript
import { useAnalyticsContext } from '@libs/analytics';

const CustomComponent = () => {
  const { data: analyticsContext } = useAnalyticsContext();

  const { hfWeek } = analyticsContext?.parameters as { hfWeek?: string } || {};

  // Use context data in event tracking
  return <Component />;
};
```

**Why**: Components can access cascaded parameters from parent providers for dynamic event construction.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/hooks/analytics/useCategoryNavigationAnalytics.ts:10`

## Testing Analytics

### Mock useAnalyticsTracker

```typescript
import { renderHook, act } from '@testing-library/react-native';
import { useAnalytics } from './useAnalytics';
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

  it('tracks card view event', () => {
    const { result } = renderHook(() => useAnalytics());

    act(() => {
      result.current.trackOnboardingCardView({
        sequenceLen: 3,
        cardIndex: 1,
        cardId: 'welcome-card',
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
          card_id: 'welcome-card',
        },
        destinations: [
          AnalyticsEventDestination.Firebase,
          AnalyticsEventDestination.Adjust,
          AnalyticsEventDestination.Statsig,
        ],
      })
    );
  });
});
```

**Key patterns:**
- Mock `useAnalyticsTracker` from `@libs/analytics`
- Mock `Tribe` enum with string values
- Return mocked `trackAnalyticsEvent` function
- Use `expect.objectContaining` for partial matching
- Verify `destinations`, `defaultParams`, and `parameters`

**Why**: Mocking enables testing analytics logic without actually sending events.

**Production Example**: `git-resources/shared-mobile-modules/src/features/app-onboarding/hooks/test/useAnalytics.test.ts:1`

## Common Mistakes to Avoid

❌ **Don't track events without destinations**:

```typescript
// ❌ Missing destinations - event won't be sent anywhere
trackAnalyticsEvent({
  defaultParams: { eventName: 'Recipe_View', /* ... */ },
  parameters: {},
  // Missing: destinations
});

// ✅ Always specify destinations
trackAnalyticsEvent({
  defaultParams: { eventName: 'Recipe_View', /* ... */ },
  parameters: {},
  destinations: [AnalyticsEventDestination.Firebase],
});
```

❌ **Don't forget to memoize tracking functions**:

```typescript
// ❌ Creates new function on every render
const trackCardView = () => {
  trackAnalyticsEvent({ /* ... */ });
};

// ✅ Use useCallback
const trackCardView = useCallback(() => {
  trackAnalyticsEvent({ /* ... */ });
}, [trackAnalyticsEvent]);
```

❌ **Don't use inconsistent naming**:

```typescript
// ❌ Inconsistent casing and format
'recipe-view'         // Wrong: kebab-case
'RecipeAddCart'       // Wrong: missing separator
'RECIPE_DELETE'       // Wrong: all caps

// ✅ Consistent PascalCase with underscore
'Recipe_View'
'Recipe_AddToCart'
'Recipe_Delete'
```

❌ **Don't use camelCase for parameters**:

```typescript
// ❌ Wrong parameter casing
parameters: {
  recipeId: 'recipe-123',        // camelCase
  recipeName: 'Chicken Tikka',   // camelCase
  userPlanType: 'premium',       // camelCase
}

// ✅ Use snake_case
parameters: {
  recipe_id: 'recipe-123',
  recipe_name: 'Chicken Tikka',
  user_plan_type: 'premium',
}
```

❌ **Don't track in render loops**:

```typescript
// ❌ Tracks on every render
recipes.map(recipe => {
  trackRecipeView({ recipe_id: recipe.id }); // Bad!
  return <RecipeCard recipe={recipe} />;
});

// ✅ Track on user action
const handleRecipePress = useCallback((recipe) => {
  trackRecipeView({ recipe_id: recipe.id });
  navigate('RecipeDetails', { recipeId: recipe.id });
}, [trackRecipeView, navigate]);
```

✅ **Do use feature-specific hooks**:

```typescript
// ✅ Encapsulated analytics logic
const useCartAnalytics = () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();

  const trackCartOpen = useCallback(() => {
    trackAnalyticsEvent({
      defaultParams: {
        eventName: 'Cart_Open',
        eventCategory: 'cart',
        eventAction: 'open',
        eventLabel: cartId,
        screenName: 'Cart',
        tribe: Tribe.CustomerOrderManagement,
      },
      parameters: { cart_id: cartId },
      destinations: [AnalyticsEventDestination.Firebase],
    });
  }, [trackAnalyticsEvent, cartId]);

  return { trackCartOpen };
};
```

✅ **Do provide complete context via Provider**:

```typescript
// ✅ Context cascades to all children
<AnalyticsProvider
  defaultParams=\{{
    screenName: 'Storefront',
    eventCategory: 'store',
    tribe: Tribe.ShoppingExperience,
  }}
  parameters=\{{
    hfWeek: selectedWeek,
    category_id: selectedCategory,
  }}
>
  <StorefrontContent />
</AnalyticsProvider>
```

✅ **Do specify tribe for every event**:

```typescript
// ✅ Tribe enables team-based tracking
trackAnalyticsEvent({
  defaultParams: {
    eventName: 'Recipe_AddToCart',
    tribe: Tribe.ShoppingExperience,  // Required
    /* ... */
  },
  /* ... */
});
```

## Performance Considerations

### Avoid High-Frequency Tracking

Don't track scroll events without throttling:

```typescript
// ❌ Tracks on every scroll frame
onScroll={() => {
  trackScrollEvent({ position: scrollY });
}}

// ✅ Throttle or debounce high-frequency events
const throttledTrackScroll = useThrottledCallback(
  (position: number) => {
    trackScrollEvent({ position });
  },
  500, // 500ms throttle
  [trackScrollEvent]
);
```

**Why**: Excessive tracking impacts performance and inflates analytics data volume.

## Quick Reference

**Feature Hook Pattern:**
```typescript
const use{Feature}Analytics = () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();

  const track{Action} = useCallback(() => {
    trackAnalyticsEvent({
      defaultParams: {
        eventName: '{Feature}_{Action}',
        eventCategory: 'category',
        eventAction: 'action',
        eventLabel: 'label',
        screenName: 'Screen',
        tribe: Tribe.{TeamName},
      },
      parameters: { /* snake_case */ },
      destinations: [AnalyticsEventDestination.Firebase],
    });
  }, [trackAnalyticsEvent]);

  return { track{Action} };
};
```

**Event Naming:**
- Events: `PascalCase` with `FeatureName_EventType`
- Parameters: `snake_case`
- Categories: `camelCase` or `kebab-case`

**Destinations:**
- `AnalyticsEventDestination.Firebase` - Analytics
- `AnalyticsEventDestination.Adjust` - Attribution
- `AnalyticsEventDestination.Statsig` - Experimentation

**Required Fields:**
- `eventName`, `eventCategory`, `eventAction`, `eventLabel`
- `screenName`, `tribe`

**Provider Pattern:**
```typescript
<AnalyticsProvider
  defaultParams={{ screenName, tribe }}
  parameters={}
>
  {children}
</AnalyticsProvider>
```

**Testing:**
- Mock `useAnalyticsTracker`
- Mock `Tribe` enum
- Verify with `expect.objectContaining`

**Key Libraries:**
- React Native 0.75.4
- @libs/analytics (internal)
- @libs/native-modules/analytics-tracker (internal)

For production examples, see [references/examples.md](references/examples.md).
