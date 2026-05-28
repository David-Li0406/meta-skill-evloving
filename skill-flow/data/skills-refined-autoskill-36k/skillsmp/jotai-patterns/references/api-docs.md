# Jotai API Reference

**Version**: Jotai v1.11.0

## Official Documentation

- **Getting Started**: https://jotai.org/docs/introduction
- **Core API**: https://jotai.org/docs/core/atom
- **Utils**: https://jotai.org/docs/utilities/storage
- **Guides**: https://jotai.org/docs/guides/typescript

## Core API

### atom

Create an atom for storing state.

```typescript
import { atom } from 'jotai';

// Read-only atom
const countAtom = atom(0);

// Read-write atom
const textAtom = atom('hello');

// Typed atom
const userAtom = atom<User | null>(null);

// Derived read-only atom
const doubleAtom = atom((get) => get(countAtom) * 2);

// Derived read-write atom
const uppercaseAtom = atom(
  (get) => get(textAtom).toUpperCase(),
  (get, set, newValue: string) => set(textAtom, newValue.toLowerCase())
);

// Write-only atom (action)
const incrementAtom = atom(
  null,
  (get, set) => set(countAtom, get(countAtom) + 1)
);
```

**Parameters**:
- `initialValue` - Initial state value
- `read` - Read function: `(get) => value`
- `write` - Write function: `(get, set, update) => void`

**Returns**: Atom object

### useAtom

Read and write atom value in component.

```typescript
import { useAtom } from 'jotai';

const [count, setCount] = useAtom(countAtom);

// Usage
setCount(5); // Set value
setCount((prev) => prev + 1); // Update function
```

**Parameters**:
- `atom` - Atom to use

**Returns**: `[value, setValue]` tuple

### useAtomValue

Read atom value (no setter).

```typescript
import { useAtomValue } from 'jotai';

const count = useAtomValue(countAtom);
```

**Parameters**:
- `atom` - Atom to read

**Returns**: Current atom value

**When to use**: Read-only access, no need for setter

### useSetAtom

Get setter function (no value).

```typescript
import { useSetAtom } from 'jotai';

const setCount = useSetAtom(countAtom);
const increment = useSetAtom(incrementAtom); // Action atom

// Usage
setCount(10);
increment(); // Trigger action
```

**Parameters**:
- `atom` - Atom to get setter for

**Returns**: Setter function

**When to use**: Write-only access, value not needed

## Utility Functions

### atomWithStorage

Create atom that persists to storage.

```typescript
import { atomWithStorage } from 'jotai/utils';

// localStorage (web)
const userAtom = atomWithStorage<User>('user-key', defaultUser);

// AsyncStorage (React Native)
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createJSONStorage } from 'jotai/utils';

const storage = createJSONStorage(() => AsyncStorage);
const settingsAtom = atomWithStorage('settings', defaultSettings, storage);
```

**Parameters**:
- `key` - Storage key
- `initialValue` - Default value
- `storage` - Storage implementation (optional)

**Features**:
- Automatic serialization/deserialization
- Syncs across tabs (web)
- Type-safe

### atomWithReset

Create atom with reset functionality.

```typescript
import { atomWithReset, useResetAtom } from 'jotai/utils';

const countAtom = atomWithReset(0);

// In component
const [count, setCount] = useAtom(countAtom);
const resetCount = useResetAtom(countAtom);

resetCount(); // Resets to initial value
```

**Parameters**:
- `initialValue` - Value to reset to

### atomWithReducer

Create atom with reducer pattern.

```typescript
import { atomWithReducer } from 'jotai/utils';

type State = { count: number };
type Action = { type: 'increment' } | { type: 'decrement' };

const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
  }
};

const counterAtom = atomWithReducer({ count: 0 }, reducer);

// Usage
const [state, dispatch] = useAtom(counterAtom);
dispatch({ type: 'increment' });
```

### atomFamily

Create atom factory for dynamic atoms.

```typescript
import { atomFamily } from 'jotai/utils';

// Create atom for each ID
const itemAtomFamily = atomFamily((id: string) =>
  atom({ id, name: '', count: 0 })
);

// Usage
const item1Atom = itemAtomFamily('item-1');
const item2Atom = itemAtomFamily('item-2');

const [item1] = useAtom(item1Atom);
```

**Parameters**:
- `initializeAtom` - Function that creates atom

**Returns**: Function that returns atom for parameter

## Advanced Patterns

### Custom Read Function

```typescript
// Computed value
const fullNameAtom = atom((get) => {
  const firstName = get(firstNameAtom);
  const lastName = get(lastNameAtom);
  return `${firstName} ${lastName}`;
});

// Conditional read
const visibleItemsAtom = atom((get) => {
  const items = get(itemsAtom);
  const filter = get(filterAtom);
  return items.filter(item => item.type === filter);
});
```

### Custom Write Function

