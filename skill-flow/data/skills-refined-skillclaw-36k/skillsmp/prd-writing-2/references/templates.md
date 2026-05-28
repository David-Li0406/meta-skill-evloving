# PRD Templates

This file contains all templates used in the PRD writing process.

## Table of Contents

1. [Clarification Log Template](#clarification-log-template)
2. [PRD Main File Template](#prd-main-file-template)
3. [Section Templates](#section-templates)
4. [For-AI Outline Template](#for-ai-outline-template)

---

## Clarification Log Template

Create this file as `prd-[feature]-clarification.md`:

```markdown
# Clarification Log: [Feature Name]

> Decision record from requirement clarification phase.
> Related PRD: [prd-[feature].md](prd-[feature].md)

---

## Original Input

[PM's original input, preserved verbatim]

---

## Key Decisions

| Topic | Question | Decision |
|-------|----------|----------|
| | | |

---

## Escalation Notes

[If any suggestions to consult others]

---

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| | |
```

---

## PRD Main File Template

Create this file as `prd-[feature].md`:

```markdown
# PRD: [Feature Name]

> **Status:** Draft
> **Author:** [PM Name]
> **Last Updated:** [Date]

---

> **Clarification Log:** [prd-[feature]-clarification.md](prd-[feature]-clarification.md)

---

## Overview
[To be filled in Phase 1]

## Success Metrics
[To be filled in Phase 1]

## Impact Scope
[To be filled in Phase 1]

## User Perspective
[To be filled in Phase 1]

## System Perspective
[To be filled in Phase 1]

## Other Notes
[To be filled in Phase 1]

## For AI
[To be filled in Phase 3]

---

## Document Status

| Phase | Status | Date |
|-------|--------|------|
| Clarification | ⏳ In Progress | [Date] |
| Human Sections | ⏳ Pending | - |
| For AI Outline | ⏳ Pending | - |
| Final | ⏳ Pending | - |
```

---

## Section Templates

### Overview

```markdown
## Overview

**Feature Name:** [Name]

**Summary:** [One sentence: what problem this solves]

**Background:** [Why now? What's the pain point? Business context]
```

### Success Metrics

```markdown
## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |
```

### Impact Scope

```markdown
## Impact Scope

**Systems Affected:**
- [system-a] — [brief impact description]
- [system-b] — [brief impact description]
```

### User Perspective

```markdown
## User Perspective

### User Stories
- As a [user type], I want to [action], so that [benefit]

### Happy Path
1. User does X
2. System responds with Y
3. User sees Z

### Edge Cases & Error Handling
| Scenario | System Behavior |
|----------|-----------------|
| [Edge case] | [How system handles it] |

### UI Prototype
[Link to designs or embed simple wireframes]
```

### System Perspective

```markdown
## System Perspective

### Architecture Overview
[ASCII diagram or description of system interactions]

```
Client → API Gateway → Service A → Database
                    ↘ Service B
```

### Functional Requirements
| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| FR-001 | [Requirement] | [How to verify] |

### Non-Functional Requirements
| ID | Type | Requirement | Target |
|----|------|-------------|--------|
| NFR-001 | Performance | [Requirement] | [Target value] |
```

### Other Notes

```markdown
## Other Notes

> Include only what's relevant. Skip sections that don't apply.

**Dependencies:**
- [Dependency]: [Purpose]

**Compliance:**
- [Requirement]

**Assumptions:**
- [Assumption]

**Risks:**
| Risk | Mitigation |
|------|------------|
| [Risk] | [Mitigation] |

**Out of Scope:**
- [Item]

**Timeline Constraints:**
- [Constraint]

**Known Issues:**
- [Issue]
```

---

## For-AI Outline Template

Append this to PRD during Phase 2 for PM review:

```markdown
## For AI Section — Outline for Review

> ⚠️ **Pending PM Approval**

### 1. Entities Identified
I identified these data entities. Please confirm:
- [ ] **EntityName** — field1, field2, field3
- [ ] **EntityName2** — field1, field2

### 2. APIs/Interfaces
- [ ] `POST /path` — description
- [ ] `GET /path` — description (**inferred, not explicitly stated**)

### 3. Business Rules
- [ ] Rule 1: condition → action
- [ ] Rule 2: condition → action

### 4. Technical Details I Added
These were NOT in the original requirements. I added defaults based on common practice. Please confirm or modify:

| Detail | My Default | Confirm? |
|--------|-----------|----------|
| API timeout | 10s | ⬜ |
| Retry policy | No retry | ⬜ |
| Token expiry | 24h | ⬜ |
| [Detail] | [Value] | ⬜ |

### 5. Open Questions
These need PM clarification before I can complete the spec:
- ❓ [Question 1]
- ❓ [Question 2]

---
**PM:** Please review and confirm. After approval, I will:
1. Update human-readable sections with important details
2. Generate the complete For AI section
```
