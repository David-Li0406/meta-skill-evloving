---
name: redux-patterns
description: "WHAT: Redux 4 state management with react-redux hooks and reducers. WHEN: global state, complex state logic, state persistence across routes. KEYWORDS: redux, useSelector, useDispatch, reducer, thunk, selector, action, Immutable.js, web."
---

# Redux Patterns - Web

Redux state management patterns for the React web application using Redux 4 and react-redux 4.4.10.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use Redux for:
- Global application state that multiple components need
- Complex state logic that benefits from predictable state containers
- State that persists across route changes
- State that needs to be easily testable in isolation

## Core Principles

### 1. Use Hooks Over Connect

**Prefer useSelector and useDispatch hooks for accessing Redux state.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/pages/settings/src/components/Reactivation/hooks/useTrackCustomerReactivation.ts:1
import { useSelector } from 'react-redux';
import { selectSubscriptionId } from '@/whitelabel-libraries/store/src/customer/subscription';
import { selectCustomerId } from '@/whitelabel-libraries/store/src/customer/customerData/selectors';

export const useTrackCustomerReactivation = () => {
  const subscriptionId = useSelector(selectSubscriptionId);
  const customerId = useSelector(selectCustomerId);
  const selectedSKU = useSelector(selectReactivationSelectedSKU);

  // Use the selected state...
};
```

❌ **Bad:**
```typescript
// Don't use connect HOC for new components
import { connect } from 'react-redux';

const mapStateToProps = (state) => ({
  subscriptionId: state.customer.subscriptionId,
});

export default connect(mapStateToProps)(MyComponent);
```

**Why:** Hooks provide better TypeScript support, are easier to test, and reduce boilerplate compared to the connect HOC.

### 2. Type-Safe Reducers

**Define reducers with explicit TypeScript types for state and actions.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/store/src/router/routerReducer.ts:1
import type { Reducer } from 'redux';
import type { RouterState, SetRouterInfoAction } from './types';

const defaultState: RouterState = {
  pathname: '',
  query: {},
  prev: {},
};

export const routerReducer: Reducer<RouterState, SetRouterInfoAction> = (
  state = defaultState,
  action
) => {
  if (action.type !== 'SET_ROUTER_INFO') {
    return state;
  }

  const { pathname, query } = action.payload;

  return {
    pathname,
    query,
    prev: {
      pathname: state.pathname,
      query: state.query,
    },
  };
};
```

**Why:** Type-safe reducers catch errors at compile time and provide autocomplete for action payloads.

### 3. Thunk Action Creators

**Use thunk pattern for async actions and side effects.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/store/src/reactivation/actions.ts:1
import type { Dispatch } from 'redux';
import { SET_SELECTED_REACTIVATION_SKU } from './types';

export const setSelectedReactivationSKU =
  (sku: string) => (dispatch: Dispatch) => {
    return dispatch({ type: SET_SELECTED_REACTIVATION_SKU, payload: sku });
  };
```

**Why:** Thunks allow you to dispatch multiple actions, perform async logic, and access getState before dispatching.

### 4. Selector Functions

**Create selector functions to encapsulate state access logic.**

✅ **Good:**
```typescript
// Define selectors in separate files
export const selectSubscriptionId = (state: RootState) =>
  state.customer.subscription.id;

export const selectCustomerId = (state: RootState) =>
  state.customer.customerData.id;

// Use in components
const subscriptionId = useSelector(selectSubscriptionId);
const customerId = useSelector(selectCustomerId);
```

❌ **Bad:**
```typescript
// Don't access state structure directly in components
const subscriptionId = useSelector(state => state.customer.subscription.id);
```

**Why:** Selectors centralize state access logic, make refactoring easier, and enable memoization.

## Working with Immutable.js

### Legacy Code Patterns

**Some legacy code uses Immutable.js for state management.**

✅ **Example:**
```javascript
// app/spaces/legacy/modules/reactivate/reactivation/page/utils/filterBoltDeliveryDates.js:1
import { fromJS } from 'immutable';

export const filterBoltDates = (possibleDates, isInBoltExperimentVariation) => {
  let deliveryOptions;

  if (isInBoltExperimentVariation) {
    deliveryOptions = possibleDates?.map((option) =>
      fromJS({
        deliveryDate: option?.get('deliveryDate'),
        deliveryOptions: option
          ?.get('deliveryOptions')
          .filter((o) => o?.get('handle').includes('BOLT')),
      })
    );

    const hasBoltDates = deliveryOptions.some(
      (option) => option.get('deliveryOptions').size > 0
    );

    if (hasBoltDates) {
      return deliveryOptions;
    }
  }

  return deliveryOptions;
};
```

**Why:** Immutable.js ensures data immutability in legacy code, but new code should use plain JavaScript objects with TypeScript readonly types.

## Testing Redux

### Mock Store for Tests

**Use redux-mock-store or createStore for testing components with Redux.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/pages/settings/src/pages/PlanSettings.spec.tsx:4
import { createStore } from 'redux';
import { Provider } from 'react-redux';

const mockState = {
  customer: {
    subscriptionId: 'test-123',
    customerId: 'customer-456',
  },
};

const mockStore = createStore(() => mockState);

render(
  <Provider store={mockStore}>
    <PlanSettings />
  </Provider>
);
```

**Why:** Mock stores allow you to test components in isolation without the full Redux setup.

## File Organization

```
store/
├── customer/
│   ├── subscription/
│   │   ├── selectors.ts      # Selector functions
│   │   └── types.ts          # Type definitions
│   └── customerData/
│       └── selectors.ts
├── reactivation/
│   ├── actions.ts            # Action creators
│   ├── selectors.ts          # Selectors
│   └── types.ts              # Action types
└── router/
    ├── routerReducer.ts      # Reducer
    └── types.ts              # State/action types
```

## Common Mistakes

1. **Using connect HOC in new code** - Use hooks instead (useSelector, useDispatch)
2. **Inline state selectors** - Create reusable selector functions
3. **Missing TypeScript types** - Always type your reducers, actions, and state
4. **Mutating state** - Return new objects, don't modify existing state
5. **Not memoizing selectors** - Use reselect for expensive derived state

## Quick Reference

### Basic Patterns

```typescript
// Selector
export const selectValue = (state: RootState) => state.feature.value;

// Hook usage
const value = useSelector(selectValue);
const dispatch = useDispatch();

// Action creator (thunk)
export const updateValue = (newValue: string) => (dispatch: Dispatch) => {
  dispatch({ type: 'UPDATE_VALUE', payload: newValue });
};

// Dispatch action
dispatch(updateValue('new value'));

// Reducer
export const reducer: Reducer<State, Action> = (state = initialState, action) => {
  switch (action.type) {
    case 'UPDATE_VALUE':
      return { ...state, value: action.payload };
    default:
      return state;
  }
};
```

### Testing

```typescript
// Mock store
import { createStore } from 'redux';
const mockStore = createStore(() => mockState);

// Wrap component
<Provider store={mockStore}>
  <Component />
</Provider>
```
