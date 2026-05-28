# Analytics - Implementation Patterns

Implementation patterns and anti-patterns for analytics tracking in React web applications.

## Pattern: Use Feature-Specific Analytics Hooks

Create dedicated hooks for each feature's analytics.

✅ **Good:**
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
          screenName: 'Storefront',
          tribe: Tribe.ShoppingExperience,
        },
        parameters: {
          parent_category: category.id,
          position,
        },
        destinations: [AnalyticsEventDestination.Firebase],
      });
    },
    [trackAnalyticsEvent]
  );

  return { trackParentCategoryClick };
};
```

❌ **Bad:**
```typescript
// Inline tracking in component
const Component = () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();

  const handleClick = (category: Category) => {
    // Repeated boilerplate in every component
    trackAnalyticsEvent({
      defaultParams: {
        eventName: 'SelectMeals_ParentCategoryClick',
        eventCategory: 'BrowseCategory',
        eventAction: 'clickParentCategory',
        screenName: 'Storefront',
        tribe: Tribe.ShoppingExperience,
      },
      parameters: {
        parent_category: category.id,
      },
      destinations: [AnalyticsEventDestination.Firebase],
    });
  };
};
```

**Why:** Feature-specific hooks:
- Centralize event definitions
- Ensure consistency
- Easy to test
- Reusable across components
- Clear ownership

## Pattern: Use useCallback for Tracking Functions

Wrap tracking functions with useCallback.

✅ **Good:**
```typescript
export const useFeatureAnalytics = () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();

  const trackButtonClick = useCallback(
    (buttonId: string) => {
      trackAnalyticsEvent({
        defaultParams: {
          eventName: 'Feature_ButtonClick',
          eventCategory: 'UI',
          eventAction: 'click',
          tribe: Tribe.Growth,
        },
        parameters: { button_id: buttonId },
        destinations: [AnalyticsEventDestination.Firebase],
      });
    },
    [trackAnalyticsEvent] // Include in dependencies
  );

  return { trackButtonClick };
};
```

❌ **Bad:**
```typescript
export const useFeatureAnalytics = () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();

  // No useCallback - function recreated on every render
  const trackButtonClick = (buttonId: string) => {
    trackAnalyticsEvent({
      defaultParams: {
        eventName: 'Feature_ButtonClick',
        eventCategory: 'UI',
        eventAction: 'click',
        tribe: Tribe.Growth,
      },
      parameters: { button_id: buttonId },
      destinations: [AnalyticsEventDestination.Firebase],
    });
  };

  return { trackButtonClick };
};
```

**Why:** useCallback:
- Prevents function recreation
- Improves performance
- Prevents unnecessary re-renders
- Stable function reference

## Pattern: Follow Event Naming Conventions

Use PascalCase with feature prefix for event names.

✅ **Good:**
```typescript
eventName: 'SelectMeals_ParentCategoryClick'
eventName: 'Checkout_PaymentMethodSelected'
eventName: 'AccountSettings_ProfileUpdated'
eventName: 'Search_QuerySubmitted'
```

❌ **Bad:**
```typescript
eventName: 'parent_category_click'           // snake_case
eventName: 'selectmeals-parentcategoryclick' // kebab-case
eventName: 'ParentCategoryClick'             // No feature prefix
eventName: 'clickParentCategory'             // camelCase
```

**Why:** PascalCase with prefix:
- Consistent across codebase
- Easy to filter by feature
- Clear ownership
- Follows standard

## Pattern: Use snake_case for Parameters

All event parameters should use snake_case.

✅ **Good:**
```typescript
parameters: {
  parent_category: category.id,
  position: 0,
  number_of_items: items.length,
  user_id: userId,
}
```

❌ **Bad:**
```typescript
parameters: {
  parentCategory: category.id,      // camelCase
  Position: 0,                       // PascalCase
  'number-of-items': items.length,   // kebab-case
  UserID: userId,                    // PascalCase + capitalization
}
```

**Why:** snake_case:
- Consistent with analytics platforms
- Easier to query in databases
- Standard convention
- Better readability

## Pattern: Always Specify Destinations

Explicitly specify analytics destinations.

✅ **Good:**
```typescript
trackAnalyticsEvent({
  defaultParams: { /* ... */ },
  parameters: { /* ... */ },
  destinations: [AnalyticsEventDestination.Firebase], // Explicit
});

// Multiple destinations
destinations: [
  AnalyticsEventDestination.Firebase,
  AnalyticsEventDestination.Adjust,
]
```

❌ **Bad:**
```typescript
trackAnalyticsEvent({
  defaultParams: { /* ... */ },
  parameters: { /* ... */ },
  // No destinations specified - unclear where data goes
});
```

**Why:** Explicit destinations:
- Clear data flow
- Cost control
- Compliance requirements
- Easier debugging

## Pattern: Use AnalyticsProvider for Context

Cascade analytics context with AnalyticsProvider.

✅ **Good:**
```typescript
<AnalyticsProvider
  defaultParams={{
    screenName: 'Checkout',
    tribe: Tribe.Growth,
  }}
>
  <CheckoutFlow />
</AnalyticsProvider>

