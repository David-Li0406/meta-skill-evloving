# Deep Linking - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating deep linking patterns.

## Example 1: Basic Linking Configuration with createModuleLinking

**File**: `modules/store/stacks/store/linking/linkingConfig.ts:65`

This example shows basic linking configuration for the Store stack.

```typescript
import type { LinkingOptions } from '@react-navigation/native';
import { createModuleLinking } from '@libs/deeplinking';
import { StoreStackRoutes } from '../routes';
import type { StoreStackParamsList } from '../types';
import { STORE_PATH_NAME } from './constants';

/**
 * React Navigation screen configuration with parameter parsing
 *
 * Defines how deep link URLs map to screens and how their parameters are parsed.
 *
 * Supported query parameters:
 * - `week`: Week identifier (e.g., "2025-W42")
 * - `category`: Product category ("market", "specials", "dinners", etc.)
 * - `subcategory`: Product subcategory (e.g., "free-for-life")
 * - `c`: Box voucher code (handled natively)
 * - `ac`: Addon voucher code (handled natively)
 *
 * @example
 * store?week=2025-W42&category=market&subcategory=free-for-life
 */
const config: LinkingOptions<StoreStackParamsList>['config'] = {
  screens: {
    [StoreStackRoutes.Storefront]: STORE_PATH_NAME,
    [StoreStackRoutes.Upsell]: STORE_PATH_NAME,
  },
};

const base = createModuleLinking<StoreStackParamsList>(config);

export const linkingConfig: LinkingOptions<StoreStackParamsList> = {
  ...base,
};
```

**Key patterns demonstrated:**
- Use createModuleLinking with typed config
- Route enum constants for screen names (StoreStackRoutes)
- Both Storefront and Upsell use same path ('store')
- Routing logic determined by getStateFromPath (see next example)
- JSDoc comments documenting supported query parameters
- Example URL format in documentation

## Example 2: Complex getStateFromPath with Query Parameter Routing

**File**: `modules/store/stacks/store/linking/linkingConfig.ts:78`

This example shows sophisticated routing logic based on query parameters and brand detection.

```typescript
import { parseStoreQueryParams } from './helpers';
import { StoreCategoryTypes } from './types';
import { BrandCategory, type Brand } from '@libs/system-country';
import { brandCategoryMap } from '@libs/brand-variants';
import { queryClient } from '@libs/query';

/**
 * Helper function to check if current brand is RTE (Factor, YouFoodz)
 */
const isRTEBrand = (): boolean => {
  try {
    const appConfig = queryClient.getQueryData<{ brand: Brand }>([
      NATIVE_MODULES_REPOSITORY_QUERY_KEY,
      AppConfigDataAccess.repositoryKey,
    ]);

    if (!appConfig?.brand) return false;

    const rteBrands = brandCategoryMap[BrandCategory.RTE];
    return rteBrands.includes(appConfig.brand);
  } catch {
    // If brand is not available, default to non-RTE behavior (YourCompany)
    return false;
  }
};

/**
 * Custom state parser that determines which screen to navigate to based on URL parameters
 *
 * @param path - The full deep link path (e.g., "store?week=2025-W39&category=market")
 * @returns Navigation state with the appropriate screen and parsed parameters
 */
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
          isDeepLink: true,
        },
      ],
    };
  }

  // Parse query parameters to determine routing and extract parameters
  const { week, category, subcategory, voucherApplied, voucherMessage } =
    parseStoreQueryParams(queryString);

  // Market category routing depends on brand
  // - RTE brands (Factor, YouFoodz): go to Upsell screen
  // - Other brands: go to Storefront with market category
  if (category === StoreCategoryTypes.Market) {
    if (isRTEBrand()) {
      // RTE brands: route to Upsell screen
      return {
        routes: [
          {
            name: StoreStackRoutes.Upsell,
            params: {
              weekId: week,
              preSelectedSubcategory: subcategory,
              isDeepLink: true,
              voucherApplied,
              voucherMessage,
            },
          },
        ],
      };
    } else {
      // Non-RTE brands: route to Storefront with market category
      return {
        routes: [
          {
            name: StoreStackRoutes.Storefront,
            params: {
              categoryId: category,
              selectedWeek: week,
              isDeepLink: true,
              voucherApplied,
              voucherMessage,
              preSelectedSubcategory: subcategory,
            },
          },
        ],
      };
    }
  }

  // All other categories route to Storefront screen
  return {
    routes: [
      {
        name: StoreStackRoutes.Storefront,
        params: {
          categoryId: category,
          selectedWeek: week,
          isDeepLink: true,
          voucherApplied,
          voucherMessage,
        },
      },
    ],
  };
};

export const linkingConfig: LinkingOptions<StoreStackParamsList> = {
  ...base,
  getStateFromPath,
};
```

