---
name: redux-patterns-web
description: "WHAT: Redux 4 patterns with selectors, reducers, and thunk actions for web. WHEN: accessing Redux store, creating state slices, dispatching actions. KEYWORDS: redux, selector, reducer, thunk, useSelector, useDispatch, action, web, store, v4.4.10."
---

# Redux Patterns - Web

Redux 4 with react-redux v4.4.10 for managing application state in Next.js web applications. This skill covers traditional Redux patterns including selectors, reducers, thunk actions, and React hooks integration.

## When to Use

Use this skill when:
- Managing global application state that needs to be shared across multiple components
- Working with the existing Redux store in the web codebase
- Creating new slices of state following established Redux patterns
- Selecting data from the Redux store in React components
- Dispatching actions to update state

## Core Principles

### Principle 1: Use Selectors to Access State

**Selectors are pure functions that extract specific data from the Redux store.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/store/src/customer/subscription/selectors/subscriptions.js
import { selectCustomerExists } from '../../customerData/selectors';

export const selectSubscription = (state) => {
  const subscription = get(state.customer, ['subscription', 'item']);
  return subscription ? subscription : {};
};

export const selectHasSubscription = (state) =>
  selectSubscription(state).hasSubscription || false;

export const selectSubscriptionId = (state) =>
  getSubscriptionId(selectSubscription(state));

// Composed selector using other selectors
export const selectSubscriptionIsActive = (state) =>
  selectHasSubscription(state) &&
  isSubscriptionActive(selectSubscription(state));
```

❌ **Bad:**
```typescript
// Accessing state directly in component
const Component = () => {
  const subscription = useSelector(state => state.customer.subscription.item);
  // ❌ Direct state access, not reusable
};

// Non-memoized complex selector
export const selectExpensiveData = (state) => {
  return state.items.map(item => /* expensive computation */);
  // ❌ Runs on every state change, should use reselect
};
```

**Why:** Selectors provide a single source of truth for accessing state, enable composition, and can be easily tested. They decouple components from the store structure.

### Principle 2: Use Switch-Based Reducers with TypeScript

**Reducers handle actions and return new state using switch statements.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/store/src/additionalVouchers/reducer.ts
import { ADDITIONAL_VOUCHERS_SET } from './constants';

import type {
  AdditionalVouchersAction,
  AdditionalVouchersState,
} from './types';

export const initialState: AdditionalVouchersState = {
  isLoaded: false,
  items: null,
};

export default (
  state: AdditionalVouchersState = initialState,
  { type, payload }: AdditionalVouchersAction
) => {
  switch (type) {
    case ADDITIONAL_VOUCHERS_SET:
      return {
        ...state,
        isLoaded: true,
        items: payload,
      };

    default:
      return state;
  }
};
```

❌ **Bad:**
```typescript
// Mutating state directly
export default (state = initialState, action) => {
  switch (action.type) {
    case SET_DATA:
      state.items = action.payload;  // ❌ Mutation!
      return state;
  }
};

// Missing default case
export default (state = initialState, action) => {
  switch (action.type) {
    case SET_DATA:
      return { ...state, items: action.payload };
    // ❌ No default case
  }
};
```

**Why:** Redux requires immutable updates. The spread operator ensures new state objects are created. The default case ensures the reducer returns state for unknown actions.

### Principle 3: Use Thunk Actions for Async Operations

**Thunk actions enable async logic by returning functions that receive dispatch and getState.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/store/src/additionalVouchers/actions.ts
import { requestAdditionalVoucher } from '@/whitelabel-libraries/gateway/src/api/vouchers/vouchers';
import { selectSubscriptionId } from '../customer/subscription/selectors/subscriptions';
import { ADDITIONAL_VOUCHERS_SET } from './constants';

import type { Dispatch } from 'react';
import type { AxiosClient } from '@/whitelabel-libraries/gateway/src/client/AxiosClient';
import type {
  AdditionalVouchersAction,
  AdditionalVoucherResult,
} from './types';

type GetState = () => { [key: string]: string };

export const fetchSubscriptionAdditionalVoucher =
  () =>
  async (
    dispatch: Dispatch<AdditionalVouchersAction>,
    getState: GetState,
    { gwClient }: { gwClient: AxiosClient }
  ) => {
    const subscriptionId = selectSubscriptionId(getState());
    let additionalVouchers: AdditionalVoucherResult;

    try {
      const response = await requestAdditionalVoucher(gwClient, {
        subscriptionId,
      });

      additionalVouchers = response.data;
    } catch (err) {
      // when subscription doesnt have additional vouchers, endpoint returns 404
      additionalVouchers = [];
    }

    dispatch({
      type: ADDITIONAL_VOUCHERS_SET,
      payload: additionalVouchers,
    });
  };
