---
name: cloudflare-workers-api-development
description: Use this skill for comprehensive guidance on building serverless APIs with Cloudflare Workers, TypeScript, and the Hono framework.
---

# Cloudflare Workers API Development

This skill provides guidelines for developing high-performance, serverless APIs using Cloudflare Workers, TypeScript, and the Hono framework.

## TypeScript General Guidelines

### Basic Principles

- Use English for all code and documentation.
- Always declare types for variables and functions (parameters and return values).
- Avoid using `any` type; create necessary types instead.
- Use JSDoc to document public classes and methods.
- Write concise, maintainable, and technically accurate code.
- Use functional and declarative programming patterns; avoid classes.
- Prefer iteration and modularization to adhere to DRY principles.

### Nomenclature

- Use PascalCase for types and interfaces.
- Use camelCase for variables, functions, and methods.
- Use kebab-case for file and directory names.
- Use UPPERCASE for environment variables.
- Use descriptive variable names with auxiliary verbs: `isLoading`, `hasError`, `canDelete`.
- Start each function with a verb.

### Functions

- Write short functions with a single purpose.
- Use arrow functions for handlers and middleware.
- Prefer the RO-RO pattern: Receive an Object, Return an Object.
- Use default parameters instead of null checks.

### Types and Interfaces

- Prefer interfaces over types for object shapes.
- Avoid enums; use maps or const objects instead for better type safety.
- Use Zod for runtime validation with inferred types.
- Use `readonly` for immutable properties.
- Use `import type` for type-only imports.

## Hono-Specific Guidelines

### Project Structure

```
src/
  routes/
    {resource}/
      index.ts
      handlers.ts
      validators.ts
  middleware/
    auth.ts
    cors.ts
    logger.ts
  services/
    {domain}Service.ts
  types/
    index.ts
  utils/
  config/
  index.ts
```

### App Initialization

```typescript
import { Hono } from 'hono';

// Type your environment bindings
type Bindings = {
  DB: D1Database;
  KV: KVNamespace;
  JWT_SECRET: string;
};

const app = new Hono<{ Bindings: Bindings }>();
```

### Middleware

- Use Hono's built-in middleware where available.
- Create typed middleware for custom logic.
- Chain middleware for composability.

```typescript
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { jwt } from 'hono/jwt';

app.use('*', logger());
app.use('/api/*', cors());
app.use('/api/*', jwt({ secret: 'your-secret' }));

// Custom middleware
const authMiddleware = async (c: Context, next: Next) => {
  const token = c.req.header("Authorization");
  if (!token?.startsWith("Bearer")) {
    return c.text("Missing or invalid Authorization header", 401);
  }
  await next();
};
```

### Routing

- Use method chaining for clean route definitions.
- Group related routes with `app.route()`.

```typescript
const users = new Hono<{ Bindings: Bindings }>();

users.get('/', listUsers);
users.get('/:id', getUser);
users.post('/', zValidator('json', createUserSchema), createUser);
users.put('/:id', zValidator('json', updateUserSchema), updateUser);
users.delete('/:id', deleteUser);

app.route('/api/users', users);
```

### Request Validation with Zod

- Use `@hono/zod-validator` for request validation.
- Define schemas for all request inputs.
- Infer types from Zod schemas.

```typescript
import { z } from 'zod';
import { zValidator } from '@hono/zod-validator';

const createUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  role: z.enum(['user', 'admin']).default('user'),
});

app.post('/users', zValidator('json', createUserSchema), async (c) => {
  const data = c.req.valid('json');
});
```

### Error Handling

- Use Hono's `HTTPException` for expected errors.
- Create global error handler middleware.

```typescript
import { HTTPException } from 'hono/http-exception';

app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status);
  }
  return c.json({ error: 'Internal Server Error' }, 500);
});
```

### Cloudflare Workers Integration

- Use Workers KV for key-value storage.
- Use D1 for SQL databases.
- Use R2 for object storage.
- Use Durable Objects for stateful applications.

```typescript
const result = await c.env.DB.prepare('SELECT * FROM users').all();
await c.env.KV.put('key', 'value');
```

### Testing

- Use Hono's test client for integration tests.
- Use Vitest or Jest as test runner.

```typescript
import { testClient } from 'hono/testing';
import { describe, it, expect } from 'vitest';

describe('User API', () => {
  const client = testClient(app);
  it('should list users', async () => {
    const res = await client.api.users.$get();
    expect(res.status).toBe(200);
  });
});
```

## Best Practices

- **Type Safety**: Use TypeScript interfaces for request/response types and environment bindings.
- **Security**: Implement proper CORS policies and validate all inputs with Zod schemas.
- **Authentication**: Use Bearer token authentication for protected routes.
- **Configuration**: Store API URLs and feature flags in environment variables.
- **API Documentation**: Define comprehensive OpenAPI schemas with examples and error responses.
- **Error Handling**: Return appropriate HTTP status codes and structured error responses.
- **Performance**: Set appropriate cache headers and use observability for monitoring.
- **Deployment**: Use Wrangler for local development and production deployment.

## Multi-Runtime Support

Hono runs on multiple runtimes. Configure appropriately:

```typescript
// Cloudflare Workers
export default app;

// Node.js
import { serve } from '@hono/node-server';
serve(app);
```

## Related Skills

- `sveltekit-development`: For frontend integration with Workers APIs.
- `frontend-developer`: For building client applications that consume Worker endpoints.
- `deployment-specialist`: For advanced deployment strategies and CI/CD with Cloudflare.
- `backend-developer`: For general API design and server-side development patterns.