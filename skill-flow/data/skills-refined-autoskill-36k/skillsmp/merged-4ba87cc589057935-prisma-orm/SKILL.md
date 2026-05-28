---
name: prisma-orm
description: Use this skill when you need type-safe database access with Prisma ORM, covering schema design, migrations, relations, queries, and TypeScript integration.
---

# Prisma ORM - Type-Safe Database Toolkit

Prisma is a next-generation Node.js and TypeScript ORM that provides a type-safe database access layer with schema-first development, auto-generated client, and powerful migration system.

## Quick Start

### Installation

```bash
npm install prisma @prisma/client
npx prisma init
```

### Basic Workflow

```bash
# 1. Define schema
# Edit prisma/schema.prisma

# 2. Create migration
npx prisma migrate dev --name init

# 3. Generate client
npx prisma generate

# 4. Open Studio
npx prisma studio
```

## Schema Design

### Basic Model Structure

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql" // mysql, sqlite, sqlserver, mongodb
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
}
```

### Field Types & Modifiers

```prisma
model Product {
  id          Int      @id @default(autoincrement())
  sku         String   @unique
  name        String
  description String?  // Optional field
  price       Decimal  @db.Decimal(10, 2)
  inStock     Boolean  @default(true)
  quantity    Int      @default(0)
  tags        String[] // Array field (PostgreSQL)
  metadata    Json?    // JSON field
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([sku])
  @@index([name, inStock])
}
```

### Relations

**One-to-Many:**
```prisma
model User {
  id    String @id @default(cuid())
  posts Post[]
}

model Post {
  id       String @id @default(cuid())
  author   User   @relation(fields: [authorId], references: [id])
  authorId String

  @@index([authorId])
}
```

**Many-to-Many:**
```prisma
model Post {
  id         String     @id @default(cuid())
  categories Category[] @relation("PostCategories")
}

model Category {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[] @relation("PostCategories")
}
```

**One-to-One:**
```prisma
model User {
  id      String   @id @default(cuid())
  profile Profile?
}

model Profile {
  id     String @id @default(cuid())
  bio    String
  user   User   @relation(fields: [userId], references: [id])
  userId String @unique
}
```

## Prisma Client Queries

### Type-Safe CRUD Operations

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Create
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    name: 'Alice',
    posts: {
      create: { title: 'First Post', content: 'Hello World' }
    }
  },
  include: { posts: true }
});

// Read with filters
const users = await prisma.user.findMany({
  where: { email: { contains: '@example.com' } },
  include: { posts: { where: { published: true } } },
  orderBy: { createdAt: 'desc' },
  take: 10
});

// Update
await prisma.user.update({
  where: { id: userId },
  data: { name: 'Bob' }
});

// Delete
await prisma.user.delete({ where: { id: userId } });
```

### Filtering and Aggregations

```typescript
const userCount = await prisma.user.count({
  where: { isActive: true },
});

const stats = await prisma.post.aggregate({
  _count: { id: true },
  _avg: { views: true },
  _sum: { likes: true },
  _max: { createdAt: true },
  where: { published: true }
});
```

## Migrations

### Development Workflow

```bash
# Create and apply migration
npx prisma migrate dev --name add_user_role

# Reset database (WARNING: deletes all data)
npx prisma migrate reset

# View migration status
npx prisma migrate status
```

### Production Deployment

```bash
# Apply pending migrations
npx prisma migrate deploy

# Generate client (in CI/CD)
npx prisma generate
```

## Transactions

### Sequential (Interactive)

```typescript
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { email: 'alice@example.com' }
  });

  await tx.post.create({
    data: { title: 'Post', authorId: user.id }
  });

  // Rollback if error thrown
  if (someCondition) {
    throw new Error('Rollback transaction');
  }
});
```

### Batch (Parallel)

```typescript
const [deletedPosts, updatedUser] = await prisma.$transaction([
  prisma.post.deleteMany({ where: { published: false } }),
  prisma.user.update({
    where: { id: userId },
    data: { name: 'Updated' }
  })
]);
```

## Best Practices

1. **Singleton Pattern** - Reuse `PrismaClient` instance (especially in dev).
2. **Connection Management** - Configure pool size for serverless.
3. **Select Specific Fields** - Use `select` to reduce payload size.
4. **Use Transactions** - For multi-step operations requiring atomicity.
5. **Index Strategically** - Add `@@index` on frequently queried fields.
6. **Migration Discipline** - Never edit migrations after deployment.
7. **Soft Deletes** - Add `deletedAt` field instead of hard deletes.
8. **Validate Before Saving** - Use Zod schemas before Prisma operations.

## Common Pitfalls

- Creating multiple `PrismaClient` instances can lead to connection leaks.
- Not using transactions for multi-step operations can leave inconsistent states.
- Missing indexes on foreign keys or frequently queried fields can degrade performance.

## Resources

- **Documentation**: [Prisma Documentation](https://www.prisma.io/docs)
- **Schema Reference**: [Prisma Schema Reference](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference)
- **Client API**: [Prisma Client Reference](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)