```

❌ **Bad:**
```typescript
// Async logic in component
const Component = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(data => dispatch({ type: 'SET_DATA', payload: data }));
    // ❌ API logic in component, hard to test
  }, []);
};

// Not handling errors
export const fetchData = () => async (dispatch) => {
  const response = await fetch('/api/data');
  dispatch({ type: 'SET_DATA', payload: response.data });
  // ❌ No error handling
};
```

**Why:** Thunk actions centralize async logic, making it reusable and testable. They can access the current state via getState() and dispatch multiple actions as needed.

### Principle 4: Use React-Redux Hooks in Components

**Use useSelector and useDispatch hooks to connect components to Redux.**

✅ **Good:**
```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/components/reactivation-success-dialog/BoxTotal.tsx
import React from 'react';
import { useSelector } from 'react-redux';
import {
  selectSubscription,
  getSubscriptionProductSku,
} from '@/whitelabel-libraries/store/src/customer/subscription';
import { selectReactivationSelectedSKU } from '@/whitelabel-libraries/store/src/reactivation/selectors';

export const BoxTotal: React.FC = () => {
  const selectedReactivationSKU = useSelector(selectReactivationSelectedSKU);
  const subscription = useSelector(selectSubscription);
  const currentPlanSKU = getSubscriptionProductSku(subscription);
  const selectedSKU = selectedReactivationSKU || currentPlanSKU;

  return (
    <div>
      <Text>{selectedSKU}</Text>
    </div>
  );
};
```

```typescript
// app/spaces/whitelabel/modules/whitelabel-web/packages/libraries/store/src/customer/subscription/hooks/useSubscriptionId.ts
import { useSelector } from 'react-redux';
import { selectSubscriptionId } from '../selectors/subscriptions';

export const useSubscriptionId = (): string =>
  useSelector(selectSubscriptionId);
```

❌ **Bad:**
```typescript
import { connect } from 'react-redux';

// Using legacy connect() HOC
const Component = ({ subscription }) => {
  return <div>{subscription.id}</div>;
};

export default connect(
  state => ({ subscription: state.customer.subscription })
)(Component);
// ❌ Prefer hooks over connect()
```

**Why:** Hooks provide a simpler, more direct way to interact with Redux compared to the legacy connect() HOC. They're easier to type with TypeScript and result in less boilerplate.

### Principle 5: Organize Store by Domain

**Structure Redux code by feature/domain, not by type (actions, reducers, etc.).**

✅ **Good:**
```
store/
├── customer/
│   └── subscription/
│       ├── selectors/
│       │   └── subscriptions.js
│       ├── hooks/
│       │   └── useSubscriptionId.ts
│       └── constants.ts
├── additionalVouchers/
│   ├── reducer.ts
│   ├── actions.ts
│   ├── selectors.ts
│   ├── types.ts
│   ├── constants.ts
│   └── hooks/
│       └── useAdditionalVoucher.ts
└── priceBreakdown/
    ├── reducer/
    │   └── reducePriceBreakdown.ts
    ├── actions/
    │   └── fetchPriceBreakdown.ts
    ├── types.ts
    └── hooks/
        └── usePriceBreakdownTotals.ts
```

❌ **Bad:**
```
store/
├── actions/
│   ├── subscription.ts
│   ├── vouchers.ts
│   └── price.ts
├── reducers/
│   ├── subscription.ts
│   ├── vouchers.ts
│   └── price.ts
└── selectors/
    ├── subscription.ts
    └── vouchers.ts
// ❌ Organized by type, harder to find related code
```

**Why:** Organizing by domain keeps related code together, making it easier to understand and maintain features. This is especially important in large applications.

## Type Definitions

### Action Types

```typescript
// Define action types
export const ADDITIONAL_VOUCHERS_SET = 'ADDITIONAL_VOUCHERS_SET';

// Type the action
export type AdditionalVouchersAction = {
  type: typeof ADDITIONAL_VOUCHERS_SET;
  payload: AdditionalVoucherResult;
};
```

### State Types

```typescript
export type AdditionalVouchersState = {
  isLoaded: boolean;
  items: AdditionalVoucherResult | null;
};
```

### Thunk Types

```typescript
import type { Dispatch } from 'react';
import type { AxiosClient } from '@/whitelabel-libraries/gateway/src/client/AxiosClient';

type GetState = () => RootState;

// Thunk action creator
export const fetchData = () => async (
  dispatch: Dispatch<MyAction>,
  getState: GetState,
  { gwClient }: { gwClient: AxiosClient }
) => {
  // Implementation
};
```

## Legacy Code Patterns

### Immutable.js Usage

Some legacy code uses Immutable.js for state management:

```javascript
// In tests - app/spaces/auth/modules/login/components/app-install-login/AppInstallWrapper.test.tsx
import { fromJS } from 'immutable';

