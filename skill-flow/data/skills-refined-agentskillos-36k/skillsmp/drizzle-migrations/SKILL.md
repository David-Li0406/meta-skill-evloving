---
name: drizzle-migrations
description: Comprehensive guide for Drizzle ORM database migrations with PostgreSQL. Use when adding/modifying database columns, creating migrations, updating schemas, or working with Drizzle schema definitions. Includes migration workflows (push vs migrate), column type reference, schema patterns, and safe migration practices.
---

# Drizzle Migrations

Complete guide for managing database schema changes with Drizzle ORM and PostgreSQL.

## Quick Start

1. **Update schema** - Modify your schema file (e.g., `src/db/schema/league.schema.ts`)
2. **Generate migration** - Run `npx drizzle-kit generate`
3. **Review SQL** - Check generated migration file
4. **Apply changes** - Run `npx drizzle-kit push` (dev) or `npx drizzle-kit migrate` (prod)
5. **Verify** - Test the changes in your application

## Migration Workflow

See [migration-workflow.md](references/migration-workflow.md) for complete process including:

- Step-by-step migration guide
- Push vs Migrate decision tree
- Handling existing data
- Rollback strategies
- Troubleshooting common errors
- Best practices

**Key decision:** Use `push` for development (fast iteration), `migrate` for production (version control).

## Column Types

See [column-types.md](references/column-types.md) for all Drizzle column types:

- **Text:** `text()`, `varchar()`, `char()`
- **Numeric:** `integer()`, `bigint()`, `decimal()`, `real()`
- **Boolean:** `boolean()`
- **Date/Time:** `timestamp()`, `date()`, `time()`
- **UUID:** `uuid()`
- **JSON:** `json()`, `jsonb()`
- **Arrays:** `array()`
- **Enums:** `pgEnum()`

**Common modifiers:** `.notNull()`, `.default()`, `.unique()`, `.primaryKey()`, `.references()`

## Schema Patterns

See [schema-patterns.md](references/schema-patterns.md) for reusable patterns:

- Timestamps (createdAt/updatedAt)
- Soft deletes
- Foreign keys with cascade
- Indexes (single and multi-column)
- Unique constraints
- Enums
- JSON fields
- Self-referencing tables
- Many-to-many junction tables
- Audit trails
- Versioning

## Common Tasks

### Adding a Column

```typescript
// 1. Update schema
export const organizations = pgTable("organizations", {
    // existing columns...
    newColumn: integer("new_column").default(0).notNull(),
})

// 2. Generate migration
// npx drizzle-kit generate

// 3. Apply
// npx drizzle-kit push
```

### Adding a NOT NULL Column

**Always provide a default for existing rows:**

```typescript
requiredField: text("required_field").default("default_value").notNull()
```

### Creating an Index

```typescript
export const users = pgTable("users", {
    email: text("email").notNull(),
}, (table) => ({
    emailIdx: index("email_idx").on(table.email),
}))
```

### Adding a Foreign Key

```typescript
userId: uuid("user_id")
    .references(() => users.id, { onDelete: "cascade" })
    .notNull()
```

## Safety Checklist

Before running migrations:

- [ ] Reviewed generated SQL
- [ ] Provided defaults for NOT NULL columns
- [ ] Tested on development database
- [ ] Backed up production database (if applicable)
- [ ] Verified no data loss will occur
- [ ] Checked for constraint violations
- [ ] Planned rollback strategy

## Development vs Production

**Development (drizzle-kit push):**
- Fast iteration
- No migration files
- Direct schema sync
- Good for prototyping

**Production (drizzle-kit migrate):**
- Version controlled migrations
- Rollback support
- Team collaboration
- Audit trail

## Troubleshooting

**"relation already exists"**
- Migration already applied
- Check migration history

**"violates not-null constraint"**
- Missing default value
- Existing NULL data

**"column type mismatch"**
- Incompatible type change
- Transform data first

See [migration-workflow.md](references/migration-workflow.md) for detailed troubleshooting.

## Best Practices

1. **Small migrations** - One logical change per migration
2. **Review SQL** - Always check generated statements
3. **Test first** - Run on development before production
4. **Backup** - Always backup before major changes
5. **Defaults** - Provide defaults for NOT NULL columns
6. **Indexes** - Add indexes for frequently queried columns
7. **Foreign keys** - Use cascade deletes appropriately
8. **Timestamps** - Include createdAt/updatedAt on all tables
