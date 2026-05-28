---
name: nextjs
description: Best practices and guidelines for working with Next.js 16 App Router
---

# Next.js Development Guidelines

## Project Structure

This project uses Next.js 16.1.1 with the App Router. Key conventions:

- **App Directory**: Use the `app/` directory for all routes and layouts
- **File-based Routing**: Routes are created using the file system in the `app/` directory
- **Layouts**: Use `layout.tsx` files for shared UI across routes
- **Pages**: Use `page.tsx` files to create route segments
- **Server Components by Default**: All components are Server Components unless marked with `'use client'`

## Component Guidelines

### Server vs Client Components

- **Default to Server Components**: Most components should be Server Components for better performance
- **Use Client Components** (`'use client'`) only when needed for:
  - Interactive features (onClick, onChange, etc.)
  - Browser APIs (localStorage, window, etc.)
  - React hooks (useState, useEffect, useContext, etc.)
  - Third-party libraries that require client-side JavaScript

### Component Patterns

```typescript
// Server Component (default)
export default function ServerComponent() {
  return <div>Server Component</div>;
}

// Client Component
'use client';
import { useState } from 'react';

export default function ClientComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

## Routing

- **Dynamic Routes**: Use `[param]` folders for dynamic segments (e.g., `app/users/[id]/page.tsx`)
- **Route Groups**: Use `(folderName)` for organization without affecting the URL
- **Nested Routes**: Create nested layouts by adding `layout.tsx` in subdirectories
- **Loading States**: Use `loading.tsx` for route-level loading UI
- **Error Boundaries**: Use `error.tsx` for route-level error handling
- **Not Found**: Use `not-found.tsx` for custom 404 pages

## Data Fetching

- **Server Components**: Fetch data directly in Server Components using async/await
- **No useEffect for Data**: Don't use useEffect for data fetching in Server Components
- **API Routes**: Create API routes in `app/api/` directory using `route.ts` files
- **Caching**: Leverage Next.js caching with `fetch` options (`cache`, `revalidate`, etc.)

```typescript
// Server Component data fetching
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // Revalidate every hour
  });
  const json = await data.json();
  return <div>{json.title}</div>;
}
```

## Image Optimization

- **Always use `next/image`**: Import from `next/image` for optimized images
- **Required Props**: Always provide `width`, `height`, and `alt` props
- **Priority**: Use `priority` prop for above-the-fold images
- **Responsive Images**: Use `fill` with a container for responsive images

```typescript
import Image from 'next/image';

<Image
  src="/image.jpg"
  alt="Description"
  width={500}
  height={300}
  priority // for above-the-fold images
/>
```

## Metadata and SEO

- **Metadata Export**: Use the `metadata` export in `layout.tsx` or `page.tsx`
- **Dynamic Metadata**: Use `generateMetadata` function for dynamic metadata
- **Type Safety**: Import `Metadata` type from `next`

```typescript
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
};
```

## Styling

- **Tailwind CSS**: This project uses Tailwind CSS v4
- **CSS Modules**: Can be used alongside Tailwind if needed
- **Global Styles**: Add global styles in `app/globals.css`
- **Dark Mode**: Support dark mode using Tailwind's `dark:` variant

## TypeScript

- **Type Safety**: Leverage TypeScript for all components and functions
- **Props Types**: Define proper types for component props
- **Route Params**: Type route parameters using `params` prop types
- **Search Params**: Type search parameters using `searchParams` prop types

```typescript
// Typed route params
export default function UserPage({
  params,
}: {
  params: { id: string };
}) {
  return <div>User {params.id}</div>;
}
```

## Best Practices

1. **Performance**:
   - Use Server Components by default
   - Implement proper image optimization
   - Leverage Next.js caching strategies
   - Use dynamic imports for large client components

2. **Code Organization**:
   - Keep components in logical directories
   - Use colocation for related files
   - Create reusable components in shared directories

3. **Error Handling**:
   - Use `error.tsx` for error boundaries
   - Implement proper error states in components
   - Handle loading states with `loading.tsx`

4. **API Routes**:
   - Use `route.ts` files in `app/api/` directory
   - Export named functions (GET, POST, etc.) for HTTP methods
   - Return proper Response objects

```typescript
// app/api/users/route.ts
export async function GET() {
  return Response.json({ users: [] });
}

export async function POST(request: Request) {
  const body = await request.json();
  return Response.json({ created: body });
}
```

5. **Environment Variables**:
   - Use `.env.local` for local development
   - Prefix client-side variables with `NEXT_PUBLIC_`
   - Access server-side variables directly

## Common Patterns

- **Layouts**: Create nested layouts for shared UI across route segments
- **Templates**: Use `template.tsx` for UI that needs to remount on navigation
- **Parallel Routes**: Use `@folder` syntax for parallel routes
- **Intercepting Routes**: Use `(.)folder` syntax for intercepting routes

## Development Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
