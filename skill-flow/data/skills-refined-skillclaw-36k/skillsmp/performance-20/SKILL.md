---
name: performance
description: "WHAT: Performance optimization with memoization, React.memo, and FlatList techniques. WHEN: profiler shows slow renders, preventing re-renders, optimizing list performance. KEYWORDS: performance, useMemo, useCallback, React.memo, FlatList, getItemLayout, optimization, profile, windowSize."
---

# Performance Optimization Patterns

## Core Principles

**Optimize strategically, not prematurely.** Use React Profiler to identify bottlenecks, then apply targeted optimizations with useRef, useMemo, useCallback, React.memo, and FlatList optimization techniques.

**Why**: Strategic optimization prevents unnecessary complexity while addressing real performance issues. Measure first, optimize second.

## When to Use This Skill

Use performance optimization when:

- Profiler shows slow renders (>16ms)
- Components re-render unnecessarily
- Expensive computations run on every render
- List rendering causes lag
- Tracking values across renders without triggering updates
- Preventing callback recreation
- Need to preserve referential equality

**Don't optimize prematurely**: Write clean code first, profile to find bottlenecks, then optimize strategically.

## useRef: Tracking Without Re-renders

### Track Values Across Renders

Use useRef to store values that persist across renders without triggering re-renders.

```typescript
import { useRef, useEffect } from 'react';

const MyComponent = () => {
  // Track processing flag
  const hasProcessedInitialLoad = useRef(false);
  const lastProcessedCount = useRef(0);

  useEffect(() => {
    const shouldProcess =
      !isLoadingSharedUrls &&
      hasSharedUrls &&
      (!hasProcessedInitialLoad.current ||
        sharedUrls.length > lastProcessedCount.current);

    if (shouldProcess) {
      hasProcessedInitialLoad.current = true;
      lastProcessedCount.current = sharedUrls.length;
      processSharedUrls(sharedUrls);
    }
  }, [isLoadingSharedUrls, hasSharedUrls, sharedUrls]);
};
```

**Why**: useRef provides mutable storage without triggering re-renders. Perfect for flags, counters, and tracking state.

**Production Example**: `git-resources/shared-mobile-modules/src/operations/meal-selection-listener/useMealSelectionListener.ts:64`

### Store Previous Values

Track previous values for comparison logic.

```typescript
const MyComponent = ({ selection }) => {
  // Store the last successful selection state for reversion on error
  const lastSuccessfulSelectionRef = useRef<CartFragmentFragment | undefined>(
    undefined
  );

  // Track the previous selection to use as fallback
  const previousSelectionRef = useRef<CartFragmentFragment | undefined>(
    undefined
  );

  // Track previous selection before current selection changes
  useEffect(() => {
    if (selection) {
      // Initialize lastSuccessfulSelectionRef with current selection on first mount
      if (!lastSuccessfulSelectionRef.current) {
        lastSuccessfulSelectionRef.current = selection;
      }

      // Store the previous selection as the last successful one before it changes
      if (previousSelectionRef.current) {
        lastSuccessfulSelectionRef.current = previousSelectionRef.current;
      }
      // Update the previous selection ref
      previousSelectionRef.current = selection;
    }
  }, [selection]);
};
```

**Why**: Enables comparison logic, error recovery, and undo functionality without state updates.

**Production Example**: `git-resources/shared-mobile-modules/src/operations/meal-selection-listener/useMealSelectionListener.ts:64`

### Store Component References

Store refs to child components or DOM elements.

```typescript
import { useRef, useEffect } from 'react';
import { FlatList } from 'react-native';

const MyComponent = ({ currentSlideIndex, slides }) => {
  const flatListRef = useRef<FlatList>(null);

  // Scroll to the correct index when currentSlideIndex changes
  useEffect(() => {
    if (
      flatListRef.current &&
      currentSlideIndex >= 0 &&
      currentSlideIndex < slides.length
    ) {
      flatListRef.current.scrollToOffset({
        offset: currentSlideIndex * screenWidth,
        animated: true,
      });
    }
  }, [currentSlideIndex, slides.length]);

  return (
    <FlatList
      ref={flatListRef}
      data={slides}
      renderItem={renderSlide}
      // ...
    />
  );
};
```

