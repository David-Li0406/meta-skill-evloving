# ClickUp CLI Command Reference

Complete reference for all CLI commands and options.

## Task Commands

### `tasks search [query]`

Search for tasks across the workspace.

```bash
npm run dev -- tasks search "billing"
npm run dev -- tasks search "" --assignee me --status "in progress"
```

**Options:**
| Option | Description |
|--------|-------------|
| `-s, --status <status>` | Filter by status name |
| `-a, --assignee <assignee>` | Filter by assignee (use "me" for yourself) |
| `-l, --list <list>` | Filter by list name |
| `--space <space>` | Filter by space ID |
| `--include-subtasks` | Include subtasks in results |
| `--include-closed` | Include closed/completed tasks |
| `-t, --table` | Output as table |
| `--json` | Output as JSON |
| `-p, --page <number>` | Page number for pagination |

---

### `tasks get <taskId>`

Get detailed task information.

```bash
npm run dev -- tasks get TCG-4752
npm run dev -- tasks get TCG-4752 --full
npm run dev -- tasks get 86dz8kbp5  # Also works with internal IDs
```

**Options:**
| Option | Description |
|--------|-------------|
| `-c, --comments` | Include task comments |
| `-s, --subtasks` | Include subtask details |
| `-f, --full` | Include everything (comments, subtasks) |
| `-v, --verbose` | Show full description |
| `--json` | Output as JSON |

---

### `tasks create <name>`

Create a new task.

```bash
npm run dev -- tasks create "New feature" --list "Sprint 13"
npm run dev -- tasks create "Bug fix" --list "Sprint 13" --priority high --assignee me
npm run dev -- tasks create "Subtask" --parent TCG-4752
```

**Options:**
| Option | Description |
|--------|-------------|
| `-l, --list <list>` | **Required.** List name or ID |
| `-d, --description <desc>` | Task description |
| `-s, --status <status>` | Initial status |
| `-p, --priority <priority>` | Priority: urgent, high, normal, low |
| `-a, --assignee <assignee>` | Assignee (use "me" for yourself) |
| `--due <date>` | Due date (YYYY-MM-DD) |
| `--start <date>` | Start date (YYYY-MM-DD) |
| `--estimate <duration>` | Time estimate (e.g., "4h", "2h 30m") |
| `--parent <taskId>` | Parent task ID for subtasks |
| `--json` | Output as JSON |

---

### `tasks update <taskId>`

Update an existing task.

```bash
npm run dev -- tasks update TCG-4752 --status "complete"
npm run dev -- tasks update TCG-4752 --priority urgent --due "2026-01-30"
npm run dev -- tasks update TCG-4752 --due null  # Clear due date
```

**Options:**
| Option | Description |
|--------|-------------|
| `-n, --name <name>` | New task name |
| `-d, --description <desc>` | New description |
| `-s, --status <status>` | New status |
| `-p, --priority <priority>` | Priority or "null" to clear |
| `--due <date>` | Due date or "null" to clear |
| `--start <date>` | Start date or "null" to clear |
| `--estimate <duration>` | Time estimate or "null" to clear |
| `--json` | Output as JSON |

---

### `tasks delete <taskId>`

Delete a task.

```bash
npm run dev -- tasks delete TCG-4752          # Preview only
npm run dev -- tasks delete TCG-4752 --force  # Actually delete
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --force` | Skip confirmation and delete |

---

## Time Entry Commands

### `time list`

List time entries.

```bash
npm run dev -- time list                           # Today
npm run dev -- time list --date 2026-01-20         # Specific date
npm run dev -- time list --date yesterday
npm run dev -- time list --start 2026-01-13 --end 2026-01-19
npm run dev -- time list --task TCG-4752           # For specific task
```

**Options:**
| Option | Description |
|--------|-------------|
| `-d, --date <date>` | Show entries for date (default: today) |
| `--start <date>` | Start date for range |
| `--end <date>` | End date for range |
| `--task <taskId>` | Filter by task ID |
| `-t, --table` | Output as table |
| `--json` | Output as JSON |

---

### `time report`

Generate weekly time report.

```bash
npm run dev -- time report                    # Current week
npm run dev -- time report --week 2026-01-13  # Specific week
npm run dev -- time report --detailed
```

