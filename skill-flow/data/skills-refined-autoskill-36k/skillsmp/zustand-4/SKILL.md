---
name: zustand-4
description: >
  Zustand 4 state management patterns for MiGestion.
  Trigger: When creating Zustand stores for state management.
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [web]
  auto_invoke: 'Writing Zustand stores'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Store Pattern (REQUIRED)

```typescript
import { create } from 'zustand';

interface ExampleState {
  // State
  items: Item[];
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchItems: () => Promise<void>;
  addItem: (item: Item) => Promise<void>;
  clearError: () => void;
}

export const useExampleStore = create<ExampleState>((set, get) => ({
  // Initial state
  items: [],
  isLoading: false,
  error: null,

  // Actions
  fetchItems: async () => {
    try {
      set({ isLoading: true, error: null });
      const items = await exampleService.getItems();
      set({ items, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  addItem: async item => {
    const newItem = await exampleService.createItem(item);
    set(state => ({ items: [...state.items, newItem] }));
  },

  clearError: () => set({ error: null }),
}));
```

## Usage in Components

```typescript
function ExampleComponent() {
  const { items, isLoading, error, fetchItems } = useExampleStore();

  useEffect(() => {
    fetchItems();
  }, []);

  if (isLoading) return <Spinner />;
  if (error) return <Alert message={error} />;

  return (
    <div>
      {items.map(item => <ItemCard key={item.id} item={item} />)}
    </div>
  );
}
```

## Selectors (Performance)

```typescript
// ✅ Select specific state to prevent re-renders
const items = useExampleStore(state => state.items);
const isLoading = useExampleStore(state => state.isLoading);

// ✅ Selector with derived state
const activeItems = useExampleStore(state => state.items.filter(item => item.status === 'active'));
```

## Update Pattern

```typescript
// ✅ Append to array
addItem: (item) => set(state => ({ items: [...state.items, item] })),

// ✅ Update item in array
updateItem: (id, updates) => set(state => ({
  items: state.items.map(item =>
    item.id === id ? { ...item, ...updates } : item
  ),
})),

// ✅ Remove from array
removeItem: (id) => set(state => ({
  items: state.items.filter(item => item.id !== id),
})),

// ✅ Set directly
setName: (name) => set({ name }),
```

## Async Actions

```typescript
fetchData: async () => {
  try {
    set({ isLoading: true, error: null });
    const data = await service.getData();
    set({ data, isLoading: false });
  } catch (error) {
    set({ error: error.message, isLoading: false });
  }
},
```

## get() for Derived State

```typescript
getState: () => get().items,
totalCount: () => get().items.length,

// Using get() within actions
refreshAll: async () => {
  const currentFilters = get().filters;
  await fetchItems(currentFilters);
},
```

## Multiple Actions in One Set

```typescript
reset: () => set({
  items: [],
  isLoading: false,
  error: null,
  filters: DEFAULT_FILTERS,
}),
```

## Action Return Values

```typescript
createClient: async (data) => {
  try {
    set({ isSubmitting: true, error: null });
    const client = await service.createClient(data);
    set({ isSubmitting: false });
    return client; // Return for caller to use
  } catch (error) {
    set({ error: error.message, isSubmitting: false });
    throw error; // Rethrow for caller to handle
  }
},
```

## Store Persistence

```typescript
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist<AuthState>(
    (set, get) => ({
      user: null,
      token: null,
      login: async credentials => {
        const { user, token } = await authService.login(credentials);
        set({ user, token });
      },
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
```

## Store Slices (Modular Stores)

```typescript
// slices/items-slice.ts
export const createItemsSlice = (set: StateSetter, get: StateGetter) => ({
  items: [],
  fetchItems: async () => {
    const items = await service.getItems();
    set({ items });
  },
});

// slices/ui-slice.ts
export const createUISlice = (set: StateSetter) => ({
  isLoading: false,
  error: null,
  setLoading: isLoading => set({ isLoading }),
});

// Combined store
export const useStore = create<ItemsState & UIState>((set, get) => ({
  ...createItemsSlice(set, get),
  ...createUISlice(set),
}));
```

## Typing Actions

```typescript
interface ExampleState {
  // State
  items: Item[];

  // Actions
  fetchItems: () => Promise<void>;
  addItem: (item: Item) => Promise<void>;
  updateItem: (id: string, updates: Partial<Item>) => Promise<void>;
  removeItem: (id: string) => Promise<void>;
  clearItems: () => void;
}
```

## TypeScript with Generics

```typescript
interface ListState<T> {
  items: T[];
  selected: T | null;
  isLoading: boolean;
}

function createListStore<T>(initialItems: T[] = []) {
  return create<ListState<T>>(set => ({
    items: initialItems,
    selected: null,
    isLoading: false,
  }));
}

// Usage
const useClientsStore = createListStore<Client>();
```

## Testing Stores

```typescript
import { renderHook, act, waitFor } from '@testing-library/react';
import { useExampleStore } from './example.store';

describe('useExampleStore', () => {
  it('should fetch items', async () => {
    const { result } = renderHook(() => useExampleStore());

    await act(async () => {
      await result.current.fetchItems();
    });

    expect(result.current.items).toHaveLength(10);
  });
});
```

## DevTools

```typescript
import { devtools } from 'zustand/middleware';

export const useStore = create(
  devtools(
    (set, get) => ({
      // store implementation
    }),
    { name: 'MyStore' }
  )
);
```

## Related Skills

- `migestion-web` - MiGestion Web patterns
- `react-18` - React component patterns
- `typescript` - TypeScript patterns
