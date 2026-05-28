# PRD Templates

Detailed templates for different PRD types.

## Feature PRD Template

```markdown
# [Feature Name] PRD

## Document Info
| Field | Value |
|-------|-------|
| Author | [Name] |
| Status | Draft / In Review / Approved |
| Created | YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |
| Target Release | [Version or Quarter] |
| Reviewers | [Names] |
| Approvers | [Names] |

---

## Executive Summary

[2-3 paragraph overview for stakeholders who won't read the full document]

---

## Problem Statement

### Current State
[Describe how things work today]

### Pain Points
1. [Pain point 1 with impact]
2. [Pain point 2 with impact]
3. [Pain point 3 with impact]

### Opportunity
[What becomes possible if we solve this?]

---

## Goals & Success Metrics

### Primary Goal
[One sentence describing the main objective]

### Success Metrics
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| [Metric 1] | [Baseline] | [Target] | [How we measure] |
| [Metric 2] | [Baseline] | [Target] | [How we measure] |

### Non-Goals
- [What we explicitly are NOT trying to achieve]

---

## User Research

### Target Users
| Persona | Description | Size | Priority |
|---------|-------------|------|----------|
| [Persona 1] | [Brief description] | [% of users] | Primary |
| [Persona 2] | [Brief description] | [% of users] | Secondary |

### User Interviews/Research
[Summary of research conducted, key insights]

---

## User Stories

### [Persona 1]: [Persona Name]

**US-1:** As a [persona], I want to [action] so that [benefit].

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**US-2:** As a [persona], I want to [action] so that [benefit].

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### [Persona 2]: [Persona Name]

**US-3:** As a [persona], I want to [action] so that [benefit].

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## Requirements

### Functional Requirements

| ID | Requirement | User Story | Priority | Notes |
|----|-------------|------------|----------|-------|
| FR-1 | [Description] | US-1 | P0 | |
| FR-2 | [Description] | US-1, US-2 | P0 | |
| FR-3 | [Description] | US-3 | P1 | |
| FR-4 | [Description] | US-2 | P2 | Future phase |

### Non-Functional Requirements

#### Performance
- Page load time: < [X] seconds
- API response time: < [X] ms (p95)
- Concurrent users supported: [X]

#### Security
- Authentication: [requirements]
- Authorization: [requirements]
- Data protection: [requirements]

#### Accessibility
- WCAG 2.1 Level [AA/AAA]
- Screen reader compatibility
- Keyboard navigation

#### Scalability
- Expected load: [X] requests/day
- Data growth: [X] records/month

---

## Design

### User Flow
[Diagram or description of main user flow]

### Wireframes/Mockups
[Links to Figma, screenshots, or embedded images]

### Design Decisions
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| [Decision 1] | [Why] | [Other options] |

---

## Technical Approach

### Architecture Overview
[High-level system diagram or description]

### Key Technical Decisions
| Decision | Rationale |
|----------|-----------|
| [Decision 1] | [Why this approach] |
| [Decision 2] | [Why this approach] |

### Data Model
[Key entities, relationships, new fields]

### API Changes
[New endpoints, modified endpoints]

### Integrations
- [System 1]: [Integration type and purpose]
- [System 2]: [Integration type and purpose]

---

## Out of Scope

Explicitly excluded from this release:

- [Item 1]: [Reason for exclusion]
- [Item 2]: [Reason for exclusion]
- [Item 3]: Will be addressed in Phase 2

---

## Dependencies

### Internal Dependencies
| Dependency | Owner | Status | Risk |
|------------|-------|--------|------|
| [Feature/Team] | [Name] | [Status] | [Low/Med/High] |

### External Dependencies
| Dependency | Type | Status | Contingency |
|------------|------|--------|-------------|
| [Vendor/API] | [Integration] | [Status] | [Backup plan] |

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|------------|--------|------------|-------|
| [Risk 1] | [High/Med/Low] | [High/Med/Low] | [Plan] | [Name] |
| [Risk 2] | [High/Med/Low] | [High/Med/Low] | [Plan] | [Name] |

---

## Timeline

### Milestones
| Phase | Start | End | Deliverable |
|-------|-------|-----|-------------|
| Design | [Date] | [Date] | Final mockups |
| Development | [Date] | [Date] | Feature complete |
| QA | [Date] | [Date] | Test sign-off |
| Release | [Date] | [Date] | Production deploy |

### Resource Requirements
- Engineering: [X] developers for [Y] weeks
- Design: [X] designers for [Y] weeks
- QA: [X] testers for [Y] weeks

---

## Open Questions

| ID | Question | Owner | Due Date | Resolution |
|----|----------|-------|----------|------------|
| Q1 | [Question] | [Name] | [Date] | [Pending/Resolved: answer] |
| Q2 | [Question] | [Name] | [Date] | [Pending/Resolved: answer] |

---

## Appendix

### Glossary
| Term | Definition |
|------|------------|
| [Term 1] | [Definition] |

### References
- [Link to related PRD]
- [Link to research]
- [Link to competitor analysis]

### Changelog
| Date | Author | Change |
|------|--------|--------|
| YYYY-MM-DD | [Name] | Initial draft |
| YYYY-MM-DD | [Name] | [Change description] |
```

