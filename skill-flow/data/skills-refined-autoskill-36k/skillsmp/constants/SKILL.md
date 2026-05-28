---
name: constants
description: "WHAT: Constants organization with naming conventions and type-safe as const assertions. WHEN: defining test IDs, animation durations, query keys, feature flags. KEYWORDS: constants, SCREAMING_SNAKE_CASE, PascalCase, as const, test IDs, query keys, type safety, naming."
---

# Constants Organization Patterns

## Core Principles

**Organize constants in feature-level constants.ts files.** Use SCREAMING_SNAKE_CASE for primitive constants, PascalCase for grouped constant objects, and always add `as const` for type safety and literal types.

**Why**: Centralized constants prevent magic numbers, improve maintainability, enable easy updates, and provide type-safe access to configuration values.

## When to Use This Skill

Use these patterns when:

- Defining animation durations or timing values
- Organizing test IDs for E2E testing
- Setting up analytics event destinations
- Declaring UI sizes, spacing, or limits
- Managing feature flag keys
- Defining query keys for data access
- Creating configuration constants
- Avoiding magic numbers in code

## File Organization

### Feature-Level Constants

Create `constants.ts` at feature root.

```typescript
features/
└── reactivation-banner-feature/
    ├── components/
    ├── hooks/
    ├── constants.ts          # Feature constants
    └── index.ts
```

**Why**: Feature-level organization keeps constants close to their usage, making them easier to find and maintain.

**Production Example**: `git-resources/shared-mobile-modules/src/features/reactivation-banner-feature/constants.ts:1`

### Module/Library-Level Constants

For shared constants across multiple features:

```typescript
libs/
└── tracing/
    ├── hooks/
    ├── utils/
    ├── constants.ts          # Shared tracing constants
    └── index.ts

data-access/
└── native/
    ├── auth/
    │   └── constants.ts      # Auth repository constants
    ├── plan/
    │   └── constants.ts      # Plan repository constants
    └── constants.ts          # Aggregated repository keys
```

**Why**: Centralized constants at module level enable reuse across features while maintaining clear organization.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/constants.ts:1`

## Naming Conventions

### SCREAMING_SNAKE_CASE for Primitives

Use SCREAMING_SNAKE_CASE for primitive constants.

```typescript
// ✅ Correct - Clear, consistent naming
export const BANNER_ANIMATION_DURATION = 250;
export const API_TIMEOUT_MS = 5000;
export const DEFAULT_LOCALE = 'en-US';
export const MAX_RETRY_ATTEMPTS = 3;

// ❌ Wrong - Inconsistent casing
export const maxRetries = 3;              // camelCase
export const API-TIMEOUT = 5000;          // kebab-case
export const defaultlocale = 'en-US';     // no separator
```

**Why**: SCREAMING_SNAKE_CASE clearly identifies constants at a glance and distinguishes them from variables.

### PascalCase for Constant Objects

Use PascalCase for grouped constant objects.

```typescript
// ✅ Correct - Object naming
export const TestIds = {
  BUTTON: 'submit-button',
  INPUT: 'email-input',
  MODAL: 'confirmation-modal',
} as const;

export const AnimationDurations = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500,
} as const;

export const VitalAttributesKeys = {
  COUNTRY: 'application.real_country',
  LOCALE: 'application.locale',
  CUSTOMER_ID: 'application.customer.id',
} as const;

// ❌ Wrong - Inconsistent naming
export const test_ids = { ... };          // snake_case
export const ANIMATION_DURATIONS = { ... }; // SCREAMING_SNAKE_CASE
```

**Why**: PascalCase for objects differentiates them from primitive constants and follows TypeScript conventions.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/tracing/constants.ts:5`

## Type-Safe Constants with `as const`

### Always Use `as const`

Add `as const` assertion for readonly literal types.

