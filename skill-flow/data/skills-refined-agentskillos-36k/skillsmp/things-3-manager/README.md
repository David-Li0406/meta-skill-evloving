# Things 3 Skills for Claude Code

Comprehensive task management integration with Things 3 using natural language commands through Claude Code.

## Overview

This skill set provides seamless integration between Claude Code and Things 3, allowing you to manage your tasks using natural language. It combines fast database reads with the official Things URL scheme for reliable, feature-rich task management.

### What You Can Do

- ✅ **Add tasks** with notes, tags, dates, deadlines, and checklists
- 📅 **View today's schedule** with full context
- 📥 **Review inbox** for task triage
- 🔍 **Search tasks** with powerful filtering
- ✓ **Complete tasks** by title or UUID
- 📊 **Get summaries** of your task lists

## Quick Start

### 1. Install Dependencies

```bash
cd ~/.claude/skills/things
pip3 install -r requirements.txt
```

This installs:
- `things.py` (Python library for reading Things database)
- `python-dateutil` (Date parsing utilities)

### 2. Verify Things 3 is Installed

Make sure Things 3 is installed on your Mac:

```bash
open -Ra Things3
```

### 3. Enable Things URLs (Optional - Required for Completing Tasks)

To complete or update tasks, you need an auth token:

1. Open Things 3
2. Go to **Preferences → General**
3. Check **"Enable Things URLs"**
4. Copy the **auth token**

Save it using one of these methods:

**Method 1: Environment Variable (Temporary)**
```bash
export THINGS_AUTH_TOKEN="your-auth-token-here"
```

**Method 2: Config File (Permanent)**
```bash
python3 -c "
import sys
sys.path.insert(0, '$HOME/.claude/skills/things/lib')
from writer import ThingsWriter
ThingsWriter.set_auth_token('your-auth-token-here')
"
```

**Note:** Auth token is only needed for completing/updating tasks. Adding and viewing tasks work without it.

### 4. Test the Installation

In Claude Code, try:

```
"Show me today's tasks"
```

or

```
"Add task 'Test task' today"
```

## Usage Examples

### Adding Tasks

```
"Add a task to write blog post today with tag work"
→ Creates task "Write blog post" scheduled for today with tag "work"

"Create task 'Call dentist' tomorrow with tag health"
→ Creates task scheduled for tomorrow

"Add 'Plan vacation' with checklist: book flights, reserve hotel, pack bags"
→ Creates task with 3 checklist items

"New task 'Review Q4 report' in Work project, due December 1st"
→ Creates task in Work project with deadline
```

### Viewing Tasks

```
"What's on my plate today?"
→ Shows all tasks scheduled for today

"Show my inbox"
→ Lists all inbox items needing triage

"List today grouped by project"
→ Shows today's tasks organized by project
```

### Searching Tasks

```
"Find all tasks mentioning 'API'"
→ Searches for "API" in titles and notes

"Show incomplete tasks in Marketing area tagged urgent"
→ Filtered search with multiple criteria

"What completed tasks mention 'blog'?"
→ Search completed tasks only

"Search for 'deployment' in Backend project"
→ Search within a specific project
```

### Completing Tasks

```
"Mark task ABC-123 as complete"
→ Completes task by UUID (shown in list output)

"Complete the dentist task"
→ Finds and completes task by title

"I finished the blog post"
→ Natural language completion
```

## Architecture

### Hybrid Approach

This skill uses the best of both worlds:

- **Reading**: Direct SQLite database access via `things.py`
  - Fast queries
  - No rate limits
  - Complete data access

- **Writing**: Official Things URL Scheme
  - Reliable
  - Fully supported
  - Rich feature set

### File Structure

```
~/.claude/skills/things/
├── Skill.md                # Main skill dispatcher
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── lib/
│   ├── reader.py           # Database reading (ThingsReader)
│   ├── writer.py           # URL scheme writing (ThingsWriter)
│   └── helpers.py          # Formatting utilities (ThingsFormatter)
└── skills/                 # Standalone sub-skills
    ├── add-task.md         # Add task sub-skill
    ├── list-today.md       # List today sub-skill
    ├── list-inbox.md       # List inbox sub-skill
    ├── search.md           # Search tasks sub-skill
    └── complete-task.md    # Complete task sub-skill
```

## Available Sub-Skills

### 1. Add Task (`add-task.md`)

