# Jotai Implementation Patterns

Implementation patterns and anti-patterns for Jotai v1.11.0 atomic state management.

## Pattern: Module-Scoped Atoms

Define atoms at module scope, not inside components.

✅ **Good:**
```typescript
// atoms.ts
import { atom } from 'jotai';

export const countAtom = atom(0);
export const textAtom = atom('hello');
export const userAtom = atom<User | null>(null);

// Component.tsx
import { useAtom } from 'jotai';
import { countAtom } from './atoms';

export const Component = () => {
  const [count, setCount] = useAtom(countAtom);
  return <div>{count}</div>;
};
```

❌ **Bad:**
```typescript
// Creating atom inside component
export const Component = () => {
  const countAtom = atom(0); // New atom every render!
  const [count, setCount] = useAtom(countAtom);
  return <div>{count}</div>;
};
```

**Why:** Module-scoped atoms:
- Single instance across app
- Persist across re-renders
- Can be shared between components
- Can be accessed outside React

## Pattern: Custom Hooks for Enhanced API

Wrap atoms in custom hooks with convenient methods.

✅ **Good:**
```typescript
import { atom, useAtom } from 'jotai';

const feedbackStepAtom = atom<'feedback' | 'cancel' | 'success'>('feedback');

export const useFeedbackStep = () => {
  const [step, setStep] = useAtom(feedbackStepAtom);

  return {
    step,
    setFeedbackStep: (newStep: typeof step) => setStep(newStep),
    resetStep: () => setStep('feedback'),
    isSuccess: step === 'success',
  };
};

// Usage
const { step, resetStep, isSuccess } = useFeedbackStep();
```

❌ **Bad:**
```typescript
// Exposing atom directly
export const feedbackStepAtom = atom<'feedback' | 'cancel' | 'success'>('feedback');

// Component has to know implementation details
const [step, setStep] = useAtom(feedbackStepAtom);
const resetStep = () => setStep('feedback');
```

**Why:** Custom hooks:
- Encapsulate implementation
- Provide convenient methods
- Hide complexity
- Better API for components

## Pattern: atomWithStorage for Persistence

Use atomWithStorage for data that should persist.

✅ **Good:**
```typescript
import { atomWithStorage } from 'jotai/utils';

export const addressFormAtom = atomWithStorage(
  'address-form',
  {
    firstName: '',
    lastName: '',
    address: '',
  }
);

// Data persists across page reloads
const [form, setForm] = useAtom(addressFormAtom);
```

❌ **Bad:**
```typescript
// Manual localStorage management
const formAtom = atom({ firstName: '', lastName: '' });

const Component = () => {
  const [form, setForm] = useAtom(formAtom);

  useEffect(() => {
    const saved = localStorage.getItem('form');
    if (saved) setForm(JSON.parse(saved));
  }, []);

  useEffect(() => {
    localStorage.setItem('form', JSON.stringify(form));
  }, [form]);
};
```

**Why:** atomWithStorage:
- Automatic persistence
- Syncs across tabs
- Type-safe
- Less code

## Pattern: Derived Atoms for Computed Values

Use read-only atoms for computed values.

✅ **Good:**
```typescript
const addressFormAtom = atomWithStorage('address-form', defaultForm);

// Derived atom
export const postcodeAtom = atom(
  (get) => get(addressFormAtom).formData?.postcode
);

// Usage - automatically updates when form changes
const postcode = useAtomValue(postcodeAtom);
```

❌ **Bad:**
```typescript
// Computing in component
const Component = () => {
  const [form] = useAtom(addressFormAtom);
  const postcode = form.formData?.postcode; // Recomputes every render

  return <div>{postcode}</div>;
};
```

**Why:** Derived atoms:
- Automatically memoized
- Reusable across components
- Single source of truth
- Better performance

## Pattern: Action Atoms for State Updates

Use write-only atoms for actions.

