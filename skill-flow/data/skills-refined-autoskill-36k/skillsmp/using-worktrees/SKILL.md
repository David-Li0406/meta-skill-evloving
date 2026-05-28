---
name: using-worktrees
description: Use when starting feature work that needs isolation - creates git worktrees with smart directory selection, safety verification, and environment setup
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** Systematic directory selection + safety verification + environment setup = reliable isolation.

**Announce at start:** "I'm using gambit:worktree to set up an isolated workspace."

## Rigidity Level

LOW FREEDOM - Follow the 6-step process exactly. No skipping steps. Explicit STOP points must halt execution.

## Quick Reference

| Step | Action | STOP If |
|------|--------|---------|
| 1 | Check existing directories | - |
| 2 | Check CLAUDE.md preference | - |
| 3 | Ask user for preference | No answer received |
| 4 | Verify directory is gitignored | Cannot add to .gitignore |
| 5 | Create worktree | Git command fails |
| 6 | Run environment setup | Setup fails |
| 7 | Verify clean baseline | Tests fail AND user says investigate |
| 8 | Report ready | - |

## When to Use

- Starting feature work that needs isolation from main workspace
- Before executing implementation plans
- Working on multiple features simultaneously
- Experimenting without affecting main workspace

**Don't use for:**
- Quick fixes that don't need isolation
- Single-file changes
- When user explicitly wants to work in current directory

## The Process

### Step 1: Check Existing Directories

**Run these commands in order:**

```bash
ls -d .worktrees 2>/dev/null     # Check first (preferred, hidden)
ls -d worktrees 2>/dev/null      # Check second (alternative)
```

**Decision tree:**
- `.worktrees/` exists → Use it, go to Step 4
- `worktrees/` exists (and no .worktrees) → Use it, go to Step 4
- Both exist → Use `.worktrees/`, go to Step 4
- Neither exists → Go to Step 2

---

### Step 2: Check CLAUDE.md Preference

```bash
grep -i "worktree" CLAUDE.md 2>/dev/null
```

**Decision tree:**
- CLAUDE.md specifies worktree location → Use that location, go to Step 4
- CLAUDE.md exists but no worktree preference → Go to Step 3
- No CLAUDE.md → Go to Step 3

---

### Step 3: Ask User for Preference

**REQUIRED: Use AskUserQuestion tool**

```
AskUserQuestion
  questions:
    - question: "No worktree directory found. Where should I create worktrees?"
      header: "Location"
      options:
        - label: ".worktrees/ (Recommended)"
          description: "Project-local, hidden directory"
        - label: "worktrees/"
          description: "Project-local, visible directory"
        - label: "~/.worktrees/<project>/"
          description: "Global location outside project"
      multiSelect: false
```

**STOP: Wait for user response before proceeding.**

---

### Step 4: Verify Directory is Gitignored

**For project-local directories (.worktrees or worktrees) ONLY:**

```bash
git check-ignore -q .worktrees 2>/dev/null
# OR
git check-ignore -q worktrees 2>/dev/null
```

**Decision tree:**
- Exit code 0 (ignored) → Go to Step 5
- Exit code 1 (not ignored) → Fix it immediately:

```bash
# Add to .gitignore
echo ".worktrees/" >> .gitignore
# OR
echo "worktrees/" >> .gitignore

# Commit the change
git add .gitignore
git commit -m "chore: add worktree directory to gitignore"
```

**STOP if commit fails.** Do not create worktree with unignored directory.

**For global directory (~/.worktrees/):**
- Skip this step entirely - outside project, no gitignore needed

---

### Step 5: Create Worktree

**Determine full path:**

```bash
# Get project name
project=$(basename "$(git rev-parse --show-toplevel)")

# Set path based on location choice
# For .worktrees:
path=".worktrees/$BRANCH_NAME"

# For worktrees:
path="worktrees/$BRANCH_NAME"

# For global:
path="$HOME/.worktrees/$project/$BRANCH_NAME"
```

**Create worktree:**

```bash
git worktree add "$path" -b "$BRANCH_NAME"
```

**STOP if git command fails.** Report error and ask user how to proceed.

**Verify creation:**

```bash
cd "$path"
git status  # Should show clean working tree on new branch
```

---

### Step 6: Run Environment Setup

**Detection order - run FIRST matching setup:**

#### 6a. Devenv/Nix Projects

