---
name: nextjs-best-practices
description: Use this skill for implementing best practices and guidelines for Next.js applications with App Router, focusing on Server Components, data fetching, routing patterns, and performance optimization.
---

# Next.js Best Practices

> Principles for Next.js App Router development.

## Core Principles

1. **Server-First Architecture**: Default to Server Components, using Client Components only when necessary for interactivity.
2. **File-Based Routing**: Utilize the `app/` directory for all routes and layouts, following file conventions.
3. **Data Fetching**: Fetch data where needed using async/await in Server Components, avoiding useEffect for data fetching.
4. **Type Safety**: Leverage TypeScript for route parameters, search parameters, and data types.
5. **Performance Optimization**: Optimize with streaming, parallel data fetching, and static generation.

## Project Structure

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── about/
│   └── page.tsx        # /about route
├── blog/
│   ├── page.tsx        # /blog route
│   └── [slug]/
│       └── page.tsx    # /blog/[slug] dynamic route
└── api/
    └── users/
        └── route.ts    # API route handler
```

## Server vs Client Components

### Decision Tree

```
Does it need...?
│
├── useState, useEffect, event handlers
│   └── Client Component ('use client')
│
├── Direct data fetching, no interactivity
│   └── Server Component (default)
│
└── Both?
    └── Split: Server parent + Client child
```

### By Default

| Type       | Use                                   |
| ---------- | ------------------------------------- |
| **Server** | Data fetching, layout, static content |
| **Client** | Forms, buttons, interactive UI        |

## Data Fetching Patterns

### Fetch Strategy

| Pattern        | Use                      |
| -------------- | ------------------------ |
| **Default**    | Static (cached at build) |
| **Revalidate** | ISR (time-based refresh) |
| **No-store**   | Dynamic (every request)  |

### Data Flow

| Source     | Pattern                      |
| ---------- | ---------------------------- |
| Database   | Server Component fetch       |
| API        | fetch with caching           |
| User input | Client state + server action |

## Routing Principles

### File Conventions

| File            | Purpose        |
| --------------- | -------------- |
| `page.tsx`      | Route UI       |
| `layout.tsx`    | Shared layout  |
| `loading.tsx`   | Loading state  |
| `error.tsx`     | Error boundary |
| `not-found.tsx` | 404 page       |

### Dynamic Routes

Use `[param]` folders for dynamic segments (e.g., `app/users/[id]/page.tsx`).

### Route Groups

Use `(folderName)` for organization without affecting the URL.

## API Routes

### Route Handlers

| Method    | Use         |
| --------- | ----------- |
| GET       | Read data   |
| POST      | Create data |
| PUT/PATCH | Update data |
| DELETE    | Remove data |

### Best Practices

- Validate input with Zod
- Return proper status codes
- Handle errors gracefully
- Use Edge runtime when possible

## Performance Principles

### Image Optimization

- Use `next/image` component for optimized images.
- Set priority for above-the-fold images.
- Provide blur placeholders and use responsive sizes.

### Bundle Optimization

- Use dynamic imports for heavy components.
- Implement route-based code splitting (automatic).
- Analyze with bundle analyzer.

## Metadata

### Static vs Dynamic

| Type             | Use               |
| ---------------- | ----------------- |
| Static export    | Fixed metadata    |
| generateMetadata | Dynamic per-route |

### Essential Tags

- title (50-60 chars)
- description (150-160 chars)
- Open Graph images
- Canonical URL

## Caching Strategy

### Cache Layers

| Layer      | Control         |
| ---------- | --------------- |
| Request    | fetch options   |
| Data       | revalidate/tags |
| Full route | route config    |

### Revalidation

| Method     | Use                  |
| ---------- | -------------------- |
| Time-based | `revalidate: 60`     |
| On-demand  | `revalidatePath/Tag` |
| No cache   | `no-store`           |

## Anti-Patterns

| ❌ Don't                   | ✅ Do             |
| -------------------------- | ----------------- |
| 'use client' everywhere    | Server by default |
| Fetch in client components | Fetch in server   |
| Skip loading states        | Use loading.tsx   |
| Ignore error boundaries    | Use error.tsx     |
| Large client bundles       | Dynamic imports   |

## Best Practices Checklist

- [ ] Use Server Components by default
- [ ] Add 'use client' only when necessary
- [ ] Implement loading.tsx for loading states
- [ ] Implement error.tsx for error handling
- [ ] Use generateMetadata for SEO
- [ ] Optimize images with next/image
- [ ] Use server actions for mutations
- [ ] Implement proper caching strategies
- [ ] Handle not-found cases
- [ ] Use TypeScript for type safety

> **Remember:** Server Components are the default for a reason. Start there, add client only when needed.