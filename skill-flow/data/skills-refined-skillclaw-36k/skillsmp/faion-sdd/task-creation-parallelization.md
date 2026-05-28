---
id: task-creation-parallelization
name: "Task Creation & Parallelization"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Task Creation & Parallelization

## Metadata

| Field | Value |
|-------|-------|
| **ID** | task-creation-parallelization |
| **Version** | 2.1.0 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #tasks, #parallelization, #decomposition |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-task-creator-agent, faion-task-executor-agent |

---

## Problem

Implementation plans become bottlenecks when:
- Tasks are executed sequentially when they could run in parallel
- Task granularity is wrong (too big or too small)
- Dependencies are unclear or circular
- Progress is hard to track
- Tasks lack context for AI/human execution
- No traceability to requirements or design decisions

**The root cause:** Poor task decomposition, missing context, and inadequate dependency analysis.

---

## Integrated Best Practices

This methodology integrates principles from:

| Domain | Methodology | Key Principle |
|--------|-------------|---------------|
| **BA** | smart-requirements | SMART criteria for requirements |
| **BA** | acceptance-criteria | Given-When-Then acceptance criteria |
| **BA** | requirements-traceability | Requirements traceability (FR-X, AD-X links) |
| **PM** | wbs-decomposition | WBS decomposition (8-80 rule, 100% rule) |
| **PM** | dependency-management | Dependency types (FS, SS, FF, SF) |
| **PdM** | backlog-management | INVEST principle for task quality |
| **SDD** | writing-specifications | Spec → Task traceability |
| **SDD** | writing-design-documents | Design → Task traceability |

---

## Framework

### 1. Task Decomposition Principles

#### 1.1 Right Size (Project Management Framework 8-80 Rule Adapted)

| Complexity | Effort | Tokens | Description |
|------------|--------|--------|-------------|
| **simple** | 1-2h | <30k | Single file, clear pattern |
| **normal** | 2-3h | 30-60k | Multiple files, some decisions |
| **complex** | 3-4h | 60-100k | Architecture decisions, research needed |

**Maximum:** 4 hours / 100k tokens per task (single work session)

**Too big:** "Implement authentication" (multiple days)
**Too small:** "Add import statement" (minutes)
**Right size:** "Create password hashing utilities" (2-3 hours)

#### 1.2 INVEST Principle (from backlog-management)

Each task must be:

| Criterion | Question | Example |
|-----------|----------|---------|
| **Independent** | Can be done without other tasks? | ✅ Password utils (no deps) |
| **Negotiable** | Details can be refined? | ✅ Algorithm choice negotiable |
| **Valuable** | Clear user/business value? | ✅ "Enables secure login" |
| **Estimable** | Can estimate effort? | ✅ "2-3 hours" |
| **Small** | Fits in 1-4 hours? | ✅ Not "build auth system" |
| **Testable** | Clear acceptance criteria? | ✅ Given-When-Then defined |

#### 1.3 Clear Boundaries

Each task must define:
- **Input:** What exists before (files, data, dependencies)
- **Output:** What exists after (files created/modified, features)
- **Success criteria:** How to verify completion (tests, AC)

#### 1.4 SMART Criteria (from smart-requirements)

| Criterion | Application |
|-----------|-------------|
| **Specific** | Only one interpretation of task |
| **Measurable** | Can verify completion objectively |
| **Achievable** | Technically feasible with given context |
| **Relevant** | Traces to business need (FR-X) |
| **Time-bound** | Effort estimate provided |

### 2. Traceability (from requirements-traceability)

Every task must link to:

```
TASK → FR-X (spec.md) → AD-X (design.md)
```

| Link Type | What It Answers |
|-----------|-----------------|
| **FR-X** | WHY this task exists (user need) |
| **AD-X** | HOW to implement (architecture decision) |
| **NFR-X** | Constraints (performance, security) |

**Template:**
```markdown
## Requirements Coverage
### FR-2: User can log in with email/password
Full text of requirement from spec.md

## Architecture Decisions
### AD-1: JWT for authentication
Full text of decision from design.md
```

### 3. Acceptance Criteria (from acceptance-criteria)

Use Given-When-Then (BDD) format:

```markdown
## Acceptance Criteria

**AC-1: Successful login**
- Given: registered user with valid credentials
- When: user submits login form
- Then: JWT token returned, user redirected to dashboard

**AC-2: Invalid password**
- Given: registered user with wrong password
- When: user submits login form
- Then: error message "Invalid credentials" displayed
```

