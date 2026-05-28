# Documentation Patterns

Common documentation patterns and anti-patterns.

## Pattern: @description for Comprehensive Explanations

Use @description to provide detailed explanations of component purpose and behavior.

✅ **Good:**
```typescript
/**
 * @description
 * `RepositoryLoader` ensures critical repository data is loaded before rendering child components.
 * Uses React Query's useQueries to fetch multiple repositories simultaneously.
 *
 * Error Handling Strategy:
 * - Does not handle errors internally
 * - Throws errors explicitly to bubble up to ErrorBoundary
 * - Validates required properties after successful load
 *
 * @param props.requiredRepositories - Map of repository keys to required property arrays
 * @param props.loadingFallback - Component to show while loading
 * @param props.children - Components to render after data loads
 */
export const RepositoryLoader = ({
  children,
  requiredRepositories,
  loadingFallback,
}: RepositoryLoaderProps) => {
  // Implementation
};
```

**Why:** @description provides comprehensive context including behavior, strategy, and error handling.

## Pattern: @context for Usage Guidance

Use @context to explain when and where to use a component or function.

✅ **Good:**
```typescript
/**
 * @context
 * This provider is typically used at the root of a feature module.
 * It should wrap all screens in the feature to provide consistent analytics context.
 *
 * Use this when:
 * - Creating a new feature module
 * - Need to add default analytics parameters for all screens
 * - Want to centralize analytics configuration
 *
 * Don't use this when:
 * - Only one screen needs analytics
 * - Analytics parameters vary significantly per screen
 */
export const AnalyticsProvider = ({ children, defaultParams }: AnalyticsProviderProps) => {
  // Implementation
};
```

**Why:** @context helps developers understand appropriate use cases and when to avoid using the code.

## Pattern: @example with Realistic Code

Provide concrete, realistic examples showing typical usage.

✅ **Good:**
```typescript
/**
 * Custom hook for tracking reactivation banner analytics events.
 *
 * @example
 * ```typescript
 * const { trackBannerView, trackBannerDismiss } = useReactivationAnalytics();
 *
 * useEffect(() => {
 *   trackBannerView({ banner_type: 'reactivation' });
 * }, [trackBannerView]);
 *
 * const handleDismiss = () => {
 *   trackBannerDismiss({ reason: 'user_action' });
 *   onDismiss();
 * };
 * ```
 */
export const useReactivationAnalytics = () => {
  // Implementation
};
```

❌ **Bad:**
```typescript
/**
 * Custom hook for analytics.
 *
 * @example
 * ```typescript
 * const analytics = useAnalytics();
 * analytics.track();
 * ```
 */
```

**Why:** Realistic examples show actual parameters, error handling, and integration with other code.

## Pattern: Document Complex Calculations

Explain complex calculations with the reasoning behind the approach.

✅ **Good:**
```typescript
/**
 * Calculate discount percentage, rounding up to nearest whole number.
 * Rounding up ensures we never show a discount smaller than actual
 * (e.g., 19.8% shows as 20% not 19%).
 */
const discountPercent = Math.ceil(((originalPrice - discountedPrice) / originalPrice) * 100);
```

❌ **Bad:**
```typescript
// Calculate discount percentage
const discountPercent = Math.ceil(((originalPrice - discountedPrice) / originalPrice) * 100);
```

**Why:** The "why" (rounding up to avoid underselling discount) is more valuable than the "what" (calculating discount).

## Pattern: Explain Performance Optimizations

Document performance-related decisions with the reasoning.

✅ **Good:**
```typescript
// Prefetch next page while user views current page to improve perceived performance
prefetchNextPage();

// Memoize expensive calculation to avoid recomputation on every render
const sortedItems = useMemo(() => items.sort(compareFn), [items]);

// Debounce search to avoid excessive API calls while user is typing
const debouncedSearch = useDebounce(searchTerm, 300);
```

❌ **Bad:**
```typescript
// Prefetch next page
prefetchNextPage();

// Use useMemo
const sortedItems = useMemo(() => items.sort(compareFn), [items]);
```

**Why:** Performance optimizations should explain the problem being solved, not just the technique.

## Pattern: Document Race Conditions and Timing

Explain timing-related logic and race condition prevention.

