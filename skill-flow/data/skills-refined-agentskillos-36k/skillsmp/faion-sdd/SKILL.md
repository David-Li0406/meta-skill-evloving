---
name: faion-sdd
user-invocable: false
description: "SDD orchestrator: Specification-Driven Development workflow. Specifications, design docs, implementation plans, constitutions, task lifecycle (backlog->done), quality gates, reflexion learning, pattern/mistake memory. 17 methodologies."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# SDD Domain Skill

**Communication: User's language. Docs/code: English.**

## Philosophy

**"Intent is the source of truth"** - specification is the main artifact, code is just its implementation.

**No Time Estimates:** Use complexity levels (Low/Medium/High) and token estimates (~Xk) instead.

## Workflow Overview

```
CONSTITUTION -> SPEC -> DESIGN -> IMPL-PLAN -> TASKS -> EXECUTE -> DONE
      |          |        |          |           |         |        |
   project    feature  technical   100k rule   atomic    agent    learn
   principles  intent   approach   compliance   units   execution reflect
```

---

## Agents

| Agent | Purpose | Modes |
|-------|---------|-------|
| `faion-task-executor-agent` | Execute SDD tasks autonomously | - |
| `faion-task-creator-agent` | Create detailed TASK_*.md files | - |
| `faion-sdd-reviewer-agent` | Quality gate reviews | spec, design, plan, tasks |
| `faion-hallucination-checker-agent` | Validate task completion | - |

---

## Section Navigation

