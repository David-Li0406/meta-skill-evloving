---
name: test-ids
description: "WHAT: Test ID constants with hierarchical naming for React Native automated testing. WHEN: unit tests with Testing Library, E2E tests with Maestro, testing interactive elements. KEYWORDS: testID, TEST_IDS, constants, hierarchical naming, feature-component-element, Maestro, accessibility, getByTestId."
---

# Test ID Patterns for React Native

## Core Principles

**Define test IDs as constants grouped by feature.** Use descriptive, hierarchical naming that prevents collisions and makes test IDs easy to find.

**Why**: Consistent test IDs enable reliable automated testing, prevent duplication, and allow refactoring test IDs from a single location.

## When to Use This Skill

Use test IDs when:

- Writing unit tests with React Native Testing Library
- Creating E2E tests with Maestro
- Testing user interactions (buttons, inputs, navigation)
- Testing dynamic lists and modals
- Ensuring components are testable

## Feature-Level Organization

Define test IDs in feature constants file:

```typescript
// features/reactivation-banner-feature/constants.ts

export const TEST_IDS = {
  // Banner components
  EXPANDED_BANNER: 'reactivation-banner-expanded',
  COLLAPSED_BANNER: 'reactivation-banner-collapsed',
  BANNER_TITLE: 'reactivation-banner-title',
  BANNER_DESCRIPTION: 'reactivation-banner-description',

  // Interactive elements
  CLOSE_BUTTON: 'reactivation-banner-close',
  REACTIVATE_BUTTON: 'reactivation-banner-reactivate',

  // Plan display
  PLAN_CONTAINER: 'reactivation-banner-plan-container',
  PLAN_PRICE: 'reactivation-banner-plan-price',

  // Dialogs
  DISCOUNT_ERROR_DIALOG: 'discount-error-dialog',
  DISCOUNT_ERROR_DIALOG_ICON: 'discount-error-dialog-icon',
  DISCOUNT_ERROR_DIALOG_PRIMARY_BUTTON: 'discount-error-dialog-primary-button',
} as const;
```

**Why**: Grouping by feature prevents duplication and improves organization.

## Naming Conventions

Use hierarchical naming: **feature-component-element-variant**

```typescript
export const TEST_IDS = {
  // ✅ Good: Hierarchical and descriptive
  RECIPE_LIST_SCREEN: 'recipe-list-screen',
  RECIPE_LIST_FILTER: 'recipe-list-filter',
  RECIPE_LIST_FILTER_BUTTON: 'recipe-list-filter-button',
  RECIPE_LIST_EMPTY_STATE: 'recipe-list-empty-state',

  RECIPE_CARD_CONTAINER: 'recipe-card-container',
  RECIPE_CARD_IMAGE: 'recipe-card-image',
  RECIPE_CARD_TITLE: 'recipe-card-title',
  RECIPE_CARD_ADD_BUTTON: 'recipe-card-add-button',

  // ❌ Bad: Unclear hierarchy
  SCREEN: 'screen',
  FILTER: 'filter',
  BUTTON: 'button',
};
```

**Why**: Hierarchical naming makes test IDs easy to find and prevents collisions.

## Using Test IDs in Components

Apply test IDs using constants:

```typescript
import { TEST_IDS } from '../../constants';

export const ReactivationBanner = () => {
  return (
    <View testID={TEST_IDS.EXPANDED_BANNER}>
      <Text testID={TEST_IDS.BANNER_TITLE}>Welcome Back!</Text>
      <Text testID={TEST_IDS.BANNER_DESCRIPTION}>
        Reactivate your subscription with a special discount.
      </Text>
      <Button testID={TEST_IDS.REACTIVATE_BUTTON} onPress={handleReactivate}>
        Reactivate Now
      </Button>
      <TouchableOpacity testID={TEST_IDS.CLOSE_BUTTON} onPress={handleClose}>
        <Icon icon="CloseOutline24" />
      </TouchableOpacity>
    </View>
  );
};
```

