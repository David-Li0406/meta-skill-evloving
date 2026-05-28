# Shark Task Management Skill

## What This Skill Provides

This skill enables task lifecycle management through the shark CLI and provides integration points for other skills to reference task tracking workflows.

## Components

### 1. Slash Commands (`.claude/commands/`)

Direct, discoverable commands for task management:

- `/task-start <task-id>` - Start a task
- `/task-complete <task-id>` - Complete a task
- `/task-next` - Get next task
- `/task-list [filters]` - List tasks
- `/task-info <task-id>` - Get task details

**Usage:**
```bash
# In Claude Code REPL
> /task-next
> /task-start T-E04-F02-001
> /task-complete T-E04-F02-001
```

These appear in `/help` output and support tab completion.

### 2. Skill Documentation (`SKILL.md`)

Centralized knowledge about:
- Task management workflows
- Integration with implementation skills
- CLI reference
- Best practices
- Troubleshooting

**How Other Skills Reference It:**

```markdown
## Phase 0: Start Task Tracking

See the `shark-task-management` skill for complete task lifecycle documentation.

Start your task:
```bash
/task-start <task-id>
```
```

### 3. Optional Hooks (`HOOKS.md`)

Optional automation for power users:
- Test completion reminders
- Auto-start on file read
- Task validation before edits

Users can choose to enable these in their settings.

## How This Integrates

### With Implementation Skill

The `implementation` skill includes Phase 0 in all workflows:

```markdown
## Phase 0: Start Task Tracking

/task-start <task-id>

This updates status and enables progress tracking.
```

### With Other Skills

- **Quality Skill**: Can check task status before reviews
- **Orchestration Skill**: Can coordinate task assignment
- **DevOps Skill**: Can link deployments to tasks

## Why This Design

### Slash Commands for User Control

- **Explicit**: Users choose when to run commands
- **Discoverable**: Appear in `/help`
- **Documented**: Built-in descriptions
- **Flexible**: Support arguments

### Skill for Knowledge Sharing

- **Centralized**: Single source of truth
- **Reusable**: Other skills reference it
- **Progressive Disclosure**: SKILL.md → detailed docs
- **Context Efficient**: Loaded only when needed

### Hooks for Optional Automation

- **Opt-in**: Users choose what to enable
- **Deterministic**: Always runs when triggered
- **Transparent**: Clear what they do
- **Safe**: Can warn without blocking

## File Structure

```
.claude/
├── commands/
│   ├── task-start.md        # Slash command: /task-start
│   ├── task-complete.md     # Slash command: /task-complete
│   ├── task-next.md         # Slash command: /task-next
│   ├── task-list.md         # Slash command: /task-list
│   └── task-info.md         # Slash command: /task-info
├── hooks/
│   └── task-completion-reminder.json  # Optional hook config
└── skills/
    └── shark-task-management/
        ├── SKILL.md         # Main skill documentation
        ├── HOOKS.md         # Optional hooks guide
        └── README.md        # This file
```

## Getting Started

### For Users

1. **Basic Usage**: Just use the slash commands
   ```bash
   /task-next
   /task-start T-E04-F02-001
   ```

2. **Learn More**: Read the skill when needed
   ```
   The skill auto-loads when you use slash commands
   ```

3. **Optional Automation**: Enable hooks from `HOOKS.md`
   ```
   Add to .claude/settings.json if desired
   ```

### For Skill Authors

Reference task management in your skills:

```markdown
## Integration with Task Management

Use `/task-start <task-id>` before beginning work.
See `shark-task-management` skill for details.
```

## Benefits

- Database tracks all task activity
- Enables progress reporting
- Provides audit trail

### Consistent Workflow

- All implementation workflows follow same pattern
- Reduces cognitive load
- Builds good habits

## Examples

### Daily Workflow

```bash
# Morning: See what's next
> /task-next

# Start the task
> /task-start T-E04-F02-003

# [... do implementation work ...]

# Tests pass, validation gates pass
> /task-complete T-E04-F02-003

# Get next task
> /task-next
```

### With Hooks Enabled

```bash
# Run tests
> Run pytest

# Output:
# ================================ test session starts =================================
# collected 42 items
#
# tests/test_service.py::test_create_user PASSED
# tests/test_service.py::test_get_user PASSED
# ... all tests pass ...
#
# ⚠️  All tests passed! Consider completing the task with: /task-complete T-E04-F02-003

# Complete the task
> /task-complete T-E04-F02-003
```

## Maintenance

### Adding New Commands

Create a new file in `.claude/commands/`:

```bash
echo "..." > .claude/commands/task-status.md
```

Command appears immediately in `/help`.

### Updating Documentation

Edit `SKILL.md` to update knowledge.

### Adding Hooks

Add new optional hooks to `HOOKS.md` with:
- Clear description
- Installation instructions
- Safety warnings
- Customization examples

## See Also

- [Implementation Skill](../implementation/SKILL.md)
- [Shark CLI Documentation](../../../docs/CLI_REFERENCE.md)
