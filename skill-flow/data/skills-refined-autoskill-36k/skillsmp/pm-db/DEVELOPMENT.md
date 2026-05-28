# PM-DB Development Guide

Complete guide for developers contributing to or maintaining the pm-db system.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Development Setup](#development-setup)
3. [Code Standards](#code-standards)
4. [Testing](#testing)
5. [Database Migrations](#database-migrations)
6. [Hook Development](#hook-development)
7. [Script Development](#script-development)
8. [Debugging](#debugging)
9. [Performance](#performance)
10. [Maintenance](#maintenance)
11. [Release Process](#release-process)

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────┐
│                  CLI Layer                      │
│  /pm-db init | import | dashboard | migrate    │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│              Script Layer                       │
│  init_db.py | import_specs.py | migrate.py     │
│  generate_report.py | export_to_memory_bank.py │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│           Python API Layer                      │
│        lib/project_database.py                  │
│  create_*, update_*, get_*, list_*, search_*   │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│            Database Layer                       │
│           SQLite (projects.db)                  │
│  WAL mode, Foreign keys, Parameterized queries │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│              Hook Layer (Parallel)              │
│  on-job-start | on-task-start | on-tool-use    │
│  on-code-review | on-task-complete              │
└─────────────────────────────────────────────────┘
```

### Data Flow

1. **User triggers action** (via CLI or hook)
2. **Script processes** (validates, transforms)
3. **API executes** (database operations)
4. **Database persists** (SQLite, ACID transactions)
5. **Hooks notify** (event-driven updates)

### Key Design Principles

1. **Zero External Dependencies**
   - Only Python stdlib
   - Portable across systems
   - No pip install required

2. **Security First**
   - Parameterized queries (SQL injection prevention)
   - Input validation on all user inputs
   - Safe filesystem operations

3. **Performance**
   - WAL mode for concurrency
   - Indexed queries
   - LIMIT enforcement
   - Truncated output (50KB max)

4. **Reliability**
   - ACID transactions
   - Foreign key constraints
   - Context managers (auto-cleanup)
   - Graceful error handling

---

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Claude Code environment

### Clone and Setup

```bash
# Already in ~/.claude/ if using Claude Code
cd ~/.claude

# Verify structure
ls -la lib/project_database.py
ls -la skills/pm-db/
ls -la migrations/
ls -la hooks/pm-db/

# Initialize database
/pm-db init

# Run tests
python3 skills/pm-db/tests/test_project_database.py
python3 skills/pm-db/tests/test_integration.py
python3 skills/pm-db/tests/test_performance.py
```

### Development Database

```bash
# Use test database (don't pollute production)
export CLAUDE_DB_PATH=~/.claude/projects-test.db

# Initialize test database
python3 skills/pm-db/scripts/init_db.py

# Run operations
python3 skills/pm-db/scripts/import_specs.py
```

### IDE Setup

**VS Code settings.json:**
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "editor.rulers": [88, 120]
}
```

**MyPy configuration (.mypy.ini):**
```ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

---

## Code Standards

### Python Style

Follow PEP 8 with these specifics:

**Line length:**
- 88 characters (Black default)
- 120 characters absolute max

**Imports:**
```python
# Standard library first
import sqlite3
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

# Local imports last
from lib.project_database import ProjectDatabase
```

**Type Hints:**
```python
# Always use type hints
def create_project(
    self,
    name: str,
    description: Optional[str] = None,
    filesystem_path: Optional[str] = None
) -> int:
    """
    Create a new project.

    Args:
        name: Unique project name
        description: Optional project description
        filesystem_path: Absolute path to project folder

    Returns:
        Project ID (integer)

    Raises:
        ValueError: If name is empty or filesystem_path is invalid
    """
```

**Docstrings:**
```python
# Google style docstrings
def search_logs(pattern: str) -> List[Dict[str, Any]]:
    """
    Search execution logs by pattern.

    Args:
        pattern: SQL LIKE pattern (e.g., "%pytest%")

    Returns:
        List of matching log dicts

    Example:
        >>> logs = db.search_logs("%error%")
        >>> print(f"Found {len(logs)} errors")
    """
```

### SQL Style

**Formatting:**
```sql
-- Uppercase keywords, lowercase table/column names
SELECT id, name, status
FROM jobs
WHERE status = 'in-progress'
  AND created_at >= datetime('now', '-7 days')
ORDER BY created_at DESC
LIMIT 100;

-- Indent WHERE clauses
-- Always use LIMIT for safety
```

**Parameterized Queries:**
```python
# GOOD - Parameterized (safe)
cursor = self.conn.execute(
    "SELECT * FROM jobs WHERE status = ? AND priority = ?",
    (status, priority)
)

# BAD - String interpolation (SQL injection risk!)
cursor = self.conn.execute(
    f"SELECT * FROM jobs WHERE status = '{status}'"
)
```

### Error Handling

```python
# Specific exceptions
try:
    db.create_project(name)
except ValueError as e:
    print(f"Validation error: {e}")
except sqlite3.IntegrityError as e:
    print(f"Duplicate project: {e}")
except sqlite3.Error as e:
    print(f"Database error: {e}")
    # Consider rollback here

# Always use context managers
with ProjectDatabase() as db:
    # Operations
    # Auto-closes on exit
```

### Validation

```python
# Validate all inputs
def create_project(self, name: str, ...) -> int:
    # Empty check
    if not name or not name.strip():
        raise ValueError("Project name cannot be empty")

    # Path validation
    if filesystem_path and not Path(filesystem_path).is_absolute():
        raise ValueError("filesystem_path must be an absolute path")

    # Enum validation
    valid_statuses = ['draft', 'approved', 'in-progress', 'completed']
    if status not in valid_statuses:
        raise ValueError(f"Status must be one of: {valid_statuses}")
```

---

## Testing

### Test Organization

```
skills/pm-db/tests/
├── test_project_database.py  # Unit tests (30 tests)
├── test_integration.py        # Integration tests (7 tests)
├── test_performance.py        # Performance tests (6 tests)
├── test_hooks.py              # Hook tests (6 tests)
├── test_security.py           # Security tests (18 tests)
├── test_end_to_end.py         # End-to-end tests (6 tests)
├── test_deployment.py         # Deployment validation (17 tests)
├── test_backup_restore.py     # Backup/restore tests (9 tests)
└── test_uat.py                # User acceptance tests (7 tests)
```

**Total:** 106 tests across 9 test suites

### Running Tests

```bash
# Run all test suites
python3 skills/pm-db/tests/test_project_database.py   # Unit (30 tests)
python3 skills/pm-db/tests/test_integration.py         # Integration (7 tests)
python3 skills/pm-db/tests/test_performance.py         # Performance (6 tests)
python3 skills/pm-db/tests/test_hooks.py               # Hooks (6 tests)
python3 skills/pm-db/tests/test_security.py            # Security (18 tests)
python3 skills/pm-db/tests/test_end_to_end.py          # E2E (6 tests)
python3 skills/pm-db/tests/test_deployment.py          # Deployment (17 tests)
python3 skills/pm-db/tests/test_backup_restore.py      # Backup/Restore (9 tests)
python3 skills/pm-db/tests/test_uat.py                 # UAT (7 tests)

# Run all tests in sequence
for test in skills/pm-db/tests/test_*.py; do python3 "$test"; done

# Verbose output
python3 skills/pm-db/tests/test_project_database.py -v

# Specific test
python3 skills/pm-db/tests/test_project_database.py TestProjectDatabase.test_create_project
```

### Writing Unit Tests

```python
import unittest
import tempfile
from pathlib import Path
from lib.project_database import ProjectDatabase

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        """Create temporary database for each test"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        self.db = ProjectDatabase(db_path=self.db_path)

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

    def tearDown(self):
        """Clean up temporary database"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def test_new_feature(self):
        """Test the new feature works correctly"""
        # Arrange
        project_id = self.db.create_project("test", "Test", "/tmp/test")

        # Act
        result = self.db.new_feature(project_id)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result['status'], 'success')
```

### Test Coverage Goals

- **Unit tests:** 100% method coverage (30 tests)
- **Integration tests:** All workflows tested (7 tests)
- **Performance tests:** All targets met (6 tests)
- **Hook tests:** All hooks verified (6 tests)
- **Security tests:** OWASP Top 10 validated (18 tests)
- **End-to-end tests:** Complete user workflows (6 tests)
- **Deployment tests:** Production readiness (17 tests)
- **Backup/Restore tests:** Data integrity (9 tests)
- **UAT tests:** User acceptance scenarios (7 tests)

**Total Coverage:** 106 tests ensuring production quality

### Test Data

```python
# Use realistic but minimal test data
def create_test_project(db):
    """Helper to create test project"""
    return db.create_project(
        "test-app",
        "Test application",
        "/tmp/test-app"
    )

def create_test_spec(db, project_id):
    """Helper to create test spec"""
    return db.create_spec(
        project_id,
        "feature-test",
        frd_content="# Test Feature\n\nMinimal test data"
    )
```

---

## Database Migrations

### Migration Lifecycle

1. **Create migration file**
2. **Test with --dry-run**
3. **Apply migration**
4. **Verify schema**
5. **Update version**

### Creating a Migration

**File:** `migrations/004_add_new_table.sql`

```sql
-- Migration 004: Add new_table
-- Date: 2026-01-17
-- Purpose: Track new feature

-- Check current version
SELECT MAX(version) FROM schema_version;
-- Should be 3 before this migration

-- Create new table
CREATE TABLE new_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    data TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Add indexes
CREATE INDEX idx_new_table_job_id ON new_table(job_id);
CREATE INDEX idx_new_table_created_at ON new_table(created_at);

-- Update schema version
INSERT INTO schema_version (version, description, applied_at)
VALUES (4, 'Add new_table for new feature', datetime('now'));
```

### Testing Migrations

```bash
# Dry run (doesn't apply)
/pm-db migrate --dry-run

# Check what would happen
sqlite3 ~/.claude/projects.db "SELECT * FROM schema_version"

# Apply migration
/pm-db migrate

# Verify
sqlite3 ~/.claude/projects.db ".schema new_table"
```

### Migration Best Practices

1. **Always add indexes** for foreign keys
2. **Use ON DELETE CASCADE** for cleanup
3. **Include version update** in same file
4. **Test on copy of production** database first
5. **Document purpose** in comments
6. **Never modify existing migrations** after release

### Rollback Strategy

```sql
-- Include rollback instructions in comments
-- ROLLBACK:
-- DROP TABLE new_table;
-- DELETE FROM schema_version WHERE version = 4;
```

### Common Migration Patterns

**Add column:**
```sql
ALTER TABLE jobs ADD COLUMN new_field TEXT;
```

**Add index:**
```sql
CREATE INDEX idx_jobs_new_field ON jobs(new_field);
```

**Add table:**
```sql
CREATE TABLE new_table (...);
CREATE INDEX idx_new_table_fk ON new_table(foreign_key_id);
```

**Data migration:**
```sql
-- Migrate existing data
UPDATE jobs SET new_field = 'default' WHERE new_field IS NULL;
```

---

## Hook Development

### Hook Structure

**Template:** `hooks/pm-db/on-new-event.py`

```python
#!/usr/bin/env python3
"""
Hook: on-new-event

Triggered when: [Event description]
Purpose: [What this hook does]

Input (JSON via stdin):
{
    "field1": "value",
    "field2": 123
}

Output (JSON to stdout):
{
    "status": "success|failed",
    "message": "...",
    "data": {...}
}
"""

import sys
import json
import os
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path.home() / ".claude" / "lib"))

from project_database import ProjectDatabase

def main():
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())

        # Validate required fields
        required = ['field1', 'field2']
        missing = [f for f in required if f not in input_data]
        if missing:
            return {
                "status": "failed",
                "error": f"Missing required fields: {missing}"
            }

        # Get database path (allow override for testing)
        db_path = os.environ.get('CLAUDE_DB_PATH')

        # Execute hook logic
        with ProjectDatabase(db_path=db_path) as db:
            # ... hook operations ...
            result = db.some_operation(input_data['field1'])

        # Return success
        return {
            "status": "success",
            "message": "Operation completed",
            "data": result
        }

    except Exception as e:
        # Return failure (don't raise - hooks should never crash)
        return {
            "status": "failed",
            "error": str(e)
        }

if __name__ == "__main__":
    output = main()
    print(json.dumps(output))
```

### Hook Best Practices

1. **Never raise exceptions** - always return JSON
2. **Validate all inputs** - check required fields
3. **Use environment override** - allow CLAUDE_DB_PATH
4. **Log errors** - include error in output
5. **Keep it fast** - hooks block execution
6. **Make executable:** `chmod +x hooks/pm-db/on-new-event.py`

### Testing Hooks

```bash
# Test with sample input
echo '{"field1": "test", "field2": 123}' | \
  CLAUDE_DB_PATH=~/.claude/projects-test.db \
  python3 hooks/pm-db/on-new-event.py

# Verify output is valid JSON
echo '{"field1": "test"}' | \
  python3 hooks/pm-db/on-new-event.py | jq .
```

### Hook Performance

- **Target:** <100ms execution
- **Measure:** Add timing to hook output
- **Optimize:** Minimize database queries

```python
import time

start = time.time()
# ... hook logic ...
duration_ms = int((time.time() - start) * 1000)

return {
    "status": "success",
    "duration_ms": duration_ms
}
```

---

## Script Development

### Script Structure

**Template:** `skills/pm-db/scripts/new_script.py`

```python
#!/usr/bin/env python3
"""
Script: new_script.py

Purpose: [What this script does]

Usage:
    python3 skills/pm-db/scripts/new_script.py [OPTIONS]

Options:
    --arg1 VALUE    Description
    --flag          Description
    --help          Show help
"""

import sys
import argparse
from pathlib import Path

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase

def main():
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('--arg1', help='Argument description')
    parser.add_argument('--flag', action='store_true', help='Flag description')

    args = parser.parse_args()

    try:
        with ProjectDatabase() as db:
            # ... script logic ...
            result = db.some_operation(args.arg1)
            print(f"Success: {result}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Script Best Practices

1. **Use argparse** - standard CLI parsing
2. **Add --help** - document all options
3. **Exit codes** - 0 success, 1 error
4. **stderr for errors** - stdout for output
5. **Confirm destructive** operations - ask before delete
6. **Make executable:** `chmod +x skills/pm-db/scripts/new_script.py`

### User Prompts

```python
# Confirm destructive operations
def confirm(message: str) -> bool:
    """Prompt user for confirmation"""
    response = input(f"{message} (y/N): ").lower()
    return response in ['y', 'yes']

if confirm("Delete all data?"):
    # ... proceed ...
```

---

## Debugging

### Enable SQL Logging

```python
# In project_database.py __init__
self.conn.set_trace_callback(print)  # Log all SQL

# Or use with context
import sqlite3

sqlite3.enable_callback_tracebacks(True)
```

### Inspect Database

```bash
# Open database
sqlite3 ~/.claude/projects.db

# List tables
.tables

# Show schema
.schema jobs

# Query data
SELECT * FROM jobs LIMIT 5;

# Check indexes
.indexes jobs

# Analyze query plan
EXPLAIN QUERY PLAN
SELECT * FROM jobs WHERE status = 'in-progress';
```

### Common Issues

**Database locked:**
```bash
# Find processes
lsof ~/.claude/projects.db

# Force close (last resort)
rm ~/.claude/projects.db-wal
rm ~/.claude/projects.db-shm
```

**Migration failed:**
```bash
# Check current version
sqlite3 ~/.claude/projects.db "SELECT * FROM schema_version"

# Manual rollback
sqlite3 ~/.claude/projects.db "DELETE FROM schema_version WHERE version = N"
sqlite3 ~/.claude/projects.db "DROP TABLE problematic_table"
```

**Hook not triggering:**
```bash
# Check hook is executable
ls -la hooks/pm-db/on-job-start.py

# Test manually
echo '{"spec_id": 1, "job_name": "Test"}' | \
  python3 hooks/pm-db/on-job-start.py
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Use in code
logger.debug(f"Creating project: {name}")
logger.info(f"Project created: {project_id}")
logger.error(f"Failed to create project: {e}")
```

---

## Performance

### Query Optimization

**Use indexes:**
```sql
-- Create index for frequently queried columns
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created_at ON jobs(created_at);

-- Compound index for common queries
CREATE INDEX idx_jobs_status_created ON jobs(status, created_at);
```

**Use LIMIT:**
```python
# Always limit result sets
jobs = db.list_jobs(limit=100)  # Good
jobs = db.list_jobs()  # Bad if thousands of jobs
```

**Avoid N+1 queries:**
```python
# Bad - N+1 queries
jobs = db.list_jobs()
for job in jobs:
    tasks = db.get_tasks(job['id'])  # Query per job!

# Good - Single query with JOIN
cursor = db.conn.execute("""
    SELECT jobs.*, tasks.*
    FROM jobs
    LEFT JOIN tasks ON tasks.job_id = jobs.id
    WHERE jobs.status = 'in-progress'
""")
```

### Profiling

```python
import cProfile
import pstats

# Profile function
cProfile.run('db.generate_dashboard()', 'profile.stats')

# Analyze results
stats = pstats.Stats('profile.stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

### Benchmarking

```python
import time

# Benchmark query
iterations = 100
start = time.time()

for _ in range(iterations):
    db.list_jobs(limit=10)

elapsed = time.time() - start
avg_ms = (elapsed / iterations) * 1000

print(f"Average: {avg_ms:.2f}ms")
```

---

## Maintenance

### Database Backup

**Use automated backup scripts (recommended):**

```bash
# Create backup
python3 scripts/backup_db.py

# Create backup before migrations
python3 scripts/backup_db.py --keep 30

# List all backups
python3 scripts/backup_db.py --list
```

**Features:**
- Online backups using SQLite backup API
- Integrity verification
- Automatic cleanup of old backups
- Timestamped filenames with microseconds
- No downtime required

**Backup location:** `~/.claude/backups/`

**Manual backup (legacy):**

```bash
# Simple file copy (database must be idle)
cp ~/.claude/projects.db ~/.claude/projects.db.backup.$(date +%Y%m%d)

# Or use sqlite3 backup command
sqlite3 ~/.claude/projects.db ".backup ~/.claude/projects.db.backup"
```

**Note:** Automated scripts are preferred as they handle online backups safely.

### Database Restore

**Restore from backup:**

```bash
# Interactive restore (with confirmation)
python3 scripts/restore_db.py ~/.claude/backups/projects-backup-20260117-143022-456789.db

# Force restore (no confirmation)
python3 scripts/restore_db.py backup.db --force

# Restore without safety backup
python3 scripts/restore_db.py backup.db --no-backup
```

**Restore process:**
1. Verifies backup integrity
2. Creates safety backup of current database
3. Prompts for confirmation
4. Restores backup
5. Verifies restored database

**Safety backup location:** `~/.claude/lib/projects-pre-restore-YYYYMMDD-HHMMSS.db`

### Backup Testing

**Test backup/restore cycle:**

```bash
# Run backup/restore tests
python3 skills/pm-db/tests/test_backup_restore.py

# Manual verification
python3 scripts/backup_db.py
python3 scripts/restore_db.py --list
```

**Verify backup integrity:**

```bash
# Check backup file
sqlite3 backup.db "PRAGMA integrity_check;"

# Verify schema version
sqlite3 backup.db "SELECT version FROM schema_version ORDER BY version DESC LIMIT 1;"
```

### Vacuum Database

```bash
# Reclaim space (run periodically)
sqlite3 ~/.claude/projects.db "VACUUM;"

# Analyze statistics (improve query plans)
sqlite3 ~/.claude/projects.db "ANALYZE;"
```

### Archive Old Data

```sql
-- Archive completed jobs older than 90 days
CREATE TABLE jobs_archive AS
SELECT * FROM jobs
WHERE status = 'completed'
  AND completed_at < datetime('now', '-90 days');

DELETE FROM jobs
WHERE status = 'completed'
  AND completed_at < datetime('now', '-90 days');

VACUUM;
```

### Monitor Database Size

```bash
# Check database size
ls -lh ~/.claude/projects.db

# Check table sizes
sqlite3 ~/.claude/projects.db "
SELECT name, SUM(pgsize) as size_bytes
FROM dbstat
GROUP BY name
ORDER BY size_bytes DESC
LIMIT 10;
"
```

---

## Release Process

### Version Numbering

- **Major:** Breaking API changes (v2.0.0)
- **Minor:** New features, backward compatible (v1.1.0)
- **Patch:** Bug fixes (v1.0.1)

### Pre-Release Checklist

- [ ] All tests passing
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Migration tested
- [ ] Changelog updated
- [ ] Version bumped

### Release Steps

1. **Update version:**
   ```python
   # In project_database.py
   __version__ = "1.1.0"
   ```

2. **Update CHANGELOG.md:**
   ```markdown
   ## [1.1.0] - 2026-01-17
   ### Added
   - New feature X
   ### Fixed
   - Bug Y
   ```

3. **Run full test suite:**
   ```bash
   python3 skills/pm-db/tests/test_project_database.py
   python3 skills/pm-db/tests/test_integration.py
   python3 skills/pm-db/tests/test_performance.py
   ```

4. **Create git tag:**
   ```bash
   git tag -a v1.1.0 -m "Release 1.1.0"
   git push origin v1.1.0
   ```

5. **Deploy to production:**
   ```bash
   # Backup production database
   cp ~/.claude/projects.db ~/.claude/projects.db.backup.pre-v1.1.0

   # Run migrations
   /pm-db migrate

   # Verify
   /pm-db dashboard
   ```

---

## Contributing

### Contribution Workflow

1. **Create feature branch:**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make changes**
3. **Add tests**
4. **Run tests**
5. **Commit with clear message:**
   ```bash
   git commit -m "Add feature X

   - Implements Y
   - Fixes Z
   - Tests included"
   ```

6. **Push and create PR**

### Code Review Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Type hints included
- [ ] Docstrings complete
- [ ] No SQL injection risks
- [ ] Input validation present
- [ ] Error handling appropriate
- [ ] Performance acceptable

---

## Support and Resources

### Documentation

- [README.md](README.md) - Project overview
- [USER_GUIDE.md](USER_GUIDE.md) - User documentation
- [API_REFERENCE.md](API_REFERENCE.md) - Complete API docs
- [TR.md](../../../job-queue/feature-sqlite-pm-db/docs/TR.md) - Technical requirements
- [FRD.md](../../../job-queue/feature-sqlite-pm-db/docs/FRD.md) - Feature requirements

### Getting Help

1. Check documentation first
2. Search existing issues
3. Run tests to isolate problem
4. Create minimal reproduction
5. Ask for help with context

---

**Version:** 1.0
**Last Updated:** 2026-01-17
**Maintainers:** Claude Code Infrastructure Team
