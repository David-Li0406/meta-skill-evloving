---
name: tanstack-start
description: TanStack Start SSR framework. Use for server functions, API routes, SSR modes, middleware chains, server-only code
---

# TanStack Start

## Server Functions

```tsx
import { createServerFn } from '@tanstack/react-start';
import { z } from 'zod';

// GET - No input validation needed
const getUsers = createServerFn({ method: 'GET' }).handler(async () => {
  return await db.query.users.findMany();
});

// POST - Always validate with Zod
const createUser = createServerFn({ method: 'POST' })
  .inputValidator(z.object({ name: z.string().min(1), email: z.email() }))
  .handler(async ({ data }) => {
    return await db.insert(users).values(data).returning();
  });
```

## Authenticated Server Functions

```tsx
import { auth } from '@oakoss/auth/server';

const deletePost = createServerFn({ method: 'POST' })
  .inputValidator(z.object({ id: z.string() }))
  .handler(async ({ data, request }) => {
    const session = await auth.api.getSession({ headers: request.headers });

    if (!session) {
      return { error: 'Authentication required', code: 'AUTH_REQUIRED' };
    }

    const post = await db.query.posts.findFirst({
      where: eq(posts.id, data.id),
    });

    if (post?.authorId !== session.user.id) {
      return { error: 'Not authorized', code: 'FORBIDDEN' };
    }

    await db.delete(posts).where(eq(posts.id, data.id));
    return { success: true };
  });
```

## API Routes (Server Routes)

```tsx
// routes/api/posts.ts
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/api/posts')({
  server: {
    handlers: {
      GET: async () => {
        const posts = await db.query.posts.findMany();
        return Response.json(posts);
      },

      POST: async ({ request }) => {
        const body = await request.json();
        const result = schema.safeParse(body);

        if (!result.success) {
          return Response.json(
            { error: 'Validation failed', code: 'VALIDATION_ERROR' },
            { status: 400 },
          );
        }

        const [post] = await db.insert(posts).values(result.data).returning();
        return Response.json(post, { status: 201 });
      },
    },
  },
});
```

## Middleware Chain

```tsx
import { createServerFn, createMiddleware } from '@tanstack/react-start';

const authMiddleware = createMiddleware().server(async ({ next, request }) => {
  const session = await auth.api.getSession({ headers: request.headers });

  if (!session) {
    throw new Error('Unauthorized');
  }

  return next({ context: { user: session.user } });
});

const getProtectedData = createServerFn({ method: 'GET' })
  .middleware([authMiddleware])
  .handler(async ({ context }) => {
    return await fetchUserData(context.user.id);
  });
```

## Environment Functions

```tsx
import {
  createIsomorphicFn,
  createServerOnlyFn,
  createClientOnlyFn,
} from '@tanstack/react-start';

// Runs different code on client vs server
const getStorageValue = createIsomorphicFn()
  .server(() => process.env.FEATURE_FLAG)
  .client(() => localStorage.getItem('featureFlag'));

// Server-only (throws on client)
const readSecretConfig = createServerOnlyFn(() => {
  return process.env.SECRET_API_KEY;
});

// Client-only (throws on server)
const getGeolocation = createClientOnlyFn(() => {
  return navigator.geolocation.getCurrentPosition();
});
```

## Error Handling Pattern

```tsx
type ApiResult<T> = { data: T } | { error: string; code: string };

const updateUser = createServerFn({ method: 'POST' })
  .inputValidator(schema)
  .handler(async ({ data }): Promise<ApiResult<User>> => {
    try {
      const [user] = await db.update(users).set(data).returning();
      return { data: user };
    } catch (error) {
      console.error('updateUser failed:', error);
      return { error: 'Update failed', code: 'INTERNAL_ERROR' };
    }
  });
```

## Standard Error Codes

| Code               | Status | Description                |
| ------------------ | ------ | -------------------------- |
| `AUTH_REQUIRED`    | 401    | User must be authenticated |
| `FORBIDDEN`        | 403    | User lacks permission      |
| `NOT_FOUND`        | 404    | Resource doesn't exist     |
| `VALIDATION_ERROR` | 400    | Invalid input data         |
| `CONFLICT`         | 409    | Resource already exists    |
| `INTERNAL_ERROR`   | 500    | Server error               |

## Common Mistakes

| Mistake                                | Correct Pattern                            |
| -------------------------------------- | ------------------------------------------ |
| Missing auth check                     | Always verify session from request headers |
| Throwing instead of returning error    | Return `{ error, code }` format            |
| Not validating input                   | Always use `.inputValidator(schema)`       |
| Not validating input                   | Always use `.inputValidator(schema)`       |
| Using GET for mutations                | Use POST for create/update/delete          |
| Not logging server errors              | Use `console.error()` before returning     |
| Exposing raw DB errors                 | Catch and return user-friendly messages    |
| Missing error code                     | Always include both `error` and `code`     |
| Returning sensitive data in errors     | Only return what the client needs          |
| Not handling validation errors in POST | Check `result.success` and return 400      |

## Delegation

- **Auth patterns**: For authentication, see [auth](../auth/SKILL.md) skill
- **Database queries**: For Drizzle patterns, see [database](../database/SKILL.md) skill
- **Route integration**: For loader patterns, see [tanstack-router](../tanstack-router/SKILL.md) skill
- **Code review**: After implementing server functions, delegate to `code-reviewer` agent

## Topic References

- [Server Functions](server-functions.md) - Middleware, environment functions, error handling
- [API Routes](api-routes.md) - RESTful routes, webhooks, file uploads