const mockState = fromJS({
  customer: {
    subscription: {
      item: { id: '123' }
    }
  }
});
```

**Note:** New code should avoid Immutable.js and use plain JavaScript objects with immutable update patterns (spread operator, etc.).

## Common Mistakes

### 1. Mutating State

```typescript
// ❌ Wrong
const reducer = (state = initialState, action) => {
  state.items.push(action.payload);  // Mutation!
  return state;
};

// ✅ Correct
const reducer = (state = initialState, action) => {
  return {
    ...state,
    items: [...state.items, action.payload]
  };
};
```

### 2. Not Handling Errors in Thunks

```typescript
// ❌ Wrong
export const fetchData = () => async (dispatch) => {
  const response = await fetch('/api/data');  // Can throw!
  dispatch({ type: 'SET_DATA', payload: response.data });
};

// ✅ Correct
export const fetchData = () => async (dispatch) => {
  try {
    const response = await fetch('/api/data');
    dispatch({ type: 'SET_DATA', payload: response.data });
  } catch (error) {
    dispatch({ type: 'SET_ERROR', payload: error.message });
  }
};
```

### 3. Creating Selectors in useSelector

```typescript
// ❌ Wrong - Creates new selector on every render
const data = useSelector(state =>
  state.items.map(item => ({ ...item, computed: item.a + item.b }))
);

// ✅ Correct - Use memoized selector
const selectComputedData = createSelector(
  state => state.items,
  items => items.map(item => ({ ...item, computed: item.a + item.b }))
);

const data = useSelector(selectComputedData);
```

### 4. Not Exporting initialState

```typescript
// ❌ Wrong - Can't test reducer easily
const reducer = (state = { items: [] }, action) => {
  // ...
};

// ✅ Correct - Export for testing
export const initialState = { items: [] };

const reducer = (state = initialState, action) => {
  // ...
};
```

## Testing

### Testing Reducers

```typescript
import reducer, { initialState } from './reducer';
import { ADDITIONAL_VOUCHERS_SET } from './constants';

describe('additionalVouchers reducer', () => {
  it('should handle ADDITIONAL_VOUCHERS_SET', () => {
    const action = {
      type: ADDITIONAL_VOUCHERS_SET,
      payload: [{ id: '1', code: 'ABC123' }]
    };

    const result = reducer(initialState, action);

    expect(result.isLoaded).toBe(true);
    expect(result.items).toEqual(action.payload);
  });

  it('should return state for unknown actions', () => {
    const result = reducer(initialState, { type: 'UNKNOWN' });
    expect(result).toBe(initialState);
  });
});
```

### Testing Selectors

```typescript
import { selectSubscriptionId, selectHasSubscription } from './selectors';

describe('subscription selectors', () => {
  it('should select subscription ID', () => {
    const state = {
      customer: {
        subscription: {
          item: { id: '12345', hasSubscription: true }
        }
      }
    };

    expect(selectSubscriptionId(state)).toBe('12345');
    expect(selectHasSubscription(state)).toBe(true);
  });
});
```

### Testing Thunks

```typescript
import { fetchSubscriptionAdditionalVoucher } from './actions';

describe('fetchSubscriptionAdditionalVoucher', () => {
  it('should dispatch vouchers on success', async () => {
    const dispatch = jest.fn();
    const getState = () => ({
      customer: { subscription: { item: { id: '123' } } }
    });
    const gwClient = {
      get: jest.fn().mockResolvedValue({ data: [{ code: 'ABC' }] })
    };

    await fetchSubscriptionAdditionalVoucher()(
      dispatch,
      getState,
      { gwClient }
    );

    expect(dispatch).toHaveBeenCalledWith({
      type: 'ADDITIONAL_VOUCHERS_SET',
      payload: [{ code: 'ABC' }]
    });
  });
});
```

## Quick Reference

### Create a Selector

```typescript
export const selectData = (state) => state.domain.data;
```

### Create a Reducer

```typescript
export const initialState = { items: [], isLoaded: false };

export default (state = initialState, { type, payload }) => {
  switch (type) {
    case ACTION_TYPE:
      return { ...state, items: payload, isLoaded: true };
    default:
      return state;
  }
};
```

### Create a Thunk Action

```typescript
export const fetchData = () => async (dispatch, getState, { gwClient }) => {
  try {
    const response = await gwClient.get('/api/data');
    dispatch({ type: 'SET_DATA', payload: response.data });
  } catch (error) {
    dispatch({ type: 'SET_ERROR', payload: error });
  }
};
```

### Use in Component

```typescript
import { useSelector, useDispatch } from 'react-redux';
import { selectData } from './selectors';
import { fetchData } from './actions';

export const Component = () => {
  const data = useSelector(selectData);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchData());
  }, [dispatch]);

  return <div>{data}</div>;
};
```
