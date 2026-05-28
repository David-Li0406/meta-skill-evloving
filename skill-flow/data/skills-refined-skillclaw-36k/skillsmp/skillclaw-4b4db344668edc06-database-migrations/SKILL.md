---
name: database-migrations
description: Use this skill when you need to perform safe database migrations with zero-downtime strategies, ensuring backward compatibility and reversibility.
---

# Database Migrations

Change your schema without breaking production.

## When to Use This Skill

- Adding or modifying database tables
- Changing column types or constraints
- Creating indexes
- Data migrations or backfills
- Schema versioning

## Migration Principles

1. **Backwards Compatible**: Migrations should work with current AND previous code versions.
2. **Reversible**: Always include a rollback strategy.
3. **Atomic**: Each migration does one logical change.
4. **Tested**: Test migrations on a copy of production data.
5. **Documented**: Explain why, not just what.

## Safe Migration Patterns

### Adding a Column

```typescript
// ✅ Safe: Add nullable column (no lock on reads)
export async function up(db: Database) {
  await db.schema.alterTable('users', (table) => {
    table.string('phone').nullable();
  });
}

export async function down(db: Database) {
  await db.schema.alterTable('users', (table) => {
    table.dropColumn('phone');
  });
}
```

### Adding a NOT NULL Column

```typescript
// Migration 1: Add nullable column
export async function up(db: Database) {
  await db.schema.alterTable('users', (table) => {
    table.string('status').nullable();
  });
}

// Migration 2: Backfill data (after deployment)
export async function up(db: Database) {
  await db('users')
    .whereNull('status')
    .update({ status: 'active' });
}

// Migration 3: Add NOT NULL constraint (after verification)
export async function up(db: Database) {
  await db.schema.alterTable('users', (table) => {
    table.string('status').notNullable().alter();
  });
}
```

### Renaming a Column (Zero Downtime)

```typescript
// Migration 1: Add new column
export async function up(db: Database) {
  await db.schema.alterTable('users', (table) => {
    table.string('full_name');
  });
}

// Migration 2: Copy data
export async function up(db: Database) {
  await db.raw('UPDATE users SET full_name = name');
}

// Migration 3: Deploy code using full_name
// ... code changes ...

// Migration 4: Drop old column (after all code deployed)
export async function up(db: Database) {
  await db.schema.alterTable('users', (table) => {
    table.dropColumn('name');
  });
}
```

### Adding an Index (Safely)

```sql
-- PostgreSQL: Create index without blocking writes
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

## Zero-Downtime Migration Strategy

1. **Add new column** (nullable).
2. **Dual-write**: Write to both old and new columns.
3. **Backfill old data**.
4. **Switch reads** to the new column.
5. **Remove old column writes**.
6. **Drop old column**.