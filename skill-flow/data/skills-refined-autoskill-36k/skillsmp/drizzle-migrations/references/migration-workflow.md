# Drizzle Migration Workflow

## Safe Migration Process

### Step 1: Update Schema File

Modify your schema file (e.g., `src/db/schema/league.schema.ts`):

```typescript
export const organizations = pgTable("organizations", {
    id: uuid("id").primaryKey().defaultRandom(),
    name: text("name").notNull(),
    // Add new columns
    defaultHoles: integer("default_holes").default(18).notNull(),
    rotationStrategy: varchar("rotation_strategy", { length: 50 }).default("sequential").notNull(),
})
```

**Important:**
- Always provide default values for new NOT NULL columns
- Use appropriate column types (see column-types.md)
- Consider existing data when adding constraints

### Step 2: Generate Migration

```bash
npx drizzle-kit generate
```

This creates a new migration file in `drizzle/` directory with SQL statements.

**Review the generated SQL:**
- Check ALTER TABLE statements
- Verify default values
- Ensure no data loss

### Step 3: Choose Migration Method

**Option A: Push (Development)**
```bash
npx drizzle-kit push
```
- Applies changes directly to database
- No migration history
- Good for development/prototyping
- **Use when:** Iterating quickly, no production data

**Option B: Migrate (Production)**
```bash
npx drizzle-kit migrate
```
- Runs migration files in order
- Maintains migration history
- Rollback support
- **Use when:** Production deployments, team collaboration

### Step 4: Verify Changes

```typescript
// Test the new columns
const [org] = await db.select().from(organizations).limit(1)
console.log(org.defaultHoles) // Should show 18
console.log(org.rotationStrategy) // Should show "sequential"
```

## Common Migration Scenarios

### Adding a Column

```typescript
// Schema
newColumn: text("new_column").default("default_value")

// Generated SQL
ALTER TABLE "table_name" ADD COLUMN "new_column" text DEFAULT 'default_value';
```

### Adding a NOT NULL Column

```typescript
// ALWAYS provide a default for existing rows
requiredColumn: text("required_column").default("default").notNull()

// Generated SQL
ALTER TABLE "table_name" ADD COLUMN "required_column" text DEFAULT 'default' NOT NULL;
```

### Modifying a Column

```typescript
// Change type or constraints
// Note: Drizzle generates ALTER COLUMN statements
updatedColumn: integer("column_name").notNull() // was text before
```

### Renaming a Column

```typescript
// Drizzle doesn't auto-detect renames
// Manually edit migration file or use raw SQL
await db.execute(sql`ALTER TABLE "table_name" RENAME COLUMN "old_name" TO "new_name"`)
```

### Dropping a Column

```typescript
// Remove from schema, generate migration
// Drizzle will create DROP COLUMN statement
```

### Adding an Index

```typescript
export const organizations = pgTable("organizations", {
    // ... columns
}, (table) => ({
    slugIdx: index("slug_idx").on(table.slug),
}))
```

### Adding a Foreign Key

```typescript
userId: uuid("user_id").references(() => users.id).notNull()
```

## Handling Existing Data

### Backfilling Data

After adding a column, you may need to populate it:

```typescript
// In a separate script or migration
await db.update(organizations)
    .set({ defaultHoles: 18 })
    .where(eq(organizations.defaultHoles, null))
```

### Data Transformation

```typescript
// Transform existing data during migration
const orgs = await db.select().from(organizations)
for (const org of orgs) {
    await db.update(organizations)
        .set({ 
            rotationStrategy: org.oldField === 'random' ? 'random' : 'sequential' 
        })
        .where(eq(organizations.id, org.id))
}
```

## Rollback Strategy

### Manual Rollback

1. Identify the migration to rollback
2. Create a new migration that reverses changes
3. Apply the rollback migration

```sql
-- Rollback example
ALTER TABLE "organizations" DROP COLUMN "default_holes";
ALTER TABLE "organizations" DROP COLUMN "rotation_strategy";
```

### Database Backup

Always backup before major migrations:

```bash
# PostgreSQL
pg_dump dbname > backup.sql

# Restore if needed
psql dbname < backup.sql
```

## Troubleshooting

### Migration Conflicts

**Error:** "relation already exists"
- **Cause:** Migration already applied
- **Fix:** Check migration history, skip or modify migration

### Type Mismatches

**Error:** "column type mismatch"
- **Cause:** Existing data incompatible with new type
- **Fix:** Transform data first, then change type

### Constraint Violations

**Error:** "violates not-null constraint"
- **Cause:** Existing NULL values with new NOT NULL column
- **Fix:** Provide default value or backfill data first

## Best Practices

1. **Always review generated SQL** before applying
2. **Test migrations** on development database first
3. **Backup production** before migrating
4. **Use transactions** for complex migrations
5. **Keep migrations small** - one logical change per migration
6. **Document breaking changes** in migration comments
7. **Version control** migration files
8. **Never edit applied migrations** - create new ones instead
