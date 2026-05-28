---
name: brainstorm
description: "Use when generating ideas, exploring options, defining requirements, or making decisions. Covers both discovery (what to build) and approach (how to build). Triggers - ideate, brainstorm, options, alternatives, explore, what if, could we, ways to, approaches, spec, requirements, user story."
---

# Brainstorming

**Iron Law:** NEVER commit to requirements or approach without exploring alternatives first.

## No Code Policy

> **All output documents must be plain prose.** No code blocks, no technical snippets, no implementation details. Explain concepts in written English that any stakeholder can understand.

This applies to:
- Specs (Discovery Mode output)
- Decision records (Approach Mode output)
- All brainstorming artifacts

## Overview

Brainstorming is structured ideation with two modes:
1. **Discovery Mode** - What should we build? → Outputs a spec
2. **Approach Mode** - How should we build it? → Outputs a decision

Both use divergent thinking first (quantity), then convergent thinking (quality).

## The Spec Rule

> **A spec contains WHAT and WHY. Never HOW.**

| In Spec | NOT In Spec |
|---------|-------------|
| User stories | Code snippets |
| Acceptance criteria | Technical approach |
| Success metrics | Database schema |
| Requirements | API design |
| Constraints | Implementation details |

**If you're writing code or technical details, you've left spec territory and entered design.**

## When to Use

**Discovery Mode (Spec):**
- Starting a new feature from scratch
- Unclear requirements - need to explore use cases
- User asks "what should this feature do?"
- Before any technical discussion

**Approach Mode (Decision):**
- Requirements are clear, need to choose implementation
- Architecture or design decisions with trade-offs
- User asks "how could we..." or "what are the options for..."
- Multiple valid approaches exist

---

# Mode 1: Discovery (Spec Writing)

> **Iron Law:** Specs define WHAT and WHY. Never HOW. No code. No technical decisions.

## The Discovery Process

```
1. EXPLORE    -> What problems exist? Who has them?
2. BRAINSTORM -> What are ALL the things this could do?
3. PRIORITIZE -> What's essential vs nice-to-have?
4. SPECIFY    -> Write user stories + acceptance criteria
5. VALIDATE   -> Review with stakeholder
```

## Step 1: Explore the Problem Space

Before listing features, understand the problem:

```markdown
## Problem Exploration

**Who has this problem?**
- Primary user: [persona]
- Secondary users: [others affected]

**What's the pain today?**
- [Current workaround 1]
- [Current workaround 2]

**What triggers the need?**
- [Trigger event 1]
- [Trigger event 2]

**What does success look like?**
- [Outcome 1]
- [Outcome 2]
```

## Step 2: Brainstorm Requirements

Generate ALL possible requirements without filtering:

```markdown
## Raw Requirements (Unfiltered)

### Core Functionality
- [ ] [Requirement] - even if seems obvious
- [ ] [Requirement] - even if seems complex
- [ ] [Requirement] - even if seems edge case

### User Experience
- [ ] [UX requirement]
- [ ] [Accessibility need]

### Edge Cases
- [ ] What if [edge case]?
- [ ] What about [unusual scenario]?

### Integration
- [ ] Must work with [system]
- [ ] Must support [format]
```

**Quantity over quality at this stage.**

## Step 3: Prioritize Requirements

Apply MoSCoW prioritization:

```markdown
## Prioritized Requirements

### Must Have (P0) - Without these, feature is useless
- [ ] [Requirement 1]
- [ ] [Requirement 2]

### Should Have (P1) - Important but not critical
- [ ] [Requirement 3]
- [ ] [Requirement 4]

### Could Have (P2) - Nice to have
- [ ] [Requirement 5]

### Won't Have (This Release)
- [Requirement 6] - Reason: [why deferred]
```

## Step 4: Write the Spec

Formalize requirements into user stories:

```markdown
# Feature Spec: [Name]

**Status**: Draft | Review | Approved
**Author**: [Name]
**Created**: [Date]

## Problem Statement
[2-3 sentences on the problem being solved]

## Target Users
- **Primary**: [Who] - [Goal]
- **Secondary**: [Who] - [Goal]

## Success Metrics
| Metric | Current | Target |
|--------|---------|--------|
| [Metric] | X | Y |

---

## User Stories

### US-1: [Title]

**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]
- [ ] Edge: Given [edge case], then [behavior]

### US-2: [Title]
[Same format]

---

## Out of Scope
- [Explicitly excluded 1]
- [Explicitly excluded 2]

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

## Next Steps
1. Review spec with stakeholders
2. Brainstorm approach: `/brainstorm how to implement [feature]`
3. Create design doc
4. Create implementation plan
```

## Step 5: Validate

Before proceeding:
- [ ] All must-haves have user stories
- [ ] Each story has acceptance criteria
- [ ] Edge cases are covered
- [ ] Success metrics are measurable
- [ ] Stakeholder reviewed
- [ ] **NO code or technical details in spec**

