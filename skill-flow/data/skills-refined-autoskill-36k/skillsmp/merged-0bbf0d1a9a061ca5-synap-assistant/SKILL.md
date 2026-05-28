---
name: synap-assistant
description: Manage a personal knowledge capture system. Use when the user wants to capture ideas, track todos, organize projects, review their synap, or mentions "synap", "brain dump", "capture this", "add to my list", "what's on my plate", "what should I focus on", or "daily review".
---

# synap Assistant

A CLI for externalizing your working memory - capture ideas, projects, features, todos, and questions without the overhead of complex tools.

## Why?

Your brain is for having ideas, not holding them. But sticky notes get lost, notepads pile up unread, and tools like Asana are overkill for personal capture.

**synap** solves this by providing:
- **Zero-friction capture** - dump thoughts in seconds
- **Structured retrieval** - find anything with search and filters
- **AI-assisted triage** - agents help you organize, prioritize, and act

## Agent Mindset

When assisting users with their synap entries:

1. **Capture first, organize later** - Never block on classification during fast capture. Get the thought out, refine later.
2. **Proactive triage** - Regularly surface raw entries needing processing. Don't let the inbox grow stale.
3. **Connect the dots** - Link related entries, identify patterns, consolidate ideas into projects.
4. **Reduce cognitive load** - Present summaries and prioritized lists, not exhaustive dumps.
5. **Preserve context** - Include enough detail for future recall. A cryptic note is useless later.
6. **Respect simplicity** - Simple thoughts don't need tags, priorities, and parents. Don't over-engineer.

## User Preferences (Memory)

synap stores user data in a configurable data directory (default: `~/.config/synap/`).

**Data files (syncable):**
- `entries.json` - Active entries
- `archive.json` - Archived entries  
- `user-preferences.md` - Agent memory / user preferences

**Config files (local only):**
- `config.json` - Settings (including `dataDir` for custom data location)
- `deletion-log.json` - Audit trail for restore

### Custom Data Directory (for sync)

Users can point synap to a custom folder (e.g., a git repo for multi-device sync):

```bash
synap config dataDir ~/synap-data
# Or during setup:
synap setup
```

When custom `dataDir` is set:
- Data files go to the custom location
- Config stays in `~/.config/synap/`
- User can sync data folder via git, Dropbox, iCloud, etc.

### Preferences Operations

- Read preferences at the start of a session when present.
- Prefer idempotent updates with `synap preferences set --section "Tag Meanings" --entry "#urgent = must do today"`.
- Remove entries with `synap preferences remove --section tags --match "urgent"`.
- List entries with `synap preferences list --section tags --json`.
- `synap preferences --append "## Section" "..."` is still supported for raw appends.
- Avoid overwriting user-written content; prefer section-based updates.

## Operating Modes

Detect user intent and respond appropriately:

| Mode | Triggers | Behavior |
|------|----------|----------|
| **Capture** | "Add this...", "Remind me...", "I had an idea..." | Fast capture, minimal questions, default to idea type |
| **Review** | "What's on my plate?", "Daily review", "Show me..." | Stats + prioritized summary, grouped by type |
| **Triage** | "Process my synap", "Process my brain dump", "What needs attention?" | Surface raw entries, help classify and prioritize |
| **Focus** | "What should I work on?", "Priority items" | WIP items + P1 todos + active projects, clear next actions |
| **Cleanup** | "Archive completed", "Clean up old stuff" | Bulk operations with preview and confirmation |

### Volume Modes (Quick vs Deep)

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Quick** | <10 entries returned | Direct answers, lightweight summaries, minimal batching |
| **Deep** | 10+ entries returned | Summarize first, propose batches, confirm before bulk actions |

## Quick Start

| Task | Command |
|------|---------|
| Capture idea | `synap add "your thought here"` |
| Add todo | `synap todo "task description"` |
| Add todo with due date | `synap todo "Review PR #42" --due tomorrow` |
| Add question | `synap question "what you're wondering"` |
| List active | `synap list` |
| See all | `synap list --all` |
| Search | `synap search "keyword"` |
| Show details | `synap show <id>` |
| Mark done | `synap done <id>` |
| Start working | `synap start <id>` |
| Stop working | `synap stop <id>` |
| Get stats | `synap stats` |
| Setup wizard | `synap setup` |
| Edit preferences | `synap preferences --edit` |
| Set preference | `synap preferences set --section tags --entry "#urgent = must do today"` |

