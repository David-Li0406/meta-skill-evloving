# Jotai Patterns - Production Examples

This document contains real production code examples from the YourCompany web codebase demonstrating Jotai v1.11.0 patterns.

## Example 1: Simple Atom with Custom Hook

**File**: `app/features/product-details-feature/components/animation/hooks/useDirectionAtom.tsx`

This example demonstrates creating a basic typed atom and exposing it through a custom hook.

```typescript
import { atom, useAtom } from 'jotai';

const directionAtom = atom<'up' | 'left'>('up');

export const useDirectionAtom = () => {
  return useAtom(directionAtom);
};

// Usage in component
export const AnimationComponent = () => {
  const [direction, setDirection] = useDirectionAtom();

  return (
    <div>
      <button onClick={() => setDirection('up')}>Up</button>
      <button onClick={() => setDirection('left')}>Left</button>
      <p>Direction: {direction}</p>
    </div>
  );
};
```

**Key patterns:**
- Atom defined at module scope (not inside component)
- TypeScript union type for atom value
- Custom hook wraps `useAtom` for encapsulation
- Export custom hook, not the atom itself
- Returns tuple: `[value, setter]`

## Example 2: Atom with Enhanced API

**File**: `app/features/recipe-feedback-feature/hooks/useFeedbackStep.ts`

This example shows wrapping atom usage with convenience methods.

```typescript
import { atom, useAtom } from 'jotai';

type FeedbackStep = 'feedback' | 'cancel' | 'success';

const feedbackStepAtom = atom<FeedbackStep>('feedback');

export const useFeedbackStep = () => {
  const [feedbackStep, setFeedbackStep] = useAtom(feedbackStepAtom);

  return {
    step: feedbackStep,
    setFeedbackStep: (step: FeedbackStep) => setFeedbackStep(step),
    resetStep: () => setFeedbackStep('feedback'),
  };
};

// Usage in component
export const FeedbackFlow = () => {
  const { step, setFeedbackStep, resetStep } = useFeedbackStep();

  if (step === 'feedback') {
    return <FeedbackForm onSubmit={() => setFeedbackStep('success')} />;
  }

  if (step === 'success') {
    return <SuccessMessage onClose={resetStep} />;
  }

  return null;
};
```

**Key patterns:**
- Custom hook returns object with descriptive names
- Helper methods (`resetStep`) encapsulate common operations
- Type-safe setter with explicit parameter type
- Better API than raw `[value, setter]` tuple

## Example 3: atomWithStorage for Persistence

**File**: `app/spaces/checkout/modules/__shared_context/state/billingFormState.ts`

This example demonstrates persisting atom state to localStorage.

```typescript
import { atomWithStorage } from 'jotai/utils';
import { BILLING_FORM_PERSISTENCE_KEY } from '../constants/constants';

export type FormWithData = {
  firstName: string;
  lastName: string;
  address1: string;
  city: string;
  region: string;
  postcode: string;
};

export type ValidatedForm = {
  isValid: boolean;
  formData: FormWithData;
};

export const validatedFormData: ValidatedForm = {
  isValid: false,
  formData: {
    firstName: '',
    lastName: '',
    address1: '',
    city: '',
    region: '',
    postcode: '',
  },
};

// Persisted to localStorage automatically
export const billingFormStateAtom = atomWithStorage(
  BILLING_FORM_PERSISTENCE_KEY,
  validatedFormData
);

export const billingFormValidation = atomWithStorage(
  `${BILLING_FORM_PERSISTENCE_KEY}-valid`,
  false
);

// Usage in component
import { useAtom } from 'jotai';

export const BillingForm = () => {
  const [formState, setFormState] = useAtom(billingFormStateAtom);
  const [isValid, setIsValid] = useAtom(billingFormValidation);

  return (
    <form>
      <input
        value={formState.formData.firstName}
        onChange={(e) =>
          setFormState({
            ...formState,
            formData: { ...formState.formData, firstName: e.target.value },
          })
        }
      />
    </form>
  );
};
```

