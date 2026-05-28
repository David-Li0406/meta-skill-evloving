---
title: "ADR-[NUMBER]: [Decision Title]"
description: "[Brief description of the architectural decision in 1-2 sentences]"
type: adr
category: architecture
status: accepted
tags:
  - architecture
  - adr
  - [technology/domain]
created: YYYY-MM-DD
lastUpdated: YYYY-MM-DD
---


**Status**: [Proposed | Accepted | Deprecated | Superseded]

**Date**: YYYY-MM-DD

**Deciders**: [List of people involved in the decision]

**Technical Story**: [[Link to issue/ticket]](https://example.com/issue/123) _(optional)_

## Context

[Describe the context and problem statement. What forces are at play? What are the constraints?]

**Background**:

- [Relevant background information]
- [Current situation]
- [Why this decision is needed]

**Business drivers**:

- [Business requirement 1]
- [Business requirement 2]
- [Business requirement 3]

**Technical constraints**:

- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

## Decision

[Describe the decision in clear, explicit language. What is being decided?]

**We will**: [Brief statement of the decision]

**Specifically**:

- [Specific aspect 1 of the decision]
- [Specific aspect 2 of the decision]
- [Specific aspect 3 of the decision]

## Rationale

[Explain why this decision was chosen over alternatives]

**Key factors**:

1. **[Factor 1]** - [Why this matters]
2. **[Factor 2]** - [Why this matters]
3. **[Factor 3]** - [Why this matters]

**How this addresses the problem**:

- [Explanation of how decision solves the context/problem]
- [Benefits this decision provides]

## Alternatives Considered

### Alternative 1: [Name]

**Description**: [What this alternative would involve]

**Pros**:

- [Advantage 1]
- [Advantage 2]
- [Advantage 3]

**Cons**:

- [Disadvantage 1]
- [Disadvantage 2]
- [Disadvantage 3]

**Why not chosen**: [Specific reason this was rejected]

### Alternative 2: [Name]

**Description**: [What this alternative would involve]

**Pros**:

- [Advantage 1]
- [Advantage 2]

**Cons**:

- [Disadvantage 1]
- [Disadvantage 2]

**Why not chosen**: [Specific reason this was rejected]

### Alternative 3: Do Nothing

**Description**: Keep the current approach

**Pros**:

- No implementation cost
- No migration risk
- Team already familiar

**Cons**:

- [Problem continues]
- [Technical debt accumulates]
- [Missed opportunity]

**Why not chosen**: [Why status quo is unacceptable]

## Consequences

### Positive Consequences

**Immediate benefits**:

- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**Long-term benefits**:

- [Benefit 1]
- [Benefit 2]

### Negative Consequences

**Immediate costs**:

- [Cost/drawback 1]
- [Cost/drawback 2]
- [Cost/drawback 3]

**Long-term costs**:

- [Cost/drawback 1]
- [Cost/drawback 2]

### Risks

**Technical risks**:

- **[Risk 1]** - [Description and mitigation]
- **[Risk 2]** - [Description and mitigation]

**Business risks**:

- **[Risk 1]** - [Description and mitigation]
- **[Risk 2]** - [Description and mitigation]

## Implementation

**Timeline**: [Expected implementation timeframe]

**Phases**:

1. **Phase 1**: [First step]
   - **Duration**: [Timeframe]
   - **Owner**: [Person/team]
   - **Deliverable**: [What will be completed]

2. **Phase 2**: [Second step]
   - **Duration**: [Timeframe]
   - **Owner**: [Person/team]
   - **Deliverable**: [What will be completed]

3. **Phase 3**: [Final step]
   - **Duration**: [Timeframe]
   - **Owner**: [Person/team]
   - **Deliverable**: [What will be completed]

**Resource requirements**:

- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Dependencies**:

- [Dependency 1]
- [Dependency 2]

## Validation

**Success criteria**:

- ✅ [Measurable criterion 1]
- ✅ [Measurable criterion 2]
- ✅ [Measurable criterion 3]

**Metrics to track**:

- [Metric 1]: Target [X], Current [Y]
- [Metric 2]: Target [X], Current [Y]
- [Metric 3]: Target [X], Current [Y]

**Review date**: YYYY-MM-DD - [When to review if decision was correct]

## Related Decisions

- [[ADR-XXX]](/docs/adr/adr-xxx) - [Related decision that this builds on]
- [[ADR-YYY]](/docs/adr/adr-yyy) - [Related decision in same area]
- [[ADR-ZZZ]](/docs/adr/adr-zzz) - [Decision this supersedes] _(if applicable)_

## References

- [[Technical Spec]](/docs/specs/[spec]) - Detailed technical specification
- [[Design Document]](/docs/design/[doc]) - Related design document
- [External Resource] - Relevant article/documentation
- [RFC/Standard] - Industry standard reference

## Notes

**Discussion highlights**:

- [Key point from discussion 1]
- [Key point from discussion 2]
- [Dissenting opinion that was considered]

**Assumptions**:

- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

**Future considerations**:

- [What might change this decision in the future]
- [When to revisit this decision]

---

## Change History

| Date | Author | Change | Reason |
|------|--------|--------|--------|
| YYYY-MM-DD | [Name] | Status: Proposed → Accepted | Initial approval |
| YYYY-MM-DD | [Name] | [Description] | [Reason] |

---

## Status Definitions

- **Proposed** - Decision is under discussion
- **Accepted** - Decision has been approved and will be implemented
- **Deprecated** - Decision is no longer recommended but not removed
- **Superseded** - Decision has been replaced (link to replacement ADR)

## ADR Numbering

ADRs are numbered sequentially:

- ADR-001, ADR-002, etc.
- Once assigned, numbers are never reused
- Gaps in numbering are acceptable

## File Naming Convention

Use the format: `adr-[NUMBER]-[short-title].md`

**Examples**:

- `adr-001-use-postgresql.md`
- `adr-015-migrate-to-microservices.md`
- `adr-042-adopt-graphql-api.md`