✅ **Good:**
```typescript
// Disable interactions during animation to prevent race conditions
setIsAnimating(true);

// Wait for layout to complete before measuring component dimensions
// Otherwise measurements may be incorrect or zero
requestAnimationFrame(() => {
  measureComponent();
});

// Cancel pending requests before starting new one
// Prevents stale data from overwriting newer results
abortController.abort();
```

❌ **Bad:**
```typescript
// Set animating
setIsAnimating(true);

// Wait for frame
requestAnimationFrame(() => {
  measureComponent();
});
```

**Why:** Timing and synchronization issues are non-obvious and benefit greatly from explanation.

## Pattern: TODO Comments with Context

Provide sufficient context in TODO comments for future work.

✅ **Good:**
```typescript
// TODO(@hamza): Do we need this field? Validate with product team before next release
interface ExpandedVariantProps {
  experimentalFeature?: boolean;
}

// TODO: Add error retry logic after implementing exponential backoff (ticket PUMA-610)
fetchData();

// FIXME: Race condition when multiple requests complete simultaneously
// See issue #1234 for reproduction steps
processResponses();

// HACK: Temporary workaround until API supports batch requests
// Remove after v2 API launch (Q2 2025)
for (const item of items) {
  await fetchItem(item.id);
}
```

❌ **Bad:**
```typescript
// TODO: Fix this
interface Props {
  field?: boolean;
}

// TODO: Add retry
fetchData();

// FIXME: Bug here
processResponses();
```

**Why:** Context helps future developers understand priority, blockers, and next steps.

## Pattern: Document Edge Cases

Explain handling of edge cases and special conditions.

✅ **Good:**
```typescript
// Subscription disabled when product is sold out or delivery date has passed
// Keep enabled for admins to allow manual overrides
if (isSubscribeDisabled && !user.isAdmin) {
  return 'disabled';
}

// Handle empty state separately to avoid division by zero
if (items.length === 0) {
  return null;
}

// iOS requires manual keyboard dismissal, Android handles automatically
if (Platform.OS === 'ios') {
  Keyboard.dismiss();
}
```

❌ **Bad:**
```typescript
// Check if disabled
if (isSubscribeDisabled && !user.isAdmin) {
  return 'disabled';
}

// Handle empty
if (items.length === 0) {
  return null;
}
```

**Why:** Edge cases are often non-obvious and need explanation of the business logic or platform behavior.

## Pattern: Document Prop Purpose and Usage

Explain the purpose of each prop, not just its type.

✅ **Good:**
```typescript
export interface RecipeCardProps {
  /**
   * Recipe data to display.
   */
  recipe: Recipe;

  /**
   * Callback when recipe card is pressed.
   * Typically used for navigation to recipe details.
   */
  onPress?: (recipeId: string) => void;

  /**
   * Callback when add to cart button is pressed.
   * Only called if recipe is available for purchase.
   * @param recipe - Recipe being added to cart
   */
  onAddToCart?: (recipe: Recipe) => void;

  /**
   * Whether card should show loading state.
   * Displays skeleton placeholder when true.
   * @default false
   */
  isLoading?: boolean;
}
```

❌ **Bad:**
```typescript
export interface RecipeCardProps {
  /** Recipe */
  recipe: Recipe;

  /** Press handler */
  onPress?: (recipeId: string) => void;

  /** Add to cart */
  onAddToCart?: (recipe: Recipe) => void;

  /** Loading */
  isLoading?: boolean;
}
```

**Why:** Prop documentation should explain purpose, typical usage, and important constraints.

## Pattern: Document Function Parameters

Provide clear descriptions of function parameters and their constraints.

✅ **Good:**
```typescript
/**
 * Transforms reactivation price response into voucher price info.
 *
 * @param response - API response from reactivation price endpoint
 *                   Must contain at least one product with valid pricing
 * @returns Voucher price information with prices in cents and analytics data
 *
 * @throws {Error} If response contains no products
 * @throws {ValidationError} If product data is missing required fields
 */
export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  // Implementation
};
```

❌ **Bad:**
```typescript
/**
 * Transform price response.
 * @param response - Response data
 * @returns Price info
 */
export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  // Implementation
};
```

**Why:** Parameter documentation should include constraints, expected format, and what errors might be thrown.

## Anti-Pattern: Stating the Obvious

Don't document what is obvious from the code.

❌ **Bad:**
```typescript
// Set loading to true
setIsLoading(true);

// Increment counter by 1
counter++;

// Call the fetchData function
fetchData();

// Map over items array
items.map(item => item.id);
```

