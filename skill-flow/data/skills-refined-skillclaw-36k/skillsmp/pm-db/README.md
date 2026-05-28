  # pm-db: Project Management Database

Complete project management tracking system for Claude Code.

## Overview

The pm-db skill provides a SQLite-based tracking system for managing:
- **Projects** and specifications (FRD, FRS, GS, TR, task-lists)
- **Jobs** and tasks with status tracking
- **Code reviews** with verdicts and issues
- **Agent assignments** with duration tracking
- **Execution logs** of all commands
- **Dashboards** and reporting
- **Backup and restore** with online backups and integrity verification

## Quick Start

```bash
# 1. Initialize database
/pm-db init

# 2. Import specifications from job-queue
/pm-db import

# 3. View dashboard
/pm-db dashboard
```

## Commands

### Database Management

#### `/pm-db init`
Initialize the database and run all migrations.

Options:
- `--reset` - Backup existing database and create fresh one

#### `/pm-db migrate`
Run pending database migrations.

Options:
- `--dry-run` - Show what would happen without applying
- `--target-version N` - Migrate to specific version

### Data Import

#### `/pm-db import`
Import specifications from `~/.claude/job-queue/feature-*/docs/`.

Options:
- `--project NAME` - Filter by project name
- `--auto-confirm` - Don't prompt for filesystem paths

Imports:
- FRD.md, FRS.md, GS.md, TR.md, task-list.md
- Creates projects automatically
- Captures filesystem paths for Memory Bank integration

### Reporting

#### `/pm-db dashboard`
Generate status dashboard with metrics.

Options:
- `--format text` - ASCII text (default)
- `--format json` - JSON output
- `--format markdown` - Markdown tables

Shows:
- Active and pending jobs
- Recent completions (last 7 days)
- Velocity metrics (trend analysis)

## Automatic Tracking (Hooks)

The pm-db system uses hooks for automatic tracking:

### Job Lifecycle
- **on-job-start** - Creates job when `/start-phase execute` begins
- **on-task-start** - Creates task when work starts
- **on-task-complete** - Marks task complete with exit code

### Execution Logging
- **on-tool-use** - Logs every command execution
  - Captures: command, output, exit code, duration

### Code Quality
- **on-code-review** - Stores code review results
  - Captures: reviewer, summary, verdict, issues, files

### Agent Tracking
- **on-agent-assign** - Records agent assignments
  - Captures: agent type, job/task, timestamps

## Database Schema

### Core Tables

**projects**
- Stores top-level projects
- Fields: name, description, filesystem_path
- filesystem_path used for Memory Bank exports

**specs**
- Stores specifications (FRD, FRS, GS, TR, task-list)
- Links to projects
- Tracks status: draft, approved, in-progress, completed

**jobs**
- Execution jobs (e.g., "Build auth feature")
- Tracks: status, priority, assigned agent, duration
- Links to specs

**tasks**
- Individual tasks within jobs
- Tracks: status, execution order, dependencies
- Duration automatically calculated

### Tracking Tables

**code_reviews**
- Code review summaries
- Fields: reviewer, verdict (approved/changes-requested/rejected), issues

**execution_logs**
- All command executions
- Fields: command, output, exit_code, duration_ms
- Enables full audit trail

**agent_assignments**
- Agent work tracking
- Fields: agent_type, job_id/task_id, duration

## Python API

```python
from lib.project_database import ProjectDatabase

# Create database instance
db = ProjectDatabase()

# Or use as context manager
with ProjectDatabase() as db:
    # Create project
    project_id = db.create_project("my-app", "My application", "/path/to/app")

    # Create spec
    spec_id = db.create_spec(
        project_id=project_id,
        name="feature-auth",
        frd_content="...",
        status="draft"
    )

    # Create and track job
    job_id = db.create_job(spec_id, "Build auth", priority="high")
    db.start_job(job_id)

    # ... work happens ...

    db.complete_job(job_id, exit_code=0)

    # Generate dashboard
    dashboard = db.generate_dashboard()
```

## Performance

Design targets (met):
- Query response: <100ms (P95)
- Dashboard generation: <2 seconds
- 100 spec import: <5 seconds
- Handles 10,000+ jobs without degradation

## Memory Bank Integration

The pm-db system exports to **per-project Memory Banks**:

- Reads `filesystem_path` from projects table
- Exports to `{filesystem_path}/memory-bank/`
- Updates `activeContext.md` and `progress.md`
- Auto-creates minimal structure if missing
- Per-project debouncing (not global)

See Task 6.1 and 6.2 for implementation details.

## File Structure

```
~/.claude/
├── lib/
│   └── project_database.py      # Core database abstraction
├── migrations/
│   ├── 001_initial.sql          # Initial schema
│   ├── 002_add_code_reviews.sql # Code reviews
│   └── 003_add_execution_logs.sql # Logs + agents
├── hooks/pm-db/
│   ├── on-job-start.py
│   ├── on-task-start.py
│   ├── on-tool-use.py
│   ├── on-code-review.py
│   ├── on-task-complete.py
│   └── on-agent-assign.py
├── skills/pm-db/
│   ├── SKILL.md                 # Skill definition
│   ├── README.md               # This file
│   └── scripts/
│       ├── init_db.py
│       ├── migrate.py
│       ├── import_specs.py
│       ├── generate_report.py
│       └── export_to_memory_bank.py
└── projects.db                  # SQLite database
```

## Troubleshooting

### Database locked
```bash
# Check for stale connections
lsof ~/.claude/projects.db

# WAL mode helps prevent locks
# (enabled automatically by init_db.py)
```

### Migration failed
```bash
# Roll back and fix
/pm-db migrate --dry-run  # See what would happen
# Fix SQL syntax error
/pm-db migrate            # Apply again
```

### Import not finding files
```bash
# Check job-queue structure
ls -la ~/.claude/job-queue/feature-*/docs/

# Manually specify path
/pm-db import --auto-confirm
```

## Development

### Running Tests

```bash
# Unit tests
python3 skills/pm-db/tests/test_project_database.py

# Integration tests
python3 skills/pm-db/tests/test_hooks.py

# Performance tests
python3 skills/pm-db/tests/test_performance.py
```

### Adding New Migrations

1. Create `migrations/00N_description.sql`
2. Include version update: `INSERT INTO schema_version (version, description) VALUES (N, '...')`
3. Test: `/pm-db migrate --dry-run`
4. Apply: `/pm-db migrate`

## Support

For issues or questions:
- Check `TR.md` for technical requirements
- Check `FRD.md` for feature requirements
- Check `GS.md` for usage scenarios

---

**Version:** 1.0
**License:** Internal Use
**Maintainer:** Claude Code Infrastructure