| Need | Section | Reference |
|------|---------|-----------|
| Start new project | Section 1: Constitutions | [workflows.md#1](workflows.md#1-writing-constitutions) |
| Define feature requirements | Section 2: Specifications | [workflows.md#2](workflows.md#2-writing-specifications) |
| Technical architecture | Section 3: Design Documents | [workflows.md#3](workflows.md#3-writing-design-documents) |
| Break into tasks | Section 4: Implementation Plans | [workflows.md#4](workflows.md#4-writing-implementation-plans) |
| Create task files | Section 5: Task Creation | [workflows.md#5](workflows.md#5-task-creation) |
| Execute single task | Section 6: Task Execution | [workflows.md#6](workflows.md#6-task-execution) |
| Execute all tasks | Section 7: Batch Execution | [workflows.md#7](workflows.md#7-batch-execution) |
| Optimize execution | Section 8: Parallelization | [workflows.md#8](workflows.md#8-parallelization-analysis) |
| Prepare features | Section 9: Backlog Grooming | [workflows.md#9](workflows.md#9-backlog-grooming) |
| Strategic planning | Section 10: Roadmapping | [workflows.md#10](workflows.md#10-roadmapping) |
| Code/SDD review | Section 11: Quality Gates | [workflows.md#11](workflows.md#11-quality-gates) |
| Pre-phase validation | Section 12: Confidence Checks | [workflows.md#12](workflows.md#12-confidence-checks) |
| Learn from outcomes | Section 13: Reflexion | [workflows.md#13](workflows.md#13-reflexion-learning) |

**Templates:** [templates.md](templates.md)

---

## Decision Tree: What to Do?

### Starting a Project

```
Is this a new project?
  |
  +-- YES: Does codebase exist?
  |         |-- YES -> Section 1 (MODE 1: Analyze codebase)
  |         |-- NO  -> Section 1 (MODE 2: Socratic dialogue)
  |
  +-- NO: Working on existing project
          |
          Does constitution.md exist?
            |-- NO  -> Section 1 first
            |-- YES -> Continue below
```

### Starting a Feature

```
Feature in backlog?
  |
  +-- NO: Add new feature
  |       -> Section 9: Backlog Grooming
  |
  +-- YES: Check document status
          |
          spec.md exists and approved?
            |-- NO  -> Section 2: Writing Specifications
            |-- YES -> design.md exists and approved?
                        |-- NO  -> Section 3: Design Documents
                        |-- YES -> implementation-plan.md exists?
                                    |-- NO  -> Section 4: Implementation Plans
                                    |-- YES -> tasks created?
                                                |-- NO  -> Section 5: Task Creation
                                                |-- YES -> Section 6 or 7: Execute
```

### Executing Tasks

```
How many tasks to execute?
  |
  +-- Single task -> Section 6: Task Execution
  |
  +-- All tasks -> Need parallel optimization?
                    |-- NO  -> Section 7: Batch Execution
                    |-- YES -> Section 8: Parallelization first
                               then Section 7
```

### Quality & Learning

```
What phase?
  |
  +-- Before spec    -> Section 12 (Pre-Spec confidence)
  +-- Before design  -> Section 12 (Pre-Design confidence)
  +-- Before tasks   -> Section 12 (Pre-Task confidence)
  +-- Before code    -> Section 12 (Pre-Implementation confidence)
  |
  +-- After task     -> Section 13 (Reflexion)
  +-- Code review    -> Section 11 (Quality Gates - Code)
  +-- SDD review     -> Section 11 (Quality Gates - SDD)
```

---

## Quick Reference

| Section | Input | Output | Agent |
|---------|-------|--------|-------|
| 1 | Project analysis/dialogue | constitution.md | - |
| 2 | Problem + requirements | spec.md | faion-sdd-reviewer-agent (mode: spec) |
| 3 | Approved spec | design.md | faion-sdd-reviewer-agent (mode: design) |
| 4 | Design + 100k rule | implementation-plan.md | faion-sdd-reviewer-agent (mode: plan) |
| 5 | Impl-plan + codebase | Task files in todo/ | faion-task-creator-agent |
| 6 | Single task | Task in done/ + commit | faion-task-executor-agent |
| 7 | All tasks | All tasks done/ | faion-task-executor-agent |
| 8 | Task dependencies | Optimized wave plan | - |
| 9 | Backlog features | Features ready in todo/ | - |
| 10 | Progress + priorities | roadmap.md | - |
| 11 | Code or SDD docs | Review report | faion-sdd-reviewer-agent |
| 12 | Pre-phase validation | Confidence score | - |
| 13 | Task outcomes | Lessons in memory | - |

---

## Directory Structure

```
.aidocs/
|-- constitution.md                    # Project principles
|-- contracts.md                       # API contracts
|-- roadmap.md                         # Milestones
+-- features/
    |-- backlog/                       # Waiting for grooming
    |-- todo/                          # Ready for execution
    |-- in-progress/                   # Being worked on
    +-- done/                          # Completed
        +-- {NN}-{feature}/
            |-- spec.md                # WHAT and WHY
            |-- design.md              # HOW
            |-- implementation-plan.md # Tasks breakdown
            +-- tasks/
                |-- backlog/
                |-- todo/              # Ready tasks
                |-- in-progress/       # Executing
                +-- done/              # Completed
```

**Lifecycle:** `backlog/ -> todo/ -> in-progress/ -> done/`

---

## 100k Token Rule

Each task MUST fit within 100k token context:

```
Research:       ~20k (read existing code)
Task file:       ~5k
Implementation: ~50k
Buffer:         ~25k
TOTAL:         <100k
```

**Token Estimation:**

| Component | Tokens |
|-----------|--------|
| Django model (simple) | 5-10k |
| Django model (complex) | 15-25k |
| Service class | 20-40k |
| ViewSet | 15-30k |
| Test file | 20-40k |

**Rule:** If uncertain, estimate higher and split.

---

## Confidence Thresholds

| Score | Action |
|-------|--------|
| >=90% | Proceed confidently |
| 70-89% | Present alternatives, clarify gaps |
| <70% | Stop, ask questions first |

**ROI:** 100-200 tokens checking saves 5-50K tokens of wrong-direction work.

---

## Quality Gate Levels

| Level | Check | Pass Criteria |
|-------|-------|---------------|
| L1 | Syntax | Linting zero errors |
| L2 | Types | Type checking zero errors |
| L3 | Tests | Unit tests 100% pass |
| L4 | Integration | Integration tests 100% pass |
| L5 | Review | Code review approved |
| L6 | Acceptance | All AC criteria met |

---

## Memory Storage

```
~/.sdd/memory/
|-- patterns_learned.jsonl    # Successful patterns
|-- mistakes_learned.jsonl    # Errors and solutions
|-- workflow_metrics.jsonl    # Execution metrics
+-- session_context.md        # Current session state
```

---

## Section 1: Constitutions (Summary)

**Purpose:** Define immutable project principles.

**Modes:**
1. **Existing Project** - Analyze codebase, present findings, draft
2. **New Project** - Socratic dialogue: Vision -> Tech -> Architecture -> Standards

**Output:** `.aidocs/constitution.md`

**Details:** [workflows.md#1](workflows.md#1-writing-constitutions) | [templates.md](templates.md#constitution-template)

---

## Section 2: Specifications (Summary)

**Purpose:** Define WHAT and WHY.

**Workflow:** Brainstorm -> Research -> Clarify -> Draft -> Review -> Save

**Key Techniques:**
- Five Whys for root cause
- Alternatives (A/B/C) with pros/cons
- User stories (As/I want/So that)
- Given-When-Then acceptance criteria

**Review:** Call `faion-sdd-reviewer-agent (mode: spec)` before save.

**Output:** `features/{status}/{feature}/spec.md`

**Details:** [workflows.md#2](workflows.md#2-writing-specifications) | [templates.md](templates.md#specification-template)

---

## Section 3: Design Documents (Summary)

**Purpose:** Define HOW.

**Prerequisites:** Approved spec.md, constitution.md

**Workflow:** Read Spec -> Read Constitution -> Research -> Decisions -> Approach -> Testing -> Risks -> Review -> Save

**Key Elements:**
- Architecture Decisions (AD-X) with context, options, rationale
- File mappings (CREATE/MODIFY)
- API endpoints (reference contracts.md)
- Testing strategy

**Review:** Call `faion-sdd-reviewer-agent (mode: design)` before save.

**Output:** `features/{status}/{feature}/design.md`

**Details:** [workflows.md#3](workflows.md#3-writing-design-documents) | [templates.md](templates.md#design-document-template)

---

## Section 4: Implementation Plans (Summary)

**Purpose:** Break design into 100k-compliant tasks.

**Workflow:** Load Context -> Analyze Complexity -> Work Units -> Apply 100k Rule -> Dependencies -> Review -> Save

**Key Elements:**
- Token estimates per task
- Dependency graph
- Execution waves (parallel/sequential)
- Critical path

**Review:** Call `faion-sdd-reviewer-agent (mode: plan)` before save.

**Output:** `features/{status}/{feature}/implementation-plan.md`

**Details:** [workflows.md#4](workflows.md#4-writing-implementation-plans) | [templates.md](templates.md#implementation-plan-template)

---

## Section 5: Task Creation (Summary)

**Purpose:** Create TASK_*.md files from implementation plan.

**Agent:** `faion-task-creator-agent`

**Workflow:** Load SDD -> Verify documents -> For each task: Call agent -> Review all tasks

**Review:** Call `faion-sdd-reviewer-agent (mode: tasks)` (4-pass review).

**Output:** Task files in `tasks/todo/`

**Details:** [workflows.md#5](workflows.md#5-task-creation) | [templates.md](templates.md#task-file-template)

---

## Section 6: Task Execution (Summary)

**Purpose:** Execute single task.

**Agent:** `faion-task-executor-agent`

**Workflow:** Find task -> Load context -> Execute -> Quality checks -> Commit -> Move to done

**Task Lifecycle:**
```
tasks/todo/ -> tasks/in-progress/ -> tasks/done/
```

**Output:** Executed task + commit

**Details:** [workflows.md#6](workflows.md#6-task-execution)

---

## Section 7: Batch Execution (Summary)

**Purpose:** Execute all tasks for a feature.

**Workflow:** Find all tasks -> Load context -> Clarify -> Execute each -> Review -> Report

**Continue/Stop Rules:**
- **Continue:** Single task fails, test failures, minor issues
- **Stop:** Git conflict, build broken, security issue

**Output:** All tasks in done/ (or partial)

**Details:** [workflows.md#7](workflows.md#7-batch-execution)

---

## Section 8: Parallelization (Summary)

**Purpose:** Optimize execution with wave pattern.

**Workflow:** Read tasks -> Extract dependencies -> Build graph -> Group waves -> Add checkpoints

**Wave Pattern:**
```
Wave 1: [Independent] -> Checkpoint -> Wave 2: [Dependent] -> ... -> Final
```

**Speedup:** 1.8x - 3.5x typical

**Output:** Parallelized execution plan

**Details:** [workflows.md#8](workflows.md#8-parallelization-analysis)

---

## Section 9: Backlog Grooming (Summary)

**Purpose:** Prepare features for execution.

**Workflow:** Load backlog -> Display status -> Select feature -> Refine spec -> Create design -> Generate tasks -> Move to todo

**Definition of Ready:**
- Problem clear, AC defined, dependencies known
- Spec approved, design approved, tasks created

**Output:** Feature with complete artifacts in todo/

**Details:** [workflows.md#9](workflows.md#9-backlog-grooming)

---

## Section 10: Roadmapping (Summary)

**Purpose:** Strategic planning and progress tracking.

**Structure:**
- **Now (90%):** Detailed, committed
- **Next (70%):** Planned, flexible
- **Later (50%):** Thematic, vision

**Output:** `roadmap.md`

**Details:** [workflows.md#10](workflows.md#10-roadmapping) | [templates.md](templates.md#roadmap-template)

---

## Section 11: Quality Gates (Summary)

**Purpose:** Code and SDD document reviews.

**Code Review Criteria:**
- Critical: Correctness, tests, security
- Style: Conventions, patterns, naming
- Quality: Complexity, error handling
- Performance: N+1, indexes, leaks

**SDD Review:** Sequential reviewers (spec -> design -> plan -> tasks)

**Output:** Review report with verdict

**Details:** [workflows.md#11](workflows.md#11-quality-gates)

---

## Section 12: Confidence Checks (Summary)

**Purpose:** Pre-phase validation to prevent wasted work.

**Phases:**
- Pre-Spec: Problem validated? Market gap? Target audience?
- Pre-Design: Requirements clear? AC testable? Scope defined?
- Pre-Task: Architecture decided? Patterns established?
- Pre-Implementation: Task clear? Approach decided? No blockers?

**Output:** Confidence score + recommendation

**Details:** [workflows.md#12](workflows.md#12-confidence-checks) | [templates.md](templates.md#confidence-check-template)

---

## Section 13: Reflexion Learning (Summary)

**Purpose:** PDCA cycle - learn from outcomes.

**Cycle:** Plan -> Do -> Check -> Act -> Store

**Triggers:**
- After task success: Extract patterns
- After task failure: Analyze root cause, store solution
- Before task start: Check memory for warnings/recommendations

**Output:** Lessons in `~/.sdd/memory/`

**Details:** [workflows.md#13](workflows.md#13-reflexion-learning) | [templates.md](templates.md#pattern-record-template)

---

## Methodologies

| Name | File |
|------|------|
| SDD Workflow Overview | [sdd-workflow-overview.md](sdd-workflow-overview.md) |
| Writing Specifications | [writing-specifications.md](writing-specifications.md) |
| Writing Design Documents | [writing-design-documents.md](writing-design-documents.md) |
| Writing Implementation Plans | [writing-implementation-plans.md](writing-implementation-plans.md) |
| Task Creation Parallelization | [task-creation-parallelization.md](task-creation-parallelization.md) |
| Quality Gates Confidence | [quality-gates-confidence.md](quality-gates-confidence.md) |
| Reflexion Learning | [reflexion-learning.md](reflexion-learning.md) |
| Backlog Grooming Roadmapping | [backlog-grooming-roadmapping.md](backlog-grooming-roadmapping.md) |
| Code Review Cycle | [code-review-cycle.md](code-review-cycle.md) |
| Pattern Memory | [pattern-memory.md](pattern-memory.md) |
| Mistake Memory | [mistake-memory.md](mistake-memory.md) |
| AI-Assisted Specification | [meth-ai-assisted-specification-writing.md](meth-ai-assisted-specification-writing.md) |
| Living Documentation | [meth-living-documentation-docs-as-code.md](meth-living-documentation-docs-as-code.md) |
| Architecture Decision Records | [meth-architecture-decision-records.md](meth-architecture-decision-records.md) |
| API-First Development | [meth-api-first-development.md](meth-api-first-development.md) |
| Design Docs Patterns | [design-docs-patterns.md](design-docs-patterns.md) |

---

## References

| File | Content |
|------|---------|
| [templates.md](templates.md) | All SDD document templates |
| [workflows.md](workflows.md) | Detailed workflow instructions |
| [key-trends-summary.md](key-trends-summary.md) | 2025-2026 SDD trends |
| [ai-assisted-specification-writing.md](ai-assisted-specification-writing.md) | AI-assisted spec writing |
| [api-first-development.md](api-first-development.md) | API-First development |
| [architecture-decision-records.md](architecture-decision-records.md) | ADR patterns |
| [living-documentation-docs-as-code.md](living-documentation-docs-as-code.md) | Docs-as-Code |
| [design-docs-patterns-big-tech.md](design-docs-patterns-big-tech.md) | Big Tech design patterns |
| [yaml-frontmatter.md](yaml-frontmatter.md) | YAML frontmatter conventions |

---

*SDD Domain Skill v3.0*
*Flat structure - all files in skill root*
