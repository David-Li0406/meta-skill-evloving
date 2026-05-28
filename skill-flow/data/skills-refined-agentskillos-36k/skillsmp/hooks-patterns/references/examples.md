# Hooks Patterns - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating React hooks patterns.

## Example 1: useWeekInitialization - Complex useEffect with useRef

**File**: `modules/store/screens/storefront/hooks/use-week-initialization/useWeekInitialization.ts`

This example demonstrates sophisticated useEffect patterns including consumption flags, previous value tracking, and preventing user selection overrides.

```typescript
import { useEffect, useRef } from 'react';
import { useStorefrontStore } from '@modules/store/zustand-store';

/**
 * Custom hook that handles week initialization and deeplink/routing parameter week selection.
 *
 * Key Problem Solved: Without consumption logic, the hook would re-run every time
 * and continuously override user selections back to the original preSelectedWeekId, creating
 * a frustrating UX where manual week selections get reset.
 *
 * Consumption Flag Logic:
 * - hasConsumedPreSelectedWeekId: Tracks if current deeplink was already processed
 * - Resets to false when preSelectedWeekId changes (new deeplink arrives)
 * - Prevents processing same deeplink multiple times
 * - Protects user selections from being overridden
 */
export const useWeekInitialization = ({ weeks, preSelectedWeekId }: Props) => {
  const { initializeWeeks, setSelectedWeek, selectedWeekId, availableWeeks } =
    useStorefrontStore();

  // Track consumption per current deeplink
  const hasConsumedPreSelectedWeekIdRef = useRef(false);
  const prevSelectedWeekIdRef = useRef<string | undefined>(preSelectedWeekId);

  useEffect(() => {
    const haveWeeks = weeks.length > 0;
    const haveAvailable = availableWeeks.length > 0;

    // Reset consumption flag when preSelectedWeekId changes
    if (prevSelectedWeekIdRef.current !== preSelectedWeekId) {
      hasConsumedPreSelectedWeekIdRef.current = false;
      prevSelectedWeekIdRef.current = preSelectedWeekId;
    }

    // 1) Initialize weeks once
    if (haveWeeks && availableWeeks.length !== weeks.length) {
      initializeWeeks(weeks, preSelectedWeekId);
    }

    if (!preSelectedWeekId) {
      return;
    }

    // If we're already on the target week, mark consumed and bail
    if (selectedWeekId === preSelectedWeekId) {
      hasConsumedPreSelectedWeekIdRef.current = true;
      return;
    }

    // Process deeplink only once
    if (!hasConsumedPreSelectedWeekIdRef.current) {
      // Prefer store weeks if present; otherwise fall back to raw weeks
      const source = haveAvailable ? availableWeeks : weeks;
      const target = source.find((week) => week.id === preSelectedWeekId);

      if (target) {
        setSelectedWeek(target);
        hasConsumedPreSelectedWeekIdRef.current = true;
      }
    }
  }, [
    weeks,
    availableWeeks,
    preSelectedWeekId,
    selectedWeekId,
    initializeWeeks,
    setSelectedWeek,
  ]);
};
```

**Key patterns demonstrated:**
- `useRef` to track consumption flags (prevents repeated processing)
- `useRef` to track previous values (detects changes)
- Complex `useEffect` logic with multiple conditions
- Early returns to prevent unnecessary processing
- Protecting user selections from being overridden

## Example 2: useInitialStoreDataLoader - Load-Once Pattern with useMemo

**File**: `modules/store/screens/storefront/hooks/use-initial-store-data-loader/useInitialStoreDataLoader.ts`

This example demonstrates the "load-once" pattern to prevent unnecessary network requests while maintaining cached data access.