## Spec Anti-Patterns

```markdown
# BAD - Implementation in spec
## Requirements
- Use PostgreSQL for storage
- Implement with React and Next.js
- Cache with Redis

# GOOD - Pure requirements
## Requirements
- Data must persist across sessions
- UI must load within 2 seconds
- Frequently accessed data should be fast
```

```markdown
# BAD - Code in acceptance criteria
Given the user calls POST /api/users with { email, password }
Then the bcrypt hash is stored in the users table

# GOOD - Behavior only
Given the user submits the registration form
When they provide valid email and password
Then their account is created
And they receive a confirmation email
```

```markdown
# BAD - Technical constraints as requirements
- Must use WebSocket for real-time updates
- Database must be normalized to 3NF

# GOOD - Business constraints
- Updates must appear within 1 second
- No data duplication that could cause inconsistency
```

**The test:** Could a non-technical stakeholder understand and validate this spec? If not, it contains too much "how".

---

# Mode 2: Approach (Solution Brainstorming)

## The Approach Process

```
1. DIVERGE  -> Generate options (minimum 3)
2. CAPTURE  -> Document ALL ideas without judgment
3. EVALUATE -> Apply criteria to each option
4. DECIDE   -> Choose with explicit reasoning
5. DOCUMENT -> Record decision and alternatives
```

## Step 1: Diverge - Generate Options

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

## Step 2: Capture - Document Without Judgment

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

## Step 3: Evaluate - Apply Criteria

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

## Step 4: Decide - Choose with Explicit Reasoning

```markdown
## Decision

**Selected**: Option 3 - [Name]

**Reasoning**:
- [Why this option wins]
- [Alignment with constraints]

**Why NOT Option 1**: [explicit reason]
**Why NOT Option 2**: [explicit reason]
```

## Step 5: Document - Record for Future

```markdown
## Decision Record

**Date**: [date]
**Context**: [what prompted this]
**Options Considered**: [list all]
**Decision**: [chosen option]
**Consequences**: [trade-offs accepted]
**Review Date**: [when to revisit]
```

---

# Combined Workflow

For a complete feature, use both modes:

```
/brainstorm what should [feature] do?
  ↓
[Discovery Mode → Spec output]
  ↓
/brainstorm how should we implement [feature]?
  ↓
[Approach Mode → Decision output]
  ↓
/design [feature]
  ↓
/plan [feature]
```

---

## Examples

### Discovery Mode Example

```
User: "We need user notifications"

Discovery Phase:
- Who: All authenticated users
- Pain: Miss important updates, have to refresh manually
- Triggers: New message, status change, mention

Requirements Brainstorm:
- Real-time in-app notifications
- Email fallback for away users
- Notification preferences
- Read/unread status
- Notification center
- Push notifications (mobile)
- Do not disturb mode
- Digest mode for high volume

Prioritized:
- P0: In-app real-time, read status
- P1: Email fallback, preferences
- P2: Push, digest mode

Output: Feature spec with 4 user stories
```

### Approach Mode Example

```
User: "How should we implement notifications?"

Options Generated:
1. WebSocket real-time push
2. Polling with exponential backoff
3. Server-Sent Events (SSE)
4. Push notifications via service worker
5. Email digests only (async)

Evaluation:
- Real-time needed: Yes
- Browser support: All modern
- Complexity budget: Low

Decision: SSE for in-app, email for away
Reasoning: SSE simpler than WebSocket, native support

Rejected: WebSocket (overkill), Polling (wasteful)
```

---

## Red Flags - STOP

**Discovery Mode:**
- Jumping to solutions before understanding problem
- No user stories, just feature list
- Missing acceptance criteria
- No prioritization

**Approach Mode:**
- Implementing first idea without alternatives
- Fewer than 3 options considered
- No evaluation criteria defined
- No documented reasoning

---

## Verification Checklist

### Discovery Mode
- [ ] Problem clearly understood
- [ ] At least 5 requirements brainstormed
- [ ] Prioritized (P0/P1/P2)
- [ ] User stories with acceptance criteria
- [ ] Edge cases covered
- [ ] Success metrics defined

### Approach Mode
- [ ] At least 3 options generated
- [ ] Evaluation criteria defined
- [ ] Each option scored
- [ ] Decision documented with reasoning
- [ ] Rejected alternatives explained
- [ ] Trade-offs acknowledged

---

## Quick Reference

```
DISCOVERY: Problem → Requirements → Prioritize → Spec
APPROACH:  Options → Evaluate → Decide → Record

MINIMUM: 3 options (approach), 5 requirements (discovery)
ALWAYS:  Document reasoning
NEVER:   Skip to implementation
```

## Integration

**Outputs to:**
- **writing-design** - Technical architecture
- **plan** - Implementation steps
- **execute** - Execute the plan

**Triggers:** brainstorm, ideate, options, alternatives, explore, spec, requirements, user story, what should, how could
