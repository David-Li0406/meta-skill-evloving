---
name: jira-ticket-enrichment
description: Enriches Jira tickets created by Sentry with code analysis, relevant files, and creates a GitHub PR with the fix plan
---

# Jira Ticket Enrichment Skill

This skill is triggered when Sentry creates a Jira ticket. It uses MCP tools to:
1. Fetch the full Sentry error details (stack trace, tags, context)
2. Discover the relevant code files in the GitHub repository
3. Analyze the root cause of the error
4. Update the Jira ticket with enriched information
5. Create a GitHub Pull Request with a detailed fix plan

## Trigger

This skill activates when:
- A Jira webhook fires with `issue_created` event
- The ticket description contains a Sentry Issue link (e.g., `JAVASCRIPT-REACT-1`)

## MCP Tools Required

### 1. Sentry MCP (`@sentry/mcp-server`)
Used to fetch complete error details from Sentry.

**Tools:**
- `get_sentry_issue`: Get issue details including title, status, and metadata
- `get_sentry_event`: Get full stack trace and context for a specific event

### 2. GitHub MCP (`@anthropic-ai/github-mcp`)  
Used to access the repository, create branches, and open PRs.

**Tools:**
- `get_file_contents`: Read specific files from the repository
- `search_code`: Search for code patterns across the repo
- `create_branch`: Create a new branch for the fix
- `create_pull_request`: Open a PR with the plan
- `create_or_update_file`: Add PLAN.md to the PR

### 3. Atlassian/Jira MCP (`@anthropic-ai/atlassian-mcp`)
Used to update the Jira ticket with enriched information.

**Tools:**
- `get_issue`: Fetch full ticket details
- `update_issue`: Update description with analysis
- `add_comment`: Add comments with progress updates

## Workflow Steps

### Step 0: Notify Jira - Starting Work
Add a comment to the Jira ticket to notify that work has started.

```
Call: mcp_atlassian.add_comment(
  issue_key="PROJ-123",
  body="🤖 **AI Agent Started**\n\nThe AI Planning Agent has picked up this ticket and is now:\n- Fetching Sentry error details\n- Analyzing the codebase\n- Creating a fix plan\n\n⏳ This typically takes 2-5 minutes."
)
```

### Step 1: Parse Jira Webhook
Extract the Sentry Issue ID from the ticket description.

```
Input: Jira webhook payload
Extract: Sentry Issue ID (e.g., "JAVASCRIPT-REACT-1")
Extract: Repository name from Sentry tags (e.g., "rom-orlovich/manga-creator")
```

### Step 2: Fetch Sentry Details
Use the Sentry MCP to get the complete error information.

```
Call: mcp_sentry.get_sentry_issue(issue_id="JAVASCRIPT-REACT-1")
Call: mcp_sentry.get_sentry_event(issue_id="JAVASCRIPT-REACT-1", event_id="latest")

Output:
- Full stack trace with all frames
- Error message
- Browser/OS context
- User affected
- Tags (including repository)
```

### Step 3: Discover Relevant Files
Use the GitHub MCP to find and read the affected files.

```
Parse stack trace for file paths:
- /components/Header.tsx:24:17
- /utils/auth.ts:45:3

Call: mcp_github.get_file_contents(repo="rom-orlovich/manga-creator", path="src/components/Header.tsx")
Call: mcp_github.search_code(repo="rom-orlovich/manga-creator", query="onClick Header")

Output:
- Full source code of affected files
- Related files that import/use the affected code
```

### Step 4: Analyze Root Cause
Use Claude's understanding to determine the root cause.

```
Analyze:
- The exact line causing the error
- Why the error occurs (null reference, type error, etc.)
- The broader context of the affected function//component
- Similar patterns in the codebase that might also be affected

Output:
- Root cause explanation
- Affected code scope
- Risk assessment (low/medium/high)
```

### Step 5: Create Fix Plan
Generate a detailed plan following TDD principles.

