---
name: nextjs-project
description: Best practices and conventions for working with Next.js 16 App Router projects using TypeScript, Tailwind CSS v4, and React 19. Use when working on Next.js components, pages, API routes, server actions, writing tests, or configuring Next.js features.
---

# Next.js Project Guidelines

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

### Server Components (Default)

Use Server Components by default. They run on the server, reducing client bundle size.

```tsx
// ✅ Server Component (default)
export default async function Page() {
  const data = await fetch('https://api.example.com/data');
  return <div>{/* render data */}</div>;
}
```

### Client Components

Use `'use client'` directive only when needed:
- Event handlers (onClick, onChange)
- Browser APIs (localStorage, window)
- React hooks (useState, useEffect, useContext)
- Third-party libraries requiring client-side execution

```tsx
'use client';

import { useState } from 'react';

export default function ClientComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Component Organization

- Keep Server Components as the default
- Extract interactive parts into small Client Components
- Colocate related components in feature folders

```tsx
// app/products/page.tsx (Server Component)
import ProductList from '@/components/products/ProductList';
import ProductFilters from '@/components/products/ProductFilters';

export default async function ProductsPage() {
  const products = await getProducts();
  return (
    <div>
      <ProductFilters /> {/* Client Component */}
      <ProductList products={products} /> {/* Server Component */}
    </div>
  );
}
```

## Routing

### File-based Routing

- `app/page.tsx` → `/`
- `app/about/page.tsx` → `/about`
- `app/blog/[slug]/page.tsx` → `/blog/:slug`
- `app/shop/[...slug]/page.tsx` → `/shop/*` (catch-all)
- `app/docs/[[...slug]]/page.tsx` → `/docs` and `/docs/*` (optional catch-all)

### Dynamic Routes

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);
  return <article>{post.content}</article>;
}
```

### Route Groups

Use `(groupName)` for organization without affecting URL:

```
app/
  (marketing)/
    about/
    contact/
  (dashboard)/
    admin/
    settings/
```

## Data Fetching

### Server Components

Fetch data directly in Server Components:

```tsx
export default async function Page() {
  // ✅ Fetch in Server Component
  const res = await fetch('https://api.example.com/data', {
    cache: 'no-store', // or 'force-cache', { next: { revalidate: 3600 } }
  });
  const data = await res.json();
  return <div>{data.title}</div>;
}
```

### Server Actions

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

// app/components/CreatePostForm.tsx
'use client';

import { createPost } from '@/app/actions';

export default function CreatePostForm() {
  return (
    <form action={createPost}>
      <input name="title" />
      <button type="submit">Create</button>
    </form>
  );
}
```

### Route Handlers (API Routes)

```tsx
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const posts = await getPosts();
  return NextResponse.json(posts);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const post = await createPost(body);
  return NextResponse.json(post, { status: 201 });
}
```

## Metadata and SEO

### Static Metadata

```tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
  openGraph: {
    title: 'OG Title',
    description: 'OG Description',
  },
};
```

### Dynamic Metadata

```tsx
export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.excerpt,
  };
}
```

## Styling with Tailwind CSS v4

### Class Conventions

- Use Tailwind utility classes directly
- Prefer composition over custom CSS
- Use dark mode variants: `dark:bg-zinc-900`

```tsx
<div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black">
  <h1 className="text-3xl font-semibold text-black dark:text-zinc-50">
    Title
  </h1>
</div>
```

### Responsive Design

```tsx
<div className="flex flex-col sm:flex-row md:grid lg:flex">
  {/* Mobile-first responsive classes */}
</div>
```

## TypeScript Patterns

### Type Safety

- Use TypeScript for all components
- Define prop types explicitly
- Use `Readonly<>` for props when appropriate

```tsx
interface PageProps {
  params: Readonly<{ slug: string }>;
  searchParams: Readonly<{ [key: string]: string | string[] | undefined }>;
}

