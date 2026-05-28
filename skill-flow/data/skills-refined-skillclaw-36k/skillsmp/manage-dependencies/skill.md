---
name: manage-dependencies
description: Add, remove, or query task dependencies in the local tasks database
allowed-tools: Bash
---

# Manage Dependencies Skill

Manages task dependencies in the local `tasks.db` SQLite database. Dependencies define which tasks must be completed before another task can be started.

## Commands

### Add a dependency

Make a task depend on another task (the dependency must be completed first):

```bash
python3 scripts/manage_dependencies.py add <task_id> <depends_on_id>
```

Example: Task 5 cannot start until Task 3 is done:
```bash
python3 scripts/manage_dependencies.py add 5 3
```

### Remove a dependency

Remove a dependency relationship:

```bash
python3 scripts/manage_dependencies.py remove <task_id> <depends_on_id>
```

### List dependencies for a task

Show all tasks that must be completed before a specific task can start:

```bash
python3 scripts/manage_dependencies.py list <task_id>
```

### List dependents of a task

Show all tasks that are waiting on a specific task:

```bash
python3 scripts/manage_dependencies.py dependents <task_id>
```

### Show blocked tasks

List all tasks that cannot be started because their dependencies are incomplete:

```bash
python3 scripts/manage_dependencies.py blocked
```

### Show ready tasks

List all tasks that are ready to start (all dependencies complete or no dependencies):

```bash
python3 scripts/manage_dependencies.py ready
```

### Show all dependencies

Display all dependency relationships in the system:

```bash
python3 scripts/manage_dependencies.py all
```

## Usage Examples

**Setting up a dependency chain:**
```bash
# Task 10 (Deploy feature) depends on Task 8 (Write tests)
python3 scripts/manage_dependencies.py add 10 8

# Task 8 (Write tests) depends on Task 5 (Implement feature)
python3 scripts/manage_dependencies.py add 8 5
```

**Checking what's blocking a task:**
```bash
python3 scripts/manage_dependencies.py list 10
```

**Finding what a completed task unblocks:**
```bash
python3 scripts/manage_dependencies.py dependents 5
```

**Finding work that can be started now:**
```bash
python3 scripts/manage_dependencies.py ready
```

## Validation

The script automatically validates:

- **Task existence**: Both tasks must exist in the database
- **Self-dependency**: A task cannot depend on itself
- **Circular dependencies**: Adding a dependency that would create a cycle is rejected

## Error Handling

- If a task ID doesn't exist, an error message is displayed
- If a dependency already exists, it reports "Dependency already exists"
- If removing a non-existent dependency, it reports "No dependency found"
- Circular dependency attempts are blocked with an error message

## Arguments

Parse the user's request to determine:
1. The command (add, remove, list, dependents, blocked, ready, all)
2. The task IDs involved (if applicable)

Then run the appropriate command from the examples above.
