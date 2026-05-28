---
name: server-functions
description: Use createServerFn for RPC-style functions. Use when writing server functions with validators, middleware chains, or form action handlers.
---

# Server Functions

## Quick Start

```ts
import { createServerFn } from '@tanstack/react-start';
import { z } from 'zod';
import { db } from '@oakoss/database';

const getUsers = createServerFn({ method: 'GET' }).handler(async () => {
  return await db.query.users.findMany();
});

const createUser = createServerFn({ method: 'POST' })
  .inputValidator(z.object({ name: z.string().min(1), email: z.email() }))
  .handler(async ({ data }) => {
    const [user] = await db.insert(users).values(data).returning();
    return user;
  });
```

## Pattern Overview

| Pattern              | Use Case                 | Method            |
| -------------------- | ------------------------ | ----------------- |
| Data fetching        | Route loaders, queries   | GET               |
| Form submission      | Create/update operations | POST              |
| Authenticated action | Protected mutations      | POST + auth check |

## GET Functions

```ts
import { db, eq } from '@oakoss/database';
import { posts } from '@oakoss/database/schema';

const getAllPosts = createServerFn({ method: 'GET' }).handler(async () => {
  return await db.query.posts.findMany();
});

const getPost = createServerFn({ method: 'GET' })
  .inputValidator(z.object({ id: z.string() }))
  .handler(async ({ data }) => {
    return await db.query.posts.findFirst({
      where: eq(posts.id, data.id),
    });
  });

export const Route = createFileRoute('/posts/$id')({
  loader: async ({ params }) => await getPost({ data: { id: params.id } }),
});
```

## POST Functions

```ts
const createPost = createServerFn({ method: 'POST' })
  .inputValidator(
    z.object({
      title: z.string().min(1),
      content: z.string(),
    }),
  )
  .handler(async ({ data }) => {
    const [post] = await db.insert(posts).values(data).returning();
    return post;
  });

const handleSubmit = async (formData: FormData) => {
  const result = await createPost({
    data: { title: formData.get('title'), content: formData.get('content') },
  });
};
```

## Authenticated Functions

```ts
import { auth } from '@oakoss/auth/server';
import { db, eq } from '@oakoss/database';
import { posts } from '@oakoss/database/schema';

const deletePost = createServerFn({ method: 'POST' })
  .inputValidator(z.object({ id: z.string() }))
  .handler(async ({ data, request }) => {
    // Get session from request headers
    const session = await auth.api.getSession({ headers: request.headers });

    if (!session) {
      return { error: 'Authentication required', code: 'AUTH_REQUIRED' };
    }

    // Check ownership
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

## Error Handling

Standard error response format:

```ts
type ApiResult<T> = { data: T } | { error: string; code: string };

const updateUser = createServerFn({ method: 'POST' })
  .inputValidator(schema)
  .handler(async ({ data, request }): Promise<ApiResult<User>> => {
    try {
      const [user] = await db.update(users).set(data).returning();
      return { data: user };
    } catch (error) {
      console.error('updateUser failed:', error);
      return { error: 'Update failed', code: 'INTERNAL_ERROR' };
    }
  });
```

## Request Context

Access request details:

```ts
const serverFn = createServerFn({ method: 'POST' }).handler(
  async ({ request }) => {
    // Headers
    const authHeader = request.headers.get('Authorization');

    // URL info
    const url = new URL(request.url);

    // Cookies (via Better Auth)
    const session = await auth.api.getSession({ headers: request.headers });
  },
);
```

## Common Mistakes

| Mistake                             | Correct Pattern                                   |
| ----------------------------------- | ------------------------------------------------- |
| Missing auth check                  | Always verify session from request headers        |
| Throwing instead of returning error | Return `{ error, code }` format                   |
| Not validating input                | Always use `.inputValidator(schema)`              |
| Using deprecated Zod v3 syntax      | Use `z.email()` not `z.string().email()`          |
| Missing error code                  | Return `{ error: 'message', code: 'ERROR_CODE' }` |
| Not logging server errors           | Use `console.error()` before returning            |
| Returning raw DB errors             | Catch and return user-friendly messages           |
| Using GET for mutations             | Use POST for create/update/delete                 |

## Delegation

- **Complex queries**: For database patterns, see `database` skill
- **Auth patterns**: For authentication, see `auth` skill
- **API routes**: For REST endpoints, see `tanstack-start` skill
- **Code review**: After creating server functions, delegate to `code-reviewer` agent

## References

- Middleware patterns: [reference.md](reference.md)
- File uploads: [reference.md](reference.md)
- Streaming: [reference.md](reference.md)
