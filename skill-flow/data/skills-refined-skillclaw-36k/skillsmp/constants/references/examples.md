# Constants - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating constants organization patterns.

## Example 1: Feature-Level Constants with Animation and Test IDs

**File**: `features/reactivation-banner-feature/constants.ts`

This shows the standard pattern for feature-level constants with animation durations and comprehensive test IDs.

```typescript
export const BANNER_ANIMATION_DURATION = 250;
export const BANNER_FADE_ANIMATION_DURATION = 500;

export const TEST_IDS = {
  EXPANDED_BANNER: 'reactivation-banner-expanded',
  EXPANDED_TITLE: 'reactivation-banner-expanded-title',
  EXPANDED_DESCRIPTION: 'reactivation-banner-expanded-description',
  PLAN_CONTAINER: 'reactivation-banner-plan-container',
  PLAN_TITLE: 'reactivation-banner-plan-title',
  DISCOUNT_PILL: 'reactivation-banner-discount-pill',
  PLAN_DETAILS_BUTTON: 'reactivation-banner-plan-details-button',
  REVIEW_PLAN_BUTTON: 'reactivation-banner-review-plan-button',
  PROMO_CODE_CONTAINER: 'reactivation-banner-promo-code-container',
  PROMO_CODE_CTA_CONTAINER: 'reactivation-banner-promo-code-cta-container',
  PROMO_CODE_CTA_BUTTON: 'reactivation-banner-promo-code-cta-button',
  APPLY_CODE_BUTTON: 'reactivation-banner-apply-code-button',
  PROMO_CODE_COMPACT_BUTTON: 'reactivation-banner-promo-code-details-compact',
  COLLAPSED_BANNER: 'reactivation-banner-collapsed',
  COLLAPSED_TITLE: 'reactivation-banner-collapsed-title',
  COLLAPSED_DESCRIPTION: 'reactivation-banner-collapsed-description',

  // Promo Code Modal
  PROMO_CODE_MODAL: 'promo-code-modal',
  PROMO_CODE_MODAL_TITLE: 'promo-code-modal-title',
  PROMO_CODE_INPUT: 'promo-code-modal-input',
  PROMO_CODE_UPDATE_BUTTON: 'promo-code-modal-update-button',
  PROMO_CODE_INFO_TEXT: 'promo-code-modal-info-text',
  PROMO_CODE_BENEFIT_TEXT: 'promo-code-modal-benefit-text',

  GLOBAL_REACTIVATION_BUTTON: 'reactivation-banner-global-reactivation-button',

  // Discount Error Dialog
  DISCOUNT_ERROR_DIALOG: 'discount-error-dialog',
  DISCOUNT_ERROR_DIALOG_ICON: 'discount-error-dialog-icon',
  DISCOUNT_ERROR_DIALOG_PRIMARY_BUTTON: 'discount-error-dialog-primary-button',

  // Promo Code Comparison Modal
  PROMO_CODE_SWAP_MODAL: 'promo-code-swap-modal',
  PROMO_CODE_SWAP_TITLE: 'promo-code-swap-modal-title',
  PROMO_CODE_SWAP_CURRENT: 'promo-code-swap-current',
  PROMO_CODE_SWAP_NEW: 'promo-code-swap-new',
  UPDATE_PROMO_BUTTON: 'update-promo-button',
  KEEP_PROMO_BUTTON: 'keep-promo-button',
};
```

**Key patterns demonstrated:**
- SCREAMING_SNAKE_CASE for primitive constants (BANNER_ANIMATION_DURATION)
- PascalCase for the TEST_IDS object
- No `as const` in original (should be added for type safety)
- Grouped test IDs by logical sections (Main, Promo Code Modal, Discount Error Dialog)
- Comment headers to organize related test IDs
- Descriptive naming: feature prefix + component + element (reactivation-banner-expanded-title)
- Animation durations in milliseconds (250, 500)

## Example 2: Simple Feature Constants

**File**: `features/country-selection/constants.ts`

This shows a minimal feature constants file with a single tracing ID.

```typescript
export const COUNTRY_SELECTION_TRACE_ID = 'rnsm_onboarding_country_selection';
```

**Key patterns demonstrated:**
- SCREAMING_SNAKE_CASE for primitive constant
- Descriptive name indicating purpose (TRACE_ID for performance tracing)
- Namespaced value: module_domain_feature (rnsm_onboarding_country_selection)
- Single constant file is fine when feature only needs one value

## Example 3: Toast Feature with Type-Safe Configuration

**File**: `features/toast-feature/constants.ts`

This demonstrates complex configuration constants with TypeScript integration.

```typescript
import type { ColorType, IconsType } from '@zest/react-native';

import type { ToastVariant } from './types';

export const DEFAULT_TOAST_DURATION = 5000;
export const TOAST_FADE_DURATION = 300;

type ToastIconConfig = {
  icon: IconsType;
  color: ColorType;
};

export const TOAST_ICON_CONFIG: Record<ToastVariant, ToastIconConfig> = {
  success: {
    icon: 'CircleCheckmarkOutline24',
    color: 'alias.color.positive.background.default',
  },
  error: {
    icon: 'CircleMinusOutline24',
    color: 'alias.color.negative.background.default',
  },
  info: {
    icon: 'CircleInfoOutline24',
    color: 'alias.color.info.background.default',
  },
  warning: {
    icon: 'CircleMinusOutline24',
    color: 'alias.color.warning.background.default',
  },
};
```