**Coverage checklist:**
- [ ] Happy path (success scenario)
- [ ] Alternative paths (valid variations)
- [ ] Boundary conditions (limits, edge cases)
- [ ] Error handling (invalid inputs, failures)
- [ ] Security (unauthorized access)
- [ ] Performance (if NFR applies)

### 4. Dependency Analysis

#### 4.1 Dependency Types (from dependency-management)

| Type | Meaning | Example |
|------|---------|---------|
| **FS** | Finish-to-Start | User model must finish before login handler starts |
| **SS** | Start-to-Start | Frontend and API can start together |
| **FF** | Finish-to-Finish | Tests must finish when code finishes |
| **SF** | Start-to-Finish | Rare, migration starts when old code finishes |

#### 4.2 Create Task Graph

Draw tasks as nodes, dependencies as arrows:

```
TASK-001 (DB Tables)
    ↓ [FS]
TASK-003 (User Model) ────→ TASK-005 (Register Handler)
    ↓ [FS]                        ↓ [FS]
TASK-002 (Password Utils) → TASK-004 (JWT Utils) → TASK-006 (Login Handler)
```

#### 4.3 Identify Parallel Paths

Tasks without arrows between them can run in parallel:

**Can parallelize:**
- TASK-001 (DB) and TASK-002 (Password Utils) - no dependency
- TASK-003 (Model) and TASK-004 (JWT Utils) - both depend on TASK-001

**Cannot parallelize:**
- TASK-005 and TASK-003 - TASK-005 needs TASK-003

#### 4.4 Calculate Critical Path

The longest chain determines minimum time:

```
Path A: TASK-001 → TASK-003 → TASK-005 = 6 hours
Path B: TASK-001 → TASK-004 → TASK-006 = 5 hours
Path C: TASK-002 → TASK-004 → TASK-006 = 4 hours

Critical path: A (6 hours minimum)
```

### 5. Wave-Based Task Creation

**Principle:** Create tasks in waves based on dependency graph, not all at once.

#### 5.1 Why Waves?

| Approach | Problem |
|----------|---------|
| All tasks at once | Later tasks lack context from completed tasks |
| Sequential creation | Slow, no parallelization |
| **Wave-based** | Balance: create parallel tasks together, incorporate learnings |

#### 5.2 Wave Creation Process

```
1. Analyze dependency graph
2. Identify Wave 1 tasks (no dependencies)
3. Create Wave 1 tasks with full detail
4. Execute Wave 1
5. Update context with learnings
6. Create Wave 2 tasks (depend on Wave 1)
7. Repeat until all tasks created
```

**Example:**
```
Wave 1 Creation: [TASK-001, TASK-002] - both have no dependencies
    ↓ execute
Wave 2 Creation: [TASK-003, TASK-004] - depend on Wave 1
    ↓ execute
Wave 3 Creation: [TASK-005, TASK-006] - depend on Wave 2
```

#### 5.3 Benefits of Wave Creation

| Benefit | Description |
|---------|-------------|
| **Incremental context** | Later tasks incorporate learnings from earlier waves |
| **Pattern discovery** | Wave 1 establishes patterns used in later waves |
| **Reduced rework** | Don't create tasks that may change after discoveries |
| **Better estimates** | Real effort data improves later estimates |

#### 5.4 When to Create All Tasks at Once

Sometimes all tasks should be created upfront:
- Small feature (< 6 tasks)
- Well-understood domain with clear patterns
- Need full scope estimate for planning
- Team needs parallel assignment immediately

### 6. Context Management (for AI Execution)

#### 6.1 Context Budget

| Phase | Budget | Purpose |
|-------|--------|---------|
| **SDD Docs** | 15% | constitution, spec, design |
| **Task Tree** | 10% | completed dependency tasks |
| **Research** | 25% | existing code patterns |
| **Implementation** | 40% | actual coding |
| **Testing** | 10% | verification |

**Total:** <100k tokens per task

#### 6.2 Reference Documents with Task Dependency Tree

**CRITICAL:** Each task MUST include the full dependency tree of completed tasks.

```markdown
## SDD References

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Code standards |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X, FR-Y |
| Design | `{FEATURE_DIR}/design.md` | AD-X, AD-Y |
| Contracts | `.aidocs/contracts.md` | (if API) |

## Task Dependency Tree

**This task depends on:**

```
TASK-001 (DB Tables) ─────────────────────┐
    Summary: Created users, sessions tables│
    Files: migrations/001_*.py            │
    Patterns: AlterField for nullable     │
                                          ↓
