---
name: review-tickets
description: Audit your ScoreVision Jira tickets against the current codebase—identify completed work, stale tickets, and status mismatches
---

# Review ScoreVision Tickets

Review and update Jira tickets based on the current codebase state.

## References

- For **workflow states and valid transitions**, reference the `ticket-workflow` skill
- For **acli command syntax**, reference the `jira-cli` skill

## Workflow

### Step 1: Gather Open Tickets

Query for open tickets assigned to the current user:

```bash
acli jira workitem search --jql "assignee = currentUser() AND resolution = Unresolved" --fields "key,status,summary"
```

### Step 2: Categorize Tickets

Group tickets by their current status. Reference the `ticket-workflow` skill for ScoreVision's workflow states and status categories.

### Step 3: Analyze Each Ticket

For each ticket, correlate with codebase state to determine appropriate action.

#### Check Codebase for Evidence

1. **Search for related code:**
   - Look for file paths mentioned in ticket description
   - Search for keywords from ticket summary
   - Check recent git commits for ticket key

2. **Check git history:**

   ```bash
   git log --oneline --grep="<ticket-id>"
   ```

3. **Check recent releases:**

   ```bash
   git tag --sort=-v:refname | head -10
   git log --oneline <previous-tag>..<current-tag>
   ```

### Step 4: Present Recommendation Plan

**IMPORTANT:** Before executing any modifications, present a recommendation plan for user approval.

For each ticket that needs modification:

```
## Recommendation: <TICKET-ID>

### Current State
- **Status:** <current status>
- **Summary:** <ticket summary>

### Evidence Gathered
- Git commits: <list relevant commits>
- Code files: <list relevant files>
- Release inclusion: <which release, if any>
- Deployment status: <deployed to which environment>

### Recommended Action
<What to do: transition, comment, close, or keep as-is>

### Rationale
<Why this action is appropriate based on evidence>

### Command to Execute
<acli command - reference jira-cli skill for syntax>
```

Wait for user approval before executing commands.

### Step 5: Execute Approved Actions

Only after user approval, execute the recommended actions.

#### Action Types

**Add Comment** - When you have status updates to share:

- Partial completion updates
- Investigation findings
- Blockers identified
- Work no longer relevant

**Transition Status** - When ticket should move to a different state. Reference `ticket-workflow` for valid transitions.

**Close** - When work is complete and deployed

**Keep As-Is** - When status accurately reflects reality

### Step 6: Batch Updates

For multiple tickets needing the same action, present as a batch recommendation and execute together after approval.

## Decision Criteria

### When to Close/Complete

- Code is merged to main branch
- Feature is included in a tagged release
- Release has been deployed (if applicable)

### When to Move to Blocked/On Hold

- External dependency not available
- Waiting for clarification from stakeholder
- Blocked by another ticket

### When to Add Comment Only

- Partial progress made
- Investigation complete but implementation not started
- Status update without state change

### When to Keep As-Is

- Actively being worked on
- Status accurately reflects reality
- No new information to add

## Output Format

After review, provide a summary:

```
## Ticket Review Summary

### Updated
- <TICKET-1>: <action taken>
- <TICKET-2>: <action taken>

### Kept As-Is
- <TICKET-3>: <reason>

### Needs Manual Review
- <TICKET-4>: <why it needs discussion>

### Recommended Actions (Not Executed)
- <TICKET-5>: <suggested action and why>
```

## Safety Notes

- Always verify before transitioning tickets
- Prefer manual confirmation over auto-execution
- Add comments explaining changes for audit trail
- Don't close tickets without confirming deployment status
