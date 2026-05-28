# Daily Codebase Insights Prompt

Generate a daily summary of codebase activity.

## Input Data

**Date:** {{DATE}}

### Pull Requests

{{PRS_DATA}}

### Commits

{{COMMITS_DATA}}

### Work Items

{{WORKITEMS_DATA}}

### Confluence (if available)

{{CONFLUENCE_DATA}}

## Task

Create a concise daily codebase activity summary covering:

1. **Pull Requests** - What was opened, merged, or reviewed
2. **Commits** - Key changes by area/author
3. **Work Items** - What started, what completed
4. **Key Changes** - Synthesize the most significant activity

## Output Format

```markdown
## {{DATE}} - Codebase Activity

### Summary

Brief 1-2 sentence overview of the day's activity.

### Pull Requests

- **Opened:** N
- **Merged:** N
- **In Review:** N

Notable PRs:

- [PR#ID](pr-url) type([#ticketId](ticket-url)): title (author) - brief context

### Commits

- Total: N commits
- Key changes by area

### Work Items

- **Started:** N items moved to Active/In Progress
- **Completed:** N items moved to Done/Closed

### Key Changes

Synthesized summary of the most significant changes and their impact.
```

## URL Construction

When `url` field is null, construct URLs using these patterns:

**Azure DevOps PRs:**

```
https://dev.azure.com/{org}/{project}/_git/{repository}/pullrequest/{id}
```

- Default org: `drmaxglobal`
- Default project: `ecommerce-operations`
- Repository: use the `repository` field from PR data

**Azure DevOps Work Items:**

```
https://dev.azure.com/{org}/{project}/_workitems/edit/{id}/
```

- Default org: `drmaxglobal`
- Default project: `platform-team`

**Ticket ID extraction:**

- Extract from PR title patterns like `feat(123456):`, `fix(123456):`, `chore(123456):`
- The number in parentheses is the work item/ticket ID

## Guidelines

- **Make ALL references clickable** - PRs, tickets, and work items should be markdown links
- **Format:** `[PR#89400](url) feat([#178334](ticket-url)): description`
- **Group by `updatedDate`** - this is the most recent activity date (update > close > create)
- If a PR was created earlier but updated on {{DATE}}, include it in this report
- Focus on **what changed** and **why it matters**
- Group related commits into themes
- Highlight cross-cutting changes that affect multiple areas
- Note any blocked or abandoned work
- Keep it scannable - busy developers will skim
