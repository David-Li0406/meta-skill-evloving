---
name: planner
description: Use when planning complex features, architecture design, multi-session work, or when plans need to be shared/reviewed. Activates for requests like "create a plan", "design implementation", "blueprint", or "plan out".
allowed-tools: ["shell", "read_file", "write_file", "update_plan"]
metadata:
  short-description: Create standalone implementation plan documents
---

# Implementation Planner

Create standalone implementation plan documents that can be:
- Understood without planning context
- Executed by different sessions or agents
- Validated for completeness before work begins
- Reviewed and approved before execution

**Read these references:**
- `~/.config/agent/core/methodology.md` - 5-phase problem-solving framework
- `~/.config/agent/domain/architecture/decomposition.md` - Problem breakdown strategies
- `~/.config/agent/domain/architecture/parallelization.md` - Concurrent execution patterns
- `~/.config/agent/core/task-management.md` - TODO discipline and task tracking
- `~/.config/agent/workflows/planning.md` - Complete planning workflow and template

## Instructions

### Phase 1: Gather Requirements

If requirements are unclear, start with **Design Discovery** before proceeding:
- Review existing context (files, docs, prior decisions)
- Ask **batched** clarifying questions (group related items)
- Propose 2–3 approaches with trade-offs when ambiguity remains
- Confirm scope, constraints, and success criteria
Then continue with requirements gathering:

Before creating a plan, thoroughly understand:

1. **Explicit requirements** - what was directly requested
2. **Implicit requirements** - what's needed but not stated
3. **Constraints** - technical, business, resource limitations
4. **Success criteria** - how will we know it's done
5. **Assumptions** - what are we assuming that needs validation

Ask clarifying questions if requirements are unclear. Do not proceed with ambiguous requirements.

### Phase 2: Research and Exploration

Explore the codebase to understand:

1. **Current state** - what exists now
2. **Relevant patterns** - how similar problems were solved
3. **Dependencies** - what this work depends on
4. **Integration points** - where this connects to existing code
5. **Potential conflicts** - what might this break

Use tools to gather evidence. Do not guess about code structure.

### Phase 3: Design Architecture

Make and document key decisions:

1. **Approach selection** - which solution path
2. **Component design** - what modules/functions needed
3. **Interface design** - how components interact
4. **Trade-off analysis** - what was considered and rejected

Document rationale for significant decisions.

### Phase 4: Decompose into Tasks

Break work into atomic, executable tasks:

1. **Identify atomic tasks** - single, clear responsibility each
2. **Map dependencies** - what must happen before what
3. **Find parallelization** - what can run concurrently
4. **Estimate effort** - size each task (S/M/L/XL)
5. **Define acceptance criteria** - how to verify each task

Each task must be:
- **Self-contained**: Can be executed without reading the whole plan
- **Testable**: Has clear acceptance criteria
- **Appropriately sized**: Not too coarse, not too granular

Use `decompose` for atomic breakdowns and `parallelize` to identify concurrent work.

### Phase 5: Define Verification

Specify how to validate the implementation:

1. **Test strategy** - what tests are needed
2. **Success criteria** - how to know it's complete
3. **Quality gates** - what must pass before done
4. **Rollback plan** - how to undo if needed

### Phase 5b: Evidence and Handoff (Required)

Document:
1. **Evidence mode** - label information as **Verified** vs **Reported (Unverified)**
2. **Handoff contract** - assumptions to validate, dependencies, and do-not-change items
3. **Risk register** - explicit risks with likelihood, impact, and mitigations

### Phase 6: Format and Output

Generate the plan document using the standard template from `planning.md`.

**Output options:**
- **File (default)**: Write to project-local `docs/plans/<name>.md` or `docs/plans/<name>/plan.md`
- **In-context**: Display plan directly if user requests

**File structure:**
- **Single file** (default): `docs/plans/<name>.md` for most plans
- **Directory** (complex plans): `docs/plans/<name>/plan.md` + supporting files
  - Use when: plan >500 lines, has supporting artifacts, or needs to split concerns
  - Supporting files: `research.md`, `architecture.md`, `alternatives.md`, `assets/`

**Project root detection:**
1. Check if PWD contains `.git/`
2. If yes, use PWD as project root
3. If no, ask user to either confirm PWD or provide a different directory

**File creation:**
- Single file: `mkdir -p <project-root>/docs/plans && touch <name>.md`
- Directory: `mkdir -p <project-root>/docs/plans/<name> && touch plan.md`

### Plan Quality Checklist

Before presenting the plan, verify:

- [ ] **Self-contained**: Can be understood without external context
- [ ] **Complete**: All tasks identified, no gaps
- [ ] **Executable**: Clear enough for blind execution
- [ ] **Correct**: Actually solves the stated problem
- [ ] **Atomic tasks**: Each task is single responsibility
- [ ] **Dependencies mapped**: Ordering is clear
- [ ] **Parallelization identified**: Concurrent work marked
- [ ] **Verification defined**: Success criteria specified
- [ ] **Risks documented**: Known risks and mitigations listed
- [ ] **Evidence labeled**: Verified vs reported information is explicit
- [ ] **Handoff-ready**: Assumptions, dependencies, and do-not-change items are explicit

All guidance from AGENT.md also applies.

## Arguments

Topic to plan: ${ARGUMENTS}
