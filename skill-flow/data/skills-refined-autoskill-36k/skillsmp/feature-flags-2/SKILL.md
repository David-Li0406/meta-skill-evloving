---
name: feature-flags
description: "WHAT: Feature flag management with useFeatureIsEnabled hook for gradual rollouts. WHEN: implementing A/B tests, conditional rendering, gradual feature releases. KEYWORDS: feature flag, useFeatureIsEnabled, rollout, A/B test, toggle, experiment, flag, variant."
---

# Feature Flags

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns


## Core Principles

**Always use feature flag constants instead of hardcoded strings.** Feature flag keys must be defined as constants in FEATURE_FLAG_KEYS objects (ProfileServiceModuleFeatureFlagKeys, StoreModuleFeatureFlagKeys, etc.) with SCREAMING_SNAKE_CASE naming. Never hardcode feature flag strings directly in useFeatureIsEnabled calls.

**Always handle async initialization loading states.** useFeatureIsEnabled returns false initially until the feature flag SDK initializes. For UI-critical decisions, implement loading states or use timeouts to prevent flashing the wrong UI variant while initializing.

**Use custom wrapper hooks for reusable feature flag checks.** Create named hooks like useIsShortShippingEnabled() that encapsulate feature flag logic with constants. This provides better discoverability, type safety, and prevents duplicate feature flag checks across components.

**Always mock useFeatureIsEnabled in tests.** Feature flag tests must mock useFeatureIsEnabled to test both enabled and disabled states. Use jest.mock with mockReturnValue(true/false) to ensure components behave correctly under all feature flag configurations.

**Why**: Feature flags enable gradual rollouts, A/B testing, quick feature toggles without deployments, and targeted feature releases while maintaining code safety through constants and comprehensive testing.

## When to Use This Skill

Use these patterns when:

- Implementing gradual feature rollouts to subsets of users
- A/B testing different UI implementations or flows
- Building features that need quick kill switches
- Targeting features to specific user segments (plan, country, userId)
- Testing new features in production with limited exposure
- Conditionally rendering components based on feature state
- Switching between feature variants for experiments
- Tracking feature adoption and impact with analytics
- Rolling back features instantly without deployments
- Developing features behind flags before full release

## useFeatureIsEnabled Hook

### Basic Usage

Check if a feature is enabled with feature flag constants.

```typescript
import { useFeatureIsEnabled } from '@libs/native-modules/feature-toggle';
import { ProfileServiceModuleFeatureFlagKeys } from '@libs/native-modules/feature-toggle';

const RecipeListScreen = () => {
  const isNewRecipeUIEnabled = useFeatureIsEnabled(
    ProfileServiceModuleFeatureFlagKeys.NEW_RECIPE_UI
  );

  if (isNewRecipeUIEnabled) {
    return <NewRecipeList />;
  }

  return <LegacyRecipeList />;
};
```

**Why**: useFeatureIsEnabled provides async feature flag checks with automatic state management. Returns boolean indicating feature state for the current user. Always use constants from ProfileServiceModuleFeatureFlagKeys, StoreModuleFeatureFlagKeys, etc. for type safety and preventing typos.

**Production Example**: `operations/profile-service/feature-flags/useIsShortShippingEnabled.ts:1`

### With User Segmentation Attributes

Pass user attributes for targeted feature flags (gradual rollouts to specific segments).

```typescript
import { useFeatureIsEnabled } from '@libs/native-modules/feature-toggle';
import { StoreModuleFeatureFlagKeys } from '@libs/native-modules/feature-toggle';

const CheckoutScreen = () => {
  const isPremiumCheckoutEnabled = useFeatureIsEnabled(
    StoreModuleFeatureFlagKeys.PREMIUM_CHECKOUT,
    {
      userId: user.id,
      plan: user.plan,
      country: user.country,
    }
  );

  return isPremiumCheckoutEnabled ? <PremiumCheckout /> : <StandardCheckout />;
};
```

**Why**: Attributes enable targeting specific user segments (plans, countries, user IDs) for gradual rollouts. SDK uses attributes to determine feature eligibility based on server-side rules. Enables percentage rollouts, user targeting, and segmented experiments.

## Feature Flag Constants

### Define Module-Specific Constants

Create module-specific feature flag key objects with SCREAMING_SNAKE_CASE names.

