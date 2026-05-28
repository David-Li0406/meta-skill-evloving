# SDD Document Templates

All templates for SDD artifacts. Copy and customize for your project.

---

## Constitution Template

```markdown
# Constitution: {Project Name}

**Version:** 1.0
**Created:** YYYY-MM-DD
**Status:** Active

---

## Vision

{1-2 sentences: what is this project and why does it exist}

---

## Tech Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Language | {lang} | {ver} | {why} |
| Framework | {framework} | {ver} | {why} |
| Database | {db} | {ver} | {why} |
| Hosting | {platform} | - | {why} |

---

## Architecture Patterns

| Pattern | Description |
|---------|-------------|
| {pattern} | {brief explanation} |

---

## Code Standards

### Naming Conventions
- Files: `{convention}`
- Classes: `{convention}`
- Functions: `{convention}`
- Variables: `{convention}`

### Formatting
- Formatter: {tool}
- Linter: {tool}
- Config: {location}

### Testing
- Framework: {framework}
- Coverage target: {X}%
- Test location: {path}

---

## Git Workflow

- Branch strategy: {strategy}
- Commit format: `{format}`
- PR requirements: {requirements}

---

## Project Structure

```
{project}/
├── {folder}/     # {purpose}
├── {folder}/     # {purpose}
└── {folder}/     # {purpose}
```

---

## Quality Gates

| Gate | Criteria | When |
|------|----------|------|
| Lint | Zero errors | Pre-commit |
| Types | Zero errors | Pre-commit |
| Tests | 100% pass | Pre-push |
| Coverage | >{X}% | Pre-merge |

---

## Principles

1. {Principle 1}
2. {Principle 2}
3. {Principle 3}
```

---

## Specification Template

```markdown
# Feature: {Feature Name}

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** {Name}
**Date:** YYYY-MM-DD
**Project:** {project-name}

---

## Reference Documents

| Document | Path |
|----------|------|
| Constitution | `.aidocs/constitution.md` |
| Related Feature | `features/done/{NN}-{feature}/spec.md` |

---

## Overview

{2-3 sentences describing the feature and its purpose}

---

## Problem Statement

**Who:** {User persona}
**Problem:** {What they cannot do}
**Impact:** {Business/user impact}
**Solution:** {High-level approach}
**Success Metric:** {How we measure success}

---

## User Personas

### Persona 1: {Name/Archetype}
- **Role:** {What they do}
- **Goal:** {What they want}
- **Pain Points:** {Current frustrations}
- **Context:** {When/where they use product}

---

## User Stories

### US-001: {Story Title}
**As a** {persona}
**I want to** {action}
**So that** {benefit}

**Priority:** Must | Should | Could
**Acceptance Criteria:** AC-001

### US-002: {Story Title}
...

---

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL {requirement} | US-001 | Must |
| FR-002 | System SHALL {requirement} | US-001 | Must |
| FR-003 | System SHOULD {requirement} | US-002 | Should |

---

## Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|-------------|--------|----------|
| NFR-001 | Performance | Response time | < 500ms p95 | Must |
| NFR-002 | Security | Password storage | bcrypt 12 rounds | Must |

---

## Acceptance Criteria

### AC-001: {Scenario Title}

**Scenario:** {Brief description}

**Given:** {precondition}
**And:** {additional precondition}
**When:** {action}
**Then:** {expected result}
**And:** {additional result}

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| {Feature} | {Why excluded} | {Future phase or Never} |

---

## Assumptions & Constraints

### Assumptions
- {Assumption 1}
- {Assumption 2}

### Constraints
- {Technical constraint}
- {Business constraint}

---

## Dependencies

### Internal
- {Other feature this depends on}

### External
- {Third-party service}
```

---

## Design Document Template

```markdown
# Design: {Feature Name}

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** {Name}
**Date:** YYYY-MM-DD
**Spec:** {link to spec.md}

---

## Reference Documents

| Document | Path |
|----------|------|
| Specification | `spec.md` |
| Constitution | `.aidocs/constitution.md` |
| Contracts | `.aidocs/contracts.md` |

---

## Overview

{2-3 sentences: technical approach summary}

---

## Architecture Decisions

### AD-1: {Decision Name}

**Context:**
{Problem being solved and relevant context}

**Options:**
- **A: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}
- **B: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}

**Decision:** {Chosen solution}

**Rationale:** {Why this solution, influencing factors}

### AD-2: {Decision Name}
...

---

## Components

### Component 1: {Name}
- **Purpose:** {what it does}
- **Location:** {path}
- **Dependencies:** {what it uses}

```
[Diagram if complex]
```

---

## Data Flow

```
{Component A} → {Component B} → {Component C}
       ↓              ↓              ↓
   validate       process        persist
