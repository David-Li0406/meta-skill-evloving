# Module: Sprint Selection + Phase Planning

## Objective

Select a subset of backlog items that form a coherent increment and can be integrated safely.

## Pre-Sprint Checklist (MANDATORY)

Before starting any sprint, check for existing integration branches:

```bash
git branch -a | grep "int/"
```

**If integration branches exist with unmerged work:**

| Option | When to Use |
|--------|-------------|
| Base new sprint on the int/* branch | When the existing work is related or foundational |
| Merge int/* to develop first | When the existing work is complete and tested |
| Sync both branches regularly | When parallel work is truly needed |

**Never branch new sprint work from develop when develop is behind an active int/* branch.**

## Rules

- Do not schedule conflicting tasks in parallel unless you introduce:
  - Explicit integration branch(es)
  - Explicit merge order
  - Contract ownership assignment

## Phase design

Each phase must include:
- Tasks runnable in parallel
- Tasks that must be sequenced
- Integration checkpoint definition

## Phase structure template

```
Phase N: <Name>
├── Parallel tasks: [TASK-X, TASK-Y]
├── Sequential tasks: TASK-Z (after TASK-X completes)
├── Integration checkpoint: <what merges where>
└── CI gate: <what must pass>
```

## Required outputs

1) **Sprint narrative** - What we're trying to accomplish
2) **Included/excluded items** - What's in scope and what's deferred
3) **Phase plan** - How work is organized across phases
4) **Merge plan outline** - Branch strategy and integration order
5) **Risks + mitigations** - What could go wrong and how we handle it

## Integration checkpoint requirements

Each phase must end with:
- All phase tasks merged to integration branch
- CI passing on integration branch
- No unresolved conflicts
- Contract compatibility verified

## LLM Capacity Guidelines

When planning phases for agentic engineers (LLM instances):

### Parallelism limits
- **Per-phase**: 3-5 parallel tasks max per LLM instance
- **Complexity budget**: ~200K-500K tokens total per phase (sum of all tasks)
- **Context management**: Tasks sharing contracts should be sequential to avoid drift

### Capacity planning
| Phase Complexity | Max Parallel Tasks | Typical Token Budget |
|------------------|-------------------|----------------------|
| Light | 5 | ~100-200K tokens |
| Moderate | 3-4 | ~200-400K tokens |
| Heavy | 2-3 | ~400-600K tokens |

### Buffer allocation
- Include 20% buffer for unforeseen complexity
- Add explicit "integration verification" token budget per phase
- Complex tasks may need human review checkpoints

### Red flags (capacity)
- Phase with total estimated tokens > 500K without checkpoint
- Single task estimated at > 150K tokens without breakdown
- All "complex" or "very_complex" tasks in same phase

## Red flags (general)

- Phase with >5 parallel tasks touching shared code
- Phase without explicit integration checkpoint
- Tasks spanning multiple phases without clear handoff

## Parallel Execution with Git Worktrees

When running multiple tasks in parallel, use git worktrees to isolate each task's work.

### Worktree Setup (Phase Start)

```bash
# For each parallel task in the phase
git worktree add Mad-task-<NNN> feature/TASK-<NNN>-<slug>
```

### Worktree Management During Sprint

| Situation | Action |
|-----------|--------|
| Task complete, PR merged | Worktree can be removed immediately or at sprint end |
| Task blocked | Keep worktree until resolution |
| Task cancelled | Remove worktree promptly |

### Worktree Cleanup (MANDATORY at Sprint End)

**Full reference:** `.claude/docs/shared/git-branching.md` → "Git Worktrees" section

After all sprint PRs are merged:
```bash
# Bulk cleanup
for wt in Mad-task-*; do [ -d "$wt" ] && git worktree remove "$wt" --force; done
```

### PM Responsibility

When closing a sprint, verify:
- [ ] All worktrees from the sprint are removed
- [ ] `git worktree list` shows only the main repo

---

## Sprint Capacity Guidelines

**Purpose:** Prevent scope overflow by setting explicit limits based on historical data.

**Source:** SPRINT-010 retrospective - 7 tasks planned, 4 completed. Sequential chains and parallel sprint execution exceeded capacity.

### Capacity Limits

| Sprint Type | Max Tasks | Max Sequential Chain |
|-------------|-----------|----------------------|
| Solo sprint | 5-7 tasks | 2-3 sequential |
| Parallel sprints | 4-5 per sprint | 1-2 sequential |

### Rules

1. **Sequential chains beyond 2 tasks should be separate sprints**
   - Each task in a chain blocks the next
   - Risk of deferral compounds with chain length
   - Exception: Very small tasks (~5-10K tokens each)

2. **When running parallel sprints, reduce capacity**
   - Context switching overhead
   - Merge conflict risk increases
   - CI queue congestion
   - Reduce by ~30% from solo capacity

3. **Stretch goals should be explicitly marked**
   - Tasks 6-7 in a 7-task sprint = stretch
   - Don't count stretch goals in commitment
   - Label in sprint file as "(stretch)"

### Sprint Structure Examples

**Good sprint structure:**
```
Phase 1 (Parallel): 4 tasks
Phase 2 (Sequential): 2 tasks (depends on 1 task from Phase 1)
Stretch: 1 task (explicitly marked)
```

**Risky sprint structure:**
```
Phase 1 (Parallel): 3 tasks
Phase 2 (Sequential): 4 tasks (chain of 4)  <- Too long
```

**Why risky:** A 4-task sequential chain means:
- Task 2 waits for Task 1
- Task 3 waits for Tasks 1+2
- Task 4 waits for Tasks 1+2+3
- Any blocker in the chain delays everything downstream

**Fix:** Split into 2 sprints:
- Sprint A: 3 parallel + 2 sequential
- Sprint B: 2 sequential (former chain tasks 3-4)

### Capacity Calculation

```
Base capacity: 5-7 tasks (solo sprint)

Adjustments:
- Parallel sprint execution: -30%
- Sequential chain > 2: Split chain
- High complexity tasks: Count as 1.5-2 tasks
- Documentation-only tasks: Count as 0.5 tasks
```

### Planning Checklist

Before finalizing sprint:
- [ ] Total tasks <= capacity limit
- [ ] Sequential chains <= 2-3 tasks
- [ ] Stretch goals explicitly marked
- [ ] Parallel sprint overlap considered

**Reference:** BACKLOG-127