```typescript
// libs/native-modules/feature-toggle/constants/ProfileServiceModuleFeatureFlagKeys.ts
export const ProfileServiceModuleFeatureFlagKeys = {
  RTEA_SHORT_SHIPPING: 'rtea_short_shipping',
  MEAL_PREF_EXTRACTION: 'meal_pref_extraction',
  PROFILE_ONBOARDING_V2: 'profile_onboarding_v2',
} as const;

export type ProfileServiceFeatureFlags =
  (typeof ProfileServiceModuleFeatureFlagKeys)[keyof typeof ProfileServiceModuleFeatureFlagKeys];

// libs/native-modules/feature-toggle/constants/StoreModuleFeatureFlagKeys.ts
export const StoreModuleFeatureFlagKeys = {
  RNSM_SEAMLESS_BOX_DOWNGRADE: 'rnsm_seamless_box_downgrade',
  CHECKOUT_NEW_FLOW: 'checkout_new_flow',
  RECIPE_RECOMMENDATIONS: 'recipe_recommendations',
} as const;

export type StoreFeatureFlags =
  (typeof StoreModuleFeatureFlagKeys)[keyof typeof StoreModuleFeatureFlagKeys];
```

**Why**: Module-specific constants organize feature flags by domain (ProfileService, Store, etc.) for better discoverability. SCREAMING_SNAKE_CASE prevents typos and enables IDE autocomplete. `as const` makes keys readonly for type safety. Type extraction enables type-safe string unions.

### Naming Convention

Use SCREAMING_SNAKE_CASE for feature flag key constants, prefix with module abbreviation.

```typescript
// ✅ Good names - descriptive with module prefix
ProfileServiceModuleFeatureFlagKeys.RTEA_SHORT_SHIPPING;
StoreModuleFeatureFlagKeys.RNSM_SEAMLESS_BOX_DOWNGRADE;
StoreModuleFeatureFlagKeys.CHECKOUT_APPLE_PAY;
ProfileServiceModuleFeatureFlagKeys.PROFILE_ONBOARDING_V2;

// ❌ Bad names
FEATURE_FLAG_KEYS.newCheckout; // Wrong case, no module prefix
FEATURE_FLAG_KEYS.feature1; // Not descriptive
FEATURE_FLAG_KEYS.CHECKOUT; // Too generic
```

**Why**: Consistent naming with module prefixes makes feature flags easy to find, understand ownership, and prevents naming collisions. SCREAMING_SNAKE_CASE follows constant convention and improves readability.

## Custom Wrapper Hooks

### Create Reusable Feature Flag Hooks

Wrap useFeatureIsEnabled in custom hooks for reusability and discoverability.

```typescript
// operations/profile-service/feature-flags/useIsShortShippingEnabled.ts
import {
  useFeatureIsEnabled,
  ProfileServiceModuleFeatureFlagKeys,
} from '@libs/native-modules/feature-toggle';

export const useIsShortShippingEnabled = () => {
  return useFeatureIsEnabled(
    ProfileServiceModuleFeatureFlagKeys.RTEA_SHORT_SHIPPING
  );
};

// Usage in components
import { useIsShortShippingEnabled } from '@operations/profile-service/feature-flags/useIsShortShippingEnabled';

const ShippingScreen = () => {
  const isShortShippingEnabled = useIsShortShippingEnabled();

  return isShortShippingEnabled ? <ShortShippingFlow /> : <StandardShippingFlow />;
};
```

**Why**: Custom wrapper hooks provide clear intent (useIsShortShippingEnabled vs useFeatureIsEnabled), prevent duplicate feature flag constant usage, improve discoverability through named hooks, enable easier refactoring, and make testing simpler (mock single hook instead of multiple useFeatureIsEnabled calls).

**Production Example**: `operations/profile-service/feature-flags/useIsShortShippingEnabled.ts:1`

### Wrapper Hooks with Additional Logic

Add computed logic or multiple feature flag combinations in wrapper hooks.

