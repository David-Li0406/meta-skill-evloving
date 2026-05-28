---
name: linear-sync
description: Updates Linear issues based on project-status evidence. Use when asked to sync Linear with code evidence or update issue status.
---

## Purpose

Synchronize Linear issue status with implementation evidence from code repositories. Updates issues to reflect actual development progress based on evidence from `/project-status`.

## When to Use

Apply when user asks:
- "Sync Linear with actual status"
- "Update Linear based on code"
- "Linear issues are out of date"
- "Mark Linear issues as done/in progress"

**Important:** Only invoke when user explicitly asks to update Linear. This skill modifies Linear data.

## Prerequisites

- Linear MCP configured or `LINEAR_API_TOKEN` in `.env.local`
- At least one evidence source configured (local repo, GitHub, or Linear)

---

## Workflow

### Step 1: Get Implementation Evidence

If components specified, invoke `/project-status <components>`.
If no components specified, invoke `/project-status` for full project scan.

Parse the output table to extract:
- Component name
- Status (Triage, Backlog, Todo, In Progress, In Review, Done, Shipped, Canceled, Unknown)
- Evidence description
- Source

### Step 2: Query Linear Current State

**Resolve team identifier:**
Before querying issues, resolve the configured `teamName` to a valid team:
1. Call `mcp__linear__list_teams` to get available teams
2. Match configured `teamName` against team name, key, or UUID
3. Use the matched team's `name` for all subsequent queries

This allows users to configure any of: team key ("TEAM"), team name ("My Team"), or UUID.

**Important:** The Linear MCP `team` parameter only accepts team **name** or **UUID**, not team keys. Always resolve keys via `list_teams` first.

1. Get team's workflow states:
   - Use `mcp__linear__list_issue_statuses` with the resolved team name

2. For each component, search for matching Linear issues:
   - Use `mcp__linear__list_issues` with query parameter set to component name

### Step 3: Match Components to Linear Issues

For each component from project-status:

**Primary: Exact Title Match**
- Issue title matches component name (case-insensitive)
- Score: 100

**Secondary: Partial Title Match**
- Component name appears anywhere in issue title
- Score: 60

**Tertiary: Identifier Match**
- If component looks like "TEAM-123", query by identifier directly
- Use `mcp__linear__get_issue` with the identifier

**No Match**
- Add to unmatched list
- Report in output with option to create new issue

### Step 4: Determine Required Actions

For each matched component-to-issue pair:

1. Compare project-status status to Linear issue status
2. Apply status priority ordering (see Status Mapping)
3. Determine if upgrade is needed

**Upgrade-Only Rule:** Never downgrade status automatically. If Linear shows higher status than evidence, skip the update and note it.

### Step 5: Generate Change Preview

Output a preview table showing all proposed changes:

```
## Linear Sync Preview

| Component | Issue | Current | Proposed | Evidence |
|-----------|-------|---------|----------|----------|
| auth | TEAM-123 | Backlog | In Progress | Feature branch exists |
| dashboard | TEAM-456 | In Progress | Done | PR #78 merged, CI passing |

### No Change Needed
- TEAM-789 (payments): Already at Done

### Skipped (Linear status higher)
- TEAM-111 (analytics): Linear at Done, evidence shows In Progress

### No Linear Issue Found
- notifications: No matching issue

Proceed with updates? (y/n)
```

### Step 6: Request Confirmation

**Check for auto-confirm mode:**

If `LINEAR_SYNC_AUTO_CONFIRM=1` environment variable is set:
1. Display one-time warning:
   ```
   ⚠️  AUTO-CONFIRM MODE ENABLED

   This will create, modify, and cancel temporary issues in your configured
   Linear workspace. All test issues will be:
   - Prefixed with [TEST]
   - Set to Canceled status after testing
   - Auto-archived by Linear after the configured period

   Workspace: {workspace_name}
   Team: {team_name}

   Consider creating a dedicated test workspace if you're concerned about
   affecting your production workspace.

   Proceed with automated write tests? (y/n)
   ```
2. If user confirms, skip per-operation confirmation and proceed to Step 7
3. If user declines, abort the sync

**Normal mode (no env var):**
- For any updates: Request explicit confirmation
- For bulk updates (>3 issues): Require "yes" typed confirmation
- User can select individual issues to update or skip

### Step 7: Apply Updates

For each confirmed update:

1. Update issue status:
   ```
   mcp__linear__update_issue(id=issue_id, state=new_state_name)
   ```

2. Add explanatory comment:
   ```
   mcp__linear__create_comment(
     issueId=issue_id,
     body="Status updated to [New Status] based on code evidence:\n- [Evidence description]\n- Source: /linear-sync"
   )
   ```

### Step 8: Report Results

Output final results:

```
## Linear Sync Results

### Updated (2)
| Issue | Previous | New | Evidence |
|-------|----------|-----|----------|
| TEAM-123 | Backlog | In Progress | Feature branch exists |
| TEAM-456 | In Progress | Done | PR #78 merged, CI passing |

### Skipped (1)
- TEAM-789: Linear status (Done) already higher than evidence (In Progress)

### No Match (1)
- notifications: No Linear issue found
```

