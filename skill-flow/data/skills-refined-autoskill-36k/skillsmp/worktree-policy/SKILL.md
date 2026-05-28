---
name: worktree-policy
description: Enforce mandatory git worktree usage for multi-agent file modifications
version: 1.1.0
---

# Worktree Policy Skill

## Purpose

Enforce the mandatory use of git worktrees for all file modifications in multi-agent environments. Worktrees provide complete isolation between agents working on different features.

## When to Use

- Before any file modification
- When starting a new task
- When another agent is already working
- Before editing protected files

## Trigger Phrases

- "edit this file"
- "modify the code"
- "update the document"
- "make changes to"

## Core Rule

```
WORKTREE IS MANDATORY FOR ALL FILE MODIFICATIONS
Overhead: ~3 seconds | Benefit: Complete isolation
```

## Valid Exceptions (Only 3)

1. **READ-ONLY**: Analysis without file modification
2. **APPEND-ONLY**: tasks.md, sessions.json (add lines only)
3. **USER EXPLICIT REQUEST**: Documented in tasks.md

## Worktree Commands

### Create Worktree
```bash
git worktree add .worktrees/{agent-hex}-{feature} -b {tipo}/{name}
cd .worktrees/{agent-hex}-{feature}

# Example:
git worktree add .worktrees/c614-policy -b docs/policy-c614
```

### List Worktrees
```bash
git worktree list
```

### Remove Worktree
```bash
rm -rf .worktrees/{agent}-{feature}
git worktree prune
```

## Naming Standards

### Directory
```
.worktrees/{agent-short}-{feature-kebab}/
```

### Branch
```
{tipo}/{escopo}-{agent-hex}
```

| Type | Use |
|------|-----|
| `feature/` | New functionality |
| `bugfix/` | Bug correction |
| `hotfix/` | Urgent fix |
| `docs/` | Documentation |
| `refactor/` | Refactoring |
| `chore/` | Maintenance |

## Lifecycle

```
CREATE → WORK → VALIDATE QA → MERGE → CLEANUP
```

## Retention Policy

| Event | Action | Deadline |
|-------|--------|----------|
| PR merged | Delete worktree | 24h |
| Task completed | Delete worktree | 72h |
| Worktree stale | Evaluate and clean | Immediate |
| Maximum absolute | Force cleanup | 7 days |

## Enforcement

If you are editing a file without being in a worktree:
1. STOP immediately
2. Create worktree
3. Continue from there

---

*Skill based on Worktree Policy v1.1 | multi-agent-os*
