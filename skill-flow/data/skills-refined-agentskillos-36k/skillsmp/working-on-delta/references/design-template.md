# Feature Design Template

Use this template when creating feature design documents.

## Template

```markdown
# Design: [FEATURE-ID] - [Feature Name]

**Feature Spec**: [../feature-specs/FEATURE-ID.md](../feature-specs/FEATURE-ID.md)
**Status**: Draft | Approved | Superseded

## Retrofit Note (if applicable)

This design was created from existing code at:
- `src/path/to/file.py`
- `src/path/to/other.py`

Original implementation date: [date or "Unknown (pre-framework)"]
Decisions documented during retrofit: [ADR-NNN, DES-NNN]

---

## Purpose

This document explains the design rationale for this feature: the modeling choices, data flow, system behavior, and architectural approach.

## Problem Context

[What specific problem does this feature solve? What constraints exist? What interactions with other features/systems?]

## Design Overview

[High-level description of the design approach. What are the main components/concepts?]

## Modeling

[How is the domain modeled? What are the key entities/concepts? What relationships exist?]

Example:
```
User
├─ has many Sessions
└─ has many Snippets

Session
└─ belongs to User

Snippet
├─ belongs to User
└─ has content (text)
```

## Data Flow

[How does data move through the system? What are the key paths?]

Example:
```
1. User triggers action
2. System reads from storage
3. UI displays result
4. User makes selection
5. System updates state
```

## Key Decisions

### [Decision Name]

**Choice**: [What was chosen]
**Why**: [Rationale for this choice]
**Alternatives Considered**:
- [Alternative 1]: [Why not chosen]
- [Alternative 2]: [Why not chosen]

**Consequences**:
- Pro: [benefit]
- Con: [tradeoff]

## System Behavior

[How does the system behave in important scenarios? Edge cases?]

### Scenario: [Name]

**Given**: [context]
**When**: [trigger]
**Then**: [expected behavior]
**Rationale**: [why this behavior]

## Open Questions

- [ ] [Question that needs resolution]

## Notes

[Any additional context, links to research, related decisions]
```

## Guidelines

### Problem Context

Describe:
- The problem this feature solves
- Constraints (performance, security, compatibility)
- Interactions with other features
- Scope boundaries (what's NOT included)

### Design Overview

Provide a mental model:
- Main components and their responsibilities
- How they fit together
- The "elevator pitch" of the design

### Modeling

Show domain structure:
- Use ASCII diagrams for clarity
- Show entities and relationships
- Include state machines if applicable
- Match the spec's domain language

### Data Flow

Trace data through the system:
- Entry points (user input, API calls, events)
- Processing steps
- Output (UI updates, side effects, storage)
- Error paths

### Key Decisions

For each significant choice:
- State what was chosen clearly
- Explain why (not just "it's better")
- List alternatives considered
- Note consequences (both positive and negative)

Decisions should reference ADRs/DES if applicable:
"Per ADR-007, we use X for logging"

### System Behavior

Cover scenarios from the spec's acceptance criteria:
- How does each scenario work?
- What's the rationale for the behavior?
- Include edge cases

### When to Promote to DES

If a pattern emerges that could apply to other features:
- Similar modeling structure
- Reusable data flow pattern
- Decision that establishes a convention

Suggest promoting to a DES pattern document.
