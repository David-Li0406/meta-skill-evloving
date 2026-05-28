---
name: nextjs-app-development
description: Use this skill when building, reviewing, or refactoring Next.js applications with App Router and TypeScript, focusing on components, data fetching, routing, and production readiness.
---

# Next.js App Development

This guide provides a comprehensive approach to building Next.js applications using the App Router architecture, emphasizing best practices for Server and Client Components, data fetching, routing, and overall project structure.

## When to Use

- Creating new pages or layouts in Next.js App Router
- Implementing Server and Client Component patterns
- Setting up data fetching with Server Components
- Building API route handlers
- Implementing navigation and routing
- Debugging Next.js-specific issues
- Working with dynamic routes and parameters
- Reviewing and refactoring existing Next.js projects

## Defaults

- **Framework**: Next.js App Router (`app/`)
- **Language**: TypeScript
- **Component Types**: Server Components by default; add `"use client"` only when necessary
- **Styling**: Tailwind CSS if present; otherwise, follow existing styling conventions

## Domain Knowledge

### Critical Patterns

#### Server vs Client Components

- **Server Components**: Render on the server, can be async for data fetching, cannot use React hooks or browser APIs.
- **Client Components**: Require `"use client"` directive, can use React hooks and browser APIs, necessary for interactivity.

#### Data Fetching

- Prefer colocated server fetchers in `lib/` and call them from Server Components.
- Use `fetch()` with Next.js caching semantics when appropriate.
- Handle loading and errors with `loading.tsx` and `error.tsx` per route segment.

### Navigation

- Use Next.js Link for client-side navigation.
- Programmatic navigation can be achieved using `useRouter` in Client Components.

### Dynamic Routes

- In Next.js 15+, dynamic route parameters and search parameters must be awaited.

## Workflows

### Workflow 1: Create New Page with Data Fetching

1. **Create Page File**: Define a new page in the `app/` directory.
2. **Create Client Component for Interactivity**: Use Client Components for UI interactions.
3. **Add Loading State**: Implement a loading state with `loading.tsx`.
4. **Add Error Handling**: Implement error handling with `error.tsx`.

### Workflow 2: Create Dynamic Route

1. **Create Dynamic Route File**: Define a dynamic route in the `app/` directory.
2. **Generate Static Params (Optional)**: Provide all possible params for static site generation.
3. **Add Metadata**: Configure metadata for SEO.

### Workflow 3: Create API Route Handler

1. **Create Route File**: Define API routes in the `app/api/` directory.
2. **Use Route from Frontend**: Call the API from Client Components.

### Workflow 4: Implement Protected Route

1. **Create Middleware**: Use middleware for authentication.
2. **Access User in Server Component**: Fetch user data in Server Components.
3. **Access User in Client Component**: Use hooks to access user data in Client Components.

### Workflow 5: Implement Navigation

1. **Use Link Component for Navigation**: Implement navigation using Next.js Link.
2. **Programmatic Navigation in Client Component**: Use `useRouter` for navigation after actions.
3. **Access Current Route Information**: Use `usePathname` and `useSearchParams` for route info.

## Troubleshooting

### Common Issues

- **Cannot Use useState/useEffect in Component**: Ensure the component is a Client Component.
- **Navigation Hooks Not Found**: Import from `"next/navigation"` and ensure the component is a Client Component.
- **Params is Promise Error**: Await params in Next.js 15+.
- **Hydration Mismatch**: Ensure consistent rendering between server and client.

## Validation Checklist

Before considering the Next.js implementation complete:

- [ ] Use Server Components by default.
- [ ] Ensure Client Components have the `"use client"` directive where needed.
- [ ] Validate data fetching uses async Server Components.
- [ ] Ensure navigation hooks are only used in Client Components.
- [ ] Await params and searchParams in Next.js 15+.
- [ ] Use Next.js Link for client-side navigation.
- [ ] Implement proper error handling in API routes.
- [ ] Protect routes with middleware.
- [ ] Implement loading and error states.

## Best Practices

1. **Default to Server Components**: Use Client Components only when necessary.
2. **Colocate Server and Client**: Mix Server and Client Components in the same tree.
3. **Fetch on the server**: Use async Server Components instead of `useEffect`.
4. **Implement loading states**: Create `loading.tsx` for better perceived performance.
5. **Handle errors properly**: Use `error.tsx` for graceful error handling.
6. **Protect routes with middleware**: Don't rely on client-side checks alone.
7. **Type everything**: Use TypeScript for better developer experience and fewer bugs.

## References

- **Official docs**: [Next.js Documentation](https://nextjs.org/docs)