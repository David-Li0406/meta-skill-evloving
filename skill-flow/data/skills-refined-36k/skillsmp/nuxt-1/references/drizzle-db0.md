# Database with Drizzle ORM and db0

**Check if installed:** Look for `drizzle-orm` and optionally `db0` in package.json before using.

## Overview

Drizzle ORM is a TypeScript-first ORM. In Nuxt, it's commonly used with Nitro's `db0` for database access.

## Setup

### Database Configuration

```typescript
// server/database/index.ts
import { drizzle } from "drizzle-orm/better-sqlite3"
import Database from "better-sqlite3"

const sqlite = new Database("sqlite.db")
export const db = drizzle(sqlite)
```

### Schema Definition

```typescript
// server/database/schema.ts
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core"

export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  createdAt: integer("created_at", { mode: "timestamp" }).$defaultFn(
    () => new Date(),
  ),
})

export const posts = sqliteTable("posts", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  title: text("title").notNull(),
  content: text("content"),
  authorId: integer("author_id").references(() => users.id),
  createdAt: integer("created_at", { mode: "timestamp" }).$defaultFn(
    () => new Date(),
  ),
})
```

## CRUD Operations

### Insert

```typescript
// server/api/users.post.ts
import { db } from "~/server/database"
import { users } from "~/server/database/schema"

export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  const [user] = await db
    .insert(users)
    .values({
      name: body.name,
      email: body.email,
    })
    .returning()

  return user
})
```

### Select

```typescript
// server/api/users.get.ts
import { db } from "~/server/database"
import { users } from "~/server/database/schema"
import { eq } from "drizzle-orm"

export default defineEventHandler(async () => {
  // Get all users
  const allUsers = await db.select().from(users)

  // Get user by id
  const user = await db.select().from(users).where(eq(users.id, 1))

  // Get with specific columns
  const userEmails = await db
    .select({
      email: users.email,
      name: users.name,
    })
    .from(users)

  return allUsers
})
```

### Update

```typescript
import { db } from "~/server/database"
import { users } from "~/server/database/schema"
import { eq } from "drizzle-orm"

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id")
  const body = await readBody(event)

  const [updated] = await db
    .update(users)
    .set({ name: body.name })
    .where(eq(users.id, Number(id)))
    .returning()

  return updated
})
```

### Delete

```typescript
import { db } from "~/server/database"
import { users } from "~/server/database/schema"
import { eq } from "drizzle-orm"

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id")

  await db.delete(users).where(eq(users.id, Number(id)))

  return { success: true }
})
```

## Queries

### With Joins

```typescript
import { db } from "~/server/database"
import { users, posts } from "~/server/database/schema"
import { eq } from "drizzle-orm"

export default defineEventHandler(async () => {
  const usersWithPosts = await db
    .select()
    .from(users)
    .leftJoin(posts, eq(users.id, posts.authorId))

  return usersWithPosts
})
```

### Relational Queries

```typescript
// Define relations
import { relations } from "drizzle-orm"

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}))

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}))

// Query with relations
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true,
  },
})
```

### Filtering

```typescript
import { eq, ne, gt, gte, lt, lte, like, and, or } from "drizzle-orm"

// Equal
const user = await db.select().from(users).where(eq(users.id, 1))

// Greater than
const recentPosts = await db
  .select()
  .from(posts)
  .where(gt(posts.createdAt, new Date("2024-01-01")))

// Like (pattern matching)
const searchUsers = await db
  .select()
  .from(users)
  .where(like(users.name, "%john%"))

// Multiple conditions
const filtered = await db
  .select()
  .from(users)
  .where(
    and(eq(users.active, true), gt(users.createdAt, new Date("2024-01-01"))),
  )
```

### Ordering and Limiting

```typescript
import { desc, asc } from "drizzle-orm"

const latestPosts = await db
  .select()
  .from(posts)
  .orderBy(desc(posts.createdAt))
  .limit(10)

const paginatedUsers = await db
  .select()
  .from(users)
  .orderBy(asc(users.name))
  .limit(20)
  .offset(40)
```

## Transactions

```typescript
export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  const result = await db.transaction(async (tx) => {
    const [user] = await tx
      .insert(users)
      .values({
        name: body.name,
        email: body.email,
      })
      .returning()

    const [post] = await tx
      .insert(posts)
      .values({
        title: body.postTitle,
        authorId: user.id,
      })
      .returning()

    return { user, post }
  })

  return result
})
```

## Migrations

### Generate Migration

```bash
npx drizzle-kit generate
```

Database type is specified in `drizzle.config.ts`, not the command.

### Run Migration

```typescript
// server/database/migrate.ts
import { migrate } from "drizzle-orm/better-sqlite3/migrator"
import { db } from "./index"

migrate(db, { migrationsFolder: "./drizzle" })
```

## Type Safety

Drizzle provides full TypeScript type inference:

```typescript
// Types are inferred automatically
const users = await db.select().from(users)
// users: { id: number; name: string; email: string; createdAt: Date }[]

// Partial selects are typed too
const names = await db.select({ name: users.name }).from(users)
// names: { name: string }[]
```

## Using with db0 (Nitro)

```typescript
// server/database/index.ts
import { drizzle } from "drizzle-orm/d1"

export default defineNitroPlugin(() => {
  // Access db0 database
  const db = drizzle(useDatabase())

  return {
    provide: {
      db,
    },
  }
})

// Usage in API routes
export default defineEventHandler(async (event) => {
  const { $db } = event.context
  const users = await $db.select().from(users)
  return users
})
```
