---
name: import-tasks
description: This skill should be used when you need to import tasks from another Claude Code session's TaskList into your current session, enabling coordination across sessions without restarting.
argument-hint: "[TaskList ID (UUID)]"
---

# Import Tasks from Another Session

Import tasks from another Claude Code session's TaskList into your current session.

## When to Use

- When picking up work from a `/workflows:plan` that created tasks
- When coordinating with another Claude session
- When you want to continue work started in a different session
- When a subagent needs to work on tasks from the main session

## How It Works

Each Claude Code session has its own TaskList stored at:
```
~/.claude/tasks/[session-uuid]/
├── 1.json
├── 2.json
└── ...
```

This skill reads tasks from another session and recreates them in your current session using TaskCreate, preserving descriptions, status, and dependencies.

## Usage

**Input:** TaskList ID (the UUID from the plan's `task_list_id` frontmatter or from another session)

```
skill: import-tasks a69ce44f-1559-4052-89e2-66605323adca
```

## Execution Steps

### 1. Validate the TaskList exists

```bash
task_list_id="$ARGUMENTS"

if [ -z "$task_list_id" ]; then
  echo "Error: No TaskList ID provided"
  echo "Usage: skill import-tasks [TaskList ID]"
  exit 1
fi

if [ ! -d ~/.claude/tasks/$task_list_id ]; then
  echo "Error: TaskList not found at ~/.claude/tasks/$task_list_id"
  echo ""
  echo "Available TaskLists:"
  ls -la ~/.claude/tasks/
  exit 1
fi
```

### 2. Read and display tasks from source

```bash
echo "Tasks in source TaskList $task_list_id:"
echo ""
for f in ~/.claude/tasks/$task_list_id/*.json; do
  cat "$f" | jq -r '"#\(.id) [\(.status)] \(.subject)"'
done
```

### 3. Import tasks into current session

For each task in the source TaskList:

1. **Read the task JSON:**
   ```bash
   cat ~/.claude/tasks/$task_list_id/1.json | jq .
   ```

2. **Create in current session:**
   ```
   TaskCreate:
     subject: [from source task]
     description: [from source task]
     activeForm: [from source task]
   ```

3. **Note the ID mapping** (source ID → new ID) for dependency resolution

4. **After all tasks created, set up dependencies:**
   ```
   TaskUpdate: task #[new_id] addBlockedBy [mapped_dependency_ids]
   ```

### 4. Verify import

```
TaskList  # Should show all imported tasks
```

### 5. Report completion

```
Imported X tasks from TaskList [source_id]

ID Mapping:
- Source #1 → Current #1: [subject]
- Source #2 → Current #2: [subject]
...

Ready to execute. Use TaskList to see available work.
```

## Example

**From a plan file with:**
```yaml
---
title: Add user authentication
task_list_id: a69ce44f-1559-4052-89e2-66605323adca
---
```

**Import the tasks:**
```
skill: import-tasks a69ce44f-1559-4052-89e2-66605323adca
```

**Result:**
```
Imported 5 tasks from TaskList a69ce44f-1559-4052-89e2-66605323adca

ID Mapping:
- Source #1 → Current #1: Implement User model
- Source #2 → Current #2: Add authentication service
- Source #3 → Current #3: Create login endpoint
- Source #4 → Current #4: Add session middleware
- Source #5 → Current #5: Write integration tests

Dependencies preserved:
- #5 blocked by #1, #2, #3, #4

Ready to execute. Use TaskList to see available work.
```

## Notes

- Tasks are **copied**, not moved - source TaskList remains unchanged
- Task IDs in the new session may differ from source (use the mapping)
- Dependencies are automatically remapped to new IDs
- Status is preserved (pending/in_progress/completed)
- If current session already has tasks, imported tasks get new IDs (no conflicts)