Create new tasks with rich metadata.

**Parameters:**
- Title (required)
- Notes
- When (today, tomorrow, evening, anytime, someday, YYYY-MM-DD)
- Deadline (YYYY-MM-DD)
- Tags (list)
- Project/Area (by name)
- Checklist items (list)

### 2. List Today (`list-today.md`)

View all tasks scheduled for today.

**Output includes:**
- Task titles with checkboxes
- Notes preview
- Tags
- Project/Area context
- Deadlines
- UUIDs (for follow-up actions)

### 3. List Inbox (`list-inbox.md`)

View inbox tasks needing triage.

**Purpose:**
- Daily/weekly review
- Organizing captured tasks
- Scheduling unscheduled items

### 4. Search (`search.md`)

Find tasks with powerful filtering.

**Filters:**
- Query (keyword in title/notes)
- Status (incomplete, completed, canceled)
- Area
- Project
- Tag

### 5. Complete Task (`complete-task.md`)

Mark tasks as done.

**Methods:**
- By UUID (most reliable)
- By title (searches for match)
- Batch completion

## API Reference

### ThingsReader (lib/reader.py)

```python
from reader import ThingsReader

# Get tasks by list
tasks = ThingsReader.get_today()
tasks = ThingsReader.get_inbox()
tasks = ThingsReader.get_upcoming()
tasks = ThingsReader.get_anytime()

# Search with filters
results = ThingsReader.search(
    query="blog",
    status="incomplete",
    area="Work",
    project="Marketing",
    tag="urgent"
)

# Get projects and areas
projects = ThingsReader.get_projects(area="Work")
areas = ThingsReader.get_areas()
tags = ThingsReader.get_tags()

# Find by title or UUID
tasks = ThingsReader.find_by_title("dentist")
task = ThingsReader.get_by_uuid("ABC-123-DEF")
```

### ThingsWriter (lib/writer.py)

```python
from writer import ThingsWriter

# Add a task
ThingsWriter.add_task(
    title="Write blog post",
    notes="Focus on API design",
    when="today",
    deadline="2025-12-01",
    tags=["writing", "work"],
    list_name="Content Creation",
    checklist_items=["Research", "Outline", "Draft"]
)

# Add a project
ThingsWriter.add_project(
    title="Q1 Marketing Campaign",
    area="Marketing",
    deadline="2025-03-31",
    todos=[
        {"title": "Design assets"},
        {"title": "Write copy"}
    ]
)

# Complete a task
ThingsWriter.complete_task("task-uuid-here")

# Update a task
ThingsWriter.update_task(
    task_id="task-uuid",
    title="New title",
    when="tomorrow"
)
```

### ThingsFormatter (lib/helpers.py)

```python
from helpers import ThingsFormatter

# Format tasks for display
output = ThingsFormatter.format_task_list(
    tasks,
    verbose=True,        # Include metadata
    show_uuid=True,      # Show UUIDs
    group_by='project'   # Group by project/area/tag
)

# Generate summary
summary = ThingsFormatter.summarize_tasks(tasks)

# Export to JSON
json_str = ThingsFormatter.to_json(tasks, pretty=True)
```

## Advanced Usage

### Batch Operations

Complete multiple tasks:

```python
import os, sys
sys.path.insert(0, os.path.expanduser('~/.claude/skills/things/lib'))
from reader import ThingsReader
from writer import ThingsWriter

# Find all cleanup tasks
tasks = ThingsReader.search(query="cleanup", status="incomplete")

# Complete them
for task in tasks:
    print(f"Completing: {task['title']}")
    ThingsWriter.complete_task(task['uuid'])

print(f"✅ Completed {len(tasks)} tasks!")
```

### Custom Workflows

Daily planning script:

```python
from reader import ThingsReader
from helpers import ThingsFormatter

# Show morning dashboard
print("📅 TODAY'S AGENDA")
print("=" * 50)
today = ThingsReader.get_today()
print(ThingsFormatter.format_task_list(today, verbose=True, group_by='project'))

print("\n📥 INBOX TO TRIAGE")
print("=" * 50)
inbox = ThingsReader.get_inbox()
print(ThingsFormatter.format_task_list(inbox, verbose=False))

print("\n📊 SUMMARY")
print("=" * 50)
print(ThingsFormatter.summarize_tasks(today))
```

### Integration with Other Tools

Export tasks to Markdown:

