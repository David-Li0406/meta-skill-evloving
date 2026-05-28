# Documentation Examples

Real-world documentation examples from the YourCompany shared-mobile-modules project.

## Component Documentation with @description, @context, @example

From `src/entry-providers/providers.tsx`:

```typescript
/**
 * @description
 * `NavigationEntryProvider` is a higher-order component designed to wrap a navigation stack.
 * It provides the necessary context for navigation and deep linking within the app.
 * Now supports optional repository loading to ensure critical data is available before rendering.
 *
 * This provider is typically used when creating a module that contains multiple screens.
 * All Screens within the stack are wrapped around the `ScreenEntryProvider` to ensure
 * proper services are available.
 * You can pass a `linking` prop to enable deep linking functionality, which allows the Stack
 * to handle URLs and navigate to specific screens within the stack structure.
 *
 * @param props.requiredRepositories - Optional map of repository keys to required properties that must be loaded before rendering.
 *                                Each key maps to an array of property names that must exist in that repository's data.
 * @param props.repositoryLoadingFallback - Optional custom loading component to display while repositories are loading
 * @param props.linking - Optional deep linking configuration for navigation
 *
 * @example
 * ```tsx
 * import { NavigationEntryProvider } from './providers';
 * import { REPOSITORY_KEYS } from '@data-access/native/constants';
 * import { createStackNavigator } from '@react-navigation/stack';
 *
 * const Stack = createStackNavigator();
 *
 * // Basic usage without repository loading
 * const BasicStack = () => (
 *   <NavigationEntryProvider linking={linkingConfig}>
 *     <Stack.Navigator>
 *       // ... screens
 *     </Stack.Navigator>
 *   </NavigationEntryProvider>
 * );
 *
 * // Usage with repository loading
 * const OnboardingStack = () => (
 *   <NavigationEntryProvider
 *     linking={linkingConfig}
 *     requiredRepositories={{
 *       [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
 *       [REPOSITORY_KEYS.auth]: ['authToken']
 *     }}
 *     repositoryLoadingFallback={LoadingSpinner}
 *   >
 *     <Stack.Navigator>
 *       // ... screens
 *     </Stack.Navigator>
 *   </NavigationEntryProvider>
 * );
 * ```
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
```

**Key patterns:**
- **@description** provides comprehensive explanation
- **@param** documents each parameter
- **@example** shows both basic and advanced usage
- Examples use realistic code from the actual codebase

## TODO Comments

From `src/features/reactivation-banner-feature/`:

```typescript
// TODO(@hamza): Do we need this? Validate with the team.
interface ExpandedVariantProps {
  // ...
}

// @TODO(@conversion-mobile): Verify if this is correct.
const styles = {
  // ...
};

// @TODO(@conversion-mobile): Replace hardcoded value with dynamic values
{/* Static display value */}

// @TODO @hamzahayat | Determine what other information we need from the response.
export const transformSubscriptionData = (response: SubscriptionResponse) => {
  // ...
};

/**
 * @TODO: @hamzahayat | Add Feature Flag for Reactivation Banner and Global Reactivation Button
 */
export const useReactivationEligibility = () => {
  // ...
};

// @TODO: use turbo image for the image : https://yourcompany.atlassian.net/browse/PUMA-610
export const RecipeImage = ({ source }: RecipeImageProps) => {
  // ...
};

// TODO: update to key that points to home-page-meals once available
const CAROUSEL_KEY = 'temp-key';

// @TODO: Add logic for Free For Life Banner
const renderBanner = () => {
  // ...
};
```

**Patterns:**
- `TODO` - General future work
- `TODO(@username)` - Assigned to specific developer
- `@TODO` - Alternative format used in codebase
- `TODO: description | details` - With detailed context
- Include ticket URLs when relevant

## Feature README

From `src/features/reactivation-banner-feature/README.md`:

```markdown
# Reactivation Banner Feature

The Reactivation Banner is a UI component that appears at the top of the home screen when a user's subscription is inactive. This feature is part of Project ABBA's Reactivation State homepage.

## Overview

The banner has two distinct visual states that transition smoothly based on scroll position:

1. **Expanded** – Shown when the user first lands on the homepage, displaying comprehensive reactivation information
2. **Collapsed** – Shown when the user scrolls down, displaying a more compact version of the banner

## Components Structure

```
reactivation-banner-feature/
├── components/               # Smaller subcomponents
│   ├── discount-applied-pill/ # Discount applied indicator component
│   │   ├── DiscountAppliedPill.tsx   # Component implementation
│   │   └── index.ts          # Re-export of component
│   ├── plan-details/         # Plan details component
│   │   ├── PlanDetails.tsx   # Component implementation
│   │   ├── styles.ts         # Component styles
│   │   └── index.ts          # Re-export of component
│   └── index.ts              # Re-export of subcomponents
├── hooks/
│   ├── useReactivationBannerAnimation.ts  # Custom hook for banner animation
│   └── index.ts              # Re-export of hooks
├── styles/
│   ├── containerStyles.ts    # Styles for the main container
│   ├── expandedBannerStyles.ts  # Styles for the expanded state
│   ├── collapsedBannerStyles.ts # Styles for the collapsed state
│   └── index.ts              # Re-export of style configs
├── constants.ts              # Constants including test IDs, accessibility roles
├── types.ts                  # Type definitions for components and hooks
├── ReactivationBanner.tsx    # Main container component
├── ReactivationBannerExpanded.tsx  # Expanded state component
├── ReactivationBannerCollapsed.tsx # Collapsed state component
└── index.ts                  # Public exports
```

## Features

- **Responsive Scroll Behavior**: Transitions between expanded and collapsed states based on scroll position
- **Smooth Animation**: Uses fade transitions for a polished user experience
- **Accessibility Support**: Includes proper accessibility attributes and test IDs
- **Modular Design**: Components are structured for reusability and maintainability

## Usage

```tsx
import { ReactivationBanner } from '@features/reactivation-banner-feature';
import { Animated, ScrollView } from 'react-native';

const HomeScreen = () => {
  // Create animated scroll value to track scroll position
  const scrollY = new Animated.Value(0);

  // Track banner height for proper content padding
  const [bannerHeight, setBannerHeight] = useState(0);

  return (
    <View style={{ flex: 1 }}>
      <ReactivationBanner
        scrollY={scrollY}
        onMaxHeightChange={setBannerHeight}
      />

      <Animated.ScrollView
        contentContainerStyle={{ paddingTop: bannerHeight }}
        onScroll={Animated.event(
          [{ nativeEvent: { contentOffset: { y: scrollY } } }],
          { useNativeDriver: false }
        )}
        scrollEventThrottle={16}
      >
        {/* Scrollable content */}
      </Animated.ScrollView>
    </View>
  );
};
```

## Key Components

### ReactivationBanner

The main container component that:

- Manages the state transition between expanded and collapsed versions
- Handles animation based on scroll position
- Determines when to show/hide each banner variant

### ReactivationBannerExpanded

The expanded version of the banner that appears when a user first lands on the page or scrolls back to the top. It includes:

- Banner title and description
- Plan details with user's subscription information
- Promo code information to encourage reactivation
- Promo code CTA for entering promotional codes

### ReactivationBannerCollapsed

The compact version of the banner that appears when the user scrolls down. It includes:

- Condensed reactivation message
- Visual indicator (arrow) to encourage tapping

## Animation Behavior

The animation between expanded and collapsed states is managed by the `useReactivationBannerAnimation` hook:

1. When the user scrolls past a certain threshold (calculated based on the expanded banner's height), the collapsed banner fades in
2. Both expanded and collapsed banners are kept in the DOM for smoother transitions
3. The banners use translateY transforms to slide in and out of view based on scroll position:
   - The expanded banner translates upward (negative Y) as the user scrolls down
   - The collapsed banner translates from an off-screen position to visible as opacity increases
4. When the user scrolls back up, the expanded banner slides back into view and the collapsed banner fades out

## Customization

The feature currently uses mocked data for development and testing. In a real implementation:

1. Replace mock data in `constants.ts` with data from your reactivation service
2. Add appropriate handlers for button presses to trigger reactivation flows
3. Customize the styling as needed using the modular style files

## Testing

The feature includes comprehensive tests for all components:

- `ReactivationBanner.test.tsx` - Tests for the main container and animation behavior
- `ReactivationBannerExpanded.test.tsx` - Tests for the expanded state UI
- `ReactivationBannerCollapsed.test.tsx` - Tests for the collapsed state UI
- `hooks/useReactivationBannerAnimation.test.ts` - Tests for the animation hook
- `components/meal-plan/MealPlan.test.tsx` - Tests for the meal plan component with different discount states
- `components/promo-code-input/PromoCodeInput.test.tsx` - Tests for the promo code input component
- `components/promo-code-modal/PromoCodeModal.test.tsx` - Tests for the promo code modal component

## Implementation Note

This feature implements the UI and animation behavior only. Business logic for fetching user subscription status and handling reactivation actions should be implemented separately.
```

**README structure:**
- **Overview** - High-level feature description
- **Components Structure** - Directory tree with explanations
- **Features** - Key capabilities
- **Usage** - Code example showing integration
- **Key Components** - Detailed component descriptions
- **Animation Behavior** - Complex behavior explanation
- **Customization** - How to adapt for production
- **Testing** - Test file locations
- **Implementation Note** - Important caveats

## Inline "Why" Comments

Examples of good inline comments that explain reasoning:

```typescript
// From data-access patterns:

// Prefetch next page while user views current page to improve perceived performance
prefetchNextPage();

// Disable interactions during animation to prevent race conditions
setIsAnimating(true);

// Rounding up ensures we never show a discount smaller than actual
// (e.g., 19.8% shows as 20% not 19%)
const discountPercent = Math.ceil(((originalPrice - discountedPrice) / originalPrice) * 100);

// Subscription disabled when product is sold out or delivery date has passed
if (isSubscribeDisabled) {
  return 'disabled';
}

// Global manager that handles loyalty state changes and invalidates caches.
// This ensures that when loyalty program state changes, all related data is refreshed.
const GlobalLoyaltyStateManager: React.FC = () => {
  useLoyaltyStateManager();
  return null;
};

// Disable submit while validating to prevent duplicate submissions
setIsSubmitting(true);
```

**Patterns:**
- Explain performance optimizations
- Clarify timing and synchronization
- Document business logic decisions
- Explain edge case handling
- Describe side effects and their purpose

## Interface Documentation

Example of well-documented configuration interface:

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

  /**
   * Custom loading component displayed while fetching price data.
   * @default LoadingSpinner
   */
  loadingFallback?: React.ComponentType;
}
```

**Patterns:**
- Interface-level description
- Per-property documentation
- @example for non-obvious values
- Business context in descriptions
- @default for optional properties

## Props Documentation

Example of well-documented component props:

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
   * Displays skeleton placeholder when true.
   * @default false
   */
  isLoading?: boolean;

  /**
   * Test ID for automated testing.
   * Used by Detox and other testing frameworks.
   * @default 'recipe-card'
   */
  testID?: string;

  /**
   * Style overrides for the card container.
   */
  style?: ViewStyle;

  /**
   * Accessibility label for screen readers.
   * Auto-generated from recipe name if not provided.
   */
  accessibilityLabel?: string;
}
```

**Patterns:**
- Brief property description
- Usage context for callbacks
- @param for callback parameters
- @default for optional props
- Implementation notes where helpful
