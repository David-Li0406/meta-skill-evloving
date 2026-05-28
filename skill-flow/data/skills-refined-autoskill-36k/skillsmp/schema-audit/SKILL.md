---
name: schema-audit
description: Review database schema changes for tenant isolation, performance, and integrity in Drizzle ORM
---

# Database Schema Audit Instructions

## Purpose
Ensure database schema changes maintain multi-tenant isolation, performance, and data integrity in the OutreachGlobal PostgreSQL database using Drizzle ORM.

## When to Use This Skill
- Reviewing new schema migrations
- Adding new tables or columns
- Modifying existing schemas
- Before deploying database changes
- Investigating performance issues

## Core Requirements

### 1. Multi-Tenant Isolation
**Every table must have:**
```typescript
export const teamsTable = pgTable("teams", {
  id: uuid("id").primaryKey().defaultRandom(),
  // ... other columns
});

export const leadsTable = pgTable("leads", {
  id: uuid("id").primaryKey().defaultRandom(),
  teamId: uuid("team_id").notNull().references(() => teamsTable.id),
  // ... other columns
});
```

**Audit checks:**
- [ ] All tables have `teamId` column
- [ ] Foreign keys properly reference tenant-isolated tables
- [ ] No shared tables without tenant context

### 2. Indexing Strategy
**Required indexes for performance:**
```typescript
// Team-scoped queries
export const leadsTeamIdx = index("leads_team_idx").on(leadsTable.teamId);

// Composite indexes for common queries
export const leadsStatusIdx = index("leads_status_team_idx").on(
  leadsTable.status,
  leadsTable.teamId
);
```

**Performance patterns to index:**
- `teamId` + `createdAt` for recent records
- `teamId` + `status` for workflow queries
- `teamId` + `phoneNumber` for duplicate checking

### 3. Data Types & Constraints
**Best practices:**
- Use `uuid` for primary keys (not serial)
- Add `createdAt` and `updatedAt` timestamps
- Use appropriate constraints (NOT NULL, CHECK, UNIQUE)
- Consider `text` vs `varchar` for flexibility

### 4. Migration Safety
**Review migration files:**
```typescript
// Safe migration example
export const migration_001 = {
  name: "add_team_id_to_properties",
  up: (db) => db.execute(sql`
    ALTER TABLE properties ADD COLUMN team_id UUID REFERENCES teams(id);
    CREATE INDEX CONCURRENTLY properties_team_idx ON properties(team_id);
  `),
  down: (db) => db.execute(sql`
    DROP INDEX properties_team_idx;
    ALTER TABLE properties DROP COLUMN team_id;
  `)
};
```

**Safety checks:**
- [ ] Migrations are reversible
- [ ] No data loss on rollback
- [ ] Indexes created CONCURRENTLY to avoid locks
- [ ] Foreign key constraints added safely

## Common Issues to Flag

### Performance Problems
- Missing indexes on `teamId` columns
- Inefficient queries without proper filtering
- Large tables without partitioning strategy

### Data Integrity Issues
- Missing foreign key constraints
- Nullable columns that should be required
- Inconsistent naming conventions

### Scalability Concerns
- Tables growing without archiving strategy
- No consideration for 10K+ record operations
- Missing composite indexes for complex queries

## Audit Checklist

### Schema Structure
- [ ] All tables have `teamId` foreign key
- [ ] Primary keys use UUID
- [ ] Timestamps include timezone info
- [ ] Column names follow snake_case

### Relationships
- [ ] Foreign keys maintain referential integrity
- [ ] Cascade deletes considered carefully
- [ ] Self-referencing tables handle properly

### Performance
- [ ] Indexes on all `teamId` columns
- [ ] Composite indexes for common query patterns
- [ ] No redundant indexes

### Migrations
- [ ] All changes have migration scripts
- [ ] Migrations tested on staging
- [ ] Rollback strategy documented

## Response Format
When auditing schemas, provide:
1. **Compliance score** (percentage of requirements met)
2. **Critical issues** blocking deployment
3. **Performance recommendations** with specific index suggestions
4. **Migration review** with safety assessment

## Related Skills
- Use with `multi-tenant-audit` for runtime query checking
- Combine with `infra-capacity` for scaling considerations
- Reference `cost-guardian` for query cost analysis