```typescript
// operations/meal-selection-listener/useMealSelectionListener.ts
import {
  StoreModuleFeatureFlagKeys,
  useFeatureIsEnabled,
} from '@libs/native-modules/feature-toggle';

export const useMealSelectionListener = ({ deliveryId }) => {
  const isSeamlessDowngradeEnabled = useFeatureIsEnabled(
    StoreModuleFeatureFlagKeys.RNSM_SEAMLESS_BOX_DOWNGRADE
  );

  const [updateCart, { loading }] = useUpdateCartMutation({
    variables: {
      planId,
      deliveryId,
      selectionInput: selectionToSave ?? [],
      isSeamlessDowngradeEnabled, // Pass to mutation
    },
    onCompleted,
    onError,
  });

  // Feature flag affects mutation behavior
  return { updateCart, loading };
};
```

**Why**: Wrapper hooks can pass feature flags to mutations, combine multiple flags, or add conditional logic. Encapsulates feature flag complexity and makes components cleaner.

**Production Example**: `operations/meal-selection-listener/useMealSelectionListener.ts:97`

## Conditional Rendering

### Feature-Gated Components

Show/hide components based on feature flags with early returns.

```typescript
import { useIsShortShippingEnabled } from '@operations/profile-service/feature-flags/useIsShortShippingEnabled';

const ShippingOptionsScreen = () => {
  const isShortShippingEnabled = useIsShortShippingEnabled();

  return (
    <View>
      <Header />
      {isShortShippingEnabled && <ShortShippingBanner />}
      <StandardShippingOptions />
    </View>
  );
};

// Or with early return for different component trees
const CheckoutFlow = () => {
  const isNewCheckoutEnabled = useFeatureIsEnabled(
    StoreModuleFeatureFlagKeys.CHECKOUT_NEW_FLOW
  );

  if (isNewCheckoutEnabled) {
    return <NewCheckoutScreen />;
  }

  return <LegacyCheckoutScreen />;
};
```

**Why**: Conditional rendering enables gradual feature rollouts and quick rollbacks. Early returns prevent rendering unused component trees. Feature flags isolate new code paths from production until ready.

### Variant Selection with Switch

Choose between multiple variants using feature flag values for A/B testing.

```typescript
const CheckoutScreen = () => {
  const checkoutVariant = useFeatureIsEnabled(
    StoreModuleFeatureFlagKeys.CHECKOUT_VARIANT
  );

  switch (checkoutVariant) {
    case 'variantA':
      return <CheckoutVariantA />;
    case 'variantB':
      return <CheckoutVariantB />;
    case 'variantC':
      return <CheckoutVariantC />;
    default:
      return <DefaultCheckout />;
  }
};
```

**Why**: Switch statements enable multi-variant A/B testing. Feature flag can return string values ('variantA', 'variantB') instead of booleans for complex experiments. Default case provides fallback when variant is undefined.

## Loading State Handling

### Handle Async Initialization

useFeatureIsEnabled returns false initially until SDK initializes - implement loading states for UI-critical decisions.

```typescript
import { useState, useEffect } from 'react';
import { useFeatureIsEnabled } from '@libs/native-modules/feature-toggle';
import { StoreModuleFeatureFlagKeys } from '@libs/native-modules/feature-toggle';

const RecipeListScreen = () => {
  const isNewUIEnabled = useFeatureIsEnabled(
    StoreModuleFeatureFlagKeys.NEW_RECIPE_UI
  );
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    // Wait for feature flag SDK to initialize
    const timer = setTimeout(() => setIsInitialized(true), 100);
    return () => clearTimeout(timer);
  }, []);

  if (!isInitialized) {
    return <LoadingSpinner />;
  }

  return isNewUIEnabled ? <NewRecipeList /> : <LegacyRecipeList />;
};
```

**Why**: Feature flag SDK initialization is async and returns false before ready. Without loading state, UI briefly renders wrong variant (false) then switches, causing flash. Timeout ensures SDK has time to initialize before rendering decision-critical UI.

### Alternative: Skeleton Loading

Show skeleton UI while feature flag initializes instead of spinner.

```typescript
const ProductListScreen = () => {
  const isNewLayoutEnabled = useFeatureIsEnabled(
    StoreModuleFeatureFlagKeys.PRODUCT_LAYOUT_V2
  );
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsReady(true), 100);
    return () => clearTimeout(timer);
  }, []);

  if (!isReady) {
    return <ProductListSkeleton />;
  }

  return isNewLayoutEnabled ? <ProductListV2 /> : <ProductListV1 />;
};
```

