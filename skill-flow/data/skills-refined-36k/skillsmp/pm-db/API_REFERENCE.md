# PM-DB API Reference

Complete API documentation for the ProjectDatabase class.

## Table of Contents

1. [Overview](#overview)
2. [Database Connection](#database-connection)
3. [Project Management](#project-management)
4. [Specification Management](#specification-management)
5. [Job Management](#job-management)
6. [Task Management](#task-management)
7. [Code Review Management](#code-review-management)
8. [Agent Assignment Management](#agent-assignment-management)
9. [Execution Logging](#execution-logging)
10. [Reporting and Queries](#reporting-and-queries)
11. [Error Handling](#error-handling)
12. [Common Patterns](#common-patterns)

---

## Overview

The `ProjectDatabase` class provides a complete SQLite-based API for project management tracking. It uses:

- **Zero external dependencies** - Python standard library only
- **Parameterized queries** - SQL injection prevention
- **Context managers** - Automatic transaction handling
- **WAL mode** - Better concurrency
- **Foreign keys** - Data integrity enforcement

**Import:**
```python
from lib.project_database import ProjectDatabase
```

---

## Database Connection

### `ProjectDatabase(db_path=None)`

Initialize database connection.

**Parameters:**
- `db_path` (str, optional): Path to SQLite database file. Defaults to `~/.claude/projects.db`

**Raises:**
- `sqlite3.Error`: If database connection fails

**Example:**
```python
# Use default path
db = ProjectDatabase()

# Use custom path
db = ProjectDatabase("/path/to/custom.db")

# Use as context manager (recommended)
with ProjectDatabase() as db:
    # Database operations
    pass
```

**Notes:**
- Automatically enables WAL mode for better concurrency
- Enables foreign key constraints
- Sets row_factory to sqlite3.Row for dict-like access

---

### `close()`

Close database connection.

**Example:**
```python
db = ProjectDatabase()
# ... operations ...
db.close()
```

**Notes:**
- Automatically called when using context manager
- Safe to call multiple times

---

### `transaction()`

Context manager for explicit transactions.

**Yields:**
- None

**Example:**
```python
with ProjectDatabase() as db:
    with db.transaction():
        db.create_project("project1", "Description")
        db.create_project("project2", "Description")
        # Commits on success, rolls back on exception
```

**Notes:**
- Automatically commits on success
- Automatically rolls back on exception
- Can be nested (outer transaction controls)

---

## Project Management

### `create_project(name, description=None, filesystem_path=None)`

Create a new project.

**Parameters:**
- `name` (str): Unique project name (e.g., "message-well")
- `description` (str, optional): Project description
- `filesystem_path` (str, optional): Absolute path to project folder for Memory Bank exports

**Returns:**
- `int`: Project ID

**Raises:**
- `ValueError`: If name is empty or filesystem_path is invalid
- `sqlite3.IntegrityError`: If project name already exists

**Example:**
```python
# Minimal project
project_id = db.create_project("my-app")

# With description
project_id = db.create_project(
    "my-app",
    "My application project"
)

# With Memory Bank path
project_id = db.create_project(
    "my-app",
    "My application project",
    "/home/mark/applications/my-app"
)
```

**Notes:**
- `name` must be unique across all projects
- `filesystem_path` must be absolute if provided
- `filesystem_path` is required for Memory Bank exports
- Name is automatically trimmed of whitespace

---

### `get_project(project_id)`

Get project by ID.

**Parameters:**
- `project_id` (int): Project ID

**Returns:**
- `dict` or `None`: Project dict with keys: id, name, description, filesystem_path, created_at

**Example:**
```python
project = db.get_project(1)
if project:
    print(project['name'])  # "my-app"
    print(project['filesystem_path'])  # "/home/mark/applications/my-app"
```

---

### `get_project_by_name(name)`

Get project by name.

**Parameters:**
- `name` (str): Project name

**Returns:**
- `dict` or `None`: Project dict or None if not found

**Example:**
```python
project = db.get_project_by_name("my-app")
if project:
    print(f"Project ID: {project['id']}")
```

---

### `list_projects()`

List all projects.

**Returns:**
- `list[dict]`: List of project dicts ordered by created_at DESC (newest first)

**Example:**
```python
projects = db.list_projects()
for project in projects:
    print(f"{project['name']}: {project['description']}")
```

---

## Specification Management

### `create_spec(project_id, name, frd_content=None, frs_content=None, gs_content=None, tr_content=None, task_list_content=None, status='draft')`

Create a new specification.

**Parameters:**
- `project_id` (int): Foreign key to projects table
- `name` (str): Spec name (e.g., "feature-auth")
- `frd_content` (str, optional): Full text of FRD.md
- `frs_content` (str, optional): Full text of FRS.md
- `gs_content` (str, optional): Full text of GS.md
- `tr_content` (str, optional): Full text of TR.md
- `task_list_content` (str, optional): Full text of task-list.md
- `status` (str): Spec status (draft, approved, in-progress, completed)

**Returns:**
- `int`: Spec ID

**Raises:**
- `ValueError`: If project_id/name invalid or status not in valid list
- `sqlite3.IntegrityError`: If spec already exists for this project

**Example:**
```python
# Create spec with FRD
spec_id = db.create_spec(
    project_id=1,
    name="feature-auth",
    frd_content="# Authentication Feature\n\n...",
    status="draft"
)

# Import all docs from job-queue
with open("job-queue/feature-auth/docs/FRD.md") as f:
    frd = f.read()
with open("job-queue/feature-auth/docs/task-list.md") as f:
    tasks = f.read()

spec_id = db.create_spec(
    project_id=1,
    name="feature-auth",
    frd_content=frd,
    task_list_content=tasks,
    status="approved"
)
```

**Valid statuses:**
- `draft`: Initial draft
- `approved`: Approved for implementation
- `in-progress`: Currently being implemented
- `completed`: Fully implemented

---

### `get_spec(spec_id)`

Get specification by ID.

**Parameters:**
- `spec_id` (int): Spec ID

**Returns:**
- `dict` or `None`: Spec dict with all fields

**Example:**
```python
spec = db.get_spec(1)
if spec:
    print(spec['name'])
    print(spec['frd_content'][:100])  # First 100 chars
```

---

### `list_specs(project_id=None)`

List specifications, optionally filtered by project.

**Parameters:**
- `project_id` (int, optional): Filter by project ID

**Returns:**
- `list[dict]`: List of spec dicts ordered by created_at DESC

**Example:**
```python
# All specs
all_specs = db.list_specs()

# Specs for specific project
project_specs = db.list_specs(project_id=1)
```

---

## Job Management

### `create_job(spec_id, name, priority='normal', assigned_agent=None, session_id=None)`

Create a new job.

**Parameters:**
- `spec_id` (int, optional): Foreign key to specs table (can be None)
- `name` (str): Job name (e.g., "Build auth feature")
- `priority` (str): Job priority (low, normal, high, critical)
- `assigned_agent` (str, optional): Agent type assigned to job
- `session_id` (str, optional): Unique session identifier

**Returns:**
- `int`: Job ID

**Raises:**
- `ValueError`: If name is empty or priority invalid

**Example:**
```python
# Minimal job
job_id = db.create_job(spec_id=1, name="Build authentication")

# With priority and agent
job_id = db.create_job(
    spec_id=1,
    name="Build authentication",
    priority="high",
    assigned_agent="nextjs-backend-developer"
)

# Job without spec (ad-hoc work)
job_id = db.create_job(
    spec_id=None,
    name="Fix production bug",
    priority="critical"
)
```

**Valid priorities:**
- `low`: Low priority work
- `normal`: Normal priority (default)
- `high`: High priority
- `critical`: Critical/urgent work

**Status flow:**
- Created → `pending`
- Started → `in-progress`
- Completed → `completed` (exit_code=0) or `failed` (exit_code≠0)

---

### `update_job_status(job_id, status, exit_code=None, summary=None)`

Update job status.

**Parameters:**
- `job_id` (int): Job ID
- `status` (str): New status (pending, in-progress, completed, failed, blocked)
- `exit_code` (int, optional): Exit code
- `summary` (str, optional): Summary text

**Raises:**
- `ValueError`: If status is invalid

**Example:**
```python
# Mark as blocked
db.update_job_status(job_id, "blocked", summary="Waiting for API access")

# Mark as failed
db.update_job_status(job_id, "failed", exit_code=1, summary="Tests failed")
```

**Valid statuses:**
- `pending`: Queued for execution
- `in-progress`: Currently executing
- `completed`: Finished successfully
- `failed`: Finished with errors
- `blocked`: Blocked by external dependency

---

### `start_job(job_id)`

Mark job as started (sets status to 'in-progress').

**Parameters:**
- `job_id` (int): Job ID

**Example:**
```python
job_id = db.create_job(spec_id=1, name="Build feature")
db.start_job(job_id)

job = db.get_job(job_id)
print(job['status'])  # "in-progress"
print(job['started_at'])  # "2026-01-17 14:23:00"
```

**Notes:**
- Sets `started_at` timestamp
- Updates `last_activity_at`
- Changes status from `pending` to `in-progress`

---

### `complete_job(job_id, exit_code=0, summary=None)`

Mark job as completed.

**Parameters:**
- `job_id` (int): Job ID
- `exit_code` (int): Exit code (0 = success, non-zero = failure)
- `summary` (str, optional): Completion summary

**Example:**
```python
# Successful completion
db.complete_job(job_id, exit_code=0, summary="All tasks completed")

# Failed completion
db.complete_job(job_id, exit_code=1, summary="Tests failed in task 3")
```

**Notes:**
- Sets status to `completed` (exit_code=0) or `failed` (exit_code≠0)
- Sets `completed_at` timestamp
- Updates `last_activity_at`

---

### `get_job(job_id)`

Get job by ID.

**Parameters:**
- `job_id` (int): Job ID

**Returns:**
- `dict` or `None`: Job dict with all fields

**Example:**
```python
job = db.get_job(1)
if job:
    print(f"Job: {job['name']}")
    print(f"Status: {job['status']}")
    print(f"Priority: {job['priority']}")
```

---

### `list_jobs(spec_id=None, status=None, limit=100)`

List jobs with optional filters.

**Parameters:**
- `spec_id` (int, optional): Filter by spec ID
- `status` (str, optional): Filter by status
- `limit` (int): Maximum number of jobs to return (default: 100)

**Returns:**
- `list[dict]`: List of job dicts ordered by created_at DESC

**Example:**
```python
# All active jobs
active_jobs = db.list_jobs(status='in-progress')

# Jobs for specific spec
spec_jobs = db.list_jobs(spec_id=1)

# All pending jobs (first 50)
pending_jobs = db.list_jobs(status='pending', limit=50)

# All jobs (up to 100)
all_jobs = db.list_jobs()
```

**Notes:**
- Returns most recent jobs first
- LIMIT prevents memory issues with large datasets

---

## Task Management

### `create_task(job_id, name, order=0, dependencies=None)`

Create a new task.

**Parameters:**
- `job_id` (int): Foreign key to jobs table
- `name` (str): Task name
- `order` (int): Task execution order (default: 0)
- `dependencies` (str, optional): JSON array of task IDs this depends on

**Returns:**
- `int`: Task ID

**Raises:**
- `ValueError`: If name is empty

**Example:**
```python
# Simple task
task1_id = db.create_task(job_id, "Setup database", order=1)

# Task with dependencies
task2_id = db.create_task(
    job_id,
    "Run migrations",
    order=2,
    dependencies=json.dumps([task1_id])
)

# Task with multiple dependencies
task3_id = db.create_task(
    job_id,
    "Integration test",
    order=3,
    dependencies=json.dumps([task1_id, task2_id])
)
```

**Notes:**
- `order` determines execution sequence
- `dependencies` must be valid JSON array of integers
- Tasks default to `pending` status

---

### `update_task_status(task_id, status, exit_code=None)`

Update task status.

**Parameters:**
- `task_id` (int): Task ID
- `status` (str): New status (pending, in-progress, completed, failed, blocked)
- `exit_code` (int, optional): Exit code

**Raises:**
- `ValueError`: If status is invalid

**Example:**
```python
# Mark as blocked
db.update_task_status(task_id, "blocked")

# Mark as failed
db.update_task_status(task_id, "failed", exit_code=1)
```

---

### `start_task(task_id)`

Mark task as started.

**Parameters:**
- `task_id` (int): Task ID

**Example:**
```python
task_id = db.create_task(job_id, "Build component")
db.start_task(task_id)

task = db.get_task(task_id)
print(task['status'])  # "in-progress"
```

---

### `complete_task(task_id, exit_code=0)`

Mark task as completed.

**Parameters:**
- `task_id` (int): Task ID
- `exit_code` (int): Exit code (0 = success, non-zero = failure)

**Example:**
```python
# Success
db.complete_task(task_id, exit_code=0)

# Failure
db.complete_task(task_id, exit_code=1)
```

**Notes:**
- Sets status to `completed` (exit_code=0) or `failed` (exit_code≠0)
- Sets `completed_at` timestamp

---

### `get_tasks(job_id)`

Get all tasks for a job.

**Parameters:**
- `job_id` (int): Job ID

**Returns:**
- `list[dict]`: List of task dicts ordered by execution order

**Example:**
```python
tasks = db.get_tasks(job_id)
for task in tasks:
    print(f"{task['order']}: {task['name']} - {task['status']}")
```

---

### `get_task(task_id)`

Get a single task by ID.

**Parameters:**
- `task_id` (int): Task ID

**Returns:**
- `dict` or `None`: Task dict or None if not found

**Example:**
```python
task = db.get_task(123)
if task:
    print(task['name'])
```

---

## Code Review Management

### `add_code_review(job_id, task_id, reviewer, summary, verdict, issues_found=None, files_reviewed=None)`

Add a code review record.

**Parameters:**
- `job_id` (int, optional): Foreign key to jobs table
- `task_id` (int, optional): Foreign key to tasks table
- `reviewer` (str): Reviewer name or agent type
- `summary` (str): Review summary text
- `verdict` (str): Review verdict (approved, changes-requested, rejected)
- `issues_found` (str, optional): JSON array of issues
- `files_reviewed` (str, optional): JSON array of files

**Returns:**
- `int`: Review ID

**Raises:**
- `ValueError`: If reviewer/summary empty or verdict invalid

**Example:**
```python
# Simple approval
review_id = db.add_code_review(
    job_id=job_id,
    task_id=None,
    reviewer="code-reviewer-agent",
    summary="Good code quality, no issues found",
    verdict="approved"
)

# Review with issues
review_id = db.add_code_review(
    job_id=job_id,
    task_id=task_id,
    reviewer="senior-dev",
    summary="Found type safety issues",
    verdict="changes-requested",
    issues_found=json.dumps([
        {"type": "type-safety", "severity": "high", "file": "app.py", "line": 42},
        {"type": "security", "severity": "medium", "file": "auth.py", "line": 15}
    ]),
    files_reviewed=json.dumps(["app.py", "auth.py", "tests/test_app.py"])
)
```

**Valid verdicts:**
- `approved`: Code is acceptable
- `changes-requested`: Changes needed
- `rejected`: Code must be rewritten

---

### `get_code_reviews(job_id=None, task_id=None)`

Get code reviews, optionally filtered by job or task.

**Parameters:**
- `job_id` (int, optional): Filter by job ID
- `task_id` (int, optional): Filter by task ID

**Returns:**
- `list[dict]`: List of code review dicts ordered by created_at DESC

**Example:**
```python
# All reviews for job
reviews = db.get_code_reviews(job_id=job_id)

# All reviews for task
reviews = db.get_code_reviews(task_id=task_id)

# All reviews
all_reviews = db.get_code_reviews()
```

---

## Agent Assignment Management

### `assign_agent(agent_type, job_id=None, task_id=None)`

Record an agent assignment.

**Parameters:**
- `agent_type` (str): Type of agent (e.g., "python-backend-developer")
- `job_id` (int, optional): Job ID
- `task_id` (int, optional): Task ID

**Returns:**
- `int`: Assignment ID

**Raises:**
- `ValueError`: If agent_type is empty or both job_id and task_id are None

**Example:**
```python
# Assign agent to job
assignment_id = db.assign_agent("nextjs-backend-developer", job_id=job_id)

# Assign agent to task
assignment_id = db.assign_agent("qa-engineer", task_id=task_id)
```

---

### `complete_agent_work(assignment_id, exit_code=0)`

Mark agent assignment as completed.

**Parameters:**
- `assignment_id` (int): Assignment ID
- `exit_code` (int): Exit code (0 = success, non-zero = failure)

**Example:**
```python
assignment_id = db.assign_agent("qa-engineer", task_id=task_id)
# ... agent does work ...
db.complete_agent_work(assignment_id, exit_code=0)
```

---

### `get_agent_assignments(job_id=None, task_id=None)`

Get agent assignments, optionally filtered by job or task.

**Parameters:**
- `job_id` (int, optional): Filter by job ID
- `task_id` (int, optional): Filter by task ID

**Returns:**
- `list[dict]`: List of agent assignment dicts ordered by assigned_at DESC

**Example:**
```python
# All assignments for job
assignments = db.get_agent_assignments(job_id=job_id)

# All assignments for task
assignments = db.get_agent_assignments(task_id=task_id)
```

---

## Execution Logging

### `log_execution(job_id, task_id, command, output=None, exit_code=None, duration_ms=None)`

Log a command execution.

**Parameters:**
- `job_id` (int): Job ID
- `task_id` (int, optional): Task ID
- `command` (str): Command that was executed
- `output` (str, optional): Command output (stdout + stderr)
- `exit_code` (int, optional): Exit code
- `duration_ms` (int, optional): Duration in milliseconds

**Returns:**
- `int`: Log ID

**Raises:**
- `ValueError`: If command is empty

**Example:**
```python
import time

# Log command execution
start = time.time()
result = subprocess.run(["npm", "test"], capture_output=True, text=True)
duration_ms = int((time.time() - start) * 1000)

log_id = db.log_execution(
    job_id=job_id,
    task_id=task_id,
    command="npm test",
    output=result.stdout + result.stderr,
    exit_code=result.returncode,
    duration_ms=duration_ms
)
```

**Notes:**
- Output is automatically truncated if > 50KB
- Useful for debugging and audit trails

---

### `get_execution_logs(job_id=None, task_id=None, limit=100)`

Get execution logs, optionally filtered by job or task.

**Parameters:**
- `job_id` (int, optional): Filter by job ID
- `task_id` (int, optional): Filter by task ID
- `limit` (int): Maximum number of logs to return (default: 100)

**Returns:**
- `list[dict]`: List of execution log dicts ordered by executed_at DESC

**Example:**
```python
# All logs for job
logs = db.get_execution_logs(job_id=job_id)

# All logs for task
logs = db.get_execution_logs(task_id=task_id)

# Recent 10 logs
logs = db.get_execution_logs(limit=10)
```

---

### `search_execution_logs(job_id=None, task_id=None, command_pattern=None, output_pattern=None, exit_code=None, start_date=None, end_date=None, limit=100)`

Search execution logs with multiple filter criteria.

**Parameters:**
- `job_id` (int, optional): Filter by job ID
- `task_id` (int, optional): Filter by task ID
- `command_pattern` (str, optional): SQL LIKE pattern for command text
- `output_pattern` (str, optional): SQL LIKE pattern for output text
- `exit_code` (int, optional): Filter by exit code (exact match)
- `start_date` (str, optional): Start date (ISO format: YYYY-MM-DD HH:MM:SS)
- `end_date` (str, optional): End date (ISO format: YYYY-MM-DD HH:MM:SS)
- `limit` (int): Maximum results (default: 100)

**Returns:**
- `list[dict]`: List of execution log dicts matching criteria

**Example:**
```python
# Search for failed commands
failed = db.search_execution_logs(exit_code=1)

# Search for pytest commands
pytest_logs = db.search_execution_logs(command_pattern='%pytest%')

# Search for output containing "error"
errors = db.search_execution_logs(output_pattern='%error%')

# Search for pytest commands in last week
recent_pytest = db.search_execution_logs(
    command_pattern='%pytest%',
    start_date='2026-01-10 00:00:00'
)

# Complex search: failed npm commands with error output
npm_errors = db.search_execution_logs(
    command_pattern='%npm%',
    output_pattern='%error%',
    exit_code=1
)
```

**Notes:**
- Patterns use SQL LIKE syntax (% for wildcard)
- Case-insensitive matching
- Multiple filters are AND-ed together
- Returns most recent matches first

---

## Reporting and Queries

### `generate_dashboard()`

Generate status dashboard with job metrics.

**Returns:**
- `dict`: Dashboard dict with:
  - `active_jobs`: List of in-progress jobs
  - `pending_jobs`: List of pending jobs
  - `recent_completions`: Jobs completed in last 7 days
  - `velocity`: This week vs last week completion metrics

**Example:**
```python
dashboard = db.generate_dashboard()

print(f"Active: {len(dashboard['active_jobs'])}")
print(f"Pending: {len(dashboard['pending_jobs'])}")
print(f"Completed this week: {dashboard['velocity']['this_week']}")
print(f"Velocity trend: {dashboard['velocity']['trend_percent']}%")

# List active jobs
for job in dashboard['active_jobs']:
    print(f"- {job['name']} (started {job['started_at']})")
```

**Dashboard structure:**
```python
{
    'active_jobs': [...],  # In-progress jobs
    'pending_jobs': [...],  # Queued jobs
    'recent_completions': [...],  # Last 7 days
    'velocity': {
        'this_week': 12,  # Jobs completed this week
        'last_week': 8,   # Jobs completed last week
        'trend_percent': 50.0  # +50% velocity
    }
}
```

---

### `get_job_timeline(job_id)`

Get complete timeline of events for a job.

**Parameters:**
- `job_id` (int): Job ID

**Returns:**
- `list[dict]`: List of timeline events sorted chronologically

**Example:**
```python
timeline = db.get_job_timeline(job_id)

for event in timeline:
    print(f"{event['timestamp']}: {event['type']}")
    if event['type'] == 'task_completed':
        print(f"  Task: {event['data']['name']}")
    elif event['type'] == 'code_review':
        print(f"  Verdict: {event['data']['verdict']}")
```

**Event types:**
- `job_created`: Job was created
- `job_started`: Job execution started
- `job_completed`: Job finished
- `task_created`: Task was created
- `task_started`: Task execution started
- `task_completed`: Task finished
- `code_review`: Code review added

---

### `get_dependency_graph(job_id)`

Get task dependency graph for a job.

**Parameters:**
- `job_id` (int): Job ID

**Returns:**
- `dict`: Graph with nodes (tasks) and edges (dependencies)

**Example:**
```python
graph = db.get_dependency_graph(job_id)

print("Tasks:")
for node in graph['nodes']:
    print(f"  {node['id']}: {node['name']} ({node['status']})")

print("Dependencies:")
for edge in graph['edges']:
    print(f"  Task {edge['from']} → Task {edge['to']}")
```

**Graph structure:**
```python
{
    'nodes': [
        {'id': 1, 'name': 'Setup DB', 'status': 'completed', 'order': 1},
        {'id': 2, 'name': 'Run migrations', 'status': 'in-progress', 'order': 2}
    ],
    'edges': [
        {'from': 1, 'to': 2}  # Task 2 depends on Task 1
    ]
}
```

---

### `get_code_review_metrics(job_id=None, start_date=None, end_date=None)`

Get aggregated code review metrics and statistics.

**Parameters:**
- `job_id` (int, optional): Filter by job ID
- `start_date` (str, optional): Start date (ISO format: YYYY-MM-DD HH:MM:SS)
- `end_date` (str, optional): End date (ISO format: YYYY-MM-DD HH:MM:SS)

**Returns:**
- `dict`: Review metrics including:
  - `total_reviews`: Total number of reviews
  - `verdict_distribution`: Count by verdict
  - `avg_issues_per_review`: Average issues found
  - `reviewer_activity`: Reviews per reviewer
  - `common_issues`: Top issue types
  - `recent_reviews`: Last 10 reviews

**Example:**
```python
# Get metrics for all reviews
metrics = db.get_code_review_metrics()

print(f"Total reviews: {metrics['total_reviews']}")
print(f"Approval rate: {metrics['verdict_distribution'].get('approved', 0) / metrics['total_reviews'] * 100:.1f}%")
print(f"Avg issues: {metrics['avg_issues_per_review']}")

# Top reviewers
for r in metrics['reviewer_activity'][:5]:
    print(f"  {r['reviewer']}: {r['review_count']} reviews")

# Common issues
for issue in metrics['common_issues'][:5]:
    print(f"  {issue['issue_type']}: {issue['count']} occurrences")
```

**Metrics structure:**
```python
{
    'total_reviews': 45,
    'verdict_distribution': {
        'approved': 32,
        'changes-requested': 10,
        'rejected': 3
    },
    'avg_issues_per_review': 2.3,
    'reviewer_activity': [
        {'reviewer': 'code-reviewer', 'review_count': 25},
        {'reviewer': 'senior-dev', 'review_count': 20}
    ],
    'common_issues': [
        {'issue_type': 'type-safety', 'count': 15},
        {'issue_type': 'security', 'count': 8}
    ],
    'recent_reviews': [...]  # Last 10 reviews
}
```

---

## Error Handling

All methods use exceptions for error handling:

### `ValueError`

Raised when input validation fails:
- Empty required fields (name, command, etc.)
- Invalid enum values (status, priority, verdict)
- Invalid filesystem paths

**Example:**
```python
try:
    db.create_project("")  # Empty name
except ValueError as e:
    print(f"Error: {e}")  # "Project name cannot be empty"
```

---

### `sqlite3.IntegrityError`

Raised when database constraints are violated:
- Duplicate project names
- Foreign key violations
- Unique constraint violations

**Example:**
```python
try:
    db.create_project("my-app")
    db.create_project("my-app")  # Duplicate
except sqlite3.IntegrityError as e:
    print(f"Database error: {e}")
```

---

### `sqlite3.Error`

Raised for general database errors:
- Connection failures
- Invalid SQL
- File permissions

**Example:**
```python
try:
    db = ProjectDatabase("/invalid/path/db.sqlite")
except sqlite3.Error as e:
    print(f"Database error: {e}")
```

---

## Common Patterns

### Pattern 1: Create and Execute Job

```python
from lib.project_database import ProjectDatabase
import json

with ProjectDatabase() as db:
    # Create project
    project_id = db.create_project(
        "my-app",
        "My application",
        "/home/mark/applications/my-app"
    )

    # Create spec
    spec_id = db.create_spec(
        project_id,
        "feature-auth",
        frd_content="# Authentication\n..."
    )

    # Create job
    job_id = db.create_job(
        spec_id,
        "Build authentication",
        priority="high",
        assigned_agent="nextjs-backend-developer"
    )

    # Start job
    db.start_job(job_id)

    # Create tasks
    task1 = db.create_task(job_id, "Setup API", order=1)
    task2 = db.create_task(
        job_id,
        "Add tests",
        order=2,
        dependencies=json.dumps([task1])
    )

    # Execute tasks
    db.start_task(task1)
    # ... do work ...
    db.complete_task(task1, exit_code=0)

    db.start_task(task2)
    # ... do work ...
    db.complete_task(task2, exit_code=0)

    # Add code review
    db.add_code_review(
        job_id,
        None,
        "code-reviewer",
        "Excellent work",
        "approved"
    )

    # Complete job
    db.complete_job(job_id, exit_code=0, summary="All tasks completed")
```

---

### Pattern 2: Monitor Dashboard

```python
from lib.project_database import ProjectDatabase

def print_dashboard():
    with ProjectDatabase() as db:
        dashboard = db.generate_dashboard()

        print("━━━ PM-DB Dashboard ━━━")
        print(f"\nActive Jobs: {len(dashboard['active_jobs'])}")
        for job in dashboard['active_jobs']:
            print(f"  • {job['name']} (priority: {job['priority']})")

        print(f"\nPending Jobs: {len(dashboard['pending_jobs'])}")
        for job in dashboard['pending_jobs'][:5]:
            print(f"  • {job['name']}")

        print(f"\nRecent Completions: {len(dashboard['recent_completions'])}")
        print(f"Velocity: {dashboard['velocity']['this_week']} this week")
        print(f"          {dashboard['velocity']['last_week']} last week")
        print(f"          {dashboard['velocity']['trend_percent']:+.1f}% trend")

print_dashboard()
```

---

### Pattern 3: Bulk Import from Job Queue

```python
from pathlib import Path
from lib.project_database import ProjectDatabase

def import_spec_from_folder(db, project_id, folder_path):
    """Import spec from job-queue folder"""
    folder = Path(folder_path)
    docs_dir = folder / "docs"

    if not docs_dir.exists():
        return None

    # Read all spec files
    frd = (docs_dir / "FRD.md").read_text() if (docs_dir / "FRD.md").exists() else None
    frs = (docs_dir / "FRS.md").read_text() if (docs_dir / "FRS.md").exists() else None
    gs = (docs_dir / "GS.md").read_text() if (docs_dir / "GS.md").exists() else None
    tr = (docs_dir / "TR.md").read_text() if (docs_dir / "TR.md").exists() else None
    tasks = (docs_dir / "task-list.md").read_text() if (docs_dir / "task-list.md").exists() else None

    # Create spec
    spec_id = db.create_spec(
        project_id,
        folder.name,
        frd_content=frd,
        frs_content=frs,
        gs_content=gs,
        tr_content=tr,
        task_list_content=tasks,
        status="approved"
    )

    return spec_id

# Import all specs from job-queue
with ProjectDatabase() as db:
    project_id = db.get_project_by_name("my-app")['id']

    job_queue = Path.home() / ".claude" / "job-queue"
    for folder in job_queue.glob("feature-*"):
        spec_id = import_spec_from_folder(db, project_id, folder)
        if spec_id:
            print(f"✅ Imported: {folder.name}")
```

---

### Pattern 4: Advanced Reporting

```python
from lib.project_database import ProjectDatabase

def generate_project_report(project_id):
    with ProjectDatabase() as db:
        project = db.get_project(project_id)
        specs = db.list_specs(project_id)

        print(f"Project: {project['name']}")
        print(f"Specs: {len(specs)}")

        for spec in specs:
            jobs = db.list_jobs(spec_id=spec['id'])
            print(f"\n  Spec: {spec['name']} ({spec['status']})")
            print(f"  Jobs: {len(jobs)}")

            for job in jobs:
                tasks = db.get_tasks(job['id'])
                reviews = db.get_code_reviews(job_id=job['id'])

                print(f"    Job: {job['name']} - {job['status']}")
                print(f"      Tasks: {len(tasks)}")
                print(f"      Reviews: {len(reviews)}")

                # Task breakdown
                completed = sum(1 for t in tasks if t['status'] == 'completed')
                print(f"      Progress: {completed}/{len(tasks)} tasks")

generate_project_report(1)
```

---

### Pattern 5: Search and Debug

```python
from lib.project_database import ProjectDatabase

def find_failed_commands():
    """Find all failed command executions"""
    with ProjectDatabase() as db:
        failed = db.search_execution_logs(exit_code=1, limit=50)

        print(f"Found {len(failed)} failed commands\n")

        for log in failed:
            print(f"Time: {log['executed_at']}")
            print(f"Command: {log['command']}")
            if log['output']:
                print(f"Output: {log['output'][:200]}...")
            print()

def find_review_issues():
    """Find common code review issues"""
    with ProjectDatabase() as db:
        metrics = db.get_code_review_metrics()

        print("Common Issues:")
        for issue in metrics['common_issues']:
            print(f"  {issue['issue_type']}: {issue['count']} occurrences")

find_failed_commands()
find_review_issues()
```

---

## Performance Tips

1. **Use LIMIT for large queries**
   ```python
   # Good - limits result set
   jobs = db.list_jobs(limit=100)

   # Bad - may return thousands of rows
   jobs = db.list_jobs(limit=999999)
   ```

2. **Use context managers**
   ```python
   # Good - automatic cleanup
   with ProjectDatabase() as db:
       # operations

   # Less ideal - manual cleanup
   db = ProjectDatabase()
   # operations
   db.close()
   ```

3. **Use transactions for bulk operations**
   ```python
   with ProjectDatabase() as db:
       with db.transaction():
           for i in range(100):
               db.create_task(job_id, f"Task {i}", order=i)
       # Single commit at end
   ```

4. **Archive old data**
   ```python
   # Move completed jobs to archive table
   # Keep active dataset small for fast queries
   ```

---

## See Also

- [User Guide](USER_GUIDE.md) - Complete usage guide
- [README](README.md) - Project overview
- [TR.md](../../../job-queue/feature-sqlite-pm-db/docs/TR.md) - Technical requirements

---

**Version:** 1.0
**Last Updated:** 2026-01-17
