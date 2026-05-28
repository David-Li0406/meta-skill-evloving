# Zustand API Reference

**Version**: 5.0.3

## Official Documentation

- **Getting Started**: https://docs.pmnd.rs/zustand/getting-started/introduction
- **Guides**: https://docs.pmnd.rs/zustand/guides/updating-state
- **Recipes**: https://docs.pmnd.rs/zustand/guides/immutable-state-and-merging
- **TypeScript**: https://docs.pmnd.rs/zustand/guides/typescript

## Core API

### create

Create a store with state and actions.

```typescript
import { create } from 'zustand';

interface Store {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

const useStore = create<Store>((set, get) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));
```

**Parameters**:
- `initializer` - Function that receives `set`, `get`, and `api` and returns state object

**Returns**: Custom hook for accessing store

### set

Update store state (synchronous).

```typescript
// Object merge (shallow)
set({ count: 5 });

// Function updater
set((state) => ({ count: state.count + 1 }));

// Replace entire state
set({ count: 5 }, true); // Second param = replace

// Multiple updates
set((state) => ({
  count: state.count + 1,
  lastUpdated: Date.now()
}));
```

**Signature**: `set(partial, replace?)`
- `partial` - Object or function returning object
- `replace` - Boolean, if true replaces entire state

### get

Read current state outside React.

```typescript
const useStore = create<Store>((set, get) => ({
  count: 0,
  doubleCount: () => get().count * 2,
  incrementIfEven: () => {
    if (get().count % 2 === 0) {
      set((state) => ({ count: state.count + 1 }));
    }
  },
}));
```

**Returns**: Current state snapshot

## Using Stores in Components

### Basic Usage

```typescript
// Get entire store
const store = useStore();

// Select specific state
const count = useStore((state) => state.count);

// Select action
const increment = useStore((state) => state.increment);

// Select multiple values
const { count, increment } = useStore((state) => ({
  count: state.count,
  increment: state.increment,
}));
```

### Shallow Selector

Prevent re-renders when selected objects have same values.

```typescript
import { shallow } from 'zustand/shallow';

const { count, increment } = useStore(
  (state) => ({ count: state.count, increment: state.increment }),
  shallow
);
```

**Why**: Without `shallow`, new object reference causes re-render even if values unchanged.

## Store Patterns

### Computed Values

```typescript
const useStore = create<Store>((set, get) => ({
  firstName: 'John',
  lastName: 'Doe',
  get fullName() {
    return `${get().firstName} ${get().lastName}`;
  },
  setFirstName: (name: string) => set({ firstName: name }),
  setLastName: (name: string) => set({ lastName: name }),
}));
```

### Async Actions

```typescript
const useStore = create<Store>((set) => ({
  recipes: [],
  isLoading: false,
  error: null,
  fetchRecipes: async () => {
    set({ isLoading: true, error: null });
    try {
      const recipes = await fetchRecipesAPI();
      set({ recipes, isLoading: false });
    } catch (error) {
      set({ error, isLoading: false });
    }
  },
}));
```

### Resetting State

```typescript
const initialState = {
  count: 0,
  text: '',
};

const useStore = create<Store>((set) => ({
  ...initialState,
  increment: () => set((state) => ({ count: state.count + 1 })),
  setText: (text: string) => set({ text }),
  reset: () => set(initialState),
}));
```

### Slicing Store

```typescript
// Define slices
const createCountSlice = (set, get) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
});

const createTextSlice = (set, get) => ({
  text: '',
  setText: (text) => set({ text }),
});

// Combine slices
const useStore = create((set, get) => ({
  ...createCountSlice(set, get),
  ...createTextSlice(set, get),
}));
```

## Middleware

### persist

Persist store to localStorage/AsyncStorage.

```typescript
import { persist } from 'zustand/middleware';

const useStore = create(
  persist<Store>(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
    }),
    {
      name: 'my-store', // Storage key
      storage: createJSONStorage(() => AsyncStorage), // For React Native
      partialize: (state) => ({ count: state.count }), // Select fields to persist
      onRehydrateStorage: () => (state, error) => {
        if (error) {
          console.error('Rehydration failed:', error);
        } else {
          console.log('Rehydration complete');
        }
      },
    }
  )
);
```

### devtools

Enable Redux DevTools integration.

```typescript
import { devtools } from 'zustand/middleware';

const useStore = create(
  devtools<Store>(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 }), undefined, 'increment'),
    }),
    { name: 'MyStore' }
  )
);
```

### immer

Simplify immutable updates with mutable syntax.

```typescript
import { immer } from 'zustand/middleware/immer';

const useStore = create(
  immer<Store>((set) => ({
    nested: { count: 0 },
    increment: () => set((state) => {
      state.nested.count++; // Direct mutation with immer
    }),
  }))
);
```

### Combining Middleware

