---
name: react
description: Use when writing React components, creating hooks, using useState/useEffect/useReducer, building Next.js pages, implementing Server Components or Client Components, working with Remix loaders, Astro islands, or Vite SPA. Use for React performance issues, re-render problems, or component refactoring.
---

# React Development

## Overview

Write components that are small, focused, and follow framework conventions. Detect the framework first - patterns differ significantly between Next.js App Router, Remix, Vite SPA, and Astro.

## When to Use

- Creating any React component
- Choosing state management approach
- Deciding client vs server rendering
- Optimizing re-renders
- Setting up data fetching

## Framework Detection

**Always check before writing React code:**

```typescript
// Check package.json for framework
import pkg from './package.json';

const framework = detectFramework(pkg.dependencies);
// 'next' → Next.js (check for app/ vs pages/)
// '@remix-run/react' → Remix
// 'astro' → Astro
// 'vite' only → Vite SPA
// none → Create React App or custom
```

| File/Config | Framework | Router Type |
|------------|-----------|-------------|
| `app/` directory + `next.config` | Next.js App Router | File-based, RSC |
| `pages/` directory + `next.config` | Next.js Pages Router | File-based, CSR/SSR |
| `remix.config.js` or `@remix-run/*` | Remix | Nested, loader-based |
| `astro.config.mjs` | Astro | Islands, mostly static |
| `vite.config.ts` only | Vite SPA | Client-side only |

## The Iron Rules

### 1. 'use client' Goes at File Top - NEVER Middle

```typescript
// ❌ FATAL: This breaks compilation
function ServerComponent() { ... }

'use client'; // WRONG - can't be after other code

function ClientComponent() { ... }

// ✅ CORRECT: Separate files
// -- server-component.tsx --
export function ServerComponent() { ... }

// -- client-component.tsx --
'use client';
export function ClientComponent() { ... }
```

**Never write "for demonstration" code that violates this.** Broken code teaches nothing.

### 2. Server Components by Default (Next.js App Router)

Data fetching belongs on the server. Only add 'use client' when you need:
- Event handlers (onClick, onChange)
- useState, useEffect, useReducer
- Browser APIs (localStorage, window)

**Keep 'use client' boundaries deep** to minimize JavaScript bundle size.

```typescript
// ✅ GOOD: Server Component fetches data
// app/products/page.tsx
async function ProductsPage() {
  const products = await db.product.findMany(); // Direct DB access
  return <ProductList products={products} />;
}

// ❌ BAD: Client Component fetches in useEffect
'use client';
function ProductsPage() {
  const [products, setProducts] = useState([]);
  useEffect(() => {
    fetch('/api/products').then(...) // Extra round-trip
  }, []);
}

// ✅ GOOD: Mixed - only Search is client
function Layout({ children }) {
  return (
    <nav>
      <Logo /> {/* Server Component */}
      <Search /> {/* 'use client' - only this interactive */}
    </nav>
  );
}
```

### 3. Component Responsibilities: Max 3 Concerns

A component should handle at most 3 concerns:
1. Data → Layout → Interaction (orchestrator)
2. Fetch → Transform → Display (data component)
3. State → Render → Events (interactive component)

If you have more, split.

```typescript
// ❌ BAD: Too many concerns
function ProductPage() {
  // Fetching
  // Validation
  // Cart logic
  // Analytics
  // Rendering
  // Error handling
}

// ✅ GOOD: Split by concern
function ProductPage() {
  return (
    <ProductDataProvider>
      <ProductDisplay />
      <AddToCartButton />
    </ProductDataProvider>
  );
}
```

### 4. State Placement Decision Tree

```
Need state?
├── Used by 1 component → useState in that component
├── Used by siblings → lift to parent
├── Used across routes → URL params or context
├── Complex/async → useReducer or server state (TanStack Query)
└── Global → Zustand or Jotai (NOT Redux unless massive app)
```

### 5. Hooks Rules

```typescript
// ❌ BAD: Conditional hook
if (condition) {
  useEffect(() => { ... }); // Breaks rules of hooks
}

// ✅ GOOD: Condition inside hook
useEffect(() => {
  if (!condition) return;
  // ... effect logic
}, [condition]);

// ❌ BAD: Too many useState
const [name, setName] = useState('');
const [email, setEmail] = useState('');
const [error, setError] = useState(null);
const [loading, setLoading] = useState(false);
const [submitted, setSubmitted] = useState(false);

// ✅ GOOD: Related state in reducer
const [formState, dispatch] = useReducer(formReducer, initialState);
```

### 6. Server Actions for Forms (Next.js App Router)

Server Actions handle mutations without API routes. Use `useActionState` (React 19+) for form state.