---

## Enhancement PRD Template

```markdown
# [Enhancement Name] PRD

## Document Info
| Field | Value |
|-------|-------|
| Author | [Name] |
| Status | Draft / In Review / Approved |
| Related Feature | [Link to original feature PRD] |
| Target Release | [Version] |

---

## Current State

### Existing Behavior
[How the feature works today]

### Limitations
1. [Limitation 1]
2. [Limitation 2]

### User Feedback
[Relevant feedback, support tickets, NPS comments]

---

## Proposed Changes

### Summary
[One paragraph describing the enhancement]

### Before/After Comparison
| Aspect | Current | Proposed |
|--------|---------|----------|
| [Aspect 1] | [Current behavior] | [New behavior] |
| [Aspect 2] | [Current behavior] | [New behavior] |

---

## Impact Analysis

### Affected Users
- [User segment 1]: [Impact]
- [User segment 2]: [Impact]

### Affected Systems
- [System 1]: [Changes needed]
- [System 2]: [Changes needed]

### Migration Plan
[How existing users/data will transition]

---

## Requirements
[Use same format as Feature PRD]

---

## Timeline
[Use same format as Feature PRD]
```

---

## Technical PRD Template

```markdown
# [Technical Initiative] PRD

## Document Info
| Field | Value |
|-------|-------|
| Author | [Name] |
| Status | Draft / In Review / Approved |
| Type | Infrastructure / Architecture / Performance |
| Target Release | [Version] |

---

## Technical Problem

### Current Architecture
[Diagram and description of current state]

### Pain Points
1. [Technical limitation 1]
2. [Technical limitation 2]

### Impact on Product
[How technical debt affects users/features]

---

## Proposed Solution

### Architecture Overview
[Diagram of proposed architecture]

### Key Changes
| Component | Current | Proposed | Rationale |
|-----------|---------|----------|-----------|
| [Component 1] | [Current] | [Proposed] | [Why] |

### Trade-offs
| Approach | Pros | Cons |
|----------|------|------|
| [Option 1] | [Pros] | [Cons] |
| [Option 2] | [Pros] | [Cons] |

**Recommended:** [Option X] because [rationale]

---

## Technical Specifications

### API Contracts
[OpenAPI spec or endpoint documentation]

### Data Model Changes
[Schema changes, migrations]

### Performance Requirements
- Latency: [target]
- Throughput: [target]
- Availability: [target]

---

## Migration Plan

### Phases
1. [Phase 1]: [Description]
2. [Phase 2]: [Description]

### Rollback Plan
[How to revert if issues arise]

### Feature Flags
[Flags needed for gradual rollout]

---

## Testing Strategy

### Unit Tests
[Coverage requirements]

### Integration Tests
[Key integration points to test]

### Load Tests
[Performance testing approach]

### Rollout Validation
[How we verify success in production]
```

---

## Spike/Research PRD Template

```markdown
# [Research Topic] Spike

## Document Info
| Field | Value |
|-------|-------|
| Author | [Name] |
| Timebox | [X] days |
| Due Date | YYYY-MM-DD |

---

## Objective

### Question to Answer
[Primary question this spike will answer]

### Success Criteria
- [ ] [What we need to learn/prove]
- [ ] [What we need to learn/prove]

---

## Background

### Context
[Why we need this research]

### Constraints
[Known limitations, requirements]

---

## Approach

### Research Methods
1. [Method 1]: [Description]
2. [Method 2]: [Description]

### Deliverables
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

---

## Findings

[To be completed during spike]

### Key Learnings
1. [Learning 1]
2. [Learning 2]

### Recommendations
[What to do next based on findings]

### Open Questions
[Questions that remain after spike]
```