**Options:**
| Option | Description |
|--------|-------------|
| `-w, --week <date>` | Week containing this date |
| `--detailed` | Show detailed breakdown |
| `--json` | Output as JSON |

---

### `time add <taskId>`

Add a time entry to a task.

```bash
# By duration
npm run dev -- time add TCG-4752 --duration "2h 30m"
npm run dev -- time add TCG-4752 --duration "4h" --date "2026-01-20"

# By start/end times
npm run dev -- time add TCG-4752 --start "2026-01-20 10:30" --end "2026-01-20 15:00"

# With description
npm run dev -- time add TCG-4752 --duration "2h" --description "Code review"
```

**Options:**
| Option | Description |
|--------|-------------|
| `-d, --duration <duration>` | Duration (e.g., "2h 30m", "150m") |
| `--start <datetime>` | Start time (YYYY-MM-DD HH:MM) |
| `--end <datetime>` | End time (YYYY-MM-DD HH:MM) |
| `--date <date>` | Date for entry (default: today) |
| `--description <desc>` | Entry description |
| `--billable` | Mark as billable |
| `--json` | Output as JSON |

**Duration formats:**
- `2h` - 2 hours
- `30m` - 30 minutes
- `2h 30m` - 2 hours 30 minutes
- `150` - 150 minutes

---

### `time update <entryId>`

Update a time entry.

```bash
npm run dev -- time update <id> --duration "3h"
npm run dev -- time update <id> --description "Updated description"
npm run dev -- time update <id> --billable
```

**Options:**
| Option | Description |
|--------|-------------|
| `-d, --duration <duration>` | New duration |
| `--start <datetime>` | New start time |
| `--end <datetime>` | New end time |
| `--description <desc>` | New description |
| `--billable` | Mark as billable |
| `--not-billable` | Mark as not billable |
| `--json` | Output as JSON |

---

### `time move <entryId>`

Move a time entry to a different date (preserves time of day).

```bash
npm run dev -- time move <id> --to "2026-01-21"
npm run dev -- time move <id> --to tomorrow
```

**Options:**
| Option | Description |
|--------|-------------|
| `--to <date>` | **Required.** Target date |
| `--json` | Output as JSON |

---

### `time delete <entryId>`

Delete a time entry.

```bash
npm run dev -- time delete <id>          # Preview only
npm run dev -- time delete <id> --force  # Actually delete
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --force` | Skip confirmation and delete |

---

### `time start <taskId>`

Start a timer on a task.

```bash
npm run dev -- time start TCG-4752
npm run dev -- time start TCG-4752 --description "Working on feature"
```

**Options:**
| Option | Description |
|--------|-------------|
| `--description <desc>` | Description for the time entry |

---

### `time stop`

Stop the current running timer.

```bash
npm run dev -- time stop
```

---

### `time current`

Show the current running timer.

```bash
npm run dev -- time current
npm run dev -- time current --json
```

---

## Utility Commands

### `workspaces list`

List all accessible workspaces.

```bash
npm run dev -- workspaces list
npm run dev -- workspaces list --json
```

---

### `spaces list`

List all spaces in the workspace.

```bash
npm run dev -- spaces list
npm run dev -- spaces list --json
```

---

### `members list`

List all workspace members.

```bash
npm run dev -- members list
npm run dev -- members list --table
npm run dev -- members list --json
```

---

### `members find <nameOrEmail>`

Find a member by name or email.

```bash
npm run dev -- members find "Will"
npm run dev -- members find "will@blackairplane.com"
```

---

### `lists find <name>`

Find a list by name.

```bash
npm run dev -- lists find "Sprint 13"
```

---

### `config show`

Show current configuration.

```bash
npm run dev -- config show
```

---

## Date Formats

Commands accept various date formats:

| Format | Example |
|--------|---------|
| `YYYY-MM-DD` | `2026-01-20` |
| `YYYY-MM-DD HH:MM` | `2026-01-20 14:30` |
| `today` | Current date |
| `yesterday` | Previous date |
| `tomorrow` | Next date |

---

## Task ID Formats

Both formats work interchangeably:

- **Custom ID**: `TCG-4752` (user-friendly)
- **Internal ID**: `86dz8kbp5` (API ID)

The CLI automatically resolves custom IDs to internal IDs.
