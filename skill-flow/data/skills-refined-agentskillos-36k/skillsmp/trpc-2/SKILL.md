---
name: trpc
description: "End-to-end typesafe API development with tRPC v11. Use when building TypeScript APIs with type inference between client and server, creating routers and procedures, setting up React/Next.js integrations, implementing middleware and context, handling errors, or configuring real-time subscriptions. Triggers on tRPC setup, router creation, procedure definition, input validation with Zod, mutation/query implementation, React Query integration, WebSocket/SSE subscriptions."
---

# tRPC Development Skill

Build end-to-end typesafe APIs with tRPC v11. This skill covers server setup, client integration, React Query, and real-time subscriptions.

## Quick Reference

### Core Concepts

- **Router**: Container for procedures, defines API structure
- **Procedure**: API endpoint (query, mutation, or subscription)
- **Context**: Shared data available to all procedures (auth, db, etc.)
- **Middleware**: Reusable logic that wraps procedures
- **Link**: Controls data flow on the client (batching, retries, etc.)

### Installation

```bash
# Server + Vanilla Client
npm install @trpc/server @trpc/client zod

# With React Query (recommended)
npm install @trpc/server @trpc/client @trpc/tanstack-react-query @tanstack/react-query zod

# With Next.js
npm install @trpc/server @trpc/client @trpc/tanstack-react-query @trpc/next @tanstack/react-query zod
```

## Server Setup

### 1. Initialize tRPC (server/trpc.ts)

```typescript
import { initTRPC, TRPCError } from '@trpc/server';
import superjson from 'superjson';

// Define context type
type Context = {
  db: PrismaClient;
  session: Session | null;
};

// Initialize tRPC - do this ONCE per backend
const t = initTRPC.context<Context>().create({
  transformer: superjson, // Preserves Date, Map, Set, etc.
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
export const middleware = t.middleware;
export const createCallerFactory = t.createCallerFactory;
```

### 2. Create Protected Procedure

```typescript
const isAuthed = middleware(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({
    ctx: { user: ctx.session.user }, // Add user to context
  });
});

export const protectedProcedure = publicProcedure.use(isAuthed);
```

### 3. Define Router (server/routers/user.ts)

```typescript
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';

export const userRouter = router({
  // Query - for fetching data
  list: publicProcedure.query(async ({ ctx }) => {
    return ctx.db.user.findMany();
  }),

  // Query with input
  byId: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const user = await ctx.db.user.findUnique({ where: { id: input.id } });
      if (!user) throw new TRPCError({ code: 'NOT_FOUND' });
      return user;
    }),

  // Mutation - for creating/updating/deleting
  create: protectedProcedure
    .input(z.object({
      name: z.string().min(1),
      email: z.string().email(),
    }))
    .mutation(async ({ ctx, input }) => {
      return ctx.db.user.create({ data: input });
    }),

  // Output validation (optional but recommended)
  getProfile: protectedProcedure
    .output(z.object({
      id: z.string(),
      name: z.string(),
      email: z.string(),
    }))
    .query(async ({ ctx }) => {
      return ctx.db.user.findUnique({ where: { id: ctx.user.id } });
    }),
});
```

### 4. Merge Routers (server/routers/_app.ts)

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

### 5. Create Context

```typescript
import { CreateNextContextOptions } from '@trpc/server/adapters/next';
import { getServerSession } from 'next-auth';

export const createContext = async (opts: CreateNextContextOptions) => {
  const session = await getServerSession(opts.req, opts.res, authOptions);
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
      headers: () => ({
        authorization: `Bearer ${getToken()}`,
      }),
    }),
  ],
});

// Usage
const users = await trpc.user.list.query();
const user = await trpc.user.byId.query({ id: '1' });
const newUser = await trpc.user.create.mutate({ name: 'John', email: 'john@example.com' });
```

### React Query Integration (Recommended)

See [references/react-integration.md](references/react-integration.md) for complete setup.

```typescript
// Quick example
const userQuery = useQuery(trpc.user.byId.queryOptions({ id: '1' }));
const createUser = useMutation(trpc.user.create.mutationOptions());
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

// Chain middleware
export const rateLimitedProcedure = protectedProcedure
  .use(loggerMiddleware)
  .use(rateLimitMiddleware);
```

## Error Handling

```typescript
import { TRPCError } from '@trpc/server';

// Throw errors in procedures
throw new TRPCError({
  code: 'NOT_FOUND',        // HTTP 404
  message: 'User not found',
  cause: originalError,     // Optional
});

// Error codes: PARSE_ERROR, BAD_REQUEST, UNAUTHORIZED, FORBIDDEN,
// NOT_FOUND, METHOD_NOT_SUPPORTED, TIMEOUT, CONFLICT, PRECONDITION_FAILED,
// PAYLOAD_TOO_LARGE, UNPROCESSABLE_CONTENT, TOO_MANY_REQUESTS,
// CLIENT_CLOSED_REQUEST, INTERNAL_SERVER_ERROR
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

// Usage: automatically validates organizationId and adds org to context
export const orgRouter = router({
  getMembers: orgProcedure
    .input(z.object({ role: z.enum(['admin', 'member']).optional() }))
    .query(({ ctx, input }) => {
      // input.organizationId and input.role both available
      // ctx.org is typed and available
    }),
});
```

### Optimistic Updates Pattern

```typescript
// Client-side with React Query
const utils = trpc.useUtils();

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