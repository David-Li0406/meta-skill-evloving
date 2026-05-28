---
name: hooks-patterns
description: "WHAT: React hooks patterns for state, effects, memoization, and custom hooks. WHEN: managing state, side effects, expensive calculations, stable callbacks. KEYWORDS: hooks, useState, useEffect, useMemo, useCallback, useRef, cleanup, dependencies, custom hooks."
---

# Hooks Patterns for React Native

## Core Principles

**Use hooks to manage state, effects, memoization, and callbacks with proper dependency arrays.** Follow React rules of hooks, cleanup side effects, and compose custom hooks for reusable logic.

**Why**: Hooks provide a functional approach to state management and side effects. Proper usage prevents memory leaks, stale closures, unnecessary re-renders, and ensures predictable component behavior.

## When to Use This Skill

Use these patterns when:

- Managing local component state
- Performing side effects (data fetching, subscriptions, timers)
- Optimizing expensive calculations
- Creating stable function references for child components
- Tracking mutable values without triggering re-renders
- Composing reusable logic across components
- Integrating with Zustand stores or TanStack Query
- Preventing stale closures in async operations

## useState Patterns

### Local State Management

```typescript
import { useState } from 'react';

export const ProductSelector = () => {
  const [selectedId, setSelectedId] = useState<string>('');
  const [quantity, setQuantity] = useState(1);
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <View>
      <Button onPress={() => setIsExpanded(!isExpanded)}>
        Toggle Details
      </Button>
      {isExpanded && (
        <QuantityPicker
          value={quantity}
          onChange={setQuantity}
        />
      )}
    </View>
  );
};
```

**Why**: `useState` manages local component state that triggers re-renders when changed.

### Derived State with useMemo

```typescript
import { useState, useMemo } from 'react';

export const CartSummary = ({ items }: Props) => {
  const [discount, setDiscount] = useState(0);

  // ✅ Good - Derived state from props + state
  const total = useMemo(() => {
    const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    return subtotal - discount;
  }, [items, discount]);

  return (
    <View>
      <Text>Total: ${total.toFixed(2)}</Text>
      <DiscountInput value={discount} onChange={setDiscount} />
    </View>
  );
};
```

**Why**: Derive values from state/props using `useMemo` rather than storing redundant state.

### Complex State with Multiple Related Values

```typescript
import { useState } from 'react';

export const useProductDetailsSelection = (id: string, isCustomization: boolean) => {
  const [selectedCustomization, setSelectedCustomization] = useState(id);
  const [selectedPairing, setSelectedPairing] = useState<string[]>([]);

  return {
    selectedCustomization,
    selectedPairing,
    setSelectedCustomization,
    setSelectedPairing,
  };
};
```

**Why**: Group related state values together, but keep them separate if they change independently.

**Production Example**: `operations/shoppable-product/useProductDetailsSelection.ts:22`

## useEffect Patterns

### Data Synchronization

```typescript
import { useEffect } from 'react';

export const WeekSelector = ({ weeks, preSelectedWeekId }: Props) => {
  const { initializeWeeks, setSelectedWeek } = useStorefrontStore();

  useEffect(() => {
    // Synchronize external data with store
    if (weeks.length > 0) {
      initializeWeeks(weeks, preSelectedWeekId);
    }
  }, [weeks, preSelectedWeekId, initializeWeeks]);

  return <WeekList weeks={weeks} />;
};
```

**Why**: `useEffect` syncs external data (props, route params) with internal state.

**Production Example**: `hooks/use-week-initialization/useWeekInitialization.ts:54`

### Side Effects with Cleanup

```typescript
import { useEffect } from 'react';

export const RealTimeSubscription = ({ userId }: Props) => {
  useEffect(() => {
    // ✅ Good - Setup subscription
    const subscription = subscribeToUserUpdates(userId, (data) => {
      handleUpdate(data);
    });

    // ✅ Good - Cleanup function
    return () => {
      subscription.unsubscribe();
    };
  }, [userId]);

  return <View>{/* ... */}</View>;
};
```

