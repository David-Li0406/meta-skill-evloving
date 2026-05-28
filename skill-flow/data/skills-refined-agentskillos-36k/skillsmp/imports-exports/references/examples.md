# Import and Export Examples

Real-world import and export examples from the YourCompany shared-mobile-modules project.

## Screen Component with Full Import Organization

From `src/modules/home/screens/rte-home/index.tsx`:

```typescript
// Group 1: React/React Native
import { useEffect, useRef, useState } from 'react';
import { View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

// Group 2: Data access layer
import { isSubscriptionCancelled as selectIsSubscriptionCancelled } from '@data-access/query/customer';

// Group 3: Features (alphabetized)
import { FactorFormEntrypoint } from '@features/factor-form-entrypoint';
import {
  useReactivationEligibility,
  ReactivationBannerFeature,
  ReactivationBannerProvider,
  useReactivationHomeScreenStyle,
  GlobalReactivationButtonWithContext,
} from '@features/reactivation-banner-feature';
import { TopBar } from '@features/top-bar';

// Group 4: Libs (alphabetized)
import { useT9n } from '@libs/localization';
import { DefaultScreenProvider } from '@libs/tracing';

// Group 5: Module imports (same module, different paths)
import { DeliveriesFeed } from '@modules/home/screens/rte-home/components/deliveries-feed/DeliveriesFeed';
import { HomeSkeletonLoader } from '@modules/home/screens/rte-home/components/home-skeleton-loader';
import { PersonalGreeting } from '@modules/home/screens/rte-home/components/personal-greeting/PersonalGreeting';
import { useDeliveryUpdatedListener } from '@modules/home/screens/rte-home/hooks/useDeliveryUpdatedListener';
import { useRTEHomeRepository } from '@modules/home/screens/rte-home/hooks/useRTEHomeRepository';
import type { HomefrontScreenProps } from '@modules/home/screens/types';

// Group 6: Operations
import { AnalyticsWrapper } from '@operations/analytics/AnalyticsWrapper';
import { SCREEN_NAME } from '@operations/analytics/types';
import { useFactorFormExperience } from '@operations/factor-form/feature-flags/useFactorFormExperience';

// Group 7: Zest design system
import { useZestStyles } from '@zest/react-native';

// Group 8: Sibling imports
import { useRTEHomeAnalytics } from './analytics';
import { stylesConfig } from './styles';

export const RTEHome = ({ route }: HomefrontScreenProps) => {
  // Component implementation
  const [activeTabIndex, setActiveTabIndex] = useState(0);
  const { deliveries, subscriptions, upcomingMenu, isLoadingRteHome } =
    useRTEHomeRepository();

  // ... rest of implementation
};
```

**Key patterns demonstrated:**
- React hooks imported together from 'react'
- React Native components grouped on one line
- Internal aliases grouped by tier (@data-access, @features, @libs, @modules, @operations, @zest)
- Within each tier, imports are alphabetized
- Type imports (`type { HomefrontScreenProps }`) appear with related imports
- Local/sibling imports at the end
- Blank lines between groups for readability

## Barrel Export Patterns

### Module Stack Export

From `src/modules/home/stacks/home/index.ts`:

```typescript
import { registerStack, withNavigationEntryProvider } from '@entry-providers';

import { REPOSITORY_KEYS } from '@data-access/native/constants';

import { Spinner } from '@zest/react-native';

import { HomeStack } from './HomeStack';
import { linkingConfig } from './linking/linkingConfig';
import type {
  HomeStackParamsList,
  IHomeStackProps,
  HomeStackNavigationProp,
  RTEShoppingRouteParams,
} from './types';

// Named exports for stack routes and components
export { HomeStackRoutes } from './routes';
export {
  HomeStack,
  HomeStackParamsList,
  HomeStackNavigationProp,
  IHomeStackProps,
  RTEShoppingRouteParams,
};

// Register stack with navigation system
registerStack(
  'Home',
  withNavigationEntryProvider(
    HomeStack,
    linkingConfig,
    {
      [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
    },
    Spinner
  )
);
```

**Pattern:** Import dependencies at top, export public API, then execute side effects (registration).

### Simple Barrel Export

From `src/modules/home/stacks/index.ts`:

```typescript
export * from './home';
```

**Pattern:** Re-export everything from subdirectories for clean imports.

### Component Barrel Export

From `src/modules/home/screens/rte-home/components/home-skeleton-loader/index.ts`:

```typescript
export { HomeSkeletonLoader } from './HomeSkeletonLoader';
export type { HomeSkeletonLoaderProps } from './type';
```

**Pattern:** Export component and its props type separately, using named exports.

## Entry Provider Imports

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

export const ScreenEntryProvider: React.FC<PropsWithChildren> = ({
  children,
}) => {
  return (
    <QueryClientProvider client={queryClient}>
      <SafeAreaProvider>
        <AppWithTranslation>
          <ZestProvider>
            <ErrorBoundary scope={{ moduleName: 'App' }}>
              {children}
            </ErrorBoundary>
          </ZestProvider>
        </AppWithTranslation>
      </SafeAreaProvider>
    </QueryClientProvider>
  );
};
```

**Key patterns:**
- Inline type import: `type { PropsWithChildren }`
- External libraries (QueryClientProvider, SafeAreaProvider) grouped
- Features imported before libs
- Libs alphabetized (@libs/error-boundary before @libs/localization)

## Data Access Layer Imports

From `src/data-access/query/payments/customer-balance/customerBalance.ts`:

```typescript
import { useQuery } from '@tanstack/react-query';

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

