---
name: acli-jira
description: Atlassian CLI (acli) for Jira operations. Use when creating tickets, searching issues, updating status, or managing Jira work items from the command line.
---

# Atlassian CLI (acli) - Jira Reference

The Atlassian CLI (`acli`) provides command-line access to Jira. Authentication is automatic via devcontainer environment variables.

## Command Structure

```
acli jira <resource> <action> [flags]
```

**Resources**: `workitem`, `project`, `sprint`, `board`, `filter`

---

## Work Item Operations

### Create Ticket

```bash
acli jira workitem create \
  --project "CLDS" \
  --type "Task" \
  --summary "Ticket summary here" \
  --description "Detailed description (supports markdown)"

# With additional options
acli jira workitem create \
  --project "CLDS" \
  --type "Bug" \
  --summary "Fix login issue" \
  --description "Users cannot login after password reset" \
  --assignee "user@wiliot.com" \
  --label "bug,urgent"

# Self-assign
acli jira workitem create \
  --project "CLDS" \
  --type "Task" \
  --summary "My task" \
  --assignee "@me"
```

**Flags**:
| Flag | Description |
|------|-------------|
| `--project`, `-p` | Project key (e.g., "CLDS", "INF") - **required** |
| `--type`, `-t` | Work item type: Task, Bug, Story, Epic - **required** |
| `--summary`, `-s` | Ticket title - **required** |
| `--description`, `-d` | Detailed description (markdown supported) |
| `--assignee`, `-a` | Email, account ID, `@me`, or `default` |
| `--label`, `-l` | Comma-separated labels |
| `--parent` | Parent work item ID (for subtasks) |
| `--json` | Output in JSON format |

**Output**: Returns the ticket key and URL (e.g., `CLDS-16825`)

---

### View Ticket

```bash
# Basic view
acli jira workitem view CLDS-12345

# JSON output for parsing
acli jira workitem view CLDS-12345 --json

# Specific fields only
acli jira workitem view CLDS-12345 --fields "summary,status,assignee"

# Open in browser
acli jira workitem view CLDS-12345 --web
```

**Flags**:
| Flag | Description |
|------|-------------|
| `--fields`, `-f` | Comma-separated field list (default: key,issuetype,summary,status,assignee,description) |
| `--json` | JSON output |
| `--web`, `-w` | Open in web browser |

**Special field values**:
- `*all` - All fields
- `*navigable` - All navigable fields
- `-description` - Exclude description

---

### Search Tickets (JQL)

```bash
# Search by project
acli jira workitem search --jql "project = CLDS" --limit 20

# Search by status
acli jira workitem search --jql "project = CLDS AND status = 'In Progress'"

# Search by assignee
acli jira workitem search --jql "assignee = currentUser()"

# Search recent tickets
acli jira workitem search --jql "project = CLDS ORDER BY created DESC" --limit 10

# Get count only
acli jira workitem search --jql "project = CLDS AND status = Open" --count

# CSV output
acli jira workitem search --jql "project = CLDS" --csv --fields "key,summary,status"

# Paginate all results
acli jira workitem search --jql "project = CLDS" --paginate
```

**Flags**:
| Flag | Description |
|------|-------------|
| `--jql`, `-j` | JQL query string - **required** |
| `--limit`, `-l` | Max results (default: none) |
| `--count` | Return count only |
| `--json` | JSON output |
| `--csv` | CSV output |
| `--fields`, `-f` | Fields to display |
| `--paginate` | Fetch all pages |
| `--filter` | Use saved filter ID instead of JQL |

**Common JQL patterns**:
```
project = CLDS                           # By project
status = "In Progress"                   # By status
assignee = currentUser()                 # My tickets
created >= -7d                           # Last 7 days
labels in (urgent, bug)                  # By labels
summary ~ "login"                        # Text search
ORDER BY priority DESC, created DESC     # Ordering
```

---

### Edit Ticket

```bash
# Update summary
acli jira workitem edit --key "CLDS-12345" --summary "New summary"

# Update description
acli jira workitem edit --key "CLDS-12345" --description "Updated description"

# Change assignee
acli jira workitem edit --key "CLDS-12345" --assignee "user@wiliot.com"

# Remove assignee
acli jira workitem edit --key "CLDS-12345" --remove-assignee

# Add labels
acli jira workitem edit --key "CLDS-12345" --labels "new-label"

# Remove labels
acli jira workitem edit --key "CLDS-12345" --remove-labels "old-label"

# Multiple tickets via JQL
acli jira workitem edit --jql "project = CLDS AND labels = temp" --remove-labels "temp" --yes
```

**Flags**:
| Flag | Description |
|------|-------------|
| `--key`, `-k` | Ticket key(s), comma-separated |
| `--jql` | JQL query to select tickets |
| `--summary`, `-s` | New summary |
| `--description`, `-d` | New description |
| `--assignee`, `-a` | New assignee |
| `--remove-assignee` | Remove assignee |
| `--labels`, `-l` | Add labels |
| `--remove-labels` | Remove labels |
| `--type`, `-t` | Change work item type |
| `--yes`, `-y` | Skip confirmation |

---

### Transition Status

```bash
# Move to Done
acli jira workitem transition --key "CLDS-12345" --status "Done" --yes

# Move to In Progress
acli jira workitem transition --key "CLDS-12345" --status "In Progress" --yes

# Bulk transition via JQL
acli jira workitem transition --jql "project = CLDS AND status = 'To Do'" --status "In Progress" --yes
```