TASK-003 (User Model) ──────────→ TASK-005 (THIS TASK)
    Summary: User model with validation
    Files: models/user.py
    Patterns: BaseModel, email validator
    Key code:
    ```python
    class User(BaseModel):
        email = models.EmailField(unique=True)
    ```
```

**Read these task summaries before starting:**
- `{TASKS_DIR}/done/TASK_001_db_tables.md` → Summary section
- `{TASKS_DIR}/done/TASK_003_user_model.md` → Summary section

## Recommended Skills

| Skill | When to Use |
|-------|-------------|
| faion-software-developer | Code implementation |
| faion-devops-engineer | CI/CD, Docker, infra |
| faion-ml-engineer | AI/LLM integration |

## Recommended Methodologies

| ID | Name | Purpose |
|----|------|---------|
| code-review | Python Best Practices | Code standards |
| shadcn-ui-components | shadcn/ui Components | UI implementation |
| docker-patterns | Docker Patterns | Containerization |
```

#### 6.3 Task Tree Content Requirements

For each completed dependency task, include:

| Field | Purpose | Example |
|-------|---------|---------|
| **Summary** | What was done | "Created User model with email validation" |
| **Files** | What was created/modified | `models/user.py`, `migrations/002_*.py` |
| **Patterns** | Reusable patterns discovered | "BaseModel inheritance", "email validator" |
| **Key code** | Critical code snippets | Class definition, key functions |
| **Decisions** | Implementation decisions made | "Used UUID for PK instead of auto-increment" |

#### 6.4 Why Task Tree is Critical

| Without Task Tree | With Task Tree |
|-------------------|----------------|
| Agent re-discovers patterns | Agent reuses established patterns |
| Inconsistent implementations | Consistent code style |
| Duplicate research effort | Builds on prior work |
| Context wasted on discovery | Context used for implementation |
| May contradict earlier tasks | Aligned with earlier decisions |

### 6. Risk & Blocker Pre-identification

```markdown
## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| API rate limits | Medium | High | Implement retry with backoff |
| Schema migration fails | Low | High | Test on staging first |

## Potential Blockers
- [ ] External API access required (need credentials)
- [ ] Design decision AD-3 unclear (ask PO)
```

### 7. Task States

```
BACKLOG → TODO → IN_PROGRESS → DONE
                      ↓
                  BLOCKED
```

| State | Meaning | Action |
|-------|---------|--------|
| BACKLOG | Future work, not prioritized | Grooming needed |
| TODO | Ready to start, deps met | Can pick up |
| IN_PROGRESS | Being worked on | Single assignee |
| BLOCKED | Cannot proceed | Document blocker |
| DONE | Completed, verified | Move to done/ |

---

## Templates

### Enhanced Task Template v2.0

```markdown
# TASK_XXX: {Title}
<!-- SUMMARY: {One sentence business value} -->

## Metadata
| Field | Value |
|-------|-------|
| **Complexity** | simple / normal / complex |
| **Effort** | X hours |
| **Priority** | P0 / P1 / P2 |
| **Created** | YYYY-MM-DD |
| **Project** | {project} |
| **Feature** | {feature} |

---

## SDD References

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Code standards |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X, FR-Y |
| Design | `{FEATURE_DIR}/design.md` | AD-X, AD-Y |
| Contracts | `.aidocs/contracts.md` | (if API) |

## Task Dependency Tree

**This task depends on:** (read summaries before starting)

```
TASK_YYY ({title}) ────────────────────────┐
    Status: DONE                           │
    Summary: {what was done}               │
    Files: {files created/modified}        │
    Patterns: {patterns to follow}         │
    Key decisions: {decisions made}        ↓
                                     TASK_XXX (THIS TASK)
TASK_ZZZ ({title}) ────────────────────────┘
    Status: DONE
    Summary: {what was done}
    Files: {files created/modified}
    Key code:
    ```{lang}
    {critical code snippet}
    ```