**Key patterns demonstrated:**
- Split path into pathname and queryString
- Early return fallback for non-matching paths
- Parse query parameters with helper function
- Brand-specific routing logic (RTE vs non-RTE)
- Synchronous queryClient.getQueryData for brand check
- Try/catch with fallback for missing data
- Always include isDeepLink: true in params
- Multiple conditional routing paths
- Inline comments explaining business logic

## Example 3: Query Parameter Parsing Helper

**File**: `modules/store/stacks/store/linking/helpers.ts:10`

This example shows reusable query parameter parsing logic.

```typescript
import { DEFAULT_STORE_CATEGORY } from './constants';
import { StoreQueryParams, type ParsedStoreQueryParams } from './types';

/**
 * Parses query parameters from a Store deep link URL
 *
 * @param queryString - The query string portion of the URL (after '?')
 * @returns Parsed query parameters with defaults applied
 */
export const parseStoreQueryParams = (
  queryString?: string
): ParsedStoreQueryParams => {
  const searchParams = new URLSearchParams(queryString ?? '');

  const voucherAppliedParam = searchParams.get(StoreQueryParams.VoucherApplied);
  let voucherApplied: boolean | undefined;
  if (voucherAppliedParam) {
    voucherApplied = voucherAppliedParam === 'true';
  } else {
    voucherApplied = undefined;
  }

  const voucherMessage =
    searchParams.get(StoreQueryParams.VoucherMessage) ?? undefined;

  return {
    week: searchParams.get(StoreQueryParams.Week) ?? undefined,
    category:
      searchParams.get(StoreQueryParams.Category) ?? DEFAULT_STORE_CATEGORY,
    subcategory: searchParams.get(StoreQueryParams.Subcategory) ?? undefined,
    voucherApplied,
    voucherMessage,
  };
};
```

**Key patterns demonstrated:**
- URLSearchParams for query parsing
- Null coalescing operator (??) for defaults
- Boolean parameter parsing (string 'true' → boolean)
- Default values for missing parameters (DEFAULT_STORE_CATEGORY)
- undefined for optional parameters
- Enum constants for query parameter keys (StoreQueryParams)
- Type-safe return type (ParsedStoreQueryParams)

## Example 4: createModuleLinking Implementation

**File**: `libs/deeplinking/createModuleLinking.ts:15`

This example shows the internal implementation of createModuleLinking.

```typescript
import type { LinkingOptions } from '@react-navigation/native';
import { SharedModulesNavigation } from '@libs/native-modules/navigation';
import { deepLinkQueue } from './DeepLinkQueue';
import { createEventSubscriber } from './executeDeeplinkEventListeners';

/**
 * Creates a stack-scoped linking configuration that:
 * - Uses native-provided initialURL via SharedModulesNavigation
 * - Subscribes to React Native Linking 'url' events (re-emitted by native bridge)
 * - Accepts a per-stack config mapping of paths to screen names
 * - Handles cold start deeplinks through queue to prevent race conditions
 */
export const createModuleLinking = <T extends object>(
  config: LinkingOptions<T>['config']
): LinkingOptions<T> => {
  return {
    // Use a minimal prefix to help React Navigation's URL matching
    prefixes: [''],
    config,
    getInitialURL: async () => {
      const initialURL = await SharedModulesNavigation.getInitialURL();

      if (!initialURL) {
        return null;
      }

      // If queue is ready, process immediately
      if (deepLinkQueue.getIsReady()) {
        console.warn(
          '[createModuleLinking] Queue ready, returning initial URL for React Navigation'
        );
        return initialURL;
      }

      // If queue is not ready, enqueue the URL and return null
      // This prevents React Navigation from processing it before essential data is loaded
      console.warn(
        '[createModuleLinking] Queue not ready, enqueueing initial URL and blocking React Navigation'
      );
      deepLinkQueue.enqueue(initialURL);
      return null;
    },
    subscribe: createEventSubscriber,
  };
};
```

