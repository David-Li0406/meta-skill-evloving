---
name: Vault Task Management
description: This skill should be used when the user asks to "find tasks", "show tasks", "list tasks", "query tasks", "tasks with status", "fire tasks", "incomplete tasks", "tasks in inbox", "tasks in projects", or mentions task checkboxes with status markers (x, f, /, b, ?). Provides task querying across PARA directories in Obsidian vaults.
version: 0.1.0
---

# Vault Task Management

This skill provides Claude with knowledge about task management in Obsidian vaults using checkbox syntax with status markers, and tools to efficiently find and query tasks across PARA directories.

## Task Definition

A **task** is any line in a markdown file that starts with `- [ ]` where the character within the brackets denotes the current status.

### Task Status Markers

- `x` - Complete
- `f` - Fire (important/urgent)
- `/` - Partial (in progress)
- `b` - Bookmarked (deferred)
- `?` - Has open questions

### Task Syntax Examples

```markdown
- [ ] This is an incomplete task
- [x] This is a completed task
- [f] This is a fire/urgent task
- [/] This is a partial/in-progress task
- [b] This is a bookmarked/deferred task
- [?] This task has open questions
```

## Task Categories

Tasks are organized into three primary categories based on their location in the PARA structure:

1. **Inbox** - Tasks in `00_Inbox/` files (unprocessed, need categorization)
2. **Projects** - Tasks in `01_Projects/` files (time-bound initiatives)
3. **Areas** - Tasks in `02_Areas/` files (ongoing responsibilities)

**Note:** Tasks may exist in `03_Resources/` and `04_Archive/` directories, but these are considered secondary for active task management purposes.

## Finding Tasks

Two scripts are available for querying tasks:

1. **`scripts/find-tasks.sh`** - Raw pipe-delimited output for parsing
2. **`scripts/show-tasks.sh`** - Human-readable formatted output

### Find Tasks (Raw Output)

Use for programmatic parsing or piping to other commands:

```bash
./scripts/find-tasks.sh [status_filter] [vault_path]
```

### Show Tasks (Formatted Output)

Use for presenting results to users:

```bash
./scripts/show-tasks.sh [status_filter] [vault_path]
```

**Parameters:**
- `status_filter` - Filter tasks by status (default: `all`)
  - `all` - Show all tasks regardless of status
  - `incomplete` - Show all tasks that are NOT complete (excludes `x`)
  - `x`, `f`, `/`, `b`, `?` - Show only tasks with specific status
- `vault_path` - Path to Obsidian vault (default: current directory)

### Script Output Format

The script outputs pipe-delimited results:

```
category|status|file_path|line_number|task_text
```

**Example output:**
```
inbox|f|00_Inbox/2026-01-14.md|15|Follow up with team on SDK adoption
projects|/|01_Projects/Epic-Social-39.00/README.md|42|Complete authentication integration
areas|?|02_Areas/EOS-SDK-Team/Team-Project-Status.md|8|Clarify deployment timeline with ops
```

### Common Query Patterns

**Find all fire tasks (formatted):**
```bash
./scripts/show-tasks.sh f /path/to/vault
```

**Find all incomplete tasks (formatted):**
```bash
./scripts/show-tasks.sh incomplete /path/to/vault
```

**Find tasks with open questions (raw for parsing):**
```bash
./scripts/find-tasks.sh ? /path/to/vault
```

**Find all tasks in current vault:**
```bash
./scripts/show-tasks.sh all .
```

## Using the Scripts in Claude Sessions

When a user asks about tasks, prefer `show-tasks.sh` for direct presentation to users, or `find-tasks.sh` when you need to parse and analyze the data programmatically.

### Example Workflow (Formatted Output)

1. User asks: "Show me all my fire tasks"
2. Execute: `./scripts/show-tasks.sh f /home/rjroy/Projects/Vaults/second-brain`
3. Present the formatted output directly

**Example output from show-tasks.sh:**
```
Inbox:
  [f] Unreal Fest Chicago 2026 proposal (due Jan 22)
    File: 00_Inbox/2026-01-05.md (line 158)

Areas:
  [f] SDK Performance: Get it formally tied to Epic Social Overlay
    File: 02_Areas/Leadership-Development/2026-Manager-Operating-System.md (line 38)

Total tasks: 2
```

### Example Workflow (Parsed Analysis)

1. User asks: "How many incomplete tasks do I have in each category?"
2. Execute: `./scripts/find-tasks.sh incomplete /home/rjroy/Projects/Vaults/second-brain`
3. Parse pipe-delimited output and count by category
4. Present analysis:

```
Incomplete Task Summary:
- Inbox: 12 tasks
- Projects: 5 tasks
- Areas: 8 tasks
Total: 25 incomplete tasks
```

### Formatting Guidelines

When presenting task results:

1. **Group by category** - Separate inbox, projects, and areas
2. **Include context** - Show file path and line number for easy navigation
3. **Count tasks** - Provide total count in header
4. **Clean presentation** - Remove technical pipe-delimited format from user view
5. **Highlight status** - Make status markers clear when showing multiple statuses

### Reasoning About Tasks

Beyond querying, use task information to:

- **Identify bottlenecks** - Many `?` tasks may indicate unclear requirements
- **Spot urgency** - High `f` task count suggests overcommitment
- **Track progress** - Ratio of `/` to incomplete tasks shows momentum
- **Process inbox** - Large number of inbox tasks suggests need for organization
- **Surface blockers** - `b` tasks that remain bookmarked too long may need attention

## Task Context and Metadata

When examining tasks, consider:

1. **File context** - Tasks in project READMEs vs daily notes have different implications
2. **Heading context** - Read the surrounding markdown to understand task context
3. **Related tasks** - Tasks in the same file or section may be dependent
4. **Temporal context** - Tasks in daily notes vs persistent project files have different urgency

To get full context for a task:
1. Use the script to locate the task (file + line number)
2. Read the file around that line number to understand context
3. Check the file's YAML frontmatter if present
4. Consider the file's location in PARA structure

## Advanced Queries

Combine script execution with other tools for complex queries:

**Find tasks in a specific project:**
```bash
./scripts/find-tasks.sh all /path/to/vault | grep "01_Projects/ProjectName"
```

**Count tasks by status:**
```bash
./scripts/find-tasks.sh all /path/to/vault | cut -d'|' -f2 | sort | uniq -c
```

**Find oldest inbox tasks (by filename date):**
```bash
./scripts/find-tasks.sh all /path/to/vault | grep "^inbox" | sort -t'|' -k3
```

## Best Practices

When working with tasks in the vault:

1. **Always use the script** - Don't try to grep manually; the script handles edge cases
2. **Provide full context** - Include file path and line number when discussing specific tasks
3. **Respect PARA boundaries** - Understand implications of tasks in different categories
4. **Don't modify tasks without asking** - Task status changes should be intentional
5. **Consider task age** - Old incomplete tasks in inbox may need attention
6. **Batch similar queries** - Run script once and filter results rather than multiple executions

## Script Implementation Details

The `find-tasks.sh` script:

- Searches only PARA directories (`00_Inbox`, `01_Projects`, `02_Areas`)
- Uses `grep` with recursive search through `.md` files only
- Captures line numbers for precise task location
- Categorizes tasks based on file path
- Sorts output by category, status, then file path
- Handles edge cases (missing directories, special characters in tasks)
- Outputs pipe-delimited format for easy parsing

## Examples

### Example 1: Daily review workflow

User: "What tasks do I have in my inbox?"

Claude executes:
```bash
./scripts/find-tasks.sh all /home/rjroy/Projects/Vaults/second-brain | grep "^inbox"
```

Then presents grouped, formatted results.

### Example 2: Project focus

User: "Show me incomplete tasks for Epic 39"

Claude executes:
```bash
./scripts/find-tasks.sh incomplete /home/rjroy/Projects/Vaults/second-brain | grep "Epic-Social-39"
```

Then presents tasks with file context.

### Example 3: Priority triage

User: "What needs my attention right now?"

Claude executes:
```bash
./scripts/find-tasks.sh f /home/rjroy/Projects/Vaults/second-brain
```

Then analyzes fire tasks and suggests priority order.

### Example 4: Blocked work

User: "Which tasks have been deferred?"

Claude executes:
```bash
./scripts/find-tasks.sh b /home/rjroy/Projects/Vaults/second-brain
```

Then reviews bookmarked tasks and asks if any should be unblocked.

## Integration with Other Workflows

This task management skill integrates with:

- **Daily review** - `/daily-review` can surface tasks created during the day
- **Inbox processing** - `/inbox-processor` can identify tasks that need categorization
- **Project tracking** - Task queries inform project status updates
- **Weekly synthesis** - Task completion rates contribute to productivity insights

When tasks appear in these workflows, use the script to retrieve full task context and current status.

## Troubleshooting

**Script returns no results:**
- Verify vault path is correct
- Check that search directories exist
- Ensure markdown files contain task syntax
- Confirm status filter is valid

**Tasks appear in wrong category:**
- Verify file is in correct PARA directory
- Check for symbolic links or unusual directory structures

**Script fails to execute:**
- Ensure script has execute permissions (`chmod +x`)
- Verify bash is available
- Check for syntax errors if modified

## Summary

Use this skill to:
1. **Understand task syntax** - Recognize status markers and their meanings
2. **Query efficiently** - Use the script rather than manual searching
3. **Present clearly** - Format results for user comprehension
4. **Reason contextually** - Consider file location, status patterns, and temporal context
5. **Integrate holistically** - Connect task information with other vault workflows

The task management system provides structured tracking while maintaining flexibility through status markers and PARA organization.
