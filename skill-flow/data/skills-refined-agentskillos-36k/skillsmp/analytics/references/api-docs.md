# Analytics - API Reference

API reference for analytics tracking with Snowplow, Firebase, Adjust, and Statsig.

## Official Documentation

- **Snowplow Browser Tracker**: https://docs.snowplow.io/docs/collecting-data/collecting-from-own-applications/javascript-trackers/browser-tracker/
- **Firebase Analytics**: https://firebase.google.com/docs/analytics/get-started
- **Adjust SDK**: https://help.adjust.com/en/article/sdk-quickstart
- **Statsig**: https://docs.statsig.com/

## Import Statements

```typescript
import { useCallback } from 'react';
import { useAnalyticsTracker } from '@libs/analytics';
import { AnalyticsEventDestination } from '@libs/native-modules/analytics-tracker';
import { Tribe } from '@libs/analytics/types';
import { AnalyticsProvider } from '@libs/analytics/AnalyticsProvider';
```

## useAnalyticsTracker()

Hook for tracking analytics events.

```typescript
function useAnalyticsTracker(): {
  trackAnalyticsEvent: (event: AnalyticsEvent) => void;
  trackScreenView: (screen: ScreenViewEvent) => void;
};
```

**Returns:**
- `trackAnalyticsEvent` - Function to track custom events
- `trackScreenView` - Function to track screen views

**Usage:**
```typescript
const { trackAnalyticsEvent } = useAnalyticsTracker();

trackAnalyticsEvent({
  defaultParams: {
    eventName: 'ButtonClick',
    eventCategory: 'User Interaction',
    eventAction: 'click',
    tribe: Tribe.Growth,
  },
  parameters: {
    button_id: 'submit',
  },
  destinations: [AnalyticsEventDestination.Firebase],
});
```

## Analytics Event Types

### AnalyticsEvent

Structure for tracking custom events.

```typescript
interface AnalyticsEvent {
  defaultParams: DefaultParams;
  parameters?: Record<string, any>;
  destinations: AnalyticsEventDestination[];
}
```

### DefaultParams

Required parameters for all events.

```typescript
interface DefaultParams {
  eventName: string;          // PascalCase, e.g., 'FeatureName_EventName'
  eventCategory: string;      // Category grouping
  eventAction: string;        // camelCase action
  eventLabel?: string;        // Optional label
  screenName?: string;        // Current screen
  tribe: Tribe;              // Team assignment
}
```

### Parameters

Event-specific parameters (snake_case).

```typescript
parameters?: {
  user_id?: string;
  product_id?: string;
  position?: number;
  [key: string]: any;
}
```

### AnalyticsEventDestination

Enum for analytics destinations.

```typescript
enum AnalyticsEventDestination {
  Firebase = 'firebase',
  Adjust = 'adjust',
  Statsig = 'statsig',
  All = 'all',
}
```

**Usage:**
```typescript
destinations: [
  AnalyticsEventDestination.Firebase,
  AnalyticsEventDestination.Adjust,
]
```

### Tribe

Enum for team assignment.

```typescript
enum Tribe {
  Growth = 'growth',
  ShoppingExperience = 'shopping_experience',
  AccountManagement = 'account_management',
  CustomerService = 'customer_service',
}
```

## Screen View Tracking

### trackScreenView()

Track screen navigation.

```typescript
const { trackScreenView } = useAnalyticsTracker();

trackScreenView({
  screenName: 'ProductDetails',
  tribe: Tribe.ShoppingExperience,
  parameters: {
    product_id: '123',
    category: 'recipes',
  },
});
```

**Parameters:**
- `screenName: string` - Screen identifier
- `tribe: Tribe` - Team assignment
- `parameters?: Record<string, any>` - Additional context

## AnalyticsProvider

Provider component for cascading analytics context.

```typescript
<AnalyticsProvider
  defaultParams={{
    screenName: 'Checkout',
    tribe: Tribe.Growth,
  }}
>
  {children}
</AnalyticsProvider>
```

**Props:**
- `defaultParams: Partial<DefaultParams>` - Default parameters for all child events
- `children: ReactNode` - Child components

