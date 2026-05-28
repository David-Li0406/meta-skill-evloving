# Epic Commands Reference

**Always use `--plain` flag for scriptable output.**

## `jira epic` (alias: `epics`)

Manage epics in a project.

---

## `jira epic list` (aliases: `ls`, `lists`)

List epics or epic issues.

```bash
jira epic list --plain
jira epic list EPIC-KEY --plain
```

### Epic List Mode (no EPIC-KEY)

Lists all epics in the project.

```bash
jira epic list --table --plain
```

### Epic Issues Mode (with EPIC-KEY)

Lists issues belonging to an epic.

```bash
jira epic list MDBIM-100 --plain --columns key,summary,status
```

### Filter Flags

| Flag | Description |
|------|-------------|
| `-s, --status` | Filter by status (repeatable) |
| `-y, --priority` | Filter by priority |
| `-a, --assignee` | Filter by assignee |
| `-r, --reporter` | Filter by reporter |
| `-l, --label` | Filter by label (repeatable) |
| `-C, --component` | Filter by component |
| `-R, --resolution` | Filter by resolution |
| `-w, --watching` | Issues you are watching |
| `--history` | Issues you accessed recently |

### Date Filters

| Flag | Description |
|------|-------------|
| `--created` | Filter by created: `today`, `week`, `month`, `year`, `yyyy-mm-dd`, `-10d` |
| `--updated` | Filter by updated (same format) |
| `--created-after` | Created after date |
| `--created-before` | Created before date |
| `--updated-after` | Updated after date |
| `--updated-before` | Updated before date |

### Display Flags

| Flag | Description |
|------|-------------|
| `--plain` | Plain text output |
| `--table` | Table view for epic list |
| `--no-headers` | Hide headers (with --plain) |
| `--no-truncate` | Show all columns (with --plain) |
| `--columns` | Columns: TYPE, KEY, SUMMARY, STATUS, ASSIGNEE, REPORTER, PRIORITY, RESOLUTION, CREATED, UPDATED, LABELS |
| `--raw` | JSON output |
| `--csv` | CSV output |
| `--order-by` | Order field (default: `created`) |
| `--reverse` | Reverse order |
| `--paginate` | Pagination (default: `0:100`) |

### JQL

| Flag | Description |
|------|-------------|
| `-q, --jql` | Raw JQL query in project context |

**Examples:**
```bash
# List all epics
jira epic list --table --plain

# List issues in an epic
jira epic list MDBIM-100 --plain --columns key,summary,status,assignee

# Open epics only
jira epic list --table --plain -s"Open" -s"In Progress"
```

---

## `jira epic create`

Create a new epic.

```bash
jira epic create -n"Epic Name" -s"Epic Summary" --no-input
```

| Flag | Description |
|------|-------------|
| `-n, --name` | Epic name |
| `-s, --summary` | Epic summary/title |
| `-b, --body` | Epic description |
| `-y, --priority` | Priority |
| `-a, --assignee` | Assignee |
| `-r, --reporter` | Reporter |
| `-l, --label` | Labels (repeatable) |
| `-C, --component` | Components (repeatable) |
| `-e, --original-estimate` | Time estimate |
| `--fix-version` | Fix version (repeatable) |
| `--affects-version` | Affects version (repeatable) |
| `--custom` | Custom fields: `--custom field=value` |
| `-T, --template` | Template file for body |
| `--no-input` | Skip prompts |
| `--web` | Open in browser after creation |

**Examples:**
```bash
# Simple epic
jira epic create -n"Q1 Goals" -s"Q1 2024 Objectives" --no-input

# Epic with details
jira epic create -n"Auth Revamp" -s"Authentication System Overhaul" -yHigh -lsecurity -b"Redesign auth..." --no-input
```

---

## `jira epic add` (alias: `assign`)

Add issues to an epic.

```bash
jira epic add EPIC-KEY ISSUE-1 [ISSUE-2 ... ISSUE-N]
```

| Argument | Description |
|----------|-------------|
| `EPIC-KEY` | Epic issue key |
| `ISSUE-1...N` | Issue keys to add (max 50) |

**Example:**
```bash
jira epic add MDBIM-100 MDBIM-101 MDBIM-102 MDBIM-103
```

---

## `jira epic remove` (aliases: `rm`, `unassign`)

Remove epic assignment from issues.

```bash
jira epic remove ISSUE-1 [ISSUE-2 ... ISSUE-N]
```

| Argument | Description |
|----------|-------------|
| `ISSUE-1...N` | Issue keys to unassign from their epic (max 50) |

**Example:**
```bash
jira epic remove MDBIM-101 MDBIM-102
```

---

## Common Workflows

### Create epic and add issues

```bash
# Create epic
jira epic create -n"Feature X" -s"Implement Feature X" --no-input

# Get the epic key from output, then add issues
jira epic add MDBIM-200 MDBIM-150 MDBIM-151 MDBIM-152
```

### List all issues in an epic

```bash
jira epic list MDBIM-100 --plain --columns type,key,summary,status,assignee
```

### Move issues between epics

```bash
# Remove from old epic
jira epic remove MDBIM-150 MDBIM-151

# Add to new epic
jira epic add MDBIM-200 MDBIM-150 MDBIM-151
```
