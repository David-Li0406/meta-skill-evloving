---
name: jira-ticket-manager
description: Manage Jira tickets - create, search, update, comment, and transition issues
---

# Jira Ticket Manager Skill Instructions

Use curl to interact with the Jira REST API. All responses are saved locally for reliable parsing.

## Pre-Flight Check

Verify environment variables are set (source the shell profile first):

```bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; echo "JIRA_URL: ${JIRA_URL:-(not set)}"; echo "JIRA_USER: ${JIRA_USER:-(not set)}"; echo "JIRA_TOKEN: ${JIRA_TOKEN:+set}"
```

**If variables are missing**, guide the user to add them to `~/.zshrc`:

```bash
# Appends to ~/.zshrc
printf '\nexport JIRA_URL="https://company.atlassian.net"\nexport JIRA_USER="your-email@company.com"\nexport JIRA_TOKEN="your-api-token"\n' >> ~/.zshrc && source ~/.zshrc
```

Do NOT ask users to paste credentials directly—the token should stay in their shell profile.

## Data Storage

API responses are saved to `.claude/skills/jira/tickets/` for reliable parsing (Jira responses are 30KB+ and get truncated when piped).

**First-time setup** (creates directory + gitignore):
```bash
mkdir -p .claude/skills/jira/tickets && echo '*' > .claude/skills/jira/tickets/.gitignore
```

**Files stored:**
- `{TICKET-KEY}.json` - Individual ticket data (e.g., `VE-3225.json`)
- `search-latest.json` - Most recent search results
- `my-tickets.json` - Current user's tickets

Users can delete the `tickets/` folder anytime to clear cached data.

## Command Pattern

Every command must source the shell profile first:

```bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; <curl command>
```

All examples below omit this prefix for brevity—**always include it**.

## Operations

### Get Ticket

**Step 1: Fetch and save**
```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" "$JIRA_URL/rest/api/2/issue/PROJ-123" -o .claude/skills/jira/tickets/PROJ-123.json
```

**Step 2: Parse**
```bash
jq '{
  key: .key,
  summary: .fields.summary,
  status: .fields.status.name,
  type: .fields.issuetype.name,
  priority: .fields.priority.name,
  assignee: .fields.assignee.displayName,
  reporter: .fields.reporter.displayName,
  created: .fields.created[0:10],
  updated: .fields.updated[0:10],
  description: .fields.description,
  parent_key: .fields.parent.key,
  parent_summary: .fields.parent.fields.summary
}' .claude/skills/jira/tickets/PROJ-123.json
```

**Output format:**
```
PROJ-123: Summary here
Status: In Progress | Type: Bug | Priority: High
Assignee: John Doe | Reporter: Jane Smith
Created: 2024-01-15 | Updated: 2024-01-20
Parent: PROJ-100 - Epic Name

Description:
[description text]
```

### Search Tickets

**Step 1: Fetch and save**
```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" -G \
  --data-urlencode 'jql=project = PROJ AND status = Open' \
  --data-urlencode 'maxResults=20' \
  --data-urlencode 'fields=key,summary,status,assignee,priority' \
  "$JIRA_URL/rest/api/2/search" -o .claude/skills/jira/tickets/search-latest.json
```

**Step 2: Parse**
```bash
jq '.issues[] | {key: .key, summary: .fields.summary, status: .fields.status.name, assignee: .fields.assignee.displayName, priority: .fields.priority.name}' .claude/skills/jira/tickets/search-latest.json
```

Output as a table for user.

### My Tickets

**Step 1: Fetch and save**
```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" -G \
  --data-urlencode 'jql=assignee = currentUser() AND status != Done ORDER BY updated DESC' \
  --data-urlencode 'maxResults=20' \
  --data-urlencode 'fields=key,summary,status,priority,updated' \
  "$JIRA_URL/rest/api/2/search" -o .claude/skills/jira/tickets/my-tickets.json
```

**Step 2: Parse**
```bash
jq '.issues[] | {key: .key, summary: .fields.summary, status: .fields.status.name, priority: .fields.priority.name, updated: .fields.updated[0:10]}' .claude/skills/jira/tickets/my-tickets.json
```

### Create Ticket

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -X POST -H 'Content-Type: application/json' \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Ticket summary here",
      "description": "Detailed description here",
      "issuetype": {"name": "Bug"}
    }
  }' \
  "$JIRA_URL/rest/api/2/issue" | jq '{key: .key, self: .self}'
```

**Issue types:** Task, Bug, Story, Epic, Sub-task (varies by project)

**Optional fields:** `"priority": {"name": "High"}`, `"assignee": {"accountId": "..."}`, `"labels": ["label1"]`

After creation, report: "Created PROJ-123: [summary]" with link.

### Update Ticket

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -X PUT -H 'Content-Type: application/json' \
  -d '{"fields": {"summary": "Updated summary"}}' \
  "$JIRA_URL/rest/api/2/issue/PROJ-123"
```

PUT returns empty on success (HTTP 204). Verify by fetching the ticket.

### Add Comment

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -X POST -H 'Content-Type: application/json' \
  -d '{"body": "Comment text here"}' \
  "$JIRA_URL/rest/api/2/issue/PROJ-123/comment" | jq '{id: .id, created: .created}'
```

### Transition Ticket

**Step 1: Get available transitions**
```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  "$JIRA_URL/rest/api/2/issue/PROJ-123/transitions" | jq '.transitions[] | {id: .id, name: .name}'
```

**Step 2: Apply transition**
```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -X POST -H 'Content-Type: application/json' \
  -d '{"transition": {"id": "21"}}' \
  "$JIRA_URL/rest/api/2/issue/PROJ-123/transitions"
```

Transition IDs vary by project—always fetch available transitions first.

### Get Comments

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  "$JIRA_URL/rest/api/2/issue/PROJ-123/comment" | jq '.comments[] | {author: .author.displayName, created: .created[0:10], body: .body}'
```

## Error Handling

If a response contains `errorMessages` or `errors`, it failed. Common errors:

| Error | Fix |
|-------|-----|
| "Issue does not exist" | Check ticket key format (PROJ-123) |
| "Field 'project' is required" | Add project key to create request |
| "Transition id is invalid" | Fetch available transitions first |
| 401 Unauthorized | Check JIRA_USER and JIRA_TOKEN |
| 403 Forbidden | User lacks permission for this action |

## Output Guidelines

1. **Be concise**: Show key fields, not raw JSON
2. **Format dates**: Use `[0:10]` slice for YYYY-MM-DD
3. **Link tickets**: `$JIRA_URL/browse/PROJ-123`
4. **Include parent**: Show parent key and summary when present

## URL Parsing

Extract ticket keys from URLs:

| URL Pattern | Key Location |
|-------------|--------------|
| `.../browse/PROJ-123` | After `/browse/` |
| `...?selectedIssue=PROJ-123` | Query param `selectedIssue` |