**Why**: Skeleton loaders provide better UX than spinners for feature flag initialization. Shows expected layout structure immediately while waiting for SDK, reducing perceived loading time.

## Testing Feature Flags

### Mock useFeatureIsEnabled

Mock useFeatureIsEnabled to test both enabled and disabled states.

```typescript
// useIsShortShippingEnabled.spec.ts
import { renderHook } from '@testing-library/react-native';
import {
  useFeatureIsEnabled,
  ProfileServiceModuleFeatureFlagKeys,
} from '@libs/native-modules/feature-toggle';
import { useIsShortShippingEnabled } from './useIsShortShippingEnabled';

jest.mock('@libs/native-modules/feature-toggle', () => ({
  useFeatureIsEnabled: jest.fn(),
  ProfileServiceModuleFeatureFlagKeys: {
    RTEA_SHORT_SHIPPING: 'rtea_short_shipping',
  },
}));

describe('useIsShortShippingEnabled', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should return true when feature flag is enabled', () => {
    (useFeatureIsEnabled as jest.Mock).mockReturnValue(true);

    const { result } = renderHook(() => useIsShortShippingEnabled());

    expect(result.current).toBe(true);
    expect(useFeatureIsEnabled).toHaveBeenCalledWith(
      ProfileServiceModuleFeatureFlagKeys.RTEA_SHORT_SHIPPING
    );
  });

  it('should return false when feature flag is disabled', () => {
    (useFeatureIsEnabled as jest.Mock).mockReturnValue(false);

    const { result } = renderHook(() => useIsShortShippingEnabled());

    expect(result.current).toBe(false);
  });
});
```

**Why**: Mocking enables testing both feature flag states (enabled/disabled) without SDK. Tests verify correct flag key usage, correct behavior under both states, and proper integration with components. renderHook tests custom wrapper hooks, while render() tests components with feature flags.

**Production Example**: `operations/profile-service/feature-flags/useIsShortShippingEnabled.spec.ts:1`

### Mock in Component Tests

Mock feature flags in component tests to verify conditional rendering.

```typescript
import { render, screen } from '@testing-library/react-native';
import { useFeatureIsEnabled } from '@libs/native-modules/feature-toggle';
import { RecipeListScreen } from './RecipeListScreen';

jest.mock('@libs/native-modules/feature-toggle', () => ({
  useFeatureIsEnabled: jest.fn(),
  StoreModuleFeatureFlagKeys: {
    NEW_RECIPE_UI: 'new_recipe_ui',
  },
}));

describe('<RecipeListScreen />', () => {
  it('renders new UI when feature is enabled', () => {
    (useFeatureIsEnabled as jest.Mock).mockReturnValue(true);

    render(<RecipeListScreen />);

    expect(screen.getByTestId('new-recipe-list')).toBeTruthy();
    expect(screen.queryByTestId('legacy-recipe-list')).toBeFalsy();
  });

  it('renders legacy UI when feature is disabled', () => {
    (useFeatureIsEnabled as jest.Mock).mockReturnValue(false);

    render(<RecipeListScreen />);

    expect(screen.getByTestId('legacy-recipe-list')).toBeTruthy();
    expect(screen.queryByTestId('new-recipe-list')).toBeFalsy();
  });
});
```

**Why**: Component tests verify conditional rendering works correctly under both feature flag states. mockReturnValue(true/false) simulates different configurations. queryByTestId verifies opposite variant doesn't render (returns null).

## Analytics with Feature Flags

### Track Feature Flag State

Include feature flag state in analytics events to measure impact.

```typescript
import { useEffect } from 'react';
import { useFeatureIsEnabled } from '@libs/native-modules/feature-toggle';
import { StoreModuleFeatureFlagKeys } from '@libs/native-modules/feature-toggle';
import { useAnalyticsTracker } from '@libs/analytics';

const CheckoutScreen = () => {
  const isNewCheckoutEnabled = useFeatureIsEnabled(
    StoreModuleFeatureFlagKeys.NEW_CHECKOUT_FLOW
  );
  const { trackEvent } = useAnalyticsTracker();

  useEffect(() => {
    trackEvent('checkout_started', {
      checkout_variant: isNewCheckoutEnabled ? 'new' : 'legacy',
      feature_flag: 'new_checkout_flow',
      flag_enabled: isNewCheckoutEnabled,
    });
  }, [isNewCheckoutEnabled, trackEvent]);

  return isNewCheckoutEnabled ? <NewCheckout /> : <LegacyCheckout />;
};
```