```python
from reader import ThingsReader
import datetime

today = ThingsReader.get_today()
date_str = datetime.date.today().strftime('%Y-%m-%d')

with open(f'tasks-{date_str}.md', 'w') as f:
    f.write(f"# Tasks for {date_str}\n\n")
    for task in today:
        status = "x" if task['status'] == 'completed' else " "
        f.write(f"- [{status}] {task['title']}\n")
        if task.get('notes'):
            f.write(f"  - {task['notes']}\n")
```

## Troubleshooting

### "things.py not found"

**Solution:**
```bash
cd ~/.claude/skills/things
pip3 install -r requirements.txt
```

### "Auth token not configured"

**When:** Trying to complete or update tasks

**Solution:**
1. Open Things 3 → Preferences → General
2. Enable "Enable Things URLs"
3. Copy the auth token
4. Save it using Method 1 or 2 from Quick Start

### "No tasks found"

**Possible causes:**
- Things 3 is not installed
- Things 3 has no data
- Database is not accessible

**Solution:**
1. Verify Things 3 is installed: `open -Ra Things3`
2. Add some tasks in Things 3
3. Try again

### Tasks not appearing after adding

**Cause:** URL scheme opens Things but may take a moment to process

**Solution:**
1. Wait a moment
2. Check Things 3 app to verify
3. Try listing tasks again

### "Import error" when running skills

**Cause:** Python can't find the library modules

**Solution:** Make sure sys.path is set correctly in skill prompts:
```python
import os, sys
sys.path.insert(0, os.path.expanduser('~/.claude/skills/things/lib'))
```

## Extending the Skills

### Add More Sub-Skills

Ideas for additional skills:

1. **list-upcoming.md** - Show upcoming scheduled tasks
2. **list-projects.md** - List all projects with statistics
3. **list-areas.md** - Show areas with task counts
4. **add-project.md** - Create complete projects
5. **weekly-review.md** - Guided weekly review
6. **stats.md** - Productivity analytics
7. **export.md** - Export to JSON/CSV/Markdown

### Modify Existing Skills

The skills are just markdown prompts - customize them:

1. Edit the `.md` files
2. Adjust formatting preferences
3. Add custom filters
4. Change default behaviors

### Create Custom Workflows

Combine multiple operations in a new skill:

```markdown
# Weekly Review Skill

1. List all inbox items
2. List all projects
3. List overdue tasks
4. Generate statistics
5. Create next week's plan
```

## Best Practices

1. **Always show UUIDs** - Makes completing tasks easier
2. **Use verbose mode for planning** - See full context
3. **Group large result sets** - Easier to scan
4. **Search before adding** - Avoid duplicate tasks
5. **Regular inbox triage** - Keep your system clean
6. **Tag consistently** - Better filtering and organization

## Limitations

- **Mac only** - Things database only exists on macOS
- **No real-time sync** - Database reads may lag unsaved changes
- **Rate limits** - URL scheme: 250 operations per 10 seconds
- **No deletion** - Cannot delete tasks via URL scheme
- **No iOS** - Cannot access iPhone/iPad Things remotely

## Resources

### Official Documentation

- [Things URL Scheme](https://culturedcode.com/things/support/articles/2803573/)
- [Things AppleScript Guide](https://culturedcode.com/things/download/ThingsAppleScriptGuide.pdf)
- [Things Support](https://culturedcode.com/things/support/)

### things.py Library

- [GitHub Repository](https://github.com/thingsapi/things.py)
- [PyPI Package](https://pypi.org/project/things.py/)
- [Documentation](https://github.com/thingsapi/things.py#readme)

### Community

- [Things Forum](https://culturedcode.com/things/support/)
- [Reddit: r/thingsapp](https://reddit.com/r/thingsapp)
- [Things Blog](https://culturedcode.com/things/blog/)

## License

This skill set is provided as-is for personal use. Things 3 is a product of Cultured Code.

## Contributing

Found a bug or have an improvement? Feel free to modify the skills for your needs!

## Support

For issues with:
- **These skills**: Check troubleshooting section above
- **things.py library**: See [GitHub issues](https://github.com/thingsapi/things.py/issues)
- **Things 3 app**: Contact [Cultured Code support](https://culturedcode.com/things/support/)
- **Claude Code**: Check [Claude Code docs](https://code.claude.com/docs)

---

**Happy task managing! 🎯**
