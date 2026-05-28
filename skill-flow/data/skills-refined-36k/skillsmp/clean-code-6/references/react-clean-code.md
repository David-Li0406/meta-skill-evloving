# React 19 Clean Code Best Practices

## Component Principles

### Core Rules

- **Function Components**: Always use function components with the `function` keyword
- **Single Responsibility**: Each component should have one clear purpose
- **Reusability**: Design components to be reused across different contexts
- **Composability**: Build complex UIs by combining smaller components
- **No Nested Components**: Don't define components inside other components
- **Encapsulation**: Keep internal implementation details private
- **Minimal Props**: If a component needs many props, consider composition or splitting it

### JSX Best Practices

- **Key Prop**: Use the `key` prop for elements in iterables (prefer unique IDs over array indices)
- **Children Nesting**: Nest children between tags instead of passing as props
- **Ref as Prop**: Use ref as a prop instead of `React.forwardRef` (React 19+)

### Imports

- **Use React 19**: Leverage React 19 with Strict Mode enabled
- **Modern Features**: Use Suspense, `use()`, `useOptimistic()`, and `useTransition()`
- **Specific Imports**: Import only what you need: `import { useState } from 'react'`
- **Never**: `import * as React from 'react'`
- **Client/Server Directives**: Use `'use client'` for client-side, `'use server'` for server-only

### Props & Types

- **Strong Typing**: Strongly type component props
- **PropsWithChildren**: Use `PropsWithChildren<T>` for children-only props
- **Props Handling**: Use spread (`...props`) and rest operators for efficient props management

---

## Hooks

### Rules

- **Top Level Only**: Call hooks at the top level only, never conditionally or in loops
- **Custom Hooks**: Extract reusable logic into custom hooks
- **Dependency Arrays**: Specify all dependencies correctly
- **useEffect**: Provide correct dependency arrays and implement cleanup functions
- **Complex State**: Use useReducer for complex state logic
- **No Manual Memoization**: DO NOT use `useMemo` or `useCallback`; rely on React Compiler

---

## State Management

| Scenario                | Solution                        |
| ----------------------- | ------------------------------- |
| Server state (API data) | TanStack Query                  |
| Global UI state         | Zustand                         |
| Form state              | useActionState + Server Actions |
| Local UI state          | useState                        |
| Complex local state     | useReducer                      |
| Optimistic updates      | useOptimistic                   |

### Principles

- **Smart vs Dumb**: Smart components handle state/logic; dumb components handle presentation
- **State Lifting**: Share state between related components without prop drilling
- **Context API**: Use React Context for global state across the app
- **Keep State Local**: Keep state as local as possible; lift only when needed

---

## Performance Optimization

- **No Manual Memoization**: DO NOT use `useMemo` or `useCallback`; React Compiler handles this
- **Re-render Optimization**: Use React DevTools Performance tab to identify bottlenecks
- **Virtualization**: Implement virtualization for long lists with FlashList
- **Code Splitting**: Use dynamic imports for route-based code splitting
- **Lazy Loading**: Lazy load non-critical components
- **Anonymous Functions**: Avoid in render methods or component props
- **Suspense**: Wrap client components in `Suspense` with fallback UI
- **Error Boundaries**: Implement appropriate error boundaries
- **Avoid Spread in Loops**: Don't use spread syntax in accumulators within loops
- **Top-level Regex**: Use top-level regex literals instead of creating them in loops
- **Specific Imports**: Prefer specific imports over namespace imports
- **No Barrel Files**: Avoid barrel files (index files that re-export everything)
- **Image Components**: Use proper image components (e.g., Next.js `<Image>`) over `<img>` tags

---

## New React 19 Hooks

### `use()` - Reading Promises and Context

Can be called conditionally (unlike other hooks):

```typescript
import { use } from 'react';

function Component({ shouldLoad }: { shouldLoad: boolean }) {
  let data = null;

  if (shouldLoad) {
    // use() can be called conditionally!
    data = use(fetchDataPromise);
  }

  return <div>{data}</div>;
}
```

### `useActionState()` - Form Actions

Replaces manual form state management:

```typescript
'use client';

import { useActionState } from 'react';

function LoginForm() {
  const [error, submitAction, isPending] = useActionState(
    async (prevState, formData: FormData) => {
      const result = await login(formData);
      if (result.error) return result.error;
      redirect('/dashboard');
      return null;
    },
    null
  );

  return (
    <form action={submitAction}>
      <input name="email" type="email" required />
      <input name="password" type="password" required />
      <button disabled={isPending}>
        {isPending ? 'Logging in...' : 'Login'}
      </button>
      {error && <p className="text-red-500">{error}</p>}
    </form>
  );
}
```

### `useFormStatus()` - Form Submission State

Access form state from child components:

```typescript
'use client';

import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button disabled={pending} type="submit">
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}

function Form({ action }: { action: (data: FormData) => Promise<void> }) {
  return (
    <form action={action}>
      <input name="title" />
      <SubmitButton /> {/* Has access to form state */}
    </form>
  );
}
```

### `useOptimistic()` - Instant UI Updates

Show expected result immediately:

```typescript
'use client';

import { useOptimistic } from 'react';

function TodoList({ todos, addTodo }: Props) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, newTodo]
  );

  async function handleSubmit(formData: FormData) {
    const title = formData.get('title') as string;
    const newTodo = { id: crypto.randomUUID(), title, completed: false };

    // Instantly show in UI
    addOptimisticTodo(newTodo);

    // Then persist to server
    await addTodo(newTodo);
  }

  return (
    <>
      <form action={handleSubmit}>
        <input name="title" />
        <button type="submit">Add</button>
      </form>
      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id}>{todo.title}</li>
        ))}
      </ul>
    </>
  );
}
```

