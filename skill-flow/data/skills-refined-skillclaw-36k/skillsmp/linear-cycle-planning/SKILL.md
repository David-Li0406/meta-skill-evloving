---
name: linear-cycle-planning
description: "Plan issues for an upcoming Linear cycle/sprint. Review backlog, prioritize, assign to cycle, balance workload. Triggers - cycle planning, sprint planning, plan cycle."
---

# Linear Cycle Planning

**Iron Law:** Every cycle needs CLEAR GOALS and BALANCED WORKLOAD. No overcommitting.

## Overview

This skill helps plan issues for an upcoming Linear cycle. It involves:
1. Reviewing the backlog
2. Selecting issues for the cycle
3. Balancing workload across team
4. Setting cycle goals

## Outputs

- Issues assigned to cycle
- Cycle goals documented
- Workload balanced across assignees
- Carry-over items identified

---

## The Workflow

### Step 1: Get Cycle Context

```typescript
// Get the target cycle
mcp__linear-server__list_cycles({
  teamId: "team-uuid",
  type: "next"  // or "current" for mid-cycle adjustments
});

// Get team members
mcp__linear-server__list_users({
  team: "team-name"
});
```

### Step 2: Review Current State

```typescript
// Check carry-over from current cycle
mcp__linear-server__list_issues({
  cycle: "current",
  state: "In Progress",  // Not completed
  limit: 50
});

// Review backlog candidates
mcp__linear-server__list_issues({
  state: "Backlog",
  team: "team-name",
  limit: 50
});
```

### Step 3: Assess Capacity

```markdown
## Team Capacity

| Member | Availability | Notes |
|--------|--------------|-------|
| Alice | 100% | Full cycle |
| Bob | 50% | OOO week 2 |
| Carol | 80% | Support rotation |

**Total Capacity:** X story points / Y issues
**Cycle Length:** [dates]
**Working Days:** [count]
```

### Step 4: Identify Priorities

Use this framework:

```markdown
## Priority Assessment

### Must Have (P0)
- [Issues that MUST complete this cycle]
- Commitments, blockers, deadlines

### Should Have (P1)
- [Important but not critical]
- High value, good progress

### Nice to Have (P2)
- [If capacity allows]
- Lower impact, skill building
```

### Step 5: Select Issues

```markdown
## Proposed Cycle Plan

### From Backlog (New Work)
| Issue | Priority | Estimate | Assignee |
|-------|----------|----------|----------|
| PEA-100 | P0 | 3 | Alice |
| PEA-101 | P1 | 5 | Bob |

### Carry Over (In Progress)
| Issue | Status | Remaining | Assignee |
|-------|--------|-----------|----------|
| PEA-90 | 80% done | 1 | Alice |

### Totals
- New work: X points
- Carry over: Y points
- Total: Z points
- Capacity: W points
- Buffer: [percentage]
```

### Step 6: Balance Workload

```markdown
## Workload Distribution

| Member | Assigned | Capacity | Utilization |
|--------|----------|----------|-------------|
| Alice | 8 pts | 10 pts | 80% ✓ |
| Bob | 5 pts | 5 pts | 100% ⚠️ |
| Carol | 6 pts | 8 pts | 75% ✓ |

**Target:** 70-85% utilization (buffer for unknowns)
**Flag:** >90% utilization = overcommitted
```

### Step 7: Set Cycle Goals

```markdown
## Cycle Goals

**Theme:** [What this cycle is about]

**Objectives:**
1. [Measurable goal 1]
2. [Measurable goal 2]
3. [Measurable goal 3]

**Success Criteria:**
- [ ] [How we know we succeeded]
- [ ] [Metric or deliverable]
```

### Step 8: Assign to Cycle

```typescript
// Assign issues to cycle
for (const issue of selectedIssues) {
  await mcp__linear-server__update_issue({
    id: issue.id,
    cycle: "next-cycle-uuid",
    assignee: issue.assignee
  });
}
```

### Step 9: Document Plan

```typescript
// Create or update cycle document
mcp__linear-server__create_document({
  title: `Cycle Plan: [Cycle Name]`,
  content: `# Cycle Plan

## Goals
[Cycle goals]

## Commitments
[P0 items - must complete]

## Planned
[P1 items - should complete]

## Stretch
[P2 items - if capacity]

## Capacity
[Team capacity breakdown]

## Risks
[Known risks and mitigations]
`,
  project: "team-project-uuid"
});
```

---

## Planning Checklist

Before finalizing:

- [ ] Carry-over items accounted for
- [ ] P0 items fit in capacity
- [ ] No one over 85% utilization
- [ ] Dependencies identified
- [ ] Goals are measurable
- [ ] Risks documented
- [ ] Team reviewed and agreed

---

## Capacity Guidelines

| Utilization | Status | Action |
|-------------|--------|--------|
| < 60% | Under-planned | Add more work |
| 60-85% | Healthy | Good buffer |
| 85-95% | Tight | Remove nice-to-haves |
| > 95% | Overcommitted | Must reduce scope |

**Buffer is essential** - unexpected work, bugs, meetings, etc.

---

## Quick Reference

```
PROCESS: Context → Review → Capacity → Prioritize → Select → Balance → Goals → Assign → Document
OUTPUT:  Issues assigned to cycle, goals documented

CAPACITY TARGETS:
- Individual: 70-85% utilization
- Team: 75-85% total capacity
- Buffer: 15-25% for unknowns

TOOLS:
- mcp__linear-server__list_cycles
- mcp__linear-server__list_issues
- mcp__linear-server__list_users
- mcp__linear-server__update_issue
- mcp__linear-server__create_document
```

## Red Flags - STOP

- >90% utilization → STOP, reduce scope
- No P0 items defined → STOP, clarify priorities
- All work is P0 → STOP, prioritize properly
- No buffer planned → STOP, leave room for unknowns

---

## Integration

**Uses:**
- **Linear MCP** - All operations

**Pairs with:**
- **linear-backlog-grooming** - Clean backlog before planning
- **linear-project-health** - Track cycle progress