**Why**: Access component methods imperatively (e.g., scrollToOffset, focus, measure).

**Production Example**: `git-resources/shared-mobile-modules/src/features/app-onboarding/components/Body.tsx:92`

## useMemo: Expensive Computations

### Memoize Filtered/Sorted Data

Use useMemo to cache expensive filtering or sorting operations.

```typescript
import { useMemo } from 'react';

const useMealSelectionInfo = () => {
  const { config, totalMealKitItemsSize, totalAddonsItemsSize, errors } =
    useMealSelection(/* ... */);

  return useMemo(() => {
    if (!config) {
      return undefined;
    }

    const minMealsSize = config.variations.minMealsSize;
    const maxMealsSize = config.variations.maxMealsSize;

    const isMaxReached =
      maxMealsSize > 0 && maxMealsSize === totalMealKitItemsSize;

    const mealsNeededToReachMinimum = Math.max(
      (minMealsSize ?? 0) - totalMealKitItemsSize,
      0
    );

    const isBelowMinimum = Boolean(
      errors?.some(
        (error) => error.type === UpdateCartErrorType.BelowMinimum
      ) && mealsNeededToReachMinimum > 0
    );

    return {
      isBelowMinimum,
      isMaxReached,
      totalMealKitItemsSize,
      totalAddonsItemsSize,
      minRequiredMealKitItemsSize: config.variations.minMealsSize,
      maxSelectedMealKitItemSize: maxMealsSize,
      mealsNeededToReachMinimum,
    };
  }, [config, totalMealKitItemsSize, totalAddonsItemsSize, errors]);
};
```

**Why**: Prevents recalculating complex derived state on every render. Only recomputes when dependencies change.

**Production Example**: `git-resources/shared-mobile-modules/src/operations/use-selection-info/useMealSelectionInfo.ts:24`

### Memoize Context Values

Use useMemo for context provider values to prevent unnecessary re-renders of consumers.

```typescript
import { useMemo } from 'react';

const MyProvider = ({ children }) => {
  const [state, setState] = useState(initialState);

  const contextValue = useMemo(
    () => ({
      state,
      setState,
      // ... other values
    }),
    [state]
  );

  return (
    <MyContext.Provider value={contextValue}>
      {children}
    </MyContext.Provider>
  );
};
```

**Why**: Context value changes trigger re-renders in all consumers. Memoization prevents unnecessary updates.

### Memoize Transformed Data

Cache data transformations that depend on specific inputs.

```typescript
const useMealSelectionListener = ({ deliveryId }) => {
  const { selection } = useMealSelection(/* ... */);

  const selectionToSave = useMemo(
    () => transformSelectionForSave(selection),
    [selection]
  );

  // Use selectionToSave in mutation
  const [updateCart] = useUpdateCartMutation({
    variables: {
      selectionInput: selectionToSave ?? [],
    },
  });
};
```

**Why**: Expensive transformations only run when input data changes, not on every render.

**Production Example**: `git-resources/shared-mobile-modules/src/operations/meal-selection-listener/useMealSelectionListener.ts:58`

## useCallback: Stable Callbacks

### Memoize Event Handlers

Use useCallback for event handlers passed as props to prevent child re-renders.

```typescript
import { useCallback, useState } from 'react';

const useRefresh = (options: {
  refetchFunctions: Array<() => Promise<unknown>>;
  isRefetching?: boolean;
}) => {
  const { refetchFunctions, isRefetching } = options;
  const [isManualRefreshing, setIsManualRefreshing] = useState(false);

  const isRefreshing = Boolean(isManualRefreshing || isRefetching);

  // Handler to refresh all queries
  const handleRefresh = useCallback(async () => {
    try {
      setIsManualRefreshing(true);

      // Refresh all queries concurrently
      await Promise.all(refetchFunctions.map((fn) => fn()));
    } catch (error) {
      console.error('Error refreshing data:', error);
    } finally {
      setIsManualRefreshing(false);
    }
  }, [refetchFunctions]);

  return {
    isRefreshing,
    handleRefresh,
  };
};
```

