# Issue Commands Reference

**Always use `--plain` flag for scriptable output.**

## `jira issue list` (aliases: `ls`, `search`)

List issues in a project.

```bash
jira issue list --plain --columns key,summary,status,assignee
```

### Filter Flags

| Flag | Description |
|------|-------------|
| `-t, --type` | Filter by issue type |
| `-s, --status` | Filter by status (repeatable) |
| `-y, --priority` | Filter by priority |
| `-a, --assignee` | Filter by assignee (email/name, `x` for unassigned) |
| `-r, --reporter` | Filter by reporter |
| `-l, --label` | Filter by label (repeatable) |
| `-C, --component` | Filter by component |
| `-P, --parent` | Filter by parent issue |
| `-R, --resolution` | Filter by resolution type |
| `-w, --watching` | Issues you are watching |
| `--history` | Issues you accessed recently |

### Date Filters

| Flag | Description |
|------|-------------|
| `--created` | Filter by created date: `today`, `week`, `month`, `year`, `yyyy-mm-dd`, `-10d` |
| `--updated` | Filter by updated date (same format) |
| `--created-after` | Created after date |
| `--created-before` | Created before date |
| `--updated-after` | Updated after date |
| `--updated-before` | Updated before date |

### Display Flags

| Flag | Description |
|------|-------------|
| `--plain` | Plain text output |
| `--no-headers` | Hide headers (with --plain) |
| `--no-truncate` | Show all columns (with --plain) |
| `--columns` | Columns: TYPE, KEY, SUMMARY, STATUS, ASSIGNEE, REPORTER, PRIORITY, RESOLUTION, CREATED, UPDATED, LABELS |
| `--raw` | JSON output |
| `--csv` | CSV output |
| `--order-by` | Order field (default: `created`) |
| `--reverse` | Reverse order |
| `--paginate` | Pagination: `<limit>` or `<from>:<limit>` (default: `0:100`) |

### JQL

| Flag | Description |
|------|-------------|
| `-q, --jql` | Raw JQL query in project context |

**Examples:**
```bash
# My open issues
jira issue list -a$(jira me) -s~Done --plain

# High priority bugs
jira issue list -tBug -yHigh --plain

# Issues updated this week
jira issue list --updated week --plain

# Custom JQL
jira issue list -q"labels = urgent AND status != Done" --plain
```

---

## `jira issue view` (alias: `show`)

View issue details.

```bash
jira issue view ISSUE-KEY --plain
```

| Flag | Description |
|------|-------------|
| `--plain` | Plain text output |
| `--raw` | Raw JSON from API |
| `--comments N` | Show N comments (default: 1) |

**Examples:**
```bash
jira issue view MDBIM-123 --plain
jira issue view MDBIM-123 --comments 5 --plain
jira issue view MDBIM-123 --raw  # Full JSON
```

---

## `jira issue create`

Create a new issue.

```bash
jira issue create -tTask -s"Summary" -b"Description" --no-input
```

| Flag | Description |
|------|-------------|
| `-t, --type` | Issue type (Bug, Task, Story, etc.) |
| `-s, --summary` | Summary/title |
| `-b, --body` | Description |
| `-y, --priority` | Priority |
| `-a, --assignee` | Assignee (username/email/display name) |
| `-r, --reporter` | Reporter |
| `-l, --label` | Labels (repeatable) |
| `-C, --component` | Components (repeatable) |
| `-P, --parent` | Parent issue key (required for sub-tasks) |
| `-e, --original-estimate` | Time estimate |
| `--fix-version` | Fix version (repeatable) |
| `--affects-version` | Affects version (repeatable) |
| `--custom` | Custom fields: `--custom field=value` |
| `-T, --template` | Template file for body (use `-` for stdin) |
| `--no-input` | Skip prompts for non-required fields |
| `--web` | Open in browser after creation |
| `--raw` | Output JSON |

**Examples:**
```bash
# Simple task
jira issue create -tTask -s"Implement feature X" --no-input

# Bug with details
jira issue create -tBug -s"Login fails" -yHigh -lurgent -b"Steps to reproduce..." --no-input

# Sub-task
jira issue create -tSub-task -P MDBIM-100 -s"Sub-task title" --no-input

# With custom fields
jira issue create -tStory -s"User story" --custom story-points=3 --no-input
```

---

## `jira issue edit` (aliases: `update`, `modify`)

Edit an existing issue.

```bash
jira issue edit ISSUE-KEY -s"New summary" --no-input
```

| Flag | Description |
|------|-------------|
| `-s, --summary` | Edit summary |
| `-b, --body` | Edit description |
| `-y, --priority` | Edit priority |
| `-a, --assignee` | Edit assignee |
| `-l, --label` | Append labels (use `-label` to remove) |
| `-C, --component` | Replace components |
| `-P, --parent` | Link to parent |
| `--fix-version` | Add fix version (use `-version` to remove) |
| `--affects-version` | Add affects version |
| `--custom` | Edit custom fields |
| `--skip-notify` | Don't notify watchers |
| `--no-input` | Skip prompts |
| `--web` | Open in browser after edit |

