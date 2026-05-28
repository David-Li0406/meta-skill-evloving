---
name: pm-db
description: Project management database for tracking specs, jobs, tasks, and execution
args:
  command:
    type: string
    description: Command to execute (init, import, dashboard, migrate, backup)
    required: true
---

# pm-db Skill

Manage the project management database for tracking specifications, jobs, tasks, code reviews, and execution logs.

## Available Commands

### `init` - Initialize Database

Creates the projects.db database and runs all migrations.

```bash
/pm-db init
/pm-db init --reset  # Backup existing and create fresh database
```

### `import` - Import Specifications

Imports specifications from job-queue folders.

```bash
/pm-db import
/pm-db import --project auth  # Filter by project name
```

### `dashboard` - Show Dashboard

Displays project management dashboard with metrics.

```bash
/pm-db dashboard
/pm-db dashboard --format json
/pm-db dashboard --format markdown
```

### `migrate` - Run Migrations

Applies pending database migrations.

```bash
/pm-db migrate
/pm-db migrate --dry-run
/pm-db migrate --target-version 2
```

### `backup` - Backup Database

Creates a timestamped backup of the database (not yet implemented).

```bash
/pm-db backup
```

## Examples

```bash
# First-time setup
/pm-db init

# Import all specs
/pm-db import

# View dashboard
/pm-db dashboard

# Export to JSON
/pm-db dashboard --format json
```

## Database Location

Default: `~/.claude/projects.db`

## Hooks

The pm-db system includes automatic hooks:
- `on-job-start` - Creates job record when /start-phase begins
- `on-task-start` - Creates task record when task starts
- `on-tool-use` - Logs every command execution
- `on-code-review` - Stores code review summaries
- `on-task-complete` - Marks task complete
- `on-agent-assign` - Records agent assignments

## Schema

See `migrations/` for complete database schema.

Tables:
- `projects` - Top-level projects
- `specs` - Specifications (FRD, FRS, GS, TR, task-list)
- `jobs` - Execution jobs
- `tasks` - Individual tasks within jobs
- `code_reviews` - Code review results
- `execution_logs` - Command execution logs
- `agent_assignments` - Agent work assignments
