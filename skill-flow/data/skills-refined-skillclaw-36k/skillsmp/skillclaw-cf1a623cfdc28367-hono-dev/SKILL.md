---
name: hono-dev
description: Use this skill when building APIs with Hono, utilizing type-safe RPC, or implementing OpenAPI documentation.
---

# Hono API Development

Route chaining → type-safe RPC → end-to-end types.

<when_to_use>

- Building REST APIs with Hono
- Type-safe RPC with hono/client
- OpenAPI documentation with Zod
- Testing APIs with testClient
- When user mentions "Hono", "RPC", or "OpenAPI"

NOT for: Bun runtime APIs (use bun-dev), other frameworks (Express, Fastify)

</when_to_use>

<version_notes>

Hono v4+ with @hono/zod-openapi v1.0+
Check hono.dev for latest patterns.

</version_notes>

## Route Chaining — Critical Pattern

Type inference flows through method chain. Break chain = lose types.

<route_chaining>

```typescript
// ✅ Chained routes preserve types
const app = new Hono()
  .get('/users', (c) => c.json({ users: [] }))
  .get('/users/:id', (c) => {
    const id = c.req.param('id'); // Typed!
    return c.json({ id });
  })
  .post('/users', async (c) => {
    const body = await c.req.json();
    return c.json({ created: true }, 201);
  });

export type AppType = typeof app; // Full route types!
```

**❌ NEVER break the chain:**

```typescript
const app = new Hono();
app.get('/users', handler1);  // Types LOST!
app.post('/users', handler2);
```

**Path parameters** — typed automatically:

```typescript
.get('/posts/:id/comments/:commentId', (c) => {
  const { id, commentId } = c.req.param(); // Both string
  return c.json({ postId: id, commentId });
})
```

**Query parameters** — use Zod for validation:

```typescript
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const QuerySchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(20),
});

const app = new Hono()
  .get('/search', zValidator('query', QuerySchema), (c) => {
    const { page, limit } = c.req.valid('query'); // Fully typed!
    return c.json({ page, limit });
  });
```

**Middleware in chain:**

```typescript
const app = new Hono()
  .use('*', logger())
  .use('/api/*', cors())
  .get('/api/public', (c) => c.json({ public: true }))
  .use('/api/admin/*', authMiddleware)
  .get('/api/admin/users', (c) => c.json({ users: [] }));
```

</route_chaining>

## Factory Pattern — Context Typing

Use `createFactory<Env>()` to type context variables across middleware and routes.

<factory_pattern>

```typescript
// Example of using createFactory for context typing
const factory = createFactory<Env>();
```

</factory_pattern>