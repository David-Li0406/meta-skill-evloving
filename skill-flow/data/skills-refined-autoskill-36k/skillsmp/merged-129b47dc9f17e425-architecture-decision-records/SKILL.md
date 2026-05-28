---
name: architecture-decision-records
description: Use this skill to create and manage Architecture Decision Records (ADRs) for significant architectural decisions, documenting context, alternatives, and consequences. Ideal for decisions with long-term impact requiring structured analysis.
---

# Architecture Decision Records (ADR)

Architecture Decision Records (ADRs) are documents that capture important architectural decisions made along with their context, rationale, and consequences. They serve as a historical record to help future developers understand why certain choices were made.

## When to Use This Skill

Trigger this skill when:
- Making significant architectural decisions
- Choosing between competing technologies or approaches
- Designing new system components or APIs
- Refactoring that changes system structure
- Formally evaluating multiple alternatives with pros and cons

## Auto-Invoke Triggers

This skill automatically activates when:
1. **Keywords**: "ADR", "architecture decision", "document this decision", "create ADR"
2. **Editing ADR files**: Files in `docs/adr/`, `doc/adr/`, `architecture/decisions/`, `.adr/`
3. **Discussing architectural choices**: Framework selection, technology decisions, pattern choices

## What This Skill Delivers

### 1. ADR Creation
- Auto-detect project's ADR directory
- Auto-number ADRs (scan existing, increment)
- Adapt to project's existing template style
- Offer enhancements as optional additions

### 2. Directory Discovery
Search order for ADR directories:
1. `docs/adr/`
2. `doc/adr/`
3. `architecture/decisions/`
4. `.adr/`
5. Create `docs/adr/` if none exists

### 3. Template Detection
Analyze existing ADRs to detect:
- Naming convention: `NNNN-kebab-case-title.md` or `NNN-title.md`
- Section structure: Status, Context, Decision, Consequences
- Optional sections: Decision Drivers, Pros/Cons, Confirmation

### 4. Index Maintenance
Automatically update README.md with ADR table:
| Number | Title | Status | Date |
|--------|-------|--------|------|

### 5. Supersession Workflow
When replacing an ADR:
- Mark old ADR status as "Superseded by [ADR-NNNN]"
- Link new ADR with "Supersedes [ADR-NNNN]"
- Update README.md index

## Core Template Sections

### Required (Minimal)
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Date**: ISO 8601 format (YYYY-MM-DD)
- **Context and Problem Statement**: 2-3 sentences describing the situation
- **Decision**: What was decided and why
- **Consequences**: Positive and negative impacts

### Optional Enhancements
- **Technical Story**: Link to issue/spec (e.g., `#123`)
- **Decision Drivers**: Bulleted list of forces/concerns
- **Decision Makers**: Who made this decision
- **Consulted**: Stakeholders whose opinions were sought
- **Informed**: Stakeholders who need to know
- **Considered Options**: List of alternatives evaluated
- **Pros and Cons**: Detailed analysis per option
- **Confirmation**: How to validate the decision was implemented

## Quick Start

### Create New ADR
```bash
# Auto-invoke by saying:
"Document the decision to use PostgreSQL over MongoDB"
"Create an ADR for our authentication approach"
"I need to record why we chose React Query"
```

### Supersede Existing ADR
```bash
"Supersede ADR-0005 with a new caching strategy"
"Replace our database decision ADR with the new approach"
```

## Example ADR Structure

```markdown
# ADR-NNN: [Title]

Date: YYYY-MM-DD
Status: Proposed
Actor: human:<id>

## Context
[What issue motivated this decision?]

## Decision
[What change are we making?]

## Alternatives Considered
[Each alternative with pros/cons]

## Consequences
[What becomes easier or harder?]

## Rationale
[Why is this the right choice?]
```

## ADR Lifecycle

| Status | Meaning |
|--------|---------|
| **Proposed** | Initial state; under consideration |
| **Accepted** | Approved and in effect |
| **Deprecated** | No longer recommended; kept for history |
| **Superseded** | Replaced by another ADR (note which one) |

To change status, edit the ADR file directly. The decision log entry is immutable (captures the moment of decision).

## Best Practices

- Write ADRs when decisions are made, not after.
- Focus on "why" not just "what".
- Document trade-offs honestly.
- Include alternatives considered.
- Keep ADRs immutable; create new ones for changes.

## Common Anti-Patterns

- Writing ADRs after implementation.
- Overly technical ADRs without context.
- No alternatives documented.
- Vague consequences.

## Integration with Other Skills

ADRs complement other documentation and can be linked to code reviews, architecture reviews, and technical writing to ensure a comprehensive understanding of architectural decisions.