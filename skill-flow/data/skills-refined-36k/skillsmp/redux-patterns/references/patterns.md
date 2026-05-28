# Redux Implementation Patterns

Implementation patterns and anti-patterns for Redux 4 state management.

## Pattern: Three-State Async Pattern

Use loading, success, and error states for async operations.

✅ **Good:**
```typescript
type AsyncState<T> = {
  data: T | null;
  isLoading: boolean;
  error: string | null;
};

const initialState: AsyncState<User> = {
  data: null,
  isLoading: false,
  error: null,
};

type Action =
  | { type: 'FETCH_REQUEST' }
  | { type: 'FETCH_SUCCESS'; payload: User }
  | { type: 'FETCH_ERROR'; error: string };

const userReducer = (state = initialState, action: Action) => {
  switch (action.type) {
    case 'FETCH_REQUEST':
      return { ...state, isLoading: true, error: null };
    case 'FETCH_SUCCESS':
      return { ...state, isLoading: false, data: action.payload, error: null };
    case 'FETCH_ERROR':
      return { ...state, isLoading: false, error: action.error };
    default:
      return state;
  }
};
```

❌ **Bad:**
```typescript
// Only success state - can't show loading or errors
type State = {
  user: User | null;
};

// Mixing loading and error states
type State = {
  user: User | null;
  status: 'idle' | 'loading' | 'success' | 'error';
  error?: string; // Error could exist with status='success'
};
```

**Why:** Three-state pattern ensures:
- Clear loading state for spinners
- Error state for error messages
- Success state for data display
- No invalid combinations (loading + data, error + data)

**When to use:**
- Any async operation (API calls, file loading)
- Operations that can fail
- User-initiated actions that take time

## Pattern: Selector Functions

Export reusable selector functions instead of accessing state directly.

✅ **Good:**
```typescript
// selectors.ts
export const selectUser = (state: RootState) => state.user;
export const selectUserId = (state: RootState) => state.user?.id;
export const selectIsLoggedIn = (state: RootState) =>
  state.user !== null && state.user.id !== '';

// Component
import { useSelector } from 'react-redux';
import { selectUser, selectIsLoggedIn } from './selectors';

const MyComponent = () => {
  const user = useSelector(selectUser);
  const isLoggedIn = useSelector(selectIsLoggedIn);

  return <div>{user.name}</div>;
};
```

❌ **Bad:**
```typescript
// Accessing state directly in components
const MyComponent = () => {
  const user = useSelector((state) => state.user);
  const isLoggedIn = useSelector(
    (state) => state.user !== null && state.user.id !== ''
  );

  return <div>{user.name}</div>;
};
```

**Why:** Selector functions:
- Centralize state access logic
- Reusable across components
- Easy to test
- Easy to refactor (change state shape once)
- TypeScript auto-completion

## Pattern: Thunk for Async Logic

Use thunk actions for async operations and side effects.

✅ **Good:**
```typescript
import { ThunkAction } from 'redux-thunk';

export const fetchUser = (userId: string): ThunkAction<Promise<void>, RootState, unknown, Action> => {
  return async (dispatch, getState) => {
    dispatch({ type: 'FETCH_USER_REQUEST' });

    try {
      const response = await fetch(`/api/user/${userId}`);
      const user = await response.json();

      dispatch({ type: 'FETCH_USER_SUCCESS', payload: user });
    } catch (error) {
      dispatch({ type: 'FETCH_USER_ERROR', error: error.message });
    }
  };
};

// Usage
const MyComponent = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchUser('123'));
  }, [dispatch]);
};
```

❌ **Bad:**
```typescript
// Async logic in component
const MyComponent = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    const loadUser = async () => {
      dispatch({ type: 'FETCH_USER_REQUEST' });
      try {
        const response = await fetch('/api/user/123');
        const user = await response.json();
        dispatch({ type: 'FETCH_USER_SUCCESS', payload: user });
      } catch (error) {
        dispatch({ type: 'FETCH_USER_ERROR', error: error.message });
      }
    };
    loadUser();
  }, [dispatch]);
};
```

**Why:** Thunks:
- Centralize async logic
- Reusable across components
- Easier to test
- Access to `getState` for conditional logic
- Handle errors consistently

## Pattern: Discriminated Union Actions

Use discriminated union types for type-safe actions.

