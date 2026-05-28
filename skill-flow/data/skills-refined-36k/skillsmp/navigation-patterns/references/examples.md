# Navigation Patterns - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating navigation patterns.

## Example 1: Complete Header Configuration with Multiple Buttons

**File**: `modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:46`

This example shows comprehensive header configuration with custom title, close button, and menu button.

```typescript
import { useCallback } from 'react';
import { View, TouchableOpacity } from 'react-native';
import { useNavigation } from '@libs/navigation';
import { useNavigationHeader } from '@libs/navigation-header';
import { useT9n } from '@libs/localization';
import { Icon, Text, useZestStyles } from '@zest/react-native';

export const SocialRecipeBridgeScreen = () => {
  const navigation = useNavigation();
  const styles = useZestStyles(stylesConfig);
  const { translateRaw } = useT9n('social-recipe-bridge');

  const handleClose = useCallback(() => {
    navigation.goBack();
  }, [navigation]);

  const handleMenuButtonPress = useCallback(() => {
    setIsMenuVisible(true);
  }, []);

  const renderCloseButton = useCallback(
    () => (
      <TouchableOpacity
        accessibilityRole="button"
        onPress={handleClose}
        testID="close-button"
      >
        <Icon
          icon="CloseOutline24"
          color="alias.color.neutral.foreground.inverse"
          altText={translateRaw(
            'social-recipe-bridge.screen.header.close.alt_text'
          )}
        />
      </TouchableOpacity>
    ),
    [handleClose, translateRaw]
  );

  const renderMenuButton = useCallback(
    () => (
      <TouchableOpacity
        accessibilityRole="button"
        onPress={handleMenuButtonPress}
        testID="menu-button"
      >
        <Icon
          icon="EllipsesOutline24"
          color="alias.color.neutral.foreground.inverse"
          altText={translateRaw(
            'social-recipe-bridge.screen.header.menu.alt_text'
          )}
        />
      </TouchableOpacity>
    ),
    [handleMenuButtonPress, translateRaw]
  );

  const renderHeader = useCallback(() => {
    return (
      <View style={styles.headerContainer}>
        <Text type="headline-lg" style={styles.headerTitle}>
          {translateRaw('social-recipe-bridge.screen.header.title')}
        </Text>
        <View style={styles.tag}>
          <Text type="body-xs-regular">Beta</Text>
        </View>
      </View>
    );
  }, [translateRaw, styles.headerContainer, styles.headerTitle, styles.tag]);

  // Configure navigation header with Zest theming
  useNavigationHeader({
    navigation,
    options: {
      headerTitle: renderHeader,
      headerLeft: renderCloseButton,
      headerRight: renderMenuButton,
    },
  });

  return (
    <View style={styles.container}>
      {/* content */}
    </View>
  );
};
```

**Key patterns demonstrated:**
- useCallback memoization for all render functions
- Custom header title component with Tag badge
- headerLeft for close button (goBack navigation)
- headerRight for menu button
- Zest Icon with theme-aware colors (alias.color.neutral.foreground.inverse)
- Complete accessibility (accessibilityRole, altText)
- testID for testing
- translateRaw for i18n
- All buttons use TouchableOpacity (not Button component)

## Example 2: Basic Header with String Title

**File**: `modules/store/screens/upsell/UpsellModule.tsx:71`

This example shows simple header configuration with translated string title.

```typescript
import { useNavigationHeader } from '@libs/navigation-header';
import { useT9n } from '@libs/localization';
import type { StoreStackNavigationProp } from '@modules/store/stacks/store/types';

const Upsell = ({
  route: {
    params: {
      weekId,
      preSelectedSubcategory = undefined,
      widgetSource,
      isDeepLink,
      sourceScreen,
      voucherApplied,
      voucherMessage,
    },
  },
  navigation,
}: StoreStackNavigationProp<StoreStackRoutes.Upsell>) => {
  const { translateRaw } = useT9n('store');

  useNavigationHeader({
    navigation,
    options: {
      headerTitle: translateRaw('store.browse.second-step.heading.label'),
    },
  });

  // Use route params
  const handleCardClicked = (productId: string, position?: number) => {
    navigation.navigate(StoreStackRoutes.ProductDetails, {
      planId: planId,
      deliveryId: weekId,
      productId: productId,
      source: SOURCE.LIST,
      position,
      widgetSource,
      category: 'market',
      subcategory: subcategory ?? undefined,
      categoryPosition: subcategoryPosition ?? 1,
    });
  };

  return <View>{/* content */}</View>;
};
```