**Key patterns demonstrated:**
- Generic type parameter <T extends object>
- prefixes: [''] for minimal React Navigation prefix
- Async getInitialURL for native bridge call
- Queue readiness check (deepLinkQueue.getIsReady())
- Enqueue if not ready, return null to block navigation
- Console warnings for debugging cold start behavior
- createEventSubscriber for runtime URL events
- SharedModulesNavigation.getInitialURL() for initial URL

## Example 5: DeepLinkQueue Implementation

**File**: `libs/deeplinking/DeepLinkQueue.ts:9`

This example shows the queue class that prevents cold start race conditions.

```typescript
import { Linking } from 'react-native';

/**
 * DeepLinkQueue manages deeplinks during app initialization
 *
 * Holds deeplinks in a queue until essential data is loaded,
 * preventing race conditions during cold start.
 */
class DeepLinkQueue {
  private queue: string[] = [];
  private isReady = false;
  private listeners: (() => void)[] = [];
  private timeoutId: ReturnType<typeof setTimeout> | null = null;
  private readonly TIMEOUT_MS = 5000; // 5 seconds failsafe

  /**
   * Add a deeplink to the queue
   * If ready, execute immediately; otherwise queue for later
   */
  enqueue(url: string): void {
    if (this.isReady) {
      this.executeDeepLink(url);
    } else {
      this.queue.push(url);
      // Start timeout if this is the first item and no timeout is running
      if (this.queue.length === 1 && !this.timeoutId) {
        this.startFailsafeTimeout();
      }
    }
  }

  /**
   * Mark the queue as ready and flush all pending deeplinks
   * Should be called when essential data (plan, auth, etc.) is loaded
   */
  setReady(): void {
    if (this.isReady) return;
    this.isReady = true;

    // Clear timeout since we're now ready
    this.clearFailsafeTimeout();

    // Execute all queued deeplinks
    while (this.queue.length > 0) {
      const url = this.queue.shift();
      if (url) this.executeDeepLink(url);
    }

    // Notify listeners that we're ready
    this.listeners.forEach((listener) => listener());
    this.listeners = [];
  }

  getIsReady(): boolean {
    return this.isReady;
  }

  /**
   * Execute a deeplink immediately
   */
  private executeDeepLink(url: string): void {
    try {
      Linking.emit('url', { url });
    } catch (error) {
      console.error('[DeepLinkQueue] Error executing deeplink:', error);
    }
  }

  /**
   * Start failsafe timeout to prevent deadlocks
   */
  private startFailsafeTimeout(): void {
    this.timeoutId = setTimeout(() => {
      if (!this.isReady && this.queue.length > 0) {
        this.setReady();
      }
    }, this.TIMEOUT_MS);
  }

  private clearFailsafeTimeout(): void {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
      this.timeoutId = null;
    }
  }
}

// Singleton instance
export const deepLinkQueue = new DeepLinkQueue();
```

**Key patterns demonstrated:**
- Private fields for encapsulation
- isReady flag to track initialization state
- 5-second failsafe timeout to prevent deadlocks
- enqueue checks isReady and executes immediately if ready
- setReady flushes all queued deeplinks
- Linking.emit('url', { url }) for deeplink execution
- Try/catch in executeDeepLink for error handling
- Listener pattern with onReady() for subscribers
- Singleton pattern for global queue instance
- clearFailsafeTimeout when ready

## Example 6: Multiple Stacks with Shared Paths

**File**: `modules/home/stacks/home/linking/linkingConfig.ts:66`

This example shows how HomeStack handles both home-specific and store deeplinks.

