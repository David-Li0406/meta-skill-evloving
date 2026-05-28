---
name: deep-linking
description: "WHAT: Deep linking with createModuleLinking and DeepLinkQueue for cold start handling. WHEN: configuring URL-to-screen mappings, handling universal links, parsing query parameters. KEYWORDS: deep link, createModuleLinking, DeepLinkQueue, getStateFromPath, URL, route, universal link, app link, linking."
---

# Deep Linking

## Core Principles

**Use `createModuleLinking` for all deep linking configuration.** It abstracts away complexity of handling initial URLs, event subscriptions, and cold start queueing through `DeepLinkQueue`.

**Always include `isDeepLink: true` in route params.** This flag enables screens to distinguish deeplink navigation from normal navigation, crucial for analytics and conditional behavior.

**Why**: Deep linking improves UX by allowing direct navigation to specific content. The queue-based architecture prevents race conditions during cold start when essential data (auth, plan, config) may not be loaded yet.

## When to Use This Skill

Use these patterns when:

- Configuring deep link URLs for navigation stacks
- Implementing URL-to-screen mappings with parameters
- Handling complex routing logic based on query parameters
- Preventing cold start race conditions with data loading
- Supporting universal links (iOS) or app links (Android)
- Testing deep link navigation in development
- Ensuring consistent routing across multiple stacks
- Tracking deeplink-specific analytics

## createModuleLinking Pattern

### Basic Configuration

Use `createModuleLinking` to create stack-scoped linking configurations:

```typescript
import type { LinkingOptions } from '@react-navigation/native';
import { createModuleLinking } from '@libs/deeplinking';
import { StoreStackRoutes } from '../routes';
import type { StoreStackParamsList } from '../types';

// Define screen-to-path mapping
const config: LinkingOptions<StoreStackParamsList>['config'] = {
  screens: {
    [StoreStackRoutes.Storefront]: 'store',
    [StoreStackRoutes.Upsell]: 'store',
    [StoreStackRoutes.ProductDetails]: 'store/product/:productId',
    [StoreStackRoutes.Cart]: 'store/cart',
  },
};

// Create base linking configuration
const base = createModuleLinking<StoreStackParamsList>(config);

// Export complete configuration
export const linkingConfig: LinkingOptions<StoreStackParamsList> = {
  ...base,
};
```

**Why**: `createModuleLinking` handles initial URLs, event subscriptions, and cold start queueing automatically. It integrates with `DeepLinkQueue` to prevent race conditions.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/stacks/store/linking/linkingConfig.ts:65`

### How createModuleLinking Works

The hook provides three key integrations:

```typescript
export const createModuleLinking = <T extends object>(
  config: LinkingOptions<T>['config']
): LinkingOptions<T> => {
  return {
    prefixes: [''], // Minimal prefix for React Navigation
    config,
    getInitialURL: async () => {
      const initialURL = await SharedModulesNavigation.getInitialURL();

      if (!initialURL) return null;

      // If queue is ready, process immediately
      if (deepLinkQueue.getIsReady()) {
        return initialURL;
      }

      // If queue not ready, enqueue and return null
      deepLinkQueue.enqueue(initialURL);
      return null;
    },
    subscribe: createEventSubscriber, // Handles 'url' events from native
  };
};
```

**Why**: getInitialURL blocks navigation until queue is ready, preventing screens from rendering before data loads. createEventSubscriber handles incoming deeplinks during app runtime.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/deeplinking/createModuleLinking.ts:22`

## DeepLinkQueue

### Queue Management

The `DeepLinkQueue` holds deeplinks during app initialization until essential data is loaded:

```typescript
import { deepLinkQueue } from '@libs/deeplinking';

// In your data loading logic (e.g., after auth/plan/config loaded)
const initializeApp = async () => {
  // Load essential data
  await loadAuthToken();
  await loadUserPlan();
  await loadAppConfig();

  // Mark queue as ready to process deeplinks
  deepLinkQueue.setReady();
};

// createModuleLinking automatically handles queuing if called before setReady()
```

