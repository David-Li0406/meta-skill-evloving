---
name: prisma-orm-development
description: Use this skill when you need to implement type-safe database access with Prisma ORM in TypeScript, covering schema design, migrations, and best practices.
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
npx prisma db seed       # Run seed script
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

  @@index([email])
  @@map("users") // Custom table name
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
model Example {
  // Scalar types
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

## Function Design

- Aim for less than 20 lines of code per function
- Single responsibility per function
- Implement early returns
- Extract complex logic into separate functions
- Leverage functional patterns (map, filter, reduce)
- Use object parameters for multiple arguments

## Data & Error Handling

- Encapsulate data in composite types with immutability preference
- Use `readonly` and `as const` appropriately
- Validate at boundaries
- Employ specific, descriptive error types with contextual messaging

## Quality Standards

- Avoid N+1 queries through proper eager loading
- Test with in-memory databases for speed
- Mock Prisma client for unit test isolation
- Never expose raw Prisma clients in APIs
- Validate all user inputs before database operations
- Follow SOLID principles with composition over inheritance