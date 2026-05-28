# Jira Transitions Guide

Complete reference for transitioning issues between statuses.

## How Transitions Work

Transitions are workflow-defined paths between statuses. Not all transitions are available from every status.

```
┌─────────┐    Start     ┌─────────────┐    Submit    ┌───────────┐
│ To Do   │ ──────────── │ In Progress │ ──────────── │ In Review │
└─────────┘              └─────────────┘              └───────────┘
                               │                            │
                               │ Block                      │ Approve
                               ▼                            ▼
                         ┌─────────┐                  ┌──────────┐
                         │ Blocked │                  │   Done   │
                         └─────────┘                  └──────────┘
```

## Discovering Available Transitions

Before transitioning, always list available transitions:

```json
{
  "issueKey": "PROJ-123",
  "listTransitions": true
}
```

Response example:
```json
{
  "transitions": [
    { "id": "21", "name": "Start Progress" },
    { "id": "31", "name": "Submit for Review" },
    { "id": "41", "name": "Block" }
  ]
}
```

## Executing Transitions

### By Name (Recommended)
```json
{
  "issueKey": "PROJ-123",
  "transitionName": "Start Progress"
}
```

### By ID
```json
{
  "issueKey": "PROJ-123",
  "transitionId": "21"
}
```

## Common Transition Names

| From | To | Common Names |
|------|-----|--------------|
| To Do | In Progress | "Start Progress", "Begin Work", "Start" |
| In Progress | In Review | "Submit for Review", "Ready for Review", "Submit" |
| In Progress | Blocked | "Block", "Flag as Blocked" |
| Blocked | In Progress | "Unblock", "Resume", "Continue" |
| In Review | Done | "Approve", "Complete", "Close" |
| In Review | In Progress | "Request Changes", "Reject", "Return" |
| Any | To Do | "Reopen", "Back to Backlog" |

## Transitions with Required Fields

Some transitions require additional fields:

### Resolution Required
```json
{
  "issueKey": "PROJ-123",
  "transitionName": "Done",
  "fields": {
    "resolution": { "name": "Done" }
  }
}
```

### Comment Required
```json
{
  "issueKey": "PROJ-123",
  "transitionName": "Block",
  "comment": "Blocked waiting for API access from external team"
}
```

## Common Resolution Values

| Resolution | When to Use |
|------------|-------------|
| Done | Work completed successfully |
| Won't Do | Decided not to implement |
| Duplicate | Already covered by another issue |
| Cannot Reproduce | Bug could not be verified |
| Won't Fix | Known issue, accepted as-is |

## Validation Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Transition not found" | Invalid transition name/ID | List transitions first |
| "Field required" | Missing required field | Check transition schema |
| "Invalid resolution" | Wrong resolution value | Use valid resolution name |
| "Transition not available" | Not allowed from current status | Check current status |

## Best Practices

1. **Always list transitions first** - Don't assume transition names
2. **Use dry-run mode** - Validate before executing
3. **Add comments** - Explain why status changed
4. **Check required fields** - Some transitions need resolution
5. **Verify current status** - Transitions depend on current state
