---
name: component-patterns
description: "WHAT: React Native component patterns with variant-based architecture and repository pattern. WHEN: creating components, implementing variants, separating data logic from UI. KEYWORDS: component, variant, discriminated union, repository, FlatList, useCallback, memo, JSX, props."

tracked_repositories:
  - url: https://github.com/facebook/react-native-website
    type: external
    paths:
      - docs/**/*.md
    last_synced: 2024-01-01T00:00:00Z
    sync_frequency: monthly
---

# Component Patterns for React Native

## Core Principles

**Use TypeScript strict mode, arrow functions, and named exports only.** Structure components with variant-based architecture using discriminated unions and repository pattern for data logic.

**Why**: Consistent patterns improve code maintainability, type safety catches bugs at compile time, and established architectures make components predictable and testable.

## When to Use This Skill

Use these patterns when:

- Creating any React Native component
- Implementing variant-based components (different modes/states)
- Separating data logic from UI rendering
- Formatting JSX for readability
- Rendering conditional UI elements
- Displaying lists of data efficiently
- Handling user interactions and events
- Optimizing component performance

## Component Structure

### Basic Component Pattern

```typescript
import { View, TouchableOpacity } from 'react-native';
import { Text, useZestStyles } from '@zest/react-native';

import type { ComponentProps } from './types';
import { stylesConfig } from './styles';

export const ExampleComponent = ({
  title,
  onPress,
  variant = 'primary',
}: ComponentProps) => {
  const styles = useZestStyles(stylesConfig);

  return (
    <View style={styles.container}>
      <Text type="headline-lg">{title}</Text>
      <TouchableOpacity style={styles.button} onPress={onPress}>
        <Text type="body-md-bold">Press Me</Text>
      </TouchableOpacity>
    </View>
  );
};
```

**Structure order:**
1. Imports (React/RN → External → Zest → Types → Internal → Relative)
2. Props destructuring with defaults
3. Hooks (styles, state, effects)
4. Event handlers
5. Helper functions
6. Render logic

**Why**: Consistent structure makes components easy to navigate and understand.

## Variant-Based Component Architecture

Use discriminated unions for components with different modes or states:

```typescript
// types.ts
export type EditCardVariant = {
  variant: 'EDIT';
  product: Product;
  quantity: number;
  maxQuantity: number;
  onQuantityChange: (qty: number) => void;
};

export type SkippedCardVariant = {
  variant: 'SKIPPED';
  product: Product;
  reason: string;
  onUnskip: () => void;
};

export type LoadingCardVariant = {
  variant: 'LOADING';
  productId: string;
};

export type CardVariant =
  | EditCardVariant
  | SkippedCardVariant
  | LoadingCardVariant;

export type ProductCardProps = {
  data: CardVariant;
  brandCategory: string;
};
```

**Component implementation with exhaustive checking:**

```typescript
import { assertNever } from '@libs/utils';

export const ProductCard = ({ data, brandCategory }: ProductCardProps) => {
  const renderCardVariant = () => {
    switch (data.variant) {
      case 'EDIT':
        return (
          <EditCard
            product={data.product}
            quantity={data.quantity}
            maxQuantity={data.maxQuantity}
            onQuantityChange={data.onQuantityChange}
            brandCategory={brandCategory}
          />
        );
      case 'SKIPPED':
        return (
          <SkippedCard
            product={data.product}
            reason={data.reason}
            onUnskip={data.onUnskip}
            brandCategory={brandCategory}
          />
        );
      case 'LOADING':
        return <LoadingCard productId={data.productId} />;
      default:
        return assertNever(data);
    }
  };

  return <View>{renderCardVariant()}</View>;
};
```

**Why**:
- **Type safety**: TypeScript ensures all variants are handled
- **Exhaustive checking**: `assertNever` catches missing cases at compile time
- **Maintainability**: Adding new variants requires updating all switch statements
- **Clear intent**: Each variant has specific, type-safe props

**Usage**: 50+ instances in YourCompany codebase for cards, screens, and modal states.

