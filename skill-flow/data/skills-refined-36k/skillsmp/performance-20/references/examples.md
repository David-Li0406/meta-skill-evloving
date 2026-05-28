# Performance Optimization - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating performance optimization patterns.

## Example 1: useRef for Tracking State Across Renders

**File**: `operations/meal-selection-listener/useMealSelectionListener.ts:64`

This example shows useRef tracking previous selections for error recovery and state management.

```typescript
import { useRef, useEffect, useMemo, useCallback } from 'react';
import type { CartFragmentFragment } from '@data-access/graphql';

export const useMealSelectionListener = ({ deliveryId }) => {
  const { selection, setIsSaving, overrideStateFields, overrideSelection } =
    useMealSelection(/* ... */);

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
        // This creates a cascading update
        // 1. previousSelectionRef.current is updated
        // 2. if previousSelectionRef.current is not undefined, lastSuccessfulSelectionRef.current is updated

        // This ensure lastSuccessfulSelectionRef.current is the previous successful selection
        lastSuccessfulSelectionRef.current = previousSelectionRef.current;
      }
      // Update the previous selection ref
      // This update happens every time selection changes
      previousSelectionRef.current = selection;
    }
  }, [selection]);

  // Use refs in callbacks
  const handleSelectionUpdate = useCallback(
    (newSelection: CartFragmentFragment, isError?: boolean) => {
      if (isError) {
        overrideSelection(newSelection);
      } else {
        overrideStateFields(newSelection);
      }
      // Update lastSuccessfulSelectionRef with the successful server response
      lastSuccessfulSelectionRef.current = newSelection;
    },
    [overrideSelection, overrideStateFields]
  );
};
```

**Key patterns demonstrated:**
- Two useRef hooks tracking different states (lastSuccessful, previous)
- useEffect updates refs without triggering re-renders
- Refs provide stable references for error recovery
- Cascading update pattern: previous → lastSuccessful
- Initialize refs on first mount with conditional check
- Use refs in callbacks for state management
- No re-renders when ref values change

## Example 2: useMemo for Expensive Computed Values

**File**: `operations/use-selection-info/useMealSelectionInfo.ts:24`

This example shows useMemo caching complex derived state calculations.

```typescript
import { useMemo } from 'react';
import { useShallow } from 'zustand/react/shallow';
import { UpdateCartErrorType } from '@data-access/graphql';

export const useMealSelectionInfo = () => {
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

    // Find the minMealsSize for the product that has the same number of servings
    const minMealsSize = config.variations.minMealsSize;

    // Find the maxMealsSize for the product that has the same number of servings
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

**Key patterns demonstrated:**
- useMemo wraps entire return value for hook
- Multiple derived calculations (isMaxReached, isBelowMinimum, mealsNeeded)
- Early return for undefined config
- Dependencies: config, totalMealKitItemsSize, totalAddonsItemsSize, errors
- Complex array operations (errors.some)
- Math.max for calculations
- Only recomputes when dependencies change
- Returns object with multiple computed properties

## Example 3: useMemo for Data Transformation

**File**: `operations/meal-selection-listener/useMealSelectionListener.ts:58`

This example shows useMemo caching expensive data transformations.

```typescript
import { useMemo } from 'react';
import { transformSelectionForSave } from './utils/utils';