```typescript
const useStore = create(
  devtools(
    persist(
      immer<Store>((set) => ({
        count: 0,
        increment: () => set((state) => {
          state.count++;
        }),
      })),
      { name: 'my-store' }
    ),
    { name: 'MyStore' }
  )
);
```

## Advanced Patterns

### Subscribe to Changes

```typescript
// Subscribe in useEffect
useEffect(() => {
  const unsubscribe = useStore.subscribe(
    (state) => state.count,
    (count, prevCount) => {
      console.log('Count changed:', prevCount, '->', count);
    }
  );
  return unsubscribe;
}, []);

// Subscribe to entire store
useEffect(() => {
  const unsubscribe = useStore.subscribe((state, prevState) => {
    console.log('State changed:', prevState, '->', state);
  });
  return unsubscribe;
}, []);
```

### Access Store Outside React

```typescript
// Get state
const state = useStore.getState();

// Set state
useStore.setState({ count: 5 });

// Subscribe
const unsubscribe = useStore.subscribe((state) => {
  console.log('State:', state);
});
```

### Store Context Pattern

```typescript
import { createContext, useContext } from 'react';

const StoreContext = createContext(null);

export const StoreProvider = ({ children }) => {
  const store = create<Store>((set) => ({
    count: 0,
    increment: () => set((state) => ({ count: state.count + 1 })),
  }));

  return (
    <StoreContext.Provider value={store}>
      {children}
    </StoreContext.Provider>
  );
};

export const useMyStore = () => {
  const store = useContext(StoreContext);
  if (!store) throw new Error('Missing StoreProvider');
  return store;
};
```

### Transient Updates

Updates that don't trigger re-renders.

```typescript
const useStore = create<Store>((set, get, api) => ({
  count: 0,
  incrementTransient: () => {
    // Update without notifying subscribers
    api.setState({ count: get().count + 1 }, true);
  },
}));
```

## Testing Patterns

### Reset Store in Tests

```typescript
beforeEach(() => {
  useStore.setState(initialState);
});
```

### Mock Store for Testing

```typescript
import { renderHook } from '@testing-library/react-hooks';

const createMockStore = (initialState = {}) => {
  return create(() => ({
    count: 0,
    increment: jest.fn(),
    ...initialState,
  }));
};

test('increments count', () => {
  const mockStore = createMockStore();
  const { result } = renderHook(() => mockStore());

  result.current.increment();
  expect(result.current.increment).toHaveBeenCalled();
});
```

### Testing Async Actions

```typescript
test('fetches recipes', async () => {
  const mockFetch = jest.fn().mockResolvedValue([{ id: 1 }]);

  const useStore = create((set) => ({
    recipes: [],
    isLoading: false,
    fetchRecipes: async () => {
      set({ isLoading: true });
      const recipes = await mockFetch();
      set({ recipes, isLoading: false });
    },
  }));

  const { result } = renderHook(() => useStore());

  await act(async () => {
    await result.current.fetchRecipes();
  });

  expect(result.current.recipes).toEqual([{ id: 1 }]);
  expect(result.current.isLoading).toBe(false);
});
```

## TypeScript Best Practices

### Type-Safe Selectors

```typescript
interface Store {
  count: number;
  increment: () => void;
}

// Inferred types
const count = useStore((state) => state.count); // number
const increment = useStore((state) => state.increment); // () => void

// Explicit selector type
const selector = (state: Store) => state.count;
const count = useStore(selector);
```

### Type-Safe Actions

```typescript
type Actions = {
  increment: () => void;
  decrement: () => void;
  reset: () => void;
};

type State = {
  count: number;
};

type Store = State & Actions;

const useStore = create<Store>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));
```

## Performance Tips

1. **Use shallow comparison** for object selectors to prevent unnecessary re-renders
2. **Split stores** by feature domain instead of one giant store
3. **Memoize selectors** that perform computations
4. **Avoid selecting entire store** unless you need all values
5. **Use transient updates** for high-frequency changes (e.g., mouse position)
6. **Batch updates** by calling `set` once with multiple fields

## Common Mistakes to Avoid

❌ **Selecting objects without shallow**:
```typescript
const { count, text } = useStore((state) => ({
  count: state.count,
  text: state.text
})); // Re-renders on any state change
```

✅ **Use shallow for object selectors**:
```typescript
const { count, text } = useStore(
  (state) => ({ count: state.count, text: state.text }),
  shallow
);
```

❌ **Mutating state directly**:
```typescript
set((state) => {
  state.count++; // Don't mutate without immer
  return state;
});
```

✅ **Return new object**:
```typescript
set((state) => ({ count: state.count + 1 }));
```

## Key Considerations

- Zustand stores are plain JavaScript objects, not Proxies
- Use `shallow` for object selectors to prevent re-renders
- Actions can be async without special middleware
- No Provider needed (unlike Context or Redux)
- Works with React 18 concurrent features
- Supports React Native out of the box
- Minimal bundle size (~1KB)
- No boilerplate required