```typescript
import type { LinkingOptions } from '@react-navigation/native';
import { createModuleLinking } from '@libs/deeplinking';
import {
  parseStoreQueryParams,
  STORE_PATH_NAME,
  StoreCategoryTypes,
} from '@modules/store/stacks/store/linking';
import { StoreStackRoutes } from '@modules/store/stacks/store/routes';
import { HomeStackRoutes } from '../routes';
import type { HomeStackParamsList } from '../types';

/**
 * React Navigation linking configuration for Home stack
 *
 * Handles both home-specific and store deeplinks since HomeStack includes
 * store screens via createStoreStackScreens. Uses the same routing logic
 * as StoreStack to avoid conflicts.
 */
const config: LinkingOptions<HomeStackParamsList>['config'] = {
  screens: {
    // Home-specific screens
    [HomeStackRoutes.Homefront]: '',

    // Store screens - Storefront and Upsell use same path, resolved by getStateFromPath
    [StoreStackRoutes.Storefront]: STORE_PATH_NAME,
    [StoreStackRoutes.Upsell]: STORE_PATH_NAME,

    // Other store screens with unique paths
    [StoreStackRoutes.ProductDetails]: `${STORE_PATH_NAME}/product/:productId`,
    [StoreStackRoutes.Cart]: `${STORE_PATH_NAME}/cart`,
    [StoreStackRoutes.Promotion]: `${STORE_PATH_NAME}/promotion/:promotionId`,
    [StoreStackRoutes.OrderConfirmation]: `${STORE_PATH_NAME}/order-confirmation`,
  },
};

const base = createModuleLinking<HomeStackParamsList>(config);

const getStateFromPath: NonNullable<
  LinkingOptions<HomeStackParamsList>['getStateFromPath']
> = (path) => {
  const [pathname, queryString] = path.split('?');

  // Handle home path
  if (pathname === '' || pathname === '/') {
    return {
      routes: [{ name: HomeStackRoutes.Homefront }],
    };
  }

  // Handle store paths (same logic as StoreStack)
  if (pathname === STORE_PATH_NAME) {
    const { week, category, subcategory, voucherApplied, voucherMessage } =
      parseStoreQueryParams(queryString);

    // Market category routing depends on brand
    if (category === StoreCategoryTypes.Market) {
      if (isRTEBrand()) {
        return {
          routes: [
            {
              name: StoreStackRoutes.Upsell,
              params: {
                weekId: week,
                preSelectedSubcategory: subcategory,
                isDeepLink: true,
                voucherApplied,
                voucherMessage,
              },
            },
          ],
        };
      } else {
        return {
          routes: [
            {
              name: StoreStackRoutes.Storefront,
              params: {
                categoryId: category,
                selectedWeek: week,
                isDeepLink: true,
                voucherApplied,
                voucherMessage,
                preSelectedSubcategory: subcategory,
              },
            },
          ],
        };
      }
    }

    return {
      routes: [
        {
          name: StoreStackRoutes.Storefront,
          params: {
            categoryId: category,
            selectedWeek: week,
            isDeepLink: true,
            voucherApplied,
            voucherMessage,
          },
        },
      ],
    };
  }

  return {
    routes: [{ name: HomeStackRoutes.Homefront }],
  };
};

export const linkingConfig: LinkingOptions<HomeStackParamsList> = {
  ...base,
  getStateFromPath,
};
```

**Key patterns demonstrated:**
- HomeStack includes store screens via createStoreStackScreens
- Both home and store routes in single config
- Root path ('') for Homefront screen
- Nested paths for store screens (store/product/:productId)
- Shared routing logic between HomeStack and StoreStack
- parseStoreQueryParams imported from store module
- Fallback to Homefront for unrecognized paths
- Multiple conditional branches for different paths
- JSDoc explaining shared path handling

## Example 7: Unit Testing Deeplink Routing

**File**: `modules/store/stacks/store/linking/linkingConfig.test.ts:33`

This example shows comprehensive unit tests for deeplink routing logic.

