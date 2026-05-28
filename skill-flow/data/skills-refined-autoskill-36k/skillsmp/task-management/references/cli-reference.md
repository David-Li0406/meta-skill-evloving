# CLI Reference

## Commands

### add
Create new task.
```bash
task add "Title" [options]
  -d, --description <text>  Task description
  -p, --priority <level>    low | medium | high | critical
  -e, --effort <size>       S | M | L | XL
  -t, --tags <tags>         Comma-separated tags
  -a, --assignee <name>     Assignee name
  --due <date>              Due date (YYYY-MM-DD)
```

### list / ls
List tasks with filters.
```bash
task list [options]
  -s, --status <status>     Filter by status
  -t, --tag <tag>           Filter by tag
  -a, --assignee <name>     Filter by assignee
  -p, --priority <level>    Filter by priority
  --json                    Output as JSON
```

### get
Get task details.
```bash
task get <id> [--json]
```

### update
Update task fields.
```bash
task update <id> [options]
  --title <title>           New title
  -d, --description <text>  New description
  -s, --status <status>     pending | in_progress | completed | blocked
  -p, --priority <level>    New priority
  -e, --effort <size>       New effort
  -t, --tags <tags>         New tags
  -a, --assignee <name>     New assignee
  --due <date>              New due date
  -n, --notes <notes>       Progress notes
```

### complete / done
Complete and auto-archive.
```bash
task complete <id> [-n, --notes <notes>]
```

### delete / rm
Delete task.
```bash
task delete <id>
```

### work
Start working (sets in_progress).
```bash
task work <id>
```

### block
Set blocking relationship.
```bash
task block <id> --by <blockerId>
```

### view
Generate markdown view.
```bash
task view
```

### export
Export to markdown file.
```bash
task export [file.md]
```

## Examples

```bash
# Create high-priority backend task
task add "Implement auth" -p high -e M -t "backend,security"

# List pending high-priority tasks
task list -s pending -p high

# Start working on task
task work t-001

# Complete with notes
task complete t-001 -n "Added tests, PR #42"
```
