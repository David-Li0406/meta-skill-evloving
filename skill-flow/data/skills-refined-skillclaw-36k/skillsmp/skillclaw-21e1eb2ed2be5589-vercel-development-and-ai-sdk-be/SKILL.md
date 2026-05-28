---
name: vercel-development-and-ai-sdk-best-practices
description: Use this skill when developing applications on Vercel with Next.js, focusing on best practices for performance optimization, server components, and AI SDK integration.
---

# Vercel Development and AI SDK Best Practices

## Overview

This skill provides comprehensive guidelines for developing and deploying applications on Vercel, emphasizing Next.js, React Server Components, Edge Functions, and the Vercel AI SDK. It includes best practices for performance optimization and effective use of AI capabilities.

## Core Principles

- Write concise, technical TypeScript code with accurate examples.
- Use functional and declarative programming patterns; avoid classes.
- Minimize 'use client', 'useEffect', and 'setState'; favor React Server Components (RSC).
- Implement responsive design with Tailwind CSS using a mobile-first approach.
- Optimize for Core Web Vitals and performance.

## Project Structure

```
my-app/
├── app/                    # App Router pages and layouts
│   ├── (auth)/            # Route groups
│   ├── api/               # API routes
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # UI primitives
│   └── features/         # Feature components
├── lib/                   # Utility functions
├── hooks/                 # Custom React hooks
├── types/                 # TypeScript types
├── public/               # Static assets
└── vercel.json           # Vercel configuration
```

## Next.js App Router Guidelines

### File Naming Conventions
- Use lowercase with dashes for directories (e.g., `components/auth-wizard`).
- Prefer named exports for components and functions.
- Use `page.tsx` for route pages, `layout.tsx` for layouts.
- Use `loading.tsx` for loading states, `error.tsx` for error boundaries.

### Server Components (Default)
```typescript
// app/users/page.tsx
import { getUsers } from '@/lib/data';

export default async function UsersPage() {
  const users = await getUsers();

  return (
    <main>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </main>
  );
}
```

### Client Components (When Needed)
```typescript
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

## Vercel AI SDK Best Practices

### Guidelines for AI SDK Usage
- Use `streamText` for streaming text responses from AI models.
- Use `streamObject` for streaming structured JSON responses.
- Implement proper error handling with `onFinish` callback.
- Use `onChunk` for real-time UI updates during streaming.
- Prefer server-side streaming for better performance and security.
- Use `smoothStream` for smoother streaming experiences.
- Implement proper loading states for AI responses.
- Use `useChat` for client-side chat interfaces when needed.
- Use `useCompletion` for client-side text completion interfaces.
- Handle rate limiting and quota management appropriately.
- Implement proper authentication and authorization for AI endpoints.
- Use environment variables for API keys and sensitive configuration.
- Cache AI responses when appropriate to reduce costs.
- Implement proper logging for debugging and monitoring.

## TypeScript Standards

### Type Definitions
```typescript
// Use interfaces over types for object shapes
interface User {
  id: number;
  name: string;
}
```