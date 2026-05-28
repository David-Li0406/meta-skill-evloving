# Feature Flags - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating feature flag patterns.

## Example 1: Custom Wrapper Hook

**File**: `operations/profile-service/feature-flags/useIsShortShippingEnabled.ts:1`

This example shows a custom wrapper hook that encapsulates feature flag logic with constants.

```typescript
import {
  useFeatureIsEnabled,
  ProfileServiceModuleFeatureFlagKeys,
} from '@libs/native-modules/feature-toggle';

export const useIsShortShippingEnabled = () => {
  return useFeatureIsEnabled(
    ProfileServiceModuleFeatureFlagKeys.RTEA_SHORT_SHIPPING
  );
};
```

**Key patterns demonstrated:**
- Custom wrapper hook with descriptive name (useIsShortShippingEnabled)
- Import feature flag constants from ProfileServiceModuleFeatureFlagKeys
- Single responsibility: checks one specific feature flag
- Returns boolean from useFeatureIsEnabled directly
- No additional logic - pure wrapper for reusability
- Makes feature flag usage discoverable (named hook vs generic useFeatureIsEnabled)

## Example 2: Feature Flag in Business Logic Hook

**File**: `operations/meal-selection-listener/useMealSelectionListener.ts:97`

This example shows feature flag usage in a complex business logic hook, passing flag state to mutations.

```typescript
import { useCallback, useEffect, useMemo, useRef } from 'react';
import { useShallow } from 'zustand/react/shallow';

import type { CartFragmentFragment } from '@data-access/graphql';
import {
  useGetCartForSelectedWeek,
  useUpdateCartMutation,
} from '@data-access/graphql/cart';

import {
  StoreModuleFeatureFlagKeys,
  useFeatureIsEnabled,
} from '@libs/native-modules/feature-toggle';

export const useMealSelectionListener = ({
  deliveryId,
}: UseMealSelectionListenerArgs) => {
  const {
    selection,
    setIsSaving,
    overrideStateFields,
    overrideSelection,
    wasSelectionChanged,
    setErrors,
    setSeamlessDowngraded,
  } = useMealSelection(
    useShallow((state) => ({
      selection: state.selection,
      setIsSaving: state.setIsSaving,
      overrideStateFields: state.overrideStateFields,
      overrideSelection: state.overrideSelection,
      wasSelectionChanged: state.wasSelectionChanged,
      setErrors: state.setErrors,
      setSeamlessDowngraded: state.setSeamlessDowngraded,
    }))
  );

  // Check seamless downgrade feature flag
  const isSeamlessDowngradeEnabled = useFeatureIsEnabled(
    StoreModuleFeatureFlagKeys.RNSM_SEAMLESS_BOX_DOWNGRADE
  );

  const [getCartForSelectedWeek] = useGetCartForSelectedWeek({
    fetchPolicy: 'network-only',
  });

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
        isSeamlessDowngradeEnabled, // Pass to mutation handlers
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
      isSeamlessDowngradeEnabled, // Include in dependencies
      setSeamlessDowngraded,
    ]
  );

  // Pass feature flag to mutation variables
  const [updateCart, { loading }] = useUpdateCartMutation({
    variables: {
      planId,
      deliveryId,
      selectionInput: selectionToSave ?? [],
      isSeamlessDowngradeEnabled, // Feature flag controls mutation behavior
    },
    onCompleted,
    onError,
  });

  useEffect(() => {
    if (wasSelectionChanged) {
      hideToast();
      updateCart();
    }
  }, [selectionToSave, wasSelectionChanged]);

  useEffect(() => {
    setIsSaving(loading);
  }, [loading, setIsSaving]);
};
```

**Key patterns demonstrated:**
- Feature flag check: `useFeatureIsEnabled(StoreModuleFeatureFlagKeys.RNSM_SEAMLESS_BOX_DOWNGRADE)`
- Pass feature flag to GraphQL mutation variables
- Include feature flag in useMemo dependencies (affects mutation handlers)
- Feature flag controls server-side behavior (seamless box downgrade logic)
- Use StoreModuleFeatureFlagKeys constant (module-specific constants)
- Feature flag affects multiple parts of logic (mutation variables, handlers)
- Boolean flag state passed down to nested logic (createMutationHandlers)

