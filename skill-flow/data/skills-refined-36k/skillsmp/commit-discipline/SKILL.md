---
name: commit-discipline
description: "Use when making commits. Conventional commits, atomic changes."
---

# Commit Discipline

**Goal:** Atomic commits that are easy to review, revert, and understand.

## Rules

```
ATOMIC     -> One logical change per commit
COMPLETE   -> Each commit leaves code working
MEANINGFUL -> Message explains WHY
CONVENTIONAL -> Follow the format
```

## Format

```
<type>(<scope>): <description>

[optional body]
```

| Type | Use |
|------|-----|
| feat | New feature |
| fix | Bug fix |
| refactor | Code change (no feature/fix) |
| test | Adding/fixing tests |
| docs | Documentation |
| chore | Build, deps, config |

## Examples

```bash
git commit -m "feat(auth): add password reset endpoint"

git commit -m "$(cat <<'EOF'
fix(payments): handle webhook race condition

Two webhooks arriving simultaneously both update same order.
Added mutex to serialize.

Fixes #234
EOF
)"
```

## Atomic Commits

**Atomic:** One change. Describable in one sentence.

```bash
git add -p         # Stage specific hunks
git add src/auth/  # Stage specific files
```

## Workflow

```bash
git diff --cached          # Check staged
npm test                   # Verify tests
git commit -m "type: msg"  # Commit
```

## Fixing Mistakes (Not Pushed)

```bash
git commit --amend                 # Add to last
git commit --amend -m "new msg"    # Fix message
```

## Decision Criteria

| Situation | Action |
|-----------|--------|
| Multiple unrelated changes | Split commits |
| Tests failing | Don't commit. Fix first. |
| WIP changes | Use stash, not commit |

**Pairs with:** tdd, pr-workflow, verification
