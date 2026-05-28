# Database Service

A PostgreSQL database layer using **Drizzle ORM** with **Effect-TS** integration for type-safe, functional database operations.

## Libraries

| Package                      | Purpose                                                 |
| ---------------------------- | ------------------------------------------------------- |
| `drizzle-orm`                | Type-safe ORM with SQL-like query builder               |
| `drizzle-orm/pg-core`        | PostgreSQL column types and table definitions           |
| `@effect/sql-pg`             | Effect-native PostgreSQL client with connection pooling |
| `@effect-aws/sql-drizzle/Pg` | Bridge between Effect SQL and Drizzle ORM               |
| `@neondatabase/serverless`   | Serverless-compatible PostgreSQL driver (optional)      |
| `@paralleldrive/cuid2`       | Collision-resistant unique ID generation                |
| `drizzle-kit`                | CLI for migrations and schema management                |

## File Structure

```
lib/services/db/
├── live-layer.ts    # Effect service layer definition
├── schema.ts        # Drizzle table definitions + relations
├── types.ts         # Effect Schema validators for JSONB fields
└── migrations/      # Drizzle migration files (optional)
```

## Scaffolding from Scratch

### 1. Install Dependencies

```bash
npm install drizzle-orm @effect/sql-pg @effect-aws/sql-drizzle effect @paralleldrive/cuid2
npm install -D drizzle-kit
```

### 2. Create the Schema (`lib/services/db/schema.ts`)

```typescript
import { pgTable, text, timestamp, boolean, jsonb, real, uniqueIndex } from 'drizzle-orm/pg-core'
import { relations } from 'drizzle-orm'
import { createId } from '@paralleldrive/cuid2'

// Example: User table
export const user = pgTable('user', {
  id: text('id')
    .primaryKey()
    .$defaultFn(() => createId()),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  role: text('role', { enum: ['USER', 'ADMIN'] })
    .notNull()
    .default('USER'),
  createdAt: timestamp('createdAt').notNull().defaultNow(),
  updatedAt: timestamp('updatedAt')
    .notNull()
    .defaultNow()
    .$onUpdate(() => new Date())
})

// Example: Post table with foreign key
export const post = pgTable(
  'post',
  {
    id: text('id')
      .primaryKey()
      .$defaultFn(() => createId()),
    title: text('title').notNull(),
    content: text('content'),
    status: text('status', { enum: ['DRAFT', 'PUBLISHED', 'ARCHIVED'] })
      .notNull()
      .default('DRAFT'),
    metadata: jsonb()
      .$type<{ tags: string[]; readTime: number }>()
      .default({ tags: [], readTime: 0 }),
    userId: text('userId')
      .notNull()
      .references(() => user.id, { onDelete: 'cascade' }),
    createdAt: timestamp('createdAt').notNull().defaultNow(),
    updatedAt: timestamp('updatedAt')
      .notNull()
      .defaultNow()
      .$onUpdate(() => new Date())
  },
  table => [uniqueIndex('user_title_unique_idx').on(table.userId, table.title)]
)

// Relations for query builder
export const userRelations = relations(user, ({ many }) => ({
  posts: many(post)
}))

export const postRelations = relations(post, ({ one }) => ({
  user: one(user, {
    fields: [post.userId],
    references: [user.id]
  })
}))

// Derived types
export type User = typeof user.$inferSelect
export type InsertUser = typeof user.$inferInsert
export type Post = typeof post.$inferSelect
export type InsertPost = typeof post.$inferInsert
```

### 3. Create Effect Schema Validators (`lib/services/db/types.ts`)

For JSONB fields, use Effect Schema for runtime validation:

```typescript
import { Schema } from 'effect'

export const PostMetadataSchema = Schema.Struct({
  tags: Schema.Array(Schema.String),
  readTime: Schema.Number.pipe(Schema.nonNegative())
})

export type PostMetadata = typeof PostMetadataSchema.Type

// Validate at runtime
export const parseMetadata = Schema.decodeUnknown(PostMetadataSchema)
```

### 4. Create the Effect Service Layer (`lib/services/db/live-layer.ts`)