**Key patterns:**
- `atomWithStorage` from `jotai/utils` for persistence
- First argument: localStorage key
- Second argument: initial/default value
- Automatically syncs to/from localStorage
- TypeScript types for form structure
- Multiple related atoms for different pieces of state

## Example 4: Derived Atoms (Read-Only)

**File**: `app/spaces/checkout/modules/__shared_context/state/addressFormState.ts`

This example shows creating derived atoms that compute values from other atoms.

```typescript
import { atom } from 'jotai';
import { atomWithStorage } from 'jotai/utils';

export const addressFormStateAtom = atomWithStorage(
  ADDRESS_FORM_PERSISTENCE_KEY,
  validatedFormData
);

// Derived atom - reads from another atom
export const postcodeAtom = atom(
  (get) => get(addressFormStateAtom).formData?.postcode
);

export const postcodeValidationAtom = atom(true);

// Usage in component
import { useAtomValue } from 'jotai';

export const PostcodeDisplay = () => {
  // Read-only: useAtomValue doesn't return setter
  const postcode = useAtomValue(postcodeAtom);

  return <div>Postcode: {postcode}</div>;
};
```

**Key patterns:**
- Read-only derived atom: `atom((get) => ...)`
- `get()` function accesses other atoms
- Automatically recomputes when dependencies change
- Use `useAtomValue` for read-only access (no setter)
- Computed values stay in sync with source atoms

## Example 5: Multiple Related Atoms

**File**: `app/features/phone-number-verification-feature/hooks/useStartPhoneVerficationTemporaryTimer.ts`

This example demonstrates managing related state with multiple atoms.

```typescript
import { useEffect } from 'react';
import { atom, useAtom } from 'jotai';
import { usePhoneNumberVerificationConfig } from '../config';

const timerElapsedAtom = atom(false);
const timerIdAtom = atom<NodeJS.Timeout | null>(null);

export const useStartPhoneVerficationTemporaryTimer = () => {
  const [isTimerElapsed, setIsTimerElapsed] = useAtom(timerElapsedAtom);
  const [timerId, setTimerId] = useAtom(timerIdAtom);
  const { autoDismissalTimer, shouldShowIdleScreen } =
    usePhoneNumberVerificationConfig();

  // Function to start the timer
  const startTimer = () => {
    if (!shouldShowIdleScreen) {
      return;
    }

    clearTimer();

    const id = setTimeout(() => {
      setIsTimerElapsed(true);
    }, autoDismissalTimer * 1000);

    setTimerId(id);
    setIsTimerElapsed(false); // Reset elapsed state
  };

  // Function to clear the timer
  const clearTimer: () => void = () => {
    if (!shouldShowIdleScreen) {
      return;
    }

    if (timerId) {
      clearTimeout(timerId);
      setTimerId(null);
    }
    setIsTimerElapsed(false);
  };

  // Clear timer on unmount
  useEffect(() => {
    if (!shouldShowIdleScreen) {
      return;
    }

    return () => {
      clearTimer();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { isTimerElapsed, startTimer, clearTimer };
};

// Usage in component
export const PhoneVerification = () => {
  const { isTimerElapsed, startTimer, clearTimer } =
    useStartPhoneVerficationTemporaryTimer();

  useEffect(() => {
    startTimer();
    return () => clearTimer();
  }, []);

  if (isTimerElapsed) {
    return <IdleScreen />;
  }

  return <VerificationForm />;
};
```

**Key patterns:**
- Multiple atoms for related state (elapsed flag + timer ID)
- Custom hook coordinates multiple atoms
- Cleanup logic in `useEffect` return
- TypeScript type for NodeJS.Timeout
- Custom API hides implementation details

## Example 6: Complex Atom with Custom Read/Write

**File**: `app/features/global-chat-feature/store/state.ts`

This example shows advanced atom patterns with custom getter/setter logic.