```

---

## Data Models

### {Model Name}
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Primary key |
| {field} | {type} | {constraints} | {description} |

---

## API Endpoints

Reference: `contracts.md` section {X}

| Method | Path | Description | FR |
|--------|------|-------------|-----|
| POST | /api/v1/{resource} | Create | FR-001 |
| GET | /api/v1/{resource}/{id} | Read | FR-002 |

---

## Files

| File | Action | Description |
|------|--------|-------------|
| {path/to/file.py} | CREATE | {what to create} |
| {path/to/file.py} | MODIFY | {what to modify} |

---

## Testing Strategy

### Unit Tests
| Component | Test File | Coverage |
|-----------|-----------|----------|
| {component} | test_{component}.py | {target}% |

### Integration Tests
| Flow | Test File | Description |
|------|-----------|-------------|
| {flow} | test_{flow}_integration.py | {description} |

---

## Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| {risk} | High/Med/Low | High/Med/Low | {mitigation} |

---

## FR Coverage

| FR | AD | Files | Status |
|----|-----|-------|--------|
| FR-001 | AD-1 | models.py, services.py | Covered |
| FR-002 | AD-2 | views.py | Covered |
```

---

## Implementation Plan Template

```markdown
# Implementation Plan: {Feature Name}

**Version:** 1.0
**Status:** Draft | Approved
**Design:** {link to design.md}
**Date:** YYYY-MM-DD

---

## Overview

- **Total tasks:** {N}
- **Complexity:** Low | Medium | High
- **Est. tokens:** ~{X}k total
- **Critical path:** TASK_001 -> TASK_003 -> TASK_005

---

## Task Summary

| Task | Name | Complexity | Est. Tokens | Depends On | Enables |
|------|------|------------|-------------|------------|---------|
| TASK_001 | {name} | Low | ~10k | - | TASK_003 |
| TASK_002 | {name} | Medium | ~25k | - | TASK_003 |
| TASK_003 | {name} | High | ~40k | 001, 002 | TASK_005 |

---

## Dependency Graph

```
TASK_001 ──┬──> TASK_003 ──┐
           │               │
TASK_002 ──┘               ├──> TASK_005
                           │
TASK_004 ─────────────────┘
```

---

## Execution Waves

### Wave 1 (Parallel)
| Task | Description | Est. Tokens |
|------|-------------|-------------|
| TASK_001 | {description} | ~10k |
| TASK_002 | {description} | ~25k |

**Checkpoint 1:** Verify {criteria}

### Wave 2 (Parallel)
| Task | Depends On | Description |
|------|------------|-------------|
| TASK_003 | 001, 002 | {description} |
| TASK_004 | - | {description} |

**Checkpoint 2:** Verify {criteria}

### Wave 3 (Sequential - Critical Path)
| Task | Depends On | Description |
|------|------------|-------------|
| TASK_005 | 003, 004 | {description} |

**Final Checkpoint:** All tests pass, all AC verified

---

## Tasks Detail

### TASK_001: {Name}

**Objective:** {Clear, single-agent executable goal}

**Dependencies:** None

**Files:**
| File | Action | Description |
|------|--------|-------------|
| {path} | CREATE | {what} |

**Acceptance Criteria:**
- [ ] AC-001.1: {criterion}
- [ ] AC-001.2: {criterion}

**Est. tokens:** ~10k

### TASK_002: {Name}
...

---

## Quality Gates

| Gate | Task | Criteria |
|------|------|----------|
| Checkpoint 1 | After Wave 1 | {criteria} |
| Checkpoint 2 | After Wave 2 | {criteria} |
| Final | After Wave 3 | All tests pass |

---

## FR/AD Coverage

| FR | Task(s) | AD | Status |
|----|---------|-----|--------|
| FR-001 | TASK_001, TASK_003 | AD-1 | Planned |
| FR-002 | TASK_002 | AD-2 | Planned |

---

## Risks

| Risk | Impact | Mitigation | Contingency |
|------|--------|------------|-------------|
| {risk} | {impact} | {mitigation} | {if occurs} |
```

---

## Task File Template

