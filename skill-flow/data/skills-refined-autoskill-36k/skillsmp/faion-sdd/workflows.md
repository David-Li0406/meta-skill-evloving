# SDD Workflow Instructions

Detailed step-by-step instructions for each SDD phase. Reference this when executing specific workflows.

---

## Table of Contents

1. [Writing Constitutions](#1-writing-constitutions)
2. [Writing Specifications](#2-writing-specifications)
3. [Writing Design Documents](#3-writing-design-documents)
4. [Writing Implementation Plans](#4-writing-implementation-plans)
5. [Task Creation](#5-task-creation)
6. [Task Execution](#6-task-execution)
7. [Batch Execution](#7-batch-execution)
8. [Parallelization Analysis](#8-parallelization-analysis)
9. [Backlog Grooming](#9-backlog-grooming)
10. [Roadmapping](#10-roadmapping)
11. [Quality Gates](#11-quality-gates)
12. [Confidence Checks](#12-confidence-checks)
13. [Reflexion Learning](#13-reflexion-learning)

---

## 1. Writing Constitutions

### Philosophy

Constitution.md defines immutable project principles for ALL features. Two modes:
1. **Existing Project** - codebase analysis
2. **New Project** - Socratic dialogue

### MODE 1: Existing Project Workflow

```
Detect -> Analyze Structure -> Tech Stack -> Patterns -> Draft -> Review
```

**Step 1: Analyze Codebase**
- Directory layout, CLAUDE.md, README.md
- Config files (pyproject.toml, package.json)
- Architecture patterns, naming conventions
- Linter configs, testing setup

**Step 2: Present Findings**
```markdown
**Analysis:**
1. Tech: Python 3.11, Django 4.2, PostgreSQL
2. Architecture: Layered (views -> services -> models)
3. Standards: black + isort + flake8
Does this match? What to change?
```

**Step 3: Draft and Review**

### MODE 2: New Project Workflow

```
Vision -> Tech Choices -> Architecture -> Standards -> Draft -> Review
```

**Step 1: Vision (Socratic)**
"Tell me about the project. What problem does it solve?"
Apply Five Whys to get to real need.

**Step 2: Tech Choices (Alternatives)**
For each decision, present A/B/C with pros/cons:
- Backend: Django vs FastAPI vs NestJS
- Database: PostgreSQL vs MongoDB vs SQLite

**Step 3: Architecture Trade-offs**
- Monolith vs Microservices
- REST vs GraphQL
- ORM vs Raw SQL

**Step 4: Standards**
- Linter, formatter, type hints
- Testing coverage, CI/CD
- Git conventions

### Save Location

```bash
mkdir -p .aidocs/{backlog,todo,in-progress,done}
# Write constitution.md to .aidocs/
```

Create CLAUDE.md navigation hub in project folder.

### Anti-patterns

- Copying without understanding
- Over-engineering at start
- Ignoring team expertise

---

## 2. Writing Specifications

### Philosophy

- **Intent is source of truth** - spec is main artifact
- **Socratic dialogue** - user formulates requirements through questions
- **Brainstorming** - iterative refinement via alternatives

### Workflow

```
BRAINSTORM -> RESEARCH -> CLARIFY -> DRAFT -> REVIEW -> SAVE
```

### Phase 1: Brainstorming

Start: "Tell me about the problem. Who suffers and how?"

**Five Whys** - for each answer ask "Why?":
```
"Need export" -> Why? -> "Managers ask" -> Why? -> "No access" -> Real problem: UX
```

**Alternatives** - for each idea:
```markdown
**A:** {approach 1}
- Pros: {benefits}
- Cons: {drawbacks}

**B:** {approach 2}
- Pros: {benefits}
- Cons: {drawbacks}

Which is closer?
```

**Challenge assumptions:**
- "Is this needed for v1?"
- "What if we DON'T do this?"
- "What exists in codebase?"

### Phase 2: Research Codebase

Search: `Glob **/models.py`, `Grep class.*Model`, `Glob **/.aidocs/**/spec.md`

Share findings: "Found existing export in services.py. Does this affect approach?"

### Phase 3: Clarify Details

**User stories workshop:**
```markdown
As {role}, I want {goal}, so that {benefit}.
- How often?
- What happens if can't do this?
```

**Edge cases through questions** (not assumptions):
- "What if data invalid?"
- "What if 1000+ records?"
- "What if service unavailable?"

### Phase 4: Draft Section by Section

Each section -> show -> validate -> next:

1. Problem Statement -> "Correct?"
2. User Stories with AC -> "Complete?"
3. Functional Requirements -> "Anything redundant?"
4. Out of Scope -> "Agree with boundaries?"

### Phase 5: Review

**Checklist:**
- [ ] Problem clear (SMART)
- [ ] User Stories specific (INVEST)
- [ ] Requirements testable
- [ ] Out of Scope defined

Call `faion-sdd-reviewer-agent (mode: spec)` before save.

### Phase 6: Save

**New feature:** `.aidocs/features/backlog/{NN}-{feature}/spec.md`
**Active feature:** update existing spec.md

### Anti-patterns

- Assumptions instead of questions
- Solution before problem
- Large blocks without validation
- Ignoring "I don't know"

---

## 3. Writing Design Documents

### Prerequisites

1. `spec.md` exists with status `approved`
2. `constitution.md` exists at `.aidocs/constitution.md`
3. `contracts.md` exists (for API features)

### Workflow

```
READ SPEC -> READ CONSTITUTION -> RESEARCH -> DECISIONS -> APPROACH -> TESTING -> RISKS -> REVIEW -> SAVE
```

### Phase 1: Read Specification

Extract from spec.md:
- Problem Statement
- User Stories
- Functional Requirements
- API Contract (if present)
- Data Model (if present)
- Out of Scope

### Phase 2: Read Constitution

Extract from constitution.md:
- Architecture patterns
- Code standards
- Testing requirements

### Phase 3: Read API Contracts (if API feature)

**IMPORTANT:** Do NOT redefine API endpoints in design.md. Reference contracts.md:
```markdown
## API Endpoints

This feature implements endpoints from [contracts.md](../../contracts.md):
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
```

### Phase 4: Research Codebase

Use Grep and Glob to find:
- Similar models
- Similar services
- Similar views
- Existing patterns

Determine:
- Reusable components
- Patterns in use
- Where to place new code

### Phase 5: Architecture Decisions

For each key decision:
1. Define context - what problem solving
2. List options - minimum 2 alternatives
3. Choose solution - which and why
4. Document rationale

### Phase 6: Define Technical Approach

1. **Components** - new components, interactions
2. **Data Flow** - data path, validation, error handling
3. **Files** - CREATE and MODIFY lists with scope

### Phase 7: Define Testing Strategy

Based on constitution:
1. Unit tests - isolated testing targets
2. Integration tests - flow coverage
3. Test data - required fixtures

### Phase 8: Identify Risks

For each risk:
- Description
- Impact (High/Medium/Low)
- Mitigation strategy

### Phase 9: Review with User

Present key decisions:
1. Architecture Decisions - agreement check
2. Technical Approach - better alternatives?
3. Risks - completeness check

### Phase 10: Agent Review

Call `faion-sdd-reviewer-agent (mode: design)`. Checks:
- FR coverage
- AD structure (context, options, rationale)
- Constitution compliance
- Files list completeness

### Phase 11: Save

Save to: `{feature_path}/design.md`

---

## 4. Writing Implementation Plans

### Key Principle

**Each task MUST fit 100k token context** = atomic, single-agent executable.

### Workflow

```
LOAD CONTEXT -> ANALYZE COMPLEXITY -> DEFINE WORK UNITS -> APPLY 100k RULE -> DEPENDENCIES -> DRAFT -> REVIEW -> SAVE
```

### Phase 1: Load Context

Read: `constitution.md`, `spec.md`, `design.md`

### Phase 2: Analyze Complexity

For each file in design.md:

| File | Action | Complexity | Est. Tokens |
|------|--------|------------|-------------|
| models.py | CREATE | High | 40k |
| services.py | CREATE | High | 50k |

**Factors:** LOC, dependencies, business logic, tests

### Phase 3: Define Work Units

Group related work:
```markdown
## Work Unit 1: Data Layer
- models.py (CREATE)
Est: 40k tokens
```

### Phase 4: Apply 100k Rule

```
Research: ~20k (read existing code)
Task file: ~5k
Implementation: ~50k
Buffer: ~25k
TOTAL < 100k
```

**If > 100k:** Split into smaller tasks.

### Phase 5: Map Dependencies

| Task | Depends On | Enables |
|------|------------|---------|
| TASK_001 | - | TASK_003 |
| TASK_002 | - | TASK_003 |
| TASK_003 | 001, 002 | - |

Rules: No cycles, maximize parallelization.

### Phase 6: Draft

Show section by section:
- Overview (total tasks, critical path, est. tokens)
- Tasks list (files, deps, FR/AD coverage, AC)
- Execution order (phases, parallel/sequential)

### Phase 7: Review

Call `faion-sdd-reviewer-agent (mode: plan)`. Checks: 100k compliance, deps, coverage.

### Phase 8: Save

`.aidocs/features/{feature}/implementation-plan.md`

---

## 5. Task Creation

### Workflow

```
1. Load SDD documents
   |
2. Verify: spec approved? design approved?
   |
3. Check/create implementation-plan
   |
4. For each task in plan:
   -> Call faion-task-creator-agent
   |
5. Run faion-sdd-reviewer-agent (mode: tasks) (4-pass)
   |
6. Report results
```

### Document Verification

Check these files exist and are approved:
```
.aidocs/features/{status}/{feature}/spec.md
.aidocs/features/{status}/{feature}/design.md
.aidocs/features/{status}/{feature}/implementation-plan.md
```

If implementation-plan missing: Create it first using workflow #4.

### Task Creation Call

```python
Task(
    subagent_type="faion-task-creator-agent",
    description=f"Create {task_name}",
    prompt=f"""
PROJECT: {project}
FEATURE: {feature}
TASK_INFO: {task_from_plan}
SDD_PATH: .aidocs/features/{status}/{feature}/

Create comprehensive task file with:
- Clear objective
- Acceptance criteria (AC-XX.X)
- Technical approach
- Files to modify
- Dependencies
- Estimated complexity

Research codebase deeply before writing.
"""
)
```

### Task Review (4-Pass)

```python
Task(
    subagent_type="faion-sdd-reviewer-agent",
    prompt=f"""
MODE: tasks
PROJECT: {project}
FEATURE: {feature}

Multi-pass review:
Pass 1: Completeness - all plan items covered?
Pass 2: Consistency - no contradictions?
Pass 3: Coverage - all requirements addressed?
Pass 4: Executability - can be implemented as written?
"""
)
```

---

## 6. Task Execution

### Workflow

```
1. Parse project, feature, task_name
   |
2. Find task file in todo/ or in-progress/
   |
3. Load SDD context (constitution, spec, design, impl-plan)
   |
4. Call faion-task-executor-agent
   |
5. Report results
```

### Task Resolution

Search order:
1. `tasks/in-progress/TASK_*{name}*.md`
2. `tasks/todo/TASK_*{name}*.md`

Partial match supported: "TASK_001", "001", "models"

### Context Loading

Load these files:
```
.aidocs/constitution.md
.aidocs/features/{status}/{feature}/spec.md
.aidocs/features/{status}/{feature}/design.md
.aidocs/features/{status}/{feature}/implementation-plan.md
{task_file}
```

### Task Lifecycle

```
tasks/todo/TASK_XXX.md
       | (start execution)
tasks/in-progress/TASK_XXX.md
       | (complete successfully)
tasks/done/TASK_XXX.md
```

### Agent Invocation

```python
Task(
    subagent_type="faion-task-executor-agent",
    description=f"Execute {task_name}",
    prompt=f"""
PROJECT: {project}
FEATURE: {feature}
TASK_FILE: {task_path}

SDD CONTEXT:
- Constitution: {constitution_content}
- Spec: {spec_content}
- Design: {design_content}
- Implementation Plan: {impl_plan_content}

TASK CONTENT:
{task_content}

EXECUTION STEPS:
1. Move task to in-progress/ (if in todo/)
2. Deep research - understand codebase context
3. Plan subtasks using TodoWrite
4. Execute implementation
5. Quality checks (tests, linting)
6. Commit with message: "TASK_XXX: {description}"
7. Move task to done/
"""
)
```

---

## 7. Batch Execution

### Workflow

```
1. Parse project, feature
   |
2. Find all tasks (in-progress first, then todo, sorted)
   |
3. Load SDD context
   |
4. Clarify ambiguities BEFORE execution
   |
5. Create feature branch (optional)
   |
6. Execute each task via workflow #6
   |
7. Run post-execution review
   |
8. Quality checks (tests, lint)
   |
9. Report summary
```

### Task Discovery

```bash
# Priority order
1. tasks/in-progress/TASK_*.md  # Resume first
2. tasks/todo/TASK_*.md         # Then new tasks

# Sort by task number
TASK_001, TASK_002, TASK_003...
```

### Continue vs Stop Rules

**Continue if:**
- Single task fails (document and continue)
- Test failures (log for later fix)
- Minor code style issues
- Non-blocking warnings

**Stop if:**
- Git merge conflict
- Build completely broken
- Security vulnerability detected
- User requests stop

### Execution Loop

```python
for task in sorted_tasks:
    result = execute_task(project, feature, task.name)

    if result.status == "BLOCKED":
        if is_critical(result.error):
            STOP  # Git conflict, build broken, security
        else:
            CONTINUE  # Test failures, minor issues

    log_result(result)
```

---

## 8. Parallelization Analysis

### Workflow

```
1. Read all TASK_*.md files
   |
2. Extract dependencies from each task
   |
3. Build dependency graph
   |
4. Group into waves (independent tasks together)
   |
5. Add checkpoints between waves
   |
6. Generate execution plan
```

### Dependency Detection

**Explicit:** From task files
```markdown
## Dependencies
- TASK_001 must complete first
- Requires auth module from TASK_002
```

**Implicit:** Detect from
- File modifications (same file = sequential)
- Module imports (importing from task output)
- Database schema (migrations order)
- API contracts (consumer after producer)

### Wave Pattern

```
Wave 1: [Independent tasks - parallel]
    |
Checkpoint 1: Verify all Wave 1 complete
    |
Wave 2: [Tasks depending on Wave 1 - parallel]
    |
Checkpoint 2: Verify, merge
    |
Wave N: [Final tasks]
    |
Final Checkpoint: Integration verification
```

### Speedup Calculation

```
Sequential time = Sum of all task times
Parallel time = Sum of longest task per wave + checkpoints
Speedup = Sequential / Parallel
```

Typical speedup: 1.8x - 3.5x

### Checkpoint Types

| Type | When | Action |
|------|------|--------|
| Merge | After parallel wave | Combine outputs, resolve conflicts |
| Verify | Critical dependency | Run tests, check contracts |
| Review | Complex integration | Human review before continuing |
| Sync | State-dependent | Ensure consistent state |

---

## 9. Backlog Grooming

### Workflow

```
READ BACKLOG -> PRIORITIZE -> SELECT FEATURE -> REFINE SPEC -> CREATE DESIGN -> GENERATE TASKS -> MOVE TO TODO
```

### Phase 1: Load Context

Read: `roadmap.md`, `constitution.md`
List features by status: backlog, todo, in-progress, done

### Phase 2: Display Status

```markdown
## Feature Status

### In Progress ({n})
- {feature} - {summary}

### Todo ({n})
- {feature} - {summary}

### Backlog ({n})
- {feature} - {summary} [P0/P1/P2]
```

### Phase 3: Action Selection

AskUserQuestion: "What do you want to do?"
1. Review priorities
2. Take feature to work
3. Add new feature
4. Remove feature
5. Finish grooming

### Phase 4: Feature Selection

Show backlog with: Name, Spec status, Design status, Dependencies

### Phase 5-7: Refine Documents

- If no spec: Use workflow #2
- If spec approved: Use workflow #3
- If design approved: Use workflow #4 and #5

### Phase 8: Move to Todo

If all artifacts complete:
```bash
mv features/backlog/{feature}/ features/todo/{feature}/
```

### Definition of Ready

- [ ] Problem/need clear
- [ ] Acceptance criteria defined
- [ ] Dependencies identified
- [ ] Small enough for one sprint
- [ ] No blockers
- [ ] Spec approved
- [ ] Design approved
- [ ] Tasks created

---

## 10. Roadmapping

### When to Use

- After completing features -> progress review
- New ideas -> add to backlog
- Priorities changed -> reprioritize
- Weekly/sprint -> roadmap sync

### Workflow

```
ANALYZE -> REVIEW PRIORITIES -> ADD FEATURES -> UPDATE ROADMAP
```

### Phase 1: Analyze Progress

```bash
# Count features by status
ls .aidocs/features/done/
ls .aidocs/features/backlog/
```

### Phase 2: Review Priorities

AskUserQuestion: "Are priorities current?"

### Phase 3: Add New Features

For each new idea:
1. Discuss scope via Socratic dialogue
2. Create `backlog/{NN}-{name}/spec.md`
3. Add to roadmap.md

### Roadmap Principles

| Timeframe | Confidence | Detail Level |
|-----------|------------|--------------|
| Now | 90% | Detailed, committed |
| Next | 70% | Planned, flexible |
| Later | 50% | Thematic, vision |

Include 20% buffer for unknowns.

---

## 11. Quality Gates

### Code Review Mode

**Criteria:**

| Category | Check |
|----------|-------|
| Critical | Correctness, broken tests, security, breaking changes |
| Style | Convention violations, pattern deviations, naming |
| Quality | Complexity, error handling, edge cases |
| Performance | N+1 queries, missing indexes, resource leaks |

### SDD Review Mode

Run reviewers in sequence:
1. `faion-sdd-reviewer-agent (mode: spec)`
2. `faion-sdd-reviewer-agent (mode: design)`
3. `faion-sdd-reviewer-agent (mode: plan)`
4. `faion-sdd-reviewer-agent (mode: tasks)` (if tasks exist)

### Quality Gate Levels

| Level | Check | Pass Criteria |
|-------|-------|---------------|
| L1 | Syntax | Linting zero errors |
| L2 | Types | Type checking zero errors |
| L3 | Tests | Unit tests 100% pass |
| L4 | Integration | Integration tests 100% pass |
| L5 | Review | Code review approved |
| L6 | Acceptance | All AC criteria met |

---

## 12. Confidence Checks

### Thresholds

| Score | Action |
|-------|--------|
| >=90% | Proceed confidently |
| 70-89% | Present alternatives, clarify gaps |
| <70% | Stop, ask questions first |

### Pre-Spec Check (Idea -> Spec)

| Check | Weight |
|-------|--------|
| Problem validated | 25% |
| Market gap | 25% |
| Target audience | 20% |
| Value proposition | 15% |
| Your fit | 15% |

### Pre-Design Check (Spec -> Design)

| Check | Weight |
|-------|--------|
| Requirements clear | 25% |
| AC testable | 25% |
| No contradictions | 20% |
| Scope defined | 15% |
| Dependencies known | 15% |

### Pre-Task Check (Design -> Tasks)

| Check | Weight |
|-------|--------|
| Architecture decided | 25% |
| Patterns established | 25% |
| No duplicate work | 20% |
| Dependencies mapped | 15% |
| Estimates reasonable | 15% |

### Pre-Implementation Check (Task -> Code)

| Check | Weight |
|-------|--------|
| Task requirements clear | 25% |
| Approach decided | 25% |
| No blockers | 20% |
| Tests defined | 15% |
| Rollback plan | 15% |

### Anti-Patterns to Catch

| Pattern | Risk | Action |
|---------|------|--------|
| "I think users want..." | Assumption | Require user research |
| "Should be easy..." | Underestimate | Require technical spike |
| "Similar to X..." | Missed differences | Require detailed comparison |
| "Figure it out later" | Deferred decision | Require decision now |
| "Obviously..." | Hidden assumption | Make explicit |

---

## 13. Reflexion Learning

### Memory Structure

```
~/.sdd/memory/
├── patterns_learned.jsonl    # Successful patterns
├── mistakes_learned.jsonl    # Errors and solutions
├── workflow_metrics.jsonl    # Execution metrics
└── session_context.md        # Current session state
```

### PDCA Cycle

```
Plan (hypothesis)
  |
Do (experiment)
  |
Check (self-evaluation)
  |
Act (improvement)
  |
Store (memory update)
```

### After Task Success

1. Extract what worked
2. Identify reusable patterns
3. Store in patterns_learned.jsonl
4. Update workflow_metrics.jsonl

### After Task Failure

1. Analyze root cause
2. Check if similar error exists in mistakes_learned.jsonl
3. If exists: Show previous solution
4. If new: Store error + solution
5. Update workflow_metrics.jsonl

### Before Task Start

1. Check mistakes_learned.jsonl for similar task types
2. If found: Show warnings and prevention tips
3. Check patterns_learned.jsonl for best practices
4. If found: Suggest approach

---

*SDD Workflows v2.0*
*Use with faion-sdd skill*