export default function Page({ params, searchParams }: PageProps) {
  // ...
}
```

### Path Aliases

Use `@/` alias for imports:

```tsx
import { Button } from '@/components/ui/Button';
import { formatDate } from '@/lib/utils';
```

## Performance Optimization

### Image Optimization

Always use `next/image`:

```tsx
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Description"
  width={800}
  height={600}
  priority // For above-the-fold images
/>
```

### Font Optimization

Use `next/font`:

```tsx
import { Geist } from 'next/font/google';

const geist = Geist({
  variable: '--font-geist',
  subsets: ['latin'],
});
```

### Loading States

Create `loading.tsx` files:

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <div>Loading...</div>;
}
```

### Error Boundaries

Create `error.tsx` files:

```tsx
'use client';

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

## Common Patterns

### Form Handling

```tsx
'use client';

import { useFormState } from 'react-dom';
import { submitForm } from './actions';

export default function Form() {
  const [state, formAction] = useFormState(submitForm, null);
  
  return (
    <form action={formAction}>
      <input name="email" type="email" required />
      {state?.error && <p>{state.error}</p>}
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Revalidation

```tsx
import { revalidatePath, revalidateTag } from 'next/cache';

// Revalidate specific path
revalidatePath('/posts');

// Revalidate by tag
revalidateTag('posts');
```

## Testing

### When to Create Tests

Create unit tests for:
- **Utility functions** (`lib/` directory) - Pure functions, helpers, formatters
- **Client Components** - Interactive components with user interactions
- **Server Actions** - Form submissions, data mutations, validation logic
- **API Routes** - Route handlers, request/response handling
- **Complex logic** - Business logic, calculations, data transformations

### Test File Naming

Colocate test files next to the code they test:
- `Button.tsx` → `Button.test.tsx`
- `utils.ts` → `utils.test.ts`
- `route.ts` → `route.test.ts`

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode (development)
npm test -- --watch

# Run tests for specific file
npm test Button.test.tsx

# Run tests with coverage
npm test -- --coverage
```

### Quick Test Examples

**Utility Function:**
```tsx
// lib/formatDate.test.ts
import { formatDate } from './formatDate';

describe('formatDate', () => {
  it('formats date correctly', () => {
    expect(formatDate(new Date('2024-01-15'))).toBe('Jan 15, 2024');
  });
});
```

**Client Component:**
```tsx
// components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

**Server Action:**
```tsx
// app/actions.test.ts
import { createPost } from './actions';

describe('createPost', () => {
  it('validates required fields', async () => {
    const formData = new FormData();
    const result = await createPost(formData);
    
    expect(result.error).toBeDefined();
  });
});
```

**API Route:**
```tsx
// app/api/posts/route.test.ts
import { GET } from './route';
import { NextRequest } from 'next/server';

describe('GET /api/posts', () => {
  it('returns posts', async () => {
    const request = new NextRequest('http://localhost/api/posts');
    const response = await GET(request);
    
    expect(response.status).toBe(200);
  });
});
```

### Test Setup

Ensure test scripts are configured in `package.json`:

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch"
  }
}
```

For detailed testing patterns, see the `nextjs-testing` skill.

## Best Practices

1. **Default to Server Components** - Only use Client Components when necessary
2. **Colocate related code** - Keep components, styles, and utilities together
3. **Use TypeScript strictly** - Enable strict mode and type everything
4. **Optimize images** - Always use `next/image`
5. **Handle loading states** - Create `loading.tsx` files
6. **Handle errors gracefully** - Create `error.tsx` files
7. **Use Server Actions** - For form submissions and mutations
8. **Cache appropriately** - Use fetch cache options and revalidation
9. **Keep components small** - Extract logic into separate functions/components
10. **Follow file naming** - Use `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`
11. **Write tests for critical logic** - Test utilities, components, and API routes

## React 19 Considerations

- Use Server Components as default
- Leverage async Server Components
- Use Server Actions for mutations
- Prefer form actions over manual state management when possible
- Use `useFormState` and `useFormStatus` hooks for form handling
