---
name: checkpoint
version: 1.1.0
changelog: Added git tagging at phase boundaries
description: Save current state for session breaks. Includes context health check and recommendations.
---

# Checkpoint

Save current state for session breaks. Includes context health check and recommendations.

## Task
$ARGUMENTS

## Instructions

Output: `## Checkpoint`

### 1. Assess Current State

Review what's been accomplished:
- What task are we working on?
- What's completed vs in progress?
- Any blockers or decisions pending?
- Key files touched or discovered?

### 2. Context Health Check

**Read metrics** using shared script:

```bash
.claude/skills/shared/scripts/read-metrics.sh used_percentage
```

See `agent_docs/context.md` for utilization thresholds and recommended actions.

**Fallback** (if metrics unavailable): Watch for degradation symptoms — forgetting constraints, hallucinating APIs, missing obvious issues.

### 3. Update STATE.md (Incremental)

**Merge updates into existing STATE.md** rather than overwriting:
- Update YAML frontmatter fields (status, phase, context_percent, last_updated)
- Append new decisions to `## Decisions`
- **Prune stale decisions** (delete when encoded in code, or task complete)
- Update `## Blockers` (add new, mark resolved with [x])
- Update `## Key Files` (add new discoveries)
- Replace `## Next Steps` with current guidance

If STATE.md doesn't exist, use [state template](../shared/templates/state.md).

### 4. Git State (Required)

Always record accurate git state to prevent stale information:

```bash
git status --short && git log -1 --oneline
```

| Working tree | STATE.md update |
|--------------|-----------------|
| Clean | `## Git State` → `Clean at [hash] [message]` |
| Uncommitted changes | `## Git State` → `Uncommitted: [list files]` |

**Why required**: Prevents stale "uncommitted changes" info after commits. The checkpoint is the source of truth for git state.

### 5. Create Git Tag (Phase Boundaries)

At significant checkpoints (phase completion, pre-risky-change), create a tagged rollback point:

```bash
./scripts/checkpoint-tag.sh [phase-name]
```

Creates tag: `checkpoint/{phase}-{timestamp}`

**When to tag**:
- After each phase completion (research, plan, implement)
- Before risky refactors
- Before `/compact` (preserves rollback even if context changes)

**Rollback command** (add to STATE.md):
```markdown
## Rollback Point
Tag: checkpoint/research-20260122-143052
Command: git checkout checkpoint/research-20260122-143052
```

### 6. Update Docs (If Skills Changed)

If skills were added/modified this session, run `/docs` to update README.md.

### 7. Output Recommendation

Based on utilization (from metrics) and task status, recommend next action. See `agent_docs/context.md` for threshold guidance.

## Constraints

- Keep STATE.md under 100 lines (forces prioritization)
- Delete resolved items aggressively
- Don't checkpoint trivial progress
- Focus on what's needed to resume, not history
- When status is `complete`, set phase to `idle`

## Exit Criteria

STATE.md saved. Context recommendation provided. Session can resume from cold start.
