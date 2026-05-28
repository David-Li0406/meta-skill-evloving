# React 19 Best Practices

React 19 introduces major improvements that simplify code and improve performance.

## React Compiler

React 19's compiler automatically memoizes components and values, eliminating most manual optimization.

### What It Does

- Automatically applies `React.memo` to components
- Automatically memoizes values (like `useMemo`)
- Automatically memoizes callbacks (like `useCallback`)

### Migration Strategy

```tsx
// React 18 - manual memoization
const ExpensiveComponent = React.memo(({ data }) => {
  const processedData = useMemo(() => processData(data), [data]);
  const handleClick = useCallback(() => onClick(data), [data, onClick]);

  return <div onClick={handleClick}>{processedData}</div>;
});

// React 19 with compiler - automatic memoization
function ExpensiveComponent({ data }) {
  const processedData = processData(data); // Auto-memoized
  const handleClick = () => onClick(data); // Auto-memoized

  return <div onClick={handleClick}>{processedData}</div>;
}
```

**When to keep manual memoization:**
- Custom comparison functions in `React.memo`
- Very expensive computations that benefit from explicit control
- During gradual migration from React 18

## Server Components

Render non-interactive components on the server to reduce client bundle size.

### Server vs Client Components

```tsx
// app/page.tsx - Server Component (default)
async function ProductPage({ params }) {
  const product = await db.products.find(params.id); // Direct DB access

  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={product.id} /> {/* Client Component */}
    </div>
  );
}

// components/AddToCartButton.tsx - Client Component
'use client'; // Directive marks as client component

import { useState } from 'react';

export function AddToCartButton({ productId }) {
  const [loading, setLoading] = useState(false);

  // Interactive logic runs on client
  const handleClick = async () => {
    setLoading(true);
    await addToCart(productId);
    setLoading(false);
  };

  return <button onClick={handleClick}>{loading ? 'Adding...' : 'Add to Cart'}</button>;
}
```

**Use Server Components for:**
- Data fetching
- Accessing backend resources (databases, file system)
- Keeping sensitive data on server (API keys)
- Large dependencies (keep them server-side)

**Use Client Components for:**
- Interactivity (onClick, onChange)
- State and effects (useState, useEffect)
- Browser-only APIs (localStorage, geolocation)
- Custom hooks that use client features

## Actions

Actions simplify form handling and data mutations with automatic pending states and error handling.

### Form Actions

```tsx
'use client';

import { useActionState } from 'react';

async function createUserAction(prevState, formData) {
  const name = formData.get('name');
  const email = formData.get('email');

  try {
    const user = await api.createUser({ name, email });
    return { success: true, user };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

export function CreateUserForm() {
  const [state, formAction, isPending] = useActionState(createUserAction, null);

  return (
    <form action={formAction}>
      <input name="name" required />
      <input name="email" type="email" required />

      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create User'}
      </button>

      {state?.error && <p className="error">{state.error}</p>}
      {state?.success && <p className="success">User created!</p>}
    </form>
  );
}
```

### Optimistic Updates

```tsx
import { useOptimistic } from 'react';

function TodoList({ todos }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo) => [...state, { ...newTodo, pending: true }]
  );

  async function createTodo(formData) {
    const title = formData.get('title');
    const tempTodo = { id: crypto.randomUUID(), title };

    addOptimisticTodo(tempTodo); // Immediately show in UI

    await api.createTodo(title); // Actual API call
  }

  return (
    <div>
      <form action={createTodo}>
        <input name="title" />
        <button>Add</button>
      </form>

      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
            {todo.title}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## New Hooks

### `use()` - Read Resources

```tsx
import { use, Suspense } from 'react';

function UserProfile({ userPromise }) {
  const user = use(userPromise); // Unwrap promise

  return <div>{user.name}</div>;
}

function App() {
  const userPromise = fetchUser('123');

  return (
    <Suspense fallback={<Spinner />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}
```

### `useFormStatus()` - Form State in Children

```tsx
import { useFormStatus } from 'react';

function SubmitButton() {
  const { pending } = useFormStatus(); // Gets status from parent form

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}

function MyForm() {
  return (
    <form action={submitAction}>
      <input name="email" />
      <SubmitButton /> {/* No need to pass pending prop */}
    </form>
  );
}
```

## Simplified ref Handling

```tsx
// React 18 - forwardRef required
const Input = forwardRef((props, ref) => {
  return <input ref={ref} {...props} />;
});

// React 19 - ref is a regular prop
function Input({ ref, ...props }) {
  return <input ref={ref} {...props} />;
}

// Usage is the same
function Form() {
  const inputRef = useRef();
  return <Input ref={inputRef} />;
}
```

## Resource Preloading

Preload resources for better performance:

```tsx
import { preload, preloadModule, preinit, preinitModule } from 'react-dom';

// Preload resources
preinit('/styles/critical.css', { as: 'style' });
preload('/fonts/custom-font.woff2', { as: 'font' });
preloadModule('/components/HeavyComponent.js');

// In components
function ProductPage() {
  // Preload related resources when component renders
  preinit('/styles/product.css', { as: 'style' });
  preloadModule('/components/ProductReviews.js');

  return <div>...</div>;
}
```

## Document Metadata

Render metadata directly in components:

```tsx
function ProductPage({ product }) {
  return (
    <>
      <title>{product.name} - My Store</title>
      <meta name="description" content={product.description} />
      <link rel="canonical" href={`https://example.com/products/${product.id}`} />

      <div>
        <h1>{product.name}</h1>
        {/* ... */}
      </div>
    </>
  );
}
```

## Migration Checklist

- [ ] Enable React Compiler (remove manual memoization gradually)
- [ ] Identify components for Server/Client split
- [ ] Replace complex form logic with Actions
- [ ] Use `useOptimistic` for better UX
- [ ] Remove `forwardRef` where possible
- [ ] Add resource preloading for critical assets
- [ ] Use new `use()` hook for promises
- [ ] Simplify form status with `useFormStatus`

React 19 makes code simpler, faster, and more maintainable - embrace the new patterns!