**Check:**
```bash
[ -f devenv.nix ] || [ -f .envrc ]
```

**If devenv detected:**

1. Check if project uses a database:
```bash
grep -l "DATABASE_URL\|postgres\|mysql" devenv.nix .envrc 2>/dev/null
```

2. If database detected, **REQUIRED: Ask about database strategy:**

```
AskUserQuestion
  questions:
    - question: "This project uses devenv with a database. How should the worktree handle it?"
      header: "Database"
      options:
        - label: "Share database (Recommended)"
          description: "Use same $DATABASE_URL as main. Faster setup, shared data."
        - label: "Isolated database"
          description: "Create new database. Clean slate, but requires migration."
      multiSelect: false
```

**STOP: Wait for user response.**

3. Execute based on choice:

**For shared database:**
```bash
cd "$path"
direnv allow 2>/dev/null || devenv shell
```

**For isolated database:**
```bash
cd "$path"
createdb "${project}_${BRANCH_NAME}"
echo "DATABASE_URL=postgres://localhost/${project}_${BRANCH_NAME}" > .env.local
direnv allow 2>/dev/null || devenv shell
# Run migrations (project-specific - check Makefile or CLAUDE.md)
```

4. **Go to Step 7** (skip other setup types)

#### 6b. Node.js Projects

**Check:**
```bash
[ -f package.json ]
```

**If found:**
```bash
npm install
# OR if yarn.lock exists:
yarn install
# OR if pnpm-lock.yaml exists:
pnpm install
```

**Go to Step 7.**

#### 6c. Rust Projects

**Check:**
```bash
[ -f Cargo.toml ]
```

**If found:**
```bash
cargo build
```

**Go to Step 7.**

#### 6d. Python Projects

**Check:**
```bash
[ -f pyproject.toml ] || [ -f requirements.txt ]
```

**If found:**
```bash
# Poetry
if [ -f pyproject.toml ] && grep -q "tool.poetry" pyproject.toml; then
    poetry install
# Pip
elif [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi
```

**Go to Step 7.**

#### 6e. Go Projects

**Check:**
```bash
[ -f go.mod ]
```

**If found:**
```bash
go mod download
```

**Go to Step 7.**

#### 6f. No Recognized Project Type

**If none of the above match:**
- Report: "No recognized project type. Skipping dependency installation."
- Go to Step 7

---

### Step 7: Verify Clean Baseline

**REQUIRED: Run tests to establish baseline.**

**Detect test command:**

| Project Type | Test Command |
|--------------|--------------|
| Node.js | `npm test` |
| Rust | `cargo test` |
| Python | `pytest` or `python -m pytest` |
| Go | `go test ./...` |
| Devenv | Check Makefile for `test` target |

**Run tests:**

```bash
# Example for Go project
go test ./...
```

**Decision tree based on result:**

- **All tests pass** → Go to Step 8
- **Tests fail** → Present options:

```
Tests failing (N failures) in fresh worktree.

[Show first 3-5 failures]

These failures exist in the base branch. Options:
1. Proceed anyway (failures are known/expected)
2. Investigate before proceeding
3. Cancel worktree creation

Which option?
```

**If user selects "Investigate":**
- **STOP.** Do not proceed until user resolves or changes choice.

**If user selects "Cancel":**
```bash
cd ..
git worktree remove "$path"
```
- **STOP.** Report cancellation.

**If user selects "Proceed":**
- Continue to Step 8, noting known failures.

---

### Step 8: Report Ready

**Format:**
```
Worktree ready at <full-absolute-path>
Branch: <branch-name>
Tests: <N> passing, <M> failures (if any)
Environment: <devenv/npm/cargo/pip/go/none>

Ready to implement <feature-name>
```

**Example:**
```
Worktree ready at /home/dev/myproject/.worktrees/feature-auth
Branch: feature-auth
Tests: 47 passing, 0 failures
Environment: devenv (shared database)

Ready to implement OAuth authentication
```

## Critical Rules

### Rules That Have No Exceptions

1. **Never create project-local worktree without verifying gitignore** → Risk of committing worktree contents
2. **Never skip baseline test verification** → Can't distinguish new bugs from inherited ones
3. **Never proceed with failing tests without explicit permission** → User must acknowledge known failures
4. **Never assume directory location** → Follow priority: existing > CLAUDE.md > ask
5. **Always ask about database strategy for devenv projects** → Database isolation is a critical choice
6. **Always report full absolute path** → User needs exact location for navigation

