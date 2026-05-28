---
name: things-add-task
description: Add a new task to Things 3 with notes, tags, dates, deadlines, and checklists
version: 1.0.0
allowed-tools: [Bash]
---

# Add Task to Things 3

Create a new task in Things 3 based on the user's natural language request.

## Available Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `title` | Yes | Task title | "Write blog post" |
| `notes` | No | Detailed notes | "Focus on API design" |
| `when` | No | Schedule date | today, tomorrow, evening, anytime, someday, YYYY-MM-DD |
| `deadline` | No | Due date | "2025-12-01" |
| `tags` | No | List of tags | ["work", "urgent"] |
| `list_name` | No | Project or area | "Marketing" |
| `checklist_items` | No | Subtasks | ["Step 1", "Step 2"] |

## How to Add a Task

```python
import os, sys
sys.path.insert(0, os.path.expanduser('~/.claude/skills/things/lib'))
from writer import ThingsWriter

# Add a task
ThingsWriter.add_task(
    title="Write blog post",
    notes="Focus on API design patterns",
    when="today",
    tags=["writing", "work"]
)

print("Task added to Things!")
```

## Instructions

1. **Parse** the user's request to extract task details
2. **Call** `ThingsWriter.add_task()` with appropriate parameters
3. **Confirm** the task was added successfully
4. **Ask** clarifying questions if the request is ambiguous

## Examples

**User**: "Add a task to call the dentist tomorrow with tag health"
```python
ThingsWriter.add_task(
    title="Call dentist",
    when="tomorrow",
    tags=["health"]
)
```

**User**: "Create task to review Q4 report in Work project, due December 1st"
```python
ThingsWriter.add_task(
    title="Review Q4 report",
    list_name="Work",
    deadline="2025-12-01"
)
```

**User**: "Add 'Plan vacation' with checklist: book flights, reserve hotel, pack"
```python
ThingsWriter.add_task(
    title="Plan vacation",
    checklist_items=["Book flights", "Reserve hotel", "Pack bags"]
)
```

## Output

Confirm success:
```
Task added to Things!

Title: Call dentist
Scheduled: Tomorrow
Tags: health
```