**Why**: Without queueing, deeplinks arriving during cold start may navigate to screens before data is ready, causing errors or poor UX. The queue with 5-second failsafe prevents deadlocks.

### Queue Implementation

The queue provides enqueue/dequeue with failsafe timeout:

```typescript
class DeepLinkQueue {
  private queue: string[] = [];
  private isReady = false;
  private readonly TIMEOUT_MS = 5000; // 5 seconds failsafe

  enqueue(url: string): void {
    if (this.isReady) {
      this.executeDeepLink(url);
    } else {
      this.queue.push(url);
      if (this.queue.length === 1) {
        this.startFailsafeTimeout();
      }
    }
  }

  setReady(): void {
    if (this.isReady) return;
    this.isReady = true;

    this.clearFailsafeTimeout();

    // Execute all queued deeplinks
    while (this.queue.length > 0) {
      const url = this.queue.shift();
      if (url) this.executeDeepLink(url);
    }
  }

  private executeDeepLink(url: string): void {
    try {
      Linking.emit('url', { url });
    } catch (error) {
      console.error('[DeepLinkQueue] Error executing deeplink:', error);
    }
  }
}

export const deepLinkQueue = new DeepLinkQueue();
```

**Why**: Failsafe timeout ensures deeplinks are eventually processed even if setReady() is never called, preventing indefinite blocking.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/deeplinking/DeepLinkQueue.ts:9`

## Route Configuration

### Using Route Enums

Always use route enum constants for type safety:

```typescript
import { StoreStackRoutes } from '../routes';

// ✅ Use route enums
const config: LinkingOptions<StoreStackParamsList>['config'] = {
  screens: {
    [StoreStackRoutes.Storefront]: 'store',
    [StoreStackRoutes.ProductDetails]: 'store/product/:productId',
  },
};
```

**Why**: Route enums prevent typos, enable IDE autocomplete, and make refactoring safer when screen names change.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/stacks/store/linking/linkingConfig.ts:65`

### Path Parameters

Define URL parameters using React Navigation's path syntax:

```typescript
const config: LinkingOptions<HomeStackParamsList>['config'] = {
  screens: {
    // Home screens
    [HomeStackRoutes.Homefront]: '',

    // Store screens with parameters
    [StoreStackRoutes.ProductDetails]: 'store/product/:productId',
    [StoreStackRoutes.Cart]: 'store/cart',
    [StoreStackRoutes.Promotion]: 'store/promotion/:promotionId',
  },
};

// URLs match:
// store/product/123 -> ProductDetails with { productId: '123' }
// store/cart -> Cart screen
// store/promotion/abc -> Promotion with { promotionId: 'abc' }
```

**Why**: Path parameters enable dynamic routing and are automatically parsed by React Navigation.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/home/stacks/home/linking/linkingConfig.ts:66`

### Multiple Screens Same Path

When multiple screens share a path, use `getStateFromPath` to determine routing:

```typescript
const config: LinkingOptions<StoreStackParamsList>['config'] = {
  screens: {
    // Both Storefront and Upsell use same path 'store'
    // Routing logic in getStateFromPath determines which screen
    [StoreStackRoutes.Storefront]: 'store',
    [StoreStackRoutes.Upsell]: 'store',
  },
};
```

**Why**: Single path can route to different screens based on query parameters or other conditions, enabling sophisticated routing logic.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/stacks/store/linking/linkingConfig.ts:65`

## Query Parameter Parsing

### Custom getStateFromPath

Implement `getStateFromPath` for complex routing logic based on query parameters:

```typescript
import { parseStoreQueryParams } from './helpers';
import { StoreCategoryTypes, STORE_PATH_NAME } from './constants';

const getStateFromPath: NonNullable<
  LinkingOptions<StoreStackParamsList>['getStateFromPath']
> = (path) => {
  const [pathname, queryString] = path.split('?');

  // Only handle store paths
  if (pathname !== STORE_PATH_NAME) {
    return {
      routes: [
        {
          name: StoreStackRoutes.Storefront,
          params: { isDeepLink: true },
        },
      ],
    };
  }

  // Parse query parameters
  const { week, category, subcategory } = parseStoreQueryParams(queryString);

  // Route to different screens based on category
  if (category === StoreCategoryTypes.Market) {
    return {
      routes: [
        {
          name: StoreStackRoutes.Upsell,
          params: {
            weekId: week,
            preSelectedSubcategory: subcategory,
            isDeepLink: true,
          },
        },
      ],
    };
  }

  // Default routing
  return {
    routes: [
      {
        name: StoreStackRoutes.Storefront,
        params: {
          categoryId: category,
          selectedWeek: week,
          isDeepLink: true,
        },
      },
    ],
  };
};

// Add to linking config
export const linkingConfig: LinkingOptions<StoreStackParamsList> = {
  ...base,
  getStateFromPath,
};
```

**Why**: `getStateFromPath` enables sophisticated routing where the same path navigates to different screens based on query parameters or other conditions.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/stacks/store/linking/linkingConfig.ts:78`

### Query Parameter Helper

Extract query parameter parsing into reusable helpers:

```typescript
// helpers.ts
export const parseStoreQueryParams = (
  queryString?: string
): ParsedStoreQueryParams => {
  const searchParams = new URLSearchParams(queryString ?? '');

  const voucherAppliedParam = searchParams.get('voucherApplied');
  let voucherApplied: boolean | undefined;
  if (voucherAppliedParam) {
    voucherApplied = voucherAppliedParam === 'true';
  }

  return {
    week: searchParams.get('week') ?? undefined,
    category: searchParams.get('category') ?? 'dinners',
    subcategory: searchParams.get('subcategory') ?? undefined,
    voucherApplied,
    voucherMessage: searchParams.get('voucherMessage') ?? undefined,
  };
};
```

**Why**: Centralized parsing logic makes query parameter handling testable and reusable across multiple stacks.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/stacks/store/linking/helpers.ts:10`

## Integration with NavigationContainer

### NavigationEntryProvider

Use `NavigationEntryProvider` to wrap stacks with linking configuration:

```typescript
import { NavigationEntryProvider } from '@entry-providers';
import { linkingConfig } from './linking/linkingConfig';
import { StoreStack } from './StoreStack';

export const StoreStackWithProviders = () => (
  <NavigationEntryProvider linking={linkingConfig}>
    <StoreStack />
  </NavigationEntryProvider>
);
```

**Why**: `NavigationEntryProvider` wraps `NavigationContainer` and provides essential context (query client, localization, theme) while enabling deep linking.

### With Repository Loading

For stacks requiring data before navigation, use `requiredRepositories`:

```typescript
import { NavigationEntryProvider } from '@entry-providers';
import { REPOSITORY_KEYS } from '@data-access/native/constants';
import { linkingConfig } from './linking/linkingConfig';

export const HomeStackWithProviders = () => (
  <NavigationEntryProvider
    linking={linkingConfig}
    requiredRepositories={{
      [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
      [REPOSITORY_KEYS.plan]: ['planId'],
    }}
  >
    <HomeStack />
  </NavigationEntryProvider>
);
```

**Why**: Repository loading ensures critical data is available before screens render, preventing errors from missing data. Works with `DeepLinkQueue` to delay deeplink processing until ready.

## Handling Multiple Stacks

### Shared Path Resolution

When multiple stacks handle the same paths, use identical routing logic:

```typescript
// HomeStack and StoreStack both handle 'store' paths
// Both use the same getStateFromPath logic

// home/stacks/home/linking/linkingConfig.ts
const getStateFromPath: NonNullable<
  LinkingOptions<HomeStackParamsList>['getStateFromPath']
> = (path) => {
  const [pathname, queryString] = path.split('?');

  // Handle store paths (HomeStack includes store screens)
  if (pathname === 'store') {
    const { week, category, subcategory } = parseStoreQueryParams(queryString);

    // Same routing logic as StoreStack
    if (category === StoreCategoryTypes.Market) {
      return {
        routes: [
          {
            name: StoreStackRoutes.Upsell,
            params: { weekId: week, preSelectedSubcategory: subcategory, isDeepLink: true },
          },
        ],
      };
    }

    return {
      routes: [
        {
          name: StoreStackRoutes.Storefront,
          params: { categoryId: category, selectedWeek: week, isDeepLink: true },
        },
      ],
    };
  }

  // Handle home-specific paths
  // ...
};
```

**Why**: Consistent routing logic prevents conflicts when the same deeplink could be handled by different stacks depending on app state.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/home/stacks/home/linking/linkingConfig.ts:93`

### Nested Stacks with Parameters

Handle nested navigation with route arrays:

```typescript
const getStateFromPath: NonNullable<
  LinkingOptions<SocialRecipeBridgeStackParamsList>['getStateFromPath']
> = (path) => {
  const [pathname = ''] = path.split('?');

  // Handle recipe detail path
  const recipeDetailMatch = pathname.match(
    new RegExp(`^cookbook/recipe/(.+)$`)
  );
  if (recipeDetailMatch) {
    const recipeId = recipeDetailMatch[1];
    return {
      routes: [
        {
          name: SocialRecipeBridgeStackRoutes.SocialRecipeBridge,
          params: { isDeepLink: true },
        },
        {
          name: SocialRecipeBridgeStackRoutes.RecipeDetail,
          params: { recipeId, isDeepLink: true },
        },
      ],
    };
  }

  return undefined; // Block unrecognized paths
};
```

**Why**: Route arrays enable navigation to nested screens directly from deeplinks, maintaining correct navigation stack history.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/stacks/social-recipe-bridge/linking/linkingConfig.ts:17`

## Testing Deep Links

### Development Testing

Test deeplinks during development using platform-specific commands:

```bash
# iOS Simulator
xcrun simctl openurl booted "com.yourcompany.app://store?week=2025-W42&category=market"

# Android Emulator
adb shell am start -W -a android.intent.action.VIEW \
  -d "com.yourcompany.app://store?week=2025-W42&category=market" com.yourcompany.app
```

**Why**: Command-line testing verifies deeplink handling without external dependencies.

### Unit Testing

Test custom routing logic in isolation:

```typescript
import { linkingConfig } from './linkingConfig';
import { StoreStackRoutes } from '../routes';

describe('linkingConfig', () => {
  it('routes market category to Upsell screen', () => {
    const state = linkingConfig.getStateFromPath?.(
      'store?week=2025-W42&category=market'
    );

    expect(state?.routes[0].name).toBe(StoreStackRoutes.Upsell);
    expect(state?.routes[0].params).toEqual({
      weekId: '2025-W42',
      preSelectedSubcategory: undefined,
      isDeepLink: true,
      voucherApplied: undefined,
      voucherMessage: undefined,
    });
  });

  it('routes other categories to Storefront', () => {
    const state = linkingConfig.getStateFromPath?.(
      'store?week=2025-W42&category=dinners'
    );

    expect(state?.routes[0].name).toBe(StoreStackRoutes.Storefront);
    expect(state?.routes[0].params).toEqual({
      categoryId: 'dinners',
      selectedWeek: '2025-W42',
      isDeepLink: true,
      voucherApplied: undefined,
      voucherMessage: undefined,
    });
  });
});
```

**Why**: Unit tests ensure routing logic works correctly and prevent regressions when modifying deeplink handling.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/stacks/store/linking/linkingConfig.test.ts:33`

## Common Mistakes to Avoid

❌ **Don't use React Native Linking directly**:

```typescript
// ❌ Wrong - Missing queue handling and native integration
import { Linking } from 'react-native';

