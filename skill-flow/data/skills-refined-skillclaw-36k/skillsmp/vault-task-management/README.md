# Vault Task Management Skill

This skill teaches Claude about task management in Obsidian vaults using checkbox syntax with status markers.

## What This Skill Provides

1. **Task syntax understanding** - Recognition of status markers (x, f, /, b, ?)
2. **PARA category awareness** - Inbox, Projects, and Areas distinctions
3. **Query tools** - Scripts to efficiently find tasks across the vault
4. **Formatting guidance** - How to present task information to users

## Task Status Markers

- `[ ]` - Incomplete task
- `[x]` - Complete
- `[f]` - Fire (urgent/important)
- `[/]` - Partial/in-progress
- `[b]` - Bookmarked/deferred
- `[?]` - Has open questions

## Scripts

### `scripts/find-tasks.sh`

Raw query tool that outputs pipe-delimited data:
```bash
./scripts/find-tasks.sh [all|incomplete|x|f|/|b|?] [vault_path]
```

Output format: `category|status|file|line|task_text`

### `scripts/show-tasks.sh`

Human-readable formatted output:
```bash
./scripts/show-tasks.sh [all|incomplete|x|f|/|b|?] [vault_path]
```

Groups tasks by category with file locations and line numbers.

## Usage Examples

```bash
# Show all fire tasks
./scripts/show-tasks.sh f ~/Projects/Vaults/second-brain

# Find incomplete tasks for parsing
./scripts/find-tasks.sh incomplete ~/Projects/Vaults/second-brain

# Show tasks with open questions
./scripts/show-tasks.sh ? ~/Projects/Vaults/second-brain

# List all tasks in current directory
./scripts/show-tasks.sh all .
```

## When Claude Uses This Skill

This skill triggers when users ask to:
- "find tasks"
- "show tasks"
- "list tasks"
- "fire tasks"
- "incomplete tasks"
- "tasks in inbox"
- "tasks with status X"

## File Structure

```
vault-task-management/
├── SKILL.md              # Main skill documentation
├── README.md             # This file
└── scripts/
    ├── find-tasks.sh     # Raw query tool
    └── show-tasks.sh     # Formatted output tool
```

## Integration

This skill integrates with:
- Daily review workflows (`/daily-review`)
- Inbox processing (`/inbox-processor`)
- Project tracking
- Weekly synthesis

## Installation

This skill is automatically available in Claude Code when placed in:
- `~/.claude/skills/vault-task-management/`

Claude will discover it via the SKILL.md metadata and load it when triggered by relevant user queries.