**Key patterns demonstrated:**
- SCREAMING_SNAKE_CASE for primitive durations (DEFAULT_TOAST_DURATION)
- Type-safe configuration object (TOAST_ICON_CONFIG)
- Record<ToastVariant, ToastIconConfig> provides exhaustive checking
- Configuration maps variants to icon + color combinations
- Design system token references (alias.color.positive.background.default)
- Zest design system types (IconsType, ColorType)
- Should add `as const` to TOAST_ICON_CONFIG for literal types

## Example 4: Data Access Repository Constants

**File**: `data-access/native/constants.ts`

This shows centralized repository constants aggregating individual repository query keys.

```typescript
import { APP_CONFIG_QUERY_KEY } from './app-config/constants';
import { AUTH_QUERY_KEY } from './auth/constants';
import { INBOX_SALESFORCE_QUERY_KEY } from './inbox-salesforce/constants';
import { LOYALTY_BANNER_QUERY_KEY } from './loyalty-banner/constants';
import { LOYALTY_PROGRAM_STATE_QUERY_KEY } from './loyalty-program-state/constants';
import { NATIVE_NAVIGATION_RESULT_QUERY_KEY } from './navigation/constants';
import { NAVIGATION_BAR_QUERY_KEY } from './navigation-bar/constants';
import { PLAN_QUERY_KEY } from './plan/constants';
// @PLOP_INSERT_REPOSITORY_CONSTANT_IMPORT

/**
 * @context The base query key for all native repositories used within a useQuery hook.
 */
export const NATIVE_MODULES_REPOSITORY_QUERY_KEY = 'nativeRepositories';

/**
 * @context REPOSITORY_KEYS serves as a centralized mapping of repository names
 * to their respective query keys. These keys are imported from various data-access domain
 * subdirectories (e.g., `data-access/auth/constants.ts`, `data-access/appConfig/constants.ts`).
 *
 * This object is used to:
 * - Standardize repository names across the application.
 * - Ensure that repository query keys are referenced consistently.
 * - Provide a single source of truth for defining repository names that can be
 *   dynamically converted into a TypeScript type.
 *
 * It is primarily used in:
 * - Type definitions (`DataAccess.RepositoryName`) to enforce strict typing for repository names.
 */
export const REPOSITORY_KEYS = {
  auth: AUTH_QUERY_KEY,
  appConfig: APP_CONFIG_QUERY_KEY,
  plan: PLAN_QUERY_KEY,
  navigationBar: NAVIGATION_BAR_QUERY_KEY,
  nativeNavigation: NATIVE_NAVIGATION_RESULT_QUERY_KEY,
  loyaltyBanner: LOYALTY_BANNER_QUERY_KEY,
  inboxSalesforce: INBOX_SALESFORCE_QUERY_KEY,
  loyaltyProgramState: LOYALTY_PROGRAM_STATE_QUERY_KEY,
  // @PLOP_INSERT_REPOSITORY_QUERY_KEY
} as const;
```

**Key patterns demonstrated:**
- Import individual constants from subdirectories
- Aggregate into single REPOSITORY_KEYS object
- `as const` for type safety (enables extracting RepositoryName type)
- Comprehensive JSDoc comments explaining purpose and usage
- Plop insertion markers for code generation
- camelCase keys map to SCREAMING_SNAKE_CASE values
- Single source of truth for repository names
- Used for type definitions: `type RepositoryName = keyof typeof REPOSITORY_KEYS`

## Example 5: Tracing Vital Attributes Constants

**File**: `libs/tracing/constants.ts`

This demonstrates OpenTelemetry semantic convention constants with type extraction.

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
```

**Key patterns demonstrated:**
- PascalCase for VITAL_ATTRIBUTES_KEYS object
- SCREAMING_SNAKE_CASE for keys within the object
- `as const` for literal type inference
- Type extraction: `typeof VITAL_ATTRIBUTES_KEYS[keyof typeof VITAL_ATTRIBUTES_KEYS]`
- Type is: "application.system_country" | "application.real_country" | "application.locale" | ...
- Dotted notation for hierarchical attributes (application.customer.id)
- JSDoc explains purpose and references OpenTelemetry conventions
- Named export for the type (VitalAttributeKey)

## Example 6: Analytics Constants with Type-Safe Helpers

**File**: `libs/analytics/constants.ts`

This shows advanced pattern with readonly array constants and type-safe helper functions.

```typescript
/**
 * Analytics constants - Single source of truth for analytics keys
 */

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

/**
 * Type-safe helper to extract only valid default analytics keys from an object
 */
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