✅ **Good:**
```typescript
const chatStateAtom = atomWithStorage('chat-state', initialState);

// Write-only action atom
export const openChatAtom = atom(null, (get, set) => {
  const state = get(chatStateAtom);
  set(chatStateAtom, {
    ...state,
    isOpen: true,
    isMinimized: false,
  });
});

export const closeChatAtom = atom(null, (get, set) => {
  const state = get(chatStateAtom);
  set(chatStateAtom, {
    ...state,
    isOpen: false,
  });
});

// Usage
const openChat = useSetAtom(openChatAtom);
const closeChat = useSetAtom(closeChatAtom);

<button onClick={openChat}>Open</button>
```

❌ **Bad:**
```typescript
// Direct state manipulation in component
const Component = () => {
  const [state, setState] = useAtom(chatStateAtom);

  const openChat = () => {
    setState({
      ...state,
      isOpen: true,
      isMinimized: false,
    });
  };
};
```

**Why:** Action atoms:
- Centralize business logic
- Reusable across components
- Easier to test
- Type-safe actions

## Pattern: Multiple Related Atoms

Split related state into separate atoms.

✅ **Good:**
```typescript
const timerElapsedAtom = atom(false);
const timerIdAtom = atom<NodeJS.Timeout | null>(null);

export const useTimer = () => {
  const [isElapsed, setIsElapsed] = useAtom(timerElapsedAtom);
  const [timerId, setTimerId] = useAtom(timerIdAtom);

  const startTimer = () => {
    const id = setTimeout(() => setIsElapsed(true), 5000);
    setTimerId(id);
  };

  const clearTimer = () => {
    if (timerId) clearTimeout(timerId);
    setTimerId(null);
    setIsElapsed(false);
  };

  return { isElapsed, startTimer, clearTimer };
};
```

❌ **Bad:**
```typescript
// Single atom with complex state
const timerAtom = atom({
  isElapsed: false,
  timerId: null,
});

// Components re-render when any field changes
const Component = () => {
  const [timer, setTimer] = useAtom(timerAtom);
  // ...
};
```

**Why:** Multiple atoms:
- Granular subscriptions (less re-renders)
- Simpler updates
- Better performance
- Easier to reason about

## Pattern: useAtomValue for Read-Only

Use useAtomValue when setter not needed.

✅ **Good:**
```typescript
import { useAtomValue } from 'jotai';

const DisplayComponent = () => {
  const count = useAtomValue(countAtom); // No setter
  return <div>{count}</div>;
};
```

❌ **Bad:**
```typescript
// Using useAtom when setter not needed
const DisplayComponent = () => {
  const [count, setCount] = useAtom(countAtom); // Unused setter
  return <div>{count}</div>;
};
```

**Why:** useAtomValue:
- Clearer intent (read-only)
- Slightly better performance
- Prevents accidental updates

## Pattern: useSetAtom for Write-Only

Use useSetAtom when value not needed.

✅ **Good:**
```typescript
import { useSetAtom } from 'jotai';

const ButtonComponent = () => {
  const increment = useSetAtom(incrementAtom); // No value
  return <button onClick={increment}>+</button>;
};
```

❌ **Bad:**
```typescript
// Using useAtom when value not needed
const ButtonComponent = () => {
  const [, increment] = useAtom(incrementAtom); // Unused value
  return <button onClick={increment}>+</button>;
};
```

**Why:** useSetAtom:
- Clearer intent (write-only)
- No unnecessary subscriptions
- Better performance

## Pattern: Grouped Action Hooks

Create hooks that return multiple atom setters.

✅ **Good:**
```typescript
const openChatAtom = atom(null, (get, set) => { /* ... */ });
const closeChatAtom = atom(null, (get, set) => { /* ... */ });
const addMessageAtom = atom(null, (get, set, msg: string) => { /* ... */ });

export const useChatActions = () => {
  const openChat = useSetAtom(openChatAtom);
  const closeChat = useSetAtom(closeChatAtom);
  const addMessage = useSetAtom(addMessageAtom);

  return { openChat, closeChat, addMessage };
};

// Usage
const { openChat, closeChat, addMessage } = useChatActions();
```

❌ **Bad:**
```typescript
// Importing and using atoms individually
import { openChatAtom, closeChatAtom, addMessageAtom } from './atoms';

const Component = () => {
  const openChat = useSetAtom(openChatAtom);
  const closeChat = useSetAtom(closeChatAtom);
  const addMessage = useSetAtom(addMessageAtom);
  // ...
};
```

