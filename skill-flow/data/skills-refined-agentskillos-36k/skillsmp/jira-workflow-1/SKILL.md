---
name: jira-workflow
description: Manage development work using Jira tickets as the single source of truth. Use this skill when users want to (1) list their Jira tickets/work backlog, (2) create new Jira tickets/work items, (3) assign tickets to team members, (4) add labels to tickets, or (5) "do work" by implementing a Jira ticket—which involves creating a feature branch, implementing the changes, committing with ticket references, and updating the Jira ticket with progress. Triggers on phrases like "list my work", "show my tickets", "create a ticket", "add work", "assign PROJ-123 to", "add label", "do work", "work on PROJ-123", or "implement ticket".
---

# Jira Workflow Skill

Manage development workflows using Jira tickets. Supports four core operations: listing work, creating work, assigning work, and doing work.

## Prerequisites

- Access to Jira via MCP Atlassian tools
- Git repository in the current workspace
- Appropriate Jira project permissions

## Quick Reference

| User Intent | Workflow |
|-------------|----------|
| "List my work" / "Show my tickets" | → [List Work](#list-work) |
| "Create a ticket" / "Add work" | → [Create Work](#create-work) |
| "Assign PROJ-123 to John" | → [Assign Work](#assign-work) |
| "Add label to PROJ-123" | → [Manage Labels](#manage-labels) |
| "List components" | → [List Components](#list-components) |
| "Do work" / "Work on PROJ-123" | → [Do Work](#do-work) |

## List Work

Display the user's assigned Jira tickets.

**Steps:**

1. Get the Atlassian Cloud ID using `mcp_atlassian-mcp_getAccessibleAtlassianResources`
2. Get current user info using `mcp_atlassian-mcp_atlassianUserInfo`
3. Search for issues assigned to current user using the search tools (activate with `activate_search_tools_for_jira_and_confluence`)
4. Present tickets in a clear table format

**Output format:**

```
| Key | Summary | Status | Priority |
|-----|---------|--------|----------|
| PROJ-123 | Implement login | In Progress | High |
| PROJ-124 | Fix date bug | To Do | Medium |
```

## Create Work

Create a new Jira ticket.

**Required information** (prompt user if missing):

- Project key (or help user find it via `mcp_atlassian-mcp_getVisibleJiraProjects`)
- Summary (ticket title)
- Issue type (Story, Bug, Task, etc.)
- Component (see [List Components](#list-components) for available options)

**Mandatory fields (auto-populated):**

- **Requested by (BU)**: Default to `GLCP`. User can override if needed.
- **Labels**: Always include `created-by-github-copilot`. User can add additional labels.

**Optional information:**

- Description
- Priority
- Assignee
- Additional labels

**Steps:**

1. Get Cloud ID if not cached
2. Gather required fields from user
3. If issue type unknown, fetch available types via issue metadata tools (activate with `activate_jira_issue_management_tools`)
4. Check user preferences file for last-used component (see [User Preferences](#user-preferences))
5. If no component provided and preference exists, suggest it; otherwise prompt user
6. Create issue using `mcp_atlassian-mcp_createJiraIssue` with `additional_fields`:

   ```json
   {
     "components": [{ "name": "<component-name>" }],
     "customfield_XXXXX": { "value": "GLCP" },
     "labels": ["created-by-github-copilot", "<user-labels>"]
   }
   ```

7. Save selected component to user preferences
8. Confirm creation with ticket key and link

> **Note:** The custom field ID for "Requested by (BU)" varies by Jira instance. Discover it via issue metadata tools on first use.

## List Components

List available components for a project.

**Trigger phrases:** "list components", "show components", "what components are available"

**Steps:**

1. Get Cloud ID
2. Fetch project metadata via `activate_jira_issue_management_tools` to get components
3. Display components in a table:

```
| Component | Description |
|-----------|-------------|
| Backend   | Server-side services |
| Frontend  | UI components |
| API       | REST API endpoints |
```

## Manage Labels

Add or remove labels from a Jira ticket.

**Trigger phrases:** "add label to PROJ-123", "label PROJ-123 with", "remove label from"

**Steps:**

1. Get Cloud ID
2. Fetch current issue to get existing labels
3. Add/remove requested labels
4. Update issue using `mcp_atlassian-mcp_editJiraIssue`:

   ```json
   {
     "fields": {
       "labels": ["existing-label", "new-label"]
     }
   }
   ```

5. Confirm update

**Output format:**

```
✅ Labels updated on PROJ-123:
   Added: urgent, needs-review
   Current: created-by-github-copilot, urgent, needs-review
```

## User Preferences

Store user preferences in `.jira-workflow-prefs.json` in the workspace root.

**Stored preferences:**

```json
{
  "lastComponent": "Backend",
  "defaultProject": "PROJ",
  "requestedByBU": "GLCP"
}
```

**Behavior:**

- On **Create Work**: Check for `lastComponent`, suggest if present
- On component selection: Update `lastComponent` in preferences
- User can override `requestedByBU` default by saying "set requested by to X"

**Preference commands:**

- "Set my default component to Backend"
- "Set my default project to PROJ"
- "Set requested by to ACME"
- "Show my preferences"
- "Clear my preferences"

## Assign Work

Assign a Jira ticket to a team member.

**Trigger phrases:** "assign PROJ-123 to", "give PROJ-123 to", "assign ticket to"

**Required information:**

- Ticket key (e.g., PROJ-123)
- Assignee (name or email)

**Steps:**

1. Get Cloud ID using `mcp_atlassian-mcp_getAccessibleAtlassianResources`
2. Look up the user's account ID using `mcp_atlassian-mcp_lookupJiraAccountId` with the provided name/email
3. If multiple matches, present options and ask user to clarify
4. Update the issue using `mcp_atlassian-mcp_editJiraIssue` with the assignee field:

   ```json
   {
     "fields": {
       "assignee": { "accountId": "<account-id>" }
     }
   }
   ```

5. Confirm assignment with ticket key and assignee name

**Output format:**

```
✅ PROJ-123 assigned to John Smith
```

## Do Work

Full development workflow: implement a Jira ticket with proper Git workflow and Jira updates.

**Trigger phrases:** "do work", "work on PROJ-123", "implement PROJ-123", "pick up PROJ-123"

**Prerequisites check:**

- Confirm Git repository exists in workspace
- Confirm clean working tree (no uncommitted changes)
- Verify Jira ticket exists and is accessible

### Task Complexity Assessment

Before starting implementation, assess the task complexity:

**Break into subtasks when:**

- Task involves multiple distinct components (e.g., API + UI + tests)
- Estimated implementation time exceeds 2-3 hours
- Multiple files across different domains need changes
- Task has natural logical divisions (e.g., "setup", "core logic", "integration")

**Keep as single task when:**

- Simple bug fix or small feature
- Changes localized to one area
- Can be completed in under an hour

### Subtask Workflow

If task warrants breakdown:

1. **Analyze and decompose** the parent ticket into logical subtasks
2. **Create subtasks** in Jira using `mcp_atlassian-mcp_createJiraIssue` with:

   ```json
   {
     "issueTypeName": "Sub-task",
     "parent": "PROJ-123",
     "summary": "<subtask summary>",
     "labels": ["created-by-github-copilot"]
   }
   ```

3. **Present subtask plan** to user for confirmation:

   ```
   📋 PROJ-123: Implement user authentication

   Proposed subtasks:
   1. PROJ-124: Set up authentication middleware
   2. PROJ-125: Implement login endpoint
   3. PROJ-126: Add JWT token generation
   4. PROJ-127: Write integration tests

   Proceed? (Y/n)
   ```

4. **Work on each subtask sequentially**:
   - Implement subtask
   - Commit with subtask reference
   - Update subtask in Jira
   - Transition subtask to Done
5. **After all subtasks complete**, update and transition parent ticket

See [references/do-work-workflow.md](references/do-work-workflow.md) for detailed implementation steps.

### Workflow Steps

```
1. Fetch ticket details
2. Create feature branch
3. Implement the work
4. Commit changes
5. Update Jira ticket
```

See [references/do-work-workflow.md](references/do-work-workflow.md) for detailed implementation steps.

### Branch Naming

Format: `<type>/<ticket-key>-<short-description>`

Examples:

- `feature/PROJ-123-user-authentication`
- `bugfix/PROJ-456-fix-date-format`
- `chore/PROJ-789-update-dependencies`

Derive `<type>` from issue type:

- Story/Feature → `feature/`
- Bug → `bugfix/`
- Task/Chore → `chore/`

### Commit Message Format

**For single tasks or parent tickets:**

```
<type>(<ticket-key>): <summary>

<detailed description>

Refs: <ticket-key>
Co-authored-by: GitHub Copilot <noreply@github.com>
```

**For subtasks (commit per subtask):**

```
<type>(<subtask-key>): <summary>

<detailed description>

Refs: <subtask-key>
Part-of: <parent-key>
Co-authored-by: GitHub Copilot <noreply@github.com>
```

The `Co-authored-by` trailer is a Git convention that GitHub recognizes and displays in the commit UI.

Example (subtask commit):

```
feat(PROJ-125): implement login endpoint

Add POST /api/auth/login endpoint with:
- Email/password validation
- User lookup and password verification
- Error responses for invalid credentials

Refs: PROJ-125
Part-of: PROJ-123
Co-authored-by: GitHub Copilot <noreply@github.com>
```

### Jira Update Content

After completing work, update the Jira ticket with:

- Summary of changes made
- Files modified/created
- Any relevant technical notes
- Next steps if work is partial

Use `mcp_atlassian-mcp_addCommentToJiraIssue` for the update.

## Error Handling

| Scenario | Action |
|----------|--------|
| Cannot find Cloud ID | Prompt user to verify Jira connection |
| Ticket not found | Verify ticket key format and project access |
| User not found | Verify name/email spelling, show similar matches |
| Multiple user matches | Present options for user to select |
| Component not found | List available components, ask user to select |
| Invalid label format | Labels cannot contain spaces; suggest alternatives |
| Custom field ID unknown | Fetch issue metadata to discover field IDs |
| Subtask creation fails | Check if Sub-task issue type exists in project |
| Parent ticket not found | Verify parent key when creating subtasks |
| Dirty working tree | Prompt user to commit/stash changes first |
| Branch already exists | Offer to checkout existing or create new |
| Create issue fails | Check required fields and permissions |

## Tool Activation Reference

This skill uses these MCP tool groups:

- `mcp_atlassian-mcp_*` - Core Jira operations (always available)
- `activate_jira_issue_management_tools` - Issue creation, editing, transitions
- `activate_search_tools_for_jira_and_confluence` - JQL search capabilities