---

## Refs Simplified (No More forwardRef)

React 19 allows `ref` as a regular prop:

```typescript
// OLD (React 18)
const Button = forwardRef<HTMLButtonElement, Props>((props, ref) => {
  return <button ref={ref} {...props} />;
});

// NEW (React 19)
function Button({ ref, ...props }: Props & { ref?: React.Ref<HTMLButtonElement> }) {
  return <button ref={ref} {...props} />;
}
```

---

## Document Metadata

Render metadata directly in components:

```typescript
function BlogPost({ post }: { post: Post }) {
  return (
    <article>
      <title>{post.title}</title>
      <meta name="description" content={post.excerpt} />
      <meta name="author" content={post.author} />

      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
// React automatically hoists to <head>
```

---

## React Compiler - No Manual Memoization

React 19 Compiler handles optimization automatically:

```typescript
// OLD (React 18) - Manual optimization
function ExpensiveComponent({ data, onClick }: Props) {
  const processed = useMemo(() => expensiveWork(data), [data]);
  const handleClick = useCallback(() => onClick(), [onClick]);

  return <Child data={processed} onClick={handleClick} />;
}
export default memo(ExpensiveComponent);

// NEW (React 19) - Let compiler optimize
function ExpensiveComponent({ data, onClick }: Props) {
  const processed = expensiveWork(data);

  return <Child data={processed} onClick={onClick} />;
}
```

---

## Component Patterns

### Keep Components Small

```typescript
// BAD - Giant component
function Dashboard() {
  // 300 lines of mixed concerns
}

// GOOD - Composed from smaller parts
function Dashboard() {
  return (
    <DashboardLayout>
      <Suspense fallback={<HeaderSkeleton />}>
        <DashboardHeader />
      </Suspense>
      <Suspense fallback={<StatsSkeleton />}>
        <DashboardStats />
      </Suspense>
    </DashboardLayout>
  );
}
```

### Server Actions for Mutations

```typescript
// actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  await db.post.create({ data: { title, content } });
  revalidatePath('/posts');
}

// Component
'use client';

import { createPost } from './actions';

function NewPostForm() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

---

## Custom Hooks for Logic

```typescript
// Extract data fetching logic
function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => api.getUser(userId),
  });
}

// Extract form logic
function useLoginForm() {
  const [error, action, isPending] = useActionState(loginAction, null);

  return { error, action, isPending };
}

// Component becomes simple
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useUser(userId);

  if (isLoading) return <Skeleton />;
  return <ProfileCard user={user} />;
}
```

---

## State Management Decision Tree

| Scenario                | Solution                        |
| ----------------------- | ------------------------------- |
| Server state (API data) | TanStack Query                  |
| Global UI state         | Zustand                         |
| Form state              | useActionState + Server Actions |
| Local UI state          | useState                        |
| Complex local state     | useReducer                      |
| Optimistic updates      | useOptimistic                   |

---

## Resource Preloading

```typescript
import { prefetchDNS, preconnect, preload, preinit } from 'react-dom';

function App() {
  // Critical script - load and execute immediately
  preinit('https://cdn.example.com/critical.js', { as: 'script' });

  // Font - preload for later use
  preload('https://fonts.example.com/font.woff2', { as: 'font' });

  // External API - early connection
  preconnect('https://api.example.com');

  // Third-party domain - DNS prefetch
  prefetchDNS('https://analytics.example.com');

  return <MainContent />;
}
```

---

## Suspense & Code Splitting

```typescript
import { Suspense, lazy } from 'react';

// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));
const MarkdownEditor = lazy(() => import('./MarkdownEditor'));

function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<ChartSkeleton />}>
        <HeavyChart />
      </Suspense>

      <Suspense fallback={<EditorSkeleton />}>
        <MarkdownEditor />
      </Suspense>
    </div>
  );
}
```

---

## Error Boundaries

```typescript
'use client';

import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert" className="p-4 bg-red-50 rounded">
      <h2 className="font-bold text-red-800">Something went wrong</h2>
      <pre className="text-sm text-red-600">{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <Router />
    </ErrorBoundary>
  );
}
```

---

## Activity Component (React 19.2+)

Better than conditional rendering:

```typescript
// OLD - Unmounts component
{isVisible && <HeavyComponent />}

// NEW - Keeps mounted but inactive
<Activity mode={isVisible ? 'visible' : 'hidden'}>
  <HeavyComponent />
</Activity>
```

Benefits:

- Deferred updates for hidden components
- Pre-rendering in background
- State preserved when hidden

---

## Anti-Patterns

| Pattern                  | Problem                     | Solution               |
| ------------------------ | --------------------------- | ---------------------- |
| useEffect for fetching   | No caching, race conditions | TanStack Query         |
| useState for server data | Manual loading/error        | TanStack Query         |
| Props drilling 3+ levels | Hard to maintain            | Zustand or Context     |
| Giant components         | Untestable                  | Split into smaller     |
| Manual memoization       | Verbose, error-prone        | React Compiler         |
| forwardRef               | Verbose                     | ref as prop (React 19) |
| Manual form state        | Boilerplate                 | useActionState         |
