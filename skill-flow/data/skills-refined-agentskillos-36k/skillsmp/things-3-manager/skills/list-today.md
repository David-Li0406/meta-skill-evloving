---
name: things-list-today
description: View all tasks scheduled for today in Things 3
version: 1.0.0
allowed-tools: [Bash]
---

# List Today's Tasks from Things 3

Display all tasks scheduled for today with full context.

## How to List Today's Tasks

```python
import os, sys
sys.path.insert(0, os.path.expanduser('~/.claude/skills/things/lib'))
from reader import ThingsReader
from helpers import ThingsFormatter

# Get today's tasks
tasks = ThingsReader.get_today()

# Format and display
if tasks:
    print(f"Today's Tasks ({len(tasks)})\n")
    print(ThingsFormatter.format_task_list(tasks, verbose=True, show_uuid=True))
    print("\n" + ThingsFormatter.summarize_tasks(tasks))
else:
    print("No tasks scheduled for today!")
```

## Display Options

| Option | Default | Description |
|--------|---------|-------------|
| `verbose` | True | Include notes, tags, project |
| `show_uuid` | True | Show UUIDs for follow-up actions |
| `group_by` | None | Group by 'project' or 'area' |

## Instructions

1. **Fetch** today's tasks using `ThingsReader.get_today()`
2. **Format** using `ThingsFormatter.format_task_list()`
3. **Display** summary using `ThingsFormatter.summarize_tasks()`
4. **Always show UUIDs** so users can complete tasks easily

## Example Output

```
Today's Tasks (3)

[ ] Write blog post [ABC-123]
    Focus on API design patterns
    Tags: writing, work
    Project: Content Creation

[ ] Call dentist [DEF-456]
    Tags: health, calls

[x] Review pull request [GHI-789]
    Project: Engineering

Summary: 3 total (2 incomplete, 1 completed)
```

## User Variations

- "What's on my plate today?" -> List today
- "Show me today's tasks" -> List today
- "List today grouped by project" -> Use `group_by='project'`