### Common Excuses

All of these mean: **STOP. Follow the process.**

| Excuse | Reality |
|--------|---------|
| "Directory is probably ignored" | RUN git check-ignore to verify |
| "Tests probably pass" | RUN tests to verify |
| "Same as last time, don't need to ask" | ASK - user preferences can change |
| "Small feature, don't need isolation" | User requested worktree - create it |
| "Can fix gitignore later" | FIX NOW - prevents accidents |

## Anti-patterns

**Never:**
- Create worktree without verifying it's ignored (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip CLAUDE.md check
- Assume database strategy for devenv projects
- Report relative paths (always use absolute)

**Always:**
- Follow directory priority: existing > CLAUDE.md > ask
- Verify directory is ignored for project-local
- Use AskUserQuestion tool for all questions
- Auto-detect and run appropriate project setup
- Ask about database strategy for devenv projects
- Verify clean test baseline
- Report full absolute path, branch, and test status

## Verification Checklist

Before reporting ready:

- [ ] Checked existing directories (.worktrees, worktrees)
- [ ] Checked CLAUDE.md for preference
- [ ] Asked user if no existing preference (using AskUserQuestion)
- [ ] Verified directory is gitignored (project-local only)
- [ ] Added to .gitignore and committed if needed
- [ ] Created worktree with branch (git command succeeded)
- [ ] Detected environment type
- [ ] Asked about database strategy (devenv only, using AskUserQuestion)
- [ ] Ran environment setup
- [ ] Ran tests to verify baseline
- [ ] Got permission if tests failed
- [ ] Reported full absolute path, branch, test status, environment

## Examples

### Good: Complete Workflow

```
Claude: "I'm using gambit:worktree to set up an isolated workspace."

Step 1: Check existing directories
$ ls -d .worktrees 2>/dev/null
.worktrees

Step 4: Verify gitignored (skipped 2-3, directory exists)
$ git check-ignore -q .worktrees && echo "ignored"
ignored

Step 5: Create worktree
$ git worktree add .worktrees/auth -b feature/auth
Preparing worktree (new branch 'feature/auth')
HEAD is now at abc123 Previous commit

Step 6: Environment setup
$ [ -f devenv.nix ] && echo "devenv"
devenv
$ grep -l "DATABASE_URL" devenv.nix
devenv.nix

[AskUserQuestion about database strategy]
User selects: Share database

$ cd .worktrees/auth && direnv allow
direnv: loading .envrc

Step 7: Verify baseline
$ go test ./...
ok  	myproject/...	0.847s
47 tests passed

Step 8: Report
Worktree ready at /home/dev/myproject/.worktrees/auth
Branch: feature/auth
Tests: 47 passing, 0 failures
Environment: devenv (shared database)

Ready to implement OAuth authentication
```

### Bad: Skip Ignore Verification

```
[Check .worktrees/ - doesn't exist]
[Create .worktrees/feature directly without checking ignore]  # WRONG

# Later...
$ git status
Untracked files:
  .worktrees/feature/node_modules/
  .worktrees/feature/src/
  ... (hundreds of files)
```

**Why it fails:**
- Worktree contents pollute git status
- Risk of accidentally committing worktree
- Hard to undo without losing work

### Bad: Proceed with Failing Tests Silently

```
[Create worktree]
[Run tests - 3 failures]
[Continue without asking]  # WRONG

# Later...
[Implement feature]
[Run tests - 5 failures]
# Which 2 failures are new? Can't tell.
```

**Why it fails:**
- Can't distinguish new bugs from pre-existing
- Wastes time debugging inherited failures
- Uncertain baseline undermines confidence

## Integration

**This skill is called by:**
- `gambit:brainstorm` (after design approved)
- Any skill needing isolated workspace

**This skill pairs with:**
- `gambit:finish` - REQUIRED for cleanup after work complete
- `gambit:execute-plan` - Work happens in this worktree

**Workflow:**
```
gambit:brainstorm
    → Design approved
gambit:worktree
    → Check directories (Step 1-3)
    → Verify gitignore (Step 4)
    → Create worktree (Step 5)
    → Environment setup (Step 6)
    → Verify baseline (Step 7)
    → Report ready (Step 8)
gambit:execute-plan
    → Implement in worktree
gambit:finish
    → Merge/PR/cleanup worktree
```