---

## Status Mapping

### Priority Order (Highest to Lowest)

| Priority | Status | Linear State Type |
|----------|--------|-------------------|
| 1 | Shipped | completed |
| 2 | Done | completed |
| 3 | In Review | started |
| 4 | In Progress | started |
| 5 | Todo | unstarted |
| 6 | Backlog | backlog |
| 7 | Triage | triage |
| 8 | Canceled | canceled |
| 9 | Unknown | (no action) |

### Mapping to Linear States

| Project-Status | Linear State Name | Fallback |
|---------------|-------------------|----------|
| Shipped | Done | - |
| Done | Done | - |
| In Review | In Review | In Progress |
| In Progress | In Progress | - |
| Todo | Todo | - |
| Backlog | Backlog | - |
| Triage | Triage | - |
| Canceled | Canceled | (requires --force flag) |
| Unknown | (no action) | - |

### Resolving Team-Specific States

Since Linear teams can customize workflow states:

1. Call `mcp__linear__list_issue_statuses` to get team's states
2. Match by state name first (e.g., "In Review")
3. If no match, fall back to state type (e.g., type "started")
4. Handle teams without "In Review" state by using "In Progress"

---

## Safety Rules

1. **Never downgrade status automatically** - Only upgrade to higher priority status
2. **Always add comment explaining change** - Include evidence source
3. **Require confirmation for all updates** - No silent modifications
4. **Prompt before creating new issues** - Don't auto-create
5. **Canceled status requires explicit flag** - Use `--force` to mark as canceled

---

## Configuration

Read Linear settings from `.entourage/repos.json`:

```json
{
  "linear": {
    "teamName": "Team",
    "workspace": "my-workspace"
  }
}
```

**Note:** `teamName` accepts team name ("My Team"), team key ("TEAM"), or UUID.

### Authentication

1. **Preferred:** Use Linear MCP (handles OAuth automatically)
2. **Fallback:** API token from config file

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `LINEAR_SYNC_AUTO_CONFIRM=1` | Enables auto-confirm mode for automated testing. Shows one-time warning, then skips per-operation confirmations. |

---

## API Token Fallback (When MCP Unavailable)

When Linear MCP is not available (e.g., in automated tests), fall back to direct GraphQL API calls using `LINEAR_API_TOKEN` from `.env.local`.

### MCP Detection Protocol

1. **Attempt MCP tool call** (e.g., `mcp__linear__list_issue_statuses`)
2. **Check response:**
   - Success → Continue using MCP
   - Failure/not available → Use API token fallback

### GraphQL Mutations

**Update Issue Status:**
```graphql
mutation IssueUpdate($id: String!, $stateId: String!) {
  issueUpdate(id: $id, input: { stateId: $stateId }) {
    success
    issue {
      id
      identifier
      state { id name type }
    }
  }
}
```

**Curl example:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation($id: String!, $stateId: String!) { issueUpdate(id: $id, input: { stateId: $stateId }) { success } }",
    "variables": {"id": "issue-uuid", "stateId": "state-uuid"}
  }'
```

**Create Comment:**
```graphql
mutation CommentCreate($issueId: String!, $body: String!) {
  commentCreate(input: { issueId: $issueId, body: $body }) {
    success
    comment { id }
  }
}
```

**Curl example:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation($issueId: String!, $body: String!) { commentCreate(input: { issueId: $issueId, body: $body }) { success } }",
    "variables": {"issueId": "issue-uuid", "body": "Status updated based on code evidence..."}
  }'
```

**Get Team States (to resolve state name → ID):**
```graphql
query TeamStates($teamId: String!) {
  team(id: $teamId) {
    states {
      nodes { id name type }
    }
  }
}
```

### Write Test Safety

When running automated tests that create/modify Linear issues:
1. Prefix all test issue titles with `[TEST]`
2. Set test issues to `Canceled` status after verification
3. Linear auto-archives canceled issues per workspace settings

---

## Error Handling

### Linear MCP Not Available
```
> Linear MCP not available. Ensure Linear MCP server is configured.
> See: https://linear.app/docs/mcp
```

### Team Not Found
```
> Linear team "TEAM" not found. Check `teamName` in `.entourage/repos.json`.
```

### Permission Denied
```
> Cannot update issue TEAM-123: Insufficient permissions.
> Check your Linear role allows issue editing.
```

### State Not Found
```
> Cannot find state "In Review" in team TEAM.
> Available states: Triage, Backlog, Todo, In Progress, Done, Canceled
> Using "In Progress" instead.
```

---

## Examples

### Basic Sync

**Query:** `/linear-sync`

Runs full project status check and syncs all matching issues.

### Component-Specific Sync

**Query:** `/linear-sync auth dashboard`

Syncs only the specified components.

### After Project Status

**Query:** "Update Linear based on the status you just showed me"

Uses the most recent `/project-status` output to sync Linear.

---

## After Output

This skill modifies Linear issues and reports results. After completion:
- Summarize what was updated
- Note any issues that couldn't be matched
- Continue with next user request
