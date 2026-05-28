---
name: things-search
description: Search tasks in Things 3 with keyword and filter options
version: 1.0.0
allowed-tools: [Bash]
---

# Search Tasks in Things 3

Find tasks using keywords and powerful filtering options.

## How to Search Tasks

```python
import os, sys
sys.path.insert(0, os.path.expanduser('~/.claude/skills/things/lib'))
from reader import ThingsReader
from helpers import ThingsFormatter

# Search with filters
results = ThingsReader.search(
    query="blog",           # Required: search term
    status="incomplete",    # Optional: incomplete, completed, canceled
    area="Work",            # Optional: filter by area name
    project="Content",      # Optional: filter by project name
    tag="urgent"            # Optional: filter by tag name
)

# Display results
if results:
    print(f"Found {len(results)} task(s) matching 'blog'\n")
    print(ThingsFormatter.format_task_list(results, verbose=True, show_uuid=True))
else:
    print("No tasks found matching your criteria.")
```

## Available Filters

| Filter | Description | Example |
|--------|-------------|---------|
| `query` | Keyword in title/notes | "blog" |
| `status` | Task status | incomplete, completed, canceled |
| `area` | Filter by area | "Work", "Personal" |
| `project` | Filter by project | "Marketing" |
| `tag` | Filter by tag | "urgent" |

## Instructions

1. **Parse** the user's search request for keywords and filters
2. **Search** using `ThingsReader.search()` with appropriate parameters
3. **Display** results with `ThingsFormatter.format_task_list()`
4. **Include UUIDs** for follow-up actions
5. **Suggest** broadening search if no results

## Examples

**User**: "Find all tasks with 'meeting' in them"
```python
results = ThingsReader.search(query="meeting")
```

**User**: "Show incomplete tasks in Marketing area tagged urgent"
```python
results = ThingsReader.search(
    query="",  # Empty query matches all
    status="incomplete",
    area="Marketing",
    tag="urgent"
)
```

**User**: "What completed tasks mention 'deployment'?"
```python
results = ThingsReader.search(
    query="deployment",
    status="completed"
)
```

## Example Output

```
Found 3 task(s) matching 'blog'

[ ] Write blog post [ABC-123]
    Focus on API design patterns
    Tags: writing, work
    Project: Content Creation
    Area: Work

[ ] Edit blog images [DEF-456]
    Project: Content Creation

[x] Research blog topics [GHI-789]
    Found 5 good topics
    Tags: research
```

## Pro Tips

- Empty query ("") with filters browses by area/project/tag
- Default to `status="incomplete"` unless user asks for completed
- Combine filters to narrow large lists