```typescript
import { atom, useSetAtom, useAtomValue } from 'jotai';
import { atomWithStorage } from 'jotai/utils';

type ChatState = {
  isOpen: boolean;
  isMinimized: boolean;
  messages: ChatMessage[];
  customerId: string;
};

const initialState: ChatState = {
  isOpen: false,
  isMinimized: false,
  messages: [],
  customerId: '',
};

// Base atom with localStorage persistence
const baseAtom = atomWithStorage<ChatState>(STORAGE_KEY, initialState);

// Wrapper atom with custom read/write logic
export const chatStateAtom = atom(
  // Custom getter
  (get) => {
    const state = get(baseAtom);
    const pathname =
      typeof window !== 'undefined' ? window.location.pathname : 'common';

    // Initialize page-specific state if needed
    if (!state?.pageState?.[pathname]) {
      return {
        ...state,
        pageState: {
          ...(state?.pageState || {}),
          [pathname]: { ...defaultPageState },
        },
      };
    }
    return state;
  },
  // Custom setter with logging
  (get, set, update: ChatState) => {
    const prevState = get(baseAtom);
    set(baseAtom, update);
    logChanges(prevState, update);
  }
);

// Derived atom (read from chatStateAtom, write to chatStateAtom)
export const isMinimizedAtom = atom(
  (get) => get(chatStateAtom).isMinimized,
  (get, set, isMinimized: boolean) => {
    const state = get(chatStateAtom);
    set(chatStateAtom, {
      ...state,
      isMinimized,
    });
  }
);

// Action atom (write-only, no read)
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

export const toggleChatAtom = atom(null, (get, set) => {
  const state = get(chatStateAtom);
  set(chatStateAtom, {
    ...state,
    isOpen: !state.isOpen,
    isMinimized: state.isOpen ? false : state.isMinimized,
  });
});

// Usage in component
export const ChatWidget = () => {
  const isMinimized = useAtomValue(isMinimizedAtom);
  const openChat = useSetAtom(openChatAtom);
  const closeChat = useSetAtom(closeChatAtom);
  const toggleChat = useSetAtom(toggleChatAtom);

  return (
    <div>
      <button onClick={openChat}>Open</button>
      <button onClick={closeChat}>Close</button>
      <button onClick={toggleChat}>Toggle</button>
      {!isMinimized && <ChatMessages />}
    </div>
  );
};
```

**Key patterns:**
- Layered atoms: persistent base + wrapper with logic
- Custom read function: `atom((get) => ...)`
- Custom write function: `atom(read, (get, set, update) => ...)`
- Action atoms: `atom(null, (get, set) => ...)` for write-only
- `useSetAtom` for write-only access (no read)
- `useAtomValue` for read-only access (no write)
- Logging/debugging in custom setter
- Immutable updates with spread operator

## Example 7: Hook for Multiple Atom Actions

**File**: `app/features/global-chat-feature/store/state.ts` (continued)

This example shows creating a custom hook that exposes multiple atom setters.

```typescript
// Multiple action atoms
export const openChatAtom = atom(null, (get, set) => { /* ... */ });
export const closeChatAtom = atom(null, (get, set) => { /* ... */ });
export const addMessageAtom = atom(null, (get, set, message: string) => { /* ... */ });
export const startNewSessionAtom = atom(null, (get, set) => { /* ... */ });
export const endSessionAtom = atom(null, (get, set) => { /* ... */ });

// Custom hook to group related actions
export function useChatActions() {
  const chatState = useAtomValue(chatStateAtom);

  const _openChat = useSetAtom(openChatAtom);
  const _closeChat = useSetAtom(closeChatAtom);
  const _addMessage = useSetAtom(addMessageAtom);
  const _endSession = useSetAtom(endSessionAtom);
  const _startNewSession = useSetAtom(startNewSessionAtom);

  const openChat = ({ intent }: { intent?: string } = {}) => {
    if (chatState.hasStarted && intent) {
      _openChat();
      return _setUpdateIntent(intent);
    }
    _openChat();
    intent && _setFollowingIntent(intent);
  };

  return {
    openChat,
    _openChat,
    _closeChat,
    _addMessage,
    _endSession,
    _startNewSession,
  };
}

// Usage in component
export const ChatContainer = () => {
  const {
    openChat,
    _closeChat,
    _addMessage,
    _startNewSession,
  } = useChatActions();

  return (
    <div>
      <button onClick={() => openChat({ intent: 'support' })}>
        Open Support Chat
      </button>
      <button onClick={_closeChat}>Close</button>
      <button onClick={() => _addMessage('Hello')}>Send Message</button>
      <button onClick={_startNewSession}>New Session</button>
    </div>
  );
};
```

