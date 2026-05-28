---
name: things-list-inbox
description: View inbox tasks in Things 3 that need to be triaged
version: 1.0.0
allowed-tools: [Bash]
---

# List Inbox Tasks from Things 3

Display tasks in the inbox that need to be organized and scheduled.

## How to List Inbox Tasks

```python
import os, sys
sys.path.insert(0, os.path.expanduser('~/.claude/skills/things/lib'))
from reader import ThingsReader
from helpers import ThingsFormatter

# Get inbox tasks
tasks = ThingsReader.get_inbox()

# Format and display
if tasks:
    print(f"Inbox ({len(tasks)} tasks to triage)\n")
    print(ThingsFormatter.format_task_list(tasks, verbose=True, show_uuid=True))
    print("\n" + ThingsFormatter.summarize_tasks(tasks))
else:
    print("Inbox is empty! Everything is organized.")
```

## Purpose of Inbox

The inbox contains:
- Newly captured tasks not yet organized
- Tasks needing scheduling or project assignment
- Quick captures waiting for processing

This is typically used during daily/weekly reviews.

## Instructions

1. **Fetch** inbox tasks using `ThingsReader.get_inbox()`
2. **Format** using `ThingsFormatter.format_task_list()`
3. **Display** summary
4. **Suggest** organizing actions if inbox is large

## Example Output

```
Inbox (5 tasks to triage)

[ ] Research new framework [ABC-123]
    Look into React 19 features

[ ] Buy groceries [DEF-456]
    Tags: personal, errands

[ ] Schedule team meeting [GHI-789]
    Discuss Q1 roadmap
    Tags: work, meetings

[ ] Read article on AI [JKL-012]

[ ] Fix bug in login flow [MNO-345]
    Tags: urgent, bugs

Summary: 5 total (5 incomplete, 4 tagged)
```

## Pro Tips

- Empty inbox = good organization
- Suggest scheduling or adding to projects
- Tasks with tags are partially organized
