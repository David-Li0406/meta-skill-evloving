---
name: documentation
description: "WHAT: JSDoc and inline documentation standards for React components and hooks. WHEN: documenting components, writing JSDoc for functions, explaining complex logic. KEYWORDS: jsdoc, documentation, comments, @description, @context, @example, inline, props, hooks, api."
---

# Documentation Standards

Best practices for writing clear and maintainable code documentation.

## When to Use

Use these standards when:
- Documenting React components and their props
- Writing JSDoc for complex functions or hooks
- Adding inline comments to explain non-obvious logic
- Creating README files for features or modules
- Documenting API interfaces and type definitions
- Explaining "why" decisions were made

## Core Principles

### Document the "Why", Not the "What"

Code should be self-documenting for **what** it does. Comments should explain **why** it exists or why it's implemented in a particular way.

✅ **Good:**
```typescript
// Disable submit while validating to prevent duplicate submissions
setIsSubmitting(true);

// Subscription disabled when product is sold out or delivery date has passed
if (isSubscribeDisabled) {
  return 'disabled';
}

// Prefetch next page while user views current page to improve perceived performance
prefetchNextPage();
```

❌ **Bad:**
```typescript
// Set loading to true
setIsLoading(true);

// Call fetchData function
fetchData();

// Increment counter by 1
counter++;
```

**Why:** "Why" comments provide valuable context that code alone cannot convey, helping future developers understand intent and reasoning.

### Use JSDoc for Public APIs

Document all components, hooks, and functions that are exported or part of a public API.

✅ **Good:**
```typescript
/**
 * Transforms reactivation price response into voucher price info.
 *
 * Converts API money objects to cents, calculates savings, and formats data
 * for display and analytics tracking.
 *
 * @param response - API response from reactivation price endpoint
 * @returns Voucher price information with prices in cents and analytics data
 *
 * @throws {Error} If response contains no products
 * @throws {Error} If product data is invalid or missing required fields
 *
 * @example
 * ```typescript
 * const response = await fetchReactivationPrice(voucherId);
 * const priceInfo = transformReactivationPriceResponse(response);
 *
 * console.log(priceInfo.savings); // 1000 (10.00 in cents)
 * console.log(priceInfo.currency); // 'USD'
 * ```
 */
export const transformReactivationPriceResponse = (
  response: ReactivationPriceResponse
): VoucherPriceInfo => {
  // Implementation
};
```

**Why:** JSDoc provides structured documentation that appears in IDE tooltips and generates documentation automatically.

## Component Documentation

### Document with @description, @context, and @example

Use these three tags to provide comprehensive component documentation.

