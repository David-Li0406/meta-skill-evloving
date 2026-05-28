---
name: jotai-patterns
description: "WHAT: Jotai v1.11.0 atomic state management with atoms and useAtom hook. WHEN: lightweight global state, modal/dialog state, form state across components. KEYWORDS: jotai, atom, useAtom, atomic, state, derived, web, modal, dialog, SetStateAction."
---

# Jotai Patterns - Web

Atomic state management patterns using Jotai v1.11.0 for React web applications.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use Jotai for:
- Lightweight global state without Redux boilerplate
- Component-specific state that needs to be shared
- Form state across multiple components
- Modal/dialog open/closed state
- Simple feature flags or toggles
- State that doesn't need complex middleware

**Don't use Jotai for:**
- Complex state with many interdependencies (use Redux)
- State machines with transitions (use XState)

## Core Principles

### 1. Atom Definition

**Define atoms in separate files with clear types.**

✅ **Good:**
```typescript
// app/state/cart/cartSku/cartSkuState.ts:1
import { atom } from 'jotai';

export type CartSku = string | null;

export const cartSkuState = atom<CartSku>(null);
```

**Why:** Separating atom definitions makes them reusable and testable. Type annotations ensure type safety.

### 2. useAtom Hook

**Use useAtom to read and update atom values in components.**

✅ **Good:**
```typescript
// app/state/cart/cartSku/useCartSkuState.ts:1
import { useAtom, SetStateAction } from 'jotai';

import { CartSku, cartSkuState } from './cartSkuState';

const useCartSkuState = (): [
  CartSku,
  (update: SetStateAction<CartSku>) => void
] => useAtom(cartSkuState);

export default useCartSkuState;

// Usage in component
const [cartSku, setCartSku] = useCartSkuState();
```

**Why:** Creating a custom hook wrapper provides better type inference and makes the API easier to use.

### 3. Inline Atom Creation

**You can create atoms inline for component-specific state.**

✅ **Good:**
```typescript
// app/unified-spaces/referral-page/referral/pages/ReferralPageContent/ReferralPageContent.tsx:23
import { atom, useAtom } from 'jotai';

export const sendFreebieInHelloshareByEmailDialogFeatureAtom = atom(false);

const ReferralPageContent: React.FC = () => {
  const [isFormDialogOpen, setIsFormDialogOpen] = useAtom(
    sendFreebieInHelloshareByEmailDialogFeatureAtom
  );

  return (
    <div>
      <button onClick={() => setIsFormDialogOpen(true)}>
        Open Dialog
      </button>
      {isFormDialogOpen && <Dialog onClose={() => setIsFormDialogOpen(false)} />}
    </div>
  );
};
```

**Why:** For simple boolean flags or component-specific state, inline atoms reduce boilerplate.

### 4. Atom Updates

**Update atoms using the setter function returned by useAtom.**

✅ **Good:**
```typescript
const [cartSku, setCartSku] = useCartSkuState();

// Direct value
setCartSku('new-sku-123');

// Function updater (like useState)
setCartSku((prevSku) => prevSku ? `${prevSku}-updated` : 'default-sku');

// Reset to initial
setCartSku(null);
```

**Why:** The setter API is identical to useState, making it familiar and easy to use.

### 5. Type Safety

**Always provide explicit types for atom values.**

✅ **Good:**
```typescript
import { atom } from 'jotai';

type CartPreferences = {
  delivery: string;
  portion: string;
};

export const cartPreferencesState = atom<CartPreferences>({
  delivery: 'standard',
  portion: 'regular',
});
```

❌ **Bad:**
```typescript
// Missing type annotation
export const cartPreferencesState = atom({
  delivery: 'standard',
  portion: 'regular',
});
```

**Why:** Explicit types prevent type errors and enable better IDE autocomplete.

## File Organization

### Standard Pattern