```typescript
// ✅ GOOD: Server Action with validation
'use server';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2)
});

export async function createUser(prevState: any, formData: FormData) {
  const validatedFields = schema.safeParse({
    email: formData.get('email'),
    name: formData.get('name')
  });

  if (!validatedFields.success) {
    return { errors: validatedFields.error.flatten().fieldErrors };
  }

  // Return error object, DON'T throw
  const result = await db.user.create(validatedFields.data);
  if (!result.ok) return { message: 'Failed to create user' };

  redirect('/users');
}

// Client Component using the action
'use client';
import { useActionState } from 'react';

export function SignupForm() {
  const [state, formAction, isPending] = useActionState(createUser, { message: '' });

  return (
    <form action={formAction}>
      <input type="email" name="email" required />
      {state?.errors?.email && <p>{state.errors.email}</p>}

      <input type="text" name="name" required />
      {state?.errors?.name && <p>{state.errors.name}</p>}

      <button disabled={isPending}>Sign up</button>
      {state?.message && <p aria-live="polite">{state.message}</p>}
    </form>
  );
}
```

**Key patterns:**
- Server Actions return error objects, never throw
- Use `useActionState` for form state + pending + errors
- Progressive enhancement: works without JS
- Validate with Zod in Server Action

## React 19 Features

### React Compiler (Auto-Memoization)

React Compiler automatically adds memoization - no more manual `useMemo`, `useCallback`, or `React.memo`.

```typescript
// ❌ OLD: Manual memoization everywhere
const MemoizedComponent = React.memo(({ user }) => {
  const formattedName = useMemo(() => formatName(user), [user]);
  const handleClick = useCallback(() => saveUser(user), [user]);
  return <button onClick={handleClick}>{formattedName}</button>;
});

// ✅ NEW: React Compiler handles it automatically
function UserButton({ user }) {
  const formattedName = formatName(user);
  const handleClick = () => saveUser(user);
  return <button onClick={handleClick}>{formattedName}</button>;
}
// Compiler adds memoization during build - 25-40% fewer re-renders
```

**Key benefits:**
- No manual memoization needed
- Reduces bundle size (no memo wrappers)
- 25-40% fewer re-renders in typical apps
- Works with existing React 19 codebases

**Enable in Next.js 15+:**
```javascript
// next.config.js
module.exports = {
  experimental: {
    reactCompiler: true,
  },
};
```

### Server/Client Component Decision Tree

```
Need this in the component?
├── Event handlers (onClick, onChange) → 'use client'
├── useState, useEffect, useReducer → 'use client'
├── Browser APIs (localStorage, window) → 'use client'
├── Third-party client libs (charts, maps) → 'use client'
│
├── Data fetching from DB/API → Server Component ✅
├── Access backend resources → Server Component ✅
├── Keep sensitive data (tokens, keys) → Server Component ✅
└── Reduce client bundle → Server Component ✅
```

**Rule of thumb:** Start with Server Components. Only add 'use client' when you hit a boundary that requires it.

### use() Hook - Read Promises/Context

```typescript
import { use } from 'react';

// ✅ Read promise in component
function Message({ messagePromise }: { messagePromise: Promise<string> }) {
  const message = use(messagePromise); // Suspends until resolved
  return <p>{message}</p>;
}

// ✅ Read context without Consumer
function Button() {
  const theme = use(ThemeContext);
  return <button className={theme}>Click</button>;
}
```

### useOptimistic - Instant UI Updates

```typescript
'use client';
import { useOptimistic } from 'react';

function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, newTodo]
  );

  async function handleAdd(formData: FormData) {
    const newTodo = { id: Date.now(), text: formData.get('todo') };
    addOptimistic(newTodo); // Instant update
    await addTodo(formData); // Server mutation
  }

  return (
    <form action={handleAdd}>
      <input name="todo" />
      <button type="submit">Add</button>
      <ul>
        {optimisticTodos.map(todo => <li key={todo.id}>{todo.text}</li>)}
      </ul>
    </form>
  );
}
```

**Auto-reverts on error** - no manual rollback needed.

### Partial Pre-rendering (PPR) - Next.js 15+

Combine static shell with dynamic content in a single request:

```typescript
// app/products/[id]/page.tsx
import { Suspense } from 'react';

// Static shell - pre-rendered at build time
export default async function ProductPage({ params }) {
  const product = await getProduct(params.id); // Cached/static

  return (
    <div>
      {/* Static content - instant load */}
      <h1>{product.name}</h1>
      <p>{product.description}</p>

      {/* Dynamic content - streams in */}
      <Suspense fallback={<PriceSkeleton />}>
        <DynamicPrice productId={params.id} />
      </Suspense>

      <Suspense fallback={<InventorySkeleton />}>
        <InventoryStatus productId={params.id} />
      </Suspense>
    </div>
  );
}

// Dynamic component - fetches real-time data
async function DynamicPrice({ productId }) {
  const price = await getCurrentPrice(productId); // Always fresh
  return <span className="price">${price}</span>;
}
```

**Enable PPR:**
```javascript
// next.config.js
module.exports = {
  experimental: {
    ppr: true,
  },
};
```

