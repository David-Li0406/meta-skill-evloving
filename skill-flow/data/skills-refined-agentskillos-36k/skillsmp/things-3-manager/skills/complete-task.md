---
name: things-complete-task
description: Mark tasks as complete in Things 3 by UUID or title
version: 1.0.0
allowed-tools: [Bash]
---

# Complete Task in Things 3

Mark one or more tasks as complete.

## How to Complete a Task

```python
import os, sys
sys.path.insert(0, os.path.expanduser('~/.claude/skills/things/lib'))
from reader import ThingsReader
from writer import ThingsWriter

# Option 1: Complete by UUID (most reliable)
task_id = "ABC-123-DEF-456"
ThingsWriter.complete_task(task_id)
print(f"Task {task_id} marked as complete!")

# Option 2: Find by title and complete
tasks = ThingsReader.find_by_title("Write blog post")
if tasks:
    task = tasks[0]
    ThingsWriter.complete_task(task['uuid'])
    print(f"Completed: {task['title']}")
else:
    print("Task not found")
```

## Methods

| Method | When to Use |
|--------|-------------|
| By UUID | User provides UUID from list output |
| By Title | User references task by name |
| Batch | User wants to complete multiple tasks |

## Instructions

1. **Identify** the task(s) to complete:
   - Use UUID directly if provided
   - Search by title if referenced by name
2. **Handle multiple matches** by showing options
3. **Complete** using `ThingsWriter.complete_task(uuid)`
4. **Confirm** with success message

## Examples

**User**: "Mark task ABC-123 as done"
```python
ThingsWriter.complete_task("ABC-123")
print("Task ABC-123 completed!")
```

**User**: "Complete the dentist task"
```python
tasks = ThingsReader.find_by_title("dentist")
if len(tasks) == 1:
    ThingsWriter.complete_task(tasks[0]['uuid'])
    print(f"Completed: {tasks[0]['title']}")
elif len(tasks) > 1:
    print("Multiple matches found:")
    for i, t in enumerate(tasks, 1):
        print(f"{i}. {t['title']} [{t['uuid']}]")
    print("Which one?")
```

**User**: "Mark all today tasks as complete"
```python
today_tasks = ThingsReader.get_today()
incomplete = [t for t in today_tasks if t['status'] == 'incomplete']

for task in incomplete:
    ThingsWriter.complete_task(task['uuid'])
    print(f"Completed: {task['title']}")

print(f"\nAll {len(incomplete)} tasks completed!")
```

## Auth Token Required

Completing tasks requires an auth token. If you get an auth error:

1. Open Things 3 -> Preferences -> General
2. Check "Enable Things URLs"
3. Copy the auth token
4. Save it:
   ```bash
   export THINGS_AUTH_TOKEN="your-token"
   ```

See `README.md` for permanent setup.

## Example Output

```
Task completed: Call dentist

Task marked as complete in Things 3!
```

**Multiple matches:**
```
Found 3 tasks matching 'blog':
1. Write blog post [ABC-123] - Content Creation
2. Edit blog images [DEF-456] - Content Creation
3. Review blog draft [GHI-789] - Marketing

Which one would you like to complete? (1-3)
```