**Context Cascading:**
```typescript
<AnalyticsProvider defaultParams={{ tribe: Tribe.Growth }}>
  <AnalyticsProvider defaultParams={{ screenName: 'Checkout' }}>
    {/* Events here have tribe: Growth, screenName: Checkout */}
  </AnalyticsProvider>
</AnalyticsProvider>
```

## Feature-Specific Hooks

### Basic Hook Pattern

```typescript
export const useFeatureAnalytics = () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();

  const trackButtonClick = useCallback(
    (buttonId: string) => {
      trackAnalyticsEvent({
        defaultParams: {
          eventName: 'Feature_ButtonClick',
          eventCategory: 'UI Interaction',
          eventAction: 'clickButton',
          tribe: Tribe.Growth,
        },
        parameters: { button_id: buttonId },
        destinations: [AnalyticsEventDestination.Firebase],
      });
    },
    [trackAnalyticsEvent]
  );

  return { trackButtonClick };
};
```

## Event Naming Conventions

### Event Name Format

```
PascalCase with feature prefix: FeatureName_EventName
```

**Examples:**
- `SelectMeals_ParentCategoryClick`
- `Checkout_PaymentMethodSelected`
- `AccountSettings_ProfileUpdated`

### Parameters Format

```
snake_case for all parameters
```

**Examples:**
- `product_id`
- `user_email`
- `number_of_items`

## Testing

### Mock Analytics Tracker

```typescript
jest.mock('@libs/analytics', () => ({
  useAnalyticsTracker: () => ({
    trackAnalyticsEvent: jest.fn(),
    trackScreenView: jest.fn(),
  }),
}));
```

### Test Event Tracking

```typescript
it('tracks button click', () => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();

  render(<MyComponent />);

  fireEvent.click(screen.getByRole('button'));

  expect(trackAnalyticsEvent).toHaveBeenCalledWith({
    defaultParams: {
      eventName: 'Feature_ButtonClick',
      eventCategory: 'UI',
      eventAction: 'click',
      tribe: Tribe.Growth,
    },
    parameters: { button_id: 'submit' },
    destinations: [AnalyticsEventDestination.Firebase],
  });
});
```

## Common Patterns

### Button Click Tracking

```typescript
const { trackButtonClick } = useFeatureAnalytics();

<button onClick={() => trackButtonClick('submit')}>
  Submit
</button>
```

### List Item Click Tracking

```typescript
const { trackItemClick } = useFeatureAnalytics();

items.map((item, index) => (
  <div
    key={item.id}
    onClick={() => trackItemClick(item.id, index)}
  >
    {item.name}
  </div>
))
```

### Form Submission Tracking

```typescript
const handleSubmit = (data: FormData) => {
  trackFormSubmit(data.email);
  submitForm(data);
};
```

## Destination Selection

### Single Destination

```typescript
destinations: [AnalyticsEventDestination.Firebase]
```

### Multiple Destinations

```typescript
destinations: [
  AnalyticsEventDestination.Firebase,
  AnalyticsEventDestination.Adjust,
]
```

### All Destinations

```typescript
destinations: [AnalyticsEventDestination.All]
```

## Error Tracking

```typescript
const trackError = useCallback(
  (error: Error, context: string) => {
    trackAnalyticsEvent({
      defaultParams: {
        eventName: 'Error_Occurred',
        eventCategory: 'Error',
        eventAction: 'throw',
        tribe: Tribe.Engineering,
      },
      parameters: {
        error_message: error.message,
        error_stack: error.stack,
        context,
      },
      destinations: [AnalyticsEventDestination.Firebase],
    });
  },
  [trackAnalyticsEvent]
);
```

## Performance Tracking

```typescript
const trackPageLoad = useCallback(
  (loadTime: number) => {
    trackAnalyticsEvent({
      defaultParams: {
        eventName: 'Performance_PageLoad',
        eventCategory: 'Performance',
        eventAction: 'load',
        tribe: Tribe.Engineering,
      },
      parameters: {
        load_time_ms: loadTime,
        page_url: window.location.href,
      },
      destinations: [AnalyticsEventDestination.Firebase],
    });
  },
  [trackAnalyticsEvent]
);
```