✅ **Good:**
```typescript
type CounterAction =
  | { type: 'INCREMENT' }
  | { type: 'DECREMENT' }
  | { type: 'SET'; payload: number }
  | { type: 'RESET' };

const counterReducer = (state: State, action: CounterAction): State => {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 };
    case 'SET':
      // TypeScript knows action.payload exists here
      return { count: action.payload };
    default:
      return state;
  }
};
```

❌ **Bad:**
```typescript
// Loose action type
type Action = {
  type: string;
  payload?: any;
};

const counterReducer = (state: State, action: Action) => {
  switch (action.type) {
    case 'SET':
      // No type safety for payload
      return { count: action.payload };
  }
};
```

**Why:** Discriminated unions:
- TypeScript narrows types in switch cases
- Compile-time checking for payload types
- Autocomplete for action types
- Prevents typos in action types

## Pattern: Immutable Updates with Spread

Always return new objects - never mutate state.

✅ **Good:**
```typescript
// Update top-level property
case 'SET_NAME':
  return { ...state, name: action.payload };

// Update nested property
case 'SET_ADDRESS':
  return {
    ...state,
    user: {
      ...state.user,
      address: action.payload,
    },
  };

// Update array - add item
case 'ADD_ITEM':
  return { ...state, items: [...state.items, action.payload] };

// Update array - remove item
case 'REMOVE_ITEM':
  return {
    ...state,
    items: state.items.filter(item => item.id !== action.payload),
  };

// Update array - modify item
case 'UPDATE_ITEM':
  return {
    ...state,
    items: state.items.map(item =>
      item.id === action.payload.id
        ? { ...item, ...action.payload.updates }
        : item
    ),
  };
```

❌ **Bad:**
```typescript
// Mutating state directly
case 'SET_NAME':
  state.name = action.payload; // Mutation!
  return state;

// Mutating nested object
case 'SET_ADDRESS':
  state.user.address = action.payload;
  return state;

// Mutating array
case 'ADD_ITEM':
  state.items.push(action.payload);
  return state;
```

**Why:** Immutable updates:
- Redux relies on reference equality
- Mutation breaks Redux DevTools time-travel
- React won't detect changes
- Leads to subtle bugs

## Pattern: Normalized State

Store collections as objects with IDs as keys, not arrays.

✅ **Good:**
```typescript
type State = {
  users: {
    byId: { [id: string]: User };
    allIds: string[];
  };
};

const initialState: State = {
  users: {
    byId: {},
    allIds: [],
  },
};

// Add user
case 'ADD_USER':
  return {
    ...state,
    users: {
      byId: {
        ...state.users.byId,
        [action.payload.id]: action.payload,
      },
      allIds: [...state.users.allIds, action.payload.id],
    },
  };

// Update user (O(1) lookup)
case 'UPDATE_USER':
  return {
    ...state,
    users: {
      ...state.users,
      byId: {
        ...state.users.byId,
        [action.payload.id]: {
          ...state.users.byId[action.payload.id],
          ...action.payload.updates,
        },
      },
    },
  };

// Selector
export const selectUserById = (state: RootState, userId: string) =>
  state.users.byId[userId];
```

❌ **Bad:**
```typescript
type State = {
  users: User[]; // Array - O(n) lookups
};

// Find user (O(n) operation)
case 'UPDATE_USER':
  return {
    ...state,
    users: state.users.map(user =>
      user.id === action.payload.id
        ? { ...user, ...action.payload.updates }
        : user
    ),
  };
```

**Why:** Normalized state:
- O(1) lookups by ID
- Prevents duplicate data
- Easier to update
- Standard Redux pattern

## Pattern: Composed Selectors

Build complex selectors from simpler ones.

✅ **Good:**
```typescript
// Base selectors
export const selectUsers = (state: RootState) => state.users;
export const selectCurrentUserId = (state: RootState) => state.currentUserId;

// Composed selector
export const selectCurrentUser = (state: RootState) => {
  const users = selectUsers(state);
  const userId = selectCurrentUserId(state);
  return users.find(u => u.id === userId);
};

// Derived selector
export const selectCurrentUserName = (state: RootState) => {
  const user = selectCurrentUser(state);
  return user ? user.name : 'Guest';
};
```

❌ **Bad:**
```typescript
// Duplicate logic across selectors
export const selectCurrentUser = (state: RootState) =>
  state.users.find(u => u.id === state.currentUserId);

export const selectCurrentUserName = (state: RootState) =>
  state.users.find(u => u.id === state.currentUserId)?.name ?? 'Guest';
```

**Why:** Composed selectors:
- DRY principle
- Single source of truth
- Easier to refactor
- Reusable logic

## Pattern: Action Creator Functions

