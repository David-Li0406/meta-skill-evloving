---
name: navigation-patterns
description: "WHAT: React Navigation patterns with useNavigationHeader and type-safe route enums. WHEN: configuring screen headers, creating header buttons, navigating with parameters. KEYWORDS: navigation, useNavigationHeader, route enum, header, navigate, params, React Navigation, goBack, headerLeft."
---

# Navigation Patterns

## Core Principles

**Use `useNavigationHeader` for all header configuration.** It automatically applies Zest theme styling (colors, fonts, spacing) and uses `useLayoutEffect` internally to prevent header flicker.

**Define routes as enums for type safety.** Enums prevent typos, enable IDE autocomplete, and make route refactoring safer.

**Why**: Consistent navigation patterns improve UX, ensure design system compliance, and provide compile-time type safety.

## When to Use This Skill

Use these patterns when:

- Configuring screen headers with titles and buttons
- Creating custom header buttons (close, save, menu)
- Navigating between screens with parameters
- Defining routes for navigation stacks
- Implementing conditional header UI based on state
- Testing navigation behavior
- Ensuring consistent theming across all headers

## useNavigationHeader Hook

### Basic Header Configuration

Use `useNavigationHeader` to configure screen headers with automatic Zest theme styling.

```typescript
import { useNavigation } from '@libs/navigation';
import { useNavigationHeader } from '@libs/navigation-header';
import { useT9n } from '@libs/localization';

const ProductDetailsScreen = () => {
  const navigation = useNavigation();
  const { translateRaw } = useT9n('product-details');

  useNavigationHeader({
    navigation,
    options: {
      headerTitle: translateRaw('product-details.header.title'),
    },
  });

  return <View>{/* content */}</View>;
};
```

**Why**: `useNavigationHeader` automatically applies Zest theme styling and uses `useLayoutEffect` internally to prevent header flicker.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/screens/upsell/UpsellModule.tsx:71`

### Automatic Theme Styling

The hook applies default styling from Zest theme automatically:

```typescript
// Default styles applied by useNavigationHeader (you don't write this)
const defaultOptions: NativeStackNavigationOptions = {
  headerShown: true,
  headerBackVisible: true,
  headerTitleAlign: 'left',
  headerBackButtonDisplayMode: 'minimal',
  headerTitleStyle: {
    fontFamily: theme.global.fontFamily.headline,
    fontSize: theme.global.fontSize.headline.headlineMd,
    color: theme.alias.color.neutral.foreground.inverse,
  },
  headerStyle: {
    backgroundColor: theme.alias.color.brand.background.default,
  },
  headerTintColor: theme.alias.color.neutral.foreground.inverse,
};
```

**Why**: Automatic theming ensures all headers follow the design system without manual color/font configuration.

### Custom Header Title Component

Render custom header title component instead of string:

```typescript
import { View } from 'react-native';
import { Text } from '@zest/react-native';

const SocialRecipeBridgeScreen = () => {
  const navigation = useNavigation();
  const { translateRaw } = useT9n('social-recipe-bridge');

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
  }, [translateRaw, styles]);

  useNavigationHeader({
    navigation,
    options: {
      headerTitle: renderHeader,
    },
  });

  return <View>{/* content */}</View>;
};
```

**Why**: Custom header components enable complex layouts like badges, tags, or multi-line titles.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:195`

## Custom Header Buttons

### Header Button Pattern

Create header buttons using TouchableOpacity with Zest Icons and memoize with `useCallback`.

```typescript
import { TouchableOpacity } from 'react-native';
import { Icon } from '@zest/react-native';
import { useT9n } from '@libs/localization';
import { useNavigationHeader } from '@libs/navigation-header';

const SocialRecipeBridgeScreen = () => {
  const navigation = useNavigation();
  const { translateRaw } = useT9n('social-recipe-bridge');

  const handleClose = useCallback(() => {
    navigation.goBack();
  }, [navigation]);

  const renderCloseButton = useCallback(
    () => (
      <TouchableOpacity
        onPress={handleClose}
        testID="close-button"
        accessibilityRole="button"
        accessibilityLabel={translateRaw(
          'social-recipe-bridge.screen.header.close.alt_text'
        )}
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

  useNavigationHeader({
    navigation,
    options: {
      headerTitle: translateRaw('social-recipe-bridge.screen.header.title'),
      headerLeft: renderCloseButton,
    },
  });

  return <View>{/* content */}</View>;
};
```

