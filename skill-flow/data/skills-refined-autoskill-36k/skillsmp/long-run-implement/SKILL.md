---
name: long-run-implement
description: Execute long-running implementation tasks autonomously. Use when user wants to implement a plan, run autonomous implementation, execute tasks with minimal checkpoints, or do long-run execution.
context: fork
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep, Skill
user-invocable: true
---

# Long-Run Implement

Transform task specifications into executable plans and run them autonomously with minimal checkpoints, per-task atomic commits, and full state persistence.

## Usage

```
/long-run-implement [spec-path] [--prepare-only]
```

### Flags

- `--prepare-only`: Stop after Phase 2 (plan preparation). Use to review generated plans before execution.

## When to Use This Skill

Activate when the user says things like:
- "Implement this plan autonomously"
- "Run long-run implementation"
- "Execute these tasks with minimal interruption"
- "Implement the spec with atomic commits"

## What This Skill Does

1. **Initialize** - Set up or restore execution state
2. **Prepare Plans** - Call plan-fixer to validate, optimize, and split into individual plans
3. **Execute** - **Spawn fresh subagent per plan** via Task tool (preserves quality)
4. **Finalize** - Present summary and verification options

## Architecture: Fresh Context Per Plan

**CRITICAL**: This skill spawns a **fresh subagent for each plan** to prevent context degradation.

```
long-run-implement (orchestrator - stays in main context)
    │
    ├── Plan 01 → Task tool → fresh subagent (0% context) → executes → returns
    │                              ↑
    │                         200k tokens available
    │
    ├── Plan 02 → Task tool → fresh subagent (0% context) → executes → returns
    │
    └── Plan 03 → Task tool → fresh subagent (0% context) → executes → returns
```

Why this matters:
- **0-30% context**: Peak quality
- **30-50% context**: Good quality
- **50-70% context**: Degrading quality
- **70%+ context**: Poor quality

Each plan executes at peak quality because it starts fresh.

## Key Features

- **Fresh Context Per Plan** - Each plan spawns a new subagent with 200k tokens at 0%
- **Minimal Checkpoints** - Only stops for genuine blockers (architectural changes, external actions, unrecoverable errors)
- **Per-Task Atomic Commits** - Each completed task is committed immediately with conventional commit format
- **Full Persistence** - All state saved to disk; resume anytime from interruption point
- **Automatic Deviation Handling** - Auto-fix minor issues; log enhancements to ISSUES.md

## Workflow Phases

### Phase 1: Initialize
See [phases/1-initialize.md](phases/1-initialize.md)

- Locate and validate spec folder
- Check for existing state (resume detection)
- Initialize .long-run/ directory structure
- Pre-flight checks (clean working tree)

### Phase 2: Prepare Plans (calls plan-fixer)
See [phases/2-transform.md](phases/2-transform.md)

- If tasks.md exists and .long-run/plans/ is empty:
  - Run plan-fixer skill on tasks.md (Phases 0-4)
  - Plan-fixer validates, fixes, optimizes, and splits into individual plans
- If PLAN.md exists at root and .long-run/plans/ is empty:
  - Run plan-fixer Phase 4 only (split existing plan)
- If .long-run/plans/ already populated:
  - Skip to Phase 3

**If `--prepare-only` flag is set: STOP here**

### Phase 3: Execute
See [phases/3-execute.md](phases/3-execute.md)

- Execute plans sequentially
- Spawn subagent for each plan (agent type from orchestration.yml)
- Handle deviations automatically where possible
- Per-task atomic commits
- Update checkpoints after each task

### Phase 4: Finalize
See [phases/4-finalize.md](phases/4-finalize.md)

- Aggregate results from all summaries
- Present completion report
- Offer verification and cleanup options

## Stop Conditions

| Condition | Phase | What Happens |
|-----------|-------|--------------|
| Task group too vague | Transform | Asks for clarification |
| Architectural decision needed | Execute | Presents decision with options |
| External action needed | Execute | Provides instructions, waits |
| Error after 3 retries | Execute | Offers retry/skip/abort |