Export action creator functions for consistency.

✅ **Good:**
```typescript
// Action creators
export const increment = () => ({ type: 'INCREMENT' as const });
export const decrement = () => ({ type: 'DECREMENT' as const });
export const set = (value: number) => ({
  type: 'SET' as const,
  payload: value,
});

// Usage
dispatch(increment());
dispatch(set(10));
```

❌ **Bad:**
```typescript
// Inline action objects
dispatch({ type: 'INCREMENT' }); // Typo risk
dispatch({ type: 'SET', payload: 10 }); // No validation
```

**Why:** Action creators:
- Prevent typos
- Centralize action creation
- Type-safe payloads
- Easy to test

## Pattern: useCallback for Dispatch

Wrap dispatch calls in useCallback for stable references.

✅ **Good:**
```typescript
import { useCallback } from 'react';
import { useDispatch } from 'react-redux';

const MyComponent = () => {
  const dispatch = useDispatch();

  const handleIncrement = useCallback(() => {
    dispatch(increment());
  }, [dispatch]);

  const handleSet = useCallback((value: number) => {
    dispatch(set(value));
  }, [dispatch]);

  return (
    <>
      <button onClick={handleIncrement}>+</button>
      <ChildComponent onSet={handleSet} />
    </>
  );
};
```

❌ **Bad:**
```typescript
// New function on every render
const MyComponent = () => {
  const dispatch = useDispatch();

  return (
    <>
      <button onClick={() => dispatch(increment())}>+</button>
      <ChildComponent onSet={(value) => dispatch(set(value))} />
    </>
  );
};
```

**Why:** useCallback:
- Stable function reference
- Prevents child re-renders
- Better performance
- Cleaner dependency arrays

## Anti-Pattern: Side Effects in Reducers

Never perform side effects in reducers.

❌ **Bad:**
```typescript
const reducer = (state, action) => {
  switch (action.type) {
    case 'SAVE_USER':
      // API call in reducer - wrong!
      fetch('/api/user', { method: 'POST', body: JSON.stringify(action.payload) });
      return { ...state, user: action.payload };

    case 'LOG_ACTION':
      // Logging in reducer - side effect!
      console.log('Action:', action.type);
      return state;
  }
};
```

✅ **Good:**
```typescript
// Side effects in thunk
export const saveUser = (user: User): AppThunk => {
  return async (dispatch) => {
    dispatch({ type: 'SAVE_USER_REQUEST' });

    try {
      await fetch('/api/user', {
        method: 'POST',
        body: JSON.stringify(user),
      });

      dispatch({ type: 'SAVE_USER_SUCCESS', payload: user });
    } catch (error) {
      dispatch({ type: 'SAVE_USER_ERROR', error: error.message });
    }
  };
};

// Pure reducer
const reducer = (state, action) => {
  switch (action.type) {
    case 'SAVE_USER_SUCCESS':
      return { ...state, user: action.payload };
    default:
      return state;
  }
};
```

**Why:** Reducers must be pure:
- Predictable behavior
- Time-travel debugging
- Server-side rendering
- Testing

## Anti-Pattern: Using connect HOC

Don't use `connect` HOC - use hooks instead.

❌ **Bad:**
```typescript
import { connect } from 'react-redux';

const MyComponent = ({ user, increment }) => (
  <div>
    {user.name}
    <button onClick={increment}>+</button>
  </div>
);

const mapStateToProps = (state) => ({
  user: state.user,
});

const mapDispatchToProps = {
  increment,
};

export default connect(mapStateToProps, mapDispatchToProps)(MyComponent);
```

✅ **Good:**
```typescript
import { useSelector, useDispatch } from 'react-redux';

export const MyComponent = () => {
  const user = useSelector(selectUser);
  const dispatch = useDispatch();

  return (
    <div>
      {user.name}
      <button onClick={() => dispatch(increment())}>+</button>
    </div>
  );
};
```

**Why:** Hooks are:
- Simpler syntax
- Better TypeScript support
- Easier to test
- Standard modern React

## Summary

**Key Patterns:**
- Three-state async (loading, success, error)
- Selector functions (reusable, testable)
- Thunks for async logic
- Discriminated union actions
- Immutable updates with spread
- Normalized state (byId + allIds)
- Composed selectors
- Action creator functions
- useCallback for dispatch

**Anti-Patterns to Avoid:**
- Mutating state
- Side effects in reducers
- Using connect HOC
- Inline action objects
- Array-based collections
- Missing default case
- any types