**Why**: Cleanup functions prevent memory leaks from subscriptions, timers, or event listeners.

### Callbacks with Side Effects

```typescript
import { useEffect } from 'react';

export const useInitialStoreDataLoader = ({ categoryId, selectedWeek }: Props) => {
  const { setIsInitialStoreDataLoaded } = useStorefrontStore();

  const result = useGetInitialStoreQuery({
    variables: { categoryId, selectedWeek },
    onCompleted: () => {
      // ✅ Side effect after successful query
      setIsInitialStoreDataLoaded(true);
    },
    onError: () => {
      // ✅ Prevent retry loops
      setIsInitialStoreDataLoaded(true);
    },
  });

  return result;
};
```

**Why**: Use query callbacks for side effects instead of `useEffect` when data-fetching libraries support them.

**Production Example**: `hooks/use-initial-store-data-loader/useInitialStoreDataLoader.ts:39`

### Preventing Infinite Loops

```typescript
import { useEffect, useRef } from 'react';

export const UserProfileSync = ({ user }: Props) => {
  const { updateProfile } = useProfileStore();

  // ❌ Bad - Object dependency causes infinite loop
  useEffect(() => {
    updateProfile(user); // updateProfile creates new object → triggers effect → infinite loop
  }, [user, updateProfile]);

  // ✅ Good - Use ref to track changes
  const prevUserRef = useRef(user);

  useEffect(() => {
    if (prevUserRef.current?.id !== user.id) {
      updateProfile(user);
      prevUserRef.current = user;
    }
  }, [user, updateProfile]);

  return <ProfileView user={user} />;
};
```

**Why**: Object dependencies can cause infinite loops. Use `useRef` to track previous values.

## useMemo Patterns

### Expensive Calculations

```typescript
import { useMemo } from 'react';

export const useMealSelectionInfo = () => {
  const { config, totalMealKitItemsSize, errors } = useMealSelection();

  return useMemo(() => {
    if (!config) return undefined;

    const minMealsSize = config.variations.minMealsSize;
    const maxMealsSize = config.variations.maxMealsSize;

    const isMaxReached = maxMealsSize > 0 && maxMealsSize === totalMealKitItemsSize;
    const mealsNeededToReachMinimum = Math.max((minMealsSize ?? 0) - totalMealKitItemsSize, 0);
    const isBelowMinimum = Boolean(
      errors?.some((error) => error.type === UpdateCartErrorType.BelowMinimum) &&
      mealsNeededToReachMinimum > 0
    );

    return {
      isBelowMinimum,
      isMaxReached,
      totalMealKitItemsSize,
      minRequiredMealKitItemsSize: minMealsSize,
      maxSelectedMealKitItemSize: maxMealsSize,
      mealsNeededToReachMinimum,
    };
  }, [config, totalMealKitItemsSize, errors]);
};
```

**Why**: `useMemo` caches expensive calculations, only recomputing when dependencies change.

**Production Example**: `operations/use-selection-info/useMealSelectionInfo.ts:24`

### Memoizing Query Variables

```typescript
import { useMemo } from 'react';

export const useProductQuery = ({ categoryId, weekId, productId }: Props) => {
  // ✅ Good - Memoize variables to prevent Apollo cache misses
  const memoizedVariables = useMemo(
    () => ({
      categoryId,
      weekId,
      productId,
    }),
    [categoryId, weekId, productId]
  );

  const result = useProductDetailsQuery({
    variables: memoizedVariables,
  });

  return result;
};
```

**Why**: Memoized variables prevent Apollo cache misses and unnecessary re-fetches caused by object reference changes.

**Production Example**: `hooks/use-initial-store-data-loader/useInitialStoreDataLoader.ts:30`

### Selector Functions with Zustand