## Example 3: Testing Custom Wrapper Hook

**File**: `operations/profile-service/feature-flags/useIsShortShippingEnabled.spec.ts:1`

This example shows comprehensive testing of a custom feature flag wrapper hook.

```typescript
import { renderHook } from '@testing-library/react-native';

import {
  useFeatureIsEnabled,
  ProfileServiceModuleFeatureFlagKeys,
} from '@libs/native-modules/feature-toggle';

import { useIsShortShippingEnabled } from './useIsShortShippingEnabled';

jest.mock('@libs/native-modules/feature-toggle', () => ({
  useFeatureIsEnabled: jest.fn(),
  ProfileServiceModuleFeatureFlagKeys: {
    RTEA_SHORT_SHIPPING: 'rtea_short_shipping',
  },
}));

describe('useIsShortShippingEnabled', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should return true when feature flag is enabled', () => {
    (useFeatureIsEnabled as jest.Mock).mockReturnValue(true);

    const { result } = renderHook(() => useIsShortShippingEnabled());

    expect(result.current).toBe(true);
    expect(useFeatureIsEnabled).toHaveBeenCalledWith(
      ProfileServiceModuleFeatureFlagKeys.RTEA_SHORT_SHIPPING
    );
  });

  it('should return false when feature flag is disabled', () => {
    (useFeatureIsEnabled as jest.Mock).mockReturnValue(false);

    const { result } = renderHook(() => useIsShortShippingEnabled());

    expect(result.current).toBe(false);
    expect(useFeatureIsEnabled).toHaveBeenCalledWith(
      ProfileServiceModuleFeatureFlagKeys.RTEA_SHORT_SHIPPING
    );
  });

  it('should use the correct feature flag key', () => {
    (useFeatureIsEnabled as jest.Mock).mockReturnValue(true);

    renderHook(() => useIsShortShippingEnabled());

    expect(useFeatureIsEnabled).toHaveBeenCalledWith('rtea_short_shipping');
  });
});
```

**Key patterns demonstrated:**
- Mock entire feature-toggle module with jest.mock
- Mock useFeatureIsEnabled as jest.fn() for flexible test control
- Mock feature flag constants (ProfileServiceModuleFeatureFlagKeys)
- Test both enabled (true) and disabled (false) states
- Verify correct feature flag key is passed (toHaveBeenCalledWith)
- Use renderHook from @testing-library/react-native for hook testing
- Clear mocks in beforeEach to reset state between tests
- Test hook behavior (result.current) matches expected values
- Verify integration: hook calls useFeatureIsEnabled with correct constant
- Test actual string value ('rtea_short_shipping') used by SDK

## Summary

The YourCompany codebase consistently follows these feature flag patterns:

1. **Module-Specific Constants** - ProfileServiceModuleFeatureFlagKeys, StoreModuleFeatureFlagKeys organized by domain
2. **SCREAMING_SNAKE_CASE Naming** - Feature flag keys use consistent case (RTEA_SHORT_SHIPPING, RNSM_SEAMLESS_BOX_DOWNGRADE)
3. **Custom Wrapper Hooks** - Named hooks like useIsShortShippingEnabled() for reusability and discoverability
4. **Feature Flag in Mutations** - Pass boolean flag state to GraphQL mutations to control server behavior
5. **useMemo Dependencies** - Include feature flag in dependency arrays when it affects computed values
6. **Comprehensive Testing** - Test both enabled and disabled states, verify correct constants used
7. **Mock Module Pattern** - Mock entire @libs/native-modules/feature-toggle module with useFeatureIsEnabled and constants
8. **renderHook for Hooks** - Use @testing-library/react-native renderHook to test custom wrapper hooks
9. **Clear Test Setup** - jest.clearAllMocks() in beforeEach to reset mock state
10. **Verify Integration** - toHaveBeenCalledWith verifies correct feature flag constant passed to useFeatureIsEnabled

These patterns enable gradual rollouts, A/B testing, quick feature toggles, targeted releases, and safe testing of feature flag logic across the app.
