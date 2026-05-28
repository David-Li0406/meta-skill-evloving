# Sprint Commands Reference

**Always use `--plain` flag for scriptable output.**

## `jira sprint` (alias: `sprints`)

Manage sprints in a project board.

---

## `jira sprint list` (aliases: `ls`, `lists`)

List sprints or sprint issues.

```bash
jira sprint list --plain
jira sprint list SPRINT_ID --plain
```

### Sprint List Mode (no SPRINT_ID)

Lists sprints in the board.

```bash
jira sprint list --table --plain --columns id,name,state,start,end
```

### Sprint Issues Mode (with SPRINT_ID)

Lists issues in a specific sprint.

```bash
jira sprint list 123 --plain --columns key,summary,status,assignee
```

### Shortcut Flags

| Flag | Description |
|------|-------------|
| `--current` | List issues in current active sprint |
| `--prev` | List issues in previous sprint |
| `--next` | List issues in next planned sprint |

**Examples:**
```bash
jira sprint list --current --plain
jira sprint list --prev --plain --columns key,summary,status
```

### Filter Flags (for sprint issues)

| Flag | Description |
|------|-------------|
| `-C, --component` | Filter by component |
| `-P, --parent` | Filter by parent issue |
| `-q, --jql` | Raw JQL query |
| `--show-all-issues` | Show issues from all projects |

### Display Flags

| Flag | Description |
|------|-------------|
| `--plain` | Plain text output |
| `--table` | Table view for sprint list |
| `--no-headers` | Hide headers (with --plain) |
| `--no-truncate` | Show all columns (with --plain) |
| `--columns` | Sprint columns: ID, NAME, START, END, COMPLETE, STATE |
| | Issue columns: TYPE, KEY, SUMMARY, STATUS, ASSIGNEE, REPORTER, PRIORITY, RESOLUTION, CREATED, UPDATED, LABELS |
| `--raw` | JSON output |
| `--csv` | CSV output |
| `--order-by` | Order field (default: `created`) |
| `--paginate` | Pagination (default: `0:100`) |
| `--state` | Filter sprints by state: `future`, `active`, `closed` (comma-separated) |

**Examples:**
```bash
# List all sprints
jira sprint list --table --plain

# Current sprint issues
jira sprint list --current --plain --columns key,summary,status

# Active and future sprints only
jira sprint list --table --plain --state "active,future"

# Issues in specific sprint
jira sprint list 123 --plain
```

---

## `jira sprint add` (alias: `assign`)

Add issues to a sprint.

```bash
jira sprint add SPRINT_ID ISSUE-1 [ISSUE-2 ... ISSUE-N]
```

| Argument | Description |
|----------|-------------|
| `SPRINT_ID` | Sprint ID (get from `sprint list`) |
| `ISSUE-1...N` | Issue keys to add (max 50) |

**Example:**
```bash
jira sprint add 123 MDBIM-100 MDBIM-101 MDBIM-102
```

---

## `jira sprint close` (alias: `complete`)

Close a sprint.

```bash
jira sprint close SPRINT_ID
```

| Argument | Description |
|----------|-------------|
| `SPRINT_ID` | Sprint ID to close |

**Example:**
```bash
jira sprint close 123
```

---

## Common Workflows

### Get current sprint ID

```bash
jira sprint list --table --plain --state active --columns id,name
```

### Add issue to current sprint

```bash
# First get sprint ID, then add
SPRINT_ID=$(jira sprint list --table --plain --state active --no-headers --columns id | head -1)
jira sprint add $SPRINT_ID MDBIM-123
```

### View all issues in current sprint

```bash
jira sprint list --current --plain --columns key,summary,status,assignee
```