```
state/
├── cart/
│   ├── cartSku/
│   │   ├── cartSkuState.ts         # Atom definition
│   │   └── useCartSkuState.ts      # Custom hook
│   ├── cartPreferences/
│   │   ├── cartPreferencesState.ts # Atom definition
│   │   └── useCartPreferencesState.ts
│   └── cartProductSku/
│       ├── cartProductSkuState.ts
│       └── useCartProductSku.ts
```

**Pattern:**
1. Create a folder for each atom domain
2. Define atom in `{name}State.ts`
3. Export custom hook in `use{Name}State.ts`

## Advanced Patterns

### Derived Atoms (Read-only)

```typescript
import { atom } from 'jotai';

const priceAtom = atom(100);
const quantityAtom = atom(2);

// Derived atom (computed value)
const totalPriceAtom = atom((get) => {
  const price = get(priceAtom);
  const quantity = get(quantityAtom);
  return price * quantity;
});

// Usage
const [totalPrice] = useAtom(totalPriceAtom); // Read-only, no setter
```

### Write-only Atoms

```typescript
import { atom } from 'jotai';

const countAtom = atom(0);

// Write-only atom for incrementing
const incrementAtom = atom(
  null, // No read value
  (get, set) => {
    set(countAtom, get(countAtom) + 1);
  }
);

// Usage
const [, increment] = useAtom(incrementAtom);
increment(); // Increments countAtom
```

### Atom with Async

```typescript
import { atom } from 'jotai';

const fetchUserAtom = atom(async (get) => {
  const userId = get(userIdAtom);
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
});

// Usage
const [user] = useAtom(fetchUserAtom); // Suspends until resolved
```

## Integration with React

### With Suspense

```typescript
import { Suspense } from 'react';
import { useAtom } from 'jotai';

function UserProfile() {
  const [user] = useAtom(fetchUserAtom); // Throws promise
  return <div>{user.name}</div>;
}

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <UserProfile />
    </Suspense>
  );
}
```

### With Error Boundaries

```typescript
import { ErrorBoundary } from 'react-error-boundary';

function App() {
  return (
    <ErrorBoundary fallback={<div>Error loading data</div>}>
      <Suspense fallback={<div>Loading...</div>}>
        <UserProfile />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Testing

### Testing Atoms

```typescript
import { renderHook, act } from '@testing-library/react';
import { useAtom } from 'jotai';
import { cartSkuState } from './cartSkuState';

it('updates cart SKU', () => {
  const { result } = renderHook(() => useAtom(cartSkuState));

  expect(result.current[0]).toBe(null);

  act(() => {
    result.current[1]('new-sku');
  });

  expect(result.current[0]).toBe('new-sku');
});
```

## Common Mistakes

1. **Not providing types** - Always type your atoms explicitly
2. **Over-using Jotai for complex state** - Use Redux for complex logic
3. **Creating too many atoms** - Group related state into single atoms
4. **Not using custom hooks** - Wrap useAtom for better reusability
5. **Forgetting about initial values** - Always provide sensible defaults

## Quick Reference

### Basic Patterns

```typescript
// Define atom
import { atom } from 'jotai';
export const myAtom = atom<string>('initial');

// Custom hook
import { useAtom } from 'jotai';
export const useMyState = () => useAtom(myAtom);

// Use in component
const [value, setValue] = useMyState();

// Update
setValue('new value');
setValue((prev) => `${prev} updated`);
```

### Inline Atom

```typescript
import { atom, useAtom } from 'jotai';

const dialogAtom = atom(false);

function MyComponent() {
  const [isOpen, setIsOpen] = useAtom(dialogAtom);

  return (
    <button onClick={() => setIsOpen(true)}>
      Open Dialog
    </button>
  );
}
```

### Derived Atom

```typescript
const baseAtom = atom(10);
const derivedAtom = atom((get) => get(baseAtom) * 2);

// Usage
const [derived] = useAtom(derivedAtom); // 20
```