```typescript
import { useMemo } from 'react';
import { useShallow } from 'zustand/react/shallow';

export const useCartInfo = () => {
  const { selections, prices } = useMealSelection(
    useShallow((state) => ({
      selections: state.selection?.selections,
      prices: state.selection?.prices,
    }))
  );

  // ✅ Good - Memoize derived data from store
  const total = useMemo(() => {
    return selections?.reduce((sum, item) => {
      const price = prices?.[item.id] ?? 0;
      return sum + price * item.quantity;
    }, 0) ?? 0;
  }, [selections, prices]);

  return { selections, prices, total };
};
```

**Why**: Use `useShallow` with Zustand to prevent unnecessary re-renders, then `useMemo` for derived calculations.

## useCallback Patterns

### Event Handlers

```typescript
import { useCallback } from 'react';

export const useDeleteRecipe = ({ screenName, onDeleteSuccess }: Props) => {
  const { trackAnalyticsEvent } = useAnalyticsTracker();
  const { showToast } = useToast();
  const { translateRaw } = useT9n('recipe');
  const deleteRecipeMutation = useDeleteExternalRecipe();

  const onConfirm = useCallback(
    async (recipe: Recipe) => {
      // Track analytics
      trackAnalyticsEvent(
        CookbookRecipeDeleteConfirmEvent({
          screenName,
          recipeId: recipe.id,
          recipeTitle: recipe.title,
        })
      );

      try {
        // Execute API call
        await deleteRecipeMutation.mutateAsync({ id: recipe.id });

        // Success callback
        onDeleteSuccess?.(recipe);

        // Show success toast
        showToast({
          title: translateRaw('toast.delete_success.title'),
          variant: 'success',
        });
      } catch (error) {
        // Show error toast
        showToast({
          title: translateRaw('toast.delete_error.title'),
          variant: 'error',
        });
        throw error;
      }
    },
    [
      trackAnalyticsEvent,
      screenName,
      deleteRecipeMutation,
      onDeleteSuccess,
      showToast,
      translateRaw,
    ]
  );

  return { onConfirm };
};
```

**Why**: `useCallback` creates stable function references, preventing child component re-renders and maintaining referential equality.

**Production Example**: `operations/social-recipe-deletion/useDeleteRecipe.ts:54`

### Passing Callbacks to Child Components

```typescript
import { useCallback } from 'react';

export const RecipeList = ({ recipes }: Props) => {
  const { addToCart } = useCartStore();

  // ✅ Good - Memoized callback
  const handleAddToCart = useCallback(
    (recipeId: string) => {
      addToCart(recipeId);
      trackEvent('add_to_cart', { recipeId });
    },
    [addToCart]
  );

  return (
    <FlatList
      data={recipes}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <RecipeCard recipe={item} onAddToCart={handleAddToCart} />
      )}
    />
  );
};
```

**Why**: Memoized callbacks prevent FlatList from re-rendering all items when parent re-renders.

### Multiple Callbacks from One Hook

```typescript
import { useCallback } from 'react';

export interface DeleteRecipeCallbacks {
  onInitiate: (recipe: Recipe) => void;
  onConfirm: (recipe: Recipe) => Promise<void>;
  onCancel: (recipe: Recipe) => void;
}

export const useDeleteRecipe = (options: Options): DeleteRecipeCallbacks => {
  const { screenName } = options;
  const { trackAnalyticsEvent } = useAnalyticsTracker();

  const onInitiate = useCallback(
    (recipe: Recipe) => {
      trackAnalyticsEvent(CookbookRecipeDeleteInitiateEvent({ screenName, recipeId: recipe.id }));
    },
    [trackAnalyticsEvent, screenName]
  );

  const onConfirm = useCallback(
    async (recipe: Recipe) => {
      trackAnalyticsEvent(CookbookRecipeDeleteConfirmEvent({ screenName, recipeId: recipe.id }));
      // ... handle deletion
    },
    [trackAnalyticsEvent, screenName]
  );

  const onCancel = useCallback(
    (recipe: Recipe) => {
      trackAnalyticsEvent(CookbookRecipeDeleteCancelEvent({ screenName, recipeId: recipe.id }));
    },
    [trackAnalyticsEvent, screenName]
  );

  return { onInitiate, onConfirm, onCancel };
};
```