```

**Dependency task files:**
- `{TASKS_DIR}/done/TASK_YYY_{slug}.md` → Read Summary section
- `{TASKS_DIR}/done/TASK_ZZZ_{slug}.md` → Read Summary section

## Recommended Skills & Methodologies

**Skills:**
| Skill | Purpose |
|-------|---------|
| faion-{skill} | {When to use} |

**Methodologies:**
| ID | Name | Purpose |
|----|------|---------|
| M-XXX-YYY | {Name} | {How it helps} |

---

## Requirements Coverage

### FR-X: {requirement title}
{Full text of requirement from spec.md}

### NFR-X: {non-functional requirement}
{Full text if applicable}

## Architecture Decisions

### AD-X: {decision title}
{Full text of decision from design.md}

---

## Description

{Clear description of what needs to be done, 2-4 sentences}

**Business value:** {From spec.md problem statement}

---

## Context

### Related Files (from research)
| File | Purpose | Patterns to Follow |
|------|---------|-------------------|
| `path/to/similar.py` | Similar implementation | Pattern X, Y |

### Code Dependencies
- `module.Class` - {why needed}
- `library` - {version constraint if any}

---

## Goals

1. {Specific, measurable goal}
2. {Specific, measurable goal}
3. {Specific, measurable goal}

---

## Acceptance Criteria

**AC-1: {Scenario name}**
- Given: {precondition}
- When: {action}
- Then: {expected result}

**AC-2: {Scenario name}**
- Given: {precondition}
- When: {action}
- Then: {expected result}

---

## Dependencies

**Depends on (FS = Finish-to-Start):**
- TASK_YYY [FS] - {reason}

**Blocks:**
- TASK_ZZZ - {reason}

---

## Files to Change

| Action | File | Scope |
|--------|------|-------|
| CREATE | `path/to/new_file.py` | {description} |
| MODIFY | `path/to/existing.py` | {what changes} |

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk description} | Low/Med/High | Low/Med/High | {Mitigation strategy} |

## Potential Blockers
- [ ] {Blocker description}

---

## Out of Scope

- {Explicit exclusion 1}
- {Explicit exclusion 2}

---

## Testing

| Type | Description | File |
|------|-------------|------|
| Unit | {What to test} | `tests/unit/test_*.py` |
| Integration | {What to test} | `tests/integration/test_*.py` |

---

## Estimated Context

| Phase | Tokens | Notes |
|-------|--------|-------|
| SDD Docs | ~Xk | constitution, spec, design |
| Research | ~Xk | existing patterns |
| Implementation | ~Xk | coding |
| Testing | ~Xk | verification |
| **Total** | ~Xk | Must be <100k |

---

## Subtasks

- [ ] 01. Research: {description}
- [ ] 02. Implement: {description}
- [ ] 03. Test: {description}
- [ ] 04. Verify: {description}

---

## Implementation
<!-- Filled by executor during execution -->

### Subtask 01: Research
{Findings, patterns discovered}

### Subtask 02: Implement
{Key decisions, code written}

---

## Summary
<!-- Filled after completion -->

**Completed:** YYYY-MM-DD

**What was done:**
- {Achievement 1}
- {Achievement 2}

**Key decisions:**
- {Decision and rationale}

**Files changed:**
- `path/file.py` (CREATE, X lines)
- `path/file2.py` (MODIFY, +Y lines)

**Test results:**
- All tests pass
- Coverage: X%

---

## Lessons Learned
<!-- Optional: patterns/mistakes for ~/.sdd/memory/ -->

**Patterns:**
- {Reusable pattern discovered}

**Mistakes:**
- {What went wrong and fix}
```

### Task List Template

```markdown
# Tasks: {Feature Name}

## Summary

| Total | TODO | In Progress | Done | Blocked |
|-------|------|-------------|------|---------|
| 12 | 8 | 2 | 2 | 0 |

## Dependency Graph

```
TASK-001 ──[FS]──→ TASK-003 ──[FS]──→ TASK-005
    │                  │                  │
    ↓                  ↓                  ↓
TASK-002 ──[FS]──→ TASK-004 ──[FS]──→ TASK-006
```

## Parallel Waves

**Wave 1 (can start immediately):**
- TASK-001: Database setup (2h)
- TASK-002: Password utilities (2h)

**Wave 2 (after Wave 1):**
- TASK-003: User model (2h)
- TASK-004: JWT utilities (2h)

**Wave 3 (after Wave 2):**
- TASK-005: Register handler (2h)
- TASK-006: Login handler (2h)

**Critical Path:** Wave 1 → Wave 2 → Wave 3 = 6h minimum

## Task List by State

### TODO
| ID | Title | Effort | Deps | Skills |
|----|-------|--------|------|--------|
| TASK-001 | Database setup | 2h | - | faion-devops |

### IN_PROGRESS
| ID | Title | Assignee | Started |
|----|-------|----------|---------|
| TASK-003 | User model | Dev A | 2026-01-19 |

### DONE
| ID | Title | Completed |
|----|-------|-----------|
| - | - | - |
```

---

## Examples

### Example: Auth Feature Decomposition

