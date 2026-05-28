---
name: nextjs-app-router-development
description: Use this skill to build, review, and refactor Next.js applications with App Router, focusing on Server and Client Components, data fetching, routing, and TypeScript.
---

# Next.js App Router Development

This guide provides a comprehensive overview for building Next.js applications using the App Router architecture, including Server and Client Components, data fetching, routing, and navigation.

## When to Use

- Creating new pages or layouts in Next.js App Router
- Implementing Server and Client Component patterns
- Setting up data fetching with Server Components
- Building API route handlers
- Implementing navigation and routing
- Debugging Next.js-specific issues
- Working with dynamic routes and params
- Migrating from Pages Router to App Router
- Optimizing data fetching and caching
- Building full-stack features with Server Actions

## Core Concepts

### Server vs Client Components

In Next.js App Router, components are **Server Components by default**.

**Server Components:**
- Render on the server only
- Can be async for data fetching
- Cannot use React hooks (useState, useEffect, etc.)
- Better performance (smaller bundle size)

**Client Components:**
- Require `"use client"` directive at the top of the file
- Render on both server and client
- Can use React hooks and browser APIs
- Required for interactivity

### Data Fetching Patterns

- **Server Component Data Fetching**: Use async functions to fetch data directly in Server Components.
- **Client Component Data Fetching**: Use libraries like SWR or TanStack Query for client-side data fetching.

### File-Based Routing

Next.js uses a file-based routing system. The structure typically looks like this:

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── dashboard/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx        # /dashboard
│   └── [id]/page.tsx   # /dashboard/[id]
├── api/
│   └── users/
│       └── route.ts    # API route handler
```

### Dynamic Routes

Dynamic routes can be created using square brackets, e.g., `[slug]`. You can also create catch-all routes using `[...slug]`.

### Server Actions

Server Actions allow you to handle form submissions and data mutations directly in your components. Use them for better performance and to avoid unnecessary client-side state management.

## Workflows

### Workflow 1: Create New Page with Data Fetching

1. **Create Page File**: Define a new page in the `app` directory.
2. **Fetch Data**: Use async functions to fetch data on the server.
3. **Render UI**: Return the fetched data in your component's JSX.

### Workflow 2: Create API Route Handler

1. **Define Route**: Create a new file in the `api` directory.
2. **Handle Requests**: Use `NextRequest` and `NextResponse` to manage incoming requests and send responses.

### Workflow 3: Implement Protected Route

1. **Create Middleware**: Use middleware to protect routes based on authentication.
2. **Access User Data**: Use server components to access user data and render protected content.

### Workflow 4: Implement Navigation

1. **Use Link Component**: For client-side navigation, use the `Link` component from Next.js.
2. **Programmatic Navigation**: Use `useRouter` for programmatic navigation in Client Components.

## Best Practices

1. **Default to Server Components**: Use Server Components for data fetching and rendering.
2. **Colocate Data Fetching**: Fetch data where it is used, preferably in Server Components.
3. **Use Next.js Link**: For client-side navigation, always use the `Link` component.
4. **Implement Loading States**: Use `loading.tsx` for better user experience during data fetching.
5. **Handle Errors Gracefully**: Use `error.tsx` for error boundaries.

## Troubleshooting

### Common Issues

- **Cannot Use useState/useEffect in Component**: Ensure the component is a Client Component.
- **Navigation Hooks Not Found**: Ensure you are importing from `"next/navigation"` and using Client Components.
- **Params is Promise Error**: In Next.js 15+, ensure to await params in dynamic routes.

## Validation Checklist

Before considering your Next.js implementation complete:

- [ ] Use Server Components by default.
- [ ] Ensure Client Components have the `"use client"` directive.
- [ ] Implement proper error handling and loading states.
- [ ] Validate data on the server and use server actions where appropriate.

## References

- **Official Next.js Documentation**: [Next.js Docs](https://nextjs.org/docs)
- **React Documentation**: [React Docs](https://react.dev/)
- **TypeScript Handbook**: [TypeScript Docs](https://www.typescriptlang.org/docs/)