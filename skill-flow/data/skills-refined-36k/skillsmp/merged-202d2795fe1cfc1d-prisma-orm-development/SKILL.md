---
name: prisma-orm-development
description: Use this skill when developing applications with Prisma ORM in TypeScript, covering schema design, migrations, type-safe queries, and best practices.
---

# Prisma ORM Development

You are an expert in Prisma ORM development with TypeScript.

## Overview

Prisma is a next-generation Node.js and TypeScript ORM that provides:
- **Prisma Schema**: Declarative data modeling language
- **Prisma Migrate**: Database migration system
- **Prisma Client**: Auto-generated, type-safe query builder
- **Prisma Studio**: GUI for database exploration

## Quick Start

```bash
# Initialize Prisma in a project
npm install prisma --save-dev
npm install @prisma/client
npx prisma init

# Common commands
npx prisma generate      # Generate Prisma Client
npx prisma migrate dev   # Create and apply migrations
npx prisma db push       # Push schema without migrations (dev)
npx prisma studio        # Open database GUI
```

## TypeScript Fundamentals

### Basic Principles
- Always declare explicit types for variables and functions
- Avoid using 'any'
- Leverage JSDoc for public APIs
- Maintain single exports per file
- Prioritize self-documenting code

### Naming Conventions
- PascalCase for classes/interfaces
- camelCase for variables and methods
- kebab-case for files/directories
- UPPERCASE for constants
- Verb-based boolean names (isLoading, hasError, canDelete)

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
```

### Field Types & Modifiers

```prisma
model Example {
  id          Int       @id @default(autoincrement())
  uuid        String    @id @default(uuid())
  cuid        String    @id @default(cuid())
  name        String    @db.VarChar(255)
  content     String    @db.Text
  count       Int       @default(0)
  price       Decimal   @db.Decimal(10, 2)
  rating      Float
  isActive    Boolean   @default(true)
  data        Json
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
  
  // Optional field
  deletedAt   DateTime?
  
  // Unique constraint
  slug        String    @unique
  
  // Composite unique
  @@unique([categoryId, slug])
  
  // Composite index
  @@index([createdAt, isActive])
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

## Migrations

### Development Workflow

```bash
# Create migration from schema changes
npx prisma migrate dev --name add_user_table

# Apply migrations without creating new ones
npx prisma migrate deploy

# Reset database (drops all data!)
npx prisma migrate reset

# Check migration status
npx prisma migrate status
```

### Migration File Structure

```
prisma/
├── schema.prisma
└── migrations/
    ├── 20240115120000_init/
    │   └── migration.sql
    ├── 20240116080000_add_posts/
    │   └── migration.sql
    └── migration_lock.toml
```

## Client Operations

### Type-Safe CRUD Operations

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// CREATE
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John Doe',
    posts: {
      create: { title: 'First Post', content: 'Hello World' }
    }
  },
  include: { posts: true }
});

// READ
const users = await prisma.user.findMany({
  where: { email: { contains: '@example.com' } },
  include: { posts: { where: { published: true } } },
  orderBy: { createdAt: 'desc' },
  take: 10
});

// UPDATE
await prisma.user.update({
  where: { id: userId },
  data: { name: 'Updated Name' }
});

// DELETE
await prisma.user.delete({ where: { id: userId } });
```

## Transactions

### Sequential Operations

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

### Batch Operations

```typescript
const [deletedPosts, updatedUser] = await prisma.$transaction([
  prisma.post.deleteMany({ where: { published: false } }),
  prisma.user.update({
    where: { id: userId },
    data: { name: 'Updated' }
  })
]);
```

## Error Handling

```typescript
import { Prisma } from '@prisma/client';

try {
  await prisma.user.create({ data });
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    if (error.code === 'P2002') {
      throw new Error('Email already exists');
    }
    if (error.code === 'P2025') {
      throw new Error('Record not found');
    }
  }
  throw error;
}
```

## Best Practices

1. **Singleton Pattern** - Reuse `PrismaClient` instance (especially in dev)
2. **Connection Management** - Configure pool size for serverless
3. **Select Specific Fields** - Use `select` to reduce payload size
4. **Use Transactions** - For multi-step operations requiring atomicity
5. **Index Strategically** - Add `@@index` on frequently queried fields
6. **Migration Discipline** - Never edit migrations after deployment
7. **Schema Versioning** - Use descriptive migration names
8. **Soft Deletes** - Add `deletedAt` field instead of hard deletes
9. **Validate Before Saving** - Use Zod schemas before Prisma operations
10. **Monitor Queries** - Use `prisma.$on('query')` for logging

## Common Pitfalls

- Creating multiple `PrismaClient` instances can lead to connection leaks.
- Not using transactions for multi-step operations can leave inconsistent states.
- Missing indexes on foreign keys or frequently queried fields can degrade performance.

## Resources

- **Documentation**: [Prisma Documentation](https://www.prisma.io/docs)
- **Schema Reference**: [Prisma Schema Reference](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference)
- **Client API**: [Prisma Client Reference](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)
- **Examples**: [Prisma Examples](https://github.com/prisma/prisma-examples)