**Pattern:** External library first (TanStack Query), then internal data-access imports.

## Feature Component Imports

From `src/features/reactivation-banner-feature/`:

```typescript
import { useEffect, useState } from 'react';
import { View, Animated } from 'react-native';

import { useT9n } from '@libs/localization';

import { useZestStyles } from '@zest/react-native';

import { ReactivationBannerExpanded } from './ReactivationBannerExpanded';
import { ReactivationBannerCollapsed } from './ReactivationBannerCollapsed';
import { useReactivationBannerAnimation } from './hooks/useReactivationBannerAnimation';
import { stylesConfig } from './styles';
import type { ReactivationBannerProps } from './types';

export const ReactivationBanner = ({
  scrollY,
  onMaxHeightChange,
}: ReactivationBannerProps) => {
  // Component implementation
  const styles = useZestStyles(stylesConfig);
  const { translateRaw } = useT9n('reactivation-banner');

  // ... rest of implementation
};
```

**Pattern:** React first, libs, zest, then local imports (components, hooks, styles, types).

## Type-Only Imports

Examples from codebase:

```typescript
// Inline type imports
import { View, type ImageStyle, type ViewStyle } from 'react-native';
import { useQuery, type UseQueryOptions } from '@tanstack/react-query';

// Dedicated type imports
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import type { User, Subscription } from '@data-access/graphql';
import type { HomefrontScreenProps } from '@modules/home/screens/types';

// Mixed: both value and type imports from same source
import { useNavigation } from '@libs/navigation';
import type { NavigationProp } from '@libs/navigation/types';
```

**Patterns:**
- Use inline `type {}` when importing few types with values
- Use dedicated `import type` for type-only imports
- Group related imports even when mixing value and type imports

## Re-export Patterns

### Re-export All

```typescript
// src/modules/social-recipe-bridge/index.ts
export * from './stacks';
export * from './screens';
export * from './hooks';
export * from './stores';
export type * from './types';
```

**Pattern:** `export *` for re-exporting everything, `export type *` for types only.

### Re-export Specific

```typescript
// src/features/product-card-feature/index.ts
export { ProductCard } from './ProductCard';
export { LoadingProductCard } from './variants/loading';
export type { ProductCardProps, ProductVariant } from './types';
```

**Pattern:** Selective re-exports create a curated public API.

### Re-export with Alias

```typescript
import { isSubscriptionCancelled as selectIsSubscriptionCancelled } from '@data-access/query/customer';

// Usage
const isSubscriptionCancelled = selectIsSubscriptionCancelled(subscriptions);
```

**Pattern:** Rename imports to clarify purpose or avoid naming conflicts.

## Plop Generator Insertion Points

From `src/modules/social-recipe-bridge/screens/index.ts`:

```typescript
export * from './cookbook-faq';
export * from './onboarding';
export * from './add-recipe-link-drawer';
// @PLOP_INSERT_SCREEN_EXPORT
```

**Pattern:** Plop generator inserts new exports at the marked insertion point, maintaining consistent ordering.

## Multi-line Import Grouping

From various files:

```typescript
// React hooks grouped
import { useState, useEffect, useMemo, useCallback, useRef } from 'react';

// React Native components grouped
import { View, ScrollView, TouchableOpacity, FlatList, Image } from 'react-native';

// Zest components grouped
import { Button, Text, Input, Card, useZestStyles } from '@zest/react-native';

// Feature imports grouped from same source
import {
  useReactivationEligibility,
  ReactivationBannerFeature,
  ReactivationBannerProvider,
  useReactivationHomeScreenStyle,
  GlobalReactivationButtonWithContext,
} from '@features/reactivation-banner-feature';
```

**Pattern:** Group related imports from the same package, use multi-line format for 4+ imports.

## Operations Layer Imports

From operations files:

```typescript
import { useMutation } from '@tanstack/react-query';

import { addMeal, removeMeal } from '@data-access/query/meals';

import { useAnalytics } from '@libs/analytics';

export const useMealSelection = () => {
  const { track } = useAnalytics();

  const add = useMutation({
    mutationFn: addMeal,
    onSuccess: (data) => {
      track('Meal_Added', { mealId: data.id });
    },
  });

  return { add };
};
```

**Pattern:** External library, data-access layer, libs, then implementation.

## Path Alias Usage

Examples of all path aliases:

```typescript
// Assets
import logo from '@assets/images/logo.png';

// Data Access
import { useGetRecipes } from '@data-access/query/recipes';
import { gql } from '@data-access/graphql';

// Entry Providers
import { registerScreen, ScreenEntryProvider } from '@entry-providers';

// Features
import { ProductCard } from '@features/product-card-feature';
import { AuthForm } from '@features/auth-form';

// Libs
import { useT9n } from '@libs/localization';
import { useNavigation } from '@libs/navigation';
import { useAnalytics } from '@libs/analytics';

// Modules
import { HomeStack } from '@modules/home/stacks/home';

// Navigation
import { navigationRef } from '@navigation/root';

// Operations
import { useMealSelection } from '@operations/meal-selection';

// Types
import type { AppConfig } from '@types/config';

// Zest
import { Button, Text } from '@zest/react-native';
```

**Pattern:** Path aliases provide consistent, stable import paths across the codebase.
