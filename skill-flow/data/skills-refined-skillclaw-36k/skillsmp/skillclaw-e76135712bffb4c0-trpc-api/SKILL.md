---
name: trpc-api
description: Use this skill when building end-to-end typesafe APIs with tRPC, covering setup, routers, procedures, middleware, and real-time subscriptions in TypeScript applications.
---

# tRPC API Development

Build end-to-end typesafe APIs with tRPC, providing full type inference from backend to frontend without schemas or code generation.

## Installation

```bash
# Core packages
npm install @trpc/server @trpc/client @trpc/react-query @tanstack/react-query zod

# For Next.js
npm install @trpc/next

# For subscriptions
npm install @trpc/server ws
```

## Project Structure

```
src/
├── server/
│   ├── trpc.ts           # tRPC initialization
│   ├── context.ts        # Request context
│   ├── routers/
│   │   ├── _app.ts       # Root router
│   │   ├── user.ts       # User procedures
│   │   └── post.ts       # Post procedures
│   └── middleware/
│       └── auth.ts       # Auth middleware
├── utils/
│   └── trpc.ts           # Client configuration
└── app/
    └── api/trpc/[trpc]/route.ts  # Next.js handler
```

## Server Setup

### Initialize tRPC

```typescript
// src/server/trpc.ts
import { initTRPC, TRPCError } from "@trpc/server";
import superjson from "superjson";
import { ZodError } from "zod";
import type { Context } from "./context";

const t = initTRPC.context<Context>().create({
  transformer: superjson,
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    };
  },
});

export const router = t.router;
export const publicProcedure = t.procedure;
export const middleware = t.middleware;
export const mergeRouters = t.mergeRouters;
```

### Context Creation

```typescript
// src/server/context.ts
import { type inferAsyncReturnType } from "@trpc/server";
import { type CreateNextContextOptions } from "@trpc/server/adapters/next";
import { getServerSession } from "next-auth";
import { prisma } from "@/lib/prisma";

export async function createContext(opts: CreateNextContextOptions) {
  const session = await getServerSession(opts.req, opts.res);

  return {
    session,
    prisma,
    req: opts.req,
    res: opts.res,
  };
}

export type Context = inferAsyncReturnType<typeof createContext>;
```

## Routers and Procedures

### Basic Router

```typescript
// src/server/routers/user.ts
import { z } from "zod";
import { router, publicProcedure, protectedProcedure } from "../trpc";

// Example of a protected procedure
const isAuthed = middleware(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({
    ctx: { user: ctx.session.user }, // Add user to context
  });
});

export const userRouter = router({
  getUser: publicProcedure.query(() => {
    // Implementation here
  }),
  createUser: protectedProcedure.mutation(({ input }) => {
    // Implementation here
  }),
});
```

## Real-time Subscriptions

tRPC supports real-time subscriptions using WebSockets. Ensure to set up the necessary server and client configurations to handle real-time data flow.

## Conclusion

This skill provides a comprehensive guide to building type-safe APIs with tRPC, ensuring a seamless integration between your TypeScript backend and frontend applications.