// All events in CheckoutFlow automatically include screenName and tribe
```

❌ **Bad:**
```typescript
// Manually adding screenName to every event
const trackStepComplete = useCallback(
  (step: number) => {
    trackAnalyticsEvent({
      defaultParams: {
        eventName: 'Checkout_StepComplete',
        screenName: 'Checkout',  // Repeated everywhere
        tribe: Tribe.Growth,      // Repeated everywhere
      },
    });
  },
  [trackAnalyticsEvent]
);
```

**Why:** Provider pattern:
- Reduces boilerplate
- Ensures consistency
- Single source of truth
- Easier to update

## Pattern: Assign Tribe to All Events

Always specify the team owning the feature.

✅ **Good:**
```typescript
defaultParams: {
  eventName: 'SelectMeals_ParentCategoryClick',
  eventCategory: 'BrowseCategory',
  eventAction: 'clickParentCategory',
  tribe: Tribe.ShoppingExperience,  // Team assignment
}
```

❌ **Bad:**
```typescript
defaultParams: {
  eventName: 'SelectMeals_ParentCategoryClick',
  eventCategory: 'BrowseCategory',
  eventAction: 'clickParentCategory',
  // No tribe - unclear ownership
}
```

**Why:** Tribe assignment:
- Clear ownership
- Team attribution
- Data segmentation
- Performance tracking

## Pattern: Include Position for List Items

Track position for items in lists.

✅ **Good:**
```typescript
items.map((item, index) => (
  <div
    key={item.id}
    onClick={() => trackItemClick(item.id, index)}
  >
    {item.name}
  </div>
))

const trackItemClick = useCallback(
  (itemId: string, position: number) => {
    trackAnalyticsEvent({
      defaultParams: { /* ... */ },
      parameters: {
        item_id: itemId,
        position,  // Track position
      },
    });
  },
  [trackAnalyticsEvent]
);
```

❌ **Bad:**
```typescript
items.map((item) => (
  <div
    key={item.id}
    onClick={() => trackItemClick(item.id)}  // No position
  >
    {item.name}
  </div>
))
```

**Why:** Position tracking:
- Understand user behavior
- Optimize list ordering
- A/B test placements
- Conversion analysis

## Pattern: Mock Analytics in Tests

Mock analytics tracker in tests.

✅ **Good:**
```typescript
// __mocks__/@libs/analytics.ts
export const useAnalyticsTracker = jest.fn(() => ({
  trackAnalyticsEvent: jest.fn(),
  trackScreenView: jest.fn(),
}));

// In test
it('tracks button click', () => {
  const mockTrack = jest.fn();
  (useAnalyticsTracker as jest.Mock).mockReturnValue({
    trackAnalyticsEvent: mockTrack,
  });

  render(<MyComponent />);
  fireEvent.click(screen.getByRole('button'));

  expect(mockTrack).toHaveBeenCalledWith({
    defaultParams: {
      eventName: 'Feature_ButtonClick',
      tribe: Tribe.Growth,
    },
  });
});
```

❌ **Bad:**
```typescript
// No mocking - actual analytics calls in tests
it('tracks button click', () => {
  render(<MyComponent />);
  fireEvent.click(screen.getByRole('button'));
  // Real analytics event sent during test
});
```

**Why:** Mocking:
- Tests don't send real events
- Faster tests
- Predictable behavior
- Can assert on calls

## Pattern: Track Screen Views on Mount

Track screen views when components mount.

✅ **Good:**
```typescript
const MyScreen = () => {
  const { trackScreenView } = useAnalyticsTracker();

  useEffect(() => {
    trackScreenView({
      screenName: 'ProductDetails',
      tribe: Tribe.ShoppingExperience,
      parameters: {
        product_id: productId,
      },
    });
  }, [trackScreenView, productId]);

  return <div>{/* Screen content */}</div>;
};
```

❌ **Bad:**
```typescript
const MyScreen = () => {
  const { trackScreenView } = useAnalyticsTracker();

  // Never tracks - no effect
  return <div>{/* Screen content */}</div>;
};
```

**Why:** Screen tracking:
- User journey analysis
- Session tracking
- Navigation patterns
- Drop-off analysis

## Anti-Pattern: Hardcoding Event Parameters

Don't hardcode values that should be dynamic.

❌ **Bad:**
```typescript
const trackItemClick = useCallback(
  (itemId: string) => {
    trackAnalyticsEvent({
      defaultParams: {
        eventName: 'Feature_ItemClick',
        screenName: 'ProductList',  // Hardcoded
        tribe: Tribe.Growth,         // Hardcoded
      },
      parameters: {
        item_id: itemId,
      },
    });
  },
  [trackAnalyticsEvent]
);
```

✅ **Good:**
```typescript
// Use AnalyticsProvider for context
<AnalyticsProvider
  defaultParams={{
    screenName: currentScreen,
    tribe: Tribe.Growth,
  }}
>
  <Component />
</AnalyticsProvider>
```

## Anti-Pattern: Missing trackAnalyticsEvent in Dependencies

Don't forget to include trackAnalyticsEvent in useCallback dependencies.

❌ **Bad:**
```typescript
const trackButtonClick = useCallback(
  (buttonId: string) => {
    trackAnalyticsEvent({
      /* ... */
    });
  },
  [] // Missing trackAnalyticsEvent - stale closure
);
```

✅ **Good:**
```typescript
const trackButtonClick = useCallback(
  (buttonId: string) => {
    trackAnalyticsEvent({
      /* ... */
    });
  },
  [trackAnalyticsEvent] // Include in dependencies
);
```

## Summary

**Key Patterns:**
- Use feature-specific analytics hooks
- Wrap tracking functions with useCallback
- Follow PascalCase naming with feature prefix
- Use snake_case for all parameters
- Always specify destinations explicitly
- Use AnalyticsProvider for context cascading
- Assign tribe to all events
- Include position for list items
- Mock analytics in tests
- Track screen views on mount

**Anti-Patterns to Avoid:**
- Inline tracking without hooks
- Missing useCallback
- Inconsistent naming conventions
- Hardcoded event parameters
- Missing destinations
- No tribe assignment
- Forgetting dependencies in useCallback
- Not mocking in tests
