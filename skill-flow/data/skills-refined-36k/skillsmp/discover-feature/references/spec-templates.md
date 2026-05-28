# Feature Spec Templates

## Standard Feature Spec

Use this format for `/docs/specs/[feature-name].md`:

```markdown
# Feature Spec: [Feature Name]

**Status**: Draft | In Review | Approved | In Development | Shipped
**Author**: [Name]
**Created**: [Date]
**Last Updated**: [Date]

## Problem Statement

### Job to be Done
When [SITUATION/TRIGGER],
I want to [MOTIVATION/GOAL],
so I can [EXPECTED OUTCOME].

### Current State
[Description of how users currently handle this, including pain points]

### Evidence
- [User feedback, analytics, or research supporting this problem]

## Solution Overview

### Proposed Solution
[High-level description of the feature]

### Key User Flows
1. [Primary flow]
2. [Secondary flow]
3. [Edge cases]

### Visual Design
[Mockups, wireframes, or descriptions of UI]

## Scope

### MVP (v1) Requirements
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

### Out of Scope (Future Versions)
- [Enhancement 1] - Reason for deferral
- [Enhancement 2] - Reason for deferral

### Non-Goals
- [What this feature explicitly will NOT do]

## Technical Considerations

### Architecture
[How this fits into the existing system]

### Data Model
[New tables, fields, or state required]

### API/Service Changes
[New endpoints or service modifications]

### Dependencies
- [Dependency 1]
- [Dependency 2]

### Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Strategy] |

## Success Criteria

### User Metrics
- [ ] [Metric 1]: [Target]
- [ ] [Metric 2]: [Target]

### Technical Metrics
- [ ] [Performance metric]: [Target]
- [ ] [Reliability metric]: [Target]

### Business Metrics
- [ ] [Business metric]: [Target]

## Implementation Tasks

### Phase 1: Foundation
1. [Task 1]
2. [Task 2]

### Phase 2: Core Feature
1. [Task 1]
2. [Task 2]

### Phase 3: Polish
1. [Task 1]
2. [Task 2]

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

## Appendix

### Research Notes
[Links to user research, competitive analysis, etc.]

### Technical Spikes
[Results of technical investigations]
```

---

## Task Breakdown Format

Use this format for `/docs/tasks/[feature]/[task-name].md`:

```markdown
# Task X.Y.Z: [Task Title]

## Phase
Phase X: [Phase Name]

## Section
X.Y [Section Name]

## Description
[Detailed description of what this task accomplishes. Include context about why it's needed and how it fits into the larger feature.]

## Dependencies
- Task X.Y.Z: [Dependency name]
- Task X.Y.Z: [Dependency name]

## Files to Create/Modify
- `path/to/file.tsx` - [Brief description]
- `path/to/another/file.ts` - [Brief description]

## Implementation Details

### [Subtask 1 Title]
[Implementation guidance or code example]

### [Subtask 2 Title]
[Implementation guidance]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
- [ ] TypeScript compiles without errors
- [ ] Component renders correctly

## Notes
- [Important consideration 1]
- [Important consideration 2]
```

### Task Numbering Convention

```
Phase.Section.Task

Example: 3.3.1
- Phase 3
- Section 3.3
- Task 1
```

---

## Linear-Ready Format

Use this format when exporting to Linear or similar project management tools:

```markdown
## Linear Import: [Feature Name]

### Epic: [Feature Name]
**Description**: [JTBD statement and high-level description]
**Labels**: feature, [area], [priority]

---

### Task 1: [Task Title]
**Description**:
[Detailed description]

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Labels**: [component], [type]
**Estimate**: [1-8 points]
**Dependencies**: None

---

### Task 2: [Task Title]
**Description**:
[Detailed description]

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Labels**: [component], [type]
**Estimate**: [1-8 points]
**Dependencies**: Task 1

---
```

### Common Labels
**Types**: `feature`, `bug`, `tech-debt`, `spike`, `docs`
**Priority**: `urgent`, `high`, `medium`, `low`

---

## Quick Reference: Spec Checklist

Before finalizing any spec, verify:

### Problem Definition
- [ ] JTBD statement is specific and validated
- [ ] Current alternatives are documented
- [ ] Pain points are identified with severity

### Solution Design
- [ ] Primary user flow is clear
- [ ] Edge cases are considered
- [ ] Technical approach is viable

### Scope Management
- [ ] MVP is clearly bounded
- [ ] Out-of-scope items are explicit
- [ ] Non-goals prevent scope creep

### Success Definition
- [ ] Metrics are measurable
- [ ] Targets are realistic
- [ ] Timeframe is defined

### Implementation Readiness
- [ ] Tasks are atomic and estimable
- [ ] Dependencies are mapped
- [ ] Risks are identified with mitigations
- [ ] Open questions have owners/deadlines