**Why**: Stable callback reference prevents unnecessary re-renders when passed to child components.

**Production Example**: `git-resources/shared-mobile-modules/src/operations/refresh/useRefresh.ts:20`

### Memoize Callbacks for Dependencies

Create stable callbacks used in useEffect or other hooks' dependencies.

```typescript
const useMealSelectionListener = ({ deliveryId }) => {
  const handleSelectionUpdate = useCallback(
    (newSelection: CartFragmentFragment, isError?: boolean) => {
      if (isError) {
        overrideSelection(newSelection);
      } else {
        overrideStateFields(newSelection);
      }
      lastSuccessfulSelectionRef.current = newSelection;
    },
    [overrideSelection, overrideStateFields]
  );

  const handleErrorUpdate = useCallback(
    (errors: Parameters<typeof setErrors>[0]) => {
      setErrors(errors);
    },
    [setErrors]
  );

  // Use stable callbacks in useMemo
  const { onCompleted, onError } = useMemo(
    () =>
      createMutationHandlers({
        onSelectionUpdate: handleSelectionUpdate,
        onError: handleErrorUpdate,
        // ...
      }),
    [handleSelectionUpdate, handleErrorUpdate, /* ... */]
  );
};
```

**Why**: Stable callback references prevent dependency arrays from changing unnecessarily.

**Production Example**: `git-resources/shared-mobile-modules/src/operations/meal-selection-listener/useMealSelectionListener.ts:104`

## React.memo: Component Memoization

### Memoize List Items

Use React.memo for expensive list item components to prevent unnecessary re-renders.

```typescript
import React from 'react';

/**
 * ProductListItem renders either a Product card or a Widget container
 * based on the type of item it receives.
 */
export const ProductListItem = React.memo(
  ({
    item,
    variant,
    itemContainerStyle,
    position,
  }: ProductListingComponentProps) => {
    const styles = useZestStyles(stylesConfig);

    if (isWidget(item)) {
      return (
        <View style={[styles.widgetItemWrapper, itemContainerStyle]}>
          <WidgetContainer widget={item} />
        </View>
      );
    }

    const cardVariant = variant(item);
    const enhancedCardVariant = hasActionHandler(cardVariant)
      ? enhanceCardVariantWithPosition(cardVariant, position)
      : cardVariant;

    return (
      <AnalyticsWrapper
        parameters={{
          recipe_position: position,
          ui_element: SOURCE.LIST,
        }}
      >
        <View style={styles.productItemWrapper}>
          <ProductCard data={enhancedCardVariant} />
        </View>
      </AnalyticsWrapper>
    );
  }
);
```

**Why**: List items re-render frequently as user scrolls. Memoization prevents renders when props haven't changed.

**Production Example**: `git-resources/shared-mobile-modules/src/features/product-listing-feature/components/ProductListItem.tsx:61`

### Custom Comparison Function

Provide custom comparison for fine-grained control over re-renders.

```typescript
import React from 'react';

const RecipeCard = React.memo(
  ({ recipe, onPress }) => {
    return (
      <Card onPress={() => onPress(recipe.id)}>
        <Text>{recipe.name}</Text>
        <Text>{recipe.description}</Text>
      </Card>
    );
  },
  (prevProps, nextProps) => {
    // Only re-render if recipe ID or updatedAt changed
    return (
      prevProps.recipe.id === nextProps.recipe.id &&
      prevProps.recipe.updatedAt === nextProps.recipe.updatedAt
    );
  }
);
```

**Why**: Custom comparison ignores irrelevant prop changes (e.g., callback references) while detecting actual data changes.

## FlatList Optimization

### Use getItemLayout for Fixed Heights

Provide getItemLayout for lists with fixed-height items for instant scrolling.