export const useMealSelectionListener = ({ deliveryId }) => {
  const { selection } = useMealSelection(/* ... */);

  const selectionToSave = useMemo(
    () => transformSelectionForSave(selection),
    [selection]
  );

  // Use memoized transformation in mutation
  const [updateCart, { loading }] = useUpdateCartMutation({
    variables: {
      planId,
      deliveryId,
      selectionInput: selectionToSave ?? [],
      isSeamlessDowngradeEnabled,
    },
    onCompleted,
    onError,
  });

  useEffect(() => {
    if (wasSelectionChanged) {
      hideToast();
      updateCart();
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectionToSave, wasSelectionChanged]);
};
```

**Key patterns demonstrated:**
- useMemo caches expensive transformation function
- Single dependency: selection
- Transformed value used in mutation variables
- Transformation only runs when selection changes
- useEffect depends on memoized value (selectionToSave)
- Documented eslint-disable comment
- Fallback with ?? operator (selectionToSave ?? [])

## Example 4: useCallback for Stable Event Handlers

**File**: `operations/refresh/useRefresh.ts:20`

This example shows useCallback creating stable callback references.

```typescript
import { useCallback, useState } from 'react';

/**
 * Hook that provides general refresh functionality for any data fetching operation
 */
export const useRefresh = (options: {
  refetchFunctions: Array<() => Promise<unknown>>;
  isRefetching?: boolean;
}) => {
  const { refetchFunctions, isRefetching } = options;
  const [isManualRefreshing, setIsManualRefreshing] = useState(false);

  // Combined loading state
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

**Key patterns demonstrated:**
- useCallback wraps async event handler
- Single dependency: refetchFunctions
- Stable callback reference prevents child re-renders
- Try/catch/finally for error handling
- Promise.all for concurrent execution
- State updates in finally block (always runs)
- Returned callback has stable reference

## Example 5: useCallback in useMemo Dependencies

**File**: `operations/meal-selection-listener/useMealSelectionListener.ts:104`

This example shows useCallback creating stable callbacks used in useMemo dependencies.

```typescript
import { useCallback, useMemo } from 'react';

export const useMealSelectionListener = ({ deliveryId }) => {
  const handleSelectionUpdate = useCallback(
    (newSelection: CartFragmentFragment, isError?: boolean) => {
      // Skip the next save trigger since this is a server update
      if (isError) {
        overrideSelection(newSelection);
      } else {
        overrideStateFields(newSelection);
      }
      // Update lastSuccessfulSelectionRef with the successful server response
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

  const { onCompleted, onError } = useMemo(
    () =>
      createMutationHandlers({
        planId,
        deliveryId,
        showSuccessToast,
        showErrorToast,
        lastSuccessfulSelectionRef,
        onSelectionUpdate: handleSelectionUpdate,
        setLastAboveMinimumSelection,
        onError: handleErrorUpdate,
        trackFoodItemSave,
        getCartForSelectedWeek,
        selection,
        isSeamlessDowngradeEnabled,
        setSeamlessDowngraded,
      }),
    [
      planId,
      deliveryId,
      showSuccessToast,
      showErrorToast,
      handleSelectionUpdate,
      setLastAboveMinimumSelection,
      handleErrorUpdate,
      trackFoodItemSave,
      getCartForSelectedWeek,
      selection,
      isSeamlessDowngradeEnabled,
      setSeamlessDowngraded,
    ]
  );
};
```

**Key patterns demonstrated:**
- useCallback creates stable handleSelectionUpdate callback
- useCallback creates stable handleErrorUpdate callback
- Callbacks used in useMemo dependencies
- Prevents useMemo from recomputing unnecessarily
- Complex dependency array with multiple values
- Ref usage in callback (lastSuccessfulSelectionRef.current)
- Parameters<typeof setErrors>[0] for type-safe parameters

## Example 6: React.memo for List Items

**File**: `features/product-listing-feature/components/ProductListItem.tsx:61`

This example shows React.memo preventing expensive list item re-renders.

```typescript
import React from 'react';
import type { StyleProp, ViewStyle } from 'react-native';
import { View } from 'react-native';

type ProductListingComponentProps = {
  item: ProductListingItem;
  variant: (product: ProductListingProduct) => CardVariant;
  itemContainerStyle?: StyleProp<ViewStyle>;
  position?: number;
};

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

    if (isBenefitsCarousel(item)) {
      return null;
    }

    const cardVariant = variant(item);

    // Enhance the card variant with position data if it supports actions
    const enhancedCardVariant = hasActionHandler(cardVariant)
      ? enhanceCardVariantWithPosition(cardVariant, position)
      : cardVariant;

    const productItemSizeStyle =
      enhancedCardVariant.size === 'large'
        ? styles.productItemLargeWrapper
        : styles.productItemSmallWrapper;

    return (
      <AnalyticsWrapper
        parameters={{
          recipe_position: position,
          ui_element: SOURCE.LIST,
          top_layer: TOP_LAYER.NO_POPUP,
        }}
      >
        <View style={productItemSizeStyle}>
          <ProductCard data={enhancedCardVariant} />
        </View>
      </AnalyticsWrapper>
    );
  }
);
```

**Key patterns demonstrated:**
- React.memo wraps entire component
- No custom comparison function (shallow prop comparison)
- Complex rendering logic with conditionals
- Multiple prop types (item, variant, itemContainerStyle, position)
- Expensive child components (WidgetContainer, ProductCard)
- Prevents re-render when parent re-renders
- Used in FlatList renderItem for list performance

## Example 7: FlatList with getItemLayout

**File**: `features/app-onboarding/components/Body.tsx:144`

This example shows comprehensive FlatList optimization with getItemLayout.

```typescript
import { useRef, useEffect } from 'react';
import { FlatList, Dimensions } from 'react-native';

const { width: screenWidth } = Dimensions.get('window');

const Body = ({ slides, currentSlideIndex = 0, onSlideChange }: BodyProps) => {
  const flatListRef = useRef<FlatList>(null);

  // Scroll to the correct index when currentSlideIndex changes from buttons
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

  const handleScroll = (event: NativeSyntheticEvent<NativeScrollEvent>) => {
    const { contentOffset } = event.nativeEvent;
    const newIndex = Math.round(contentOffset.x / screenWidth);
    if (
      onSlideChange &&
      newIndex !== currentSlideIndex &&
      newIndex >= 0 &&
      newIndex < slides.length
    ) {
      onSlideChange(newIndex);
    }
  };

  const renderSlide = ({ item, index }: { item: Step; index: number }) => (
    <Slide item={item} index={index} zestStyles={zestStyles} />
  );

  return (
    <FlatList
      ref={flatListRef}
      data={slides}
      renderItem={renderSlide}
      keyExtractor={(_, index) => index.toString()}
      horizontal
      pagingEnabled
      showsHorizontalScrollIndicator={false}
      scrollEventThrottle={16}
      decelerationRate="normal"
      initialScrollIndex={currentSlideIndex}
      onMomentumScrollEnd={handleScroll}
      getItemLayout={(_, index) => ({
        length: screenWidth,
        offset: screenWidth * index,
        index,
      })}
      ItemSeparatorComponent={null}
      removeClippedSubviews={false}
      style={{ width: screenWidth }}
      testID="onboarding-carousel"
    />
  );
};
```

**Key patterns demonstrated:**
- useRef stores FlatList reference
- getItemLayout for instant scrolling (screenWidth * index)
- Fixed item width (screenWidth) enables optimization
- Stable renderSlide callback (extracted, not inline)
- useEffect with ref for imperative scrollToOffset
- horizontal pagination with pagingEnabled
- scrollEventThrottle={16} for smooth scrolling
- initialScrollIndex for initial position
- removeClippedSubviews={false} to keep items mounted
- keyExtractor using index (stable keys)

## Summary

The YourCompany codebase consistently follows these performance patterns:

1. **useRef for tracking** without re-renders (flags, previous values, component refs)
2. **useMemo for expensive computations** (filtering, sorting, transformations)
3. **useMemo for context values** to prevent consumer re-renders
4. **useCallback for stable callbacks** passed as props or in dependencies
5. **React.memo for expensive components** (especially list items)
6. **FlatList getItemLayout** for fixed-height items
7. **Extract renderItem callbacks** for stable references
8. **Document empty dependency arrays** with eslint-disable comments
9. **Strategic optimization** - profile first, optimize when needed
10. **Type-safe patterns** with TypeScript for all hooks

These patterns ensure optimal performance while maintaining clean, maintainable code throughout the app.
