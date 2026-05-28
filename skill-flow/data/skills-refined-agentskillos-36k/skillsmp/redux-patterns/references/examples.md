# Redux Patterns - Production Examples

This document contains real production code examples from the YourCompany web codebase demonstrating Redux 4 patterns.

## Example 1: useSelector for Reading State

**File**: `app/spaces/whitelabel/modules/whitelabel-web/packages/pages/settings/src/components/Reactivation/hooks/useTrackCustomerReactivation.ts`

This example demonstrates using `useSelector` to access multiple pieces of Redux state.

```typescript
import { useSelector } from 'react-redux';
import { selectSubscriptionId } from '@redux/subscription/selectors';
import { selectCustomerId } from '@redux/customer/selectors';

export const useTrackCustomerReactivation = () => {
  // Select multiple values from Redux store
  const subscriptionId = useSelector(selectSubscriptionId);
  const customerId = useSelector(selectCustomerId);

  return {
    subscriptionId,
    customerId,
  };
};
```

**Key patterns:**
- Import selectors from centralized selector files
- Use `useSelector` hook instead of `connect` HOC
- Each `useSelector` call is separate (not combined in one selector)
- TypeScript infers types from selector return values

## Example 2: Thunk Actions with useFetch Integration

**File**: `app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/store/src/reactivation/actions.ts`

This example shows async thunk actions that integrate with the useFetch hook for API calls.

```typescript
import { ThunkAction } from 'redux-thunk';
import { RootState } from '../rootReducer';
import { ReactivationActionTypes } from './types';
import { useFetch } from '@/libs/fetch';

export const fetchReactivationData = (
  subscriptionId: string
): ThunkAction<Promise<void>, RootState, unknown, ReactivationActionTypes> => {
  return async (dispatch, getState) => {
    dispatch({ type: 'REACTIVATION_REQUEST' });

    try {
      const { fetch } = useFetch();
      const response = await fetch(`/api/reactivation/${subscriptionId}`);
      const data = await response.json();

      dispatch({
        type: 'REACTIVATION_SUCCESS',
        payload: data,
      });
    } catch (error) {
      dispatch({
        type: 'REACTIVATION_FAILURE',
        error: error.message,
      });
    }
  };
};
```

**Key patterns:**
- `ThunkAction` type with `<ReturnType, RootState, ExtraArgument, Actions>`
- Async/await for API calls
- Three-state pattern: REQUEST → SUCCESS | FAILURE
- Error handling with try/catch
- Dispatch multiple actions from one thunk

## Example 3: Immutable.js in Reducers

**File**: `app/spaces/legacy/modules/reactivate/reactivation/page/utils/filterBoltDeliveryDates.js`

This example shows Immutable.js usage in legacy Redux code for filtering delivery dates.

```typescript
import { List, Map } from 'immutable';

/**
 * Filter delivery dates based on bolt eligibility
 * @param {Map} deliveryDates - Immutable Map of delivery dates
 * @param {boolean} isBoltEligible - Whether user is eligible for bolt delivery
 * @returns {Map} Filtered delivery dates
 */
export const filterBoltDeliveryDates = (deliveryDates, isBoltEligible) => {
  if (!isBoltEligible) {
    // Filter out bolt-only delivery dates
    return deliveryDates.filter(date => !date.get('isBoltOnly'));
  }

  return deliveryDates;
};

// Usage in reducer
const reactivationReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'SET_DELIVERY_DATES':
      return state.set('deliveryDates', List(action.payload));

    case 'FILTER_BOLT_DATES':
      const filtered = filterBoltDeliveryDates(
        state.get('deliveryDates'),
        action.payload.isBoltEligible
      );
      return state.set('deliveryDates', filtered);

    default:
      return state;
  }
};
```

**Key patterns:**
- Immutable.js `Map` and `List` for state structure
- `.get()` method to access nested properties
- `.set()` method to update state immutably
- `.filter()` method for filtering collections
- Always return new Immutable instance, never mutate

## Example 4: Selector Functions

**File**: `app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/store/src/subscription/selectors.ts`

This example demonstrates creating reusable selector functions.

```typescript
import { RootState } from '../rootReducer';

/**
 * Select the current subscription ID
 */
export const selectSubscriptionId = (state: RootState): string | null => {
  return state.subscription?.id ?? null;
};

/**
 * Select subscription status
 */
export const selectSubscriptionStatus = (state: RootState): string => {
  return state.subscription?.status ?? 'unknown';
};

/**
 * Select whether subscription is active
 */
export const selectIsSubscriptionActive = (state: RootState): boolean => {
  const status = selectSubscriptionStatus(state);
  return status === 'active' || status === 'paused';
};

/**
 * Derived selector - composes other selectors
 */
export const selectCanReactivate = (state: RootState): boolean => {
  const status = selectSubscriptionStatus(state);
  const hasPaymentMethod = state.customer?.hasPaymentMethod ?? false;

  return status === 'cancelled' && hasPaymentMethod;
};
```

**Key patterns:**
- Export selector functions from centralized files
- Type selectors with `(state: RootState) => ReturnType`
- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Compose selectors (call other selectors inside selectors)
- Keep selectors pure (no side effects)
- Derive complex state from simpler selectors

