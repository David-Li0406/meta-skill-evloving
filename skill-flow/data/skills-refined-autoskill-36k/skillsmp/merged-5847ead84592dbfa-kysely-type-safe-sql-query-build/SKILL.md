---
name: kysely-type-safe-sql-query-builder
description: Use this skill when you need to build type-safe SQL queries with Kysely, ensuring full TypeScript inference from schema to queries, including migrations and transactions.
---

# Kysely - Type-Safe SQL Query Builder

Kysely is a type-safe TypeScript SQL query builder that provides end-to-end type safety from database schema to query results. Unlike ORMs, it generates plain SQL and gives you full control while maintaining perfect TypeScript inference.

## Key Features
- Complete type inference (schema → queries → results)
- Zero runtime overhead (compiles to SQL)
- Database-agnostic (PostgreSQL, MySQL, SQLite)
- Migration system included
- Plugin ecosystem (CTEs, JSON, geospatial)
- Raw SQL integration when needed

## Installation
```bash
npm install kysely
# Database driver (choose one)
npm install pg              # PostgreSQL
npm install mysql2          # MySQL
npm install better-sqlite3  # SQLite
```

## Quick Start

### 1. Define Database Schema Types
```typescript
import { Generated, Selectable, Insertable, Updateable } from 'kysely';

// Table interface (all columns)
interface UserTable {
  id: Generated<number>;
  email: string;
  name: string | null;
  created_at: Generated<Date>;
  updated_at: Date;
}

interface PostTable {
  id: Generated<number>;
  user_id: number;
  title: string;
  content: string;
  published: Generated<boolean>;
  created_at: Generated<Date>;
}

// Database interface
interface Database {
  users: UserTable;
  posts: PostTable;
}

// Type-safe query result types
type User = Selectable<UserTable>;
type NewUser = Insertable<UserTable>;
type UserUpdate = Updateable<UserTable>;
```

### 2. Create Database Instance
```typescript
import { Kysely, PostgresDialect } from 'kysely';
import { Pool } from 'pg';

const db = new Kysely<Database>({
  dialect: new PostgresDialect({
    pool: new Pool({
      host: process.env.DB_HOST,
      database: process.env.DB_NAME,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      max: 10,
    }),
  }),
});
```

### 3. Type-Safe Queries
```typescript
// SELECT with full type inference
const users = await db
  .selectFrom('users')
  .select(['id', 'email', 'name'])
  .where('created_at', '>', new Date('2024-01-01'))
  .execute();

// INSERT with type checking
const newUser: NewUser = {
  email: 'alice@example.com',
  name: 'Alice',
  updated_at: new Date(),
};

const inserted = await db
  .insertInto('users')
  .values(newUser)
  .returningAll()
  .executeTakeFirstOrThrow();

// UPDATE
await db
  .updateTable('users')
  .set({ name: 'Alice Updated', updated_at: new Date() })
  .where('id', '=', 1)
  .execute();

// DELETE
await db
  .deleteFrom('users')
  .where('email', 'like', '%@spam.com')
  .execute();
```

## Advanced Query Patterns

### Joins with Type Safety
```typescript
// INNER JOIN
const usersWithPosts = await db
  .selectFrom('users')
  .innerJoin('posts', 'posts.user_id', 'users.id')
  .select(['users.id', 'users.name', 'posts.title', 'posts.content'])
  .execute();

// LEFT JOIN with null handling
const usersWithOptionalPosts = await db
  .selectFrom('users')
  .leftJoin('posts', 'posts.user_id', 'users.id')
  .select(['users.id', 'users.email', 'posts.title'])
  .execute();
```

### Aggregations and Grouping
```typescript
const stats = await db
  .selectFrom('posts')
  .select([
    'user_id',
    db.fn.count<number>('id').as('post_count'),
    db.fn.avg<number>('views').as('avg_views'),
  ])
  .groupBy('user_id')
  .having(db.fn.count('id'), '>', 5)
  .execute();
```

### Subqueries
```typescript
const usersWithPostCount = await db
  .selectFrom('users')
  .select([
    'users.id',
    'users.name',
    (eb) =>
      eb
        .selectFrom('posts')
        .select(eb.fn.count<number>('id').as('count'))
        .whereRef('posts.user_id', '=', 'users.id')
        .as('post_count'),
  ])
  .execute();
```

### Common Table Expressions (CTEs)
```typescript
const result = await db
  .with('popular_posts', (db) =>
    db
      .selectFrom('posts')
      .select(['id', 'user_id', 'title'])
      .where('views', '>', 1000)
  )
  .selectFrom('popular_posts')
  .selectAll()
  .execute();
```

## Migrations
### Migration Setup
```typescript
import { Kysely, Migrator, FileMigrationProvider } from 'kysely';
import { promises as fs } from 'fs';
import * as path from 'path';

const migrator = new Migrator({
  db,
  provider: new FileMigrationProvider({
    fs,
    path,
    migrationFolder: path.join(__dirname, 'migrations'),
  }),
});

// Run all pending migrations
async function migrateToLatest() {
  const { error, results } = await migrator.migrateToLatest();
}
```

### Migration Files
```typescript
// migrations/001_create_users.ts
import { Kysely, sql } from 'kysely';

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable('users')
    .addColumn('id', 'serial', (col) => col.primaryKey())
    .addColumn('email', 'varchar(255)', (col) => col.notNull().unique())
    .addColumn('name', 'varchar(255)')
    .addColumn('created_at', 'timestamp', (col) =>
      col.defaultTo(sql`CURRENT_TIMESTAMP`).notNull()
    )
    .execute();
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('users').execute();
}
```

## Transactions
### Basic Transactions
```typescript
await db.transaction().execute(async (trx) => {
  await trx
    .insertInto('users')
    .values({ email: 'alice@example.com', name: 'Alice', updated_at: new Date() })
    .execute();

  await trx
    .insertInto('posts')
    .values({ user_id: 1, title: 'First Post', content: 'Hello' })
    .execute();
});
```

## Best Practices
1. **Define schema types first** - Use `Generated`, `Selectable`, `Insertable`, `Updateable`
2. **Use kysely-codegen** - Generate types from existing databases
3. **Leverage type inference** - Let TypeScript infer result types
4. **Use transactions** - For multi-step operations
5. **Raw SQL when needed** - Don't fight the query builder
6. **Paginate large results** - Use LIMIT/OFFSET or cursor-based
7. **Index frequently queried columns** - Performance is your responsibility
8. **Test migrations** - Both up and down
9. **Use CTEs for readability** - Complex queries become maintainable
10. **Connection pooling** - Configure database pool appropriately

## Resources
- **Documentation**: https://kysely.dev
- **GitHub**: https://github.com/kysely-org/kysely
- **Discord**: https://discord.gg/kysely
- **kysely-codegen**: https://github.com/RobinBlomberg/kysely-codegen
- **Playground**: https://kysely-org.github.io/kysely-playground/

## Related Skills
When using Kysely, consider these complementary skills:
- **typescript-core**: TypeScript type system, advanced patterns, and tsconfig optimization
- **database-migration**: Safe schema evolution patterns for production databases
- **Node.js backend**: Server setup, connection pooling, and database configuration