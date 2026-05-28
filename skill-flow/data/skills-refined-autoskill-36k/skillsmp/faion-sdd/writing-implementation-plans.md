---
id: writing-implementation-plans
name: "Writing Implementation Plans"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Writing Implementation Plans

## Metadata

| Field | Value |
|-------|-------|
| **ID** | writing-implementation-plans |
| **Version** | 2.0.0 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #implementation, #planning |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-impl-plan-reviewer-agent |

---

## Methodology Reference

**Primary:** writing-implementation-plans (Writing Implementation Plans v2.0)

**Integrated:**
| Domain | Methodology | Principle Applied |
|--------|-------------|-------------------|
| PM | wbs-decomposition | WBS decomposition |
| PM | dependency-management | Dependency types (FS, SS, FF, SF) |
| PM | risk-assessment | Risk assessment |
| PM | schedule-management | Schedule management |
| BA | requirements-traceability | Requirements traceability (AD-X → TASK) |
| PdM | backlog-management | INVEST principle for tasks |
| Dev | testing-strategy | Testing strategy |
| SDD | task-creation-parallelization | Task parallelization and waves |

---

## Problem

Developers struggle to start coding after reading design documents because:
- Design is too high-level to act on directly
- Unclear order of operations
- Dependencies between components not obvious
- No clear success criteria for each step
- AI agents fail with tasks > 100k tokens
- Parallel work opportunities missed

**The root cause:** No bridge between design and actionable tasks.

---

## Framework

### What is an Implementation Plan?

An implementation plan breaks the design into ordered, actionable tasks with:
- Clear dependencies (graph-based)
- Effort estimates (for AI context budget)
- Success criteria (testable)
- Parallelization opportunities (waves)
- Risk mitigation strategies

### Document Hierarchy

```
SPEC (what) → DESIGN (how) → IMPL PLAN (order) → TASKS (execution)
  FR-X         AD-X          TASK-XXX outline    TASK_XXX.md files
                                   ↓
                              Wave 1: TASK-001, TASK-002 (parallel)
                              Wave 2: TASK-003, TASK-004 (depends on W1)
                              Wave 3: TASK-005 (depends on W2)
```

### Implementation Plan Structure v2.0

```markdown
# Implementation Plan: [Feature Name]

## Reference Documents
[Links to design, spec, constitution]

## Overview
[Summary of implementation approach]

## Prerequisites
[What must exist before starting]

## Dependency Graph
[Visual dependency tree]

## Wave Analysis
[Tasks grouped by execution waves]

## Phase Breakdown
[Logical grouping of tasks]

## Task List
[TASK-XXX entries with INVEST validation]

## Critical Path
[Longest dependency chain]

## Risk Assessment
[Risks and mitigations]

## Testing Plan
[What to test at each phase]

## Rollout Strategy
[How to deploy safely]

## Recommended Skills & Methodologies
[For task execution]
```

---

## Writing Process

### Phase 1: Load Full SDD Context

Before writing, read and understand:

```
1. .aidocs/constitution.md - project principles
2. {FEATURE_DIR}/spec.md - requirements (FR-X)
3. {FEATURE_DIR}/design.md - architecture (AD-X)
4. features/done/ - completed implementation plans for patterns
```

Extract:
- All AD-X decisions to implement
- File changes list (CREATE/MODIFY)
- Dependencies between components
- Testing requirements

### Phase 2: Prerequisites Check

List everything that must exist before starting:

```markdown
## Prerequisites

### Infrastructure
- [ ] PostgreSQL database running
- [ ] Redis instance configured
- [ ] SendGrid API key obtained

### Environment
- [ ] Development environment set up
- [ ] Environment variables configured
- [ ] Access permissions granted

### Code Dependencies
- [ ] Base service class exists
- [ ] Auth middleware exists
- [ ] Test framework configured

### Documentation
- [ ] Spec approved (status: Approved)
- [ ] Design approved (status: Approved)
```

### Phase 3: Work Breakdown Structure (PM: wbs-decomposition)

#### 3.1 WBS Principles

| Level | Description | Example |
|-------|-------------|---------|
| **Phase** | Logical grouping | "Phase 1: Infrastructure" |
| **Task** | Atomic work unit | "TASK-001: Create users table" |
| **Subtask** | Steps within task | "01. Create migration file" |

#### 3.2 Decomposition Rules

- **100% Rule:** All work is accounted for
- **Mutually Exclusive:** No overlap between tasks
- **Completeness:** Each task has clear done criteria
- **AI Context:** Each task < 100k tokens

### Phase 4: Build Dependency Graph

#### 4.1 Dependency Types (PM: dependency-management)