**Why**: Return multiple memoized callbacks from custom hooks for complex workflows.

**Production Example**: `operations/social-recipe-deletion/useDeleteRecipe.ts:31`

## useRef Patterns

### Tracking Previous Values

```typescript
import { useEffect, useRef } from 'react';

export const useWeekInitialization = ({ weeks, preSelectedWeekId }: Props) => {
  const { initializeWeeks, setSelectedWeek } = useStorefrontStore();

  // Track consumption to prevent overriding user selections
  const hasConsumedPreSelectedWeekIdRef = useRef(false);
  const prevSelectedWeekIdRef = useRef<string | undefined>(preSelectedWeekId);

  useEffect(() => {
    // Reset consumption when preSelectedWeekId changes
    if (prevSelectedWeekIdRef.current !== preSelectedWeekId) {
      hasConsumedPreSelectedWeekIdRef.current = false;
      prevSelectedWeekIdRef.current = preSelectedWeekId;
    }

    // Process deeplink once
    if (!hasConsumedPreSelectedWeekIdRef.current && preSelectedWeekId) {
      const target = weeks.find((week) => week.id === preSelectedWeekId);
      if (target) {
        setSelectedWeek(target);
        hasConsumedPreSelectedWeekIdRef.current = true;
      }
    }
  }, [weeks, preSelectedWeekId, setSelectedWeek]);
};
```

**Why**: `useRef` tracks values across renders without triggering re-renders. Perfect for consumption flags and previous values.

**Production Example**: `hooks/use-week-initialization/useWeekInitialization.ts:51`

### Preventing Stale Closures

```typescript
import { useEffect, useRef, useState } from 'react';

export const SearchInput = () => {
  const [query, setQuery] = useState('');
  const latestQueryRef = useRef(query);

  useEffect(() => {
    latestQueryRef.current = query;
  }, [query]);

  useEffect(() => {
    const interval = setInterval(() => {
      // ✅ Good - Always access latest value
      console.log('Current query:', latestQueryRef.current);
    }, 1000);

    return () => clearInterval(interval);
  }, []); // Empty deps - interval only created once

  return <TextInput value={query} onChangeText={setQuery} />;
};
```

**Why**: `useRef` provides access to latest values in callbacks/intervals without adding dependencies.

### Mutable State Without Re-renders

```typescript
import { useRef } from 'react';

export const VideoPlayer = () => {
  const playerRef = useRef<VideoPlayerInstance>(null);

  const handlePlay = () => {
    // ✅ Access DOM/native instance without triggering re-render
    playerRef.current?.play();
  };

  const handlePause = () => {
    playerRef.current?.pause();
  };

  return (
    <View>
      <Video ref={playerRef} />
      <Button onPress={handlePlay}>Play</Button>
      <Button onPress={handlePause}>Pause</Button>
    </View>
  );
};
```

**Why**: `useRef` stores mutable values (like DOM refs) that don't need to trigger re-renders.

## Custom Hooks Patterns

### Composing Reusable Logic

```typescript
import { useMemo } from 'react';
import { useShallow } from 'zustand/react/shallow';

export const useMealSelectionInfo = () => {
  // ✅ Compose multiple hooks
  const { config, totalMealKitItemsSize, totalAddonsItemsSize, errors } =
    useMealSelection(
      useShallow((state) => ({
        config: state.selection?.config,
        totalMealKitItemsSize: totalMealKitItemsSelector(state),
        totalAddonsItemsSize: totalAddonsItemsSelector(state),
        errors: state.errors,
      }))
    );

  // Derive complex state
  return useMemo(() => {
    if (!config) return undefined;

    const minMealsSize = config.variations.minMealsSize;
    const maxMealsSize = config.variations.maxMealsSize;
    const isMaxReached = maxMealsSize > 0 && maxMealsSize === totalMealKitItemsSize;
    const mealsNeededToReachMinimum = Math.max((minMealsSize ?? 0) - totalMealKitItemsSize, 0);

    return {
      isMaxReached,
      mealsNeededToReachMinimum,
      totalMealKitItemsSize,
      totalAddonsItemsSize,
    };
  }, [config, totalMealKitItemsSize, totalAddonsItemsSize]);
};
```