## Repository Pattern for Data Logic

Separate data fetching and transformation from UI components:

```typescript
// hooks/useDeliveryFeedItemRepository.tsx
import { useQuery } from '@tanstack/react-query';

export const useDeliveryFeedItemRepository = ({ delivery }: { delivery: Delivery }) => {
  const { data: benefitUnits } = useBenefitUnitsQuery(delivery.id);
  const { data: addOns } = useAddOnsQuery(delivery.id);

  // Computed properties
  const hasBenefitUnits = benefitUnits && benefitUnits.length > 0;
  const isSkippedStatus = delivery.state === 'SKIPPED';
  const deliverySizeMeals = delivery.config?.numberOfRecipes || 0;

  // Complex data transformation
  const meals = delivery.items
    .filter((item) => item.type === 'MEAL')
    .map((item) => ({
      id: item.id,
      name: item.product.name,
      imageUrl: item.product.imageUrl,
      servings: item.quantity,
    }));

  const totalItems = meals.length + (addOns?.length || 0);

  return {
    hasBenefitUnits,
    isSkippedStatus,
    deliverySizeMeals,
    meals,
    addOns,
    totalItems,
  };
};
```

**Component usage:**

```typescript
export const DeliveryFeedItem = ({ delivery }: Props) => {
  const repository = useDeliveryFeedItemRepository({ delivery });
  const styles = useZestStyles(stylesConfig);

  return (
    <View style={styles.container}>
      <Text type="headline-md">
        {repository.totalItems} items
      </Text>
      {repository.hasBenefitUnits && <BenefitBadge />}
      {repository.isSkippedStatus && <SkippedBanner />}
      <MealList meals={repository.meals} />
    </View>
  );
};
```

**Why**:
- **Separation of concerns**: Data logic separate from UI
- **Reusability**: Multiple components can use same repository
- **Testability**: Repository hooks can be tested independently
- **Maintainability**: Data changes don't affect UI structure

**Usage**: 30+ repository hooks in YourCompany codebase for complex data operations.

## JSX Formatting

### Multiple Props

Put each prop on a separate line:

```typescript
// ✅ Good - Readable
<Button
  variant="primary"
  appearance="brand"
  size="lg"
  disabled={isLoading}
  accessibilityLabel="Submit form"
  onPress={handleSubmit}
>
  Submit
</Button>

// ❌ Bad - Hard to read
<Button variant="primary" appearance="brand" size="lg" disabled={isLoading} onPress={handleSubmit}>Submit</Button>
```

### Single Prop

Keep on same line:

```typescript
// ✅ Good
<Text type="headline-lg">Title</Text>
<Icon icon="CloseOutline24" altText="Close" />

// ❌ Bad - Unnecessary line breaks for single prop
<Text
  type="headline-lg"
>
  Title
</Text>
```

### Boolean Props

Always explicit:

```typescript
// ✅ Good - Explicit
<Button enabled={true} loading={false} />
<Input required={true} disabled={false} />

// ❌ Bad - Implicit (avoid)
<Button enabled loading />
```

**Why**: Explicit formatting improves readability and prevents ambiguity.

## Conditional Rendering

### Ternary for Inline Conditions

```typescript
// ✅ Good - Clear ternary
{isLoading ? <LoadingSpinner /> : <Content data={data} />}

// ✅ Good - With null
{hasData ? <DataDisplay data={data} /> : null}
```

### Logical AND for Show/Hide

```typescript
// ✅ Good - Simple show/hide
{hasData && <DataDisplay data={data} />}
{isError && <ErrorMessage error={error} />}
{items.length > 0 && <ItemList items={items} />}
```

### Early Returns for Complex Conditions

```typescript
export const UserProfile = ({ user }: Props) => {
  // ✅ Good - Early returns
  if (!user) {
    return <EmptyState message="No user found" />;
  }

  if (user.isBlocked) {
    return <BlockedUserMessage />;
  }

  if (!user.profile) {
    return <IncompleteProfileWarning />;
  }

  // Main render
  return (
    <View>
      <ProfileHeader user={user} />
      <ProfileContent profile={user.profile} />
    </View>
  );
};
```