**Benefits:**
- Static shell loads instantly (like SSG)
- Dynamic parts stream in (like SSR)
- Best of both worlds in one request
- No full-page waterfall

## Streaming & Suspense

### Full Page Streaming with loading.tsx

```typescript
// app/posts/loading.tsx
export default function Loading() {
  return <PostsSkeleton />;
}

// app/posts/page.tsx (automatically wrapped in Suspense)
export default async function PostsPage() {
  const posts = await fetchPosts(); // Streams when ready
  return <PostsList posts={posts} />;
}
```

### Granular Streaming with Suspense

```typescript
import { Suspense } from 'react';

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1> {/* Sent immediately */}

      <Suspense fallback={<StatsSkeleton />}>
        <Stats /> {/* Async, streams later */}
      </Suspense>

      <Suspense fallback={<ChartSkeleton />}>
        <RevenueChart /> {/* Async, independent stream */}
      </Suspense>
    </div>
  );
}
```

**Benefits:**
- TTFB improvement - show shell instantly
- Independent loading states
- Partial prefetching for faster navigation

## Quick Reference: Framework Patterns

| Task | Next.js App Router | Remix | Vite SPA |
|------|-------------------|-------|----------|
| Data fetching | async component | loader function | useQuery |
| Mutations | Server Action | action function | useMutation |
| Loading UI | loading.tsx | useNavigation | suspense |
| Error UI | error.tsx | ErrorBoundary | ErrorBoundary |
| Metadata | metadata export | meta function | react-helmet |
| Navigation | Link + router | Link + navigate | Link + navigate |

## Testing Strategy

| What to Test | How |
|--------------|-----|
| Server Components | Import directly, verify data fetching |
| Client Components | Render with Testing Library, verify interactions |
| Server Actions | Call with FormData, assert return values |
| Suspense fallbacks | Wait for async resolution, verify both states |
| Forms with useActionState | Submit form, verify pending/error/success states |

```typescript
// Test Server Component
import ProductsPage from '@/app/products/page';

test('fetches and displays products', async () => {
  const result = await ProductsPage(); // It's an async function
  expect(result.props.children).toContain('Product 1');
});

// Test Server Action
import { createUser } from '@/app/actions';

test('validates email format', async () => {
  const formData = new FormData();
  formData.set('email', 'invalid');

  const result = await createUser(null, formData);
  expect(result.errors.email).toBeDefined();
});

// Test Client Component with Suspense
import { render, waitFor } from '@testing-library/react';

test('shows fallback then content', async () => {
  const { getByText, queryByText } = render(
    <Suspense fallback={<div>Loading...</div>}>
      <AsyncComponent />
    </Suspense>
  );

  expect(getByText('Loading...')).toBeInTheDocument();
  await waitFor(() => expect(queryByText('Loading...')).not.toBeInTheDocument());
  expect(getByText('Content')).toBeInTheDocument();
});
```

## References

- [Next.js Documentation](https://nextjs.org/docs) - App Router, Server Components, Server Actions
- [React 19 Release](https://react.dev/blog/2024/12/05/react-19) - use(), useActionState, useOptimistic
- [React Compiler](https://react.dev/learn/react-compiler) - Auto-memoization setup and usage
- [React Server Components](https://react.dev/reference/rsc/server-components) - Official RSC guide

**Version Notes:**
- Next.js 14+: App Router stable, Server Actions stable
- Next.js 15: Turbopack stable, React Compiler support, PPR experimental
- React 19: use(), Actions, useOptimistic, useActionState
- React 19.2+: Partial Pre-rendering (PPR), enhanced Suspense
- React Compiler: Auto-memoization, 25-40% fewer re-renders

## Red Flags - STOP and Restructure

| Thought | Reality |
|---------|---------|
| "I'll put 'use client' here just for demo" | Broken code teaches nothing. Write it correctly. |
| "This component does a lot but it's fine" | Max 3 concerns. Split now. |
| "I'll fetch client-side, it's simpler" | Server fetching is simpler AND faster. |
| "Let me add useState for this" | Check: can it be URL params, server state, or derived? |
| "Redux for this small app" | Zustand/Jotai unless you have 50+ reducers. |
| "I need useEffect for this fetch" | In Next.js/Remix: no. Use server components or loaders. |
| "I'll create an API route for this form" | Use Server Actions - no API route needed. |
| "Let me throw an error in Server Action" | Return error object for useActionState. Don't throw. |
| "I'll add 'use client' to the whole layout" | Keep boundaries deep. Only interactive parts need it. |
| "Forms need JavaScript to work" | Server Actions work with progressive enhancement. |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 'use client' not at file top | Move to separate file |
| useEffect for data fetching in Next.js | Server component or loader |
| Prop drilling 3+ levels | Context or composition |
| Re-render on every keystroke | Debounce or uncontrolled input |
| window/localStorage in server component | 'use client' or dynamic import |
| Inline function in JSX causing re-renders | useCallback or extract |