```typescript
import { useMemo } from 'react';
import { useGetInitialStoreQuery } from '@data-access/graphql/store';
import { useStorefrontStore } from '@modules/store/zustand-store/navigation/useStorefrontStore';

/**
 * This hook implements a "load-once" pattern for initial store data to prevent unnecessary
 * network requests when users switch between weeks or navigate between stacks.
 *
 * The original challenge: We observed that Apollo was triggering the query
 * multiple times when users switch between weeks or navigate away and back.
 *
 * The solution: We use a global flag to track if we've loaded initial data. After the first load,
 * we switch to 'cache-only' fetchPolicy to prevent network calls while still returning cached data.
 */
export const useInitialStoreDataLoader = ({
  categoryId,
  selectedWeek,
  startWeek,
}: Props) => {
  const { isInitialStoreDataLoaded, setIsInitialStoreDataLoaded } =
    useStorefrontStore();

  // Memoize variables to prevent unnecessary re-renders and Apollo cache misses
  const memoizedVariables = useMemo(
    () => ({
      categoryId,
      selectedWeek,
      startWeek,
    }),
    [categoryId, selectedWeek, startWeek]
  );

  const result = useGetInitialStoreQuery({
    variables: memoizedVariables,
    onCompleted: () => {
      // Mark as attempted globally after successful completion
      setIsInitialStoreDataLoaded(true);
    },
    onError: () => {
      // Mark as attempted globally after error to prevent infinite retry loops
      setIsInitialStoreDataLoaded(true);
    },
    // Use cache-only after first load to prevent backend calls
    // Use cache-first on first load to fetch from network if cache is empty
    fetchPolicy: isInitialStoreDataLoaded ? 'cache-only' : 'cache-first',
    // Continue on errors to ensure the completion callback can still fire
    errorPolicy: 'all',
  });

  return result;
};
```

**Key patterns demonstrated:**
- `useMemo` to prevent Apollo cache misses
- Load-once pattern with global flag
- Dynamic `fetchPolicy` based on load state
- `onCompleted` and `onError` callbacks for side effects
- Error handling to prevent retry loops

## Example 3: useMealSelectionInfo - useMemo for Complex Derived State

**File**: `operations/use-selection-info/useMealSelectionInfo.ts`

This example shows complex derived state calculations using `useMemo` and `useShallow` with Zustand.

```typescript
import { useMemo } from 'react';
import { useShallow } from 'zustand/react/shallow';
import { UpdateCartErrorType } from '@data-access/graphql';
import { NavigationBarDataAccess } from '@data-access/native';
import {
  totalAddonsItemsSelector,
  totalMealKitItemsSelector,
  useMealSelection,
} from '@operations/meal-selection';

export const useMealSelectionInfo = () => {
  // Use useShallow to prevent unnecessary re-renders
  const { config, totalMealKitItemsSize, totalAddonsItemsSize, errors } =
    useMealSelection(
      useShallow((state) => ({
        config: state.selection?.config,
        totalMealKitItemsSize: totalMealKitItemsSelector(state),
        totalAddonsItemsSize: totalAddonsItemsSelector(state),
        errors: state.errors,
      }))
    );

  return useMemo(() => {
    if (!config) {
      return undefined;
    }

    // Find the minMealsSize for the product
    const minMealsSize = config.variations.minMealsSize;

    // Find the maxMealsSize for the product
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

    // Side effect: Update native navigation bar
    NavigationBarDataAccess.events.belowMinimumBoxSizeStateChanged(
      isBelowMinimum
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

**Key patterns demonstrated:**
- `useShallow` with Zustand to prevent unnecessary re-renders
- Selector functions for derived store state
- `useMemo` for complex calculations
- Multiple derived values returned as object
- Side effect within useMemo (native bridge call)

## Example 4: useProductDetailsSelection - Multiple useState and useEffect

**File**: `operations/shoppable-product/useProductDetailsSelection.ts`

This example demonstrates managing complex local state with multiple related values and synchronization effects.

```typescript
import { useEffect, useRef, useState } from 'react';
import { useShallow } from 'zustand/react/shallow';
import { selectionsMapSelector, useMealSelection } from '@operations/meal-selection';

/**
 * Hook to manage selection related state for product details
 */