**Key patterns:**
- Group related action atoms into single hook
- Custom hook provides enhanced API (with parameters)
- Prefix with `_` for raw atom setters
- Enhanced methods without `_` prefix
- Encapsulate complex logic in custom methods
- Return object with descriptive method names

## Common Anti-Patterns

### ❌ Defining Atoms Inside Components

```typescript
// DON'T: Atom inside component - creates new atom on every render!
const MyComponent = () => {
  const countAtom = atom(0); // Wrong!
  const [count, setCount] = useAtom(countAtom);
  return <div>{count}</div>;
};

// DO: Define atoms at module scope
const countAtom = atom(0);

const MyComponent = () => {
  const [count, setCount] = useAtom(countAtom);
  return <div>{count}</div>;
};
```

### ❌ Not Using atomWithStorage for Persistence

```typescript
// DON'T: Manual localStorage management
const userAtom = atom({ name: '' });

const MyComponent = () => {
  const [user, setUser] = useAtom(userAtom);

  useEffect(() => {
    const saved = localStorage.getItem('user');
    if (saved) setUser(JSON.parse(saved));
  }, []);

  useEffect(() => {
    localStorage.setItem('user', JSON.stringify(user));
  }, [user]);
};

// DO: Use atomWithStorage
import { atomWithStorage } from 'jotai/utils';

const userAtom = atomWithStorage('user', { name: '' });
```

### ❌ Using useState When Jotai is Better

```typescript
// DON'T: Local state that needs to be shared
const ParentComponent = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <ChildA isOpen={isOpen} setIsOpen={setIsOpen} />
      <ChildB isOpen={isOpen} />
      <ChildC setIsOpen={setIsOpen} />
    </>
  );
};

// DO: Use Jotai atom
const isOpenAtom = atom(false);

const ParentComponent = () => (
  <>
    <ChildA />
    <ChildB />
    <ChildC />
  </>
);

const ChildA = () => {
  const [isOpen, setIsOpen] = useAtom(isOpenAtom);
  // ...
};
```

### ❌ Not Using useAtomValue/useSetAtom

```typescript
// DON'T: Using useAtom when you only need read or write
const Component = () => {
  const [value, setValue] = useAtom(myAtom);
  return <div>{value}</div>; // Never use setValue!
};

// DO: Use useAtomValue for read-only
import { useAtomValue } from 'jotai';

const Component = () => {
  const value = useAtomValue(myAtom);
  return <div>{value}</div>;
};

// DO: Use useSetAtom for write-only
import { useSetAtom } from 'jotai';

const Component = () => {
  const setValue = useSetAtom(myAtom);
  return <button onClick={() => setValue(10)}>Set</button>;
};
```

## Summary

The YourCompany web codebase uses Jotai v1.11.0 with these patterns:

1. **Module-scoped atoms** - Always define atoms at module scope, not in components
2. **Custom hooks** - Wrap atoms in custom hooks for better API
3. **atomWithStorage** - Use for localStorage persistence
4. **Derived atoms** - Compute values from other atoms with `atom((get) => ...)`
5. **Action atoms** - Write-only atoms for actions: `atom(null, (get, set) => ...)`
6. **useAtomValue** - Read-only access when setter not needed
7. **useSetAtom** - Write-only access when value not needed
8. **Multiple atoms** - Split related state into separate atoms
9. **Custom read/write** - Advanced atoms with custom getter/setter logic
10. **Grouped actions** - Custom hooks that return multiple atom setters

**Key Libraries:**
- Jotai v1.11.0
- jotai/utils (atomWithStorage, atomWithReset, etc.)
- TypeScript 5.7.3

**Import patterns:**
```typescript
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';
import { atomWithStorage } from 'jotai/utils';
```

For Jotai v1 documentation, see: https://jotai.org/docs/introduction
