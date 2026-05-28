---
name: linear-check
description: Verify implementation status by querying Linear API for issues. Use when checking issue tracking status.
---

## Purpose

Query Linear to verify planning/implementation status of components/features. Returns evidence-based status levels using issue data from Linear.

## When to Use

- Directly invoked: `/linear-check authentication`
- Checking issue status for a component
- Verifying planning and tracking status
- When invoked by other skills (like `/project-status`)

## Input

Component or feature name(s) to verify. Examples:
- `/linear-check authentication`
- `/linear-check user-dashboard payments`

**Note:** Component searches are case-insensitive.

---

## Authentication

### Step 1: Check Linear MCP Availability

The Linear MCP server is preferred because it handles authentication via OAuth.

Check if Linear MCP tools are available by attempting to use a Linear MCP tool. If the tool responds successfully, use MCP for all queries.

### Step 2: Fallback to API Token

If Linear MCP is unavailable, fall back to `LINEAR_API_TOKEN` environment variable from `.env.local`:

```bash
# .env.local
LINEAR_API_TOKEN=lin_api_xxxxxxxxxxxx
```

Also ensure `.entourage/repos.json` has the team configuration:

```json
{
  "linear": {
    "teamName": "Team",
    "workspace": "my-workspace"
  }
}
```

**Note:** `teamName` accepts team name ("My Team"), team key ("TEAM"), or UUID.

Use curl with the token for GraphQL queries:
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "..."}'
```

### MCP Detection Protocol

When executing queries, follow this detection flow:

1. **Attempt MCP tool call** (e.g., `mcp__linear__list_issues`)
2. **Check response:**
   - If successful response with data → Continue using MCP
   - If error "MCP not available" or tool not found → Fall back to API
   - If auth error from MCP → Fall back to API token from config

**Example detection:**
```
Attempting: mcp__linear__list_teams
├── Success → Use MCP for all operations
└── Failure → Check LINEAR_API_TOKEN env var from .env.local
```

---

## Configuration Discovery

### Step 1: Check for Config File

Use the Read tool to check if `.entourage/repos.json` exists.

**If the file does not exist:**
```
> No repository configuration found. Create `.entourage/repos.json` with your Linear settings.
```

### Step 2: Extract Linear Config

Look for `linear` section in the config:

```json
{
  "linear": {
    "token": "lin_api_...",
    "teamName": "My Team",
    "workspace": "my-workspace"
  }
}
```

### Step 3: No Linear Configuration

If no `linear` section exists and MCP is unavailable:
```
> No Linear configuration found. Either configure Linear MCP or add `linear` section to `.entourage/repos.json`.
```

---

## Linear API Queries

For each component/feature, run these queries:

### Using MCP (Preferred)

**Resolve team identifier:**
Before querying issues, resolve the configured `teamName` to a valid team:
1. Call `list_teams` to get available teams
2. Match configured `teamName` against team name, key, or UUID
3. Use the matched team's `name` for all subsequent queries

This allows users to configure any of: team key ("TEAM"), team name ("My Team"), or UUID.

**Important:** The Linear MCP `team` parameter only accepts team **name** or **UUID**, not team keys. Always resolve keys via `list_teams` first.

**Search issues by component name:**
Use the `list_issues` MCP tool with the query parameter set to the component name and the resolved team name from config.

**Get issue details:**
Use the `get_issue` MCP tool with the issue ID.

**Get team's workflow states:**
Use the `list_issue_statuses` MCP tool with the resolved team name.

### Using API Token (Fallback)

Linear uses a GraphQL API at `https://api.linear.app/graphql`.

**Search issues by component name:**
```graphql
query SearchIssues($term: String!) {
  searchIssues(term: $term, first: 20) {
    nodes {
      identifier
      title
      state {
        name
        type
      }
      assignee {
        name
      }
      updatedAt
      url
    }
  }
}
```

**Get team's workflow states:**
```graphql
query TeamStates($teamKey: String!) {
  team(id: $teamKey) {
    id
    name
    states {
      nodes {
        name
        type
        position
      }
    }
  }
}
```