export const useProductDetailsSelection = (
  id: string,
  productDetails: ProductDetails | null | undefined,
  isCustomizationDrawer: boolean
) => {
  const [selectedCustomization, setSelectedCustomization] = useState(id);
  const [selectedPairing, setSelectedPairing] = useState<string[]>([]);
  const prevCustomization = useRef(selectedCustomization);

  const { selections, prices } = useMealSelection(
    useShallow((selectionState) => ({
      selections: selectionState.selection?.selections,
      prices: selectionState.selection?.prices,
    }))
  );

  const selectionsMap = useMealSelection(useShallow(selectionsMapSelector));
  const quantity = selectionsMap[selectedCustomization]?.quantity || 0;

  // Effect 1: Sync pairing with customization selection
  useEffect(() => {
    if (quantity === 0 && selectedCustomization !== prevCustomization.current) {
      // Don't reset the pairing if the customization is changed and the product is not in the selection
      prevCustomization.current = selectedCustomization;
      return;
    }

    // Use the id if in customization drawer, otherwise use selected customization
    const customizationId = isCustomizationDrawer ? id : selectedCustomization;
    const pairedAddons = selections
      ?.filter((selection) => {
        if (selection.pairedWith?.includes(customizationId)) {
          return true;
        }
        return false;
      })
      .map((selection) => selection.id);
    setSelectedPairing(pairedAddons ?? []);

    prevCustomization.current = selectedCustomization;
  }, [id, selections, selectedCustomization, quantity, isCustomizationDrawer]);

  // Effect 2: Sync customization with selections in store
  useEffect(() => {
    // This useEffect keeps the customization and selections in sync
    if (!productDetails || productDetails.isAddon) {
      return;
    }

    const customizationOnSelections =
      productDetails.customization?.group.variations.find(
        (variation) => selectionsMap[variation.id]
      );

    setSelectedCustomization(customizationOnSelections?.id ?? id);
  }, [id, selectionsMap, productDetails]);

  return {
    selectedCustomization,
    selectedPairing,
    setSelectedCustomization,
    setSelectedPairing,
    prices,
  };
};
```

**Key patterns demonstrated:**
- Multiple `useState` for related but independent state
- `useRef` to track previous values
- Multiple `useEffect` hooks for different synchronization concerns
- Early returns in effects for conditional logic
- Derived values from Zustand store with `useShallow`

## Example 5: useDeleteRecipe - useCallback for Complex Async Operations

**File**: `operations/social-recipe-deletion/useDeleteRecipe.ts`

This example shows returning multiple memoized callbacks from a custom hook for complex workflows.

```typescript
import { useCallback } from 'react';
import { useDeleteExternalRecipe } from '@data-access/query/external-recipes';
import { useToast } from '@features/toast-feature/useToast';
import { useAnalyticsTracker } from '@libs/analytics';
import { useT9n } from '@libs/localization';

interface UseDeleteRecipeOptions {
  screenName: string;
  onDeleteSuccess?: (recipe: Recipe) => void;
  showToasts?: boolean;
  refetch?: () => void;
}

export interface DeleteRecipeCallbacks {
  onInitiate: (recipe: Recipe) => void;
  onConfirm: (recipe: Recipe) => Promise<void>;
  onCancel: (recipe: Recipe) => void;
}

