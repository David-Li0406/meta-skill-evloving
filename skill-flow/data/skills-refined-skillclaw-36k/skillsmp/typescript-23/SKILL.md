---
name: typescript
description: >-
  TypeScript conventions for ecommerce monorepo. Covers Next.js, Fastify, Prisma,
  Zod validation, React Query, and testing patterns. Triggers on "typescript",
  "type error", "ts", "tsx", "type hints", "zod schema", "prisma", "react query",
  "next.js", "fastify routes", "api types".
  PROACTIVE: MUST invoke when writing or editing .ts or .tsx files.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ABOUTME: TypeScript skill for ecommerce monorepo with Next.js and Fastify
# ABOUTME: Covers type patterns, Prisma, Zod, React Query, and testing conventions

# TypeScript Skill (Ecommerce)

## Quick Reference

| Rule | Convention |
|------|------------|
| Strict mode | Always enabled |
| Null checks | `strictNullChecks: true` |
| Return types | Explicit for public APIs |
| Zod schemas | Validation at boundaries |
| Prisma types | Auto-generated, never manual |

---

## Project Structure

```
apps/
├── frontend/                 # Next.js 16
│   ├── src/
│   │   ├── app/              # App Router pages
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom hooks (useProducts, useCart, etc.)
│   │   ├── lib/              # Utilities (api.ts, auth-context.tsx)
│   │   └── types/            # Type definitions
│   └── tests/                # Frontend tests
│
└── backend/                  # Fastify API
    ├── src/
    │   ├── config/           # Configuration
    │   ├── middleware/       # Auth guard, error handler
    │   ├── modules/          # Feature modules (auth, catalog, orders)
    │   └── utils/            # Prisma, Redis, logger
    ├── prisma/               # Schema and migrations
    └── tests/                # Backend tests
```

---

## Type Patterns

### API Response Types

```typescript
// types/api.ts
export interface ApiResponse<T> {
  data: T;
  meta?: {
    total: number;
    page: number;
    pageSize: number;
  };
}

export interface ApiError {
  statusCode: number;
  error: string;
  message: string;
}
```

### Zod Schemas (Validation)

```typescript
// schemas/product.ts
import { z } from 'zod';

export const ProductSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(255),
  price: z.number().positive(),
  categoryId: z.string().uuid(),
});

export type Product = z.infer<typeof ProductSchema>;

// Use at API boundaries
const validated = ProductSchema.parse(requestBody);
```

### Prisma Integration

```typescript
// DON'T manually define DB types
// DO use Prisma generated types
import { User, Product, Order } from '@prisma/client';

// Include relations explicitly
import { Prisma } from '@prisma/client';

type OrderWithItems = Prisma.OrderGetPayload<{
  include: { items: { include: { product: true } } };
}>;
```

---

## React Patterns

### Custom Hooks

```typescript
// hooks/useProducts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useProducts(categoryId?: string) {
  return useQuery({
    queryKey: ['products', categoryId],
    queryFn: () => api.getProducts(categoryId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useCreateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.createProduct,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
}
```

### Component Props

```typescript
// components/ProductCard.tsx
interface ProductCardProps {
  product: Product;
  onAddToCart?: (productId: string) => void;
  className?: string;
}

export function ProductCard({ product, onAddToCart, className }: ProductCardProps) {
  // ...
}
```

---

## Fastify Patterns

### Route Types

```typescript
// modules/catalog/catalog.routes.ts
import { FastifyPluginAsync } from 'fastify';
import { z } from 'zod';

const GetProductParams = z.object({
  id: z.string().uuid(),
});

const catalogRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.get<{
    Params: z.infer<typeof GetProductParams>;
  }>('/products/:id', {
    schema: {
      params: GetProductParams,
    },
  }, async (request, reply) => {
    const { id } = request.params;
    // ...
  });
};

export default catalogRoutes;
```

### Error Handling

```typescript
// middleware/error-handler.ts
import { FastifyError, FastifyReply, FastifyRequest } from 'fastify';

export function errorHandler(
  error: FastifyError,
  request: FastifyRequest,
  reply: FastifyReply
) {
  const statusCode = error.statusCode ?? 500;

  reply.status(statusCode).send({
    statusCode,
    error: error.name,
    message: error.message,
  });
}
```

---

## Testing Patterns

### Unit Tests (Vitest)

```typescript
// tests/hooks/useProducts.test.tsx
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useProducts } from '@/hooks/useProducts';

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={new QueryClient()}>
    {children}
  </QueryClientProvider>
);

describe('useProducts', () => {
  it('fetches products', async () => {
    const { result } = renderHook(() => useProducts(), { wrapper });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(result.current.data).toHaveLength(18);
  });
});
```

### Integration Tests (Testcontainers)

```typescript
// tests/integration/catalog.test.ts
import { PostgreSqlContainer } from '@testcontainers/postgresql';
import { buildApp } from '../../src/app';

describe('Catalog API', () => {
  let container: StartedPostgreSqlContainer;
  let app: FastifyInstance;

  beforeAll(async () => {
    container = await new PostgreSqlContainer().start();
    process.env.DATABASE_URL = container.getConnectionUri();
    app = await buildApp();
  });

  afterAll(async () => {
    await app.close();
    await container.stop();
  });

  it('GET /products returns products', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/api/products',
    });

    expect(response.statusCode).toBe(200);
  });
});
```

---

## Commands

```bash
# Type checking
npm run typecheck           # All workspaces
npm run typecheck -w apps/backend

# Linting
npm run lint
npm run lint:fix

# Testing
npm run test                # All tests
npm run test -w apps/backend

# Prisma
npm run db:generate -w apps/backend  # Generate types
npm run db:push -w apps/backend      # Push schema
npm run db:seed -w apps/backend      # Seed data
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `any` type | No type safety | Use `unknown` + type guards |
| Manual DB types | Drift from schema | Use Prisma generated types |
| Implicit returns | Unclear API | Explicit return types |
| No validation | Runtime errors | Zod at boundaries |
| `// @ts-ignore` | Hidden bugs | Fix the type issue |

---

## Checklist

Before committing TypeScript changes:

- [ ] No `any` types (use `unknown` if needed)
- [ ] Zod schemas for API inputs
- [ ] Prisma types for DB entities
- [ ] Tests cover new functionality
- [ ] `npm run typecheck` passes
- [ ] `npm run lint` passes