useEffect(() => {
  Linking.getInitialURL().then(/* ... */);
  Linking.addEventListener('url', /* ... */);
}, []);
```

✅ **Do use createModuleLinking**:

```typescript
// ✅ Correct - Handles cold start queueing automatically
import { createModuleLinking } from '@libs/deeplinking';

const base = createModuleLinking<StackParamsList>(config);
export const linkingConfig = { ...base };
```

❌ **Don't forget isDeepLink flag**:

```typescript
// ❌ Wrong - Missing isDeepLink flag
return {
  routes: [
    {
      name: StoreStackRoutes.Storefront,
      params: { categoryId: category }, // Missing isDeepLink
    },
  ],
};
```

✅ **Do include isDeepLink for analytics**:

```typescript
// ✅ Correct - Enables deeplink-specific tracking
return {
  routes: [
    {
      name: StoreStackRoutes.Storefront,
      params: {
        categoryId: category,
        isDeepLink: true, // Enables deeplink-specific tracking
      },
    },
  ],
};
```

❌ **Don't assume paths are always valid**:

```typescript
// ❌ Wrong - No fallback for invalid paths
const getStateFromPath = (path: string) => {
  const [pathname, queryString] = path.split('?');
  const { category } = parseStoreQueryParams(queryString);
  // May crash if category is required but undefined
  navigation.navigate(getCategoryScreen(category));
};
```

✅ **Do provide fallback for invalid paths**:

```typescript
// ✅ Correct - Graceful fallback
const getStateFromPath = (path: string) => {
  const [pathname, queryString] = path.split('?');

  if (pathname !== 'store') {
    // Fallback to default screen
    return {
      routes: [
        { name: StoreStackRoutes.Storefront, params: { isDeepLink: true } }
      ],
    };
  }

  const { category } = parseStoreQueryParams(queryString);
  // Handle missing or invalid category gracefully
  // ...
};
```

❌ **Don't use hardcoded strings for routes**:

```typescript
// ❌ Wrong - No type safety
const config = {
  screens: {
    Storefront: 'store', // Typos not caught at compile time
  },
};
```

✅ **Do use route enums**:

```typescript
// ✅ Correct - Type-safe, refactorable
import { StoreStackRoutes } from '../routes';

const config: LinkingOptions<StoreStackParamsList>['config'] = {
  screens: {
    [StoreStackRoutes.Storefront]: 'store',
  },
};
```

## Quick Reference

**Basic linking config:**
```typescript
const config: LinkingOptions<StackParamsList>['config'] = {
  screens: {
    [StackRoutes.Home]: '',
    [StackRoutes.Details]: 'details/:id',
  },
};

const base = createModuleLinking<StackParamsList>(config);
export const linkingConfig = { ...base };
```

**Query parameter parsing:**
```typescript
const getStateFromPath: NonNullable<
  LinkingOptions<StackParamsList>['getStateFromPath']
> = (path) => {
  const [pathname, queryString] = path.split('?');
  const params = parseQueryParams(queryString);

  return {
    routes: [
      {
        name: StackRoutes.Screen,
        params: { ...params, isDeepLink: true },
      },
    ],
  };
};
```

**Initialize queue:**
```typescript
import { deepLinkQueue } from '@libs/deeplinking';

const initializeApp = async () => {
  await loadEssentialData();
  deepLinkQueue.setReady();
};
```

**NavigationEntryProvider:**
```typescript
<NavigationEntryProvider linking={linkingConfig}>
  <Stack />
</NavigationEntryProvider>
```

**Test deeplinks:**
```bash
# iOS
xcrun simctl openurl booted "app://path?param=value"

# Android
adb shell am start -W -a android.intent.action.VIEW \
  -d "app://path?param=value" com.package.name
```

**Key Libraries:**
- React Navigation 7.0.13
- React Native 0.75.4
- TypeScript 5.1.6

For production examples, see [references/examples.md](references/examples.md).
