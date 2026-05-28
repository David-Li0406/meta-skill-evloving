---
name: nextjs-react-best-practices
description: Use this skill when working with Next.js 16 and React 19 to implement best practices, optimize performance, and maintain a clean codebase using TypeScript and Tailwind CSS v4.
---

# Next.js and React Best Practices

This document outlines best practices and conventions for working with Next.js 16 App Router and React 19, focusing on performance optimization, code organization, and component design.

## Project Structure

This project uses Next.js 16 App Router with TypeScript and Tailwind CSS v4.

### Directory Conventions

- `app/` - App Router directory (routes, layouts, pages)
- `app/[route]/page.tsx` - Page components
- `app/[route]/layout.tsx` - Layout components
- `app/[route]/loading.tsx` - Loading UI
- `app/[route]/error.tsx` - Error boundaries
- `app/[route]/not-found.tsx` - 404 pages
- `app/api/` - API routes (Route Handlers)
- `components/` - Shared React components
- `components/[component]/[Component].test.tsx` - Component tests (colocated)
- `lib/` - Utility functions and helpers
- `lib/[util].test.ts` - Utility tests (colocated)
- `public/` - Static assets

## Component Patterns

### Server vs Client Components

- **Default to Server Components** for pages/layouts/data widgets.
- Use `'use client'` only for:
  - Local state / effects
  - Browser-only APIs (`window`, `localStorage`)
  - Event handlers (`onClick`, etc.)
- Keep client components as leaf nodes; pass in plain serializable props.

### Component Organization

- Keep Server Components as the default.
- Extract interactive parts into small Client Components.
- Colocate related components in feature folders.

### Data Fetching

#### Server Components

Fetch data directly in Server Components:

```tsx
export default async function Page() {
  const res = await fetch('https://api.example.com/data', {
    cache: 'no-store',
  });
  const data = await res.json();
  return <div>{data.title}</div>;
}
```

#### Server Actions

Use Server Actions for mutations:

```tsx
// app/actions.ts
'use server';

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  // Validate and save
  revalidatePath('/posts');
  redirect('/posts');
}
```

### Performance Optimization

#### Avoid Unnecessary Re-renders

- Don’t create new inline objects/arrays/functions in JSX unless needed.
- Use `useCallback`/`useMemo` when it materially reduces renders.
- Split large components; memoize leaf components when props are stable.

#### Image Optimization

Always use `next/image`:

```tsx
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Description"
  width={800}
  height={600}
  priority
/>
```

### Styling with Tailwind CSS v4

- Use Tailwind utility classes directly.
- Prefer composition over custom CSS.
- Use dark mode variants: `dark:bg-zinc-900`.

## TypeScript Patterns

### Type Safety

- Use TypeScript for all components.
- Define prop types explicitly.
- Use `Readonly<>` for props when appropriate.

## Testing

### When to Create Tests

Create unit tests for:
- Utility functions
- Client Components
- Server Actions
- API Routes
- Complex logic

### Test File Naming

Colocate test files next to the code they test:
- `Button.tsx` → `Button.test.tsx`
- `utils.ts` → `utils.test.ts`

### Running Tests

```bash
# Run all tests
npm test
```

## Best Practices

1. **Default to Server Components** - Only use Client Components when necessary.
2. **Colocate related code** - Keep components, styles, and utilities together.
3. **Use TypeScript strictly** - Enable strict mode and type everything.
4. **Optimize images** - Always use `next/image`.
5. **Handle loading states** - Create `loading.tsx` files.
6. **Handle errors gracefully** - Create `error.tsx` files.
7. **Use Server Actions** - For form submissions and mutations.
8. **Cache appropriately** - Use fetch cache options and revalidation.
9. **Keep components small** - Extract logic into separate functions/components.
10. **Write tests for critical logic** - Test utilities, components, and API routes.

## Common Anti-patterns

### Avoid: Overusing Barrel Imports

- Small, curated barrels are fine, but avoid creating “mega barrels” that hide expensive imports or create circular dependencies.

### Avoid: Sequential Awaits

```javascript
// Bad - waterfall
const data1 = await fetchData1();
const data2 = await fetchData2();

// Good - parallel
const [data1, data2] = await Promise.all([fetchData1(), fetchData2()]);
```

### Avoid: Inline Objects in JSX

```javascript
// Bad - new object every render
<Component style={{ margin: 10 }} config={{ enabled: true }} />;

// Good - stable references
const style = useMemo(() => ({ margin: 10 }), []);
const config = useMemo(() => ({ enabled: true }), []);
<Component style={style} config={config} />;
```

### Avoid: Missing Dependencies

```javascript
// Bad - stale closure
useEffect(() => {
  fetchData(userId);
}, []);

// Good - correct dependencies
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

### Avoid: Conditional Rendering with &&

```javascript
// Bad - renders "0" if count is 0
{
  count && <Badge count={count} />;
}

// Good - explicit boolean
{
  count > 0 && <Badge count={count} />;
}
```

## React 19 Considerations

- Use Server Components as default.
- Leverage async Server Components.
- Use Server Actions for mutations.
- Prefer form actions over manual state management when possible.