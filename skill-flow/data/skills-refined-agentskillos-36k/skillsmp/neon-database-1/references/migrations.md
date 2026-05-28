# Migrations Guide for Drizzle + Neon

## Setup

Ensure `drizzle.config.ts` is configured:

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

## Migration Workflow

### 1. Generate Migration
```bash
npx drizzle-kit generate
```

This creates a migration file in `./drizzle/` based on schema changes.

### 2. Push to Database
```bash
npx drizzle-kit push
```

Applies migrations directly to database (dev/staging).

### 3. Run Migrations (Production)
```typescript
import { migrate } from 'drizzle-orm/neon-http/migrator';
import { db } from './db';

await migrate(db, { migrationsFolder: './drizzle' });
```

## Common Scenarios

### Adding a New Table
1. Add definition to `schema.ts`
2. Run `drizzle-kit generate`
3. Run `drizzle-kit push`

### Adding a Column
```typescript
// schema.ts - add new column
export const users = pgTable('users', {
  // ... existing columns
  avatarUrl: text('avatar_url'), // NEW
});
```

Then:
```bash
drizzle-kit generate
drizzle-kit push
```

### Renaming a Column
Use `.alter()` in migration:

```sql
-- Generated migration
ALTER TABLE users RENAME COLUMN name TO full_name;
```

### Adding an Index
```typescript
import { index } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  // columns...
}, (table) => ({
  emailIdx: index('email_idx').on(table.email),
}));
```

## Best Practices

1. **Never edit generated migrations** - regenerate instead
2. **Test migrations** on dev database first
3. **Backup production** before migrating
4. **Use introspect** to sync existing databases:
   ```bash
   drizzle-kit introspect
   ```
5. **Version control** migration files in git