**Why**: Custom hooks compose primitive hooks and encapsulate complex logic for reuse.

**Production Example**: `operations/use-selection-info/useMealSelectionInfo.ts:13`

### Load-Once Pattern

```typescript
import { useMemo } from 'react';

export const useInitialStoreDataLoader = ({ categoryId, selectedWeek }: Props) => {
  const { isInitialStoreDataLoaded, setIsInitialStoreDataLoaded } = useStorefrontStore();

  // Memoize variables to prevent Apollo cache misses
  const memoizedVariables = useMemo(
    () => ({ categoryId, selectedWeek }),
    [categoryId, selectedWeek]
  );

  const result = useGetInitialStoreQuery({
    variables: memoizedVariables,
    onCompleted: () => setIsInitialStoreDataLoaded(true),
    onError: () => setIsInitialStoreDataLoaded(true),
    // Switch to cache-only after first load to prevent backend calls
    fetchPolicy: isInitialStoreDataLoaded ? 'cache-only' : 'cache-first',
  });

  return result;
};
```

**Why**: "Load-once" pattern prevents unnecessary network requests while maintaining cached data access.

**Production Example**: `hooks/use-initial-store-data-loader/useInitialStoreDataLoader.ts:21`

### Custom Hook with Multiple Effects

```typescript
import { useEffect, useState, useRef } from 'react';

export const useProductDetailsSelection = (
  id: string,
  productDetails: ProductDetails | null,
  isCustomizationDrawer: boolean
) => {
  const [selectedCustomization, setSelectedCustomization] = useState(id);
  const [selectedPairing, setSelectedPairing] = useState<string[]>([]);
  const prevCustomization = useRef(selectedCustomization);

  const { selections, prices } = useMealSelection(useShallow((state) => ({
    selections: state.selection?.selections,
    prices: state.selection?.prices,
  })));

  // Effect 1: Sync pairing with customization
  useEffect(() => {
    const customizationId = isCustomizationDrawer ? id : selectedCustomization;
    const pairedAddons = selections
      ?.filter((selection) => selection.pairedWith?.includes(customizationId))
      .map((selection) => selection.id);
    setSelectedPairing(pairedAddons ?? []);
    prevCustomization.current = selectedCustomization;
  }, [id, selections, selectedCustomization, isCustomizationDrawer]);

  // Effect 2: Sync customization with selections
  useEffect(() => {
    if (!productDetails || productDetails.isAddon) return;

    const customizationOnSelections = productDetails.customization?.group.variations.find(
      (variation) => selections?.[variation.id]
    );

    setSelectedCustomization(customizationOnSelections?.id ?? id);
  }, [id, selections, productDetails]);

  return {
    selectedCustomization,
    selectedPairing,
    setSelectedCustomization,
    setSelectedPairing,
    prices,
  };
};
```

**Why**: Custom hooks can contain multiple effects for different synchronization concerns.

**Production Example**: `operations/shoppable-product/useProductDetailsSelection.ts:17`

### Naming Convention

```typescript
// ✅ Good - Prefix with "use"
export const useDeleteRecipe = () => { /* ... */ };
export const useProductRepository = () => { /* ... */ };
export const useMealSelectionInfo = () => { /* ... */ };

// ❌ Bad - Missing "use" prefix
export const deleteRecipe = () => { /* ... */ };
export const productRepository = () => { /* ... */ };
```

**Why**: "use" prefix signals to React and linters that this is a hook with special rules.