**Why**: `useCallback` memoization prevents unnecessary re-renders when navigation options update. Zest Icons ensure consistent iconography.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:156`

### Multiple Header Buttons

Add both left and right header buttons:

```typescript
const SocialRecipeBridgeScreen = () => {
  const navigation = useNavigation();
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
        onPress={handleClose}
        testID="close-button"
        accessibilityRole="button"
        accessibilityLabel={translateRaw('...close.alt_text')}
      >
        <Icon
          icon="CloseOutline24"
          color="alias.color.neutral.foreground.inverse"
          altText={translateRaw('...close.alt_text')}
        />
      </TouchableOpacity>
    ),
    [handleClose, translateRaw]
  );

  const renderMenuButton = useCallback(
    () => (
      <TouchableOpacity
        onPress={handleMenuButtonPress}
        testID="menu-button"
        accessibilityRole="button"
        accessibilityLabel={translateRaw('...menu.alt_text')}
      >
        <Icon
          icon="EllipsesOutline24"
          color="alias.color.neutral.foreground.inverse"
          altText={translateRaw('...menu.alt_text')}
        />
      </TouchableOpacity>
    ),
    [handleMenuButtonPress, translateRaw]
  );

  useNavigationHeader({
    navigation,
    options: {
      headerTitle: translateRaw('screen.title'),
      headerLeft: renderCloseButton,
      headerRight: renderMenuButton,
    },
  });
};
```

**Why**: Separate `useCallback` functions for each button enable independent memoization and testing.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:175`

### Conditional Header Buttons

Disable or change header buttons based on component state:

```typescript
const EditRecipeScreen = () => {
  const navigation = useNavigation();
  const [isFormValid, setIsFormValid] = useState(false);
  const { translateRaw } = useT9n('recipe');

  const handleSave = useCallback(() => {
    if (isFormValid) {
      saveRecipe();
    }
  }, [isFormValid, saveRecipe]);

  const renderSaveButton = useCallback(
    () => (
      <TouchableOpacity
        onPress={handleSave}
        testID="save-button"
        disabled={!isFormValid}
        accessibilityRole="button"
        accessibilityLabel={translateRaw('recipe.header.save.alt_text')}
      >
        <Icon
          icon="CheckmarkOutline24"
          color={
            isFormValid
              ? 'alias.color.neutral.foreground.inverse'
              : 'alias.color.neutral.foreground.disabled'
          }
          altText={translateRaw('recipe.header.save.alt_text')}
        />
      </TouchableOpacity>
    ),
    [handleSave, isFormValid, translateRaw]
  );

  useNavigationHeader({
    navigation,
    options: {
      headerTitle: translateRaw('recipe.header.title'),
      headerRight: renderSaveButton,
    },
  });

  return <View>{/* form */}</View>;
};
```

**Why**: Conditional styling and disabled state provide clear visual feedback about action availability.

## Route Type Safety

### Route Enums

Define route names as enums for type safety and autocomplete:

```typescript
// modules/store/stacks/store/routes.ts
export enum StoreStackRoutes {
  Storefront = 'Storefront',
  Upsell = 'Upsell',
  ProductDetails = 'ProductDetails',
  Cart = 'Cart',
  OrderConfirmation = 'OrderConfirmation',
  Promotion = 'Promotion',
}

// modules/social-recipe-bridge/types.ts
export enum SocialRecipeBridgeStackRoutes {
  SocialRecipeBridge = 'SocialRecipeBridge',
  CookbookFaq = 'CookbookFaq',
  RecipeDetail = 'RecipeDetail',
  EditRecipe = 'EditRecipe',
}
```

**Why**: Enums prevent typos, enable IDE autocomplete, and make route refactoring safer.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/stacks/store/routes.ts:1`

### Typed Navigation

Use route enums with navigation for type-safe navigation calls:

```typescript
import { useNavigation } from '@libs/navigation';
import { SocialRecipeBridgeStackRoutes } from '../../types';

