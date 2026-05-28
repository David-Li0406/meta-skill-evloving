# Example: Complex Skill with Scripts

This example shows a more sophisticated skill with executable code and multiple reference files.

## Skill: Database Migration

A skill that helps Claude create and manage database migrations.

### Directory Structure

```
.claude/skills/db-migration/
├── SKILL.md
├── patterns/
│   ├── common-migrations.md
│   └── rollback-patterns.md
├── scripts/
│   ├── validate-migration.js
│   └── generate-migration.js
└── templates/
    └── migration-template.sql
```

### SKILL.md

```markdown
---
name: Database Migration
description: Create and manage database migrations. Use when user says "create migration", "add column", "change schema", or needs database structure changes.
---

# Database Migration

You are an expert at database schema management. Your task is to create safe, reversible migrations.

## When to Use This Skill

Use this skill when:
- Adding, modifying, or removing database columns
- Creating new tables
- Changing indexes or constraints
- Any schema modification

## Migration Principles

1. **Always reversible**: Every migration must have a rollback
2. **Atomic changes**: One logical change per migration
3. **No data loss**: Preserve existing data during changes
4. **Tested**: Validate before applying

## Workflow

### Step 1: Analyze the Change

Before creating a migration:
1. Understand what schema change is needed
2. Identify affected tables and columns
3. Consider data migration requirements
4. Plan the rollback strategy

### Step 2: Generate Migration File

Run the generation script:
```bash
node .claude/skills/db-migration/scripts/generate-migration.js --name "description_of_change"
```

Or use the template:
Read: .claude/skills/db-migration/templates/migration-template.sql

### Step 3: Write the Migration

For common patterns:
Read: .claude/skills/db-migration/patterns/common-migrations.md

Key rules:
- Use explicit column types
- Add NOT NULL with defaults for existing tables
- Create indexes for foreign keys
- Include both UP and DOWN sections

### Step 4: Validate

Run validation before committing:
```bash
node .claude/skills/db-migration/scripts/validate-migration.js
```

This checks:
- SQL syntax validity
- Rollback completeness
- Naming conventions
- Data safety

### Step 5: Test

1. Apply migration to test database
2. Verify schema changes
3. Test rollback
4. Check application compatibility

## Rollback Patterns

For rollback strategies:
Read: .claude/skills/db-migration/patterns/rollback-patterns.md

## Quick Reference

| Change Type | Pattern |
|-------------|---------|
| Add column | `ALTER TABLE ADD COLUMN ... DEFAULT` |
| Remove column | Create backup, then drop |
| Rename column | Add new, migrate data, drop old |
| Add index | `CREATE INDEX CONCURRENTLY` |

## Safety Checklist

Before applying any migration:
- [ ] Migration has complete rollback
- [ ] Validated with script
- [ ] Tested on development database
- [ ] Backup of production data exists
- [ ] Team is notified of changes

## BEGIN

1. Understand what schema change the user needs
2. Analyze the impact on existing data
3. Create migration following the workflow above
4. Validate and provide testing instructions
```

### scripts/validate-migration.js

```javascript
#!/usr/bin/env node
/**
 * Migration Validation Script
 *
 * Validates SQL migration files for:
 * - Syntax correctness
 * - Presence of UP and DOWN sections
 * - Naming conventions
 * - Common safety issues
 */

const fs = require('fs');
const path = require('path');

function validateMigration(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const errors = [];
  const warnings = [];

  // Check for UP section
  if (!content.includes('-- UP') && !content.includes('-- migrate:up')) {
    errors.push('Missing UP migration section');
  }

  // Check for DOWN section
  if (!content.includes('-- DOWN') && !content.includes('-- migrate:down')) {
    errors.push('Missing DOWN migration section (rollback required)');
  }

  // Check for dangerous operations
  if (content.includes('DROP TABLE') && !content.includes('IF EXISTS')) {
    warnings.push('DROP TABLE without IF EXISTS - may fail if table missing');
  }

  if (content.includes('DROP COLUMN') && !content.includes('backup')) {
    warnings.push('DROP COLUMN detected - ensure data backup exists');
  }

  // Check for NOT NULL without default on existing table
  const notNullMatch = content.match(/ADD COLUMN.*NOT NULL(?!.*DEFAULT)/i);
  if (notNullMatch) {
    errors.push('Adding NOT NULL column without DEFAULT will fail on existing rows');
  }

  // Output results
  console.log(`\nValidating: ${path.basename(filePath)}`);
  console.log('='.repeat(50));

  if (errors.length === 0 && warnings.length === 0) {
    console.log('✅ Migration is valid');
    return true;
  }

  errors.forEach(e => console.log(`❌ ERROR: ${e}`));
  warnings.forEach(w => console.log(`⚠️  WARNING: ${w}`));

  return errors.length === 0;
}

// Main execution
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Usage: node validate-migration.js <migration-file>');
  process.exit(1);
}

const isValid = validateMigration(args[0]);
process.exit(isValid ? 0 : 1);
```

### templates/migration-template.sql

```sql
-- Migration: {MIGRATION_NAME}
-- Created: {TIMESTAMP}
-- Description: {DESCRIPTION}

-- UP
-- =============================================================================
-- Add your forward migration SQL here



-- DOWN
-- =============================================================================
-- Add your rollback SQL here (must reverse the UP migration)


```

### patterns/common-migrations.md

```markdown
# Common Migration Patterns

## Adding a Column

### With Default Value (Safe for existing data)
```sql
-- UP
ALTER TABLE users ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'active';

-- DOWN
ALTER TABLE users DROP COLUMN status;
```

### Nullable Column
```sql
-- UP
ALTER TABLE users ADD COLUMN nickname VARCHAR(100);

-- DOWN
ALTER TABLE users DROP COLUMN nickname;
```

## Renaming a Column (Safe Approach)

```sql
-- UP
ALTER TABLE users ADD COLUMN full_name VARCHAR(200);
UPDATE users SET full_name = name;
ALTER TABLE users DROP COLUMN name;

-- DOWN
ALTER TABLE users ADD COLUMN name VARCHAR(200);
UPDATE users SET name = full_name;
ALTER TABLE users DROP COLUMN full_name;
```

## Adding an Index

```sql
-- UP
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- DOWN
DROP INDEX idx_users_email;
```

## Creating a Table

```sql
-- UP
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_user_id ON posts(user_id);

-- DOWN
DROP TABLE IF EXISTS posts;
```
```

---

## Key Takeaways

1. **Scripts as tools**: Claude can execute scripts for validation
2. **Templates as starting points**: Reduce boilerplate
3. **Patterns as reference**: Load detailed patterns only when needed
4. **Safety checks**: Scripts enforce best practices
5. **Clear workflow**: Step-by-step process reduces errors
