---
name: merge-helper
description: Merge feature branch to main with pre-merge checks, CHANGELOG and ARCHITECTURE updates. Use when all spec stages are complete and user wants to merge. Ensures quality gates pass before merge.
---

# Merge Helper Skill

You guide the process of merging a completed feature branch into main.

## When to Use This Skill

- All stages in spec are ✅ Завершён
- User asks to "merge to main" or "мерж в main"
- Feature is ready for integration
- PR needs to be prepared

## Prerequisites

Before merge:
1. All spec stages must be ✅
2. All tests must pass
3. No uncommitted changes
4. Branch is up to date with main

## Workflow

### Step 1: Verify Feature Completion

Load spec file and check:
```bash
branch=$(git branch --show-current)
spec_file=".ai/specs/${branch}.md"
```

Verify all stages are ✅:
```
Checking feature completion...

Spec: .ai/specs/{branch}.md
Stages: 5/5 ✅

All stages complete. Proceeding with merge preparation.
```

If incomplete stages exist:
```
⚠️ Фича не завершена

Незавершённые этапы:
- Этап 3: API endpoints (🔄 В работе)
- Этап 4: UI templates (⬜ Не начат)

Завершите все этапы перед мержем.
```
**STOP** — do not proceed.

### Step 2: Run Quality Checks

```bash
# Run all tests
uv run pytest

# Check for uncommitted changes
git status

# Check if branch is behind main
git fetch origin main
git log HEAD..origin/main --oneline
```

**If tests fail:**
```
❌ Тесты не проходят

Failed: 3, Passed: 47

Исправьте тесты перед мержем.
```
**STOP**

**If uncommitted changes:**
```
⚠️ Есть незакоммиченные изменения

Modified files:
- src/module/file.py
- tests/test_file.py

Закоммитьте или отмените изменения.
```
**STOP**

**If behind main:**
```
⚠️ Ветка отстаёт от main

Commits behind: 5

Обновите ветку:
git rebase origin/main
# или
git merge origin/main
```

### Step 3: Update CHANGELOG

Read `.ai/CHANGELOG.md` and add release entry:

```markdown
## [Unreleased]

### Added - {Feature Name}
- [path/to/file1.py](../path/to/file1.py): Description
  - Detail 1
  - Detail 2

### Changed
- [path/to/file2.py](../path/to/file2.py): What changed

### Fixed
- [path/to/file3.py](../path/to/file3.py): What was fixed
```

**Collect changes from all commits in branch:**
```bash
git log main..HEAD --oneline
```

### Step 4: Update ARCHITECTURE (if needed)

Check if architectural changes were made:
- New modules added?
- New services/dependencies?
- Database schema changes?
- API surface changes?

If yes, update `.ai/ARCHITECTURE.md`:
- Add new components to diagrams
- Update module descriptions
- Document new patterns

### Step 5: Final Spec Update

Update spec file status:

```markdown
# [Feature Name] - Feature Specification

> **Дата создания:** 2026-01-05
> **Дата завершения:** 2026-01-07  ← Add this
> **Ветка:** `feature/name`
> **Статус:** ✅ Завершён  ← Change from 🟡
```

Add final history entry:
```markdown
| 2026-01-07 | MERGE | abc1234 | Feature merged to main |
```

### Step 6: Prepare Merge

**Option A: Squash Merge (recommended)**
```bash
git checkout main
git pull origin main
git merge --squash feature/{name}
git commit -m "feat: {feature description}

- Stage 1: {description}
- Stage 2: {description}
- ...

Closes #{issue-number}"
```

**Option B: Rebase Merge**
```bash
git checkout main
git pull origin main
git rebase feature/{name}
```

### Step 7: Post-Merge Cleanup

After successful merge:

```bash
# Delete local branch
git branch -d feature/{name}

# Delete remote branch (if applicable)
git push origin --delete feature/{name}
```

**Archive spec file** (optional):
```bash
mv .ai/specs/{branch}.md .ai/specs/archive/{branch}.md
```

### Step 8: Report Completion

```
✅ Merge завершён

📋 Фича: {Feature Name}
🌿 Ветка: feature/{name} → main
📝 Коммит: {commit-hash}

📄 Обновлённые документы:
- .ai/CHANGELOG.md ✅
- .ai/ARCHITECTURE.md ✅ (если применимо)
- .ai/specs/{branch}.md → archived

🧹 Cleanup:
- Локальная ветка удалена ✅
- Remote ветка удалена ✅

Фича успешно интегрирована в main!
```

## Pre-Merge Checklist

Before proceeding with merge, verify:

- [ ] All spec stages ✅
- [ ] All tests pass
- [ ] No uncommitted changes
- [ ] Branch up to date with main
- [ ] CHANGELOG updated
- [ ] ARCHITECTURE updated (if needed)
- [ ] Spec marked as complete
- [ ] User confirmed merge

## Merge Strategies

### When to Squash

- Feature has many small commits
- Commit history is messy
- Want clean single commit in main

### When to Rebase

- Commits are well-structured
- Want to preserve commit history
- Each commit is atomic and meaningful

## References

See [commit-helper](../commit-helper/SKILL.md) for commit conventions.
See [changelog_templates.md](../commit-helper/changelog_templates.md) for CHANGELOG format.

**NOTE:** This is the ONLY place where CHANGELOG.md should be updated. Individual commits do NOT update CHANGELOG.
