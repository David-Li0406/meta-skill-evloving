---
name: hierarchical-merge
description: Enforce hierarchical merge protocol - branches merge to parent, not directly to main
version: 1.0.0
---

# Hierarchical Merge Skill

## Purpose

Validate and enforce the Hierarchical Merge Protocol (HMP) which ensures branches merge to their parent branch, not directly to main. This creates controlled convergence through parent-child relationships.

## When to Use

- Before merging any feature/task branch
- When completing work in a worktree
- Before closing a sprint or feature branch
- When validating branch structure

## Trigger Phrases

- "merge this branch"
- "ready to merge"
- "complete this task"
- "close this branch"

## Protocol Rules

### Core Principle
```
Branches merge to their PARENT branch, not directly to main.
```

### Merge Direction
| Branch Level | Merges To |
|--------------|-----------|
| Level 3 (subtask) | Level 2 (task) |
| Level 2 (task) | Level 1 (sprint) |
| Level 1 (sprint) | main |

### Child Completion Constraint
A branch can ONLY merge to its parent when ALL children are complete:
- Child branch has been merged back (or abandoned with record)
- Associated worktree has been removed
- tasks.md status is COMPLETED

### Exception Prefixes
These prefixes bypass the Child Completion Constraint:
- `bugfix/*` - Bug fixes that shouldn't wait
- `hotfix/*` - Critical production fixes
- `emergency/*` - System-critical changes
- `selective/*` - Intentional partial merge (documented)
- `partial/*` - Known incomplete work (documented)

## Validation Checklist

Before allowing merge:
```
[ ] All child branches merged or abandoned
[ ] All child worktrees removed (git worktree prune)
[ ] tasks.md entries show COMPLETED
[ ] No active lock files for child branches
[ ] CI/CD passes
[ ] Code review approved (if required)
```

## Commands

```bash
# Verify children are complete
git branch --list "feature/task-A*" | wc -l  # Should be 1

# Merge to parent (not main!)
git checkout feature/sprint-01
git merge --no-ff feature/task-A -m "merge: task-A complete"
```

## Anti-Pattern Warning

```
NEVER merge directly to main from a subtask:
  git checkout main
  git merge feature/subtask-A1  # WRONG!

CORRECT approach:
  git checkout feature/task-A
  git merge feature/subtask-A1  # Merge to parent first
```

## Integration

- Uses tasks.md for completion status
- Integrates with worktree cleanup
- Enforced by pre-merge validation

---

*Skill based on Hierarchical Merge Protocol v1.0 | multi-agent-os*
