# File Organization Examples

Real-world examples from the YourCompany shared-mobile-modules project showing the 6-tier architecture.

## Repository Structure

Top-level structure from `src/`:

```
src/
├── entry-providers/       # Tier 1: Entry providers and registration
├── modules/               # Tier 2: Domain-specific modules
├── features/              # Tier 3: Reusable UI components
├── operations/            # Tier 4: Business logic without UI
├── data-access/           # Tier 5: API layer
│   ├── graphql/           # GraphQL queries and mutations
│   ├── native/            # Native module data access
│   ├── query/             # TanStack Query definitions
│   └── maestro/           # Maestro test data
├── libs/                  # Tier 6: Infrastructure utilities
├── navigation/            # Navigation configuration (lib level)
├── assets/                # Static assets (images, fonts)
├── types/                 # Shared TypeScript types
├── __mocks__/             # Test mocks
├── __tests__/             # Shared tests
└── legacy/                # Legacy code (to be refactored)
```

## Tier 1: Entry Providers

From `src/entry-providers/providers.tsx`:

```typescript
import type { PropsWithChildren } from 'react';
import { QueryClientProvider } from '@tanstack/react-query';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { Toast } from '@features/toast-feature';
import { ErrorBoundary } from '@libs/error-boundary';
import { AppWithTranslation } from '@libs/localization';
import { queryClient } from '@libs/query';
import { RepositoryLoader } from '@libs/repository-loader';
import { ZestProvider } from '@libs/zest';

/**
 * Global manager that handles loyalty state changes and invalidates caches.
 * This ensures that when loyalty program state changes, all related data is refreshed.
 */
const GlobalLoyaltyStateManager: React.FC = () => {
  useLoyaltyStateManager();
  return null;
};

/**
 * @description
 * `NavigationEntryProvider` is a higher-order component designed to wrap a navigation stack.
 * It provides the necessary context for navigation and deep linking within the app.
 * Now supports optional repository loading to ensure critical data is available before rendering.
 *
 * This provider is typically used when creating a module that contains multiple screens.
 * All Screens within the stack are wrapped around the `ScreenEntryProvider` to ensure
 * proper services are available.
 */
export const NavigationEntryProvider = <StackType extends object>({
  children,
  linking,
  requiredRepositories,
  repositoryLoadingFallback,
}: NavigationEntryProviderProps<StackType>) => (
  <ScreenEntryProvider>
    <NavigationContainer linking={linking}>
      {requiredRepositories && Object.keys(requiredRepositories).length > 0 ? (
        <RepositoryLoader
          requiredRepositories={requiredRepositories}
          loadingFallback={repositoryLoadingFallback}
        >
          {children}
          <Toast />
        </RepositoryLoader>
      ) : (
        <>
          {children}
          <Toast />
        </>
      )}
    </NavigationContainer>
  </ScreenEntryProvider>
);

/**
 * Screen-level entry provider that wraps all screens with necessary infrastructure.
 */
export const ScreenEntryProvider: React.FC<PropsWithChildren> = ({
  children,
}) => {
  return (
    <QueryClientProvider client={queryClient}>
      <SafeAreaProvider>
        <AppWithTranslation>
          <ZestProvider>
            <ErrorBoundary scope={{ moduleName: 'App' }}>
              <GlobalLoyaltyStateManager />
              {children}
            </ErrorBoundary>
          </ZestProvider>
        </AppWithTranslation>
      </SafeAreaProvider>
    </QueryClientProvider>
  );
};
```

**Provider hierarchy:**
1. QueryClientProvider - TanStack Query caching
2. SafeAreaProvider - Safe area handling
3. AppWithTranslation - Localization
4. ZestProvider - Design system components
5. ErrorBoundary - Error handling
6. GlobalLoyaltyStateManager - State synchronization

**Why this order:** Each provider depends on the one above it, ensuring dependencies are initialized in the correct sequence.

## Tier 2: Modules

Module structure example from `src/modules/`:

```
modules/
├── active-journey/
│   ├── .claim.json              # {"team": "active-journey-alliance-react-native"}
│   ├── index.ts
│   └── screens/
├── home/
│   ├── .claim.json
│   ├── index.ts
│   ├── screens/
│   └── stacks/
├── onboarding/
│   ├── .claim.json
│   ├── index.ts
│   └── screens/
└── social-recipe-bridge/
    ├── .claim.json              # {"team": "team-social-recipes"}
    ├── index.ts
    ├── README.md
    ├── screens/
    │   ├── cookbook-faq/
    │   ├── onboarding/
    │   └── add-recipe-link-drawer/
    └── hooks/
```

**Module ownership examples:**

```json
// src/modules/active-journey/.claim.json
{
  "team": "active-journey-alliance-react-native"
}
```

```json
// src/modules/rte-programs/.claim.json
{
  "team": "rte-programs"
}
```

```json
// src/modules/rte-vms/.claim.json
{
  "team": "rte-vms"
}
```

