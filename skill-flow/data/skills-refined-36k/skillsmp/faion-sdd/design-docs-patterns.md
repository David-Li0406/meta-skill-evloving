---
id: design-docs-patterns
name: "Design Docs Patterns (Big Tech)"
domain: SDD
skill: faion-sdd
category: "best-practices-2026"
---

# Design Docs Patterns (Big Tech)

### Problem

Design docs written without structure lead to:
- Inconsistent quality across teams
- Missing critical considerations
- Difficult cross-team review
- No clear approval process

### Framework

#### Design Doc Purpose

"Our job is not to produce code per se, but rather to solve problems. Unstructured text may be the better tool for solving problems early when changes are still cheap."

#### Design Doc Functions

1. **Early issue identification** - Catch design issues when changes are cheap
2. **Consensus building** - Achieve agreement across organization
3. **Knowledge sharing** - Document decisions for future team members
4. **Onboarding** - Help new engineers understand system

#### Company Approaches

| Company | Name | Key Features |
|---------|------|--------------|
| **Google** | Design Doc | Informal, collaborative, focuses on "why" |
| **Uber** | ERD (Engineering Review Doc) | Formal approvers, service SLAs required |
| **Amazon** | 6-pager | Narrative format, silent reading |
| **Rust/OSS** | RFC | Community feedback, explicit process |

#### Uber RFC/ERD Process

```
AUTHOR WRITES -> CIRCULATE -> COLLECT FEEDBACK -> APPROVE -> IMPLEMENT
                    |              |               |
               Mailing list   Comments in doc   Approvers sign
               (segmented)    Add objections    or object
```

### Templates

#### Design Doc Template (Google-style)

```markdown
# Design Doc: [Project Name]

**Author:** [Name]
**Reviewers:** [Names]
**Status:** Draft | In Review | Approved | Implemented
**Last Updated:** YYYY-MM-DD

---

## Overview

[1-2 paragraphs describing what this doc covers and why it exists]

## Context and Scope

### Background
[What led to this design being needed?]

### Goals
- [Goal 1]
- [Goal 2]

### Non-Goals
- [Explicitly what this design does NOT address]

## Design

### System Overview
[High-level architecture diagram and description]

### Detailed Design

#### Component A
[Details about component A]

#### Component B
[Details about component B]

### Data Model
[Database schema, data structures]

### API
[API endpoints, contracts]

## Alternatives Considered

### Alternative 1: [Name]
[Description]
- **Pros:** [benefits]
- **Cons:** [drawbacks]
- **Why not chosen:** [reason]

### Alternative 2: [Name]
...

## Cross-cutting Concerns

### Security
[Security implications and mitigations]

### Privacy
[Data privacy considerations]

### Scalability
[How design handles growth]

### Monitoring
[Observability, alerting]

## Timeline and Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Design approval | YYYY-MM-DD | [ ] |
| Phase 1 complete | YYYY-MM-DD | [ ] |
| Launch | YYYY-MM-DD | [ ] |

## Open Questions

1. [Unresolved question 1]
2. [Unresolved question 2]

## References

- [Link to related docs]
- [Link to ADRs]
```

#### RFC Template (Uber-style)

```markdown
# RFC: [Title]

**RFC Number:** RFC-NNN
**Author:** [Name]
**Status:** Draft | Review | Approved | Rejected
**Created:** YYYY-MM-DD
**Approvers:** [List of required approvers]

---

## Summary

[One paragraph summary of the proposal]

## Motivation

[Why are we doing this? What problem does it solve?]

## Proposal

### Overview
[High-level description of proposed solution]

### Detailed Design
[Technical details of the implementation]

### Service SLAs (if applicable)
| Metric | Target |
|--------|--------|
| Availability | 99.9% |
| P99 Latency | <100ms |
| Throughput | 1000 RPS |

### Dependencies
- [External service/library 1]
- [External service/library 2]

### Rollout Plan
1. [Phase 1]
2. [Phase 2]
3. [Phase 3]

## Alternatives

### Alternative 1
[Description and why rejected]

## Security Considerations

[Security analysis]

## Operational Considerations

[Deployment, monitoring, rollback]

## Timeline

| Phase | Description | Target |
|-------|-------------|--------|
| 1 | [Description] | Q1 2026 |
| 2 | [Description] | Q2 2026 |

## Approvals

| Approver | Team | Status | Date |
|----------|------|--------|------|
| [Name] | [Team] | [ ] | |
| [Name] | [Team] | [ ] | |
```

### Best Practices

| Practice | Description |
|----------|-------------|
| **Silent reading** | Start review meetings with 10-15 min reading |
| **Inline comments** | Comment on specific sections, not general feedback |
| **Explicit approvers** | Define who must sign off |
| **Segmented distribution** | Send to relevant mailing lists only |
| **Templates by type** | Different templates for services, libraries, policies |
| **Keep it short** | 2-5 pages typically; longer needs justification |

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Design doc as spec | Keep separate: design doc (why/how), spec (what) |
| No alternatives section | Always document what you considered |
| Writing after implementation | Write before coding; cheap to change |
| Too many approvers | Keep under 10 participants |
