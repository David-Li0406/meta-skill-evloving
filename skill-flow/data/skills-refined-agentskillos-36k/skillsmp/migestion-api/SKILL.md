---
name: migestion-api
description: >
  Backend patterns for MiGestion API - Express, Prisma, module architecture.
  Trigger: When working on API code (controllers, services, repositories, middleware, validation).
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [api]
  auto_invoke: 'Creating new API modules'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Module Structure (REQUIRED)

```typescript
// modules/example/
├── index.ts              # Barrel export
├── example.routes.ts     # Route definitions
├── example.controller.ts # HTTP handlers (thin)
├── example.service.ts    # Business logic
├── example.repository.ts # Prisma queries
├── example.dto.ts        # DTO mappers
└── example.validator.ts  # Zod schemas
```

## Controller Pattern (REQUIRED)

Controllers are **thin** - extract from request, call service, format response.

```typescript
// ✅ ALWAYS: Thin controller
export async function list(req: Request, res: Response): Promise<Response> {
  const tenantId = req.tenantId!;
  const query = req.query as unknown as ListQuery;

  const result = await exampleService.list(tenantId, query);

  return sendSuccess(res, result);
}

// ❌ NEVER: Business logic in controller
export async function list(req: Request, res: Response) {
  const { data, total } = await prisma.example.findMany(...); // NO!
  return res.json({ data, total });
}
```

## Service Pattern (REQUIRED)

Services contain business logic and coordinate between repository and DTO.

```typescript
export async function getById(tenantId: string, id: string): Promise<ExampleDto> {
  const entity = await exampleRepository.findById(tenantId, id);

  if (!entity) {
    throw new NotFoundError('Example');
  }

  return toExampleDto(entity);
}
```

## Repository Pattern (REQUIRED)

Repositories encapsulate all Prisma database queries.

```typescript
export async function findById(tenantId: string, id: string) {
  return prisma.example.findFirst({
    where: { id, tenantId },
  });
}

export async function findMany(params: FindManyParams) {
  const { tenantId, page, limit, search, ...filters } = params;

  return await prisma.example.findMany({
    where: { tenantId, ...filters },
    skip: (page - 1) * limit,
    take: limit,
    orderBy: { createdAt: 'desc' },
  });
}
```

## Multi-Tenant Queries (REQUIRED)

All queries MUST include `tenantId` in WHERE clause.

```typescript
// ✅ ALWAYS: Include tenantId
prisma.example.findFirst({
  where: { tenantId, id },
});

// ❌ NEVER: Query without tenant
prisma.example.findUnique({
  where: { id }, // NO! Bypasses tenant isolation
});
```

## DTO Pattern (REQUIRED)

DTOs transform database entities to API responses.

```typescript
export interface ExampleDto {
  id: string;
  name: string;
  createdAt: string;
}

export function toExampleDto(entity: PrismaExample): ExampleDto {
  return {
    id: entity.id,
    name: entity.name,
    createdAt: entity.createdAt.toISOString(),
  };
}
```

## Validation (REQUIRED)

Use Zod for all input validation.

```typescript
import { z } from 'zod';

export const createExampleSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email().optional(),
});

export type CreateExampleInput = z.infer<typeof createExampleSchema>;
```

## Error Handling

Use custom error classes, NOT HTTP status codes directly.

```typescript
import { NotFoundError, BadRequestError } from '../../shared/errors/app-error.js';

if (!entity) {
  throw new NotFoundError('Example');
}

if (invalid) {
  throw new BadRequestError('Invalid input', 'INVALID_INPUT');
}
```

## Response Utilities

Use standardized response helpers.

```typescript
import { sendSuccess, sendCreated, sendNoContent } from '../../shared/utils/response.js';

sendSuccess(res, data); // 200 OK
sendCreated(res, data); // 201 Created
sendNoContent(res); // 204 No Content
```

## Middleware Pattern

Auth, RBAC, tenant, audit middleware on protected routes.

```typescript
router.get('/examples', authMiddleware, tenantMiddleware, rbacMiddleware('admin'), listHandler);
```

## Import Extensions (REQUIRED)

Backend uses ES modules - local imports MUST include `.js` extension.

```typescript
// ✅ ALWAYS: .js extension for local imports
import { sendSuccess } from '../../shared/utils/response.js';
import * as exampleService from './example.service.js';

// ❌ NEVER: Missing extension
import { sendSuccess } from '../../shared/utils/response';
```

## Commands

```bash
npm run dev:api              # Start dev server
npm run build:api            # Build
npm run test:api             # Run tests
npm run db:generate          # Generate Prisma client
npm run db:migrate           # Run migrations
npm run lint --workspace=@migestion/api  # Lint
npm run typecheck            # Type check
```

## Related Skills

- `migestion-prisma` - Prisma ORM patterns
- `zod-3` - Zod validation schemas
- `migestion-test-api` - API testing patterns