**Examples:**
```bash
# Change summary
jira issue edit MDBIM-123 -s"Updated summary" --no-input

# Add and remove labels
jira issue edit MDBIM-123 -l"new-label" -l"-old-label" --no-input

# Change priority and assignee
jira issue edit MDBIM-123 -yHigh -a"john@example.com" --no-input
```

---

## `jira issue move` (aliases: `transition`, `mv`)

Transition issue to a new state.

```bash
jira issue move ISSUE-KEY "In Progress"
```

| Flag | Description |
|------|-------------|
| `--comment` | Add comment with transition |
| `-a, --assignee` | Assign during transition |
| `-R, --resolution` | Set resolution (for Done/Closed) |
| `--web` | Open in browser after move |

**Examples:**
```bash
jira issue move MDBIM-123 "In Progress"
jira issue move MDBIM-123 Done -R"Fixed"
jira issue move MDBIM-123 Done --comment "Completed implementation"
```

---

## `jira issue assign` (alias: `asg`)

Assign issue to a user.

```bash
jira issue assign ISSUE-KEY ASSIGNEE
```

| Argument | Description |
|----------|-------------|
| `ISSUE-KEY` | Issue key |
| `ASSIGNEE` | Email, display name, `$(jira me)`, `default`, or `x` (unassign) |

**Examples:**
```bash
jira issue assign MDBIM-123 $(jira me)      # Assign to self
jira issue assign MDBIM-123 "John Doe"      # Assign to user
jira issue assign MDBIM-123 x               # Unassign
jira issue assign MDBIM-123 default         # Default assignee
```

---

## `jira issue delete` (aliases: `rm`, `del`, `remove`)

Delete an issue.

```bash
jira issue delete ISSUE-KEY
```

| Flag | Description |
|------|-------------|
| `--cascade` | Delete with all subtasks |

---

## `jira issue clone`

Clone/duplicate an issue.

```bash
jira issue clone ISSUE-KEY
```

| Flag | Description |
|------|-------------|
| `-s, --summary` | Override summary |
| `-y, --priority` | Override priority |
| `-a, --assignee` | Override assignee |
| `-l, --label` | Override labels |
| `-C, --component` | Override components |
| `-P, --parent` | Set parent |
| `-H, --replace` | Replace text: `"find:replace"` |
| `--web` | Open in browser after clone |

**Example:**
```bash
jira issue clone MDBIM-123 -s"Cloned: New summary" -a$(jira me)
```

---

## `jira issue link` (alias: `ln`)

Link two issues.

```bash
jira issue link INWARD_KEY OUTWARD_KEY LINK_TYPE
```

| Argument | Description |
|----------|-------------|
| `INWARD_KEY` | Source issue |
| `OUTWARD_KEY` | Target issue |
| `LINK_TYPE` | Relationship: `Blocks`, `Duplicates`, `Relates`, etc. |

| Flag | Description |
|------|-------------|
| `--web` | Open in browser after link |

**Example:**
```bash
jira issue link MDBIM-123 MDBIM-456 Blocks
```

### `jira issue link remote` (alias: `rmln`)

Add a web link to an issue.

```bash
jira issue link remote ISSUE-KEY URL TITLE
```

**Example:**
```bash
jira issue link remote MDBIM-123 "https://github.com/org/repo/pr/1" "PR #1"
```

---

## `jira issue unlink` (alias: `uln`)

Remove link between issues.

```bash
jira issue unlink INWARD_KEY OUTWARD_KEY
```

---

## `jira issue comment add`

Add a comment to an issue.

```bash
jira issue comment add ISSUE-KEY "Comment text"
```

| Flag | Description |
|------|-------------|
| `--internal` | Make comment internal (Service Desk) |
| `-T, --template` | Read comment from file (use `-` for stdin) |
| `--no-input` | Skip prompts |
| `--web` | Open in browser after adding |

**Examples:**
```bash
jira issue comment add MDBIM-123 "Work in progress"
jira issue comment add MDBIM-123 $'Line 1\n\nLine 2'  # Multi-line
echo "Comment from pipe" | jira issue comment add MDBIM-123
```

---

## `jira issue watch` (alias: `wat`)

Add user to issue watchers.

```bash
jira issue watch ISSUE-KEY WATCHER
```

**Example:**
```bash
jira issue watch MDBIM-123 $(jira me)
```

---

## `jira issue worklog add`

Log time on an issue.

```bash
jira issue worklog add ISSUE-KEY "2h 30m" --no-input
```

| Flag | Description |
|------|-------------|
| `--started` | Start datetime: `2022-01-01 09:30:00` |
| `--timezone` | IANA timezone (default: UTC) |
| `--comment` | Worklog comment |
| `--new-estimate` | Update remaining estimate |
| `--no-input` | Skip prompts |

**Examples:**
```bash
jira issue worklog add MDBIM-123 "2h" --no-input
jira issue worklog add MDBIM-123 "1d 4h" --started "2024-01-15 09:00:00" --comment "Feature work"
```
