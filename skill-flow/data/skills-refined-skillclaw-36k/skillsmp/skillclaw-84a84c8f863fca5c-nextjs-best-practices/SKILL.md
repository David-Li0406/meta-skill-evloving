---
name: nextjs-best-practices
description: Use this skill when developing applications with Next.js to follow best practices for server and client components, data fetching, routing, and performance optimization.
---

# Next.js Best Practices

> Principles for Next.js App Router development.

## 1. Server vs Client Components

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

## 2. Data Fetching Patterns

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

## 3. Routing Principles

### File Conventions

| File            | Purpose        |
| --------------- | -------------- |
| `page.tsx`      | Route UI       |
| `layout.tsx`    | Shared layout  |
| `loading.tsx`   | Loading state  |
| `error.tsx`     | Error boundary |
| `not-found.tsx` | 404 page       |

### Route Organization

| Pattern                 | Use                       |
| ----------------------- | ------------------------- |
| Route groups `(name)`   | Organize without URL      |
| Parallel routes `@slot` | Multiple same-level pages |
| Intercepting `(.)`      | Modal overlays            |

## 4. API Routes

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

## 5. Performance Principles

### Image Optimization

- Use next/image component
- Set priority for above-fold
- Provide blur placeholder
- Use responsive sizes

### Bundle Optimization

- Dynamic imports for heavy components
- Route-based code splitting (automatic)
- Analyze with bundle analyzer

## 6. Metadata

### Static vs Dynamic

| Type | Use |
|------|-----|
| Static export | Fixed metadata |
| generateMetadata | Dynamic per-route |

### Essential Tags

- title (50-60 chars)
- description (150-160 chars)
- Open Graph images
- Canonical URL

## 7. Caching Strategy

### Cache Layers

- Utilize caching strategies effectively to enhance performance and reduce load times.
- Implement caching at various levels (e.g., server-side, client-side) based on data requirements and user interactions.

## 8. Project Structure

- **App Directory**: Use the `app/` directory for all routes and layouts.
- **File-based Routing**: Routes are created using the file system in the `app/` directory.
- **Layouts**: Use `layout.tsx` files for shared UI across routes.
- **Pages**: Use `page.tsx` files to create route segments.
- **Server Components by Default**: All components are Server Components unless marked with `'use client'`.

## 9. Component Guidelines

### Server vs Client Components

- **Default to Server Components**: Most components should be Server Components for better performance.
- **Use Client Components** (`'use client'`) only when needed for:
  - Interactive features (onClick, onChange, etc.)
  - Browser APIs (localStorage, window, etc.)
  - React hooks (useState, useEffect, useContext, etc.)
  - Third-party libraries that require client-side JavaScript.

## 10. Dynamic Routes

- Use `[param]` folders for dynamic segments (e.g., `app/users/[id]/page.tsx`).
- Create nested layouts by adding `layout.tsx` in subdirectories.
- Use `loading.tsx` for route-level loading UI.
- Use `error.tsx` for route-level error handling.
- Use `not-found.tsx` for custom 404 pages.

## 11. Data Fetching

- Fetch data directly in Server Components using async/await.
- Avoid using useEffect for data fetching in Server Components.
- Create API routes in `app/api/` directory using `route.ts` files.
- Leverage Next.js caching with `fetch` options (`cache`, `revalidate`, etc.).