```typescript
import { FlatList } from 'react-native';

const ITEM_HEIGHT = 120;

const MyList = ({ items }) => {
  return (
    <FlatList
      data={items}
      renderItem={({ item }) => <ItemCard item={item} />}
      getItemLayout={(data, index) => ({
        length: ITEM_HEIGHT,
        offset: ITEM_HEIGHT * index,
        index,
      })}
      keyExtractor={(item) => item.id}
    />
  );
};
```

**Why**: getItemLayout enables instant scroll-to-index without measuring, dramatically improving performance for long lists.

**Production Example**: `git-resources/shared-mobile-modules/src/features/app-onboarding/components/Body.tsx:144`

### Adjust Window Size

Control how many items are rendered outside the viewport.

```typescript
<FlatList
  data={items}
  renderItem={renderItem}
  getItemLayout={getItemLayout}
  windowSize={5}                  // Render 5 viewport heights
  maxToRenderPerBatch={10}        // Batch render 10 items at a time
  updateCellsBatchingPeriod={50}  // Wait 50ms between batches
  removeClippedSubviews={true}    // Remove off-screen views (Android)
/>
```

**Why**: Reduces memory usage and improves scrolling performance by limiting rendered items.

### Extract Callbacks from renderItem

Use separate callback functions instead of inline arrow functions in renderItem.

```typescript
// ❌ Wrong - Creates new function on every render
<FlatList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} onPress={handlePress} />}
/>

// ✅ Correct - Stable function reference
const renderItem = ({ item }: { item: Item }) => (
  <ItemCard item={item} onPress={handlePress} />
);

<FlatList
  data={items}
  renderItem={renderItem}
/>
```

**Why**: Stable renderItem reference prevents FlatList from re-creating all list items on parent re-render.

**Production Example**: `git-resources/shared-mobile-modules/src/features/app-onboarding/components/Body.tsx:121`

## Empty Dependency Arrays

### Document Why Dependencies Are Empty

Always document eslint-disable comments for empty dependency arrays.

```typescript
const mergedAttributes = useMemo(() => {
  return {
    ...parentAttributes,
    ...props.attributes,
    squad: props.squad,
  };
}, []); // eslint-disable-line react-hooks/exhaustive-deps
// Attributes should only be set once on mount, not react to prop changes
```

**Why**: Empty arrays are intentional optimization decisions that need explanation for future maintainers.

```typescript
useEffect(() => {
  if (autoStart) {
    startTrace();
  }
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, []); // Only run on mount to start performance trace
```

**Why**: Documents that the effect should only run once, not on every dependency change.

## Performance Measurement

### Use React Profiler

Wrap components with React Profiler to measure render performance.

```typescript
import { Profiler } from 'react';

const onRenderCallback = (
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number
) => {
  if (actualDuration > 16) {
    console.warn(`Slow render in ${id}: ${actualDuration}ms (${phase})`);
  }
};

const App = () => (
  <Profiler id="RecipeList" onRender={onRenderCallback}>
    <RecipeListScreen />
  </Profiler>
);
```

**Why**: Profiler identifies slow components objectively. Only optimize components that actually perform poorly.

### Use __DEV__ Guards

Add development-only performance logging.

```typescript
useEffect(() => {
  if (__DEV__) {
    const start = performance.now();
    processData();
    const end = performance.now();
    console.log(`[PERF] processData took ${(end - start).toFixed(2)}ms`);
  } else {
    processData();
  }
}, [processData]);
```

**Why**: Performance logging in development helps identify bottlenecks without impacting production.

## Common Mistakes to Avoid

❌ **Don't optimize prematurely**:

```typescript
// ❌ Wrong - Unnecessary memoization for simple component
const SimpleText = React.memo(({ text }) => <Text>{text}</Text>);

// ❌ Wrong - Memoizing cheap computation
const doubled = useMemo(() => count * 2, [count]);
```

✅ **Do optimize strategically**:

```typescript
// ✅ Correct - Memoize expensive list item
const RecipeCard = React.memo(ExpensiveRecipeCard);

// ✅ Correct - Memoize expensive filtering
const filteredRecipes = useMemo(() => {
  return recipes.filter(complexFilterLogic);
}, [recipes]);
```