**Example curl command:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: lin_api_YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { searchIssues(term: \"authentication\", first: 20) { nodes { identifier title state { name type } } } }"
  }'
```

---

## Evidence Synthesis

Apply this decision tree to determine component status based on Linear issue state:

```
1. Issue state type is "completed"?
   YES -> Status: Done (High confidence)

2. Issue state type is "started" AND state name contains "review"?
   YES -> Status: In Review (High confidence)

3. Issue state type is "started"?
   YES -> Status: In Progress (High confidence)

4. Issue state type is "unstarted" AND state name is "Todo"?
   YES -> Status: Todo (High confidence)

5. Issue state type is "backlog"?
   YES -> Status: Backlog (High confidence)

6. Issue state type is "triage"?
   YES -> Status: Triage (High confidence)

7. Issue state type is "canceled"?
   YES -> Status: Canceled (High confidence)

8. No Linear issue found?
   -> Status: Unknown
   -> Output: "No Linear issue found for this component."
```

### State Type Mapping

Linear uses these state types:
- `triage` - Issues needing review before acceptance
- `backlog` - Accepted but not scheduled
- `unstarted` - Scheduled/ready to start (includes "Todo")
- `started` - Work in progress (includes "In Progress", "In Review")
- `completed` - Done
- `canceled` - Won't fix, duplicate, etc.

---

## Error Handling

### MCP Not Available, No Token
```
> Linear MCP not configured and no API token found. Configure Linear MCP or add LINEAR_API_TOKEN to `.env.local`.
```

### Token Invalid/Expired
If API returns authentication error:
```
> Linear API error: Authentication failed. Check LINEAR_API_TOKEN in `.env.local`.
```

### Rate Limited
If API returns rate limit error:
```
> Linear API rate limit reached. Try again later.
```

### Team Not Found
If team identifier is invalid:
```
> Linear team not found. Check `teamName` in `.entourage/repos.json`.
```

---

## Output Format

### With Linear Configuration

```markdown
## Linear Scan: [Component Name]

| Issue | Status | State | Assignee | Last Updated |
|-------|--------|-------|----------|--------------|
| TEAM-123 | In Progress | In Progress | @user | 2025-01-10 |

### Linear Details

**TEAM-123:** "Implement authentication flow"
- Status: In Progress
- Assignee: @user
- Updated: Jan 10, 2025
- URL: https://linear.app/my-workspace/issue/TEAM-123
```

### Without Linear Configuration

```markdown
## Linear Scan

No Linear configuration found. Either:
1. Configure Linear MCP server, or
2. Add `linear` section to `.entourage/repos.json`:

{
  "linear": {
    "token": "lin_api_...",
    "teamName": "My Team",
    "workspace": "my-workspace"
  }
}
```

### Multiple Components

When checking multiple components, output a summary table followed by details:

```markdown
## Linear Scan Summary

| Component | Status | Issue | State | Confidence |
|-----------|--------|-------|-------|------------|
| auth | In Progress | TEAM-123 | In Progress | High |
| dashboard | Backlog | TEAM-456 | Backlog | High |
| payments | Unknown | - | - | - |

### Details

[Per-component Linear details...]
```

---

## Example

**Query:** `/linear-check authentication`

**Output:**

```markdown
## Linear Scan: authentication

| Issue | Status | State | Assignee | Last Updated |
|-------|--------|-------|----------|--------------|
| TEAM-123 | In Progress | In Progress | @alice | 2025-01-10 |

### Linear Details

**TEAM-123:** "Implement Clerk authentication"
- Status: In Progress
- State: In Progress (started)
- Assignee: @alice
- Updated: Jan 10, 2025
- URL: https://linear.app/my-workspace/issue/TEAM-123
```

---

## After Output

This skill returns results to the calling context (usually `/project-status`). **Do not stop execution.**
Continue with the next step in the workflow or TODO list.