**Bad:**
```
TASK-001: Build authentication system (8 hours)
```
Problem: Too vague, can't track, can't parallelize.

**Good:**
```
TASK-001: Create users table migration (1h) - simple
TASK-002: Create sessions table migration (1h) - simple
TASK-003: Implement password hashing (2h) - normal, code-review
TASK-004: Implement JWT utilities (2h) - normal
TASK-005: Create User model with validation (2h) - normal
TASK-006: Create Session model (1h) - simple
TASK-007: Implement register handler (2h) - normal, FR-1
TASK-008: Implement login handler (2h) - normal, FR-2
TASK-009: Implement logout handler (1h) - simple, FR-3
TASK-010: Implement auth middleware (2h) - normal, AD-1
TASK-011: Write unit tests (2h) - normal, testing-strategy
TASK-012: Write integration tests (2h) - normal
```

**Parallelization waves:**
```
Wave 1 (Day 1 AM):  [TASK-001, TASK-002, TASK-003, TASK-004]
Wave 2 (Day 1 PM):  [TASK-005, TASK-006]
Wave 3 (Day 2 AM):  [TASK-007, TASK-008]
Wave 4 (Day 2 PM):  [TASK-009, TASK-010]
Wave 5 (Day 3):     [TASK-011, TASK-012]

Result: 22h of work in 2.5 days with proper parallelization
```

---

## Common Mistakes

| Mistake | Fix | Methodology |
|---------|-----|-------------|
| Tasks too large | Break down until < 4 hours | task-creation-parallelization |
| No traceability | Add FR-X, AD-X links | requirements-traceability |
| Vague acceptance criteria | Use Given-When-Then | acceptance-criteria |
| Hidden dependencies | List ALL dependencies explicitly | dependency-management |
| Circular dependencies | Redesign - split shared logic | wbs-decomposition |
| No context for AI | Add SDD References section | task-creation-parallelization |
| Missing skills recommendation | Add Recommended Skills | task-creation-parallelization |
| No risk assessment | Add Risks & Mitigations | risk-management |
| Sequential by default | Analyze for parallelization | task-creation-parallelization |
| Forgetting tests | Include testing in AC | acceptance-criteria |

---

## Quality Checklist

### Before Creating Task
- [ ] Implementation plan reviewed (writing-implementation-plans)
- [ ] Design decisions (AD-X) understood
- [ ] Requirements (FR-X) mapped

### Task Definition
- [ ] INVEST criteria met
- [ ] SMART criteria met
- [ ] Complexity/effort assigned
- [ ] SDD references included
- [ ] Recommended skills listed

### Acceptance Criteria
- [ ] Given-When-Then format
- [ ] Happy path covered
- [ ] Error cases covered
- [ ] Boundary conditions covered
- [ ] Testable (not vague)

### Dependencies
- [ ] All dependencies explicit (FS/SS/FF)
- [ ] No circular dependencies
- [ ] Blocking tasks identified

### Context
- [ ] Related files identified
- [ ] Code patterns documented
- [ ] Token estimate <100k
- [ ] Risks pre-identified

### Traceability
- [ ] Links to FR-X (spec)
- [ ] Links to AD-X (design)
- [ ] Links to NFR-X (if applicable)

---

## Related Methodologies

| ID | Name | Relationship |
|----|------|--------------|
| writing-specifications | Writing Specifications | Source of FR-X requirements |
| writing-design-documents | Writing Design Documents | Source of AD-X decisions |
| writing-implementation-plans | Writing Implementation Plans | Input for task creation |
| quality-gates-confidence | Quality Gates | Task review checkpoints |
| smart-requirements | Requirements Documentation | SMART criteria |
| requirements-traceability | Requirements Traceability | FR-X linking |
| acceptance-criteria | Acceptance Criteria | Given-When-Then format |
| wbs-decomposition | Work Breakdown Structure | Decomposition principles |
| dependency-management | Schedule Development | Dependency types |
| backlog-management | Backlog Management | INVEST principle |

---

## Agents

**faion-task-creator-agent:**
- Creates detailed TASK_*.md files from implementation plans
- Researches existing code patterns
- Identifies recommended skills and methodologies
- Triggers: "Create tasks", "Break down feature"

**faion-task-executor-agent:**
- Executes single task autonomously
- Loads SDD context before execution
- Documents implementation and summary
- Triggers: "Execute task", "Run next task"

---

*Methodology | SDD Foundation | Version 2.1.0*
*Integrates: BA (smart-requirements/005/014), PM (wbs-decomposition/004), PdM (backlog-management)*