✅ **Good:**
```typescript
/**
 * @description
 * `NavigationEntryProvider` is a higher-order component designed to wrap a navigation stack.
 * It provides the necessary context for navigation and deep linking within the app.
 * Now supports optional repository loading to ensure critical data is available before rendering.
 *
 * @context
 * This provider is typically used when creating a module that contains multiple screens.
 * All Screens within the stack are wrapped around the `ScreenEntryProvider` to ensure
 * proper services are available.
 * You can pass a `linking` prop to enable deep linking functionality.
 *
 * @param props.linking - Deep linking configuration for React Navigation
 * @param props.requiredRepositories - Optional map of repository keys to required properties
 * @param props.repositoryLoadingFallback - Optional custom loading component
 * @param props.children - Navigation stack or screens to render
 *
 * @example
 * ```tsx
 * <NavigationEntryProvider
 *   linking={linkingConfig}
 *   requiredRepositories={{
 *     [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
 *   }}
 *   repositoryLoadingFallback={LoadingSpinner}
 * >
 *   <Stack.Navigator>
 *     <Stack.Screen name="Home" component={HomeScreen} />
 *   </Stack.Navigator>
 * </NavigationEntryProvider>
 * ```
 */
export const NavigationEntryProvider = ({
  children,
  linking,
  requiredRepositories,
  repositoryLoadingFallback,
}: NavigationEntryProviderProps) => {
  // Implementation
};
```

**Structure:**
- **@description** - Explains what the component does and its purpose
- **@context** - Describes when and where to use it
- **@example** - Shows concrete usage with realistic code

### Document Props Interfaces

Add JSDoc comments to each prop explaining its purpose.

✅ **Good:**
```typescript
/**
 * Props for RecipeCard component.
 */
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
   * @param recipe - Recipe being added to cart
   */
  onAddToCart?: (recipe: Recipe) => void;

  /**
   * Whether card should show loading state.
   * @default false
   */
  isLoading?: boolean;

  /**
   * Test ID for automated testing.
   * @default 'recipe-card'
   */
  testID?: string;
}
```

**Why:** Property documentation clarifies purpose and usage, appears in IDE tooltips, and reduces need to look at implementation.

## Hook Documentation

Document custom hooks with their usage patterns and return values.

✅ **Good:**
```typescript
/**
 * Hook for fetching external recipes with infinite scroll support.
 *
 * Automatically handles pagination, loading states, and error handling.
 * Uses TanStack Query for caching and background refetching.
 *
 * @param params - Query parameters for filtering recipes
 * @param options - Additional TanStack Query options
 *
 * @returns Query result with infinite data, pagination controls, and loading states
 *
 * @example
 * ```typescript
 * const {
 *   data: infiniteData,
 *   fetchNextPage,
 *   hasNextPage,
 *   isLoading,
 * } = useGetExternalRecipesInfinite({ category: 'italian' });
 *
 * const recipes = infiniteData?.pages.flatMap(page => page.data) || [];
 * ```
 */
export const useGetExternalRecipesInfinite = (
  params: GetExternalRecipesParams,
  options?: UseInfiniteQueryOptions
) => {
  // Implementation
};
```

**Why:** Hooks have complex return values that benefit from documentation showing typical usage patterns.

## Type Documentation

### Document Interfaces and Types

Add descriptions to complex interfaces and their properties.

✅ **Good:**
```typescript
/**
 * Configuration for reactivation banner display and behavior.
 */
export interface ReactivationBannerConfig {
  /**
   * Unique identifier for the subscription being reactivated.
   */
  subscriptionId: string;

  /**
   * Voucher code from deep link, used for discount calculation.
   * @example "SAVE20"
   */
  deeplinkVoucherCode: string;

  /**
   * Distribution center ID for price calculation.
   * Prices vary by region.
   */
  dcId: string;

  /**
   * Whether to automatically show reactivation webview.
   * Set to true when user arrives via deep link.
   */
  shouldTriggerReactivationWebView: boolean;
}
```

**Why:** Interface documentation explains the purpose of each property and provides examples where helpful.

## Inline Comments

### Comment Complex Logic

Add comments to explain non-obvious logic or calculations.

✅ **Good:**
```typescript
/**
 * Calculate discount percentage, rounding up to nearest whole number.
 * Rounding up ensures we never show a discount smaller than actual
 * (e.g., 19.8% shows as 20% not 19%).
 */
const discountPercent = Math.ceil(((originalPrice - discountedPrice) / originalPrice) * 100);

// Disable interactions during animation to prevent race conditions
setIsAnimating(true);
```

**Why:** Complex calculations and non-obvious logic benefit from explanation of the approach and reasoning.

## TODO and FIXME Comments

Use structured comments for tracking future work.

✅ **Good:**
```typescript
// TODO: Add error retry logic after implementing exponential backoff
// TODO(username): Refactor this to use new API endpoint
// FIXME: Race condition when multiple requests complete simultaneously
// HACK: Temporary workaround until API supports batch requests
```

**Format:**
- `TODO` - Future improvement or feature
- `TODO(name)` - Assigned to specific person
- `FIXME` - Known bug that needs fixing
- `HACK` - Temporary solution needing proper fix

**Why:** Structured TODO comments make it easy to search for and track technical debt.

## README Files

### Feature Documentation

Create README files for complex features explaining architecture and usage.

**Structure:**
```markdown
# Feature Name

## Overview
Brief description of what the feature does

## Architecture
- `components/` - UI components
- `hooks/` - Custom hooks
- `stores/` - State management
- `constants.ts` - Feature constants

## Usage
```tsx
Code example showing how to use the feature
```

## Analytics Events
List of analytics events tracked by this feature

## Testing
Instructions for running tests
```

**Why:** README files provide high-level feature documentation and onboarding for new developers.

## Common JSDoc Tags

### Standard Tags

```typescript
/**
 * Brief one-line description of the function.
 *
 * Longer multi-line description providing more context about
 * what the function does and when to use it.
 *
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @throws {ErrorType} Description of when error is thrown
 * @example Example code showing usage
 * @see RelatedFunction for related functionality
 * @deprecated Use newFunction() instead
 * @default Default value if applicable
 */
```

### @description Tag

Provides comprehensive explanation of component or function behavior.

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
 */
```

### @context Tag

Explains when and where to use the component or function.

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
 */
```

## Anti-Patterns

### Don't State the Obvious

❌ **Bad:**
```typescript
// Increment counter by 1
counter++;

// Call the setIsLoading function with true
setIsLoading(true);

// Fetch user profile
fetchUserProfile();
```

### Don't Let Comments Become Outdated

❌ **Bad:**
```typescript
// Fetch user profile
// ^ Comment outdated after refactor
fetchProductDetails(productId);
```

**Solution:** Remove or update comments when code changes.

### Don't Over-Document

❌ **Bad:**
```typescript
/**
 * Gets the user name.
 * @param user - The user object
 * @returns The user's name
 */
const getName = (user: User) => user.name;
```

**Why:** Simple, self-explanatory code doesn't need JSDoc.

## Best Practices

1. **Document the Why** - Explain reasoning and intent, not implementation
2. **Use JSDoc for APIs** - Document all exported functions, hooks, and components
3. **Provide Examples** - Show concrete usage in @example tags
4. **Keep Current** - Update documentation when code changes
5. **Be Concise** - Clear and brief is better than verbose
6. **Use @context** - Help developers understand when to use code
7. **Document Edge Cases** - Explain non-obvious behavior or limitations

## Additional Resources

For implementation examples and patterns, see:
- [references/examples.md](references/examples.md) - Real documentation from the codebase
- [references/patterns.md](references/patterns.md) - Documentation patterns and anti-patterns
