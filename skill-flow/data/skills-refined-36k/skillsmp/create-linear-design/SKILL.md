---
name: create-linear-design
description: "Create a Linear Document with technical design using Approach Mode brainstorming. Same process as /brainstorm how, outputs to Linear Document. Triggers - linear design, design to linear, technical design, architecture decision."
---

# Create Linear Design

**Iron Law:** Same process as `/brainstorm how...`, different output target. Approach Mode → Linear Document.

## Overview

This skill runs the **brainstorm** skill in **Approach Mode** and outputs the result to a **Linear Document** attached to a project.

```
/brainstorm how...        → brainstorm (Approach) → decision record (file)
/create-linear-design     → brainstorm (Approach) → Linear Document (project)
```

**Both use the same process. Only the output differs.**

## When to Use

- After `/create-linear-spec` when you need to decide HOW to build
- When making architecture or technology decisions
- When evaluating multiple implementation approaches
- Before `/create-linear-plan` to document technical choices

---

## The Workflow

### Step 1: Run Approach Mode (Brainstorming Skill)

**This is identical to `/brainstorm how...`:**

```
1. DIVERGE   → Generate options (minimum 3)
2. CAPTURE   → Document ALL ideas without judgment
3. EVALUATE  → Apply criteria to each option
4. DECIDE    → Choose with explicit reasoning
5. DOCUMENT  → Record decision and alternatives
```

### Step 2: Diverge - Generate Options

**Minimum 3 options. Aim for 5-7.**

Techniques:
- **Inversion**: What's the opposite approach?
- **Extreme**: What if unlimited resources? Zero resources?
- **Steal**: How do others solve this?
- **Combine**: Can we merge two partial solutions?
- **Simplify**: What's the minimum viable approach?

```markdown
## Options Generated

### Option 1: [Name]
[Brief description - one paragraph max]

### Option 2: [Name]
[Brief description]

### Option 3: [Name]
[Brief description]
```

**Do NOT evaluate during this step.**

### Step 3: Capture - Document Without Judgment

```markdown
## Raw Ideas (Unfiltered)
1. [Idea] - even if seems impractical
2. [Idea] - even if already rejected mentally
3. [Idea] - even if unconventional
```

**Rules:**
- No criticism during capture
- No "but that won't work because..."
- Quantity is the goal

### Step 4: Evaluate - Apply Criteria

Define criteria BEFORE scoring:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Complexity | High | Implementation effort |
| Maintainability | High | Long-term burden |
| Performance | Medium | Runtime efficiency |
| Time | Medium | Calendar time |
| Risk | High | Unknowns |

**Score each option:**

```markdown
## Evaluation Matrix

| Option | Complexity | Maintainability | Performance | Time | Risk | Total |
|--------|------------|-----------------|-------------|------|------|-------|
| Option 1 | 3/5 | 4/5 | 5/5 | 2/5 | 4/5 | 18/25 |
| Option 2 | 5/5 | 3/5 | 3/5 | 5/5 | 3/5 | 19/25 |
| Option 3 | 4/5 | 5/5 | 4/5 | 3/5 | 5/5 | 21/25 |
```

### Step 5: Decide - Choose with Explicit Reasoning

```markdown
## Decision

**Selected**: Option 3 - [Name]

**Reasoning**:
- [Why this option wins]
- [Alignment with constraints]

**Why NOT Option 1**: [explicit reason]
**Why NOT Option 2**: [explicit reason]
```

### Step 6: Validate Before Creating

Show the user the complete design for approval:

```markdown
## Proposed Linear Document

**Title:** Technical Design: [Feature Name]
**Project:** [Project Name]

**Content:** (Full design below)

---
[Full design content]
---

Create this Linear Document? I can adjust before creating.
```

### Step 7: Select Project & Create Document

List available projects:
```typescript
mcp__linear-server__list_projects({ state: "started", limit: 50 })
```

Once approved, use Linear MCP:

```typescript
mcp__linear-server__create_document({
  title: "Technical Design: [Feature Name]",
  content: `[Full design content in Markdown]`,
  project: "[Project ID or Name]",
  icon: ":page_facing_up:"
});
```

### Step 8: Confirm Creation

```markdown
## Linear Design Created

**Document:** Technical Design: [Feature Name]
**Project:** [Project Name]
**URL:** https://linear.app/[workspace]/document/[slug]

**Next Steps:**
- Create implementation plan: `/plan [feature]`
- Sync plan to Linear: `/create-linear-plan`
```

---

## Document Template

The design should be formatted as Markdown:

```markdown
# Technical Design: [Feature Name]

**Status**: Draft | Approved
**Created**: [Date]
**Decision**: [One-line summary of chosen approach]

## Context

[What problem we're solving and constraints]

## Options Considered

### Option 1: [Name]
[Description]
- Pros: [list]
- Cons: [list]

### Option 2: [Name]
[Description]
- Pros: [list]
- Cons: [list]

### Option 3: [Name]
[Description]
- Pros: [list]
- Cons: [list]

## Evaluation

| Criterion | Option 1 | Option 2 | Option 3 |
|-----------|----------|----------|----------|
| Complexity | 3/5 | 5/5 | 4/5 |
| Maintainability | 4/5 | 3/5 | 5/5 |
| Performance | 5/5 | 3/5 | 4/5 |
| Risk | 4/5 | 3/5 | 5/5 |
| **Total** | 16/20 | 14/20 | **18/20** |

## Decision

**Selected**: Option 3 - [Name]

**Reasoning**:
- [Why this option wins]
- [Trade-offs accepted]

**Why NOT Option 1**: [reason]
**Why NOT Option 2**: [reason]

## Architecture

[High-level technical description of chosen approach]

## Consequences

- [Trade-off 1 we're accepting]
- [Trade-off 2 we're accepting]

## Review Date

[When to revisit this decision]

---
*Generated via /create-linear-design*
```

---

## Example

**User says:** `/create-linear-design notifications`

**Steps 1-5 - Approach Mode:**

```
Context: Need to implement real-time notifications

Options Generated:
1. WebSocket - Full duplex, complex
2. Server-Sent Events (SSE) - Simple, one-way
3. Polling - Simplest, wasteful
4. Push Notifications - Mobile-focused

Evaluation:
| Option | Complexity | Maintainability | Real-time | Total |
|--------|------------|-----------------|-----------|-------|
| WebSocket | 2/5 | 3/5 | 5/5 | 10/15 |
| SSE | 4/5 | 5/5 | 4/5 | 13/15 |
| Polling | 5/5 | 4/5 | 2/5 | 11/15 |

Decision: SSE
- Simpler than WebSocket
- Native browser support
- Good enough for notifications (one-way)
```

**Step 6 - Validate:**

```markdown
## Proposed Linear Document

**Title:** Technical Design: Notifications
**Project:** User Notifications

**Content:**
[Full design with options, evaluation, decision]

Create this Linear Document?
```

**Step 7 - Create:**

```typescript
mcp__linear-server__create_document({
  title: "Technical Design: Notifications",
  content: "[Full design content]",
  project: "user-notifications-uuid",
  icon: ":page_facing_up:"
})
```

**Step 8 - Confirm:**

```
## Linear Design Created

**Document:** Technical Design: Notifications
**Project:** User Notifications
**URL:** https://linear.app/pea/document/technical-design-notifications

Next: `/plan notifications` → `/create-linear-plan`
```

---

## Quick Reference

```
PROCESS: Same as /brainstorm how... (Approach Mode)
OUTPUT:  Linear Document (attached to project)
TOOLS:   mcp__linear-server__create_document

1. DIVERGE   → Generate 3+ options
2. CAPTURE   → Document all ideas
3. EVALUATE  → Score with criteria
4. DECIDE    → Choose with reasoning
5. VALIDATE  → User approval
6. SELECT    → Choose project
7. CREATE    → Linear Document
8. CONFIRM   → Return URL

MINIMUM: 3 options considered
ALWAYS:  Document reasoning for decision
NEVER:   Skip to implementation without evaluating options
```

## Red Flags - STOP

- Fewer than 3 options considered
- No evaluation criteria defined
- Implementing first idea without alternatives
- No documented reasoning for decision
- Creating without user validation

---

## Integration

**Uses:**
- **brainstorm** skill (Approach Mode) - Same process
- **Linear MCP** - Output target

**Mirrors:**
- `/brainstorm how...` - Same process, different output (file vs Linear)

**Pairs with:**
- `/create-linear-spec` - Creates project (spec) first
- `/create-linear-plan` - Creates issues after design

## Full Workflow

```
/spec [feature]           → WHAT/WHY (requirements)
    ↓
/create-linear-spec       → Linear Project (spec in description)
    ↓
/brainstorm how...        → HOW (technical decisions)
    ↓
/create-linear-design     → Linear Document (design in project) ← YOU ARE HERE
    ↓
/plan [feature]           → Implementation steps
    ↓
/create-linear-plan       → Linear Issues (phases + tasks)
    ↓
/execute                  → Build it!
```