## File Structure (Runtime)

```
{spec-folder}/
├── spec.md                    # Input
├── tasks.md                   # Input (updated with checkboxes)
└── .long-run/                 # Created by this skill
    ├── STATE.md               # Position, metrics, progress
    ├── agent-history.json     # Subagent tracking
    ├── current-agent-id.txt   # Quick resume lookup
    ├── clarifications.md      # Q&A log
    ├── ISSUES.md              # Deferred enhancements
    ├── plans/
    │   ├── 01-PLAN.md         # Transformed plans
    │   ├── 01-CHECKPOINT.json # Task-level progress
    │   └── ...
    └── summaries/
        ├── 01-SUMMARY.md      # Completion summaries
        └── ...
```

## Commit Format

```
{type}({plan}): {task-name}
```

Types: `feat`, `fix`, `test`, `refactor`, `chore`, `docs`

## Resume Capability

If execution is interrupted, invoke this skill again on the same spec. It will:
1. Detect existing state
2. Find last checkpoint
3. Offer resume options
4. Continue from where it left off

## Orchestration Integration

This skill integrates with `orchestration.yml` to enable specialized agents per task group.

### How It Works

1. **orchestrate-tasks** (upstream) creates `{spec_path}/orchestration.yml`:
   ```yaml
   task_groups:
     - name: authentication-system
       claude_code_subagent: backend-specialist
     - name: user-dashboard
       claude_code_subagent: frontend-specialist
   ```

2. **plan-fixer** (called per task group) adds metadata to PLAN.md:
   - Reads orchestration.yml
   - Adds frontmatter with `task_group` and `claude_code_subagent`

3. **long-run-implement Phase 3** spawns the correct agent:
   - Reads orchestration.yml
   - Looks up `task_group` from PLAN.md frontmatter
   - Finds matching `claude_code_subagent`
   - Spawns that agent type instead of "general-purpose"

### Agent Resolution

Agents are resolved from the PROJECT's `.claude/agents/` folder:

```
orchestration.yml: claude_code_subagent: backend-specialist
  → .claude/agents/backend-specialist.md
```

If the agent is not found in orchestration.yml or orchestration.yml doesn't exist, the fallback is `"general-purpose"`.

**Note:** Agents in `.claude/agents/` have their own hard-coded references to the standards they need. No separate standards embedding is required.

Example PLAN.md structure:
```markdown
---
task_group: authentication-system
claude_code_subagent: backend-specialist
---

<task name="implement-login">
...
</task>
```

## References

### Workflows
- [initialize-state.md](references/workflows/initialize-state.md)
- [detect-resume.md](references/workflows/detect-resume.md)
- [transform-task-group.md](references/workflows/transform-task-group.md)
- [validate-enrichment.md](references/workflows/validate-enrichment.md)
- [clarification-protocol.md](references/workflows/clarification-protocol.md)
- [validate-dependencies.md](references/workflows/validate-dependencies.md)
- [atomic-commit.md](references/workflows/atomic-commit.md)
- [apply-deviation-rules.md](references/workflows/apply-deviation-rules.md)
- [enrich-task.md](references/workflows/enrich-task.md)
- [spawn-plan-executor.md](references/workflows/spawn-plan-executor.md)
- [update-state.md](references/workflows/update-state.md)
- [track-agent.md](references/workflows/track-agent.md)
- [timeout-handling.md](references/workflows/timeout-handling.md)
- [cleanup.md](references/workflows/cleanup.md)
- [create-plan-summary.md](references/workflows/create-plan-summary.md)
- [atomic-write.md](references/workflows/atomic-write.md)

### Templates
See [references/templates/](references/templates/) for state and checkpoint templates.

## Agents

- **long-run-orchestrator** - Stays in main context, spawns subagents per plan, handles responses
- **long-run-executor** - Spawned as subagent per plan, executes tasks, returns structured output

## Related Commands

- `/long-run-orchestrator` - Execute-only entry point (expects .long-run/plans/ to exist)