```typescript
import * as PgDrizzle from '@effect-aws/sql-drizzle/Pg'
import { PgClient } from '@effect/sql-pg'
import { Config, Effect, Layer } from 'effect'
import { NodeContext } from '@effect/platform-node'
import * as schema from './schema'

// PostgreSQL connection layer
const PgLive = PgClient.layerConfig({
  url: Config.redacted('DATABASE_URL'),
  ssl: Config.succeed(true)
})

// Drizzle service with full schema typing
export class DbLive extends Effect.Service<DbLive>()('@app/DbLive', {
  dependencies: [PgLive],
  effect: PgDrizzle.make<typeof schema>({
    schema: schema
  })
}) {}

// Combined layer for external use
export const DbLayer = Layer.merge(DbLive.Default, PgLive).pipe(Layer.provide(NodeContext.layer))
```

### 5. Create Retry Policy (`lib/utils/db-retry-policy.ts`)

```typescript
import { Schedule, Effect } from 'effect'

// Base policy: 500ms, 1s, 2s backoff (3 retries max)
export const dbRetryPolicy = Schedule.exponential('500 millis', 2.0).pipe(
  Schedule.intersect(Schedule.recurs(3))
)

// Policy with warning telemetry on each retry
export const dbRetryPolicyWithWarning = (operation: string, context?: Record<string, unknown>) =>
  Schedule.exponential('500 millis', 2.0).pipe(
    Schedule.intersect(Schedule.recurs(3)),
    Schedule.tapInput((error: { _tag: string; message: string }) =>
      Effect.logWarning(`Retry attempt for ${operation}`, { error, ...context })
    )
  )
```

### 6. Create Tagged Errors (`lib/core/errors.ts`)

```typescript
import { Data } from 'effect'

export class NotFoundError extends Data.TaggedError('NotFoundError')<{
  message: string
  entity: string
  id: string
}> {}

export class ValidationError extends Data.TaggedError('ValidationError')<{
  message: string
  field?: string
}> {}
```

### 7. Configure Drizzle Kit (`drizzle.config.ts`)

```typescript
import type { Config } from 'drizzle-kit'

export default {
  schema: './lib/services/db/schema.ts',
  out: './lib/services/db/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!
  }
} satisfies Config
```

### 8. Add npm Scripts

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  }
}
```

## Usage Patterns

### Basic Query

```typescript
import { Effect } from 'effect'
import { DbLive } from '@/lib/services/db/live-layer'
import { dbRetryPolicyWithWarning } from '@/lib/utils/db-retry-policy'
import * as schema from '@/lib/services/db/schema'
import { eq } from 'drizzle-orm'
import { NotFoundError } from '@/lib/core/errors'

export const getPostById = (postId: string) =>
  Effect.gen(function* () {
    yield* Effect.annotateCurrentSpan({ 'post.id': postId, operation: 'post.query' })

    const db = yield* DbLive

    const post = yield* db.query.post.findFirst({
      where: eq(schema.post.id, postId),
      with: { user: true }
    })

    if (!post) {
      return yield* new NotFoundError({
        message: `Post not found`,
        entity: 'post',
        id: postId
      })
    }

    yield* Effect.annotateCurrentSpan({ 'post.status': post.status })
    return post
  }).pipe(
    Effect.retry(dbRetryPolicyWithWarning('get-post', { postId })),
    Effect.withSpan('post.query.by-id')
  )
```

### Insert with Returning

```typescript
export const createPost = (data: Omit<schema.InsertPost, 'id'>) =>
  Effect.gen(function* () {
    const db = yield* DbLive

    const [post] = yield* db.insert(schema.post).values(data).returning()

    yield* Effect.annotateCurrentSpan({ 'post.id': post.id })
    return post
  }).pipe(Effect.retry(dbRetryPolicyWithWarning('create-post')), Effect.withSpan('post.create'))
```

### Transaction

```typescript
import { SqlClient } from '@effect/sql'

