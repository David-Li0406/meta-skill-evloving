---
name: linear-backlog-grooming
description: "Review and clean up the Linear backlog. Close stale issues, update priorities, merge duplicates, request clarification. Triggers - backlog grooming, backlog cleanup, groom backlog."
---

# Linear Backlog Grooming

**Iron Law:** A healthy backlog is ACTIONABLE and CURRENT. Stale issues are noise.

## Overview

This skill reviews and cleans up the Linear backlog:
1. Close stale/obsolete issues
2. Update priorities based on current context
3. Merge duplicates
4. Request clarification on unclear issues
5. Archive completed-but-not-closed items

## Outputs

- Stale issues closed with explanation
- Priorities updated
- Duplicates merged
- Unclear issues flagged
- Backlog health metrics

---

## The Workflow

### Step 1: Get Backlog Snapshot

```typescript
// Get all backlog items
mcp__linear-server__list_issues({
  state: "Backlog",
  team: "team-name",
  limit: 100,
  orderBy: "createdAt"
});

// Also check triage
mcp__linear-server__list_issues({
  state: "Triage",
  team: "team-name",
  limit: 50
});
```

### Step 2: Identify Stale Issues

**Stale criteria:**
- No activity in 90+ days
- Referenced feature/code no longer exists
- Superseded by other work
- Original requester left

```markdown
## Stale Issue Review

| Issue | Age | Last Activity | Reason Stale |
|-------|-----|---------------|--------------|
| PEA-50 | 180d | 120d ago | Feature removed |
| PEA-55 | 150d | 150d ago | No engagement |
| PEA-60 | 100d | 95d ago | Superseded by PEA-200 |
```

### Step 3: Find Duplicates

Look for issues with:
- Similar titles
- Same root cause
- Overlapping scope

```markdown
## Potential Duplicates

### Group 1: Auth Issues
- PEA-100: "Login fails sometimes"
- PEA-150: "Intermittent login errors"
- PEA-180: "Auth token expiry issues"
→ Likely same root cause

### Group 2: Performance
- PEA-120: "Slow dashboard load"
- PEA-125: "Dashboard performance"
→ Merge into single issue
```

### Step 4: Flag Unclear Issues

Issues that need clarification:
- No reproduction steps
- Vague descriptions
- Missing context

```markdown
## Need Clarification

| Issue | Problem | Question to Ask |
|-------|---------|-----------------|
| PEA-70 | No steps to reproduce | How do we reproduce this? |
| PEA-75 | "It's broken" | What exactly is broken? Expected vs actual? |
```

### Step 5: Review Priorities

Check if priorities still make sense:

```markdown
## Priority Review

### Should Increase
| Issue | Current | Suggested | Reason |
|-------|---------|-----------|--------|
| PEA-80 | Medium | High | Blocking customer |

### Should Decrease
| Issue | Current | Suggested | Reason |
|-------|---------|-----------|--------|
| PEA-85 | High | Low | Edge case, workaround exists |
```

### Step 6: Execute Cleanup

#### Close Stale Issues
```typescript
mcp__linear-server__create_comment({
  issueId: "stale-issue-uuid",
  body: `## Closing: Stale

This issue has been inactive for [X] days.

**Reason:** [Why it's being closed]

If this is still relevant, please reopen with updated context.`
});

mcp__linear-server__update_issue({
  id: "stale-issue-uuid",
  state: "Canceled"
});
```

#### Merge Duplicates
```typescript
// Add context to primary issue
mcp__linear-server__create_comment({
  issueId: "primary-issue-uuid",
  body: "## Merged Issues\n\nConsolidating:\n- PEA-150: [context]\n- PEA-180: [context]"
});

// Close duplicates
mcp__linear-server__create_comment({
  issueId: "duplicate-issue-uuid",
  body: "Duplicate of PEA-100. Tracking there."
});

mcp__linear-server__update_issue({
  id: "duplicate-issue-uuid",
  state: "Duplicate"
});
```

#### Request Clarification
```typescript
mcp__linear-server__create_comment({
  issueId: "unclear-issue-uuid",
  body: `## Clarification Needed

To move forward, we need:

- [ ] Steps to reproduce
- [ ] Expected vs actual behavior
- [ ] Environment details

Please update with this information.`
});

mcp__linear-server__update_issue({
  id: "unclear-issue-uuid",
  labels: ["needs-info"]
});
```

#### Update Priorities
```typescript
mcp__linear-server__update_issue({
  id: "issue-uuid",
  priority: 2  // 1=Urgent, 2=High, 3=Normal, 4=Low
});
```

### Step 7: Generate Health Report

```markdown
## Backlog Health Report

**Date:** [Today]
**Team:** [Team Name]

### Metrics
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Issues | 150 | 120 | -30 |
| Stale (>90d) | 45 | 0 | -45 |
| Duplicates | 12 | 0 | -12 |
| Needs Info | 0 | 8 | +8 |

### Actions Taken
- Closed: 25 stale issues
- Merged: 6 duplicate groups → 6 primary issues
- Flagged: 8 issues need clarification
- Re-prioritized: 5 issues

### Backlog Age Distribution
- < 30 days: 40 issues
- 30-60 days: 35 issues
- 60-90 days: 25 issues
- > 90 days: 0 issues ✓

### Recommendations
1. [Action item for team]
2. [Process improvement]

**Next grooming:** [Suggested date - typically every 2-4 weeks]
```

---

## Grooming Cadence

| Backlog Size | Recommended Frequency |
|--------------|----------------------|
| < 50 issues | Monthly |
| 50-150 issues | Bi-weekly |
| > 150 issues | Weekly |

---

## Quick Reference

```
PROCESS: Snapshot → Stale → Duplicates → Unclear → Priorities → Execute → Report
OUTPUT:  Clean backlog, health metrics

STALE CRITERIA:
- No activity 90+ days
- Feature/code removed
- Superseded by other work

TOOLS:
- mcp__linear-server__list_issues
- mcp__linear-server__update_issue
- mcp__linear-server__create_comment
```

## Red Flags - STOP

- Closing without explanation → STOP, always document why
- Mass closing without review → STOP, review each issue
- Backlog growing faster than grooming → STOP, address root cause

---

## Integration

**Uses:**
- **Linear MCP** - All operations

**Pairs with:**
- **linear-cycle-planning** - Clean backlog before planning
- **linear-project-health** - Part of overall health
