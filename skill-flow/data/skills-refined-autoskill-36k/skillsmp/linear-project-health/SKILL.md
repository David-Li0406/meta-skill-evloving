---
name: linear-project-health
description: "Generate health report for a Linear project. Progress vs plan, blocked issues, overdue items, risk assessment. Triggers - project health, project status, project report."
---

# Linear Project Health

**Iron Law:** VISIBILITY enables action. Surface problems early, celebrate progress.

## Overview

This skill generates health reports for Linear projects:
1. Progress vs plan
2. Blocked issues
3. Overdue items
4. Risk assessment
5. Velocity trends

## Outputs

- Project health dashboard
- Risk identification
- Actionable recommendations
- Progress metrics

---

## The Workflow

### Step 1: Get Project Context

```typescript
// Get project details
mcp__linear-server__get_project({
  query: "project-name-or-id"
});

// Get all project issues
mcp__linear-server__list_issues({
  project: "project-name",
  limit: 200,
  includeArchived: false
});
```

### Step 2: Calculate Progress Metrics

```markdown
## Progress Overview

**Project:** [Name]
**Target Date:** [Date]
**Days Remaining:** [X days]

### Issue Status
| Status | Count | Percentage |
|--------|-------|------------|
| Done | 25 | 50% |
| In Progress | 10 | 20% |
| Backlog | 15 | 30% |
| **Total** | 50 | 100% |

### Progress Bar
[██████████░░░░░░░░░░] 50%

### Burndown
- Expected completion: [based on velocity]
- On track: Yes/No
```

### Step 3: Identify Blocked Issues

```typescript
// Get blocked issues
mcp__linear-server__list_issues({
  project: "project-name",
  state: "In Progress",
  // Check for blockedBy relations
  includeRelations: true
});
```

```markdown
## Blocked Issues

| Issue | Blocked By | Days Blocked | Impact |
|-------|------------|--------------|--------|
| PEA-100 | PEA-50 (external dep) | 5 | High |
| PEA-110 | Waiting on design | 3 | Medium |

**Action Required:**
- PEA-100: Escalate external dependency
- PEA-110: Follow up with design team
```

### Step 4: Find Overdue Items

```markdown
## Overdue Issues

| Issue | Due Date | Days Overdue | Assignee |
|-------|----------|--------------|----------|
| PEA-120 | Jan 10 | 5 days | Alice |
| PEA-125 | Jan 12 | 3 days | Bob |

**Root Causes:**
- PEA-120: Scope creep, needs re-estimation
- PEA-125: Assignee overloaded
```

### Step 5: Assess Risks

```markdown
## Risk Assessment

### High Risk 🔴
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| External API delay | Blocks launch | High | Prepare fallback |

### Medium Risk 🟡
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Scope creep | Timeline slip | Medium | Strict scope control |

### Low Risk 🟢
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Team availability | Minor delay | Low | Cross-training |
```

### Step 6: Calculate Velocity

```markdown
## Velocity Trends

### Last 4 Cycles
| Cycle | Completed | Carried Over | Velocity |
|-------|-----------|--------------|----------|
| Cycle 4 | 15 | 3 | 12 |
| Cycle 3 | 12 | 4 | 8 |
| Cycle 2 | 10 | 5 | 5 |
| Cycle 1 | 8 | 2 | 6 |

**Trend:** Improving ↑
**Average Velocity:** 7.75 issues/cycle
**Predicted Completion:** [X cycles / Y weeks]
```

### Step 7: Generate Health Score

```markdown
## Project Health Score

| Factor | Score | Weight | Weighted |
|--------|-------|--------|----------|
| Progress vs Plan | 7/10 | 30% | 2.1 |
| Blocked Issues | 6/10 | 20% | 1.2 |
| Overdue Items | 5/10 | 20% | 1.0 |
| Velocity Trend | 8/10 | 15% | 1.2 |
| Risk Level | 6/10 | 15% | 0.9 |

**Overall Health Score: 6.4/10** 🟡

### Health Indicators
- 🟢 8-10: Healthy - On track
- 🟡 5-7: Caution - Needs attention
- 🔴 0-4: Critical - Intervention required
```

### Step 8: Recommendations

```markdown
## Recommendations

### Immediate Actions (This Week)
1. **Unblock PEA-100** - Escalate external dependency to [person]
2. **Re-scope PEA-120** - Break into smaller issues
3. **Rebalance load** - Move 2 issues from Bob to Carol

### Short-term (This Cycle)
1. Add buffer for unknowns - currently at 0%
2. Address technical debt blocking feature work
3. Schedule design review for upcoming features

### Process Improvements
1. Earlier dependency identification in planning
2. More frequent check-ins on blocked items
3. Better estimation practices
```

### Step 9: Save Report

```typescript
mcp__linear-server__create_document({
  title: `Project Health: [Project Name] - [Date]`,
  content: `[Full report markdown]`,
  project: "project-uuid",
  icon: ":chart_with_upwards_trend:"
});
```

---

## Health Report Template

```markdown
# Project Health Report: [Project Name]

**Generated:** [Date]
**Period:** [Cycle/Sprint/Date Range]

## Executive Summary
[2-3 sentence overview of project health]

## Key Metrics
- Progress: X% complete
- Health Score: Y/10
- Velocity: Z issues/cycle
- On Track: Yes/No

## Status Breakdown
[Issue status table]

## Blockers & Risks
[Blocked issues and risk assessment]

## Recommendations
[Prioritized action items]

## Next Review
[Scheduled date]
```

---

## Quick Reference

```
PROCESS: Context → Progress → Blockers → Overdue → Risks → Velocity → Score → Recommendations → Save
OUTPUT:  Health report with metrics and recommendations

HEALTH SCORE:
- 8-10 🟢 Healthy
- 5-7 🟡 Caution
- 0-4 🔴 Critical

TOOLS:
- mcp__linear-server__get_project
- mcp__linear-server__list_issues
- mcp__linear-server__create_document
```

## Red Flags - STOP

- >20% issues blocked → STOP, address blockers immediately
- Velocity declining 3+ cycles → STOP, investigate root cause
- >10% issues overdue → STOP, re-plan or re-scope

---

## Integration

**Uses:**
- **Linear MCP** - All operations

**Pairs with:**
- **linear-cycle-planning** - Health informs planning
- **linear-backlog-grooming** - Part of overall health
- **reply-linear-bugs** - Address bug blockers
