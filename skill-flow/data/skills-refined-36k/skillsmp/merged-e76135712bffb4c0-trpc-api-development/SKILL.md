---
name: trpc-api-development
description: Use this skill when building end-to-end typesafe APIs with tRPC, including setup, router creation, procedure definition, and integration with React and Next.js.
---

# tRPC API Development

Build end-to-end typesafe APIs with tRPC. This skill covers server setup, client integration, React Query, and real-time subscriptions.

## Quick Reference

### Core Concepts

- **Router**: Container for procedures, defines API structure.
- **Procedure**: API endpoint (query, mutation, or subscription).
- **Context**: Shared data available to all procedures (auth, db, etc.).
- **Middleware**: Reusable logic that wraps procedures.
- **Link**: Controls data flow on the client (batching, retries, etc.).

## Installation

```bash
# Core packages
npm install @trpc/server @trpc/client @trpc/tanstack-react-query @tanstack/react-query zod

# For Next.js
npm install @trpc/next
```

## Server Setup

### 1. Initialize tRPC

```typescript
import { initTRPC, TRPCError } from '@trpc/server';
import superjson from 'superjson';

// Define context type
type Context = {
  db: PrismaClient;
  session: Session | null;
};

// Initialize tRPC
const t = initTRPC.context<Context>().create({
  transformer: superjson,
  errorFormatter: ({ shape, error }) => ({
    ...shape,
    data: {
      ...shape.data,
      zodError: error.cause instanceof ZodError ? error.cause.flatten() : null,
    },
  }),
});

// Export reusable helpers
export const router = t.router;
export const publicProcedure = t.procedure;
export const protectedProcedure = publicProcedure.use(middleware(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next();
}));
```

### 2. Create Routers and Procedures

```typescript
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';

export const userRouter = router({
  list: publicProcedure.query(async ({ ctx }) => {
    return ctx.db.user.findMany();
  }),
  byId: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const user = await ctx.db.user.findUnique({ where: { id: input.id } });
      if (!user) throw new TRPCError({ code: 'NOT_FOUND' });
      return user;
    }),
  create: protectedProcedure
    .input(z.object({
      name: z.string().min(1),
      email: z.string().email(),
    }))
    .mutation(async ({ ctx, input }) => {
      return ctx.db.user.create({ data: input });
    }),
});
```

### 3. Merge Routers

```typescript
import { router } from '../trpc';
import { userRouter } from './user';
import { postRouter } from './post';

export const appRouter = router({
  user: userRouter,
  post: postRouter,
});

export type AppRouter = typeof appRouter;
```

### 4. Create Context

```typescript
import { CreateNextContextOptions } from '@trpc/server/adapters/next';
import { getServerSession } from 'next-auth';

export const createContext = async (opts: CreateNextContextOptions) => {
  const session = await getServerSession(opts.req, opts.res);
  return {
    db: prisma,
    session,
  };
};

export type Context = Awaited<ReturnType<typeof createContext>>;
```

## Client Setup

### Vanilla Client

```typescript
import { createTRPCClient, httpBatchLink } from '@trpc/client';
import type { AppRouter } from './server/routers/_app';
import superjson from 'superjson';

const trpc = createTRPCClient<AppRouter>({
  links: [
    httpBatchLink({
      url: 'http://localhost:3000/api/trpc',
      transformer: superjson,
    }),
  ],
});

// Usage
const users = await trpc.user.list.query();
const user = await trpc.user.byId.query({ id: '1' });
const newUser = await trpc.user.create.mutate({ name: 'John', email: 'john@example.com' });
```

### React Query Integration

```typescript
import { trpc } from '@/utils/trpc';

const userQuery = trpc.user.byId.useQuery({ id: '1' });
const createUser = trpc.user.create.useMutation();
```

## Middleware Patterns

```typescript
// Logging middleware
const loggerMiddleware = middleware(async ({ path, type, next }) => {
  const start = Date.now();
  const result = await next();
  console.log(`${type} ${path} - ${Date.now() - start}ms`);
  return result;
});

// Rate limiting middleware
const rateLimitMiddleware = middleware(async ({ ctx, next }) => {
  const { success } = await ratelimit.limit(ctx.user.id);
  if (!success) throw new TRPCError({ code: 'TOO_MANY_REQUESTS' });
  return next();
});
```

## Error Handling

```typescript
import { TRPCError } from '@trpc/server';

// Throw errors in procedures
throw new TRPCError({
  code: 'NOT_FOUND',
  message: 'User not found',
});
```

## Additional Resources

- **React/Next.js Integration**: See [references/react-integration.md](references/react-integration.md)
- **Subscriptions (WebSocket/SSE)**: See [references/subscriptions.md](references/subscriptions.md)
- **Server Adapters**: See [references/adapters.md](references/adapters.md)

## Common Patterns

### Input Chaining

```typescript
const baseInput = z.object({ organizationId: z.string() });

const orgProcedure = protectedProcedure
  .input(baseInput)
  .use(async ({ ctx, input, next }) => {
    const org = await ctx.db.org.findUnique({ where: { id: input.organizationId } });
    if (!org) throw new TRPCError({ code: 'NOT_FOUND' });
    return next({ ctx: { org } });
  });
```

### Optimistic Updates Pattern

```typescript
const createPost = useMutation(
  trpc.post.create.mutationOptions({
    onMutate: async (newPost) => {
      await utils.post.list.cancel();
      const previous = utils.post.list.getData();
      utils.post.list.setData(undefined, (old) => [...(old ?? []), { ...newPost, id: 'temp' }]);
      return { previous };
    },
    onError: (err, newPost, context) => {
      utils.post.list.setData(undefined, context?.previous);
    },
    onSettled: () => {
      utils.post.list.invalidate();
    },
  })
);
```