✅ **Good:**
```typescript
// Show loading state while validating to prevent double submission
setIsLoading(true);

// Track number of retry attempts for exponential backoff
counter++;

// Fetch data without cache to ensure freshness after mutation
fetchData({ cache: 'no-store' });

// Extract IDs for bulk deletion API call
items.map(item => item.id);
```

**Why:** Comments should add information not obvious from reading the code.

## Anti-Pattern: Outdated Comments

Don't let comments become outdated when code changes.

❌ **Bad:**
```typescript
// Fetch user profile from API
// ^ Comment outdated after refactor
const data = await fetchProductDetails(productId);

// Returns array of user IDs
// ^ Function now returns objects, not IDs
function getUsers(): User[] {
  // Implementation
}
```

✅ **Good:**
```typescript
// Fetch product details including pricing and availability
const data = await fetchProductDetails(productId);

// Returns array of user objects with profile data
function getUsers(): User[] {
  // Implementation
}
```

**Why:** Outdated comments are worse than no comments - they mislead developers.

## Anti-Pattern: Over-Documenting Simple Code

Don't add JSDoc to simple, self-explanatory functions.

❌ **Bad:**
```typescript
/**
 * Gets the user name.
 * @param user - The user object
 * @returns The user's name
 */
const getName = (user: User) => user.name;

/**
 * Checks if number is even.
 * @param n - Number to check
 * @returns true if even, false if odd
 */
const isEven = (n: number) => n % 2 === 0;
```

✅ **Good:**
```typescript
// No documentation needed - code is self-explanatory
const getName = (user: User) => user.name;
const isEven = (n: number) => n % 2 === 0;
```

**Why:** Simple code doesn't benefit from documentation that just restates the obvious.

## Anti-Pattern: Documenting Implementation Details

Don't document how code works - document why it exists.

❌ **Bad:**
```typescript
/**
 * Uses Array.prototype.reduce to sum all numbers in the array.
 * Starts with initial value of 0 and adds each element.
 */
const sum = (numbers: number[]) => numbers.reduce((acc, n) => acc + n, 0);
```

✅ **Good:**
```typescript
/**
 * Calculate total price in cents for cart items.
 * Uses cents throughout to avoid floating point errors.
 */
const calculateTotal = (items: CartItem[]) =>
  items.reduce((acc, item) => acc + item.priceCents, 0);
```

**Why:** Implementation details are visible in code. Documentation should explain purpose and business logic.

## Anti-Pattern: Vague or Generic Descriptions

Don't use vague terms that don't add information.

❌ **Bad:**
```typescript
/**
 * Handles the thing.
 */
export const handleThing = () => {};

/**
 * Processes data.
 */
export const processData = (data: unknown) => {};

/**
 * Utility function for stuff.
 */
export const doStuff = () => {};
```

✅ **Good:**
```typescript
/**
 * Validates and sanitizes user input before saving to database.
 * Strips HTML tags and validates against XSS patterns.
 */
export const sanitizeUserInput = (input: string) => {};

/**
 * Transforms raw API response into normalized state for React Query cache.
 * Converts snake_case to camelCase and adds computed fields.
 */
export const normalizeApiResponse = (data: ApiResponse) => {};

/**
 * Debounces search input to reduce API calls while user types.
 * Waits 300ms after last keystroke before triggering search.
 */
export const debouncedSearch = useDebounce(searchTerm, 300);
```

**Why:** Specific descriptions provide valuable context, vague ones add no value.

## Pattern: README Structure for Features

Organize feature README with consistent structure.

✅ **Good:**
```markdown
# Feature Name

## Overview
Brief 2-3 sentence description of what the feature does and why it exists.

## Architecture
- `components/` - UI components
- `hooks/` - Custom hooks for data and state
- `stores/` - State management
- `constants.ts` - Constants and test IDs
- `types.ts` - Type definitions

## Usage
```tsx
<FeatureProvider config={config}>
  <FeatureComponent />
</FeatureProvider>
```

## Key Components

### MainComponent
Description of the main component and its responsibility.

### HelperComponent
Description of supporting component.

## Analytics Events
- `Feature_View` - When feature is displayed
- `Feature_Action` - When user interacts

## Testing
Run tests: `yarn test feature-name`

## Notes
Important caveats, limitations, or future work.
```

**Why:** Consistent structure makes README files scannable and helps developers find information quickly.
