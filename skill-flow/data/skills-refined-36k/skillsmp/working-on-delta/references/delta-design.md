# Design: [DLT-ID] - [Title]

<!--
NOTE: This is a DELTA design template (working document for implementing changes).
For FEATURE design templates (long-lived documentation), see feature-design.md.
For detailed design guidelines, see design-template.md.
-->

**Delta Spec**: [../delta-specs/DLT-ID.md](../delta-specs/DLT-ID.md)
**Status**: Draft | Approved | Superseded

## Purpose

This document explains the design rationale for this delta: the modeling choices, data flow, system behavior, and architectural approach.

After implementation, the "Detected Impacts" section will guide reconciliation into feature design docs.

## Problem Context

[What specific problem does this delta solve? What constraints exist?]

## Design Overview

[High-level description of the design approach. What are the main components/concepts?]

## Components

<!-- This is where implementation structure lives. Specs describe WHAT users can do; design decides HOW to implement it -->

### Implementation Structure

| Layer/Component | Responsibility | Key Decisions |
|-----------------|----------------|---------------|
| [e.g., API] | [What this layer does] | [Technology, patterns, constraints] |
| [e.g., UI] | [What this layer does] | [Framework, state management] |
| [e.g., Validation] | [Shared logic across layers] | [Where it runs, how it's shared] |

### Cross-Layer Contracts

**API Contract** (if applicable):
```
[Method] [Endpoint]
Request: { ... }
Response: { ... } | { error: ..., code: ... }
```

**Integration Points**:
- [How layers communicate]
- [Error handling strategy across layers]
- [Loading states and optimistic updates]

### Shared Logic

What's shared between components and why:
- [e.g., Validation rules]: [Rationale for sharing]
- [e.g., Error codes]: [How consistency is maintained]
- [e.g., Types/interfaces]: [Sharing mechanism - codegen, manual sync, etc.]

## Modeling

[How is the domain modeled? What are the key entities/concepts? What relationships exist?]

## Data Flow

[How does data move through the system? What are the key paths?]

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

---

## Detected Impacts

<!-- This section is populated automatically during design phase -->

### Affected Feature Designs
- **[path/to/feature-design.md]** - [Modifies/Adds/Removes]: [description]

### Notes for Reconciliation
- [What needs to change in feature design docs]
- [New design sections that need to be created]
- [Design decisions that need to be documented]

## Notes

[Any additional context, links to research, related decisions]
