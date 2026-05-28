# Transitioning Jira Tickets

Detailed guide for using `transition_ticket.py` to move tickets through workflow statuses.

## Script Location

```bash
scripts/transition_ticket.py
```

## Basic Usage

```bash
# List available transitions
python3 scripts/transition_ticket.py PROJ-123 --list

# Dry run (preview what would happen)
python3 scripts/transition_ticket.py PROJ-123 "Done" --dry-run

# Execute transition
python3 scripts/transition_ticket.py PROJ-123 "Done"
```

## Authentication

Requires environment variables:
- `ATLASSIAN_EMAIL` - Your email
- `ATLASSIAN_API_TOKEN` - API token from Atlassian
- `ATLASSIAN_SITE` - Site hostname (default: yoursite.atlassian.net)

See `scripts/SETUP.md` for authentication setup.

## Natural Language Mapping

Common phrases map to status names:

| User Says | Maps To |
|-----------|---------|
| "start", "begin", "work on" | "In Progress" |
| "finish", "complete", "done", "close" | "Done" |
| "block", "blocked", "pause" | "Blocked" |
| "test", "ready for testing" | "In Testing" |
| "review", "ready for review" | "In Review" |

**Example:**
When user says: "Start working on PROJ-123"
- Map "start" → "In Progress"
- Execute: `python3 scripts/transition_ticket.py PROJ-123 "In Progress"`

## Workflow

### 1. Check Available Transitions

Always check what transitions are possible first:

```bash
python3 scripts/transition_ticket.py PROJ-123 --list
```

**Output:**
```
📋 PROJ-123: Fix login button
Current Status: To Do

Available Transitions:
  1. In Progress → In Progress
  2. Won't Do → Won't Do
```

### 2. Preview Transition (Dry Run)

Test what would happen without making changes:

```bash
python3 scripts/transition_ticket.py PROJ-123 "In Progress" --dry-run
```

**Output:**
```
📋 PROJ-123: Fix login button
Current Status: To Do

🔍 Dry run: Would transition to 'In Progress'
   Using transition: In Progress (ID: 11)
```

### 3. Execute Transition

Make the actual status change:

```bash
python3 scripts/transition_ticket.py PROJ-123 "In Progress"
```

**Output:**
```
📋 PROJ-123: Fix login button
Current Status: To Do
Transitioning to: In Progress
✅ Success! Status: To Do → In Progress
```

## Status Name Matching

The script supports flexible matching:

### Exact Match (preferred)
```bash
python3 scripts/transition_ticket.py PROJ-123 "In Progress"
```

### Partial Match
```bash
python3 scripts/transition_ticket.py PROJ-123 "in prog"  # Matches "In Progress"
python3 scripts/transition_ticket.py PROJ-123 "done"     # Matches "Done"
```

### Case Insensitive
```bash
python3 scripts/transition_ticket.py PROJ-123 "DONE"          # Works
python3 scripts/transition_ticket.py PROJ-123 "in progress"  # Works
```

## Error Handling

### Authentication Failed (401)
```
❌ HTTP 401: Unauthorized
```

**Fix:** Regenerate API token at https://id.atlassian.com/manage-profile/security/api-tokens

### Transition Not Available
```
❌ Cannot transition to 'Done'

Available transitions:
  - In Progress
  - Blocked
  - Won't Do
```

**Fix:** Choose one of the available transitions or check workflow rules.

### Ticket Not Found (404)
```
❌ HTTP 404: Issue does not exist or you do not have permission to see it
```

**Fix:** Check ticket key and permissions.

### Permission Denied (403)
```
❌ HTTP 403: Forbidden
```

**Fix:** You may not have permission to transition this ticket. Contact Jira admin.

## Common Workflows

### Start Working on a Ticket
```bash
# 1. View current status
python3 scripts/view_ticket.py PROJ-123

# 2. Check available transitions
python3 scripts/transition_ticket.py PROJ-123 --list

# 3. Move to In Progress
python3 scripts/transition_ticket.py PROJ-123 "In Progress"
```

### Complete a Ticket
```bash
# 1. Verify it's ready
python3 scripts/view_ticket.py PROJ-123

# 2. Mark as done
python3 scripts/transition_ticket.py PROJ-123 "Done"
```

### Block a Ticket
```bash
python3 scripts/transition_ticket.py PROJ-123 "Blocked"
```

## Important Notes

### Transitions Are Ticket-Specific

Available transitions depend on:
- Current status
- Project workflow configuration
- Issue type
- User permissions
- Workflow conditions

**Never cache transitions** - always fetch fresh for each ticket.

### Workflow Conditions

Some transitions may have conditions:
- Required fields must be filled
- Specific user roles required
- Custom workflow validators

If a transition fails, check the Jira UI for requirements.

### Dry-Run Best Practice

For important transitions (especially bulk operations), always use `--dry-run` first:

```bash
# Preview first
python3 scripts/transition_ticket.py PROJ-123 "Done" --dry-run

# If looks good, execute
python3 scripts/transition_ticket.py PROJ-123 "Done"
```

## Script Features

- ✅ Python 3 standard library only (no dependencies)
- ✅ API token authentication
- ✅ List available transitions
- ✅ Partial status name matching
- ✅ Case-insensitive matching
- ✅ Dry-run mode
- ✅ Automatic transition ID lookup
- ✅ Clear success/error messages
