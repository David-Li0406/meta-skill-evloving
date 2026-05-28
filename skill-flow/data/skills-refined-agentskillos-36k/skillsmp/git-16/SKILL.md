---
name: git
description: Guided git workflow for projects using Git Flow branching strategy. Trigger with "/git" when creating feature branches, bug fixes, hotfixes, or releases. Helps with branch creation, merging, and release tagging.
---

# Git Workflow Skill

Guided git workflow following a simplified Git Flow branching strategy.

## Workflow

When invoked, ask the user what they want to do:

1. **Start a new feature** (`feature/*`)
2. **Start a bug fix** (`fix/*`)
3. **Create a hotfix** (`hotfix/*`) - for production emergencies
4. **Prepare a release** (`release/*`)
5. **Finish current branch** - merge workflow
6. **Check branch status** - show current state

## Branch Workflows

### 1. New Feature

```bash
git checkout develop
git pull origin develop
git checkout -b feature/<name>
```

Ask user for: Short feature name (kebab-case, e.g., `add-nix-source`)

### 2. Bug Fix

```bash
git checkout develop
git pull origin develop
git checkout -b fix/<name>
```

Ask user for: Short description of the bug (kebab-case, e.g., `history-parsing-crash`)

### 3. Hotfix (Production Emergency)

```bash
git checkout main
git pull origin main
git checkout -b hotfix/<name>
```

Ask user for: Short description (kebab-case)
Remind user: Hotfixes must be merged to BOTH `main` AND `develop`

### 4. Prepare Release

```bash
git checkout develop
git pull origin develop
git checkout -b release/v<version>
```

Ask user for: Version number (e.g., `0.2.0`)

Checklist for release:
- [ ] Update version in `Cargo.toml`
- [ ] Update CHANGELOG.md
- [ ] Run full test suite: `cargo test`
- [ ] Run clippy: `cargo clippy`

### 5. Finish Current Branch

Based on current branch type:

**Feature/Fix → develop:**
```bash
git checkout develop
git pull origin develop
git merge --no-ff <branch>
```

**Release → main:**
```bash
git checkout main
git merge --no-ff release/v<version>
git tag -a v<version> -m "Release v<version>"
git push origin main --tags
git checkout develop
git merge main
```

**Hotfix → main AND develop:**
```bash
git checkout main
git merge --no-ff hotfix/<name>
git tag -a v<version> -m "Hotfix v<version>"
git push origin main --tags
git checkout develop
git merge main
```

### 6. Check Branch Status

Run these commands:
```bash
git status
git branch -vv
git log --oneline -5
```

## Commit Message Format

```
type(scope): short description
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`

## Pre-PR Checklist

- [ ] `cargo test` passes
- [ ] `cargo clippy` has no warnings
- [ ] `cargo fmt` applied