```typescript
import { Brand } from '@libs/system-country';
import { StoreStackRoutes } from '../routes';
import { linkingConfig } from './linkingConfig';

// Mock dependencies
jest.mock('@libs/deeplinking', () => ({
  createModuleLinking: jest.fn((config) => ({ config })),
}));

jest.mock('@libs/query', () => ({
  queryClient: {
    getQueryData: jest.fn(),
  },
}));

const mockQueryClient = require('@libs/query').queryClient;

describe('Store Linking Config', () => {
  describe('getStateFromPath', () => {
    beforeEach(() => {
      // Default to YourCompany (non-RTE) for most tests
      mockQueryClient.getQueryData.mockReturnValue({
        brand: Brand.yourcompany,
      });
    });

    afterEach(() => {
      jest.clearAllMocks();
    });

    it('should route to Storefront with default parameters for store path without query params', () => {
      const result = linkingConfig.getStateFromPath?.('store');

      expect(result).toEqual({
        routes: [
          {
            name: StoreStackRoutes.Storefront,
            params: {
              categoryId: 'dinners',
              selectedWeek: undefined,
              isDeepLink: true,
              voucherApplied: undefined,
              voucherMessage: undefined,
            },
          },
        ],
      });
    });

    it('should route to Storefront with parsed parameters for non-market categories', () => {
      const result = linkingConfig.getStateFromPath?.(
        'store?week=2025-W42&category=specials'
      );

      expect(result).toEqual({
        routes: [
          {
            name: StoreStackRoutes.Storefront,
            params: {
              categoryId: 'specials',
              selectedWeek: '2025-W42',
              isDeepLink: true,
              voucherApplied: undefined,
              voucherMessage: undefined,
            },
          },
        ],
      });
    });

    it('should route to Upsell screen for market category on RTE brands (Factor)', () => {
      // Mock Factor brand (RTE)
      mockQueryClient.getQueryData.mockReturnValue({
        brand: Brand.factor,
      });

      const result = linkingConfig.getStateFromPath?.(
        'store?week=2025-W42&category=market&subcategory=free-for-life'
      );

      expect(result).toEqual({
        routes: [
          {
            name: StoreStackRoutes.Upsell,
            params: {
              weekId: '2025-W42',
              preSelectedSubcategory: 'free-for-life',
              isDeepLink: true,
              voucherApplied: undefined,
              voucherMessage: undefined,
            },
          },
        ],
      });
    });

    it('should route to Storefront with market category for YourCompany brand', () => {
      const result = linkingConfig.getStateFromPath?.(
        'store?week=2025-W42&category=market'
      );

      expect(result).toEqual({
        routes: [
          {
            name: StoreStackRoutes.Storefront,
            params: {
              categoryId: 'market',
              selectedWeek: '2025-W42',
              isDeepLink: true,
              voucherApplied: undefined,
              voucherMessage: undefined,
              preSelectedSubcategory: undefined,
            },
          },
        ],
      });
    });

    it('should handle voucher parameters', () => {
      const result = linkingConfig.getStateFromPath?.(
        'store?week=2025-W42&category=dinners&voucherApplied=true&voucherMessage=Success'
      );

      expect(result).toEqual({
        routes: [
          {
            name: StoreStackRoutes.Storefront,
            params: {
              categoryId: 'dinners',
              selectedWeek: '2025-W42',
              isDeepLink: true,
              voucherApplied: true,
              voucherMessage: 'Success',
            },
          },
        ],
      });
    });
  });
});
```

**Key patterns demonstrated:**
- Mock createModuleLinking to return config object
- Mock queryClient.getQueryData for brand testing
- beforeEach sets default brand (YourCompany)
- afterEach clears all mocks
- Test default parameters with no query string
- Test query parameter parsing
- Test brand-specific routing (Factor vs YourCompany)
- Test voucher parameter handling
- Verify exact route names and params
- Use optional chaining for getStateFromPath call

## Summary

The YourCompany codebase consistently follows these deep linking patterns:

1. **createModuleLinking** for all linking configurations (handles cold start, queue, native bridge)
2. **Route enums** for type-safe screen names (StoreStackRoutes, HomeStackRoutes)
3. **getStateFromPath** for sophisticated query parameter routing
4. **Query parameter helpers** for reusable parsing logic (parseStoreQueryParams)
5. **DeepLinkQueue** prevents race conditions during cold start (5-second failsafe)
6. **isDeepLink: true** in all route params for analytics tracking
7. **Fallback routing** for invalid or unrecognized paths
8. **Brand-specific logic** where needed (RTE vs non-RTE brands)
9. **Shared routing logic** between stacks handling same paths
10. **Comprehensive unit tests** for routing logic validation
11. **JSDoc comments** explaining supported query parameters
12. **URLSearchParams** for query string parsing

These patterns ensure reliable, type-safe deep linking with proper cold start handling, preventing navigation errors and enabling sophisticated routing logic throughout the app.
