# Server Functions Reference

## API Overview

```ts
import { createServerFn } from '@tanstack/react-start';

const fn = createServerFn(options)
  .inputValidator(schema) // Optional: Zod schema for input
  .middleware(mw) // Optional: Middleware chain
  .handler(handler); // Required: Function logic
```

## Options

| Option   | Type              | Default  | Description |
| -------- | ----------------- | -------- | ----------- |
| `method` | `'GET' \| 'POST'` | Required | HTTP method |

## Handler Context

```ts
.handler(async (context) => {
  context.data;      // Validated input (if validator used)
  context.request;   // Fetch Request object
})
```

## Middleware

Chain middleware for shared logic:

```ts
import { createMiddleware } from '@tanstack/react-start';
import { auth } from '@oakoss/auth/server';

const logMiddleware = createMiddleware().server(async ({ next }) => {
  console.log('Request started');
  const result = await next();
  console.log('Request completed');
  return result;
});

const authMiddleware = createMiddleware().server(async ({ next, request }) => {
  const session = await auth.api.getSession({ headers: request.headers });
  if (!session) {
    throw new Error('AUTH_REQUIRED');
  }
  return next({ context: { session } });
});

const protectedFn = createServerFn({ method: 'POST' })
  .middleware([logMiddleware, authMiddleware])
  .handler(async ({ context }) => {
    // context.session is available from authMiddleware
    return { user: context.session.user };
  });
```

## File Uploads

Handle multipart form data:

```ts
const uploadFile = createServerFn({ method: 'POST' }).handler(
  async ({ request }) => {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return { error: 'No file provided', code: 'VALIDATION_ERROR' };
    }

    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      return { error: 'Invalid file type', code: 'VALIDATION_ERROR' };
    }

    // 5MB max
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      return { error: 'File too large', code: 'VALIDATION_ERROR' };
    }

    const buffer = await file.arrayBuffer();

    return { success: true, filename: file.name };
  },
);
```

## Streaming Responses

Return streaming data:

```ts
const streamData = createServerFn({ method: 'GET' }).handler(async () => {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 10; i++) {
        controller.enqueue(encoder.encode(`data: ${i}\n\n`));
        await new Promise((r) => setTimeout(r, 100));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: { 'Content-Type': 'text/event-stream' },
  });
});
```

## Validation Patterns

### Schema Composition

```ts
const baseUserSchema = z.object({
  name: z.string().min(1),
  email: z.email(),
});

const createUserSchema = baseUserSchema.extend({
  password: z.string().min(8),
});

const updateUserSchema = baseUserSchema.partial();
```

### Async Validation

```ts
import { db, eq } from '@oakoss/database';
import { users } from '@oakoss/database/schema';

const registerUser = createServerFn({ method: 'POST' })
  .inputValidator(createUserSchema)
  .handler(async ({ data }) => {
    // Check if email exists (async validation)
    const existing = await db.query.users.findFirst({
      where: eq(users.email, data.email),
    });

    if (existing) {
      return { error: 'Email already registered', code: 'CONFLICT' };
    }

    // Proceed with registration
    const [user] = await db.insert(users).values(data).returning();
    return { data: user };
  });
```

## Error Handling Patterns

### Error Types

```ts
// Custom error class
class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public status: number = 400,
  ) {
    super(message);
  }
}

// Usage
const handler = async ({ data }) => {
  try {
    // ... operation
  } catch (error) {
    if (error instanceof ApiError) {
      return { error: error.message, code: error.code };
    }
    console.error('Unexpected error:', error);
    return { error: 'Something went wrong', code: 'INTERNAL_ERROR' };
  }
};
```

### Centralized Error Handler

```ts
function handleServerError(error: unknown): ApiError {
  if (error instanceof ApiError) return error;

  // Database errors
  if (error instanceof PostgresError) {
    if (error.code === '23505') {
      // Unique violation
      return { error: 'Resource already exists', code: 'CONFLICT' };
    }
  }

  // Default
  console.error('Unhandled error:', error);
  return { error: 'Internal server error', code: 'INTERNAL_ERROR' };
}
```

## Calling Server Functions

### From Components

```tsx
function CreatePostForm() {
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);

    const result = await createPost({
      data: {
        title: formData.get('title') as string,
        content: formData.get('content') as string,
      },
    });

    if ('error' in result) {
      toast.error(result.error);
    } else {
      toast.success('Post created');
    }
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

### From Route Loaders

```ts
export const Route = createFileRoute('/posts')({
  loader: async () => {
    const posts = await getPosts();
    return { posts };
  },
});

function RouteComponent() {
  const { posts } = Route.useLoaderData();
}
```

### With TanStack Query

```tsx
import { queryOptions, useSuspenseQuery } from '@tanstack/react-query';

const postsQuery = queryOptions({
  queryKey: ['posts'],
  queryFn: () => getPosts(),
});

function PostList() {
  const { data: posts } = useSuspenseQuery(postsQuery);
}
```

## Security Considerations

1. **Always validate input** with Zod schemas
2. **Check authentication** before protected operations
3. **Check authorization** (ownership, permissions)
4. **Never expose** stack traces or internal errors
5. **Rate limit** sensitive endpoints
6. **Sanitize** user-provided content