```typescript
// ✅ Correct - Literal types with `as const`
export const TEST_IDS = {
  BUTTON: 'submit-button',
  INPUT: 'email-input',
} as const;

// Type is: { readonly BUTTON: "submit-button"; readonly INPUT: "email-input" }

// ❌ Wrong - Missing `as const`
export const TEST_IDS = {
  BUTTON: 'submit-button',
  INPUT: 'email-input',
};

// Type is: { BUTTON: string; INPUT: string } (too loose)
```

**Why**: `as const` provides:
- Literal types instead of widened types
- Readonly properties (prevents accidental modification)
- Type-safe access to constant values
- Better TypeScript inference

### Extract Type from Constant Object

Create type aliases from constant objects for type-safe usage.

```typescript
export const RecipeCategories = {
  BREAKFAST: 'breakfast',
  LUNCH: 'lunch',
  DINNER: 'dinner',
} as const;

// Extract type from constant object
export type RecipeCategory = (typeof RecipeCategories)[keyof typeof RecipeCategories];
// Type is: "breakfast" | "lunch" | "dinner"

// Usage in function signatures
const getRecipesByCategory = (category: RecipeCategory) => {
  // category is guaranteed to be one of the defined values
};

getRecipesByCategory(RecipeCategories.BREAKFAST); // ✅ Type-safe
getRecipesByCategory('breakfast'); // ✅ Also works (literal type)
getRecipesByCategory('snack'); // ❌ TypeScript error
```

**Why**: Extracting types from constants ensures single source of truth and prevents type/value drift.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/tracing/constants.ts:13`

## Const Objects vs Enums

### Prefer Const Objects Over Enums

Use const objects instead of TypeScript enums.

```typescript
// ✅ Correct - Const object pattern
export const RecipeCategories = {
  BREAKFAST: 'breakfast',
  LUNCH: 'lunch',
  DINNER: 'dinner',
} as const;

export type RecipeCategory = (typeof RecipeCategories)[keyof typeof RecipeCategories];

// Usage
const category = RecipeCategories.BREAKFAST; // 'breakfast'

// ❌ Avoid - TypeScript enum
enum RecipeCategory {
  BREAKFAST = 'breakfast',
  LUNCH = 'lunch',
  DINNER = 'dinner',
}
```

**Why**: Const objects have:
- Better TypeScript support
- Smaller bundle size (no generated code)
- More predictable transpilation
- Easier debugging (values are literal strings)

## Constant Types by Use Case

### Animation Constants

Define animation durations and configurations.

```typescript
// features/reactivation-banner-feature/constants.ts

export const BANNER_ANIMATION_DURATION = 250;
export const BANNER_FADE_ANIMATION_DURATION = 500;
export const BANNER_SLIDE_DISTANCE = 100;

// Grouped variant
export const BannerAnimation = {
  DURATION: 250,
  FADE_DURATION: 500,
  SLIDE_DISTANCE: 100,
} as const;
```

**Why**: Consistent animation timing improves UX and makes global changes easy (e.g., accessibility preferences for reduced motion).

**Production Example**: `git-resources/shared-mobile-modules/src/features/reactivation-banner-feature/constants.ts:1`

### Test IDs

Group test IDs by feature for E2E testing.

```typescript
export const TEST_IDS = {
  // Main components
  EXPANDED_BANNER: 'reactivation-banner-expanded',
  EXPANDED_TITLE: 'reactivation-banner-expanded-title',
  EXPANDED_DESCRIPTION: 'reactivation-banner-expanded-description',

  // Interactive elements
  PLAN_DETAILS_BUTTON: 'reactivation-banner-plan-details-button',
  REVIEW_PLAN_BUTTON: 'reactivation-banner-review-plan-button',

  // Modal elements
  PROMO_CODE_MODAL: 'promo-code-modal',
  PROMO_CODE_INPUT: 'promo-code-modal-input',
  PROMO_CODE_UPDATE_BUTTON: 'promo-code-modal-update-button',

  // Error states
  DISCOUNT_ERROR_DIALOG: 'discount-error-dialog',
  DISCOUNT_ERROR_DIALOG_ICON: 'discount-error-dialog-icon',
} as const;