**Why**: Tracking feature flag state in analytics enables measuring feature impact (conversion rates, engagement, errors) across variants. Helps inform rollout decisions and quantify feature success. Include both variant name and boolean flag state for analysis.

## Feature Flag Organization

### Group by Module/Domain

Organize feature flags by module or domain for better discoverability.

```typescript
// ProfileService module flags
export const ProfileServiceModuleFeatureFlagKeys = {
  // Shipping features
  RTEA_SHORT_SHIPPING: 'rtea_short_shipping',
  RTEA_DELIVERY_PREFERENCES: 'rtea_delivery_preferences',

  // Onboarding features
  PROFILE_ONBOARDING_V2: 'profile_onboarding_v2',
  MEAL_PREF_EXTRACTION: 'meal_pref_extraction',
} as const;

// Store module flags
export const StoreModuleFeatureFlagKeys = {
  // Checkout features
  CHECKOUT_NEW_FLOW: 'checkout_new_flow',
  CHECKOUT_APPLE_PAY: 'checkout_apple_pay',
  CHECKOUT_SAVED_CARDS: 'checkout_saved_cards',

  // Product features
  RNSM_SEAMLESS_BOX_DOWNGRADE: 'rnsm_seamless_box_downgrade',
  RECIPE_RECOMMENDATIONS: 'recipe_recommendations',
  PRODUCT_LAYOUT_V2: 'product_layout_v2',
} as const;
```

**Why**: Grouping feature flags by module (ProfileService, Store) and subdomain (Shipping, Checkout) makes flags easier to find, understand ownership, and maintain. Comments organize related flags within modules. Module-specific exports prevent massive single FEATURE_FLAG_KEYS object.

## Common Mistakes to Avoid

❌ **Don't hardcode feature flag keys**:

```typescript
// ❌ Wrong - hardcoded string
const isEnabled = useFeatureIsEnabled('new_checkout');
```

**Why**: Hardcoded strings cause typos, no IDE autocomplete, difficult refactoring, and no type safety.

✅ **Do use feature flag constants**:

```typescript
// ✅ Correct - constant from module
import { StoreModuleFeatureFlagKeys } from '@libs/native-modules/feature-toggle';

const isEnabled = useFeatureIsEnabled(
  StoreModuleFeatureFlagKeys.NEW_CHECKOUT_FLOW
);
```

**Why**: Constants prevent typos, enable IDE autocomplete, provide type safety, and make refactoring easier.

❌ **Don't forget loading states for UI-critical decisions**:

```typescript
// ❌ Wrong - no loading state
const RecipeScreen = () => {
  const isNewUI = useFeatureIsEnabled(
    StoreModuleFeatureFlagKeys.NEW_RECIPE_UI
  );

  // Flashes LegacyUI (false) before SDK initializes
  return isNewUI ? <NewRecipeUI /> : <LegacyRecipeUI />;
};
```

**Why**: Feature flag SDK initialization is async. Without loading state, UI renders false variant briefly before SDK initializes, causing visible flash of wrong UI.

✅ **Do handle async initialization**:

```typescript
// ✅ Correct - loading state prevents flash
const RecipeScreen = () => {
  const isNewUI = useFeatureIsEnabled(
    StoreModuleFeatureFlagKeys.NEW_RECIPE_UI
  );
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsReady(true), 100);
    return () => clearTimeout(timer);
  }, []);

  if (!isReady) return <LoadingSkeleton />;

  return isNewUI ? <NewRecipeUI /> : <LegacyRecipeUI />;
};
```

**Why**: Loading state (spinner or skeleton) prevents flash by waiting for SDK initialization before rendering UI-critical decision.

❌ **Don't skip testing both feature flag states**:

```typescript
// ❌ Wrong - only tests enabled state
describe('CheckoutScreen', () => {
  it('renders new checkout', () => {
    (useFeatureIsEnabled as jest.Mock).mockReturnValue(true);
    render(<CheckoutScreen />);
    expect(screen.getByTestId('new-checkout')).toBeTruthy();
  });
  // Missing test for disabled state
});
```