❌ **Don't forget dependencies**:

```typescript
// ❌ Wrong - Missing dependencies causes stale closures
const handleClick = useCallback(() => {
  console.log(userId); // Uses stale userId
}, []); // Missing userId dependency

// ❌ Wrong - Missing dependencies in useMemo
const total = useMemo(() => {
  return price * quantity; // Uses stale values
}, []); // Missing price, quantity
```

✅ **Do include all dependencies**:

```typescript
// ✅ Correct - All dependencies included
const handleClick = useCallback(() => {
  console.log(userId);
}, [userId]);

// ✅ Correct - Dependencies match usage
const total = useMemo(() => {
  return price * quantity;
}, [price, quantity]);
```

❌ **Don't use React.memo without reason**:

```typescript
// ❌ Wrong - Wrapping everything in React.memo
const Button = React.memo(SimpleButton);
const Text = React.memo(SimpleText);
const Icon = React.memo(SimpleIcon);

// No performance benefit if these components re-render infrequently
```

✅ **Do use React.memo for expensive components**:

```typescript
// ✅ Correct - Expensive list items
const ProductCard = React.memo(ExpensiveProductCard);

// ✅ Correct - Custom comparison for deep props
const RecipeCard = React.memo(
  ExpensiveRecipeCard,
  (prev, next) => prev.recipe.id === next.recipe.id
);
```

❌ **Don't create new objects in dependencies**:

```typescript
// ❌ Wrong - New object on every render
const filteredData = useMemo(() => {
  return filterData(data, { status: 'active' }); // New object
}, [data, { status: 'active' }]); // Dependency changes every render!
```

✅ **Do use stable references**:

```typescript
// ✅ Correct - Stable primitive dependency
const STATUS = 'active';
const filteredData = useMemo(() => {
  return filterData(data, { status: STATUS });
}, [data, STATUS]);

// ✅ Correct - Memoize config object separately
const filterConfig = useMemo(() => ({ status: 'active' }), []);
const filteredData = useMemo(() => {
  return filterData(data, filterConfig);
}, [data, filterConfig]);
```

❌ **Don't miss getItemLayout for lists**:

```typescript
// ❌ Wrong - Missing getItemLayout for fixed-height items
<FlatList
  data={items}
  renderItem={renderItem}
  // Missing getItemLayout - slow scrolling
/>
```

✅ **Do provide getItemLayout**:

```typescript
// ✅ Correct - Fast scrolling with getItemLayout
const ITEM_HEIGHT = 100;

<FlatList
  data={items}
  renderItem={renderItem}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

## Quick Reference

**useRef patterns:**
```typescript
const flagRef = useRef(false);            // Tracking flag
const previousValueRef = useRef(value);   // Previous value
const componentRef = useRef<FlatList>(null); // Component ref
```

**useMemo patterns:**
```typescript
const filtered = useMemo(() => filter(data), [data]);
const contextValue = useMemo(() => ({ state }), [state]);
const transformed = useMemo(() => transform(input), [input]);
```

**useCallback patterns:**
```typescript
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

const handleRefresh = useCallback(async () => {
  await refetch();
}, [refetch]);
```

**React.memo patterns:**
```typescript
const ListItem = React.memo(ExpensiveItem);

const Card = React.memo(
  CardComponent,
  (prev, next) => prev.id === next.id
);
```

**FlatList optimization:**
```typescript
<FlatList
  data={items}
  renderItem={renderItem}
  getItemLayout={(_, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
  windowSize={5}
  maxToRenderPerBatch={10}
/>
```

**Empty dependency documentation:**
```typescript
}, []); // eslint-disable-line react-hooks/exhaustive-deps
// Reason: Should only run on mount
```

**Strategy:**
1. Write clean code first
2. Profile to find bottlenecks (React Profiler)
3. Optimize strategically
4. Measure improvement
5. Document decisions

**Key Libraries:**
- React Native 0.75.4
- TypeScript 5.1.6

For production examples, see [references/examples.md](references/examples.md).
