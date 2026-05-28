---
name: epic-database
description: Use this skill when you need to design database schemas, create migrations, and optimize queries with Prisma, SQLite, and LiteFS.
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
	},
})

// ❌ Avoid - Fetching everything
const user = await prisma.user.findUnique({
	where: { id: userId },
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

// ❌ Avoid - Over-optimizing before measuring
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
  content String
  
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  owner   User   @relation(fields: [ownerId], references: [id])
  ownerId String
  
  @@index([ownerId])
  @@index([ownerId, updatedAt])
}
```

### CUID2 for IDs

Epic Stack uses CUID2 to generate unique IDs.

**Advantages:**
- Globally unique
- Sortable
- Secure (no exposed information)
- URL-friendly

**Example:**
```prisma
model User {
  id String @id @default(cuid())
}
```

### Timestamps

**Standard fields:**
```prisma
model User {
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### Relationships

**One-to-Many:**
```prisma
model User {
  id    String @id @default(cuid())
  notes Note[]
}

model Note {
  id      String @id @default(cuid())
  owner   User   @relation(fields: [ownerId], references: [id])
  ownerId String
  
  @@index([ownerId])
}
```

**One-to-One:**
```prisma
model User {
  id      String  @id @default(cuid())
  image   UserImage?
}

model UserImage {
  id        String @id @default(cuid())
  user      User   @relation(fields: [userId], references: [id])
  userId    String @unique
}
```

**Many-to-Many:**
```prisma
model User {
  id    String @id @default(cuid())
  roles Role[]
}

model Role {
  id    String @id @default(cuid())
  users User[]
}
```

### Indexes

**Create indexes:**
```prisma
model Note {
  id      String @id @default(cuid())
  ownerId String
  updatedAt DateTime
  
  @@index([ownerId])
  @@index([ownerId, updatedAt])
}
```

**Best practices:**
- Index foreign keys
- Index fields used in `where` frequently
- Index fields used in `orderBy`
- Use composite indexes for complex queries

### Cascade Delete

**Configure cascade:**
```prisma
model User {
  id    String @id @default(cuid())
  notes Note[]
}

model Note {
  id      String @id @default(cuid())
  owner   User   @relation(fields: [ownerId], references: [id], onDelete: Cascade)
  ownerId String
}
```

### Migrations

**Create migration:**
```bash
npx prisma migrate dev --name add_user_field
```

**Apply migrations in production:**
```bash
npx prisma migrate deploy
```

**Automatic migrations:**
Migrations are automatically applied on deploy via `litefs.yml`.

**"Widen then Narrow" strategy for zero-downtime:**

1. **Widen app** - App accepts A or B
2. **Widen db** - DB provides A and B, app writes to both
3. **Narrow app** - App only uses B
4. **Narrow db** - DB only provides B

### Prisma Client

**Import Prisma Client:**
```typescript
import { prisma } from '#app/utils/db.server.ts'
```

**Basic query:**
```typescript
const user = await prisma.user.findUnique({
	where: { id: userId },
})
```

**Specific select:**
```typescript
const user = await prisma.user.findUnique({
	where: { id: userId },
	select: {
		id: true,
		email: true,
		username: true,
	},
})
```

**Include relations:**
```typescript
const user = await prisma.user.findUnique({
	where: { id: userId },
	include: {
		notes: {
			select: {
				id: true,
				title: true,
			},
			orderBy: { updatedAt: 'desc' },
		},
		roles: true,
	},
})
```

### Transactions

**Use transactions:**
```typescript
await prisma.$transaction(async (tx) => {
	const user = await tx.user.create({
		data: {
			email,
			username,
			roles: { connect: { name: 'user' } },
		},
	})
	
	await tx.note.create({
		data: {
			title: 'Welcome',
			content: 'Welcome to the app!',
			ownerId: user.id,
		},
	})
	
	return user
})
```

### SQLite con LiteFS

**Multi-region with LiteFS:**
- Only the primary instance can write
- Replicas can only read
- Writes are automatically replicated

**Check primary instance:**
```typescript
import { ensurePrimary, getInstanceInfo } from '#app/utils/litefs.server.ts'

export async function action({ request }: Route.ActionArgs) {
	await ensurePrimary()
	await prisma.user.create({ data: { /* ... */ } })
}
```

### Seed Scripts

**Create seed:**
```typescript
// prisma/seed.ts
import { prisma } from '#app/utils/db.server.ts'

async function seed() {
	await prisma.role.createMany({
		data: [
			{ name: 'user', description: 'Standard user' },
			{ name: 'admin', description: 'Administrator' },
		],
	})
	
	const user = await prisma.user.create({
		data: {
			email: 'user@example.com',
			username: 'testuser',
			roles: { connect: { name: 'user' } },
		},
	})
	
	console.log('Seed complete!')
}

seed()
	.catch((e) => {
		console.error(e)
		process.exit(1)
	})
	.finally(async () => {
		await prisma.$disconnect()
	})
```

### Query Optimization

**Guidelines (pragmatic approach):**
- Use `select` to fetch only needed fields
- Use selective `include` - only include relations you actually use
- Index fields used in `where` and `orderBy` - but only if queries are slow
- Use composite indexes for complex queries - when you have a real performance problem
- Avoid `select: true` (fetches everything) - be explicit about what you need
- Measure first, optimize second - don't pre-optimize

### Common mistakes to avoid

- ❌ **Fetching unnecessary data**: Use `select` to fetch only what you need.
- ❌ **Over-optimizing prematurely**: Measure first, then optimize.
- ❌ **Not using indexes when needed**: Index foreign keys and fields used in frequent queries.
- ❌ **N+1 queries**: Use `include` to fetch relations in a single query when you need them.
- ❌ **Not using transactions for related operations**: Always use transactions when multiple operations must be atomic.
- ❌ **Writing from replicas**: Verify `ensurePrimary()` before writes in production.
- ❌ **Breaking migrations without strategy**: Use "widen then narrow" for zero-downtime.
- ❌ **Not validating data before inserting**: Always validate with Zod before create/update.
- ❌ **Forgetting `onDelete` in relations**: Explicitly decide what to do when parent is deleted.
- ❌ **Not using CUID2**: Epic Stack uses CUID2 by default.
- ❌ **Not closing Prisma Client**: Ensure Prisma Client is closed in scripts.
- ❌ **Complex queries when simple ones work**: Prefer simple, readable queries.

## References

- [Epic Stack Database Docs](../epic-stack/docs/database.md)
- [Epic Web Principles](https://www.epicweb.dev/principles)
- [Prisma Documentation](https://www.prisma.io/docs)
- [LiteFS Documentation](https://fly.io/docs/litefs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)