```typescript
// Custom setter logic
const incrementByAtom = atom(
  (get) => get(countAtom),
  (get, set, amount: number) => {
    set(countAtom, get(countAtom) + amount);
  }
);

// Action with side effects
const saveUserAtom = atom(
  null,
  async (get, set, user: User) => {
    set(loadingAtom, true);
    try {
      await api.saveUser(user);
      set(userAtom, user);
      set(errorAtom, null);
    } catch (error) {
      set(errorAtom, error.message);
    } finally {
      set(loadingAtom, false);
    }
  }
);
```

### Async Atoms

```typescript
// Async read
const userAtom = atom(async () => {
  const response = await fetch('/api/user');
  return response.json();
});

// Async write
const updateUserAtom = atom(
  null,
  async (get, set, updates: Partial<User>) => {
    const user = get(userAtom);
    const updated = { ...user, ...updates };
    await api.updateUser(updated);
    set(userAtom, updated);
  }
);

// Usage with Suspense
const UserProfile = () => {
  const user = useAtomValue(userAtom); // Suspends while loading
  return <div>{user.name}</div>;
};
```

## Store API

### useStore

Access Jotai store directly (advanced).

```typescript
import { useStore } from 'jotai';

const Component = () => {
  const store = useStore();

  // Get atom value outside React
  const value = store.get(myAtom);

  // Set atom value
  store.set(myAtom, newValue);

  // Subscribe to changes
  const unsubscribe = store.sub(myAtom, () => {
    console.log('Atom changed');
  });
};
```

### createStore

Create isolated store.

```typescript
import { createStore } from 'jotai';

const store = createStore();

// Use with Provider
<Provider store={store}>
  <App />
</Provider>
```

## React Integration

### Provider

Provide store to component tree (optional).

```typescript
import { Provider } from 'jotai';

// Optional - creates isolated store
<Provider>
  <App />
</Provider>

// With custom store
<Provider store={customStore}>
  <App />
</Provider>
```

**When needed**:
- Multiple stores in one app
- Server-side rendering
- Testing with isolated stores

**When not needed**:
- Single default store (most cases)

### Hydrate

Hydrate atoms on mount.

```typescript
import { useHydrateAtoms } from 'jotai/utils';

const HydrateAtoms = ({ initialValues, children }) => {
  useHydrateAtoms(initialValues);
  return children;
};

// Usage
<HydrateAtoms initialValues={[[userAtom, userData]]}>
  <App />
</HydrateAtoms>
```

## DevTools

### Integration

```typescript
import { useAtomDevtools } from 'jotai/devtools';

const Component = () => {
  const [count, setCount] = useAtom(countAtom);
  useAtomDevtools(countAtom, 'count');

  return <div>{count}</div>;
};
```

## TypeScript Support

### Typed Atoms

```typescript
// Explicit type
const userAtom = atom<User | null>(null);

// Inferred from initial value
const countAtom = atom(0); // number

// Union types
const statusAtom = atom<'idle' | 'loading' | 'success' | 'error'>('idle');

// Generic atom
const createAtom = <T,>(initialValue: T) => atom<T>(initialValue);
```

### Type Inference

```typescript
// Inferred from read function
const doubleAtom = atom((get) => get(countAtom) * 2); // number

// Explicit return type
const userNameAtom = atom<string>((get) => {
  const user = get(userAtom);
  return user?.name ?? 'Guest';
});
```

## Performance Tips

1. **Split atoms** - Many small atoms > few large atoms
2. **Use read-only atoms** - Prevent unnecessary updates
3. **Memoize selectors** - Derived atoms are automatically memoized
4. **Use useAtomValue** - When setter not needed
5. **Use useSetAtom** - When value not needed
6. **Avoid inline atoms** - Define at module scope

## Common Patterns

### Loading State

```typescript
const dataAtom = atom<Data | null>(null);
const loadingAtom = atom(false);
const errorAtom = atom<Error | null>(null);

const fetchDataAtom = atom(
  null,
  async (get, set) => {
    set(loadingAtom, true);
    set(errorAtom, null);
    try {
      const data = await fetchData();
      set(dataAtom, data);
    } catch (error) {
      set(errorAtom, error);
    } finally {
      set(loadingAtom, false);
    }
  }
);
```

### Form State

```typescript
const emailAtom = atom('');
const passwordAtom = atom('');
const formErrorsAtom = atom<Record<string, string>>({});

const submitFormAtom = atom(
  null,
  async (get, set) => {
    const email = get(emailAtom);
    const password = get(passwordAtom);

    const errors: Record<string, string> = {};
    if (!email) errors.email = 'Required';
    if (!password) errors.password = 'Required';

    if (Object.keys(errors).length > 0) {
      set(formErrorsAtom, errors);
      return;
    }

    await submitForm({ email, password });
  }
);
```

## Key Considerations

- Atoms defined at module scope (not in components)
- Minimal API surface (atom, useAtom, useAtomValue, useSetAtom)
- No Provider needed for most cases
- Automatic dependency tracking
- Works with React Suspense
- TypeScript-first design
- Tree-shakeable
- Minimal bundle size (~3KB)