**Why**: Constants prevent typos and enable refactoring from one location.

## Using Test IDs in Tests

Reference test IDs using constants:

```typescript
import { TEST_IDS } from '../constants';

test('renders reactivation banner', () => {
  render(<ReactivationBanner />);

  expect(screen.getByTestId(TEST_IDS.EXPANDED_BANNER)).toBeTruthy();
  expect(screen.getByTestId(TEST_IDS.BANNER_TITLE)).toHaveTextContent(
    'Welcome Back!'
  );
});

test('calls onReactivate when button pressed', () => {
  const mockOnReactivate = jest.fn();

  render(<ReactivationBanner onReactivate={mockOnReactivate} />);

  fireEvent.press(screen.getByTestId(TEST_IDS.REACTIVATE_BUTTON));

  expect(mockOnReactivate).toHaveBeenCalled();
});
```

**Why**: Test ID constants keep tests and implementation in sync.

## Dialog and Modal Test IDs

Include component name in dialog test IDs:

```typescript
export const TEST_IDS = {
  // Dialog container
  DISCOUNT_ERROR_DIALOG: 'discount-error-dialog',

  // Dialog elements
  DISCOUNT_ERROR_DIALOG_ICON: 'discount-error-dialog-icon',
  DISCOUNT_ERROR_DIALOG_TITLE: 'discount-error-dialog-title',
  DISCOUNT_ERROR_DIALOG_MESSAGE: 'discount-error-dialog-message',

  // Dialog buttons
  DISCOUNT_ERROR_DIALOG_PRIMARY_BUTTON: 'discount-error-dialog-primary-button',
  DISCOUNT_ERROR_DIALOG_SECONDARY_BUTTON: 'discount-error-dialog-secondary-button',
};
```

Usage:

```typescript
<Dialog
  testID={TEST_IDS.DISCOUNT_ERROR_DIALOG}
  title={title}
  description={message}
  asset={<Icon testID={TEST_IDS.DISCOUNT_ERROR_DIALOG_ICON} icon="ErrorOutline24" />}
  buttons={[
    {
      title: 'Okay',
      onPress: onDismiss,
      testID: TEST_IDS.DISCOUNT_ERROR_DIALOG_PRIMARY_BUTTON,
    },
  ]}
/>
```

**Why**: Component-specific IDs prevent collisions when multiple dialogs exist.

## Dynamic Test IDs for Lists

Combine constant prefix with dynamic data:

```typescript
// Constants
export const TEST_IDS = {
  RECIPE_LIST: 'recipe-list',
  RECIPE_CARD_PREFIX: 'recipe-card',
};

// Component
const RecipeList = ({ recipes }) => {
  return (
    <FlatList
      testID={TEST_IDS.RECIPE_LIST}
      data={recipes}
      renderItem={({ item }) => (
        <RecipeCard
          recipe={item}
          testID={`${TEST_IDS.RECIPE_CARD_PREFIX}-${item.id}`}
        />
      )}
    />
  );
};

// Test
test('renders all recipe cards', () => {
  const recipes = [
    { id: '1', name: 'Recipe 1' },
    { id: '2', name: 'Recipe 2' },
  ];

  render(<RecipeList recipes={recipes} />);

  expect(screen.getByTestId(`${TEST_IDS.RECIPE_CARD_PREFIX}-1`)).toBeTruthy();
  expect(screen.getByTestId(`${TEST_IDS.RECIPE_CARD_PREFIX}-2`)).toBeTruthy();
});
```

**Why**: Dynamic IDs enable testing individual list items.

## Test by User Behavior

Use test IDs to test user interactions, not implementation details:

```typescript
test('user can add recipe to cart', () => {
  render(<RecipeDetailsScreen recipeId="123" />);

  // Find by test ID
  const addButton = screen.getByTestId(TEST_IDS.ADD_TO_CART_BUTTON);

  // Simulate user action
  fireEvent.press(addButton);

  // Verify outcome
  expect(screen.getByTestId(TEST_IDS.SUCCESS_MESSAGE)).toBeTruthy();
});
```