```markdown
# TASK_{NNN}: {Short Name}

**Feature:** {feature-name}
**Status:** todo | in-progress | done
**Created:** YYYY-MM-DD

---

## SDD References

| Document | Path |
|----------|------|
| Spec | .aidocs/features/{status}/{feature}/spec.md |
| Design | .aidocs/features/{status}/{feature}/design.md |
| Plan | .aidocs/features/{status}/{feature}/implementation-plan.md |

---

## Task Dependency Tree

| Dependency | Status | Key Output |
|------------|--------|------------|
| TASK_{XXX} | done | {what it provided} |

---

## Requirements Coverage

### FR-{X}: {Full requirement text}
Covered by this task.

---

## Objective

{Clear, single-agent executable goal - what exactly to implement}

---

## Dependencies

- TASK_{XXX} must complete first (provides {what})

---

## Acceptance Criteria

- [ ] AC-{NNN}.1: {Given-When-Then or criterion}
- [ ] AC-{NNN}.2: {Given-When-Then or criterion}

---

## Technical Approach

1. {Step 1}
2. {Step 2}
3. {Step 3}

---

## Files

| File | Action | Scope |
|------|--------|-------|
| {path/to/file.py} | CREATE | {what to create} |
| {path/to/file.py} | MODIFY | {what to modify} |

---

## Estimated Tokens

~{XX}k

---

## Implementation

<!-- Fill during execution -->

### Changes Made
- {file}: {change}

### Tests Added
- {test file}: {tests}

---

## Summary

<!-- Fill after completion -->

### Completed
- [x] {what was done}

### Issues Encountered
- {issue and resolution}

### Lessons Learned
- {pattern or mistake}
```

---

## Roadmap Template

```markdown
# Roadmap: {Project Name}

**Last Updated:** YYYY-MM-DD

---

## Vision

{1-2 sentences: where is this project going}

---

## Now (This Quarter) - 90% Confident

| Feature | Status | Target | Notes |
|---------|--------|--------|-------|
| {NN}-{feature} | In Progress | {month} | {notes} |
| {NN}-{feature} | Todo | {month} | {notes} |

---

## Next (Next Quarter) - 70% Confident

| Feature | Description | Dependencies |
|---------|-------------|--------------|
| {feature} | {one-liner} | {deps} |

---

## Later (Future) - 50% Confident

| Theme | Description |
|-------|-------------|
| {theme} | {high-level goal} |

---

## Done

| Feature | Completed | Highlights |
|---------|-----------|------------|
| {NN}-{feature} | YYYY-MM | {key outcome} |

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| {risk} | {impact} | {mitigation} |

---

## Metrics

| Metric | Current | Target |
|--------|---------|--------|
| {metric} | {value} | {goal} |
```

---

## Backlog Item Template

```markdown
## BL-{NNN}: {Title}

**Priority:** P0 | P1 | P2 | P3
**Estimate:** {points} pts | {T-shirt size}
**Status:** grooming | ready | in-progress | done

---

### Problem

{What need does this address}

---

### Acceptance Criteria

- [ ] {criterion 1}
- [ ] {criterion 2}

---

### Dependencies

- Requires: BL-{XXX}
- Blocks: BL-{YYY}

---

### Notes

{Additional context}
```

---

## Confidence Check Template

```markdown
## Confidence Check: {Phase}

**Date:** YYYY-MM-DD
**Phase:** Pre-Spec | Pre-Design | Pre-Task | Pre-Implementation

---

### Score: {X}%

| Check | Weight | Status | Evidence |
|-------|--------|--------|----------|
| {check} | {X}% | Pass/Warn/Fail | {evidence or gap} |
| {check} | {X}% | Pass/Warn/Fail | {evidence or gap} |

---

### Verdict: Proceed | Clarify | Stop

---

### Questions to Answer First

1. {question}
2. {question}

---

### Recommended Actions

- {action}
- {action}
```

---

## Pattern Record Template

```json
{
  "id": "PAT-{NNN}",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "project": "{project}",
  "task_type": "{type}",
  "pattern_name": "{name}",
  "description": "{what worked}",
  "context": "{when to use}",
  "code_example": "{code snippet}",
  "success_count": 1,
  "tags": ["tag1", "tag2"]
}
```

---

## Mistake Record Template

```json
{
  "id": "ERR-{NNN}",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "project": "{project}",
  "task_type": "{type}",
  "error_type": "{category}",
  "description": "{what went wrong}",
  "root_cause": "{why it happened}",
  "solution": "{how to fix}",
  "prevention": "{how to prevent}",
  "occurrence_count": 1,
  "tags": ["tag1", "tag2"]
}
```

---

## Token Estimation Guide

| Component | Typical Tokens |
|-----------|----------------|
| Django model (simple) | 5-10k |
| Django model (complex) | 15-25k |
| Service class | 20-40k |
| ViewSet | 15-30k |
| Serializer | 5-15k |
| Test file | 20-40k |
| React component (simple) | 5-10k |
| React component (complex) | 15-30k |
| API endpoint | 10-20k |

**Rule:** If uncertain, estimate higher and split.

**100k Token Budget:**
```
Research: ~20k (read existing code)
Task file: ~5k
Implementation: ~50k
Buffer: ~25k
TOTAL < 100k
```

---

*SDD Templates v2.0*
*Use with faion-sdd skill*
