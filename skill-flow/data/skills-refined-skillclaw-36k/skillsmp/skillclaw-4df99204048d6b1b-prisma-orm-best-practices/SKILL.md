---
name: prisma-orm-best-practices
description: Use this skill when you need best practices for using Prisma ORM effectively in Shopify Apps built with Remix, covering setup, schema design, migrations, and performance.
---

# Prisma ORM Best Practices (2025-2026)

This skill provides guidelines and snippets for using Prisma ORM effectively in Shopify Apps built with Remix.

## 1. Setup & Configuration

### Installation
```bash
npm install prisma --save-dev
npm install @prisma/client
npx prisma init
```

### Recommended `schema.prisma` Config
Use the `postgresql` provider (standard for Shopify apps) or `mysql`. Enable `improving-tracing` and other preview features if needed, but stick to stable for production.

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
  previewFeatures = ["driverAdapters", "metrics"]
}

// Standard Shopify Session Model
model Session {
  id          String    @id
  shop        String
  state       String
  isOnline    Boolean   @default(false)
  scope       String?
  expires     DateTime?
  accessToken String
  userId      BigInt?
}
```

## 2. Singleton Pattern for Remix
In development, Remix reloads the server, which can exhaust database connections if you create a new `PrismaClient` on every reload. Use the singleton pattern.

```typescript
// app/db.server.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

## 3. Schema Design Best Practices

### Use BigInt for Shopify IDs
Shopify IDs (Product ID, Order ID) exceed 32-bit integers.
- **BAD**: `Int`
- **GOOD**: `BigInt` (or `String` if you don't need math operations)

```prisma
model Product {
  id          BigInt   @id // Matches Shopify's ID
  shop        String
  title       String
  // ...
  @@index([shop]) // Always index by shop for multi-tenancy
}
```

### Multi-tenancy
Every query MUST filter by `shop`. This is non-negotiable for security.
- **Tip**: Use Prisma Middleware or Extensions to enforce this, or just be disciplined in your Service layer.

## 4. Migrations Workflow

NEVER use `prisma db push` in production.

- **Development**:
  ```bash
  npx prisma migrate dev --name init_tables
  ```
- **Production (CI/CD)**:
  ```bash
  npx prisma migrate deploy
  ```

## 5. Performance Optimization
- Ensure efficient queries and consider using pagination for large datasets.
- Utilize Prisma's built-in features for performance monitoring and optimization.