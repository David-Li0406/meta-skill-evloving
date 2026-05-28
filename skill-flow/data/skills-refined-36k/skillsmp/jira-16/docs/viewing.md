# Viewing Jira Tickets

Detailed guide for using `view_ticket.py` to display ticket information.

## Script Location

```bash
scripts/view_ticket.py
```

## Basic Usage

```bash
# View ticket summary
python3 scripts/view_ticket.py PROJ-123

# Full details with comments
python3 scripts/view_ticket.py PROJ-123 --full

# JSON output (for parsing)
python3 scripts/view_ticket.py PROJ-123 --json
```

## What It Shows

### Basic View (default)
- Ticket key and summary
- Status, type, priority
- Assignee and reporter
- Created and updated timestamps
- Labels, fix versions, components
- Description (truncated if long)
- Linked issues
- Subtasks
- Parent (if subtask)
- Attachments

### Full View (--full flag)
Everything above PLUS:
- Last 5 comments with authors and timestamps
- Full comment text (truncated if very long)

### JSON View (--json flag)
- Raw API response
- Useful for scripting or parsing

## Authentication

Requires environment variables:
- `ATLASSIAN_EMAIL` - Your email
- `ATLASSIAN_API_TOKEN` - API token from Atlassian
- `ATLASSIAN_SITE` - Site hostname (default: yoursite.atlassian.net)

See `scripts/SETUP.md` for authentication setup.

## Examples

### Quick Status Check
```bash
python3 scripts/view_ticket.py PROJ-123
```

### Deep Dive with Comments
```bash
python3 scripts/view_ticket.py PROJ-123 --full
```

### Get Data for Processing
```bash
python3 scripts/view_ticket.py PROJ-123 --json | jq '.fields.status.name'
```

## Error Handling

### Ticket Not Found (404)
```
❌ HTTP 404: Issue does not exist or you do not have permission to see it
```

**Fix:** Check ticket key spelling and permissions.

### Authentication Failed (401)
```
❌ HTTP 401: Unauthorized
```

**Fix:** Regenerate API token and update `ATLASSIAN_API_TOKEN`.

### No Credentials
```
❌ Error: Missing credentials

Required environment variables:
  - ATLASSIAN_EMAIL
  - ATLASSIAN_API_TOKEN
```

**Fix:** Set environment variables (see `scripts/SETUP.md`).

## Output Format

```
📋 PROJ-123: TEST ONLY
================================================================================

Status: Draft
Type: Story
Priority: Normal
Assignee: John Doe
Reporter: John Doe
Created: 2025-11-12 15:29
Updated: 2025-11-12 15:59

Description:
--------------------------------------------------------------------------------
This ticket is for testing Jira API functions only

Comments: None

================================================================================
View in browser: https://yoursite.atlassian.net/browse/PROJ-123
```

## Script Features

- ✅ Python 3 standard library only (no dependencies)
- ✅ Basic authentication (API token)
- ✅ HTML description rendering
- ✅ Handles linked issues and subtasks
- ✅ Shows attachment info
- ✅ Browser link for full details