export const useDeleteRecipe = (
  options: UseDeleteRecipeOptions
): DeleteRecipeCallbacks => {
  const { onDeleteSuccess, showToasts = true, refetch, screenName } = options;
  const { trackAnalyticsEvent } = useAnalyticsTracker();
  const { showToast } = useToast();
  const { translateRaw } = useT9n('social-recipe-bridge');
  const deleteRecipeMutation = useDeleteExternalRecipe({});

  const onInitiate = useCallback(
    (recipe: Recipe) => {
      // Track initiate analytics
      trackAnalyticsEvent(
        CookbookRecipeDeleteInitiateEvent({
          screenName,
          recipeId: recipe.id,
          recipeTitle: recipe.title,
        }).createAnalyticsEvent()
      );
    },
    [trackAnalyticsEvent, screenName]
  );

  const onConfirm = useCallback(
    async (recipe: Recipe) => {
      // Track confirm analytics
      trackAnalyticsEvent(
        CookbookRecipeDeleteConfirmEvent({
          screenName,
          recipeId: recipe.id,
          recipeTitle: recipe.title,
        }).createAnalyticsEvent()
      );

      try {
        // Execute API call
        await deleteRecipeMutation.mutateAsync({ id: recipe.id });

        // Handle success callbacks
        onDeleteSuccess?.(recipe);
        refetch?.();

        // Show success toast
        if (showToasts) {
          showToast({
            id: 'recipe-deleted',
            title: translateRaw(
              'social-recipe-bridge.toast.delete_success.title'
            ),
            description: translateRaw(
              'social-recipe-bridge.toast.delete_success.description'
            ),
            variant: 'success',
            autoHide: true,
            duration: 3000,
          });
        }
      } catch (error) {
        // Show error toast
        if (showToasts) {
          showToast({
            id: 'recipe-delete-error',
            title: translateRaw(
              'social-recipe-bridge.toast.delete_error.title'
            ),
            description: translateRaw(
              'social-recipe-bridge.toast.delete_error.description'
            ),
            variant: 'error',
            autoHide: true,
            duration: 3000,
          });
        }

        // Re-throw error for any calling code to handle
        throw error;
      }
    },
    [
      trackAnalyticsEvent,
      screenName,
      deleteRecipeMutation,
      onDeleteSuccess,
      refetch,
      showToasts,
      showToast,
      translateRaw,
    ]
  );

  const onCancel = useCallback(
    (recipe: Recipe) => {
      // Track cancel analytics
      trackAnalyticsEvent(
        CookbookRecipeDeleteCancelEvent({
          screenName,
          recipeId: recipe.id,
        }).createAnalyticsEvent()
      );
    },
    [trackAnalyticsEvent, screenName]
  );

  return { onInitiate, onConfirm, onCancel };
};
```

**Key patterns demonstrated:**
- Multiple `useCallback` for different workflow stages
- Async operations with try/catch error handling
- Optional callbacks (`onDeleteSuccess?.()`)
- Conditional side effects (toast notifications)
- Re-throwing errors for caller handling
- Return interface with TypeScript types
- Comprehensive dependency arrays

## Anti-Patterns from Codebase Review

### ❌ Missing Dependencies

```typescript
// DON'T: Missing userId dependency
useEffect(() => {
  fetchUserData(userId);
}, []); // Should include userId
```

### ❌ Inline Objects in Dependencies

```typescript
// DON'T: New object every render
useEffect(() => {
  fetchData({ category: 'food' });
}, [{ category: 'food' }]); // Infinite loop!

// DO: Memoize object
const filters = useMemo(() => ({ category: 'food' }), []);
useEffect(() => {
  fetchData(filters);
}, [filters]);
```

### ❌ Unnecessary State

```typescript
// DON'T: Redundant state
const [items, setItems] = useState([]);
const [total, setTotal] = useState(0);

useEffect(() => {
  setTotal(items.reduce((sum, item) => sum + item.price, 0));
}, [items]);

// DO: Derive with useMemo
const [items, setItems] = useState([]);
const total = useMemo(
  () => items.reduce((sum, item) => sum + item.price, 0),
  [items]
);
```

### ❌ Missing Cleanup

```typescript
// DON'T: No cleanup function
useEffect(() => {
  const interval = setInterval(() => fetchData(), 1000);
}, []); // Memory leak!

// DO: Return cleanup function
useEffect(() => {
  const interval = setInterval(() => fetchData(), 1000);
  return () => clearInterval(interval);
}, []);
```

## Summary

The YourCompany codebase consistently follows these hooks patterns:

1. **useState** for local component state (toggles, selections, inputs)
2. **useEffect** for side effects with proper cleanup and dependency arrays
3. **useMemo** for expensive calculations and memoizing query variables
4. **useCallback** for event handlers to prevent child re-renders
5. **useRef** for tracking previous values and consumption flags
6. **Custom hooks** compose primitive hooks for reusable logic
7. **useShallow** with Zustand to prevent unnecessary re-renders
8. Always include all dependencies in arrays
9. Always return cleanup functions for subscriptions/timers
10. Use TypeScript strict mode with explicit types

These patterns ensure predictable behavior, optimal performance, and prevent common issues like memory leaks, infinite loops, and stale closures.