// Usage in components
<View testID={TEST_IDS.EXPANDED_BANNER}>
  <Text testID={TEST_IDS.EXPANDED_TITLE}>{title}</Text>
  <Button testID={TEST_IDS.REVIEW_PLAN_BUTTON} />
</View>

// Usage in tests
expect(screen.getByTestId(TEST_IDS.EXPANDED_BANNER)).toBeTruthy();
```

**Why**: Grouped test IDs prevent duplication, enable easy lookup, and ensure consistency between implementation and tests.

**Production Example**: `git-resources/shared-mobile-modules/src/features/reactivation-banner-feature/constants.ts:4`

### Analytics Constants

Define analytics destinations and default parameter keys.

```typescript
import type { DefaultAnalyticsParams } from './types';

/**
 * All valid default analytics parameter keys
 * This is the SINGLE SOURCE OF TRUTH - change here when DefaultAnalyticsParams changes
 */
export const DEFAULT_ANALYTICS_KEYS: readonly (keyof DefaultAnalyticsParams)[] =
  [
    'eventName',
    'eventCategory',
    'eventAction',
    'eventLabel',
    'screenName',
    'tribe',
  ] as const;

// Type-safe helper using the constant
export const getValidDefaultAnalyticsKeys = <
  T extends Partial<DefaultAnalyticsParams>,
>(
  params: T
): Array<keyof DefaultAnalyticsParams> => {
  return DEFAULT_ANALYTICS_KEYS.filter(
    (key) => key in params && params[key] != null
  );
};
```

**Why**: Centralized analytics constants ensure consistency across events and enable compile-time validation of parameter keys.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/analytics/constants.ts:11`

### UI Constants

Define spacing, sizes, and limits.

```typescript
export const UI_CONSTANTS = {
  MAX_RECIPE_NAME_LENGTH: 100,
  DEFAULT_PAGE_SIZE: 20,
  MIN_SEARCH_QUERY_LENGTH: 3,
  CARD_BORDER_RADIUS: 8,
  HEADER_HEIGHT: 64,
} as const;

// Configuration objects for complex UI
export const ToastConfig = {
  DEFAULT_DURATION: 5000,
  FADE_DURATION: 300,
  ICON_CONFIG: {
    success: {
      icon: 'CircleCheckmarkOutline24' as const,
      color: 'alias.color.positive.background.default' as const,
    },
    error: {
      icon: 'CircleMinusOutline24' as const,
      color: 'alias.color.negative.background.default' as const,
    },
  },
} as const;
```

**Why**: UI constants enable consistent sizing, prevent magic numbers, and centralize design system values.

**Production Example**: `git-resources/shared-mobile-modules/src/features/toast-feature/constants.ts:5`

### Query Keys for Data Access

Define query keys in data access layer.

```typescript
// data-access/native/plan/constants.ts
export const PLAN_QUERY_KEY = 'plan';

// data-access/native/auth/constants.ts
export const AUTH_QUERY_KEY = 'auth';

// data-access/native/constants.ts - Aggregated
export const NATIVE_MODULES_REPOSITORY_QUERY_KEY = 'nativeRepositories';

/**
 * REPOSITORY_KEYS serves as centralized mapping of repository names
 * to their respective query keys.
 */
export const REPOSITORY_KEYS = {
  auth: AUTH_QUERY_KEY,
  appConfig: APP_CONFIG_QUERY_KEY,
  plan: PLAN_QUERY_KEY,
  navigationBar: NAVIGATION_BAR_QUERY_KEY,
  // ... more repositories
} as const;

// Extract type for type-safe repository access
export type RepositoryName = keyof typeof REPOSITORY_KEYS;
```

**Why**: Centralized query keys prevent cache key conflicts and enable type-safe repository access.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/constants.ts:30`

### Feature Flag Keys

Organize feature flags by module using enums (exception to const object rule).

```typescript
// libs/native-modules/feature-toggle/constants/featureFlagKeys.ts