## Pre-flight Check

Before operations, verify the tool is ready:

```bash
synap --version   # Verify installed
synap stats       # Quick health check
```

If `synap: command not found`, the user needs to install: `npm install -g synap`

## Command Reference

### Capture Commands

#### `synap add <content>`
Quick capture of a thought.

```bash
synap add "What if we used a graph database?"
synap add "Need to review the API design" --type todo --priority 1
synap add "Prep for demo" --type todo --due 2025-02-15
synap add "Meeting notes from standup" --type note --tags "meetings,weekly"
synap add --type project --title "Website Redesign" "Complete overhaul of the marketing site..."
```

**Options**:
- `--type <type>`: idea, project, feature, todo, question, reference, note (default: idea)
- `--title <title>`: Short title (auto-extracted from first line if not provided)
- `--priority <1|2|3>`: 1=high, 2=medium, 3=low
- `--tags <tags>`: Comma-separated tags
- `--parent <id>`: Parent entry ID
- `--due <date>`: Due date (YYYY-MM-DD, 3d/1w, weekday names: monday/friday, or keywords: today, tomorrow, next monday)
- `--json`: JSON output

#### `synap todo <content>`
Shorthand for adding a todo.

```bash
synap todo "Review PR #42"
# Equivalent to: synap add "Review PR #42" --type todo
```

Options: `--priority`, `--tags`, `--parent`, `--due`, `--json`

#### `synap question <content>`
Shorthand for adding a question.

```bash
synap question "Should we migrate to TypeScript?"
# Equivalent to: synap add "..." --type question
```

Options: `--priority`, `--tags`, `--parent`, `--due`, `--json`

#### `synap log <id> <message>`
Add a timestamped log entry under a parent entry.

```bash
synap log a1b2c3d4 "Started implementation"
synap log a1b2c3d4 "Completed first draft" --inherit-tags
```

**Options**:
- `--inherit-tags`: Copy tags from parent entry
- `--json`: JSON output

#### `synap batch-add`
Add multiple entries in one operation.

```bash
# From file
synap batch-add --file entries.json

# From stdin (pipe)
echo '[{"content":"Task 1","type":"todo"},{"content":"Task 2","type":"todo"}]' | synap batch-add

# Dry run
synap batch-add --file entries.json --dry-run
```

**Input format (JSON array):**
```json
[
  {"content": "First entry", "type": "idea"},
  {"content": "Second entry", "type": "todo", "priority": 1, "tags": ["work"]}
]
```

**Options**:
- `--file <path>`: Read from JSON file
- `--dry-run`: Preview what would be added
- `--json`: JSON output

### Query Commands

#### `synap list`
List entries with filtering.

```bash
synap list                              # Active + raw (default)
synap list --all                        # All except archived
synap list --type todo                  # Only todos
synap list --status raw                 # Needs triage
synap list --priority 1                 # High priority only
synap list --tags work,urgent           # Has ALL specified tags
synap list --since 7d                   # Created in last 7 days
synap list --overdue                    # Overdue entries
synap list --due-before 7d              # Due in next 7 days
synap list --has-due                    # Entries with due dates
synap list --json                       # JSON output for parsing
```

**Options**:
- `--type <type>`: Filter by entry type
- `--status <status>`: raw, active, wip, someday, done, archived (default: raw,active)
- `--tags <tags>`: Comma-separated, AND logic
- `--priority <1|2|3>`: Filter by priority
- `--parent <id>`: Children of specific entry
- `--orphans`: Only entries without parent
- `--since <duration>`: e.g., 7d, 24h, 2w
- `--due-before <date>`: Due before date (YYYY-MM-DD or 3d/1w)
- `--due-after <date>`: Due after date (YYYY-MM-DD or 3d/1w)
- `--overdue`: Only overdue entries
- `--has-due`: Only entries with due dates
- `--no-due`: Only entries without due dates
- `--all`: All statuses except archived
- `--done`: Include done entries
- `--archived`: Show only archived
- `--limit <n>`: Max entries (default: 50)
- `--sort <field>`: created, updated, priority, due
- `--reverse`: Reverse sort order
- `--json`: JSON output

