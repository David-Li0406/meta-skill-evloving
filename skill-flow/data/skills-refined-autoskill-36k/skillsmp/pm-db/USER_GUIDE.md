# PM-DB User Guide

Complete guide to using the Project Management Database system.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Commands](#commands)
3. [Workflow](#workflow)
4. [Python API](#python-api)
5. [Backup and Restore](#backup-and-restore)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### Installation

PM-DB is pre-installed with Claude Code. Initialize the database:

```bash
/pm-db init
```

### Basic Usage

```bash
# 1. Import specifications from job-queue
/pm-db import

# 2. View dashboard
/pm-db dashboard

# 3. Export to Memory Banks
python3 skills/pm-db/scripts/export_to_memory_bank.py
```

## Commands

### `/pm-db init`

Initialize the database and run migrations.

```bash
# Create new database
/pm-db init

# Reset existing database (backs up first)
/pm-db init --reset
```

**What it does:**
- Creates `~/.claude/projects.db`
- Sets permissions to 600 (user-only)
- Runs all migrations
- Enables WAL mode and foreign keys

### `/pm-db import`

Import specifications from job-queue folders.

```bash
# Import all projects
/pm-db import

# Import specific project
/pm-db import --project my-app

# Auto-confirm paths (no prompts)
/pm-db import --auto-confirm
```

**What it imports:**
- FRD.md, FRS.md, GS.md, TR.md, task-list.md
- Creates projects automatically
- Prompts for filesystem_path (for Memory Bank exports)

### `/pm-db dashboard`

Display project management dashboard.

```bash
# Text format (default)
/pm-db dashboard

# JSON format
/pm-db dashboard --format json

# Markdown format
/pm-db dashboard --format markdown
```

**Shows:**
- Active jobs (in-progress)
- Pending jobs (queued)
- Recent completions (last 7 days)
- Velocity metrics (trend analysis)

### `/pm-db migrate`

Run database migrations.

```bash
# Apply pending migrations
/pm-db migrate

# Dry run (show what would happen)
/pm-db migrate --dry-run

# Migrate to specific version
/pm-db migrate --target-version 2
```

## Workflow

### Typical Project Workflow

```mermaid
graph TD
    A[Create specifications] --> B[/pm-db import]
    B --> C[Job starts via hook]
    C --> D[Tasks execute]
    D --> E[Code reviews added]
    E --> F[Job completes]
    F --> G[Memory Bank export]
    G --> H[/pm-db dashboard]
```

### 1. Create Specifications

Create spec files in job-queue:

```
~/.claude/job-queue/feature-my-app/docs/
├── FRD.md          # Feature Requirements
├── FRS.md          # Feature Requirements Spec
├── GS.md           # Getting Started
├── TR.md           # Technical Requirements
└── task-list.md    # Task breakdown
```

### 2. Import to Database

```bash
/pm-db import
```

Follow prompts to set filesystem_path for Memory Bank exports.

### 3. Execute Jobs

Jobs are tracked automatically via hooks:

- `on-job-start` - Creates job when execution begins
- `on-task-start` - Creates task when task starts
- `on-tool-use` - Logs command executions
- `on-code-review` - Stores code reviews
- `on-task-complete` - Marks task complete

### 4. Monitor Progress

```bash
/pm-db dashboard
```

View active work, recent completions, and velocity trends.

### 5. Export to Memory Banks

```bash
python3 skills/pm-db/scripts/export_to_memory_bank.py
```

Updates per-project Memory Banks with latest progress.

## Python API

### Basic Usage

```python
from lib.project_database import ProjectDatabase

# Using context manager (recommended)
with ProjectDatabase() as db:
    # Create project
    project_id = db.create_project(
        name="my-app",
        description="My application",
        filesystem_path="/path/to/my-app"
    )

    # Create spec
    spec_id = db.create_spec(
        project_id=project_id,
        name="feature-auth",
        frd_content="# Authentication Feature",
        status="draft"
    )

    # Create and execute job
    job_id = db.create_job(spec_id, "Build auth", priority="high")
    db.start_job(job_id)

    # ... work happens ...

    db.complete_job(job_id, exit_code=0)
```

### Project Operations

```python
# List all projects
projects = db.list_projects()

# Get project by ID
project = db.get_project(project_id)

# Get project by name
project = db.get_project_by_name("my-app")
```

### Job Operations

```python
# Create job
job_id = db.create_job(
    spec_id=spec_id,
    name="Deploy to production",
    priority="high",
    assigned_agent="deployment-agent"
)

# Start job
db.start_job(job_id)

# Complete job
db.complete_job(job_id, exit_code=0)

# List jobs
active_jobs = db.list_jobs(status='in-progress')
pending_jobs = db.list_jobs(status='pending')
```

### Task Operations

```python
# Create task
task_id = db.create_task(
    job_id=job_id,
    name="Run tests",
    order=1,
    dependencies=json.dumps([])  # JSON array of task IDs
)

# Start task
db.start_task(task_id)

# Complete task
db.complete_task(task_id, exit_code=0)

# Get tasks for job
tasks = db.get_tasks(job_id)
```

### Logging and Reviews

```python
# Log execution
db.log_execution(
    job_id=job_id,
    task_id=task_id,
    command="pytest tests/",
    output="All tests passed",
    exit_code=0,
    duration_ms=1500
)

# Add code review
db.add_code_review(
    job_id=job_id,
    task_id=None,
    reviewer="senior-dev",
    summary="Good code quality",
    verdict="approved",
    issues_found=json.dumps([]),
    files_reviewed=json.dumps(["app.py", "tests/test_app.py"])
)
```

### Reporting

```python
# Generate dashboard
dashboard = db.generate_dashboard()
print(f"Active jobs: {len(dashboard['active_jobs'])}")
print(f"Velocity: {dashboard['velocity']['this_week']} jobs this week")

# Get job timeline
timeline = db.get_job_timeline(job_id)
for event in timeline:
    print(f"{event['timestamp']}: {event['type']}")

# Search execution logs
failed_commands = db.search_execution_logs(exit_code=1)
pytest_runs = db.search_execution_logs(command_pattern="%pytest%")

# Get code review metrics
metrics = db.get_code_review_metrics(job_id=job_id)
print(f"Approval rate: {metrics['verdict_distribution']['approved'] / metrics['total_reviews']}")
```

## Troubleshooting

### Database Locked

**Problem:** `sqlite3.OperationalError: database is locked`

**Solution:**
```bash
# Check for stale connections
lsof ~/.claude/projects.db

# WAL mode helps (enabled by default)
# If needed, reset database
/pm-db init --reset
```

### Migration Failed

**Problem:** Migration fails with SQL error

**Solution:**
```bash
# Check what would happen
/pm-db migrate --dry-run

# Fix migration file in migrations/ directory
# Then apply
/pm-db migrate
```

### Import Not Finding Files

**Problem:** `/pm-db import` finds no specs

**Solution:**
```bash
# Check job-queue structure
ls -la ~/.claude/job-queue/feature-*/docs/

# Verify files exist
ls ~/.claude/job-queue/feature-my-app/docs/FRD.md
```

### Memory Bank Export Fails

**Problem:** Export script fails with permission error

**Solution:**
```bash
# Check filesystem_path is set
sqlite3 ~/.claude/projects.db "SELECT name, filesystem_path FROM projects"

# Verify path exists and is writable
ls -la /path/to/project
mkdir -p /path/to/project/memory-bank
```

### Permission Denied

**Problem:** Cannot read projects.db

**Solution:**
```bash
# Fix permissions
chmod 600 ~/.claude/projects.db

# If still fails, reinitialize
/pm-db init --reset
```

## Best Practices

### Project Setup

1. **Set filesystem_path correctly** - Use absolute paths
2. **Keep specs updated** - Reimport after changes
3. **Use meaningful names** - Job/task names should be descriptive

### Memory Bank Integration

1. **Let hooks handle exports** - Automatic with debouncing
2. **Review exported data** - Check activeContext.md and progress.md
3. **Fill in placeholders** - Update productContext.md, teamInfo.md, etc.

### Performance

1. **Use LIMIT in queries** - Don't fetch all records
2. **Archive old jobs** - Keep active dataset small
3. **Monitor dashboard** - Check velocity trends

### Data Integrity

1. **Use transactions** - Context manager handles this
2. **Validate input** - Check filesystem_path is absolute
3. **Handle errors** - Catch exceptions, don't let hooks fail

## Advanced Usage

### Custom Queries

```python
with ProjectDatabase() as db:
    # Direct SQL (use sparingly)
    cursor = db.conn.execute("""
        SELECT jobs.name, COUNT(tasks.id) as task_count
        FROM jobs
        LEFT JOIN tasks ON tasks.job_id = jobs.id
        GROUP BY jobs.id
        HAVING task_count > 10
    """)

    for row in cursor.fetchall():
        print(f"{row['name']}: {row['task_count']} tasks")
```

### Bulk Operations

```python
# Batch insert for performance
with ProjectDatabase() as db:
    for i in range(100):
        db.create_job(spec_id, f"Job {i}")
    # Commit happens on context exit
```

### Export Automation

```bash
# Add to crontab for daily exports
0 0 * * * python3 ~/.claude/skills/pm-db/scripts/export_to_memory_bank.py
```

## Backup and Restore

### Creating Backups

Backup the database before major changes or on a schedule:

```bash
# Create backup with default settings
python3 scripts/backup_db.py

# Create backup with custom locations
python3 scripts/backup_db.py --db-path /path/to/projects.db --backup-dir /path/to/backups

# List existing backups
python3 scripts/backup_db.py --list

# Keep only 5 most recent backups (default: 10)
python3 scripts/backup_db.py --keep 5
```

**Default Locations:**
- Database: `~/.claude/lib/projects.db`
- Backups: `~/.claude/backups/`

**Features:**
- Online backups (no downtime)
- Integrity verification
- Automatic cleanup of old backups
- Timestamped filenames

**Backup Filename Format:**
```
projects-backup-YYYYMMDD-HHMMSS-microseconds.db
Example: projects-backup-20260117-143022-456789.db
```

### Restoring from Backup

Restore the database from a backup file:

```bash
# Restore from backup (interactive confirmation)
python3 scripts/restore_db.py ~/.claude/backups/projects-backup-20260117-143022-456789.db

# Restore with force (no confirmation)
python3 scripts/restore_db.py backup.db --force

# Restore to custom location
python3 scripts/restore_db.py backup.db --db-path /path/to/projects.db

# Skip safety backup of current database
python3 scripts/restore_db.py backup.db --no-backup
```

**Safety Features:**
- Backup integrity verification
- Current database backed up before restore
- Confirmation prompt (unless --force)
- Schema version compatibility check

**Restore Process:**
1. Verifies backup file integrity
2. Creates safety backup of current database (unless --no-backup)
3. Prompts for confirmation (unless --force)
4. Restores backup to target location
5. Verifies restored database integrity

**Safety Backup Location:**
```
projects-pre-restore-YYYYMMDD-HHMMSS.db
```

### Automated Backup Schedule

Add to crontab for automatic daily backups:

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM (keeps 30 backups)
0 2 * * * python3 ~/.claude/scripts/backup_db.py --keep 30

# Add weekly backup (Sunday at 3 AM)
0 3 * * 0 python3 ~/.claude/scripts/backup_db.py --backup-dir ~/.claude/weekly-backups --keep 4
```

### Backup Best Practices

1. **Regular Backups:**
   - Daily backups for active development
   - Weekly backups for stable systems
   - Before major schema changes or migrations

2. **Retention Policy:**
   - Keep 10 daily backups (default)
   - Keep 4 weekly backups
   - Keep 1 monthly backup for archival

3. **Backup Verification:**
   - Test restores periodically
   - Verify backup integrity
   - Check backup file sizes

4. **Storage Locations:**
   - Store backups on different drive
   - Consider offsite backups for critical data
   - Compress old backups to save space

5. **Before Major Changes:**
   - Always backup before migrations
   - Backup before bulk operations
   - Backup before schema changes

## Support

For issues:
- Check README.md for architecture
- Check TR.md for technical details
- Check FRD.md for feature requirements
- Run tests: `python3 skills/pm-db/tests/test_project_database.py`

---

**Version:** 1.0
**Last Updated:** 2026-01-17
