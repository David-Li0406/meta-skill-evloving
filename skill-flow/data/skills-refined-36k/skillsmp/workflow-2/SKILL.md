---
name: workflow
version: 1.0.0
changelog: Initial structured workflow with gates and state management
description: Entry point for task execution. Routes to research, plan, implement, or debug based on task type and existing state. Orchestrates phase transitions after approval.
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Skill, AskUserQuestion
---

# Workflow

Entry point and orchestrator. Routes to appropriate phase, then manages transitions after each approval gate.

## Task
$ARGUMENTS

## Instructions

Output: `## Workflow`

### 1. Check for Existing State

Read STATE.md if it exists. Parse YAML frontmatter:

```yaml
---
task: "..."
status: in_progress | blocked | complete | parked
phase: research | plan | implement | debug | idle | quick
path: research,plan,implement  # orchestration path
context_percent: N
last_updated: YYYY-MM-DD
---
```

**If `status: idle` or `status: complete`**: proceed to assessment

**If `status: in_progress` with `path` set**: offer continuation

```markdown
## Existing State Found

**Task**: [task]
**Current phase**: [phase]
**Path**: [path]
**Progress**: [which phases complete]

Options:
1. **Continue** — resume at current phase
2. **Park and switch** — set status to parked, begin new task
3. **Discard** — clear state, begin new task
```

**If `status: in_progress` without `path`**: legacy state, offer resume or restart

**If no STATE.md**: proceed to assessment

### 2. Assess Task Type

| Signals | Task Type | Path | Gates |
|---------|-----------|------|-------|
| "not working", "error", "bug", "broken" | Bug | `debug` (then implement if needed) | Normal |
| "add", "implement", "create", "build" + unclear scope | Feature | `research,plan,implement` | Normal |
| Clear, small, single-file change | **Quick fix** | (none - direct implementation) | **Minimal** |
| "refactor", "change", "update" + multi-file | Modification | `research,plan,implement` | Normal |

**Quick fix mode**: For obvious, low-risk changes (typo fix, add log statement, rename variable), skip research/plan phases entirely. Execute directly, verify, done. No STATE.md needed.

### 3. Present Recommendation

```markdown
## Task Assessment

**Task**: [one-line summary]
**Type**: [bug | feature | quick fix | modification]
**Scope**: [small | medium | large]

**Path**: [phase] → [phase] → [phase]

**Rationale**: [Why this path fits]

Proceed?
```

### 4. Initialize State

**Skip for quick fixes** — complete in one turn.

**For all other task types**, write STATE.md:

```yaml
---
task: "[one-line summary]"
status: in_progress
phase: [first phase in path]
path: [comma-separated phases]
context_percent: 0
last_updated: [today]
---

## Original Prompt
> [Capture user's request VERBATIM - this survives compaction]

## Scope
**Doing**: [What's included]
**Not doing**: [Explicit exclusions]

## Decisions
[None yet]

## Blockers
[None]

## Key Files
[To be discovered]

## Next Steps
Starting [first phase]
```

**Why capture original prompt**: After compaction or session break, the verbatim request ensures intent isn't lost. The one-line `task:` is a summary; the original prompt is the source of truth.

### 5. Orchestration Loop

After user approves, execute this loop:

```
while path has remaining phases:
    1. Pre-flight: check context utilization (automatic)
    2. Invoke current phase skill (using Skill tool)
    3. Phase skill runs, ends with gate question
    4. User approves (or redirects)
    5. AUTO: Run /checkpoint (no user action needed)
    6. Update STATE.md: advance phase, update context_percent
    7. If more phases remain, continue loop
    8. If user redirects, update path and continue
```

**Auto-checkpoint**: Checkpoint runs automatically after each gate approval — no user action required. This captures phase-specific learnings before context compaction may be needed.

**Invoking phase skills**:
- `/research` — exploration, returns findings
- `/plan` — creates implementation plan
- `/implement` — executes plan with checkpoints
- `/debug` — diagnoses issue, may lead to implement

**After each phase completes**:
- Update `phase:` to next in path
- Update `## Next Steps`
- Present transition: "Research complete. Ready to plan?"

**On user redirect**: Update `path:` to new direction, continue from there.

### 6. Completion

When all phases complete:
- Set `status: complete`, `phase: idle`
- Clear `path:`
- Run `/checkpoint` to save final state

**Exit lifecycle** — smart defaults based on state:

First, check git state: `git status --short`

| Condition | Default | Prompt |
|-----------|---------|--------|
| Uncommitted changes | Suggest commit | "Uncommitted changes detected. Commit first?" |
| Clean git + high context (>50%) | Suggest clear | "Task complete. `/clear` recommended for fresh start." |
| Clean git + low context (<50%) | Suggest continue | "Task complete. Context is light — continue or `/clear`?" |

```markdown
## Task Complete

[Smart suggestion based on above]

**Options:**
1. **Clear** — fresh context for unrelated task (`/clear`)
2. **Compact** — reduce context, preserve learnings (`/compact`)
3. **Continue** — keep context for follow-up questions

Which would you like?
```

**Why smart defaults**: Reduces decision fatigue while preserving user control. Uncommitted work should be committed before clearing.

## Constraints

- Don't skip assessment — even obvious tasks benefit from explicit routing
- Wait for approval at each phase boundary (gates are mandatory)
- Keep STATE.md as source of truth

### Context Hygiene (Mandatory)

**Pre-flight check**: Before invoking any phase skill, run:

```bash
.claude/skills/shared/scripts/read-metrics.sh used_percentage
```

| Utilization | Action |
|-------------|--------|
| < 50% | Proceed normally |
| 50-60% | Warn user, proceed with caution |
| 60%+ | **GATE**: Run context recovery protocol |

**Context estimation**: Before starting a phase, estimate its cost:

```bash
./scripts/estimate-context.sh [phase]
```

| Phase | Typical Cost |
|-------|--------------|
| research | +15% |
| plan | +10% |
| implement | +20% |
| debug | +15% |

If projected utilization exceeds 60%, run recovery protocol BEFORE starting the phase.

**Hard gate at 60%**: Do not invoke the next phase skill until context is below 60%. This is not a suggestion — degraded context means degraded work quality.

#### Context Recovery Protocol (at 60%+)

**Step 1**: Run `/checkpoint` to save current state

**Step 2**: Choose recovery action based on STATE.md status:

| STATE.md status | Action | Rationale |
|-----------------|--------|-----------|
| `in_progress` or `blocked` | `/compact` | Preserve learnings, continue task |
| `complete` or `idle` | `/clear` | Fresh start, no continuity needed |
| No STATE.md | `/clear` | Nothing to preserve |

**Step 3**: After `/compact` or `/clear`, the session-init hook automatically injects STATE.md if the task was incomplete. This ensures immediate recovery.

**Why automatic recovery**: The hook detects fresh context (<25%) + active STATE.md status and injects the full state. No manual reload needed.

**Update STATE.md `context_percent`**: After each phase completion, record current utilization from metrics.

## Exit Criteria

Task completed through all phases, or user explicitly exits workflow.