## Common Mistakes to Avoid

❌ **Don't forget dependency arrays**:

```typescript
// ❌ Bad - Missing dependencies
useEffect(() => {
  fetchData(userId);
}, []); // userId not in deps

// ✅ Good - All dependencies included
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

❌ **Don't use hooks conditionally**:

```typescript
// ❌ Bad - Conditional hook
if (isEnabled) {
  const [value, setValue] = useState(0); // Breaks React rules
}

// ✅ Good - Hook always called
const [value, setValue] = useState(0);
if (!isEnabled) return null;
```

❌ **Don't create inline objects in dependencies**:

```typescript
// ❌ Bad - New object every render
useEffect(() => {
  fetchData(filters);
}, [{ category: 'food', price: 10 }]); // New object → infinite loop

// ✅ Good - Memoize object
const filters = useMemo(() => ({ category: 'food', price: 10 }), []);
useEffect(() => {
  fetchData(filters);
}, [filters]);
```

❌ **Don't forget cleanup**:

```typescript
// ❌ Bad - No cleanup
useEffect(() => {
  const interval = setInterval(() => fetchData(), 1000);
}, []); // Memory leak!

// ✅ Good - Cleanup function
useEffect(() => {
  const interval = setInterval(() => fetchData(), 1000);
  return () => clearInterval(interval);
}, []);
```

❌ **Don't use useState for derived values**:

```typescript
// ❌ Bad - Redundant state
const [items, setItems] = useState([]);
const [total, setTotal] = useState(0);

useEffect(() => {
  setTotal(items.reduce((sum, item) => sum + item.price, 0));
}, [items]);

// ✅ Good - Derive with useMemo
const [items, setItems] = useState([]);
const total = useMemo(
  () => items.reduce((sum, item) => sum + item.price, 0),
  [items]
);
```

✅ **Do use useCallback for event handlers**:

```typescript
// ✅ Good - Memoized callback
const handlePress = useCallback(() => {
  onSelect(item.id);
}, [onSelect, item.id]);

<Button onPress={handlePress}>Select</Button>
```

✅ **Do use useRef for previous values**:

```typescript
// ✅ Good - Track previous value
const prevValueRef = useRef(value);

useEffect(() => {
  if (prevValueRef.current !== value) {
    handleChange(value);
    prevValueRef.current = value;
  }
}, [value]);
```

✅ **Do compose custom hooks**:

```typescript
// ✅ Good - Compose hooks for reusable logic
export const useMealSelection = () => {
  const store = useMealSelectionStore();
  const analytics = useAnalyticsTracker();
  const toast = useToast();

  return { store, analytics, toast };
};
```

## Quick Reference

**useState:**
- Local component state
- Triggers re-renders on change
- Use for UI state (toggles, inputs, selections)
- Derive state with `useMemo`, don't duplicate

**useEffect:**
- Side effects (data fetching, subscriptions, DOM manipulation)
- Runs after render
- Always include dependencies
- Return cleanup function for subscriptions/timers

**useMemo:**
- Expensive calculations
- Derived state from props/state
- Query variables to prevent cache misses
- Only recomputes when dependencies change

**useCallback:**
- Event handlers for child components
- Stable function references
- Prevents unnecessary child re-renders
- Include all used values in dependencies

**useRef:**
- Mutable values without re-renders
- Previous value tracking
- DOM/native instance references
- Preventing stale closures

**Custom Hooks:**
- Prefix with "use"
- Compose primitive hooks
- Encapsulate reusable logic
- Can use all hook features

**Rules of Hooks:**
- Only call at top level (not in conditions/loops)
- Only call from React functions
- Include all dependencies in arrays
- Clean up side effects

**Key Libraries:**
- React Native 0.75.4
- Zustand 5.0.3 (with `useShallow`)
- TanStack Query 5.59.16
- TypeScript 5.1.6

For production examples, see [references/examples.md](references/examples.md).
