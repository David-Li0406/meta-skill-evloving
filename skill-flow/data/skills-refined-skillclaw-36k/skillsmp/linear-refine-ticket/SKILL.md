---
name: linear-refine-ticket
description: "Refine Linear tickets tagged \"refine\" or in triage. Pull GitHub context, clarify scope, add acceptance criteria, improve descriptions. Triggers - refine ticket, ticket refinement, triage, improve ticket."
---

# Linear Refine Ticket

**Iron Law:** A refined ticket is ACTIONABLE. Clear scope, acceptance criteria, and all context included.

## Overview

This skill refines Linear tickets that need improvement:
- Tickets tagged "refine"
- Tickets in "triage" state
- Tickets referencing GitHub issues (need context pulled in)
- Tickets with unclear scope or missing information

## What Makes a Ticket Refined

| Element | Before Refinement | After Refinement |
|---------|-------------------|------------------|
| Title | "Fix the bug" | "Fix: Login fails with special chars in password" |
| Description | "It's broken" | Clear problem statement with context |
| Acceptance Criteria | Missing | Checklist of "done" conditions |
| Scope | Vague | Explicit in/out of scope |
| Context | Missing | GitHub links, related issues, dependencies |
| Estimate | None | Story points or T-shirt size |

---

## The Workflow

### Step 1: Get Tickets to Refine

```typescript
// Get tickets tagged "refine"
mcp__linear-server__list_issues({
  label: "refine",
  limit: 20
});

// Or get triage items
mcp__linear-server__list_issues({
  state: "Triage",
  team: "team-name",
  limit: 20
});
```

### Step 2: Assess Current State

For each ticket, check what's missing:

```markdown
## Refinement Checklist: [ISSUE-ID]

**Current State:**
- [ ] Clear title (action + object)
- [ ] Problem statement
- [ ] Acceptance criteria
- [ ] Scope defined (in/out)
- [ ] Context/background
- [ ] Dependencies identified
- [ ] Estimate provided
- [ ] Labels appropriate
- [ ] Assignee (if known)

**External References:**
- [ ] GitHub issue linked? → Pull context
- [ ] Related Linear issues? → Link them
- [ ] Documentation needed? → Link or note
```

### Step 3: Pull GitHub Context (if applicable)

If ticket references a GitHub issue:

```typescript
// Use gh CLI to get GitHub issue details
// Then add context to Linear issue

mcp__linear-server__create_comment({
  issueId: "linear-issue-uuid",
  body: `## GitHub Context

**From:** [repo]#[number]
**Title:** [GitHub issue title]
**Status:** [open/closed]

**Description:**
[Summarized GitHub issue content]

**Key Comments:**
- [Important comment 1]
- [Important comment 2]

**Labels:** [GitHub labels]
`
});
```

### Step 4: Improve Title

Transform vague titles into actionable ones:

| Pattern | Bad | Good |
|---------|-----|------|
| Bug | "Bug in login" | "Fix: Login fails with special characters" |
| Feature | "Add export" | "Feat: Export dashboard data to CSV" |
| Task | "Update docs" | "Docs: Add API authentication guide" |
| Chore | "Dependencies" | "Chore: Upgrade React to v18" |

### Step 5: Write Clear Description

Use this template:

```markdown
## Problem
[What's wrong or what's needed - 1-2 sentences]

## Context
[Background information, why this matters]

## Proposed Solution
[High-level approach if known, or "TBD during implementation"]

## Acceptance Criteria
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

## Scope
**In Scope:**
- [What's included]

**Out of Scope:**
- [What's explicitly excluded]

## Dependencies
- [Blocking issues or external dependencies]

## References
- [Links to related issues, docs, designs]
```

### Step 6: Add Acceptance Criteria

Good acceptance criteria are:
- **Specific** - No ambiguity
- **Testable** - Can verify pass/fail
- **Independent** - Each stands alone

```markdown
## Acceptance Criteria

### Functional
- [ ] User can login with passwords containing !@#$%^&*
- [ ] Error message shows specific validation failure
- [ ] Successful login redirects to dashboard

### Technical
- [ ] Unit tests cover special character cases
- [ ] No regression in existing login tests

### Documentation
- [ ] Password requirements updated in user docs
```

### Step 7: Define Scope

Be explicit about boundaries:

```markdown
## Scope

**In Scope:**
- Fix password validation for special characters
- Update error messages
- Add test coverage

**Out of Scope:**
- Password strength requirements (separate ticket)
- UI redesign of login form
- OAuth integration
```

### Step 8: Update the Ticket

```typescript
mcp__linear-server__update_issue({
  id: "issue-uuid",
  title: "[Refined title]",
  description: "[Full refined description]",
  state: "Backlog",  // Move out of triage
  labels: ["refined"]  // Remove "refine", add "refined"
});

// Remove refine label, add refined
// (May need to manage labels appropriately)
```

### Step 9: Report Refinement

```markdown
## Ticket Refined: [ISSUE-ID]

**Before:**
- Title: "Fix the bug"
- Description: "It's broken"
- Acceptance Criteria: None
- Scope: Unclear

**After:**
- Title: "Fix: Login fails with special characters in password"
- Description: Full problem statement with context
- Acceptance Criteria: 5 specific items
- Scope: Clearly defined in/out

**Status:** Moved to Backlog, ready for planning

**Next ticket?**
```

---

## Refinement Patterns

### Bug Tickets
```markdown
## Problem
[What's broken - expected vs actual]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Observe: actual behavior]

## Expected Behavior
[What should happen]

## Environment
- Browser/OS: [details]
- User type: [role/permissions]

## Acceptance Criteria
- [ ] Bug no longer reproduces
- [ ] Regression test added
- [ ] No new bugs introduced
```

### Feature Tickets
```markdown
## User Story
As a [user type], I want [goal] so that [benefit].

## Context
[Why this feature, business value]

## Proposed Solution
[High-level approach]

## Acceptance Criteria
- [ ] [Functional requirement]
- [ ] [Functional requirement]
- [ ] Documentation updated

## Scope
[In/out of scope]

## Design
[Link to designs or "No design needed"]
```

### Technical/Chore Tickets
```markdown
## Objective
[What we're doing and why]

## Approach
[Technical approach]

## Acceptance Criteria
- [ ] [Technical requirement]
- [ ] Tests pass
- [ ] No performance regression

## Rollback Plan
[How to revert if needed]
```

---

## Quick Reference

```
PROCESS: List → Assess → Pull Context → Improve → Update → Report
OUTPUT:  Refined tickets ready for planning

REFINED TICKET HAS:
- Clear actionable title
- Problem statement
- Acceptance criteria (testable)
- Scope (in/out)
- Context and references
- Appropriate labels

TOOLS:
- mcp__linear-server__list_issues
- mcp__linear-server__get_issue
- mcp__linear-server__update_issue
- mcp__linear-server__create_comment
- gh (for GitHub context)
```

## Red Flags - STOP

- No acceptance criteria → STOP, add them
- "TBD" in scope → STOP, define scope
- Vague title remains → STOP, make it actionable
- Missing context for external refs → STOP, pull it in

---

## Integration

**Uses:**
- **Linear MCP** - Issue operations
- **GitHub CLI** - Pull GitHub issue context

**Pairs with:**
- **linear-backlog-grooming** - Refine during grooming
- **linear-cycle-planning** - Refined tickets ready for planning

## Labels Convention

```
refine    → Needs refinement (input)
refined   → Ready for planning (output)
needs-info → Waiting on external input
```