export enum OnboardingModuleFeatureFlagKeys {
  WELCOME_CAROUSEL_V2_FEATURE_FLAG = 'rnsm_onboarding_welcome_carousel_v2',
}

export enum StoreModuleFeatureFlagKeys {
  RNSM_STOREFRONT_DESELECT_MEALS_CTA = 'rnsm_storefront_deselect_meals_cta',
  RNSM_SEAMLESS_BOX_DOWNGRADE = 'rn_seamless_box_downgrade',
  NEW_APP_ONBOARDING = 'new_app_onboarding',
}

export enum LoyaltyProgramModuleFeatureFlagKeys {
  LOYALTY_PROGRAM = 'loyalty_program',
  SMOOTHIE_BOX_CHALLENGE = 'smoothie_box_challenge',
}

// Union type for all feature flags
type EnumValues<E extends Record<string, string>> = `${E[keyof E]}`;
export type FeatureFlagKeys =
  | EnumValues<typeof OnboardingModuleFeatureFlagKeys>
  | EnumValues<typeof StoreModuleFeatureFlagKeys>
  | EnumValues<typeof LoyaltyProgramModuleFeatureFlagKeys>;
```

**Why**: Enums provide module-based organization for feature flags. This is an exception to the "prefer const objects" rule because feature flags need module-level grouping and exhaustive checking.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/native-modules/feature-toggle/constants/featureFlagKeys.ts:16`

### Tracing Constants

Define span keys and vital attribute keys for OpenTelemetry.

```typescript
/**
 * Constants for vital attributes used in tracing spans
 * These follow OpenTelemetry semantic conventions where applicable
 */
export const VITAL_ATTRIBUTES_KEYS = {
  SYSTEM_COUNTRY: 'application.system_country',
  COUNTRY: 'application.real_country',
  LOCALE: 'application.locale',
  CUSTOMER_UUID: 'application.customer.uuid',
  CUSTOMER_ID: 'application.customer.id',
} as const;

export type VitalAttributeKey =
  (typeof VITAL_ATTRIBUTES_KEYS)[keyof typeof VITAL_ATTRIBUTES_KEYS];

// Usage in tracing
span.setAttribute(
  VITAL_ATTRIBUTES_KEYS.COUNTRY,
  user.country
);
```

**Why**: Standardized attribute keys ensure consistency across all traces and follow OpenTelemetry conventions.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/tracing/constants.ts:5`

## Common Patterns

### Combine Related Constants

Group related constants in objects.

```typescript
export const BannerConfig = {
  ANIMATION_DURATION: 250,
  MAX_HEIGHT: 200,
  PADDING: 16,
  TEST_IDS: {
    CONTAINER: 'banner-container',
    CLOSE_BUTTON: 'banner-close',
    TITLE: 'banner-title',
  },
} as const;

// Access nested constants
const { ANIMATION_DURATION, TEST_IDS } = BannerConfig;
```

**Why**: Grouping prevents constant proliferation and improves organization by keeping related values together.

### Export Individual and Grouped

Export both individual values and grouped objects for flexibility.

```typescript
// Individual exports for convenience
export const ANIMATION_DURATION = 250;
export const MAX_HEIGHT = 200;
export const PADDING = 16;

// Grouped export for namespacing
export const BannerConfig = {
  ANIMATION_DURATION,
  MAX_HEIGHT,
  PADDING,
} as const;

// Usage: import either way
import { ANIMATION_DURATION } from './constants';
import { BannerConfig } from './constants';

// Both work
setTimeout(doSomething, ANIMATION_DURATION);
setTimeout(doSomething, BannerConfig.ANIMATION_DURATION);
```

**Why**: Flexible exports support different usage patterns - direct access for frequently used values, namespaced access for clarity.

### Environment-Specific Constants

Define environment-specific values with runtime checks.

```typescript
// config/constants.ts
export const API_BASE_URL =
  process.env.NODE_ENV === 'production'
    ? 'https://api.yourcompany.com'
    : 'https://api-staging.yourcompany.com';

