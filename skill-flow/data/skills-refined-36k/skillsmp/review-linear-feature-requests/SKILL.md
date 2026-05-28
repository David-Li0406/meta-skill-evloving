---
name: review-linear-feature-requests
description: "Review Linear issues tagged with \"feature-request\". Decide to spec, add to roadmap, merge, or reject. Triggers - review feature request, user request, customer feedback."
---

# Review Linear Feature Requests

**Iron Law:** Feature requests produce ROADMAP DECISIONS. Spec it, roadmap it, merge it, or reject it.

## Overview

This skill handles Linear issues tagged with "feature-request". Every request must be:
1. Turned into a spec (if approved and complex)
2. Added to roadmap (if approved and clear)
3. Merged with existing (if duplicate/similar)
4. Rejected with explanation (if not aligned)

## Valid Outcomes

| Outcome | When to Use | Action |
|---------|-------------|--------|
| **Create Spec** | Approved, needs discovery | `/create-linear-spec` |
| **Add to Roadmap** | Approved, scope clear | Add to project/initiative |
| **Merge** | Similar to existing request | Link and close |
| **Reject** | Not aligned with product direction | Explain and close |
| **Needs Info** | Unclear request | Ask clarifying questions |

---

## The Workflow

### Step 1: List Feature Requests

```typescript
mcp__linear-server__list_issues({
  label: "feature-request",
  state: "triage",  // Or "backlog"
  limit: 20
});
```

### Step 2: Analyze Request

For each request, understand:

```markdown
## Feature Request Analysis: [ID]

**Request:** [What the user/customer wants]
**Requester:** [Who asked - internal, customer tier, user segment]
**Use Case:** [Why they need it]

**Alignment Check:**
- Fits product vision: Yes/No/Partially
- Target user segment: Yes/No
- Technical feasibility: Easy/Medium/Hard/Unknown

**Demand Signals:**
- Number of requests: [count]
- Customer tier: [Free/Pro/Enterprise]
- Revenue impact: [estimate if known]

**Similar Existing:**
- [List any related issues or features]
```

### Step 3: Explore Codebase (For Feasibility)

**When technical feasibility is unclear, explore the codebase:**

```typescript
// Dispatch Explore agent for feasibility assessment
Task({
  subagent_type: "Explore",
  prompt: `
    Assess feasibility for feature request: "[request title]"

    Find:
    1. Related existing functionality
    2. Patterns that could be extended
    3. Technical constraints or blockers
    4. Estimated implementation effort

    Return findings to inform roadmap decision.
  `,
  description: "Explore codebase for feature feasibility"
});
```

**Present findings:**

```markdown
## Feasibility Analysis

### Related Existing Code
- `src/features/similar.ts` - Could extend this pattern
- `src/api/endpoints.ts` - Would need new endpoint

### Technical Assessment
- **Feasibility:** Easy / Medium / Hard
- **Effort:** 1-2 days / 1 week / 2+ weeks
- **Dependencies:** [any blocking work]

### Recommendation
[Add to roadmap / Create spec for further discovery / Reject as infeasible]
```

### Step 4: Decision Framework

```
Does it align with product vision?
├── NO → Reject with explanation
└── YES → Is scope clear?
          ├── NO → Create Spec (needs discovery)
          └── YES → Does similar exist?
                    ├── YES → Merge with existing
                    └── NO → Add to Roadmap
```

### Step 5: Execute Decision

#### Create Spec
```markdown
Request is approved but needs requirements discovery.
Using /create-linear-spec to explore:
- User stories
- Acceptance criteria
- Technical constraints
```

#### Add to Roadmap
```typescript
mcp__linear-server__update_issue({
  id: "request-issue-uuid",
  project: "product-roadmap-uuid",
  state: "Backlog",
  labels: ["approved", "feature-request"]
});

mcp__linear-server__create_comment({
  issueId: "request-issue-uuid",
  body: "## Approved for Roadmap\n\nAdded to [Project Name].\n\n**Priority:** [High/Medium/Low]\n**Target:** [Timeframe if known]\n\nThank you for the feedback!"
});
```

#### Merge with Existing
```typescript
mcp__linear-server__create_comment({
  issueId: "request-issue-uuid",
  body: "## Merging with Existing Request\n\nThis is similar to [ISSUE-ID]: [title]\n\nTracking in the original issue. Adding your use case to the discussion there."
});

// Add context to original issue
mcp__linear-server__create_comment({
  issueId: "original-issue-uuid",
  body: "## Additional Request\n\nFrom [REQUEST-ID]:\n- Use case: [their use case]\n- Requester: [who]"
});

mcp__linear-server__update_issue({
  id: "request-issue-uuid",
  state: "Duplicate"
});
```

#### Reject
```typescript
mcp__linear-server__create_comment({
  issueId: "request-issue-uuid",
  body: `## Decision: Not Proceeding

Thank you for the thoughtful request.

**Reason:** [Why this doesn't fit]

**Alternatives:**
- [Existing feature that might help]
- [Workaround if any]
- [Third-party integration if applicable]

We appreciate your feedback and will keep this in mind for future planning.`
});

mcp__linear-server__update_issue({
  id: "request-issue-uuid",
  state: "Canceled"
});
```

### Step 5: Report Summary

```markdown
## Feature Request Triage Complete

| Request | Decision | Action |
|---------|----------|--------|
| PEA-200 | Spec | Created "OAuth Integration" project |
| PEA-201 | Roadmap | Added to Q2 roadmap |
| PEA-202 | Merge | Combined with PEA-150 |
| PEA-203 | Reject | Not aligned with B2B focus |

**Stats:**
- Reviewed: 4
- Approved (spec): 1
- Approved (roadmap): 1
- Merged: 1
- Rejected: 1
```

---

## Rejection Templates

### Not Aligned with Vision
```
This doesn't align with our current product direction focused on [area].
We're prioritizing [what we're building] for [target users].
```

### Too Niche
```
This would benefit a small subset of users and the effort doesn't justify
the impact. We need to focus on features with broader value.
```

### Technical Constraints
```
Current architecture doesn't support this without significant rework.
We may revisit this when we [future milestone/refactor].
```

### Already Possible
```
This is already possible using [existing feature].
Here's how: [steps or link to docs]
```

---

## Quick Reference

```
PROCESS: List → Analyze → Decide → Execute → Report
OUTPUT:  Roadmap decisions (spec, roadmap, merge, reject)

DECISION TREE:
- Aligned + Unclear scope = Create Spec
- Aligned + Clear scope = Add to Roadmap
- Aligned + Duplicate = Merge
- Not aligned = Reject

TOOLS:
- mcp__linear-server__list_issues
- mcp__linear-server__update_issue
- mcp__linear-server__create_comment
- /create-linear-spec (for discovery)
```

## Red Flags - STOP

- Rejecting without explanation → STOP, always explain why
- Approving everything → STOP, be selective
- No response to requester → STOP, always acknowledge

---

## Integration

**Uses:**
- **Linear MCP** - Issue operations
- **create-linear-spec** - For approved features needing discovery

**Pairs with:**
- **linear-cycle-planning** - When scheduling approved features
- **linear-project-health** - Track approved feature progress
