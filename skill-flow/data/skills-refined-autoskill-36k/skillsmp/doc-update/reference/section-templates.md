# Feature Doc Section Templates

Use these templates when updating feature documentation.

## User Surfaces

```markdown
## User Surfaces

| Surface | Route/Location | Description |
|---------|---------------|-------------|
| [Page name] | /path/to/route | [What it does] |
| [Component] | [Location] | [Purpose] |
```

## Data Model

```markdown
## Data Model

### Tables
| Table | Purpose | Key Columns |
|-------|---------|-------------|
| [table_name] | [purpose] | [col1, col2, col3] |

### New/Modified Columns
- `column_name`: [type] - [purpose]
```

## Server Actions

```markdown
## Server Actions

| Action | Purpose | Tables | Auth Required |
|--------|---------|--------|---------------|
| [actionName] | [what it does] | [tables touched] | [yes/no + level] |
```

## Permissions & Security

```markdown
## Permissions & Security

### RLS Policies
- [policy_name]: [what it allows/denies]

### Admin Client Usage
- [action]: [why admin client needed]
```

## Invariants

```markdown
## Invariants

1. [Existing invariant]
2. [NEW] [Newly discovered invariant from this change]
```

## Testing Checklist

```markdown
## Testing Checklist

### Local Verification
- [ ] [Verification step]
- [ ] [Verification step]

### Regression Checks
- [ ] [Area that might break]
```

## Production SQL

```markdown
## Production SQL

⚠️ Review before running on production

```sql
-- Migration: [name]
-- Purpose: [what it does]
-- Rollback: [how to undo]

[SQL statements]
```
```
