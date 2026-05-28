---
name: resolve-linear-tech-debt
description: "Resolve Linear issues tagged with \"tech-debt\". Decide to address now, schedule, or close. Triggers - resolve tech debt, technical debt, debt triage, cleanup."
---

# Resolve Linear Tech Debt

**Iron Law:** Tech debt produces SCHEDULING DECISIONS. Address now, schedule, or close with reasoning.

> ⚠️ **ONE ISSUE AT A TIME**
>
> Work on ONE tech debt item, submit PR (if addressing), then move to the next.
> Do NOT start a second item until the first is resolved (PR submitted, scheduled, or closed).
> This ensures focused work, clean commits, and proper review cycles.

## Overview

This skill handles Linear issues tagged with "tech-debt". Every tech debt item must be:
1. Addressed in current cycle (becomes active work)
2. Scheduled for future cycle (with timeline)
3. Closed with explanation (won't do, obsolete, or already resolved)

## Valid Outcomes

| Outcome | When to Use | Action |
|---------|-------------|--------|
| **Address Now** | High impact, blocking other work | Add to current cycle, create plan |
| **Schedule** | Valid but not urgent | Assign to future cycle/milestone |
| **Close - Obsolete** | Code/feature no longer exists | Close with explanation |
| **Close - Already Fixed** | Debt was addressed elsewhere | Link to fix, close |
| **Close - Won't Do** | Cost > benefit | Document reasoning, close |

---

## The Workflow

### Step 1: List Tech Debt (Priority Order)

**Filter by "Todo" status and work highest priority first:**

```typescript
mcp__linear-server__list_issues({
  label: "tech-debt",
  state: "Todo",  // Only unstarted debt items
  limit: 20
});
// Note: Linear API doesn't filter by priority - sort results client-side
```

**Sort results by priority (work in this sequence):**
1. **Urgent** (priority: 1) - Blocking critical work
2. **High** (priority: 2) - Significant impact
3. **Normal** (priority: 3) - Standard cleanup
4. **Low** (priority: 4) - Nice to have
5. **No Priority** (priority: 0) - Needs assessment first

**Present sorted by priority:**

```markdown
## Pending Tech Debt (Priority Order)

| Priority | ID | Title | Category |
|----------|-----|-------|----------|
| 🔴 Urgent | PEA-100 | Security: Upgrade auth library | Security |
| 🟠 High | PEA-101 | Refactor user service | Maintainability |
| 🟡 Normal | PEA-102 | Add missing tests for checkout | Testing |

**Recommendation:** Start with PEA-100 (Urgent priority)
```

**Default behavior:** If user says "next item" without specifying, always pick the highest priority unaddressed item.

### Step 2: Assess Each Item (Starting from Highest Priority)

For each tech debt issue, evaluate:

```markdown
## Tech Debt Assessment: [ID]

**What:** [What needs to be cleaned up]
**Why:** [Why this is debt - shortcuts, outdated, etc.]

**Impact Assessment:**
- Blocks other work: Yes/No
- Causes bugs: Yes/No
- Slows development: High/Medium/Low
- Security risk: Yes/No

**Effort Estimate:** Small (<1 day) / Medium (1-3 days) / Large (>3 days)

**Dependencies:** [What must happen first or after]
```

### Step 3: Explore Codebase (Recommended)

**For accurate assessment, explore the affected code:**

```typescript
// Dispatch Explore agent for context
Task({
  subagent_type: "Explore",
  prompt: `
    Research tech debt item: "[debt title]"

    Find:
    1. Affected code files and scope
    2. How widespread is this pattern?
    3. Dependencies on the affected code
    4. Existing tests that would need updating
    5. Is this already partially addressed?

    Return findings to inform scheduling decision.
  `,
  description: "Explore codebase for tech debt assessment"
});
```

**Present findings:**

```markdown
## Codebase Analysis

### Affected Scope
- `src/utils/oldPattern.ts` - Main file (200 lines)
- 15 files import this module
- Used in 3 critical paths

### Actual Effort
- Code to change: ~150 lines
- Tests to update: 8 test files
- Documentation: 2 files

### Current State
- 30% of codebase uses new pattern
- This is the last holdout of old pattern

### Recommendation
Based on analysis: [DO NOW / SCHEDULE / CLOSE]
```

### Step 4: Prioritize

Use this matrix:

```
                    Low Effort    High Effort
High Impact     →   DO NOW        SCHEDULE SOON
Low Impact      →   SCHEDULE      CONSIDER CLOSING
```

### Step 5: Execute Decision

#### Address Now
```typescript
// Add to current cycle
mcp__linear-server__update_issue({
  id: "debt-issue-uuid",
  cycle: "current",
  state: "In Progress"
});

// Create plan if complex
// Use /create-linear-plan for structured approach
```

#### Schedule for Later
```typescript
mcp__linear-server__update_issue({
  id: "debt-issue-uuid",
  cycle: "Q2 2024",  // Or specific cycle
  state: "Backlog"
});

mcp__linear-server__create_comment({
  issueId: "debt-issue-uuid",
  body: "## Scheduled\n\nScheduled for [cycle] because:\n- [reasoning]\n\nWill address after [dependency/milestone]."
});
```

#### Close
```typescript
mcp__linear-server__create_comment({
  issueId: "debt-issue-uuid",
  body: "## Closing: [Reason]\n\n[Detailed explanation]\n\n**Decision:** Won't address because [cost/benefit analysis]"
});

mcp__linear-server__update_issue({
  id: "debt-issue-uuid",
  state: "Canceled"
});
```

### Step 5: Report Summary

```markdown
## Tech Debt Triage Complete

| Issue | Decision | Action |
|-------|----------|--------|
| PEA-100 | Address Now | Added to current cycle |
| PEA-101 | Schedule | Moved to Q2 2024 |
| PEA-102 | Close | Obsolete - feature removed |

**Stats:**
- Reviewed: 5
- Addressing: 1
- Scheduled: 2
- Closed: 2

**Next review:** [Suggested date]
```

---

## Tech Debt Categories

Use these to categorize and prioritize:

| Category | Examples | Typical Priority |
|----------|----------|------------------|
| **Security** | Outdated deps, weak validation | High |
| **Performance** | N+1 queries, missing indexes | Medium-High |
| **Maintainability** | Duplicated code, poor naming | Medium |
| **Testing** | Missing tests, flaky tests | Medium |
| **Documentation** | Outdated docs, missing docs | Low-Medium |
| **Cosmetic** | Code style, formatting | Low |

---

## Quick Reference

```
FILTER:  state: "Todo" only (unstarted items)
ORDER:   Urgent → High → Normal → Low → No Priority
PROCESS: List (by priority) → Assess → Decide → Execute → Report
OUTPUT:  Scheduling decisions (now, later, never)
ALWAYS:  ONE ITEM AT A TIME → resolve (PR/schedule/close) → next item. Work highest priority first

MATRIX:
- High Impact + Low Effort = DO NOW
- High Impact + High Effort = SCHEDULE SOON
- Low Impact + Low Effort = SCHEDULE
- Low Impact + High Effort = CONSIDER CLOSING

TOOLS:
- mcp__linear-server__list_issues
- mcp__linear-server__update_issue (cycle, state)
- mcp__linear-server__create_comment
```

## Red Flags - STOP

- **Starting second item before first is resolved** → STOP, finish first item
- Addressing debt without assessing impact → STOP, assess first
- Closing without explanation → STOP, document reasoning
- All debt scheduled "later" indefinitely → STOP, some must be addressed

---

## Integration

**Uses:**
- **Linear MCP** - Issue operations
- **create-linear-plan** - For complex debt requiring structured approach

**Pairs with:**
- **linear-cycle-planning** - When scheduling for future cycles
- **linear-backlog-grooming** - Part of backlog health