**Flags**:
| Flag | Description |
|------|-------------|
| `--key`, `-k` | Ticket key(s) |
| `--jql` | JQL query |
| `--status`, `-s` | Target status - **required** |
| `--yes`, `-y` | Skip confirmation |

**Common statuses**: `To Do`, `In Progress`, `In Review`, `Done`, `Closed`

---

### Comments

```bash
# Add comment
acli jira workitem comment create --key "CLDS-12345" --body "Comment text here"

# Add comment from file
acli jira workitem comment create --key "CLDS-12345" --body-file "comment.txt"

# List comments
acli jira workitem comment list --key "CLDS-12345"

# Edit last comment
acli jira workitem comment create --key "CLDS-12345" --body "Updated comment" --edit-last
```

**Subcommands**: `create`, `list`, `update`, `delete`

---

## Project Operations

### List Projects

```bash
# Recent projects
acli jira project list --recent

# All projects (paginated)
acli jira project list --paginate

# Limited list
acli jira project list --limit 50

# JSON output
acli jira project list --limit 50 --json

# Find specific project
acli jira project list --limit 100 | grep -i "cloud"
```

**Flags**:
| Flag | Description |
|------|-------------|
| `--recent` | Up to 20 recently viewed |
| `--limit`, `-l` | Max projects (default: 30) |
| `--paginate` | Fetch all pages |
| `--json` | JSON output |

### View Project

```bash
acli jira project view CLDS
```

---

## Sprint Operations

```bash
# List work items in sprint
acli jira sprint list-workitems --board-id 123 --sprint-id 456
```

---

## Common Patterns

### Create Ticket for Feature Branch

```bash
# Create ticket and capture key
TICKET=$(acli jira workitem create \
  --project "CLDS" \
  --type "Task" \
  --summary "Implement feature X" \
  --json | jq -r '.key')

# Create branch
git checkout -b "feature/${TICKET}-implement-feature-x"
```

### Find My Open Tickets

```bash
acli jira workitem search \
  --jql "assignee = currentUser() AND status != Done" \
  --fields "key,summary,status,priority"
```

### Bulk Update Labels

```bash
acli jira workitem edit \
  --jql "project = CLDS AND created >= -30d AND labels is EMPTY" \
  --labels "needs-triage" \
  --yes
```

### Create Sub-Tasks for Feature

Used by `/feature:tasks` to create sub-tasks under a parent ticket:

```bash
# Extract project from parent ticket
PARENT_TICKET="CLDS-1234"
PROJECT=$(echo "$PARENT_TICKET" | grep -oE '^[A-Z]+')

# Create sub-task
SUBTASK_KEY=$(acli jira workitem create \
  --project "$PROJECT" \
  --type "Sub-task" \
  --parent "$PARENT_TICKET" \
  --summary "T001: Create project structure" \
  --json | jq -r '.key')

echo "Created sub-task: $SUBTASK_KEY"
```

### Bulk Create Sub-Tasks from tasks.md

```bash
#!/bin/bash
PARENT_TICKET="CLDS-1234"
PROJECT=$(echo "$PARENT_TICKET" | grep -oE '^[A-Z]+')

# Parse tasks.md and create sub-tasks
grep -E '^\- \[ \] T[0-9]+' tasks.md | while read -r line; do
  # Extract task ID and description
  TASK_ID=$(echo "$line" | grep -oE 'T[0-9]+')
  SUMMARY=$(echo "$line" | sed 's/.*\] //' | sed 's/\[.*\] //')

  # Create sub-task
  KEY=$(acli jira workitem create \
    --project "$PROJECT" \
    --type "Sub-task" \
    --parent "$PARENT_TICKET" \
    --summary "$TASK_ID: $SUMMARY" \
    --json | jq -r '.key')

  echo "$TASK_ID -> $KEY"
done
```

### Status Lifecycle Transitions

Used by `/feature` workflow for automated status updates:

```bash
# When starting implementation
acli jira workitem transition --key "CLDS-1234" --status "In Progress" --yes

# When creating PR
acli jira workitem transition --key "CLDS-1234" --status "In Review" --yes

# When PR is merged
acli jira workitem transition --key "CLDS-1234" --status "Done" --yes
```

---

## Output Formats

| Flag | Format | Use Case |
|------|--------|----------|
| (none) | Table | Human-readable display |
| `--json` | JSON | Parsing with `jq`, automation |
| `--csv` | CSV | Spreadsheets, data export |

**JSON parsing examples**:
```bash
# Get ticket key
acli jira workitem create ... --json | jq -r '.key'

# Get assignee email
acli jira workitem view CLDS-123 --json | jq -r '.fields.assignee.emailAddress'
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "at least one flag required" | Missing required flag | Check required flags (--project, --type, --summary for create) |
| "project not found" | Invalid project key | Use `acli jira project list` to find valid keys |
| "transition not valid" | Invalid status transition | Check available transitions for current status |
| "not authenticated" | Auth expired/missing | Rerun `acli jira auth login` or restart devcontainer |

---

## Notes

- **Always use `acli jira workitem`**, not the old `acli issue` syntax
- Project keys are uppercase (CLDS, INF, not "Cloud Services")
- Use `--yes` / `-y` to skip confirmation prompts in scripts
- Multi-line descriptions work directly in the `--description` string
- Authentication is automatic in devcontainer via `ATLASSIAN_*` env vars