## Example 5: useDispatch for Actions

**File**: `app/spaces/whitelabel/modules/whitelabel-web/packages/pages/settings/src/components/Reactivation/ReactivationButton.tsx`

This example shows dispatching actions with `useDispatch`.

```typescript
import { useDispatch, useSelector } from 'react-redux';
import { useCallback } from 'react';
import { reactivateSubscription } from '@redux/reactivation/actions';
import { selectSubscriptionId } from '@redux/subscription/selectors';

export const ReactivationButton = () => {
  const dispatch = useDispatch();
  const subscriptionId = useSelector(selectSubscriptionId);

  const handleReactivate = useCallback(() => {
    if (subscriptionId) {
      // Dispatch thunk action
      dispatch(reactivateSubscription(subscriptionId));
    }
  }, [dispatch, subscriptionId]);

  return (
    <button onClick={handleReactivate}>
      Reactivate Subscription
    </button>
  );
};
```

**Key patterns:**
- `useDispatch` hook returns dispatch function
- Wrap dispatch calls in `useCallback` for stable references
- Include `dispatch` in dependency array (though it's stable)
- Dispatch thunk actions directly (they return functions)
- Guard against null/undefined values before dispatching

## Example 6: Reducer Structure

**File**: `app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/store/src/reactivation/reducer.ts`

This example shows a typical Redux reducer structure.

```typescript
import { ReactivationState, ReactivationActionTypes } from './types';

const initialState: ReactivationState = {
  isLoading: false,
  error: null,
  data: null,
  deliveryDates: [],
};

export const reactivationReducer = (
  state = initialState,
  action: ReactivationActionTypes
): ReactivationState => {
  switch (action.type) {
    case 'REACTIVATION_REQUEST':
      return {
        ...state,
        isLoading: true,
        error: null,
      };

    case 'REACTIVATION_SUCCESS':
      return {
        ...state,
        isLoading: false,
        data: action.payload,
        error: null,
      };

    case 'REACTIVATION_FAILURE':
      return {
        ...state,
        isLoading: false,
        error: action.error,
      };

    case 'SET_DELIVERY_DATES':
      return {
        ...state,
        deliveryDates: action.payload,
      };

    case 'RESET_REACTIVATION':
      return initialState;

    default:
      return state;
  }
};
```

**Key patterns:**
- Always return new state object (spread operator)
- Never mutate state directly
- Three-state async pattern (loading, success, failure)
- Reset actions return initialState
- Type action parameter with union type
- Always have default case that returns state

## Common Anti-Patterns

### ❌ Mutating State Directly

```typescript
// DON'T: Mutate state
case 'ADD_ITEM':
  state.items.push(action.payload); // Mutation!
  return state;

// DO: Return new state
case 'ADD_ITEM':
  return {
    ...state,
    items: [...state.items, action.payload],
  };
```

### ❌ Using connect HOC Instead of Hooks

```typescript
// DON'T: Old connect pattern
import { connect } from 'react-redux';

const MyComponent = ({ subscriptionId }) => {
  return <div>{subscriptionId}</div>;
};

export default connect(
  (state) => ({ subscriptionId: state.subscription.id })
)(MyComponent);

// DO: Use hooks
import { useSelector } from 'react-redux';

export const MyComponent = () => {
  const subscriptionId = useSelector(selectSubscriptionId);
  return <div>{subscriptionId}</div>;
};
```

### ❌ Not Typing Redux State

```typescript
// DON'T: No types
const subscriptionId = useSelector((state) => state.subscription.id);

// DO: Type with RootState
import { RootState } from '@redux/rootReducer';
const subscriptionId = useSelector((state: RootState) => state.subscription.id);

// BETTER: Use selector functions
const subscriptionId = useSelector(selectSubscriptionId);
```

### ❌ Dispatching Inside Reducers

```typescript
// DON'T: Side effects in reducers
case 'SAVE_DATA':
  fetch('/api/save', { data: action.payload }); // Side effect!
  return { ...state, data: action.payload };

// DO: Side effects in thunks
export const saveData = (data) => async (dispatch) => {
  dispatch({ type: 'SAVE_REQUEST' });
  await fetch('/api/save', { data });
  dispatch({ type: 'SAVE_SUCCESS' });
};
```

## Summary

The YourCompany web codebase uses Redux 4 with these consistent patterns:

1. **Hooks over HOCs** - Always use `useSelector` and `useDispatch`, never `connect`
2. **Centralized selectors** - Export selector functions from selector files
3. **Thunk actions** - Use redux-thunk for async operations
4. **Three-state async** - REQUEST → SUCCESS | FAILURE pattern
5. **Immutability** - Never mutate state, always return new objects
6. **Immutable.js** - Used in legacy code for complex state transformations
7. **TypeScript** - Type RootState, actions, and reducers
8. **Selector composition** - Build complex selectors from simpler ones
9. **useCallback** - Wrap dispatch calls in useCallback for stable references

**Key Libraries:**
- Redux 4.x
- react-redux 4.4.10
- redux-thunk for async actions
- Immutable.js (legacy code)
- TypeScript 5.7.3

For additional patterns, see the Redux 4 documentation: https://redux.js.org/