## Tier 3: Features

Feature directory structure from `src/features/`:

```
features/
├── addons-carousels/
│   ├── .claim.json
│   ├── index.ts
│   ├── AddonsCarousels.tsx
│   └── components/
├── reactivation-banner-feature/
│   ├── .claim.json
│   ├── index.ts
│   ├── README.md
│   ├── ReactivationBanner.tsx
│   ├── components/
│   │   ├── discount-applied-pill/
│   │   ├── meal-plan/
│   │   └── promo-code-cta/
│   ├── hooks/
│   │   └── useReactivationBannerAnimation.ts
│   └── state-management/
├── recipe-image/
│   ├── index.ts
│   └── RecipeImage.tsx
├── toast-feature/
│   ├── .claim.json
│   ├── README.md
│   ├── index.ts
│   └── Toast.tsx
└── webview/
    ├── .claim.json
    ├── README.md
    ├── index.ts
    └── Webview.tsx
```

**Feature with variants:**

```
features/reactivation-banner-feature/
├── index.ts
├── ReactivationBanner.tsx            # Main container
├── ReactivationBannerExpanded.tsx    # Expanded variant
├── ReactivationBannerCollapsed.tsx   # Collapsed variant
├── components/                        # Shared sub-components
│   ├── discount-applied-pill/
│   ├── meal-plan/
│   └── promo-code-cta/
└── hooks/
    └── useReactivationBannerAnimation.ts
```

**Why variants:** Different visual states (expanded/collapsed) are organized as separate components within the same feature, maintaining cohesion.

## Tier 4: Operations

Operations directory structure from `src/operations/`:

```
operations/
├── analytics/
│   ├── .claim.json
│   ├── index.ts
│   └── useAnalytics.ts
├── favorite-product/
│   ├── .claim.json
│   ├── index.ts
│   └── useFavoriteProduct.ts
├── meal-selection/
│   ├── .claim.json
│   ├── index.ts
│   ├── mutations/
│   │   ├── onAddProduct.ts
│   │   └── onRemoveProduct.ts
│   ├── selectors.ts
│   └── utils.ts
└── subscription-management/
    ├── .claim.json
    ├── index.ts
    └── useSubscriptionStatus.ts
```

**Operation example from data access patterns:**

```typescript
// src/operations/auth/useSignIn.ts
import { useMutation } from '@tanstack/react-query';
import { signIn } from '@data-access/native/auth';
import { usePerformanceTracker } from '@libs/observability';
import type { SignInData } from './types';

export const useSignIn = () => {
  const { startTrace, stopTrace } = usePerformanceTracker('SignIn');

  return useMutation({
    mutationFn: (data: SignInData) => signIn(data),
    onMutate: () => startTrace(),
    onSettled: () => stopTrace(),
  });
};
```

**Pattern:** Operation wraps data access call with additional concerns (performance tracking) without mixing UI.

## Tier 5: Data Access

Data access directory structure from `src/data-access/`:

```
data-access/
├── .claim.json                  # {"team": "mobile-foundation"}
├── graphql/
│   ├── __generated__/           # Generated types
│   ├── queries/
│   │   ├── getUser.graphql
│   │   └── getRecipes.graphql
│   ├── mutations/
│   │   └── updateProfile.graphql
│   └── fragments/
├── native/
│   ├── repositories/
│   │   ├── AppConfigRepository.ts
│   │   └── UserRepository.ts
│   └── index.ts
├── query/
│   ├── customer/
│   │   └── subscriptions/
│   ├── external-recipes/
│   │   ├── types.ts
│   │   └── useGetExternalRecipes.ts
│   ├── menu/
│   │   └── schema/
│   └── payments/
│       └── customer-balance/
└── maestro/
    └── mockData.ts
```

**TanStack Query hook example:**

From `src/data-access/query/payments/customer-balance/customerBalance.ts`:

```typescript
import { useFetch } from '@data-access/query/hooks/useFetch';

const getCustomerBalance = async (
  { systemCountry, locale, customerUUID },
  queryKey,
  fetch
) => {
  const response = await fetch(
    `/payments/customers/${customerUUID}/balance`,
    queryKey,
    {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      query: { country: systemCountry, locale },
    }
  );

  if (!response.ok) {
    throw new Error(`Customer balance request failed with status ${response.status}`);
  }

  return await response.json();
};

export const useCustomerBalance = (
  { systemCountry, locale, customerUUID },
  options = {}
) => {
  const fetch = useFetch();
  const queryKey = ['customer-balance', systemCountry, locale, customerUUID];

  return useQuery({
    queryKey,
    queryFn: () => getCustomerBalance({ systemCountry, locale, customerUUID }, queryKey, fetch),
    ...options,
  });
};
```

**Pattern:** Data access layer uses TanStack Query for REST APIs with proper query keys and error handling.

## Tier 6: Libs

Libs directory structure from `src/libs/`:

```
libs/
├── analytics/
│   ├── .claim.json              # {"team": "mobile-foundation"}
│   ├── index.ts
│   └── Analytics.ts
├── cache/
│   ├── index.ts
│   └── QueryCacheManager.ts
├── error-boundary/
│   ├── index.ts
│   └── ErrorBoundary.tsx
├── localization/
│   ├── index.ts
│   └── AppWithTranslation.tsx
├── loyalty-state-manager/
│   ├── index.ts
│   └── useLoyaltyStateManager.ts
├── native-modules/
│   ├── events/
│   ├── performanceTracker/
│   └── repositories/
├── observability/
│   ├── index.ts
│   └── usePerformanceTracker.ts
├── query/
│   ├── index.ts
│   └── queryClient.ts
├── repository-loader/
│   ├── index.ts
│   └── RepositoryLoader.tsx
└── zest/
    ├── index.ts
    └── ZestProvider.tsx
```

**All libs owned by mobile-foundation team.**

## Path Aliases in Action

From actual import patterns in the codebase:

```typescript
// Entry provider importing from libs
import { ErrorBoundary } from '@libs/error-boundary';
import { AppWithTranslation } from '@libs/localization';
import { queryClient } from '@libs/query';
import { ZestProvider } from '@libs/zest';

// Feature importing from operations and libs
import { useSignIn } from '@operations/auth';
import { Button, Input } from '@zest/react-native';

// Operation importing from data access and libs
import { signIn } from '@data-access/native/auth';
import { usePerformanceTracker } from '@libs/observability';

// Module importing from features
import { AuthForm } from '@features/auth-form';
import { Toast } from '@features/toast-feature';
```

**Pattern:** Clean import paths using configured aliases, no deep relative paths like `../../../`.

## Barrel Exports

From `src/entry-providers/index.ts`:

```typescript
export * from './providers';
export * from './registers';
export type * from './types';
```

From `src/features/reactivation-banner-feature/index.ts`:

```typescript
export { ReactivationBanner } from './ReactivationBanner';
export { ReactivationBannerExpanded } from './ReactivationBannerExpanded';
export { ReactivationBannerCollapsed } from './ReactivationBannerCollapsed';
export type { ReactivationBannerProps } from './types';
```

**Pattern:** Each directory has an index.ts that exports its public API, hiding internal structure.

## Testing Structure

Co-located tests from the codebase:

```
features/reactivation-banner-feature/
├── ReactivationBanner.tsx
├── ReactivationBanner.test.tsx          # Co-located
├── components/
│   ├── meal-plan/
│   │   ├── MealPlan.tsx
│   │   └── MealPlan.test.tsx            # Co-located
│   ├── promo-code-input/
│   │   ├── PromoCodeInput.tsx
│   │   └── PromoCodeInput.test.tsx      # Co-located
│   └── promo-code-modal/
│       ├── PromoCodeModal.tsx
│       └── PromoCodeModal.test.tsx      # Co-located
└── hooks/
    ├── useReactivationBannerAnimation.ts
    └── useReactivationBannerAnimation.test.ts  # Co-located
```

**Pattern:** Test files are co-located with source files, making them easy to find and maintain.

## README Structure

From `src/features/reactivation-banner-feature/README.md`:

```markdown
# Reactivation Banner Feature

The Reactivation Banner is a UI component that appears at the top of the home screen when a user's subscription is inactive.

## Overview

The banner has two distinct visual states that transition smoothly based on scroll position:

1. **Expanded** – Comprehensive reactivation information
2. **Collapsed** – Compact version

## Components Structure

```
reactivation-banner-feature/
├── components/
├── hooks/
├── styles/
└── constants.ts
```

## Usage

```tsx
<ReactivationBanner
  scrollY={scrollY}
  onMaxHeightChange={setBannerHeight}
/>
```

## Key Components

### ReactivationBanner
Main container component...

### ReactivationBannerExpanded
Expanded version...

## Animation Behavior

Animation between states is managed by...

## Testing

Tests included:
- ReactivationBanner.test.tsx
- Component-specific tests
```

**Pattern:** README files provide high-level feature overview, usage examples, and architecture explanation.

## Naming Conventions in Practice

From actual codebase structure:

**Folders (kebab-case):**
- ✅ `social-recipe-bridge/`
- ✅ `reactivation-banner-feature/`
- ✅ `error-boundary/`
- ✅ `loyalty-state-manager/`

**Component files (PascalCase):**
- ✅ `ReactivationBanner.tsx`
- ✅ `ErrorBoundary.tsx`
- ✅ `QueryCacheManager.ts`

**Hook files (camelCase with "use"):**
- ✅ `useReactivationBannerAnimation.ts`
- ✅ `useLoyaltyStateManager.ts`
- ✅ `usePerformanceTracker.ts`

**Utility files (lowercase/camelCase):**
- ✅ `constants.ts`
- ✅ `types.ts`
- ✅ `styles.ts`
- ✅ `index.ts`