**Key patterns demonstrated:**
- Simple headerTitle with translated string
- Typed route props (StoreStackNavigationProp<StoreStackRoutes.Upsell>)
- Destructured route params in component signature
- navigation.navigate with route enum and typed parameters
- Default parameter values (preSelectedSubcategory = undefined)
- Optional chaining in params (subcategory ?? undefined)

## Example 3: Route Enum Definitions

**File**: `modules/store/stacks/store/routes.ts:1`

This example shows standard route enum definition.

```typescript
export enum StoreStackRoutes {
  Storefront = 'Storefront',
  ProductDetails = 'ProductDetails',
  Cart = 'Cart',
  Promotion = 'Promotion',
  Upsell = 'Upsell',
  OrderConfirmation = 'OrderConfirmation',
  // @PLOP_INSERT_SCREEN_ROUTES
}
```

**Key patterns demonstrated:**
- Enum keys use PascalCase
- Enum values match keys (Storefront = 'Storefront')
- Plop insertion marker for code generation
- Exported for use across modules

**File**: `modules/social-recipe-bridge/types.ts:1`

```typescript
export enum SocialRecipeBridgeStackRoutes {
  SocialRecipeBridge = 'SocialRecipeBridge',
  CookbookFaq = 'CookbookFaq',
  RecipeDetail = 'RecipeDetail',
  EditRecipe = 'EditRecipe',
}
```

**Key patterns demonstrated:**
- Stack-specific route enums
- Named with Stack suffix (SocialRecipeBridgeStackRoutes)
- Each stack has own enum for logical grouping

## Example 4: Type-Safe Navigation with Parameters

**File**: `modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:218`

This example shows navigation with callback parameters.

```typescript
import { useCallback } from 'react';
import type { ExternalRecipeListItem } from '@data-access/query/external-recipes';
import { SocialRecipeBridgeStackRoutes } from '../../types';

export const SocialRecipeBridgeScreen = () => {
  const navigation = useNavigation();
  const { refetch } = useGetExternalRecipesInfinite({});

  const handleRecipePress = useCallback(
    (recipe: ExternalRecipeListItem) => {
      if (recipe.has_recipe_extracted) {
        navigation.navigate(SocialRecipeBridgeStackRoutes.RecipeDetail, {
          recipeId: recipe.id,
          // Pass list refetch so detail screen can update list after deletion
          // This is needed because the store is a singleton - when detail screen
          // registers its callbacks, it overwrites list's callbacks
          onRecipeDeleted: refetch,
        });
      } else {
        Linking.openURL(recipe.url).catch((error) => {
          console.error(
            '[SocialRecipeBridgeScreen] Failed to open recipe URL:',
            error
          );
        });
      }
    },
    [navigation, refetch]
  );

  const handleLearnMorePress = useCallback(() => {
    navigation.navigate(SocialRecipeBridgeStackRoutes.CookbookFaq);
  }, [navigation]);

  return (
    <RecipeList
      recipes={recipes}
      onRecipePress={handleRecipePress}
    />
  );
};
```

**Key patterns demonstrated:**
- Navigation with callback parameter (onRecipeDeleted: refetch)
- Conditional navigation based on data (has_recipe_extracted)
- Fallback to external link with Linking.openURL
- Error handling with catch
- useCallback with navigation and refetch dependencies
- Inline comment explaining callback pattern
- Simple navigation without parameters (CookbookFaq)

## Example 5: Going Back

**File**: `modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:112`

This example shows simple back navigation pattern.

```typescript
import { useCallback } from 'react';
import { useNavigation } from '@libs/navigation';

export const SocialRecipeBridgeScreen = () => {
  const navigation = useNavigation();

  const handleClose = useCallback(() => {
    navigation.goBack();
  }, [navigation]);

  // Used in close button
  const renderCloseButton = useCallback(
    () => (
      <TouchableOpacity
        onPress={handleClose}
        testID="close-button"
      >
        <Icon icon="CloseOutline24" />
      </TouchableOpacity>
    ),
    [handleClose]
  );

  return <View>{/* content */}</View>;
};
```