**Key patterns demonstrated:**
- SCREAMING_SNAKE_CASE for the constant array
- `readonly (keyof DefaultAnalyticsParams)[]` ensures type safety
- `as const` makes array readonly at compile time
- Single source of truth principle explicitly documented
- Type-safe helper function uses the constant
- Generic type parameter with constraint: `T extends Partial<DefaultAnalyticsParams>`
- Runtime filtering with compile-time type safety
- Comments emphasize synchronization with type definition

## Example 7: Feature Flag Keys with Enum Organization

**File**: `libs/native-modules/feature-toggle/constants/featureFlagKeys.ts`

This demonstrates module-based feature flag organization using enums (exception to const object preference).

```typescript
// Make available the feature flag keys for the modules
type EnumValues<E extends Record<string, string>> = `${E[keyof E]}`;
export type FeatureFlagKeys =
  | EnumValues<typeof CountrySelectionModuleFeatureFlagKeys>
  | EnumValues<typeof HomeModuleFeatureFlagKeys>
  | EnumValues<typeof OnboardingModuleFeatureFlagKeys>
  | EnumValues<typeof ProfileServiceModuleFeatureFlagKeys>
  | EnumValues<typeof StoreModuleFeatureFlagKeys>
  | EnumValues<typeof ReferralsModuleFeatureFlagKeys>
  | EnumValues<typeof ProfileModuleFeatureFlagKeys>
  | EnumValues<typeof CashCreditModuleFeatureFlagKeys>
  | EnumValues<typeof LoyaltyProgramModuleFeatureFlagKeys>
  | EnumValues<typeof SustainabilityNudgesFeatureFlagKeys>;

// Define the feature flag keys per module
export enum CountrySelectionModuleFeatureFlagKeys {
  Example = 'example',
}

export enum OnboardingModuleFeatureFlagKeys {
  WELCOME_CAROUSEL_V2_FEATURE_FLAG = 'rnsm_onboarding_welcome_carousel_v2',
}

export enum ProfileServiceModuleFeatureFlagKeys {
  RTE_MEAL_PREF_EXTRACTION = 'rte_meal_pref_extraction',
  RTEA_SHORT_SHIPPING = 'rtea_short_shipping',
}

export enum HomeModuleFeatureFlagKeys {
  RTE_VMS_LAUNCH_FLAG = 'rnsm_rte_vms_flag',
}

export enum StoreModuleFeatureFlagKeys {
  RNSM_STOREFRONT_DESELECT_MEALS_CTA = 'rnsm_storefront_deselect_meals_cta',
  RNSM_SEAMLESS_BOX_DOWNGRADE = 'rn_seamless_box_downgrade',
  NEW_APP_ONBOARDING = 'new_app_onboarding',
  LOYALTY_PROGRAM_TOUCHPOINT_CART = 'loyalty_program_touchpoint_cart',
  CASH_CREDIT_IN_CART = 'topup_in_ordersummary',
}

export enum ReferralsModuleFeatureFlagKeys {
  ENABLE_FREEBIE_INTO_HELLOSHARE = 'show_one_referrals_program',
}

export enum ProfileModuleFeatureFlagKeys {
  GUEST_HOME_REVAMP = 'guest_home_revamp',
  NEW_BETA_EXPERIENCE = 'elli_113_beta_program',
}

export enum CashCreditModuleFeatureFlagKeys {
  CASH_CREDIT = 'hello_credits_migration',
}

export enum LoyaltyProgramModuleFeatureFlagKeys {
  LOYALTY_PROGRAM = 'loyalty_program',
  SMOOTHIE_BOX_CHALLENGE = 'smoothie_box_challenge',
}

export enum SustainabilityNudgesFeatureFlagKeys {
  SUSTAINABILITY_TAG = 'prod-2002-shopex-bnl-sustainability-nudges',
}
```

**Key patterns demonstrated:**
- TypeScript enums for feature flags (exception to "prefer const objects" rule)
- Module-based organization (OnboardingModuleFeatureFlagKeys, StoreModuleFeatureFlagKeys)
- SCREAMING_SNAKE_CASE for enum keys
- snake_case for string values (actual feature flag keys)
- PascalCase with "Module" suffix for enum names
- Union type FeatureFlagKeys combines all module enums
- EnumValues helper type extracts string union from enum
- Template literal type: `` `${E[keyof E]}` ``
- Why enums here: Module grouping, exhaustive checking, clear organization

## Summary

The YourCompany codebase consistently follows these constants patterns:

1. **Feature-level organization** in `constants.ts` files
2. **SCREAMING_SNAKE_CASE** for primitive constants
3. **PascalCase** for constant objects (TEST_IDS, REPOSITORY_KEYS)
4. **`as const`** for type-safe literal types
5. **Type extraction** from constants: `typeof X[keyof typeof X]`
6. **Comprehensive test IDs** grouped by logical sections
7. **Animation durations** in milliseconds
8. **Query keys** for data access centralization
9. **Enums for feature flags** (organized by module)
10. **JSDoc comments** explaining purpose and usage
11. **Design system tokens** in configuration objects
12. **Type-safe helpers** using constants for runtime validation

These patterns ensure consistent, type-safe, maintainable constant management throughout the app.
