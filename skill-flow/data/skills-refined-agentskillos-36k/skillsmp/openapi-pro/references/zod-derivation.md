# Zod-First OpenAPI Derivation

## The Zod-to-OpenAPI Bridge
In 2026, writing YAML by hand is considered a legacy practice. The "Elite" workflow involves defining your data models in Zod and then automatically generating the OpenAPI specification.

---

## 1. Defining the Schema
Use `extendZodWithOpenAPI` to add metadata to your Zod objects.

```typescript
import { extendZodWithOpenAPI } from '@asteasolutions/zod-to-openapi';
import { z } from 'zod';

extendZodWithOpenAPI(z);

export const CreateUserSchema = z.object({
  name: z.string().min(3).openapi({ description: 'The user full name', example: 'John Doe' }),
  email: z.string().email().openapi({ description: 'Unique email address' }),
});
```

---

## 2. Generating the Registry
```typescript
import { OpenAPIRegistry, OpenApiGeneratorV31 } from '@asteasolutions/zod-to-openapi';

const registry = new OpenAPIRegistry();
registry.register('User', CreateUserSchema);

const generator = new OpenApiGeneratorV31(registry.definitions);
const spec = generator.generateDocument({
  openapi: '3.1.0',
  info: { title: 'My API', version: '1.0.0' },
});
```

---

## 3. Integration with Hono
Hono's `@hono/zod-openapi` makes this even simpler by integrating the schema directly into the route definition.

```typescript
import { createRoute } from '@hono/zod-openapi';

export const getUserRoute = createRoute({
  method: 'get',
  path: '/users/{id}',
  request: {
    params: z.object({ id: z.string() }),
  },
  responses: {
    200: {
      content: { 'application/json': { schema: UserSchema } },
      description: 'Success',
    },
  },
});
```

---

## Benefits
- **Zero Drift**: Your validation logic and documentation are always in sync.
- **Type Safety**: TypeScript types are inferred from the same Zod schemas used for the API.
- **Improved UX**: Clients get accurate examples and descriptions automatically.