**Why**: Testing user behavior makes tests resilient to implementation changes.

## Accessibility Labels vs Test IDs

Provide both `testID` and `accessibilityLabel`:

```typescript
<Button
  testID={TEST_IDS.ADD_TO_CART_BUTTON}
  accessibilityLabel={translateRaw('recipe.action.add_to_cart')}
  accessibilityRole="button"
  onPress={handleAddToCart}
>
  Add to Cart
</Button>
```

**Why**:
- `testID` is for automated testing
- `accessibilityLabel` is for screen readers
- Both serve different but important purposes

## E2E Testing with Maestro

Use same test IDs for Maestro E2E tests:

```yaml
# maestro-flow.yaml
appId: com.yourcompany.app
---
- launchApp
- assertVisible:
    id: 'recipe-list-screen'
- tapOn:
    id: 'recipe-card-1'
- assertVisible:
    id: 'recipe-details-screen'
- tapOn:
    id: 'add-to-cart-button'
- assertVisible:
    id: 'success-toast'
```

**Why**: Consistent test IDs enable both unit and E2E testing with same identifiers.

## Documentation

Add comments explaining test ID groups:

```typescript
export const TEST_IDS = {
  // Main banner components
  EXPANDED_BANNER: 'reactivation-banner-expanded',
  COLLAPSED_BANNER: 'reactivation-banner-collapsed',

  // User actions
  REACTIVATE_BUTTON: 'reactivation-banner-reactivate',
  DISMISS_BUTTON: 'reactivation-banner-dismiss',

  // Error states
  ERROR_DIALOG: 'reactivation-error-dialog',
  ERROR_MESSAGE: 'reactivation-error-message',
} as const;
```

**Why**: Comments help developers understand test ID organization.

## Common Mistakes to Avoid

❌ **Don't hardcode test IDs**:

```typescript
<View testID="banner"> {/* Hardcoded string */}
  <Text testID="title">Title</Text>
</View>
```

❌ **Don't use generic names**:

```typescript
export const TEST_IDS = {
  BUTTON: 'button', // Too generic
  CONTAINER: 'container', // Too generic
  TEXT: 'text', // Too generic
};
```

❌ **Don't skip test IDs on interactive elements**:

```typescript
<TouchableOpacity onPress={handlePress}>
  {/* Missing testID - hard to test */}
  <Text>Press Me</Text>
</TouchableOpacity>
```

✅ **Do use constants with hierarchical naming**:

```typescript
export const TEST_IDS = {
  REACTIVATION_BANNER_CONTAINER: 'reactivation-banner-container',
  REACTIVATION_BANNER_TITLE: 'reactivation-banner-title',
  REACTIVATION_BANNER_CLOSE_BUTTON: 'reactivation-banner-close-button',
} as const;

<View testID={TEST_IDS.REACTIVATION_BANNER_CONTAINER}>
  <Text testID={TEST_IDS.REACTIVATION_BANNER_TITLE}>Title</Text>
  <TouchableOpacity testID={TEST_IDS.REACTIVATION_BANNER_CLOSE_BUTTON}>
    <Icon icon="CloseOutline24" />
  </TouchableOpacity>
</View>
```

## Quick Reference

**Naming Pattern**: `feature-component-element-variant`

**Organization**: Group by feature in `constants.ts`

**Format**: Use `as const` for TypeScript type safety

**Interactive Elements**: Always add test IDs to buttons, inputs, touchables

**Lists**: Use prefix + dynamic ID pattern

**Dialogs**: Include component name in ID

**E2E**: Same test IDs work for Maestro tests

**Accessibility**: Provide both `testID` and `accessibilityLabel`

For production examples, see [references/examples.md](references/examples.md).