#### `synap show <id>`
Show full entry details.

```bash
synap show a1b2c3d4
synap show a1b2c3d4 --with-children
synap show a1b2c3d4 --with-related
synap show a1b2c3d4 --json
```

#### `synap search <query>`
Full-text search across content and titles.

```bash
synap search "database"
synap search "meeting" --type note --since 30d
synap search "API" --json
```

### Modify Commands

#### `synap edit <id>`
Edit entry content.

```bash
synap edit a1b2c3d4                          # Opens $EDITOR
synap edit a1b2c3d4 --content "New text"     # Non-interactive
synap edit a1b2c3d4 --append "Follow-up"     # Add to existing
synap edit a1b2c3d4 --title "New title"
```

#### `synap set <id>`
Update entry metadata.

```bash
synap set a1b2c3d4 --type project
synap set a1b2c3d4 --status active
synap set a1b2c3d4 --priority 1
synap set a1b2c3d4 --tags "work,Q1"
synap set a1b2c3d4 --add-tags "important"
synap set a1b2c3d4 --remove-tags "draft"
synap set a1b2c3d4 --clear-priority
synap set a1b2c3d4 --parent b2c3d4e5
```

#### `synap link <id1> <id2>`
Create relationships between entries.

```bash
synap link a1b2c3d4 b2c3d4e5                # Add to related
synap link a1b2c3d4 b2c3d4e5 --as-parent    # Set hierarchy
synap link a1b2c3d4 b2c3d4e5 --unlink       # Remove relationship
```

### Bulk Commands

#### `synap done <ids...>`
Mark entries as done.

```bash
synap done a1b2c3d4
synap done a1b2c3d4 b2c3d4e5 c3d4e5f6       # Multiple
synap done --type todo --tags "sprint-1"     # By filter
synap done --dry-run --type todo             # Preview first
```

#### `synap start <ids...>`
Start working on entries (mark as WIP).

```bash
synap start a1b2c3d4                         # Single entry
synap start a1b2c3d4 b2c3d4e5                # Multiple
synap start --type todo --tags urgent        # By filter
synap start --dry-run --type todo            # Preview first
```

**Options**:
- `-t, --type <type>`: Filter by type
- `--tags <tags>`: Filter by tags
- `--dry-run`: Show what would be started
- `--json`: JSON output

#### `synap stop <ids...>`
Stop working on entries (remove WIP status).

```bash
synap stop a1b2c3d4                          # Single entry
synap stop --all                             # Stop all WIP entries
synap stop --dry-run                         # Preview first
```

**Options**:
- `--all`: Stop all WIP entries
- `--dry-run`: Show what would be stopped
- `--json`: JSON output

#### `synap archive <ids...>`
Archive entries (hides from default view).

```bash
synap archive a1b2c3d4
synap archive --status done --since 30d      # Old completed items
synap archive --dry-run --status done        # Preview
```

#### `synap delete <ids...>`
Delete entries (logged for undo).

```bash
synap delete a1b2c3d4
synap delete a1b2c3d4 b2c3d4e5 --confirm
synap delete --status archived --since 90d   # Permanent cleanup
synap delete --dry-run --type reference      # Preview
```

**Safety**:
- All deletions logged to enable restore
- >10 entries requires `--confirm` or `--force`
- Entries with children require `--force`

#### `synap restore`
Restore deleted entries.

```bash
synap restore --last 1                       # Most recent
synap restore --last 5                       # Last 5
synap restore --ids a1b2c3d4,b2c3d4e5        # Specific IDs
synap restore --list                         # Show deletion log
```

### Maintenance Commands

#### `synap stats`
Overview statistics.

```bash
synap stats
synap stats --json
```

#### `synap export`
Export entries.

```bash
synap export                                 # All to stdout
synap export --file backup.json              # To file
synap export --type todo --status active     # Filtered
```

#### `synap import <file>`
Import entries.

```bash
synap import backup.json
synap import backup.json --dry-run
synap import backup.json --merge             #