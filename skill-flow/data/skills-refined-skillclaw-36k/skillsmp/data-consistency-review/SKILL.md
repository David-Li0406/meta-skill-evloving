---
name: data-consistency-review
description: Data consistency review guidance. Use when reviewing database changes, migrations, schema modifications, or data integrity concerns.
---

# Data Consistency Review

## Exports

- User self serviced Backups (export functionality) breaks older backups?

## DB

### Focus Areas

- Migration safety and reversibility
- Schema soundness and normalization
- Data integrity constraints
- Backward compatibility with existing data
- Production data impact assessment
- Transaction boundaries and atomicity

### Process

1. Identify all schema changes and migrations
2. Assess impact on existing production data
3. Verify migrations are idempotent or safely repeatable
4. Check for potential data loss scenarios
5. Review rollback strategy
6. Validate constraint additions against existing data

### Migration Safety

#### Before Deploying

- Can the migration run on production data without failing?
- Are there NULL values that would violate new NOT NULL constraints?
- Are there duplicate values that would violate new UNIQUE constraints?
- Will foreign key additions find orphaned records?
- Is the migration small enough to complete without locking issues?

#### Destructive Changes

Flag these as high-risk:

- Dropping columns or tables
- Changing column types (especially narrowing)
- Adding NOT NULL without defaults
- Removing or modifying constraints
- Renaming columns/tables (breaks existing queries)

#### Safe Patterns

- Add columns as nullable first, backfill, then add constraint
- Create new table, migrate data, swap references, drop old
- Use feature flags to decouple deploy from migration

### Schema Soundness

### Normalization

- Avoid redundant data that can become inconsistent
- Use foreign keys to enforce relationships
- Consider denormalization only with clear justification

#### Constraints

- Primary keys on all tables
- Foreign keys for relationships
- NOT NULL where business logic requires values
- CHECK constraints for domain validation
- UNIQUE constraints for natural keys

#### Indexing

- Indexes on foreign keys
- Indexes on frequently queried columns
- Composite indexes match query patterns
- Avoid over-indexing (write performance)

### Production Data Concerns

#### Data Volume

- Will queries still perform with 10x/100x data?
- Are there full table scans in migrations?
- Index creation on large tables may lock

#### Edge Cases

- Empty strings vs NULL handling
- Zero values vs NULL for numbers
- Timezone handling for dates
- Unicode and special characters

#### Rollback Strategy

- Can we revert the migration?
- Is there data loss on rollback?
- Do we need a data backup before migrating?
