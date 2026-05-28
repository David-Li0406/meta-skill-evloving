# API Routes Reference

## Server Route Handlers

Use `createFileRoute` with a `server.handlers` object to create API endpoints:

```tsx
// apps/web/src/routes/api/posts.ts
import { createFileRoute } from '@tanstack/react-router';
import { z } from 'zod';
import { db } from '@oakoss/database';
import { auth } from '@oakoss/auth/server';

export const Route = createFileRoute('/api/posts')({
  server: {
    handlers: {
      GET: async ({ request }) => {
        const url = new URL(request.url);
        const page = parseInt(url.searchParams.get('page') || '1');
        const limit = parseInt(url.searchParams.get('limit') || '10');

        const posts = await db.query.posts.findMany({
          limit,
          offset: (page - 1) * limit,
          orderBy: (posts, { desc }) => desc(posts.createdAt),
        });

        const total = await db.select({ count: count() }).from(posts);

        return Response.json({
          data: posts,
          pagination: { page, limit, total: total[0].count },
        });
      },

      POST: async ({ request }) => {
        const session = await auth.api.getSession({ headers: request.headers });
        if (!session) {
          return Response.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const body = await request.json();
        const result = createPostSchema.safeParse(body);

        if (!result.success) {
          return Response.json(
            {
              error: 'Validation failed',
              details: z.treeifyError(result.error),
            },
            { status: 400 },
          );
        }

        const [post] = await db
          .insert(posts)
          .values({ ...result.data, authorId: session.user.id })
          .returning();

        return Response.json(post, { status: 201 });
      },
    },
  },
});
```

## RESTful Resource Pattern

```tsx
// apps/web/src/routes/api/posts/$id.ts
import { createFileRoute } from '@tanstack/react-router';
import { z } from 'zod';
import { db, eq, and } from '@oakoss/database';
import { posts } from '@oakoss/database/schema';
import { auth } from '@oakoss/auth/server';

export const Route = createFileRoute('/api/posts/$id')({
  server: {
    handlers: {
      GET: async ({ params }) => {
        const post = await db.query.posts.findFirst({
          where: eq(posts.id, params.id),
          with: { author: true, comments: true },
        });

        if (!post) {
          return Response.json({ error: 'Not found' }, { status: 404 });
        }

        return Response.json(post);
      },

      PATCH: async ({ params, request }) => {
        const session = await auth.api.getSession({ headers: request.headers });
        if (!session) {
          return Response.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const body = await request.json();
        const result = updatePostSchema.safeParse(body);

        if (!result.success) {
          return Response.json(
            { error: z.treeifyError(result.error) },
            { status: 400 },
          );
        }

        const [updated] = await db
          .update(posts)
          .set({ ...result.data, updatedAt: new Date() })
          .where(
            and(eq(posts.id, params.id), eq(posts.authorId, session.user.id)),
          )
          .returning();

        if (!updated) {
          return Response.json(
            { error: 'Not found or forbidden' },
            { status: 404 },
          );
        }

        return Response.json(updated);
      },

      DELETE: async ({ params, request }) => {
        const session = await auth.api.getSession({ headers: request.headers });
        if (!session) {
          return Response.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const [deleted] = await db
          .delete(posts)
          .where(
            and(eq(posts.id, params.id), eq(posts.authorId, session.user.id)),
          )
          .returning();

        if (!deleted) {
          return Response.json(
            { error: 'Not found or forbidden' },
            { status: 404 },
          );
        }

        return new Response(null, { status: 204 });
      },
    },
  },
});
```

## Auth Handler (Better Auth)

The auth handler is a special case that uses a catch-all route:

```tsx
// apps/web/src/routes/api/auth/$.ts
import { createFileRoute } from '@tanstack/react-router';
import { auth } from '@oakoss/auth/server';

export const Route = createFileRoute('/api/auth/$')({
  server: {
    handlers: {
      GET: ({ request }) => auth.handler(request),
      POST: ({ request }) => auth.handler(request),
    },
  },
});
```

## Webhook Handler

```tsx
// apps/web/src/routes/api/webhooks/stripe.ts
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/api/webhooks/stripe')({
  server: {
    handlers: {
      POST: async ({ request }) => {
        const body = await request.text();
        const signature = request.headers.get('stripe-signature');

        if (!signature) {
          return Response.json({ error: 'Missing signature' }, { status: 400 });
        }

        try {
          const event = stripe.webhooks.constructEvent(
            body,
            signature,
            process.env.STRIPE_WEBHOOK_SECRET!,
          );

          switch (event.type) {
            case 'checkout.session.completed':
              await handleCheckoutComplete(event.data.object);
              break;
            case 'customer.subscription.updated':
              await handleSubscriptionUpdate(event.data.object);
              break;
            default:
              console.log(`Unhandled event type: ${event.type}`);
          }

          return Response.json({ received: true });
        } catch (error) {
          console.error('Webhook error:', error);
          return Response.json({ error: 'Webhook failed' }, { status: 400 });
        }
      },
    },
  },
});
```

## Health Check Endpoint

```tsx
// apps/web/src/routes/api/health.ts
import { createFileRoute } from '@tanstack/react-router';
import { db } from '@oakoss/database';
import { sql } from 'drizzle-orm';

export const Route = createFileRoute('/api/health')({
  server: {
    handlers: {
      GET: async () => {
        try {
          await db.execute(sql`SELECT 1`);

          return Response.json({
            status: 'healthy',
            timestamp: new Date().toISOString(),
          });
        } catch (error) {
          return Response.json(
            {
              status: 'unhealthy',
              error: error instanceof Error ? error.message : 'Unknown error',
            },
            { status: 503 },
          );
        }
      },
    },
  },
});
```

## File Upload Endpoint

```tsx
// apps/web/src/routes/api/upload.ts
import { createFileRoute } from '@tanstack/react-router';
import { auth } from '@oakoss/auth/server';
import { writeFile } from 'node:fs/promises';

export const Route = createFileRoute('/api/upload')({
  server: {
    handlers: {
      POST: async ({ request }) => {
        const session = await auth.api.getSession({ headers: request.headers });
        if (!session) {
          return Response.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const formData = await request.formData();
        const file = formData.get('file') as File;

        if (!file) {
          return Response.json({ error: 'No file provided' }, { status: 400 });
        }

        const maxSize = 5 * 1024 * 1024; // 5MB
        if (file.size > maxSize) {
          return Response.json({ error: 'File too large' }, { status: 400 });
        }

        const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
          return Response.json({ error: 'Invalid file type' }, { status: 400 });
        }

        const buffer = await file.arrayBuffer();
        const filename = `${Date.now()}-${file.name}`;
        await writeFile(`./uploads/${filename}`, Buffer.from(buffer));

        return Response.json({ filename, size: file.size }, { status: 201 });
      },
    },
  },
});
```

## Key Differences from Server Functions

| Use Case         | Pattern                                  |
| ---------------- | ---------------------------------------- |
| RPC-style calls  | `createServerFn` (server functions)      |
| REST API routes  | `createFileRoute` with `server.handlers` |
| Webhooks         | `createFileRoute` with `server.handlers` |
| Form submissions | `createServerFn` (easier integration)    |
| Route loaders    | `createServerFn` + loader                |