| Type | Meaning | Example |
|------|---------|---------|
| **FS** | Finish-to-Start | TASK-002 starts when TASK-001 finishes |
| **SS** | Start-to-Start | TASK-002 can start when TASK-001 starts |
| **FF** | Finish-to-Finish | TASK-002 finishes when TASK-001 finishes |
| **SF** | Start-to-Finish | TASK-002 finishes when TASK-001 starts (rare) |

#### 4.2 Dependency Graph Visualization

```markdown
## Dependency Graph

```
TASK-001 (Users table)
    │
    ├──[FS]──→ TASK-003 (Registration handler)
    │              │
    │              └──[FS]──→ TASK-005 (Registration tests)
    │
    └──[FS]──→ TASK-004 (Login handler)
                   │
                   └──[FS]──→ TASK-006 (Login tests)

TASK-002 (Password utils) ──[SS]──→ TASK-003 (Registration handler)
                          ──[SS]──→ TASK-004 (Login handler)
```
```

### Phase 5: Wave Analysis (SDD: task-creation-parallelization)

#### 5.1 Wave Identification

Group tasks by dependency level:

```markdown
## Wave Analysis

| Wave | Tasks | Can Run In Parallel | Dependencies |
|------|-------|---------------------|--------------|
| Wave 1 | TASK-001, TASK-002 | Yes | None |
| Wave 2 | TASK-003, TASK-004 | Yes | Wave 1 |
| Wave 3 | TASK-005, TASK-006 | Yes | Wave 2 |
| Wave 4 | TASK-007 | No | Wave 3 |
```

#### 5.2 Wave Visualization

```
Wave 1 (parallel)    Wave 2 (parallel)    Wave 3 (parallel)    Wave 4
┌──────────┐         ┌──────────┐         ┌──────────┐         ┌──────────┐
│ TASK-001 │─────────│ TASK-003 │─────────│ TASK-005 │─────────│ TASK-007 │
│ Users DB │         │ Register │         │ Reg Tests│         │ E2E Tests│
└──────────┘    ┌────│          │────┐    └──────────┘         └──────────┘
                │    └──────────┘    │
┌──────────┐    │                    │    ┌──────────┐
│ TASK-002 │────┤                    └────│ TASK-006 │
│ Password │    │    ┌──────────┐         │ Login Tst│
└──────────┘    └────│ TASK-004 │────────└──────────┘
                     │  Login   │
                     └──────────┘
```

#### 5.3 Wave-Based Task Creation

**Principle:** Create detailed TASK files in waves, not all at once.

```
Wave 1: Create TASK_001, TASK_002 files
    ↓ execute
Wave 2: Create TASK_003, TASK_004 files (incorporate learnings)
    ↓ execute
Wave 3: Create TASK_005, TASK_006 files (incorporate patterns)
    ...
```

**Benefits:**
- Later tasks incorporate learnings from earlier waves
- Patterns discovered in Wave 1 are documented
- Better context from completed dependency tasks
- Reduced rework from early discoveries

### Phase 6: Define Phases

Group related tasks into logical phases:

```markdown
## Phases

| Phase | Description | Tasks | Effort | Dependencies |
|-------|-------------|-------|--------|--------------|
| 1 | Infrastructure | TASK-001, TASK-002 | 1 day | None |
| 2 | Core Logic | TASK-003, TASK-004 | 2 days | Phase 1 |
| 3 | Testing | TASK-005, TASK-006, TASK-007 | 1.5 days | Phase 2 |
| 4 | Integration | TASK-008 | 0.5 days | Phase 3 |

**Total Estimated Effort:** 5 days
```

### Phase 7: Task Definition (INVEST + SMART)

#### 7.1 Task Format v2.0

```markdown
### TASK-XXX: [Concise Title]

**Phase:** [Phase number]
**Wave:** [Wave number]

**Description:**
[2-3 sentences explaining what needs to be done]

**Traces to:**
- AD-X: [Architectural decision this implements]
- FR-X: [Requirement this satisfies]

**Depends on:** TASK-YYY [FS], TASK-ZZZ [SS] (or "None")

**Blocks:** TASK-AAA, TASK-BBB

**Effort:** [X hours]
**Context Estimate:** [Xk tokens]

**Complexity:** simple (1-2h) | normal (2-3h) | complex (3-4h)

**Acceptance Criteria:**
- [ ] [Specific, testable criterion]
- [ ] [Another criterion]

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | `src/path/file.ts` | [What this file does] |
| MODIFY | `src/path/existing.ts` | [What to add/change] |

**Technical Notes:**
[Implementation hints, patterns to follow, gotchas]

**Tests:**
- [ ] Unit: [Test description]
- [ ] Integration: [Test description]

**Recommended Skills:**
- faion-software-developer: [specific aspect]
```