**Key patterns demonstrated:**
- navigation.goBack() for back navigation
- useCallback wraps goBack for stable reference
- handleClose passed to button render function
- Works with native back gestures automatically

## Example 6: Conditional Back Handler

**File**: `modules/store/screens/upsell/UpsellModule.tsx:64`

This example shows conditional logic on back navigation.

```typescript
import { useCallback } from 'react';
import { useBackHandler } from '@operations/back-navigation/useBackHandler';
import { HomeStackRoutes } from '@modules/home';

const Upsell = ({
  route: { params: { sourceScreen } },
  navigation,
}: StoreStackNavigationProp<StoreStackRoutes.Upsell>) => {
  const refetchDeliveriesOnSelection = useRefetchDeliveriesOnSelection();

  const handleGoBack = useCallback(() => {
    if (sourceScreen === HomeStackRoutes.Homefront) {
      refetchDeliveriesOnSelection();
    }
  }, [sourceScreen, refetchDeliveriesOnSelection]);

  useBackHandler(handleGoBack);

  return <View>{/* content */}</View>;
};
```

**Key patterns demonstrated:**
- Custom back handler with useBackHandler hook
- Conditional refetch based on source screen
- Route enum comparison (sourceScreen === HomeStackRoutes.Homefront)
- useCallback with route param and refetch dependencies
- Runs on hardware/gesture back button

## Example 7: Testing Navigation

**File**: `modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.test.tsx`

This example shows navigation mocking in tests.

```typescript
import { render, fireEvent } from '@testing-library/react-native';
import { SocialRecipeBridgeScreen } from './SocialRecipeBridgeScreen';

const mockNavigation = {
  navigate: jest.fn(),
  goBack: jest.fn(),
  setOptions: jest.fn(),
  getState: jest.fn(() => ({ routes: [] })),
};

jest.mock('@libs/navigation', () => ({
  useNavigation: () => mockNavigation,
}));

jest.mock('@libs/navigation-header', () => ({
  useNavigationHeader: jest.fn(),
}));

describe('SocialRecipeBridgeScreen', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render close button in header', () => {
    const { getByTestId } = render(<SocialRecipeBridgeScreen />);

    expect(getByTestId('close-button')).toBeTruthy();
  });

  it('should navigate back on close button press', () => {
    const { getByTestId } = render(<SocialRecipeBridgeScreen />);

    fireEvent.press(getByTestId('close-button'));

    expect(mockNavigation.goBack).toHaveBeenCalled();
  });

  it('should navigate to FAQ on learn more press', () => {
    const { getByTestId } = render(<SocialRecipeBridgeScreen />);

    fireEvent.press(getByTestId('learn-more-button'));

    expect(mockNavigation.navigate).toHaveBeenCalledWith(
      SocialRecipeBridgeStackRoutes.CookbookFaq
    );
  });
});
```

**Key patterns demonstrated:**
- Mock navigation object with all methods
- Mock useNavigation hook return value
- Mock useNavigationHeader as jest.fn() (no-op)
- jest.clearAllMocks() in beforeEach
- Test header button rendering with testID
- Test navigation calls with fireEvent.press
- Verify navigation.goBack() was called
- Verify navigation.navigate() with route enum
- getState mock for navigation state checks

## Summary

The YourCompany codebase consistently follows these navigation patterns:

1. **useNavigationHeader** for all header configuration (automatic Zest theming)
2. **useCallback** memoization for all header render functions
3. **Route enums** for type-safe navigation (PascalCase keys, string values match)
4. **Typed route parameters** in component props (StoreStackNavigationProp)
5. **TouchableOpacity** for header buttons (not Button component)
6. **Zest Icons** with theme tokens (alias.color.neutral.foreground.inverse)
7. **Complete accessibility** (accessibilityRole, accessibilityLabel, altText)
8. **testID** for all interactive elements
9. **translateRaw** for all user-facing strings (i18n)
10. **navigation.goBack()** for back navigation
11. **Callback parameters** for parent-child communication
12. **Mock navigation hooks** in tests

These patterns ensure consistent, type-safe, accessible, and testable navigation throughout the app.
