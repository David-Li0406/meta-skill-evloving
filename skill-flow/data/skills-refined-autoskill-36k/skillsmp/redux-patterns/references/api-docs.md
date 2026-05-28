# Redux API Reference

**Versions**: Redux 4.x, react-redux 4.4.10, redux-thunk 2.x

## Official Documentation

- **Redux Core**: https://redux.js.org/
- **React Redux**: https://react-redux.js.org/
- **Redux Toolkit**: https://redux-toolkit.js.org/ (not used in this codebase)
- **Redux Thunk**: https://github.com/reduxjs/redux-thunk

## React Redux Hooks API

### useSelector

Read data from the Redux store.

```typescript
import { useSelector } from 'react-redux';
import { RootState } from '@redux/rootReducer';

// Basic selector
const value = useSelector((state: RootState) => state.user.name);

// With selector function
const selectUserName = (state: RootState) => state.user.name;
const name = useSelector(selectUserName);

// Multiple values
const { count, text } = useSelector((state: RootState) => ({
  count: state.counter.count,
  text: state.counter.text,
}));
```

**Parameters**:
- `selector: (state: RootState) => T` - Function to select state
- `equalityFn?: (left: T, right: T) => boolean` - Custom equality check (default: `===`)

**Returns**: Selected state value

**Re-renders**: Component re-renders when selected value changes (reference equality)

### useDispatch

Get dispatch function to dispatch actions.

```typescript
import { useDispatch } from 'react-redux';

const Component = () => {
  const dispatch = useDispatch();

  const handleClick = () => {
    dispatch({ type: 'INCREMENT' });
    dispatch(asyncAction()); // Thunk action
  };

  return <button onClick={handleClick}>Click</button>;
};
```

**Returns**: `dispatch` function from Redux store

**Type Safety**: Type dispatch for thunk actions:
```typescript
type AppDispatch = typeof store.dispatch;
const dispatch = useDispatch<AppDispatch>();
```

### useStore

Get direct access to Redux store (rarely needed).

```typescript
import { useStore } from 'react-redux';

const store = useStore();
store.getState(); // Get current state
store.dispatch({ type: 'ACTION' }); // Dispatch action
store.subscribe(() => {});  // Subscribe to changes
```

**Why rarely used**: `useSelector` and `useDispatch` are preferred for accessing store in components.

## Redux Core API

### createStore

Create a Redux store (legacy, not used with Redux Toolkit).

```typescript
import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './reducers';

const store = createStore(
  rootReducer,
  applyMiddleware(thunk)
);
```

**Parameters**:
- `reducer` - Root reducer function
- `preloadedState?` - Initial state
- `enhancer?` - Store enhancer (middleware)

### combineReducers

Combine multiple reducers into root reducer.

```typescript
import { combineReducers } from 'redux';

const rootReducer = combineReducers({
  user: userReducer,
  counter: counterReducer,
  posts: postsReducer,
});

export type RootState = ReturnType<typeof rootReducer>;
```

**Returns**: Combined reducer function

### applyMiddleware

Apply middleware to store.

```typescript
import { applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import logger from 'redux-logger';

const middleware = applyMiddleware(thunk, logger);
const store = createStore(rootReducer, middleware);
```

**Common middleware**:
- `redux-thunk` - Async actions
- `redux-logger` - Logging
- Custom middleware

## Redux Thunk API

### Thunk Action Creator

Create async action creators.

```typescript
import { ThunkAction } from 'redux-thunk';
import { RootState } from './rootReducer';

type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action
>;

export const fetchUser = (userId: string): AppThunk<Promise<void>> => {
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
```

**Parameters** (thunk function receives):
- `dispatch` - Function to dispatch actions
- `getState` - Function to get current state
- `extraArgument` - Extra argument passed via thunk middleware

**Returns**: Promise or any value

### WithExtraArgument

Configure thunk with extra argument.

```typescript
import { configureStore } from '@reduxjs/toolkit';
import thunk from 'redux-thunk';

const api = createApiClient();

const store = configureStore({
  reducer: rootReducer,
  middleware: [thunk.withExtraArgument({ api })],
});

// Use in thunk
export const fetchUser = (): AppThunk => {
  return async (dispatch, getState, { api }) => {
    const user = await api.getUser();
    dispatch({ type: 'USER_LOADED', payload: user });
  };
};
```

## Reducer Patterns

### Basic Reducer

```typescript
type State = {
  count: number;
};

type Action =
  | { type: 'INCREMENT' }
  | { type: 'DECREMENT' }
  | { type: 'SET'; payload: number };

const initialState: State = {
  count: 0,
};

const counterReducer = (state = initialState, action: Action): State => {
  switch (action.type) {
    case 'INCREMENT':
      return { ...state, count: state.count + 1 };
    case 'DECREMENT':
      return { ...state, count: state.count - 1 };
    case 'SET':
      return { ...state, count: action.payload };
    default:
      return state;
  }
};
```