### Avoid Nested Ternaries

```typescript
// ❌ Bad - Nested ternaries
{isLoading ? (
  <LoadingSpinner />
) : isError ? (
  <ErrorMessage />
) : hasData ? (
  <Content />
) : (
  <EmptyState />
)}

// ✅ Good - Extract to function
const renderContent = () => {
  if (isLoading) return <LoadingSpinner />;
  if (isError) return <ErrorMessage />;
  if (hasData) return <Content />;
  return <EmptyState />;
};

return <View>{renderContent()}</View>;
```

**Why**: Simple patterns are easier to read, maintain, and debug.

## List Rendering

### Use FlatList for Performance

```typescript
import { FlatList } from 'react-native';

const ITEM_HEIGHT = 100;

export const RecipeList = ({ recipes }: Props) => {
  return (
    <FlatList
      data={recipes}
      keyExtractor={(item) => item.id}
      renderItem={({ item, index }) => (
        <RecipeCard
          recipe={item}
          index={index}
          testID={`recipe-card-${item.id}`}
        />
      )}
      getItemLayout={(data, index) => ({
        length: ITEM_HEIGHT,
        offset: ITEM_HEIGHT * index,
        index,
      })}
      initialNumToRender={10}
      maxToRenderPerBatch={5}
      windowSize={5}
    />
  );
};
```

**Performance optimizations:**
- `keyExtractor`: Stable unique keys (use IDs, never index)
- `getItemLayout`: Skip height measurements for fixed-height items
- `initialNumToRender`: Render minimum items on mount
- `maxToRenderPerBatch`: Render fewer items per scroll batch
- `windowSize`: Keep smaller render window

**Why**: FlatList virtualizes items, only rendering what's visible for optimal performance with large lists.

### Never Use Index as Key

```typescript
// ❌ Bad - Index as key
{items.map((item, index) => (
  <ItemCard key={index} item={item} />
))}

// ✅ Good - Unique ID as key
{items.map((item) => (
  <ItemCard key={item.id} item={item} />
))}

// ✅ Good - Composite key if no ID
{items.map((item) => (
  <ItemCard key={`${item.name}-${item.timestamp}`} item={item} />
))}
```

**Why**: Index keys cause React to incorrectly reuse components when list order changes, leading to bugs with component state and animations.

### Memoize renderItem

```typescript
import { useCallback } from 'react';

export const RecipeList = ({ recipes, onSelect }: Props) => {
  const renderItem = useCallback(
    ({ item }: { item: Recipe }) => (
      <RecipeCard recipe={item} onSelect={onSelect} />
    ),
    [onSelect]
  );

  return (
    <FlatList
      data={recipes}
      keyExtractor={(item) => item.id}
      renderItem={renderItem}
    />
  );
};
```

**Why**: Memoized `renderItem` prevents FlatList from re-rendering all items when parent re-renders.

## Event Handling

### useCallback for Event Handlers

```typescript
import { useCallback } from 'react';

export const ProductCard = ({ product, onSelect }: Props) => {
  const handlePress = useCallback(() => {
    onSelect(product.id);
  }, [onSelect, product.id]);

  const handleAddToCart = useCallback(() => {
    addToCart(product);
    trackEvent('add_to_cart', { productId: product.id });
  }, [product]);

  return (
    <View>
      <TouchableOpacity onPress={handlePress}>
        <ProductImage source={product.imageUrl} />
      </TouchableOpacity>
      <Button onPress={handleAddToCart}>Add to Cart</Button>
    </View>
  );
};
```

**Why**: `useCallback` prevents creating new function instances on every render, avoiding unnecessary child re-renders.

### Inline Handlers for Simple Cases