const CookbookScreen = () => {
  const navigation = useNavigation();

  const handleLearnMorePress = useCallback(() => {
    navigation.navigate(SocialRecipeBridgeStackRoutes.CookbookFaq);
  }, [navigation]);

  return (
    <Button onPress={handleLearnMorePress}>
      Learn More
    </Button>
  );
};
```

**Why**: TypeScript catches invalid route names at compile time, preventing runtime navigation errors.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:133`

### Navigation with Parameters

Pass typed parameters when navigating:

```typescript
import { StoreStackRoutes } from '@modules/store/stacks/store/routes';

const ProductList = () => {
  const navigation = useNavigation();

  const handleProductPress = useCallback(
    (productId: string, position: number) => {
      navigation.navigate(StoreStackRoutes.ProductDetails, {
        planId: planId,
        deliveryId: weekId,
        productId: productId,
        source: SOURCE.LIST,
        position,
        category: 'market',
      });
    },
    [navigation, planId, weekId]
  );

  return <ProductList onPress={handleProductPress} />;
};
```

**Why**: Typed parameters ensure required navigation data is provided and prevent runtime errors from missing parameters.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/screens/upsell/UpsellModule.tsx:120`

### Accessing Route Parameters

Use route params in the destination screen:

```typescript
import { useRoute } from '@libs/navigation';
import type { StoreStackNavigationProp } from '@modules/store/stacks/store/types';

const ProductDetailsScreen = ({
  route: {
    params: { productId, planId, deliveryId, source, position, category },
  },
}: StoreStackNavigationProp<StoreStackRoutes.ProductDetails>) => {
  // Use typed parameters
  const product = useProductQuery(productId);

  return <ProductDetails product={product} />;
};
```

**Why**: Typed route props ensure type safety for screen parameters and document expected props.

## Navigation Patterns

### Going Back

Use `navigation.goBack()` for simple back navigation:

```typescript
const DetailScreen = () => {
  const navigation = useNavigation();

  const handleClose = useCallback(() => {
    navigation.goBack();
  }, [navigation]);

  return <CloseButton onPress={handleClose} />;
};
```

**Why**: `goBack()` maintains navigation history and works with native back gestures.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:112`

### Nested Stack Navigation

Navigate within nested stacks using route enums:

```typescript
// HomeStack includes Store screens via createStoreStackScreens
const HomeScreen = () => {
  const navigation = useNavigation();

  const handleShopPress = useCallback(() => {
    // Navigate to Store screen within Home stack
    navigation.navigate(StoreStackRoutes.Storefront, {
      categoryId: 'market',
      selectedWeek: currentWeek,
    });
  }, [navigation, currentWeek]);

  return <ShopButton onPress={handleShopPress} />;
};
```

**Why**: Nested navigation allows screens to be shared across multiple stacks while maintaining correct navigation state.

### Navigation with Callbacks

Pass callback functions as route parameters for parent screen updates:

```typescript
const RecipeListScreen = () => {
  const navigation = useNavigation();
  const { refetch } = useGetExternalRecipesInfinite({});

  const handleRecipePress = useCallback(
    (recipe: ExternalRecipeListItem) => {
      navigation.navigate(SocialRecipeBridgeStackRoutes.RecipeDetail, {
        recipeId: recipe.id,
        // Pass refetch so detail screen can update list after deletion
        onRecipeDeleted: refetch,
      });
    },
    [navigation, refetch]
  );

  return <RecipeList onPress={handleRecipePress} />;
};
```

**Why**: Callback parameters enable child screens to trigger parent screen updates (e.g., refetch after deletion).

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:240`

## Testing Navigation

### Mock Navigation in Tests

Mock navigation hooks for unit tests:

```typescript
import { render, fireEvent } from '@testing-library/react-native';

const mockNavigation = {
  navigate: jest.fn(),
  goBack: jest.fn(),
  setOptions: jest.fn(),
};

jest.mock('@libs/navigation', () => ({
  useNavigation: () => mockNavigation,
}));

jest.mock('@libs/navigation-header', () => ({
  useNavigationHeader: jest.fn(),
}));