```
Create PLAN.md with:
1. Problem Summary
2. Root Cause Analysis
3. Affected Files
4. Fix Strategy
5. Test Plan (what tests to write first)
6. Implementation Steps
7. Validation Criteria
8. Risk Assessment
```

### Step 6: Update Jira Ticket
Enrich the ticket with the discovered information.

```
Call: mcp_jira.update_issue(
  issue_key="PROJ-123",
  description="{enriched_description_with_analysis}"
)

Call: mcp_jira.add_comment(
  issue_key="PROJ-123", 
  body="🤖 AI Analysis Complete. View the fix plan: {pr_url}"
)
```

### Step 7: Create GitHub PR
Open a draft PR with the plan for human approval.

```
Call: mcp_github.create_branch(repo="...", branch="fix/sentry-JAVASCRIPT-REACT-1")

Call: mcp_github.create_or_update_file(
  repo="...",
  path="PLAN.md",
  content="{plan_content}",
  branch="fix/sentry-JAVASCRIPT-REACT-1"
)

Call: mcp_github.create_pull_request(
  repo="...",
  title="[AI-FIX] Error: This is your first2 error!",
  body="{pr_description_with_plan}",
  head="fix/sentry-JAVASCRIPT-REACT-1",
  base="main",
  draft=true
)
```

## Output Format

### Enriched Jira Description
```markdown
## 🔍 AI Analysis

### Error Details
**Sentry Issue:** [JAVASCRIPT-REACT-1](https://sentry.io/...)
**First Seen:** 2026-01-19 14:30:00
**Occurrences:** 15
**Users Affected:** 3

### Stack Trace
```javascript
Error: This is your first2 error!
    at onClick (components/Header.tsx:24:17)
    at HTMLButtonElement.handleClick (react-dom.js:123)
    at dispatchEvent (events.js:45)
```

### Root Cause
The error occurs because `updateFrom` is called on an object that is undefined.
This happens when the user clicks the header button before the auth state is initialized.

### Affected Files
1. `src/components/Header.tsx` (line 24) - **Direct cause**
2. `src/hooks/useAuth.ts` - Related auth state management
3. `src/context/AuthContext.tsx` - Provides the auth state

### Fix Plan
📄 **PR Draft:** [View Plan](https://github.com/.../pull/456)

**Status:** Pending Approval
```

### GitHub PR Description
```markdown
# 🤖 AI-Generated Fix Plan

## Problem
Error `This is your first2 error!` occurring in Header.tsx

## Sentry Issue
[JAVASCRIPT-REACT-1](https://sentry.io/...)

## Root Cause Analysis
The `updateFrom` method is being called on an undefined object because the
auth state has not finished initializing when the user clicks the button.

## Plan

### 1. Write Tests First
- [ ] Add test for button click when auth is loading
- [ ] Add test for button click when auth is ready

### 2. Implement Fix
- [ ] Add null check before calling `updateFrom`
- [ ] Add loading state to prevent premature clicks
- [ ] Update button to be disabled during loading

### 3. Validation
- [ ] All existing tests pass
- [ ] New tests pass
- [ ] Manual test in browser confirms fix

---
⚠️ **This is a Draft PR.** To approve, comment `@agent approve` or use Slack.
```

## Approval Channels

After the skill completes, the task waits for human approval via:

1. **GitHub**: Comment `@agent approve` on the PR
2. **Slack**: Click the "Approve" button in the notification
3. **Jira**: Transition the ticket to "Approved" status

## Configuration

The skill requires these environment variables:
- `SENTRY_AUTH_TOKEN`: For Sentry MCP authentication
- `SENTRY_ORG`: Your Sentry organization slug
- `GITHUB_TOKEN`: For GitHub MCP authentication  
- `JIRA_URL`: Your Atlassian URL
- `JIRA_EMAIL`: Your Atlassian account email
- `JIRA_API_TOKEN`: Atlassian API token
