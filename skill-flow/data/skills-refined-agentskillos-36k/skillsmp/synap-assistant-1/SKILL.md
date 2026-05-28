---
name: synap-assistant
source: synap-cli
description: Manage a personal knowledge capture system. Use when the user wants to capture ideas, track todos, organize projects, review their synap, or mentions "synap", "brain dump", "capture this", "add to my list", "what's on my plate", "what should I focus on", or "daily review".
hash: 9c86041f8c7095822804f47de0b68715
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
synap import backup.json --merge             # Update existing + add new
synap import backup.json --skip-existing     # Only add new
```

#### `synap config`
View or update configuration.

```bash
synap config                                 # Show all settings + paths
synap config dataDir                         # Show data directory
synap config --reset                         # Reset to defaults
```

#### `synap save`, `synap pull`, `synap sync`
Git sync commands for multi-device workflow.

```bash
# Save (commit + push)
synap save                                   # Commit + push with auto timestamp
synap save "message"                         # Commit + push with custom message
synap save -m "message"                      # Same as above
synap save --dry-run                         # Preview changes without committing
synap save --no-push                         # Commit locally, don't push

# Pull
synap pull                                   # Pull latest from remote
synap pull --force                           # Pull even with uncommitted local changes

# Sync (pull + save)
synap sync                                   # Pull then save (full round-trip)
synap sync "end of day"                      # Sync with custom commit message
synap sync --dry-run                         # Preview what would happen
synap sync --no-push                         # Pull and commit, but don't push
```

**Git sync error codes:**
| Code | Meaning |
|------|---------|
| `NOT_GIT_REPO` | Data directory is not a git repository |
| `DIRTY_WORKING_TREE` | Uncommitted changes block pull (use `--force`) |
| `MERGE_CONFLICT` | Pull resulted in merge conflicts |
| `NO_REMOTE` | No git remote configured |
| `PUSH_FAILED` | Remote exists but push failed |

## Workflow Patterns

### Multi-Device Sync Setup

1. **Set data directory:**
   ```bash
   synap config dataDir ~/synap-data
   ```

2. **Initialize git (one-time):**
   ```bash
   cd $(synap config dataDir)
   git init
   git remote add origin git@github.com:user/synap-data.git
   synap save "Initial commit"
   ```

3. **Daily workflow:**
   ```bash
   synap pull    # Start of day
   synap save    # End of day
   synap sync    # Or full round-trip
   ```

4. **New device:**
   ```bash
   git clone git@github.com:user/synap-data.git ~/synap-data
   synap config dataDir ~/synap-data
   ```

### Daily Review

Run this each morning to get oriented:

1. **Health check**: `synap stats`
2. **Triage raw entries**: `synap list --status raw`
3. **Focus list**: `synap list --priority 1 --type todo`
4. **Help user decide** what to work on first

### Weekly Review

Run this weekly to maintain hygiene:

1. **Celebrate**: `synap list --done --since 7d` - show what was accomplished
2. **Check stalled**: `synap list --status active --sort updated` - find items not touched
3. **Review projects**: `synap list --type project` - are they progressing?
4. **Clean up**: `synap archive --status done --since 7d` - archive completed items

### Triage Workflow

When user has many raw entries:

1. **Fetch**: `synap list --status raw --json`
2. **For each entry**, determine:
   - Type (idea, todo, project, question, reference, note)
   - Priority (1, 2, 3, or none)
   - Tags (infer from content)
   - Parent (if belongs to existing project/feature)
3. **Update**: `synap set <id> --type todo --priority 1 --tags "work"`
4. **If entry is actually multiple items**, split and re-capture
5. **Mark refined**: `synap set <id> --status active`

### Capture Mode

When user is dumping thoughts rapidly:

1. Just capture with `synap add "..."` - don't interrupt for classification
2. Use default type (idea) and status (raw)
3. After the capture session, offer to triage

**Smart status defaulting**: When capturing with priority set, the CLI auto-promotes to `active` status (skipping triage). When adding entries with full metadata (priority, tags, due), there's no need to manually set status—the entry is already triaged.

### Grouping Detection Pattern

After capture sessions, detect opportunities to group related entries:

| Signal | Action |
|--------|--------|
| 3+ entries with same tag in one session | Suggest parent project with that tag as context |
| 3+ entries mentioning same keyword/topic | Suggest linking as related or creating parent |
| User mentions "for the X project" multiple times | Proactively suggest creating/linking to X project |

**Grouping workflow:**
1. After capture, analyze recent additions: `synap list --since 1h --json`
2. Group by common tags or detect semantic similarity
3. If grouping detected, propose: "These 4 entries seem related to [topic]. Create a parent project?"
4. On confirmation:
   - `synap add "[Topic] Project" --type project --tags "topic"`
   - For each child: `synap link <child-id> <project-id> --as-parent`

### Daily Tracking Pattern

For projects requiring ongoing progress logging (standups, journals, learning logs):

| Signal | Action |
|--------|--------|
| Project mentions "daily", "track progress", "standup" | Suggest daily tracking setup |
| User says "I need to log progress on X" | Explain `synap log` workflow |
| Project has `--tags daily-tracking` | Ask for today's update |

**Daily tracking workflow:**

1. **Setup:** Create a project to track
   ```bash
   synap add "Learn Rust" --type project --tags "learning,daily-tracking"
   ```

2. **Daily logging:** Add timestamped progress
   ```bash
   synap log <project-id> "Completed chapter 3"
   ```

3. **Review progress:** View the log tree
   ```bash
   synap tree <project-id>
   ```

**When to suggest:** User creates learning/progress project, mentions accountability, or asks about daily tracking.

**Do NOT auto-create** - always confirm with user first.

## Classification Rules

### Type Detection Heuristics

| Indicator | Likely Type |
|-----------|-------------|
| Starts with action verb ("Build", "Write", "Fix", "Review") | `todo` |
| Contains "?" or seeking information | `question` |
| Multi-step initiative, long-term scope | `project` |
| Specific capability/enhancement within a project | `feature` |
| Link, quote, or factual information | `reference` |
| Observation with no clear action | `note` |
| Speculative, "what if", creative | `idea` |

### Priority Assignment

| Priority | Criteria |
|----------|----------|
| P1 (high) | Blocking other work, deadline within 48h, explicitly urgent |
| P2 (medium) | Important but not urgent, this-week scope |
| P3 (low) | Nice-to-have, someday-maybe, learning/exploration |
| None | Truly unprioritized, needs triage |

## Safety Rules

**Non-negotiable constraints**:

1. **Never auto-delete** - Always show what will be deleted and confirm
2. **Preserve context** - Don't summarize away important details during capture
3. **Log before delete** - All deletions are recoverable via `synap restore`
4. **Confirm bulk operations** - Operations affecting >10 entries require confirmation
5. **Don't over-organize** - Simple thoughts don't need tags, priorities, and parents

**Git sync safety**:

6. **Preview before sync** - Use `--dry-run` to preview changes before committing
7. **Handle conflicts carefully** - `MERGE_CONFLICT` errors require manual resolution
8. **Protect uncommitted work** - `pull` checks for dirty tree; use `--force` only when safe
9. **Commit messages are safe** - Never executed as shell commands (stdin-based commit)

## Proactive Recommendation Patterns

- If raw entries are piling up, suggest `synap triage`.
- If P1 todos exist, suggest `synap focus`.
- If many stale active items exist, suggest a weekly review.
- If preferences specify cadence, follow it by default.
- If 3+ entries added with common tags/context, suggest grouping under a parent project (see Grouping Detection Pattern).

## Batch Processing Protocols

- Filters are for discovery; use IDs for execution.
- Keep batches small (10-25 items) and confirm between batches.
- Use `--dry-run` whenever available before bulk changes.

## Two-Step Pattern for Bulk Operations

Critical for preventing accidental mass changes:

1. **Preview**: `synap delete --status archived --since 90d --dry-run`
2. **Confirm**: Show user what will be affected, get explicit approval
3. **Execute**: `synap delete --ids "<specific-ids>" --confirm`

**Principle**: Filters are for DISCOVERY, IDs are for EXECUTION.

## Common Request Patterns

| User Says | Interpretation | Action |
|-----------|----------------|--------|
| "Add this to my synap" | Fast capture | `synap add "<content>"` |
| "I need to remember to..." | Todo item | `synap todo "<content>"` |
| "What's on my plate?" | Need overview | `synap stats` + `synap list --priority 1` |
| "What should I focus on?" | Need priorities | `synap list --priority 1 --type todo` |
| "Process my synap" | Triage needed | Run triage workflow on raw entries |
| "This is done" / "I finished X" | Mark complete | `synap done <id>` |
| "Archive old stuff" | Cleanup | `synap archive --status done --since 30d` |
| "What did I do this week?" | Review completions | `synap list --done --since 7d` |
| "Find anything about X" | Search | `synap search "X"` |
| "Link these together" | Create relationship | `synap link <id1> <id2>` |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `synap: command not found` | Run `npm install -g synap` |
| Empty synap | Start with `synap add "My first thought"` |
| Too many raw entries | Run triage workflow |
| Can't find entry | Use `synap search "<keyword>"` |
| Accidentally deleted | Use `synap restore --last 1` |
| Wrong type/status | Use `synap set <id> --type <type> --status <status>` |

## Testing / Evaluation Scenarios

| Scenario | Expected Behavior | Failure Indicator |
|----------|-------------------|-------------------|
| User says "capture this" | Immediate `synap add`, no questions | Asking for type/priority during fast capture |
| User says "what's on my plate" | Stats + prioritized summary | Listing all 50 entries individually |
| User says "clean up" | Preview + confirmation | Auto-archiving without preview |
| Large deletion (>10 items) | Show count, ask confirmation | Proceeding without confirmation |
| User mentions deadline | Suggest P1 priority | Not detecting urgency |
| User's idea relates to existing project | Suggest linking | Not checking for related entries |

## JSON Output Schemas

### Entry Object

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "content": "The full text of the entry",
  "title": "Short title (optional)",
  "type": "idea|project|feature|todo|question|reference|note",
  "status": "raw|active|wip|someday|done|archived",
  "priority": 1|2|3|null,
  "tags": ["tag1", "tag2"],
  "parent": "parent-id|null",
  "related": ["id1", "id2"],
  "due": "2026-01-10T23:59:59.000Z",
  "startedAt": "2026-01-10T08:30:00.000Z",
  "createdAt": "2026-01-05T08:30:00.000Z",
  "updatedAt": "2026-01-05T08:30:00.000Z",
  "source": "cli|agent|import"
}
```

### List Response

```json
{
  "success": true,
  "entries": [...],
  "total": 47,
  "returned": 12,
  "query": {
    "status": ["raw", "active"],
    "limit": 50
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Entry not found: a1b2c3d4",
  "code": "ENTRY_NOT_FOUND"
}
```

## Remember

- The goal is to **externalize working memory**, not build a perfect system
- Capture is king - never block a capture
- Structure serves retrieval, not organizational perfection
- The best system is one that gets used