**Why:** Grouped hooks:
- Convenient API
- Single import
- Related actions together
- Easier discovery

## Pattern: Async Atoms with Error Handling

Handle async operations with proper error states.

✅ **Good:**
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

// Usage
const data = useAtomValue(dataAtom);
const loading = useAtomValue(loadingAtom);
const error = useAtomValue(errorAtom);
const fetch = useSetAtom(fetchDataAtom);
```

❌ **Bad:**
```typescript
// Single atom, missing error state
const dataAtom = atom(async () => {
  return await fetchData(); // No loading/error states
});

// Component can't show loading spinner or errors
```

**Why:** Separate atoms for:
- Loading indicators
- Error messages
- Success data
- Proper UX

## Anti-Pattern: Defining Atoms in Components

Never create atoms inside components.

❌ **Bad:**
```typescript
const Component = () => {
  const counterAtom = atom(0); // New atom every render!
  const [count, setCount] = useAtom(counterAtom);
  return <div>{count}</div>;
};
```

✅ **Good:**
```typescript
const counterAtom = atom(0); // Module scope

const Component = () => {
  const [count, setCount] = useAtom(counterAtom);
  return <div>{count}</div>;
};
```

**Why:** Atoms in components:
- Create new instance every render
- Lose state on re-render
- Memory leaks
- Break atom identity

## Anti-Pattern: Not Using atomWithStorage

Don't manually manage localStorage for atoms.

❌ **Bad:**
```typescript
const userAtom = atom({ name: '' });

const Component = () => {
  const [user, setUser] = useAtom(userAtom);

  useEffect(() => {
    const saved = localStorage.getItem('user');
    if (saved) setUser(JSON.parse(saved));
  }, []);

  useEffect(() => {
    localStorage.setItem('user', JSON.stringify(user));
  }, [user]);
};
```

✅ **Good:**
```typescript
import { atomWithStorage } from 'jotai/utils';

const userAtom = atomWithStorage('user', { name: '' });
```

**Why:** atomWithStorage:
- Automatic persistence
- Syncs across tabs
- Less code
- Type-safe

## Anti-Pattern: Using Atoms Like useState

Don't use atoms when useState is sufficient.

❌ **Bad:**
```typescript
// Component-local state as atom
const localCountAtom = atom(0);

const Component = () => {
  const [count, setCount] = useAtom(localCountAtom);
  return <div>{count}</div>;
};
```

✅ **Good:**
```typescript
// Use useState for component-local state
const Component = () => {
  const [count, setCount] = useState(0);
  return <div>{count}</div>;
};

// Use atoms for shared state
const globalCountAtom = atom(0); // Shared across components
```

**Why:** Use atoms when:
- State shared between components
- State needs to persist
- State accessed outside React
- NOT for component-local state

## Anti-Pattern: Selecting Objects Without Equality

Be careful with derived atoms that return objects.

❌ **Bad:**
```typescript
// New object every time - causes re-renders
const userDataAtom = atom((get) => ({
  name: get(nameAtom),
  email: get(emailAtom),
}));

// Component re-renders even if values unchanged
```

✅ **Good:**
```typescript
// Separate atoms for each field
const nameAtom = atom('');
const emailAtom = atom('');

// Select only what you need
const Component = () => {
  const name = useAtomValue(nameAtom);
  const email = useAtomValue(emailAtom);
};

// Or use atomFamily for stable references
```

**Why:** Object references:
- New object = re-render
- Atoms use reference equality
- Separate atoms = granular updates

## Summary

**Key Patterns:**
- Module-scoped atoms (not in components)
- Custom hooks for enhanced API
- atomWithStorage for persistence
- Derived atoms for computed values
- Action atoms for state updates
- Multiple related atoms (granular)
- useAtomValue for read-only
- useSetAtom for write-only
- Grouped action hooks
- Async atoms with error handling

**Anti-Patterns to Avoid:**
- Atoms in components
- Manual localStorage management
- Using atoms like useState
- Object returns without equality
- Missing error handling in async
