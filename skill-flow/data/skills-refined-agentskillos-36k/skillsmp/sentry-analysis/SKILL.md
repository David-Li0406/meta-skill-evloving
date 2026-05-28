---
name: sentry-analysis
description: Analyzes Sentry errors and creates Jira tickets for recurring issues. Use when monitoring errors, creating bug tickets, or analyzing crash reports.
allowed-tools: mcp__sentry, mcp__jira, Read, Write
---

# Sentry Analysis Skill

You analyze Sentry errors and create Jira tickets for issues that exceed thresholds.

## Mission

Monitor Sentry for recurring errors and create actionable Jira tickets.

## Process

### 1. Fetch Unresolved Issues
```
mcp__sentry: list_issues with status=unresolved
```

### 2. Check Event Count Thresholds

| Level | Events (24h) | Action |
|-------|--------------|--------|
| `fatal` | 1+ | Immediate ticket |
| `error` | 10+ | Create ticket |
| `warning` | 50+ | Create ticket |
| `info` | 100+ | Create ticket |

### 3. Get Issue Details
For issues exceeding threshold:
```
mcp__sentry: get_issue_events to get latest event with stack trace
```

### 4. Create Jira Ticket
```
mcp__jira: create_issue with type=Bug
```

Use this template for description:

```markdown
## Sentry Error Report

**Error:** {title}
**Level:** {level}
**Environment:** {environment}
**Occurrences:** {count}

## Stack Trace
{formatted_stack_trace}

## Sentry Link
{permalink}

---
*Auto-created by AI Sentry Agent*
*Fingerprint: {issue_id}*
```

### 5. Track Created Tickets
Save to `sentry_tracking.json` to prevent duplicates:
```json
{
  "processed_issues": {
    "sentry-issue-id": {
      "jira_ticket": "PROJ-123",
      "created_at": "2026-01-17T12:00:00Z"
    }
  }
}
```

## Output

Save results to `sentry_result.json`:

```json
{
  "status": "success",
  "issues_checked": 50,
  "tickets_created": [
    {
      "sentry_id": "12345",
      "jira_ticket": "PROJ-456",
      "title": "Error in auth.py"
    }
  ],
  "skipped_duplicates": 3
}
```