#### 7.2 INVEST Validation

| Criterion | Question | ✅ Good | ❌ Bad |
|-----------|----------|---------|--------|
| **Independent** | Can be done without other incomplete tasks? | No code dependencies on pending tasks | Needs unfinished TASK-005 |
| **Negotiable** | Implementation details flexible? | "User can register" | "Use bcrypt version 5.1.0" |
| **Valuable** | Clear business value? | Enables user registration | Technical refactoring |
| **Estimable** | Effort estimate possible? | 3 hours | "Some time" |
| **Small** | Completable in < 4 hours? | 2-3 hours | 2 days |
| **Testable** | Acceptance criteria testable? | "Returns 201 status" | "Works correctly" |

#### 7.3 Context Budget

| Complexity | Effort | Context | Description |
|------------|--------|---------|-------------|
| **Simple** | 1-2h | < 30k tokens | Single file, clear pattern |
| **Normal** | 2-3h | 30-60k tokens | Multiple files, some research |
| **Complex** | 3-4h | 60-100k tokens | Many files, deep research |

**If > 100k tokens:** Split into multiple tasks.

### Phase 8: Critical Path Analysis

#### 8.1 Identify Critical Path

The critical path is the longest chain of dependent tasks.

```markdown
## Critical Path

```
TASK-001 → TASK-003 → TASK-005 → TASK-007
  1d         1d         0.5d       0.5d     = 3 days
```

**Critical Path Duration:** 3 days

**Implications:**
- Cannot finish feature faster than 3 days
- TASK-001, TASK-003, TASK-005, TASK-007 have no slack
- Delays on critical path delay the entire feature
```

### Phase 9: Risk Assessment (PM: risk-assessment)

```markdown
## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| External API unavailable | Medium | High | Mock API for development |
| Database schema changes | Low | High | Run migrations in staging first |
| Performance issues | Medium | Medium | Load test before production |
| Security vulnerability | Low | High | Security review before launch |

### Contingency Buffer
- Add 20% buffer to critical path
- 3 days → 3.6 days → 4 days
```

### Phase 10: Testing Plan (Dev: testing-strategy)

```markdown
## Testing Plan

### Per-Phase Testing

| Phase | Tests | Pass Criteria |
|-------|-------|---------------|
| Phase 1 | DB migrations | Tables created, rollback works |
| Phase 2 | Unit tests | 80%+ coverage, all pass |
| Phase 3 | Integration tests | All API endpoints tested |
| Phase 4 | E2E tests | Critical flows pass |

### Test Coverage Targets

| Layer | Target | Actual |
|-------|--------|--------|
| Unit | 80% | TBD |
| Integration | 100% endpoints | TBD |
| E2E | Critical flows | TBD |
```

### Phase 11: Rollout Strategy

```markdown
## Rollout Strategy

### Pre-deployment
- [ ] All tests pass in staging
- [ ] Database backup created
- [ ] Feature flag configured (disabled)
- [ ] Monitoring alerts set up

### Deployment Steps
1. Apply database migrations
2. Deploy code changes
3. Verify health checks
4. Enable feature flag (10% users)
5. Monitor error rates (30 minutes)
6. Gradual rollout (25% → 50% → 100%)

### Rollback Plan
1. Disable feature flag (immediate)
2. Revert code deployment (if needed)
3. Rollback migrations (if needed)

### Success Criteria
- Error rate < 0.1%
- Response time < 500ms p95
- No critical bugs in 24 hours
```

---

## Templates

### Full Implementation Plan Template v2.0