export const transferOwnership = (postId: string, newUserId: string) =>
  Effect.gen(function* () {
    const sql = yield* SqlClient.SqlClient
    const db = yield* DbLive

    return yield* sql.withTransaction(
      Effect.gen(function* () {
        // Verify new user exists
        const user = yield* db.query.user.findFirst({
          where: eq(schema.user.id, newUserId)
        })
        if (!user)
          return yield* new NotFoundError({
            message: 'User not found',
            entity: 'user',
            id: newUserId
          })

        // Update post
        const [updated] = yield* db
          .update(schema.post)
          .set({ userId: newUserId, updatedAt: new Date() })
          .where(eq(schema.post.id, postId))
          .returning()

        return updated
      })
    )
  }).pipe(
    Effect.retry(dbRetryPolicyWithWarning('transfer-ownership', { postId, newUserId })),
    Effect.withSpan('post.transfer-ownership')
  )
```

### Batch Delete

```typescript
export const deleteUserPosts = (userId: string) =>
  Effect.gen(function* () {
    const db = yield* DbLive

    return yield* db
      .delete(schema.post)
      .where(eq(schema.post.userId, userId))
      .returning({ id: schema.post.id })
  }).pipe(
    Effect.retry(dbRetryPolicyWithWarning('delete-user-posts', { userId })),
    Effect.withSpan('post.delete.by-user')
  )
```

## Best Practices

### 1. Always Use Retry Policy for DB Operations

Database operations can fail due to network issues, cold starts, or transient cloud infrastructure problems. Always wrap with retry:

```typescript
// Good
Effect.retry(dbRetryPolicyWithWarning('operation-name', { context }))

// Bad - no retry
db.query.post.findFirst(...)
```

### 2. Span Order: Retry BEFORE Span

The span should capture the total duration including all retries:

```typescript
// Correct
.pipe(
  Effect.retry(retryPolicy),     // 1. Retry first
  Effect.withSpan('operation'),  // 2. Span wraps retries
  Effect.tapError(reportError)   // 3. Report final failure
)

// Wrong - each retry creates a new span
.pipe(
  Effect.withSpan('operation'),
  Effect.retry(retryPolicy)
)
```

### 3. Annotate Spans with Context

Add relevant IDs and operation names to spans for debugging:

```typescript
yield *
  Effect.annotateCurrentSpan({
    operation: 'post.delete',
    'post.id': postId,
    'user.id': userId
  })
```

### 4. Use Tagged Errors

Create specific error types for different failure modes:

```typescript
export class PostNotFoundError extends Data.TaggedError('PostNotFoundError')<{
  message: string
  postId: string
}> {}

// Allows pattern matching in error handlers
Match.when('PostNotFoundError', () => ...)
```

### 5. CUID2 for Primary Keys

Use collision-resistant IDs instead of auto-increment:

```typescript
id: text('id')
  .primaryKey()
  .$defaultFn(() => createId())
```

Benefits:

- No ID conflicts in distributed systems
- IDs can be generated client-side
- No sequential enumeration attacks

### 6. Cascade Deletes for Foreign Keys

Ensure referential integrity with cascade rules:

```typescript
userId: text('userId')
  .notNull()
  .references(() => user.id, { onDelete: 'cascade' })
```

### 7. Auto-Update Timestamps

Use `$onUpdate` for automatic timestamp management:

```typescript
updatedAt: timestamp('updatedAt')
  .notNull()
  .defaultNow()
  .$onUpdate(() => new Date())
```

### 8. Effect Schema for JSONB Validation

Don't trust JSONB data from the database - validate at runtime:

```typescript
const rawMetadata = post.metadata
const metadata = yield * Schema.decodeUnknown(PostMetadataSchema)(rawMetadata)
```

## Environment Variables

| Variable       | Required | Description                  |
| -------------- | -------- | ---------------------------- |
| `DATABASE_URL` | Yes      | PostgreSQL connection string |

Example:

```
DATABASE_URL=postgresql://user:pass@host:5432/dbname?sslmode=require
```

## Serverless Considerations

For serverless environments (Vercel, AWS Lambda), consider using the Neon HTTP driver:

```typescript
import { neon } from '@neondatabase/serverless'
import { drizzle } from 'drizzle-orm/neon-http'

const sql = neon(process.env.DATABASE_URL!)
const db = drizzle(sql, { schema })
```

This avoids connection pooling issues in serverless contexts where connections may not be reused.
