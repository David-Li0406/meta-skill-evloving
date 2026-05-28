# Redux Toolkit Patterns

Legacy state management patterns. **Use only when integrating with existing Redux state.**

For new development, prefer [React Query](react-query-patterns.md).

## Table of Contents

1. [When to Use Redux](#when-to-use-redux)
2. [Slice Structure](#slice-structure)
3. [Selectors](#selectors)
4. [Anti-patterns](#anti-patterns)

---

## When to Use Redux

Use Redux **only** for:

- Client-side state shared across many unrelated components
- Complex state with multiple interacting reducers
- Integrating with existing Redux state in the codebase

**Do NOT use Redux for:**

- Server state / API data → Use React Query
- Local component state → Use `useState`
- Form state → Use `react-hook-form` or `useState`
- Theme/preferences → Use Context

---

## Slice Structure

Use Redux Toolkit's `createSlice` for all Redux state.

### Basic Slice

```javascript
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  items: [],
  selectedId: null,
  isLoading: false,
};

const itemsSlice = createSlice( {
  name: 'items',
  initialState,
  reducers: {
    setItems: ( state, action ) => {
      state.items = action.payload;
    },
    selectItem: ( state, action ) => {
      state.selectedId = action.payload;
    },
    clearSelection: ( state ) => {
      state.selectedId = null;
    },
    setLoading: ( state, action ) => {
      state.isLoading = action.payload;
    },
  },
} );

export const { setItems, selectItem, clearSelection, setLoading } = itemsSlice.actions;
export default itemsSlice.reducer;
```

### Slice with Prepare Callback

```javascript
const notificationsSlice = createSlice( {
  name: 'notifications',
  initialState: [],
  reducers: {
    addNotification: {
      reducer: ( state, action ) => {
        state.push( action.payload );
      },
      prepare: ( message, type = 'info' ) => ( {
        payload: {
          id: Date.now(),
          message,
          type,
          timestamp: new Date().toISOString(),
        },
      } ),
    },
    removeNotification: ( state, action ) => {
      return state.filter( ( n ) => n.id !== action.payload );
    },
  },
} );
```

---

## Selectors

Always use memoized selectors to prevent unnecessary re-renders.

### Basic Selectors

```javascript
// Simple selector - no memoization needed
export const selectItems = ( state ) => state.items.items;
export const selectSelectedId = ( state ) => state.items.selectedId;
export const selectIsLoading = ( state ) => state.items.isLoading;
```

### Memoized Selectors with createSelector

```javascript
import { createSelector } from '@reduxjs/toolkit';

// Memoized derived state
export const selectActiveItems = createSelector(
  [ selectItems ],
  ( items ) => items.filter( ( item ) => item.active )
);

// Multiple inputs
export const selectSelectedItem = createSelector(
  [ selectItems, selectSelectedId ],
  ( items, selectedId ) => items.find( ( item ) => item.id === selectedId )
);

// Computed values
export const selectItemStats = createSelector(
  [ selectItems ],
  ( items ) => ( {
    total: items.length,
    active: items.filter( ( i ) => i.active ).length,
    completed: items.filter( ( i ) => i.completed ).length,
  } )
);
```

### Parameterized Selectors (Selector Factories)

```javascript
// Factory for parameterized selectors
export const makeSelectItemById = () =>
  createSelector(
    [ selectItems, ( _, id ) => id ],
    ( items, id ) => items.find( ( item ) => item.id === id )
  );

// Usage in component
const Component = ( { itemId } ) => {
  const selectItemById = useMemo( makeSelectItemById, [] );
  const item = useSelector( ( state ) => selectItemById( state, itemId ) );
  // ...
};
```

### Selector Composition

```javascript
// Base selectors
const selectWorkouts = ( state ) => state.workouts.data;
const selectFilter = ( state ) => state.workouts.filter;
const selectSortBy = ( state ) => state.workouts.sortBy;

// Composed selector
export const selectFilteredAndSortedWorkouts = createSelector(
  [ selectWorkouts, selectFilter, selectSortBy ],
  ( workouts, filter, sortBy ) => {
    let result = workouts;

    if ( filter ) {
      result = result.filter( ( w ) => w.type === filter );
    }

    return [ ...result ].sort( ( a, b ) => {
      if ( sortBy === 'date' ) return new Date( b.date ) - new Date( a.date );
      if ( sortBy === 'name' ) return a.name.localeCompare( b.name );
      return 0;
    } );
  }
);
```

---

## Anti-patterns

### Never Subscribe to Entire State

```javascript
// Bad - re-renders on ANY state change
const Component = () => {
  const state = useSelector( ( state ) => state );
  const items = state.items.items;
  // ...
};

// Bad - selecting entire slice
const Component = () => {
  const itemsState = useSelector( ( state ) => state.items );
  const items = itemsState.items;
  // ...
};

// Good - select specific values
const Component = () => {
  const items = useSelector( selectItems );
  const isLoading = useSelector( selectIsLoading );
  // ...
};
```

### Avoid Inline Selectors

```javascript
// Bad - new function reference every render
const Component = () => {
  const activeItems = useSelector( ( state ) =>
    state.items.items.filter( ( i ) => i.active )
  );
  // ...
};

// Good - defined selector
const Component = () => {
  const activeItems = useSelector( selectActiveItems );
  // ...
};
```

### Don't Duplicate State

```javascript
// Bad - storing derived data
const slice = createSlice( {
  name: 'items',
  initialState: {
    items: [],
    activeItems: [], // Derived - don't store!
    itemCount: 0,    // Derived - don't store!
  },
  // ...
} );

// Good - derive in selectors
const selectActiveItems = createSelector(
  [ selectItems ],
  ( items ) => items.filter( ( i ) => i.active )
);

const selectItemCount = createSelector(
  [ selectItems ],
  ( items ) => items.length
);
```

### Avoid Dispatching in Selectors

```javascript
// Bad - side effects in selector
const selectAndLog = ( state ) => {
  const items = state.items.items;
  console.log( 'Items selected:', items.length ); // Side effect!
  return items;
};

// Good - pure selector
const selectItems = ( state ) => state.items.items;
```

### Use Object Shorthand in useSelector

```javascript
// Bad - returns new object every time
const Component = () => {
  const { items, loading } = useSelector( ( state ) => ( {
    items: state.items.items,
    loading: state.items.isLoading,
  } ) );
  // This causes re-render on EVERY state change!
};

// Good - separate useSelector calls
const Component = () => {
  const items = useSelector( selectItems );
  const loading = useSelector( selectIsLoading );
  // ...
};

// Good - shallowEqual comparison
import { shallowEqual } from 'react-redux';

const Component = () => {
  const { items, loading } = useSelector(
    ( state ) => ( {
      items: selectItems( state ),
      loading: selectIsLoading( state ),
    } ),
    shallowEqual
  );
  // ...
};
```