### Async State Pattern

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

const reducer = (state = initialState, action: Action) => {
  switch (action.type) {
    case 'FETCH_REQUEST':
      return { ...state, isLoading: true, error: null };
    case 'FETCH_SUCCESS':
      return { ...state, isLoading: false, data: action.payload };
    case 'FETCH_ERROR':
      return { ...state, isLoading: false, error: action.error };
    default:
      return state;
  }
};
```

## Selector Patterns

### Basic Selector

```typescript
export const selectUser = (state: RootState) => state.user;
export const selectUserId = (state: RootState) => state.user.id;
export const selectUserName = (state: RootState) => state.user.name;
```

### Composed Selector

```typescript
export const selectIsLoggedIn = (state: RootState): boolean => {
  const user = selectUser(state);
  return user !== null && user.id !== '';
};

export const selectFullName = (state: RootState): string => {
  const user = selectUser(state);
  return `${user.firstName} ${user.lastName}`;
};
```

### Reselect (Memoized Selectors)

```typescript
import { createSelector } from 'reselect';

const selectUsers = (state: RootState) => state.users;
const selectFilter = (state: RootState) => state.filter;

export const selectFilteredUsers = createSelector(
  [selectUsers, selectFilter],
  (users, filter) => {
    return users.filter(user =>
      user.name.toLowerCase().includes(filter.toLowerCase())
    );
  }
);
```

## Immutable.js Integration (Legacy)

### Map Methods

```typescript
import { Map } from 'immutable';

// Get value
const value = state.get('key');
const nested = state.getIn(['user', 'name']);

// Set value
const newState = state.set('key', 'value');
const newNested = state.setIn(['user', 'name'], 'John');

// Update
const updated = state.update('count', (count) => count + 1);

// Merge
const merged = state.merge({ key1: 'value1', key2: 'value2' });

// Delete
const deleted = state.delete('key');
```

### List Methods

```typescript
import { List } from 'immutable';

// Add
const newList = list.push(item);
const newList2 = list.concat([item1, item2]);

// Remove
const filtered = list.filter(item => item.id !== deleteId);

// Transform
const mapped = list.map(item => ({ ...item, selected: true }));

// Find
const found = list.find(item => item.id === searchId);
```

## TypeScript Integration

### Typing RootState

```typescript
import { combineReducers } from 'redux';

const rootReducer = combineReducers({
  user: userReducer,
  counter: counterReducer,
});

export type RootState = ReturnType<typeof rootReducer>;
```

### Typing Actions

```typescript
// Action type
type IncrementAction = { type: 'INCREMENT' };
type DecrementAction = { type: 'DECREMENT' };
type SetAction = { type: 'SET'; payload: number };

// Union type
type CounterAction = IncrementAction | DecrementAction | SetAction;

// Action creator with type
export const increment = (): IncrementAction => ({ type: 'INCREMENT' });
export const set = (value: number): SetAction => ({ type: 'SET', payload: value });
```

### Typing Thunks

```typescript
import { ThunkAction, ThunkDispatch } from 'redux-thunk';

type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action
>;

type AppDispatch = ThunkDispatch<RootState, unknown, Action>;

export const fetchUser = (): AppThunk<Promise<void>> => {
  return async (dispatch) => {
    // Implementation
  };
};
```

## Performance Considerations

1. **Use selector functions** - Reusable and testable
2. **Memoize expensive selectors** - Use reselect for derived data
3. **Avoid selecting entire store** - Select only needed slices
4. **Use shallow equality** - For object/array selections
5. **Batch dispatches** - Multiple updates in one render
6. **Normalize state** - Flat structure with IDs

## Common Mistakes

❌ **Mutating state in reducer**:
```typescript
state.count++; // Wrong
```

✅ **Return new state**:
```typescript
return { ...state, count: state.count + 1 };
```

❌ **Forgetting default case**:
```typescript
const reducer = (state, action) => {
  switch (action.type) {
    case 'INCREMENT':
      return { ...state, count: state.count + 1 };
    // Missing default!
  }
};
```

✅ **Always return state in default**:
```typescript
default:
  return state;
```

## Key Considerations

- Redux 4 uses legacy patterns (no Redux Toolkit in this codebase)
- Always use `useSelector` and `useDispatch` hooks (not `connect` HOC)
- Thunk actions handle async operations
- Immutable.js used in legacy code for complex state
- TypeScript for type-safe state and actions
- Selectors for accessing state (reusable and testable)
- Never mutate state - always return new objects
