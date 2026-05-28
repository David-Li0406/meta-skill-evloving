---
name: god-ralph
description: Autonomous development orchestrator that combines ephemeral Ralph workers with Beads granular task tracking. Use when executing multiple beads autonomously, running parallel development tasks, or when you need persistent work tracking across sessions.
version: "0.1.0"
author: "Duncan Jurman"
license: "MIT"
---

# god-ralph Skill

god-ralph is an autonomous development system that combines two powerful patterns:

1. **Ralph Wiggum**: Ephemeral, iterative agents that work until completion
2. **Beads**: Granular, dependency-tracked work items

## When to Use god-ralph

Use god-ralph when:
- You have multiple beads ready to work on
- You want autonomous execution without babysitting
- You need parallel development on independent tasks
- You want verification after each completion
- You need persistent progress tracking

## Core Concepts

### Ephemeral Ralphs
Each Ralph worker:
- Completes exactly ONE bead
- Iterates until acceptance criteria met (or max iterations)
- Dies after completion
- Works in isolated git worktree

### Orchestrator
Persistent agent that:
- Finds ready beads via `bd ready`
- Analyzes parallelism opportunities
- Spawns and monitors Ralphs
- Merges completed work
- Runs verification
- Creates fix-beads on failure

### Verification Ralph
After each merge:
- Runs all acceptance criteria
- Checks for integration issues
- Creates high-priority fix-beads on failure

## Commands

| Command | Purpose |
|---------|---------|
| `/god-ralph start` | Start autonomous execution (dry-run first) |
| `/god-ralph plan` | Interactive wizard to create beads |
| `/god-ralph status` | Show current progress |
| `/god-ralph stop` | Gracefully stop execution |
| `/god-ralph <id>` | Run Ralph on specific bead |

## Bead Specification

For god-ralph to work effectively, beads should include:

```yaml
title: "Clear, actionable title"
description: "Detailed description"
type: feature|task|bug
priority: 0-4

# In comments until schema supports:
ralph_spec:
  completion_promise: "BEAD COMPLETE"
  max_iterations: 50
  acceptance_criteria:
    - type: test
      command: "npm test"
    - type: lint
      command: "npm run lint"
```

## Workflow Example

```bash
# 1. Plan your work
/god-ralph plan
# Wizard asks questions, creates beads

# 2. Review what's ready
bd ready

# 3. Start autonomous execution
/god-ralph start
# Shows dry-run plan, asks for confirmation

# 4. Monitor progress
/god-ralph status

# 5. Stop when needed
/god-ralph stop
```

## Parallelism

god-ralph automatically parallelizes independent beads:

```
Group 1 (parallel):
  - beads-abc: "Add API endpoint" → worktree/1
  - beads-def: "Add frontend page" → worktree/2

Group 2 (after Group 1):
  - beads-ghi: "Integration tests" → worktree/3
```

Beads with file overlap run sequentially.

## Git Isolation

Each Ralph works in a separate git worktree:

```
Main repo:     /project/           → main
Worktree 1:    .worktrees/ralph-1/ → ralph/beads-abc
Worktree 2:    .worktrees/ralph-2/ → ralph/beads-def
```

This allows:
- Parallel file editing
- Independent commits
- Clean merges

## Cost Awareness

Typical costs:
- Simple bead (3-5 iterations): $1-2
- Medium bead (10-15 iterations): $3-5
- Complex bead (30+ iterations): $10-15

`/god-ralph status` shows running cost estimate.

## Error Handling

When things go wrong:

1. **Ralph fails (max iterations)**
   - Bead marked as blocked
   - Diagnostic comment added
   - Orchestrator continues to next bead

2. **Merge conflict**
   - Merge aborted
   - Fix-bead created (priority 0)
   - Original bead marked blocked

3. **Verification fails**
   - Fix-bead created with failure details
   - Linked to failed beads
   - Orchestrator continues

## Integration with Beads

god-ralph extends the beads ecosystem:

```bash
# Create beads normally
bd create --title="..." --type=feature

# Add ralph_spec via comments
bd comments <id> --add "ralph_spec: ..."

# god-ralph uses bd CLI under the hood
bd ready      # Find work
bd update     # Claim work
bd close      # Complete work
bd dep        # Manage dependencies
```

## Best Practices

1. **Right-size beads**: 5-15 iterations each
2. **Clear acceptance criteria**: Specific, runnable tests
3. **Explicit dependencies**: Link related beads
4. **Monitor progress**: Check `/god-ralph status` periodically
5. **Review fix-beads**: Address failures before continuing

## References

- [BEAD_SPEC.md](references/BEAD_SPEC.md) - Detailed bead format
- [WORKFLOWS.md](references/WORKFLOWS.md) - Common workflows