```typescript
// ✅ Good - Simple inline handler
<Button onPress={() => setIsVisible(false)}>Close</Button>
<TouchableOpacity onPress={() => navigation.goBack()}>
  <Icon icon="ChevronLeftOutline24" altText="Back" />
</TouchableOpacity>

// ❌ Bad - Complex inline handler
<Button onPress={() => {
  validateInput();
  processData();
  updateState();
  trackEvent();
}}>
  Process
</Button>

// ✅ Good - Extract complex handler
const handleProcess = useCallback(() => {
  validateInput();
  processData();
  updateState();
  trackEvent();
}, [validateInput, processData, updateState, trackEvent]);

<Button onPress={handleProcess}>Process</Button>
```

**Rule**: Use inline handlers for single-line actions, `useCallback` for multi-line or repeated handlers.

### Action Handlers with Discriminated Unions

```typescript
import { assertNever } from '@libs/utils';

type ProductAction =
  | { type: 'ADD'; productId: string; isAlcoholic?: boolean }
  | { type: 'DECREASE_QUANTITY'; productId: string }
  | { type: 'INCREASE_QUANTITY'; productId: string }
  | { type: 'CARD_CLICKED'; productId: string; position?: number };

export const createHandleAction = ({
  onAddProduct,
  onDecreaseProduct,
  onIncreaseProduct,
  navigateToProductDetails,
}: Handlers) => {
  return (action: ProductAction) => {
    switch (action.type) {
      case 'ADD':
        onAddProduct(action.productId, action.isAlcoholic);
        break;
      case 'DECREASE_QUANTITY':
        onDecreaseProduct(action.productId);
        break;
      case 'INCREASE_QUANTITY':
        onIncreaseProduct(action.productId);
        break;
      case 'CARD_CLICKED':
        navigateToProductDetails(action.productId, action.position);
        break;
      default:
        assertNever(action);
    }
  };
};
```

**Why**: Action handlers with discriminated unions provide type-safe event handling with exhaustive case checking.

## Performance Patterns

### Component Memoization

```typescript
import { memo } from 'react';

// ✅ Memo for expensive components
export const RecipeCard = memo(({ recipe, onSelect }: RecipeCardProps) => {
  return (
    <View>
      <Image source={{ uri: recipe.imageUrl }} />
      <Text>{recipe.name}</Text>
      <Button onPress={() => onSelect(recipe.id)}>Select</Button>
    </View>
  );
});

RecipeCard.displayName = 'RecipeCard';
```

**When to use memo:**
- Component in a large list
- Component with expensive rendering logic
- Component receives same props frequently
- Parent re-renders often but props rarely change

**Why**: `memo` prevents re-renders when props haven't changed, improving performance for lists and frequently updated parents.

### useMemo for Expensive Calculations

```typescript
import { useMemo } from 'react';

export const RecipeList = ({ recipes, filters }: Props) => {
  const filteredRecipes = useMemo(() => {
    return recipes
      .filter((recipe) => matchesFilters(recipe, filters))
      .sort((a, b) => a.rating - b.rating)
      .slice(0, 20);
  }, [recipes, filters]);

  return (
    <FlatList
      data={filteredRecipes}
      renderItem={renderRecipe}
    />
  );
};
```

**Why**: `useMemo` caches expensive calculations, only recomputing when dependencies change.

### Cleanup & Memory Management

```typescript
import { useEffect } from 'react';

export const RealTimeUpdates = () => {
  useEffect(() => {
    // ✅ Good - Setup subscription
    const subscription = subscribeToUpdates((data) => {
      handleUpdate(data);
    });

    // ✅ Good - Cleanup function
    return () => {
      subscription.unsubscribe();
    };
  }, []);

  useEffect(() => {
    // ✅ Good - Setup interval
    const interval = setInterval(() => {
      fetchLatestData();
    }, 30000);

    // ✅ Good - Cleanup interval
    return () => {
      clearInterval(interval);
    };
  }, []);

  return <View>{/* ... */}</View>;
};
```

**Why**: Proper cleanup prevents memory leaks, event listener buildup, and subscription issues.

## Common Mistakes to Avoid

❌ **Don't use HTML elements**:

```typescript
// ❌ Bad - HTML elements don't work in React Native
<div>Content</div>
<span>Text</span>
<img src="..." />

// ✅ Good - React Native components
<View>Content</View>
<Text>Text</Text>
<Image source={{ uri: '...' }} />
```

❌ **Don't use default exports**:

```typescript
// ❌ Bad
export default UserProfile;

// ✅ Good
export const UserProfile = ({ user }: Props) => {};
```

❌ **Don't use function declarations**:

```typescript
// ❌ Bad
function calculateTotal(items: Item[]) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// ✅ Good
const calculateTotal = (items: Item[]): number => {
  return items.reduce((sum, item) => sum + item.price, 0);
};
```

❌ **Don't use var**:

```typescript
// ❌ Bad
var count = 0;
var config = {};

// ✅ Good
let count = 0;
const config = {};
```

❌ **Don't create new objects/functions in render**:

```typescript
// ❌ Bad - Creates new style object every render
<View style={{ padding: 16, backgroundColor: 'white' }} />

// ✅ Good - Use extracted styles
const styles = useZestStyles(stylesConfig);
<View style={styles.container} />

// ❌ Bad - Creates new function every render
<Button onPress={() => handlePress(item.id)} />

// ✅ Good - Use useCallback
const handlePress = useCallback(() => {
  onSelect(item.id);
}, [item.id, onSelect]);
<Button onPress={handlePress} />
```

✅ **Do use TypeScript strict mode**:

```typescript
// ✅ Good - Explicit types
const processUser = (user: User): ProcessedUser => {
  return { ...user, processed: true };
};

// ❌ Bad - any types
const processUser = (user: any): any => {
  return { ...user, processed: true };
};
```

✅ **Do use repository pattern for complex data**:

```typescript
// ✅ Good - Separated concerns
const repository = useDataRepository({ id });
return <Component data={repository.transformedData} />;

// ❌ Bad - Data logic in component
const Component = ({ id }) => {
  const { data } = useQuery(...);
  const transformed = complexTransformation(data); // Move to repository
  return <View>{transformed}</View>;
};
```

✅ **Do use discriminated unions for variants**:

```typescript
// ✅ Good - Type-safe variants
type CardVariant =
  | { variant: 'EDIT'; quantity: number }
  | { variant: 'LOADING' };

const renderCard = (data: CardVariant) => {
  switch (data.variant) {
    case 'EDIT': return <EditCard quantity={data.quantity} />;
    case 'LOADING': return <LoadingCard />;
    default: return assertNever(data);
  }
};
```

## Quick Reference

**Component Structure:**
1. Imports (React/RN → External → Zest → Types → Internal → Relative)
2. Props destructuring with defaults
3. Hooks
4. Event handlers
5. Helper functions
6. Render logic

**Variant Architecture:**
- Use discriminated unions for different component modes
- Use `assertNever` for exhaustive case checking
- TypeScript ensures all variants are handled

**Repository Pattern:**
- Separate data fetching/transformation from UI
- Create custom hooks for complex data operations
- Return transformed, ready-to-use data

**JSX Formatting:**
- Multiple props: Each on separate line
- Single prop: Same line
- Boolean props: Always explicit

**Conditional Rendering:**
- Ternary: Inline conditions
- Logical AND: Show/hide
- Early returns: Complex conditions
- Avoid: Nested ternaries

**List Rendering:**
- Use `FlatList` for performance
- Unique ID as `key`, never index
- Memoize `renderItem`
- Use `getItemLayout` for fixed heights

**Event Handling:**
- `useCallback` for complex/repeated handlers
- Inline for simple single-line actions
- Action handlers with discriminated unions

**Performance:**
- `memo` for expensive components
- `useMemo` for expensive calculations
- Always cleanup in `useEffect`

**Key Rules:**
- ✅ Arrow functions only
- ✅ Named exports only
- ✅ TypeScript strict mode
- ✅ const/let, never var
- ❌ Never use HTML elements
- ❌ Never use default exports
- ❌ Never create objects/functions in render

For production examples, see [references/examples.md](references/examples.md).
