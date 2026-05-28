---
name: migrate
description: Run database migrations with safety checks, dry-run previews, and rollback guidance
allowed-tools: Bash, Read
disable-model-invocation: true
argument-hint: [local|staging|production]
---

# Database Migration Workflow

Apply database migrations safely for the specified environment.

## Usage

- `/devflow-migrate` - Migrate local environment (default)
- `/devflow-migrate local` - Migrate local environment
- `/devflow-migrate staging` - Migrate staging (requires dry-run first)
- `/devflow-migrate production` - Migrate production (requires confirmation)

## Arguments

Environment: $ARGUMENTS (defaults to "local" if not specified)

## Safety Rules

1. **ALWAYS** run dry-run first for staging and production
2. **NEVER** auto-execute production migrations without explicit user confirmation
3. **ALWAYS** show what will be applied before executing
4. If any step fails, stop immediately and report the error

## Workflow Steps

### Step 1: Verify Prerequisites

```bash
devflow doctor
```

Ensure database connectivity is available for the target environment.

### Step 2: Check Current Migration State

```bash
devflow db status --env <environment> --json
```

Parse the output to show:
- Total migrations
- Applied migrations
- Pending migrations (list each one)

If no migrations are pending, inform the user and stop.

### Step 3: Preview Pending Migrations

Read each pending migration file and summarize what it does:

```bash
# For each pending migration file, read and summarize
```

Explain in plain English what each migration will do (create table, add column, etc.)

### Step 4: Dry Run (Required for staging/production)

```bash
devflow db migrate --env <environment> --dry-run --json
```

Show the dry-run results. If there are any errors, stop and help debug.

### Step 5: Confirm and Execute

For **local**:
- Proceed automatically after showing the preview

For **staging**:
- Ask user to confirm: "Apply N migrations to staging?"

For **production**:
- Show a warning banner
- Require explicit confirmation: "Type 'yes' to apply N migrations to PRODUCTION"
- Recommend having a rollback plan ready

```bash
devflow db migrate --env <environment> --json
```

### Step 6: Verify Success

```bash
devflow db status --env <environment> --json
```

Confirm all migrations are now applied.

## Rollback Guidance

If migrations fail or need to be reverted:

1. Check if the migration has a corresponding `down` migration
2. If not, help the user create a reverse migration:
   ```bash
   devflow db create revert_<migration_name>
   ```
3. Guide them through writing the rollback SQL

## Error Handling

- **Connection refused**: Check if database is running, verify DATABASE_URL
- **Permission denied**: Check database user permissions
- **Migration conflict**: Check for concurrent migrations, advisory locks
- **SQL syntax error**: Show the specific line and help fix it