describe('ProductListScreen', () => {
  it('navigates to product details on press', () => {
    const { getByTestId } = render(<ProductListScreen />);

    fireEvent.press(getByTestId('product-card-123'));

    expect(mockNavigation.navigate).toHaveBeenCalledWith(
      StoreStackRoutes.ProductDetails,
      expect.objectContaining({
        productId: '123',
      })
    );
  });
});
```

**Why**: Mocking navigation enables testing navigation logic without actual navigation behavior.

## Common Mistakes to Avoid

❌ **Don't hardcode theme values**:

```typescript
// ❌ Wrong - Hardcoded colors/fonts break theming
navigation.setOptions({
  headerTitleStyle: {
    color: '#FFFFFF',
    fontSize: 18,
    fontFamily: 'Inter-Bold',
  },
});
```

✅ **Do use useNavigationHeader**:

```typescript
// ✅ Correct - Theme values applied automatically
useNavigationHeader({
  navigation,
  options: {
    headerTitle: translateRaw('screen.title'),
  },
});
```

❌ **Don't forget to memoize header buttons**:

```typescript
// ❌ Wrong - Recreates function on every render
const renderButton = () => (
  <TouchableOpacity onPress={handlePress}>
    <Icon icon="PlusOutline24" />
  </TouchableOpacity>
);
```

✅ **Do memoize with useCallback**:

```typescript
// ✅ Correct - Stable reference across renders
const renderButton = useCallback(
  () => (
    <TouchableOpacity onPress={handlePress}>
      <Icon icon="PlusOutline24" />
    </TouchableOpacity>
  ),
  [handlePress]
);
```

❌ **Don't use string literals for routes**:

```typescript
// ❌ Wrong - No type safety
navigation.navigate('ProductDetails', { id: '123' });
```

✅ **Do use route enums**:

```typescript
// ✅ Correct - Type-safe, autocomplete, refactorable
navigation.navigate(StoreStackRoutes.ProductDetails, {
  productId: '123',
});
```

❌ **Don't use useEffect for navigation options**:

```typescript
// ❌ Wrong - Can cause header flicker
useEffect(() => {
  navigation.setOptions({ title: 'Products' });
}, [navigation]);
```

✅ **Do use useNavigationHeader**:

```typescript
// ✅ Correct - useLayoutEffect runs before paint
useNavigationHeader({
  navigation,
  options: {
    headerTitle: translateRaw('products.title'),
  },
});
```

❌ **Don't miss accessibility props**:

```typescript
// ❌ Wrong - Missing accessibility
<TouchableOpacity onPress={handleClose}>
  <Icon icon="CloseOutline24" />
</TouchableOpacity>
```

✅ **Do add accessibility**:

```typescript
// ✅ Correct - Complete accessibility
<TouchableOpacity
  onPress={handleClose}
  testID="close-button"
  accessibilityRole="button"
  accessibilityLabel={translateRaw('close.alt_text')}
>
  <Icon
    icon="CloseOutline24"
    color="alias.color.neutral.foreground.inverse"
    altText={translateRaw('close.alt_text')}
  />
</TouchableOpacity>
```

## Quick Reference

**Basic header configuration:**
```typescript
useNavigationHeader({
  navigation,
  options: {
    headerTitle: translateRaw('screen.title'),
  },
});
```

**Header buttons:**
```typescript
const renderButton = useCallback(
  () => (
    <TouchableOpacity onPress={handlePress}>
      <Icon icon="PlusOutline24" />
    </TouchableOpacity>
  ),
  [handlePress]
);

useNavigationHeader({
  navigation,
  options: {
    headerLeft: renderButton,
    headerRight: renderAnotherButton,
  },
});
```

**Route enums:**
```typescript
export enum MyStackRoutes {
  ScreenOne = 'ScreenOne',
  ScreenTwo = 'ScreenTwo',
}
```

**Navigate with params:**
```typescript
navigation.navigate(MyStackRoutes.ScreenTwo, {
  id: '123',
  source: 'list',
});
```

**Access params:**
```typescript
const MyScreen = ({
  route: { params: { id, source } },
}: MyStackNavigationProp<MyStackRoutes.ScreenTwo>) => {
  // Use id, source
};
```

**Go back:**
```typescript
const handleClose = useCallback(() => {
  navigation.goBack();
}, [navigation]);
```

**Key Libraries:**
- React Navigation 7.0.13
- React Native 0.75.4
- @zest/react-native 1.3.1

For production examples, see [references/examples.md](references/examples.md).
