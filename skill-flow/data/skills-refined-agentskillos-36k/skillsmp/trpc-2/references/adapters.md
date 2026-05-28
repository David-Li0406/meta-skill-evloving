# tRPC Server Adapters

Deploy tRPC with any backend framework using adapters.

## Table of Contents

1. [Standalone (Node.js HTTP)](#standalone)
2. [Express](#express)
3. [Fastify](#fastify)
4. [Next.js](#nextjs)
5. [Fetch API (Edge/Cloudflare)](#fetch-api)
6. [AWS Lambda](#aws-lambda)
7. [Hono](#hono)
8. [Elysia (Bun)](#elysia)

---

## Standalone

Built-in Node.js HTTP server, no dependencies.

```typescript
import { createHTTPServer } from '@trpc/server/adapters/standalone';
import { appRouter } from './routers/_app';
import { createContext } from './context';
import cors from 'cors';

const server = createHTTPServer({
  router: appRouter,
  createContext,
  // Optional middleware
  middleware: cors(),
  // Error handling
  onError: ({ error, path }) => {
    console.error(`Error on ${path}:`, error);
  },
});

server.listen(3000);
console.log('Server running on http://localhost:3000');
```

### With WebSocket

```typescript
import { createHTTPServer } from '@trpc/server/adapters/standalone';
import { applyWSSHandler } from '@trpc/server/adapters/ws';
import { WebSocketServer } from 'ws';

const { server } = createHTTPServer({
  router: appRouter,
  createContext,
});

const wss = new WebSocketServer({ server });
applyWSSHandler({ wss, router: appRouter, createContext });

server.listen(3000);
```

---

## Express

```bash
npm install express @trpc/server
```

```typescript
import express from 'express';
import cors from 'cors';
import { createExpressMiddleware } from '@trpc/server/adapters/express';
import { appRouter } from './routers/_app';
import { createContext } from './context';

const app = express();

app.use(cors());
app.use(express.json());

// Mount tRPC
app.use(
  '/trpc',
  createExpressMiddleware({
    router: appRouter,
    createContext,
    onError: ({ error, path }) => {
      console.error(`tRPC error on ${path}:`, error);
    },
  })
);

// Other Express routes
app.get('/health', (req, res) => res.send('OK'));

app.listen(3000);
```

### Express Context

```typescript
import { CreateExpressContextOptions } from '@trpc/server/adapters/express';

export const createContext = async ({ req, res }: CreateExpressContextOptions) => {
  const token = req.headers.authorization?.split(' ')[1];
  const user = token ? await verifyToken(token) : null;

  return {
    req,
    res,
    user,
    db: prisma,
  };
};

export type Context = Awaited<ReturnType<typeof createContext>>;
```

---

## Fastify

```bash
npm install fastify @trpc/server @fastify/cors @fastify/websocket
```

```typescript
import fastify from 'fastify';
import cors from '@fastify/cors';
import ws from '@fastify/websocket';
import { fastifyTRPCPlugin } from '@trpc/server/adapters/fastify';
import { appRouter } from './routers/_app';
import { createContext } from './context';

const server = fastify({ logger: true });

// Register plugins
await server.register(cors, { origin: true });
await server.register(ws);

// Register tRPC
await server.register(fastifyTRPCPlugin, {
  prefix: '/trpc',
  trpcOptions: {
    router: appRouter,
    createContext,
    onError: ({ error, path }) => {
      server.log.error(`tRPC error on ${path}:`, error);
    },
  },
  useWSS: true, // Enable WebSocket subscriptions
});

await server.listen({ port: 3000, host: '0.0.0.0' });
```

### Fastify Context

```typescript
import { CreateFastifyContextOptions } from '@trpc/server/adapters/fastify';

export const createContext = async ({ req, res }: CreateFastifyContextOptions) => {
  return {
    req,
    res,
    user: req.user, // From Fastify auth plugin
    db: prisma,
  };
};
```

---

## Next.js

### Pages Router (pages/api/trpc/[trpc].ts)

```typescript
import { createNextApiHandler } from '@trpc/server/adapters/next';
import { appRouter } from '@/server/routers/_app';
import { createContext } from '@/server/context';

export default createNextApiHandler({
  router: appRouter,
  createContext,
  onError: ({ error, path }) => {
    if (error.code === 'INTERNAL_SERVER_ERROR') {
      console.error(`tRPC error on ${path}:`, error);
    }
  },
  responseMeta: ({ ctx, paths, type, errors }) => {
    // Cache successful GET requests
    const allOk = errors.length === 0;
    const isQuery = type === 'query';
    if (allOk && isQuery) {
      return {
        headers: {
          'cache-control': 'public, s-maxage=60, stale-while-revalidate=600',
        },
      };
    }
    return {};
  },
});

// Increase body size limit if needed
export const config = {
  api: {
    bodyParser: {
      sizeLimit: '4mb',
    },
  },
};
```

### App Router (app/api/trpc/[trpc]/route.ts)

```typescript
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter } from '@/server/routers/_app';
import { createContext } from '@/server/context';

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext: () => createContext(req),
    onError: ({ error, path }) => {
      console.error(`tRPC error on ${path}:`, error);
    },
  });

export { handler as GET, handler as POST };
```

### App Router Context

```typescript
import { headers, cookies } from 'next/headers';
import { auth } from '@/lib/auth';

export const createContext = async (req: Request) => {
  const session = await auth();
  
  return {
    session,
    headers: headers(),
    cookies: cookies(),
    db: prisma,
  };
};
```

---

## Fetch API

For Edge runtimes, Cloudflare Workers, Deno, Bun.

```typescript
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter } from './routers/_app';

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    return fetchRequestHandler({
      endpoint: '/trpc',
      req: request,
      router: appRouter,
      createContext: () => ({
        env, // Cloudflare bindings
        db: env.DB, // D1 database
      }),
    });
  },
};
```

### Cloudflare Workers

```typescript
// wrangler.toml
// name = "my-worker"
// main = "src/index.ts"

import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter } from './routers/_app';

export interface Env {
  DB: D1Database;
  KV: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // Handle CORS
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }

    return fetchRequestHandler({
      endpoint: '/trpc',
      req: request,
      router: appRouter,
      createContext: () => ({ env, ctx }),
      responseMeta: () => ({
        headers: {
          'Access-Control-Allow-Origin': '*',
        },
      }),
    });
  },
};
```

---

## AWS Lambda

```bash
npm install @trpc/server aws-lambda
```

```typescript
import { awsLambdaRequestHandler } from '@trpc/server/adapters/aws-lambda';
import { appRouter } from './routers/_app';
import { createContext } from './context';

export const handler = awsLambdaRequestHandler({
  router: appRouter,
  createContext,
  responseMeta: () => ({
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    },
  }),
});
```

### Lambda Context

```typescript
import { CreateAWSLambdaContextOptions } from '@trpc/server/adapters/aws-lambda';
import { APIGatewayProxyEventV2 } from 'aws-lambda';

export const createContext = async ({
  event,
  context,
}: CreateAWSLambdaContextOptions<APIGatewayProxyEventV2>) => {
  const token = event.headers.authorization?.split(' ')[1];
  
  return {
    event,
    lambdaContext: context,
    user: token ? await verifyToken(token) : null,
  };
};
```

---

## Hono

```bash
npm install hono @trpc/server
```

```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { trpcServer } from '@hono/trpc-server';
import { appRouter } from './routers/_app';
import { createContext } from './context';

const app = new Hono();

app.use('*', cors());

app.use(
  '/trpc/*',
  trpcServer({
    router: appRouter,
    createContext,
  })
);

app.get('/health', (c) => c.text('OK'));

export default app;
```

### Hono with Cloudflare

```typescript
import { Hono } from 'hono';
import { trpcServer } from '@hono/trpc-server';
import { appRouter } from './routers/_app';

type Bindings = {
  DB: D1Database;
};

const app = new Hono<{ Bindings: Bindings }>();

app.use(
  '/trpc/*',
  trpcServer({
    router: appRouter,
    createContext: (opts, c) => ({
      db: c.env.DB,
    }),
  })
);

export default app;
```

---

## Elysia

For Bun runtime.

```bash
bun add elysia @elysiajs/trpc @trpc/server
```

```typescript
import { Elysia } from 'elysia';
import { trpc } from '@elysiajs/trpc';
import { appRouter } from './routers/_app';
import { createContext } from './context';

const app = new Elysia()
  .use(
    trpc(appRouter, {
      createContext,
    })
  )
  .get('/health', () => 'OK')
  .listen(3000);

console.log(`Running at ${app.server?.hostname}:${app.server?.port}`);
```

---

## Common Context Pattern

Reusable context that works across adapters:

```typescript
// server/context.ts
import { prisma } from './db';
import { verifyToken } from './auth';

// Inner context (no request-specific data)
export const createInnerContext = async (opts: { user: User | null }) => {
  return {
    user: opts.user,
    db: prisma,
  };
};

// Outer context factory for different adapters
export const createContextFactory = <TRequest>(
  getToken: (req: TRequest) => string | null
) => {
  return async (req: TRequest) => {
    const token = getToken(req);
    const user = token ? await verifyToken(token) : null;
    return createInnerContext({ user });
  };
};

// Usage in Express
export const createExpressContext = createContextFactory<Express.Request>(
  (req) => req.headers.authorization?.split(' ')[1] ?? null
);

// Usage in Next.js
export const createNextContext = createContextFactory<Request>(
  (req) => req.headers.get('authorization')?.split(' ')[1] ?? null
);
```