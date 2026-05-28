# Drizzle ORM Setup for Neon

## Installation

```bash
npm install drizzle-orm @neondatabase/serverless
npm install -D drizzle-kit
```

## Configuration

### 1. Create `drizzle.config.ts`

```typescript
import type { Config } from 'drizzle-kit';

export default {
  schema: './src/db/schema.ts',
  out: './drizzle',
  driver: 'pg',
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
} satisfies Config;
```

### 2. Database Connection (`src/db/index.ts`)

```typescript
import { drizzle } from 'drizzle-orm/neon-http';
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql);
```

### 3. Schema Definition (`src/db/schema.ts`)

```typescript
import { pgTable, text, timestamp, boolean } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: text('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name'),
  passwordHash: text('password_hash'),
  emailVerified: boolean('email_verified').default(false),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});

export const sessions = pgTable('sessions', {
  id: text('id').primaryKey(),
  userId: text('user_id').references(() => users.id, { onDelete: 'cascade' }).notNull(),
  expiresAt: timestamp('expires_at').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});

export const chatHistory = pgTable('chat_history', {
  id: text('id').primaryKey(),
  userId: text('user_id').references(() => users.id, { onDelete: 'cascade' }).notNull(),
  message: text('message').notNull(),
  response: text('response').notNull(),
  metadata: jsonb('metadata'),
  createdAt: timestamp('created_at').defaultNow(),
});
```

## CRUD Operations

### Insert
```typescript
import { db } from './db';
import { users } from './db/schema';

await db.insert(users).values({
  id: crypto.randomUUID(),
  email: 'user@example.com',
  name: 'John Doe',
  passwordHash: hashedPassword,
});
```

### Select
```typescript
import { eq } from 'drizzle-orm';

// Find by email
const user = await db.select().from(users).where(eq(users.email, 'user@example.com'));

// Get all
const all Users = await db.select().from(users);
```

### Update
```typescript
await db.update(users)
  .set({ emailVerified: true })
  .where(eq(users.email, 'user@example.com'));
```

### Delete
```typescript
await db.delete(users).where(eq(users.id, userId));
```

## Joins

```typescript
import { chatHistory, users } from './db/schema';

const conversationsWithUsers = await db
  .select({
    id: chatHistory.id,
    message: chatHistory.message,
    response: chatHistory.response,
    userEmail: users.email,
    userName: users.name,
  })
  .from(chatHistory)
  .leftJoin(users, eq(chatHistory.userId, users.id));
```

## Transactions

```typescript
await db.transaction(async (tx) => {
  const user = await tx.insert(users).values({
    id: userId,
    email: 'user@example.com',
  }).returning();
  
  await tx.insert(sessions).values({
    id: crypto.randomUUID(),
    userId: user[0].id,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
  });
});
```

## Type Safety

Drizzle provides full TypeScript types:

```typescript
import { InferModel } from 'drizzle-orm';
import { users } from './db/schema';

type User = InferModel<typeof users>;
type NewUser = InferModel<typeof users, 'insert'>;

const newUser: NewUser = {
  id: crypto.randomUUID(),
  email: 'test@example.com',
  // TypeScript ensures all required fields are present
};
```

## Query Builder

```typescript
import { and, or, gt, lt, eq, like, desc } from 'drizzle-orm';

// Complex where clauses
const recentChats = await db
  .select()
  .from(chatHistory)
  .where(
    and(
      eq(chatHistory.userId, userId),
      gt(chatHistory.createdAt, new Date(Date.now() - 7 * 24 * 60 * 60 * 1000))
    )
  )
  .orderBy(desc(chatHistory.createdAt))
  .limit(20);
```

## Pagination

```typescript
async function getChats(page: number, pageSize: number) {
  const offset = (page - 1) * pageSize;
  
  return await db
    .select()
    .from(chatHistory)
    .limit(pageSize)
    .offset(offset);
}
```

## Best Practices

1. **Use transactions** for related operations
2. **Always use TypeScript** types for safety
3. **Use `.returning()`** to get inserted/updated data
4. **Leverage query builder** for complex queries
5. **Use indexes** on frequently queried columns