export const API_TIMEOUT_MS = 30000;
export const MAX_RETRY_ATTEMPTS = 3;

// Feature flag defaults per environment
export const FEATURE_DEFAULTS = {
  enableBetaFeatures: process.env.NODE_ENV !== 'production',
  enableDebugLogging: __DEV__,
} as const;
```

**Why**: Environment constants enable easy configuration changes and clear separation of production vs development behavior.

## Documentation

### Document Purpose with JSDoc

Add comments explaining constant purpose, especially for non-obvious values.

```typescript
/**
 * Maximum number of retry attempts for failed API requests.
 * After this limit, the request fails permanently and the error is surfaced to the user.
 */
export const MAX_RETRY_ATTEMPTS = 3;

/**
 * Animation duration for banner slide-in effect (in milliseconds).
 * Matches Material Design guidelines for medium-sized transitions.
 * @see https://material.io/design/motion/speed.html#duration
 */
export const BANNER_ANIMATION_DURATION = 250;

/**
 * Vital attributes that are automatically injected into all OpenTelemetry spans.
 * These follow the OpenTelemetry semantic conventions for application metadata.
 * @see https://opentelemetry.io/docs/reference/specification/resource/semantic_conventions/
 */
export const VITAL_ATTRIBUTES_KEYS = {
  COUNTRY: 'application.real_country',
  LOCALE: 'application.locale',
  CUSTOMER_ID: 'application.customer.id',
} as const;
```

**Why**: Documentation helps developers understand when and how to use constants, provides context for magic numbers, and links to relevant specifications.

## Testing with Constants

### Use Constants in Tests

Import and use constants in tests to ensure consistency.

```typescript
import { TEST_IDS, ANIMATION_DURATION, BannerConfig } from './constants';

test('renders with correct testID', () => {
  render(<Banner />);
  expect(screen.getByTestId(TEST_IDS.EXPANDED_BANNER)).toBeTruthy();
});

test('animation completes within duration', async () => {
  jest.useFakeTimers();
  render(<Banner />);

  act(() => {
    jest.advanceTimersByTime(ANIMATION_DURATION);
  });

  expect(screen.getByTestId(TEST_IDS.EXPANDED_BANNER)).toHaveStyle({
    opacity: 1,
  });
});

test('banner respects max height', () => {
  render(<Banner />);
  const banner = screen.getByTestId(TEST_IDS.EXPANDED_BANNER);

  expect(banner.props.style.maxHeight).toBe(BannerConfig.MAX_HEIGHT);
});
```

**Why**: Using constants in tests ensures consistency with implementation and makes refactoring easier (change constant value in one place).

## Common Mistakes to Avoid

❌ **Don't use magic numbers**:

```typescript
// ❌ Wrong - What is 250? Why 20?
setTimeout(() => doSomething(), 250);
if (items.length > 20) {
  loadMore();
}
```

✅ **Do use descriptive constants**:

```typescript
// ✅ Correct - Clear intent
export const BANNER_ANIMATION_DURATION_MS = 250;
export const MAX_ITEMS_PER_PAGE = 20;

setTimeout(() => doSomething(), BANNER_ANIMATION_DURATION_MS);
if (items.length > MAX_ITEMS_PER_PAGE) {
  loadMore();
}
```

❌ **Don't forget `as const`**:

```typescript
// ❌ Wrong - Type is too loose
export const TEST_IDS = {
  BUTTON: 'button',
};
// Type is: { BUTTON: string }

// ❌ Wrong - No TypeScript protection
export const RecipeCategories = {
  BREAKFAST: 'breakfast',
  LUNCH: 'lunch',
};
// Type is: { BREAKFAST: string; LUNCH: string }
```

✅ **Do use `as const` for literal types**:

```typescript
// ✅ Correct - Literal types
export const TEST_IDS = {
  BUTTON: 'button',
} as const;
// Type is: { readonly BUTTON: "button" }

