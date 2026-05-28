---
name: migestion-prisma
description: >
  Prisma ORM patterns for MiGestion - multi-tenant queries, migrations, seed.
  Trigger: When writing Prisma queries, migrations, or schema changes.
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [api]
  auto_invoke: 'Writing Prisma queries/migrations'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Multi-Tenant Pattern (REQUIRED)

All queries MUST include `tenantId` in WHERE clause for tenant isolation.

```typescript
// ✅ ALWAYS: Include tenantId
await prisma.client.findFirst({
  where: { tenantId, id: clientId },
});

await prisma.client.findMany({
  where: { tenantId },
});

// ❌ NEVER: Query without tenant
await prisma.client.findUnique({
  where: { id: clientId }, // NO! Bypasses tenant isolation
});
```

## Repository Pattern

Repositories encapsulate all Prisma queries.

```typescript
// ✅ Repository functions
export async function findById(tenantId: string, id: string) {
  return prisma.example.findFirst({
    where: { id, tenantId },
  });
}

export async function findMany(tenantId: string, params: FindParams) {
  const { page, limit, search, ...filters } = params;

  return await prisma.example.findMany({
    where: { tenantId, ...filters },
    skip: (page - 1) * limit,
    take: limit,
    orderBy: { createdAt: 'desc' },
  });
}

export async function create(data: PrismaExampleCreateInput) {
  return prisma.example.create({ data });
}

export async function update(tenantId: string, id: string, data: PrismaExampleUpdateInput) {
  return prisma.example.update({
    where: { id, tenantId },
    data,
  });
}

export async function remove(tenantId: string, id: string) {
  return prisma.example.delete({
    where: { id, tenantId },
  });
}
```

## Pagination

```typescript
export async function findManyPaginated(tenantId: string, page: number, limit: number) {
  const [data, total] = await Promise.all([
    prisma.example.findMany({
      where: { tenantId },
      skip: (page - 1) * limit,
      take: limit,
    }),
    prisma.example.count({ where: { tenantId } }),
  ]);

  return { data, total };
}
```

## Search/Filter

```typescript
export async function findWithSearch(tenantId: string, search?: string, status?: string) {
  return prisma.example.findMany({
    where: {
      tenantId,
      ...(search && {
        OR: [
          { name: { contains: search, mode: 'insensitive' } },
          { email: { contains: search, mode: 'insensitive' } },
        ],
      }),
      ...(status && { status }),
    },
  });
}
```

## Relations

```typescript
export async function findWithRelations(tenantId: string, id: string) {
  return prisma.example.findFirst({
    where: { id, tenantId },
    include: {
      user: true,
      interactions: {
        orderBy: { createdAt: 'desc' },
        take: 10,
      },
    },
  });
}
```

## JSON Fields

```typescript
// Reading JSON field
const client = await prisma.client.findUnique({
  where: { id },
  select: { tags: true, customFields: true },
});

// Writing JSON field
await prisma.client.create({
  data: {
    tags: ['vip', 'priority'] as Prisma.InputJsonValue,
    customFields: { preferences: { language: 'es' } } as Prisma.InputJsonValue,
  },
});

// Querying JSON field
await prisma.client.findMany({
  where: {
    tags: {
      path: ['0'],
      equals: 'vip',
    },
  },
});
```

## Transactions

```typescript
await prisma.$transaction(async tx => {
  const client = await tx.client.create({ data: clientData });

  await tx.interaction.create({
    data: {
      clientId: client.id,
      type: 'initial_contact',
    },
  });

  return client;
});
```

## Schema Pattern

```prisma
model Client {
  id          String   @id @default(cuid())
  tenantId    String
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  // Relations
  interactions Interaction[]
  assignedTo   User?    @relation(fields: [assignedToId], references: [id])
  assignedToId String?

  @@unique([id, tenantId])
  @@index([tenantId])
  @@index([tenantId, status])
}
```

## Commands

```bash
npm run db:generate          # Generate Prisma client
npm run db:migrate           # Create and apply migration
npm run db:migrate:prod      # Apply migration in production
npm run db:seed              # Seed database
npm run db:studio            # Open Prisma Studio UI

# Manual migration
npx prisma migrate dev --name add_field
npx prisma migrate deploy   # Production
npx prisma studio
```

## Migrations

```bash
# Create migration
npm run db:migrate -- --name add_client_field

# Reset database (development only)
npx prisma migrate reset

# Seed after migration
npm run db:seed
```

## Seed Pattern

```typescript
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  const hashedPassword = await bcrypt.hash('password123', 10);

  const tenant = await prisma.tenant.create({
    data: {
      name: 'Demo Company',
      users: {
        create: {
          email: 'admin@example.com',
          password: hashedPassword,
          name: 'Admin User',
          role: 'OWNER',
        },
      },
    },
  });

  console.log('Seed complete:', tenant);
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
```

## Related Skills

- `migestion-api` - Full API module patterns
- `typescript` - TypeScript patterns for Prisma types