```markdown
# Implementation Plan: [Feature Name]

**Version:** 1.0
**Design:** `{FEATURE_DIR}/design.md`
**Status:** Draft | In Progress | Complete
**Author:** [Name]
**Date:** YYYY-MM-DD
**Project:** [project-name]

---

## Reference Documents

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Standards |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X requirements |
| Design | `{FEATURE_DIR}/design.md` | AD-X decisions |
| Contracts | `.aidocs/contracts.md` | API patterns |

---

## Overview

[1-2 paragraphs summarizing implementation approach and key decisions]

**Estimated Effort:** [X days]
**Critical Path:** [X days]
**Waves:** [N waves]
**Total Tasks:** [M tasks]

---

## Prerequisites

### Infrastructure
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

### Environment
- [ ] [Prerequisite 1]

### Code Dependencies
- [ ] [Prerequisite 1]

---

## Dependency Graph

```
[Visual representation of task dependencies]
```

---

## Wave Analysis

| Wave | Tasks | Parallel | Dependencies | Effort |
|------|-------|----------|--------------|--------|
| 1 | TASK-001, TASK-002 | Yes | None | X hours |
| 2 | TASK-003, TASK-004 | Yes | Wave 1 | X hours |
| 3 | TASK-005 | No | Wave 2 | X hours |

**Wave Diagram:**
```
[Visual wave diagram]
```

---

## Phases

| Phase | Description | Tasks | Effort |
|-------|-------------|-------|--------|
| 1 | [Phase name] | TASK-001, TASK-002 | X days |
| 2 | [Phase name] | TASK-003, TASK-004 | X days |

---

## Phase 1: [Phase Name]

### TASK-001: [Task Title]

**Wave:** 1
**Complexity:** simple | normal | complex
**Effort:** X hours
**Context:** ~Xk tokens

**Description:**
[2-3 sentences]

**Traces to:** AD-001, FR-001

**Depends on:** None
**Blocks:** TASK-003, TASK-004

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Files:**
| Action | File | Description |
|--------|------|-------------|
| CREATE | `path/file.ts` | Description |

**Tests:**
- [ ] Unit: [description]
- [ ] Integration: [description]

---

### TASK-002: [Task Title]
...

---

## Phase 2: [Phase Name]

### TASK-003: [Task Title]
...

---

## Critical Path

```
[Critical path visualization]
```

**Duration:** X days
**Tasks on Critical Path:** TASK-001 → TASK-003 → TASK-005

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Strategy] |

**Contingency Buffer:** X% added to estimates

---

## Testing Plan

### Per-Phase Testing
| Phase | Tests | Pass Criteria |
|-------|-------|---------------|
| 1 | [Tests] | [Criteria] |

### Coverage Targets
| Layer | Target |
|-------|--------|
| Unit | 80%+ |
| Integration | 100% endpoints |
| E2E | Critical flows |

---

## Rollout Strategy

### Pre-deployment
- [ ] [Checklist item]

### Deployment Steps
1. [Step 1]
2. [Step 2]

### Rollback Plan
1. [Rollback step]

### Success Criteria
- [Metric 1]
- [Metric 2]

---

## Recommended Skills & Methodologies

### Skills
| Skill | Tasks | Purpose |
|-------|-------|---------|
| faion-software-developer | TASK-001 to TASK-005 | Core implementation |
| faion-devops-engineer | TASK-006 | Deployment |

### Methodologies
| ID | Name | Relevant Tasks |
|----|------|----------------|
| M-DEV-XXX | [Name] | TASK-001, TASK-002 |

---

## Open Questions

- [ ] [Question to resolve]

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| YYYY-MM-DD | 1.0 | Initial plan |
```

---

## Quality Checklist

### Implementation Plan Quality Gate

**Completeness:**
- [ ] All AD-X from design have corresponding tasks
- [ ] All file changes from design are assigned to tasks
- [ ] Prerequisites fully documented
- [ ] Testing plan covers all phases

**Structure:**
- [ ] Tasks follow INVEST criteria
- [ ] Dependencies clearly documented (FS/SS/FF/SF)
- [ ] Effort estimates provided
- [ ] Context budget < 100k per task

**Parallelization:**
- [ ] Dependency graph documented
- [ ] Waves identified
- [ ] Critical path calculated
- [ ] Parallel opportunities maximized

**Risk:**
- [ ] Risks identified with mitigations
- [ ] Rollout strategy defined
- [ ] Rollback plan documented
- [ ] Contingency buffer added

**Traceability:**
- [ ] Each task traces to AD-X
- [ ] Each task traces to FR-X
- [ ] Skills/methodologies recommended

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Tasks too large | Break down to < 4 hours, < 100k tokens |
| Missing dependencies | Every task needs explicit "Depends on" |
| No acceptance criteria | Each task needs testable criteria |
| Forgetting tests | Include test tasks in plan |
| No rollback plan | Always plan for failure |
| No wave analysis | Identify parallel opportunities |
| Tasks not traced | Every task must trace to AD-X |
| Missing context estimate | AI needs token budget |

---

## Related Methodologies

- **writing-design-documents:** Writing Design Documents
- **task-creation-parallelization:** Task Creation & Parallelization
- **wbs-decomposition:** WBS Decomposition
- **dependency-management:** Dependency Management
- **risk-assessment:** Risk Assessment
- **schedule-management:** Schedule Management
- **backlog-management:** INVEST Principle
- **testing-strategy:** Testing Strategy

---

## Agent

**faion-impl-plan-reviewer-agent** reviews implementation plans. Invoke with:
- "Review this implementation plan"
- "Break down this design into tasks"
- "Analyze dependency graph for parallelization"
- "Calculate critical path"

---

*Methodology | SDD Foundation | Version 2.0.0*
*Integrates PM, BA, PdM, Dev best practices*