// ✅ Correct - Type-safe access
export const RecipeCategories = {
  BREAKFAST: 'breakfast',
  LUNCH: 'lunch',
} as const;
// Type is: { readonly BREAKFAST: "breakfast"; readonly LUNCH: "lunch" }
```

❌ **Don't use inconsistent casing**:

```typescript
// ❌ Wrong - Mixed casing styles
export const maxRetries = 3;              // camelCase
export const API_TIMEOUT = 5000;          // SCREAMING_SNAKE_CASE
export const DefaultLocale = 'en';        // PascalCase
export const test_ids = { ... };          // snake_case
```

✅ **Do use consistent conventions**:

```typescript
// ✅ Correct - SCREAMING_SNAKE_CASE for primitives
export const MAX_RETRIES = 3;
export const API_TIMEOUT_MS = 5000;
export const DEFAULT_LOCALE = 'en-US';

// ✅ Correct - PascalCase for objects
export const TestIds = { ... } as const;
export const ApiConfig = { ... } as const;
```

❌ **Don't duplicate constants**:

```typescript
// ❌ Wrong - Duplicated values
// features/banner/constants.ts
export const ANIMATION_DURATION = 250;

// features/modal/constants.ts
export const ANIMATION_DURATION = 250;  // Duplicate!

// features/drawer/constants.ts
export const ANIMATION_DURATION = 250;  // Another duplicate!
```

✅ **Do centralize shared constants**:

```typescript
// ✅ Correct - Shared animation constants
// libs/animation/constants.ts
export const AnimationDurations = {
  FAST: 150,
  NORMAL: 250,
  SLOW: 500,
} as const;

// features/banner/BannerComponent.tsx
import { AnimationDurations } from '@libs/animation/constants';
const duration = AnimationDurations.NORMAL;
```

❌ **Don't hardcode test IDs in multiple places**:

```typescript
// ❌ Wrong - Hardcoded string
<View testID="reactivation-banner-expanded">
  {/* ... */}
</View>

// tests/Banner.spec.ts
expect(screen.getByTestId('reactivation-banner-expanded')).toBeTruthy();
// Typo: 'reactivation-banner-exanded' - test breaks!
```

✅ **Do use constant test IDs**:

```typescript
// ✅ Correct - Single source of truth
export const TEST_IDS = {
  EXPANDED_BANNER: 'reactivation-banner-expanded',
} as const;

// BannerComponent.tsx
<View testID={TEST_IDS.EXPANDED_BANNER}>
  {/* ... */}
</View>

// tests/Banner.spec.ts
expect(screen.getByTestId(TEST_IDS.EXPANDED_BANNER)).toBeTruthy();
// No typos possible - TypeScript catches errors!
```

## Quick Reference

**Feature-level constants:**
```typescript
// features/my-feature/constants.ts
export const ANIMATION_DURATION = 250;
export const MAX_HEIGHT = 200;

export const TEST_IDS = {
  CONTAINER: 'my-feature-container',
  BUTTON: 'my-feature-button',
} as const;
```

**Type-safe constant objects:**
```typescript
export const RecipeCategories = {
  BREAKFAST: 'breakfast',
  LUNCH: 'lunch',
  DINNER: 'dinner',
} as const;

export type RecipeCategory = (typeof RecipeCategories)[keyof typeof RecipeCategories];
```

**Grouped configuration:**
```typescript
export const ApiConfig = {
  BASE_URL: 'https://api.example.com',
  TIMEOUT_MS: 5000,
  MAX_RETRIES: 3,
} as const;
```

**Feature flags (enum exception):**
```typescript
export enum MyModuleFeatureFlagKeys {
  NEW_UI = 'my_module_new_ui',
  BETA_FEATURE = 'my_module_beta',
}
```

**Naming conventions:**
- Primitives: `SCREAMING_SNAKE_CASE`
- Objects: `PascalCase`
- Always use `as const` for objects
- Prefer const objects over enums (except feature flags)

**Key Libraries:**
- React Native 0.75.4
- TypeScript 5.1.6

For production examples, see [references/examples.md](references/examples.md).
