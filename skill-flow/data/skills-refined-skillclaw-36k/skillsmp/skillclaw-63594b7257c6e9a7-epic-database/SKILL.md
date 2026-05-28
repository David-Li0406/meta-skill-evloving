---
name: epic-database
description: Use this skill when you need to design and manage a database schema with Prisma, SQLite, and LiteFS in the Epic Stack.
---

# Epic Stack: Database

## When to use this skill

Use this skill when you need to:
- Design database schema with Prisma
- Create migrations
- Work with SQLite and LiteFS
- Optimize queries and performance
- Create seed scripts
- Work with multi-region deployments
- Manage backups and restores

## Patterns and conventions

### Database Philosophy

Following Epic Web principles:

**Do as little as possible** - Only fetch the data you actually need. Use `select` to fetch specific fields instead of entire models. Avoid over-fetching data "just in case" - fetch what you need, when you need it.

**Pragmatism over purity** - Optimize queries when there's a measurable benefit, but don't over-optimize prematurely. Simple, readable queries are often better than complex optimized ones. Add indexes when queries are slow, not before.

**Example - Fetch only what you need:**
```typescript
// ✅ Good - Fetch only needed fields
const user = await prisma.user.findUnique({
	where: { id: userId },
	select: {
		id: true,
		username: true,
		name: true,
		// Only fetch what you actually use
	},
})

// ❌ Avoid - Fetching everything
const user = await prisma.user.findUnique({
	where: { id: userId },
	// Fetches all fields including password hash, email, etc.
})
```

**Example - Pragmatic optimization:**
```typescript
// ✅ Good - Simple query first, optimize if needed
const notes = await prisma.note.findMany({
	where: { ownerId: userId },
	select: { id: true, title: true, updatedAt: true },
	orderBy: { updatedAt: 'desc' },
	take: 20,
})

// Only add indexes if this query is actually slow
// Don't pre-optimize

// ❌ Avoid - Over-optimizing before measuring
// Adding complex indexes, joins, etc. before knowing if it's needed
```

### Prisma Schema

Epic Stack uses Prisma with SQLite as the database.

**Basic configuration:**
```prisma
// prisma/schema.prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["typedSql"]
}

datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}
```

**Basic model:**
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  username  String   @unique
  name      String?
  
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  notes     Note[]
  roles     Role[]
}

model Note {
  id      String @id @default(cuid())
  title   String
  content String?
  ownerId String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```