**Why**: Testing only one state (enabled) misses bugs in the other state (disabled). Both code paths must be tested.

✅ **Do test both enabled and disabled states**:

```typescript
// ✅ Correct - tests both states
describe('CheckoutScreen', () => {
  it('renders new checkout when enabled', () => {
    (useFeatureIsEnabled as jest.Mock).mockReturnValue(true);
    render(<CheckoutScreen />);
    expect(screen.getByTestId('new-checkout')).toBeTruthy();
    expect(screen.queryByTestId('legacy-checkout')).toBeFalsy();
  });

  it('renders legacy checkout when disabled', () => {
    (useFeatureIsEnabled as jest.Mock).mockReturnValue(false);
    render(<CheckoutScreen />);
    expect(screen.getByTestId('legacy-checkout')).toBeTruthy();
    expect(screen.queryByTestId('new-checkout')).toBeFalsy();
  });
});
```

**Why**: Testing both states ensures both code paths work correctly. Verifies conditional rendering, prevents regressions, and validates feature flag integration.

❌ **Don't use generic or vague flag names**:

```typescript
// ❌ Wrong - too generic
FEATURE_FLAG_KEYS.NEW_FEATURE;
FEATURE_FLAG_KEYS.EXPERIMENT_1;
FEATURE_FLAG_KEYS.CHECKOUT;
```

**Why**: Generic names don't describe what feature does, difficult to understand purpose, and prone to naming collisions across modules.

✅ **Do use descriptive names with module prefixes**:

```typescript
// ✅ Correct - descriptive with module prefix
StoreModuleFeatureFlagKeys.RNSM_SEAMLESS_BOX_DOWNGRADE;
ProfileServiceModuleFeatureFlagKeys.RTEA_SHORT_SHIPPING;
StoreModuleFeatureFlagKeys.CHECKOUT_APPLE_PAY;
```

**Why**: Descriptive names with module prefixes make purpose clear, prevent collisions, and indicate ownership.

## Quick Reference

**Basic feature flag check**:
```typescript
import { useFeatureIsEnabled, StoreModuleFeatureFlagKeys } from '@libs/native-modules/feature-toggle';

const isEnabled = useFeatureIsEnabled(StoreModuleFeatureFlagKeys.NEW_FEATURE);
```

**Custom wrapper hook**:
```typescript
// Define hook
export const useIsShortShippingEnabled = () => {
  return useFeatureIsEnabled(
    ProfileServiceModuleFeatureFlagKeys.RTEA_SHORT_SHIPPING
  );
};

// Use in component
const isEnabled = useIsShortShippingEnabled();
```

**Conditional rendering**:
```typescript
const Screen = () => {
  const isNewUI = useFeatureIsEnabled(StoreModuleFeatureFlagKeys.NEW_UI);

  if (isNewUI) {
    return <NewScreen />;
  }

  return <LegacyScreen />;
};
```

**With loading state**:
```typescript
const [isReady, setIsReady] = useState(false);

useEffect(() => {
  const timer = setTimeout(() => setIsReady(true), 100);
  return () => clearTimeout(timer);
}, []);

if (!isReady) return <LoadingSkeleton />;
```

**Mock in tests**:
```typescript
jest.mock('@libs/native-modules/feature-toggle', () => ({
  useFeatureIsEnabled: jest.fn(),
  StoreModuleFeatureFlagKeys: { NEW_FEATURE: 'new_feature' },
}));

(useFeatureIsEnabled as jest.Mock).mockReturnValue(true); // or false
```

**Feature flag constants**:
```typescript
export const ModuleFeatureFlagKeys = {
  FEATURE_NAME: 'feature_name', // SCREAMING_SNAKE_CASE
} as const;

export type ModuleFeatureFlags =
  (typeof ModuleFeatureFlagKeys)[keyof typeof ModuleFeatureFlagKeys];
```

**With analytics**:
```typescript
trackEvent('feature_used', {
  feature_flag: 'new_checkout',
  flag_enabled: isNewCheckoutEnabled,
  variant: isNewCheckoutEnabled ? 'new' : 'legacy',
});
```

**Key Libraries:**
- @libs/native-modules/feature-toggle (custom native module)
- react-native 0.75.4
- @testing-library/react-native 12.9.0

For production examples, see [references/examples.md](references/examples.md).
