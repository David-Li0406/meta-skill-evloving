---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Directory Selection Process

Follow this priority order:

### 1. Check Existing Directories

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```

**If found:** Use that directory. If both exist, `.worktrees` wins.

### 2. Check CLAUDE.md

```bash
grep -i "worktree.*directory" CLAUDE.md 2>/dev/null
```

**If preference specified:** Use it without asking.

### 3. Ask User

If no directory exists and no CLAUDE.md preference:

```
No worktree directory found. Where should I create worktrees?

1. Sibling directories (e.g., project-name-feature/) (Recommended - best module resolution)
2. .worktrees/ (project-local, hidden - may have module resolution issues in subfolders)
3. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

**Note:** Sibling directories (option 1) are recommended for projects with complex module resolution (like Nuxt, Next.js) as they avoid symlink and path resolution issues that can occur with nested worktree directories.

## Safety Verification

### For Project-Local Directories (.worktrees or worktrees)

**MUST verify .gitignore before creating worktree:**

```bash
# Check if directory pattern in .gitignore
grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore
```

**If NOT in .gitignore:**

Per Jesse's rule "Fix broken things immediately":
1. Add appropriate line to .gitignore
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents to repository.

### For Global Directory (~/.config/superpowers/worktrees)

No .gitignore verification needed - outside project entirely.

## Creation Steps

### 1. Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create Worktree

```bash
# Determine full path
case $LOCATION in
  sibling)
    # Create sibling directory (e.g., myproject-feature/)
    parent_dir=$(dirname "$(git rev-parse --show-toplevel)")
    path="$parent_dir/${project}-${BRANCH_NAME#feature/}"
    ;;
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="$HOME/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# Create worktree with new branch
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then pnpm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. Verify Clean Baseline

Run tests to ensure worktree starts clean:

```bash
# Examples - use project-appropriate command
pnpm test
cargo test
pytest
go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.

**If tests pass:** Report ready.

### 5. Report Location

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify .gitignore) - may have module issues |
| `worktrees/` exists | Use it (verify .gitignore) - may have module issues |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → Ask user (recommend sibling) |
| Nuxt/Next.js/complex modules | Prefer sibling directories |
| Directory not in .gitignore | Add it immediately + commit |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |

**Best Practice:** Use sibling directories (e.g., `project-name-feature/`) for projects with:
- Complex module resolution (Nuxt, Next.js, etc.)
- Many dependencies
- Monorepo setups
- Build tools that resolve paths from project root

## Common Mistakes

**Using nested directories for complex projects**
- **Problem:** Nuxt/Next.js/modern frameworks may fail to resolve modules in nested `.worktrees/` subdirectories due to symlink handling
- **Fix:** Use sibling directories for projects with complex module resolution

**Skipping .gitignore verification**
- **Problem:** Worktree contents get tracked, pollute git status
- **Fix:** Always grep .gitignore before creating project-local worktree

**Assuming directory location**
- **Problem:** Creates inconsistency, violates project conventions
- **Fix:** Follow priority: existing > CLAUDE.md > ask

**Proceeding with failing tests**
- **Problem:** Can't distinguish new bugs from pre-existing issues
- **Fix:** Report failures, get explicit permission to proceed

**Hardcoding setup commands**
- **Problem:** Breaks on projects using different tools
- **Fix:** Auto-detect from project files (package.json, etc.)

## Example Workflows

### Example 1: Sibling Directory (Recommended for Nuxt/Next.js)

```
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[No existing worktree directories found]
[Ask user preference]
User: Sibling directories

[Create worktree: cd /Users/lova/www && git worktree add antkeeper-news-auth -b feature/auth]
[Run pnpm install]
[Run pnpm test - 47 passing]

Worktree ready at /Users/lova/www/antkeeper-news-auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

### Example 2: Project-Local Directory

```
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[Check .worktrees/ - exists]
[Verify .gitignore - contains .worktrees/]
[Create worktree: git worktree add .worktrees/auth -b feature/auth]
[Run npm install]
[Run npm test - 47 passing]

Worktree ready at /Users/jesse/myproject/.worktrees/auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

## Red Flags

**Never:**
- Create worktree without .gitignore verification (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip CLAUDE.md check

**Always:**
- Follow directory priority: existing > CLAUDE.md > ask
- Verify .gitignore for project-local
- Auto-detect and run project setup
- Verify clean test baseline

## Integration

**Called by:**
- **brainstorming** (Phase 4) - REQUIRED when design is approved and implementation follows
- Any skill needing isolated workspace

