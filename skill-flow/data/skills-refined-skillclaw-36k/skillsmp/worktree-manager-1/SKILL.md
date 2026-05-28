---
name: "Worktree Manager"
version: 1.1.0
description: "Manage git worktrees for parallel development with conflict prevention and wave-aware execution strategy. Use when creating feature branches, starting parallel work sessions, merging worktree PRs, or coordinating multiple Claude sessions. Includes dependency analysis for choosing single vs. multiple worktree patterns."
triggers:
  keywords:
    - create worktree
    - parallel development
    - worktree strategy
    - single worktree
    - multiple worktrees
  explicit:
    - /worktree
composes:
  - wave-planner
  - hive-mind
  - linear
---

# Worktree Manager

> **Attribution**: This skill is inspired by [@obra's using-git-worktrees skill](https://github.com/obra/superpowers/blob/main/skills/using-git-worktrees/SKILL.md) from the Superpowers repository and the [git worktree pattern](https://github.com/anthropics/claude-code/issues/1052) documented in claude-code issues.

## What This Skill Does

Creates and manages isolated git worktrees for parallel feature development while **preventing merge conflicts** in shared files like `packages/core/src/index.ts`.

**Key Features**:
1. Smart worktree creation with pre-configured export stubs
2. Rebase-first workflow to prevent conflict cascades
3. Shared file registry for conflict detection
4. Coordination protocol for multi-session development
5. **Wave-aware strategy selection** for agentic execution

---

## Worktree Strategy for Wave-Based Execution

When using wave-planner or hive-mind for multi-agent task execution, choose the right worktree strategy based on **dependency patterns** between waves.

### Decision Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WORKTREE STRATEGY SELECTOR                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Analyze your waves:                                                        │
│                                                                             │
│  Wave 1 ──► Wave 2 ──► Wave 3     SEQUENTIAL DEPENDENCIES                  │
│  (output feeds next wave)         → Use: SINGLE WORKTREE                   │
│                                   → Reason: Waves must run in order        │
│                                   → PR Strategy: Single PR for all waves   │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Wave 1                           INDEPENDENT WAVES                         │
│  Wave 2   (no dependencies)       → Use: MULTIPLE WORKTREES (optional)     │
│  Wave 3                           → Reason: Can run in parallel            │
│                                   → PR Strategy: One PR per wave           │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Wave 1 ──► Wave 2                HYBRID (mixed dependencies)              │
│  Wave 3 ──► Wave 4                → Use: WORKTREE PER DEPENDENCY CHAIN     │
│  (two parallel chains)            → Reason: Chains are independent         │
│                                   → PR Strategy: One PR per chain          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Strategy Comparison

| Strategy | When to Use | Pros | Cons |
|----------|-------------|------|------|
| **Single Worktree** | Sequential waves, shared state, resource-constrained | Simple coordination, single PR, no merge conflicts | No parallelism |
| **Multiple Worktrees** | Independent waves, ample resources | True parallelism, isolated contexts | Merge coordination, multiple PRs |
| **Worktree per Chain** | Mixed dependencies, complex projects | Balanced parallelism, logical grouping | Medium complexity |

### Detecting Dependency Patterns

Before creating worktrees, analyze your issues for dependencies:

```bash
# Check if issues have parent-child relationships
npx tsx ~/.claude/skills/linear/scripts/linear-ops.ts list-sub-issues SMI-XXX

# Check for blocking relationships in issue descriptions
# Look for: "depends on", "blocked by", "requires", "after"
```

**Common dependency indicators:**
- Database migrations must run before code that uses new schema
- API changes must complete before frontend updates
- Shared utilities must be implemented before features using them
- Tests often depend on implementation being complete

### Single Worktree Pattern (Sequential Waves)

Use when waves have dependencies or feed into each other.

**Example: Database Migration Project**
```
Wave 1: Add new category (schema change)
   ↓
Wave 2: Expand categorization rules (uses new category)
   ↓
Wave 3: Run migration and validate (depends on rules)
```

**Setup:**
```bash
# Create ONE worktree for the entire project
git worktree add ../worktrees/category-expansion -b feature/category-expansion

cd ../worktrees/category-expansion

# Execute waves sequentially in the same worktree
./claude-flow swarm --config .claude/hive-mind/category-wave-1.yaml
# Wait for completion...
./claude-flow swarm --config .claude/hive-mind/category-wave-2.yaml
# Wait for completion...
./claude-flow swarm --config .claude/hive-mind/category-wave-3.yaml

# Single PR for all waves
gh pr create --title "feat: Category system expansion (SMI-1675)"
```

**Launch Script Template (Single Worktree, All Waves):**
```bash
#!/bin/bash
# scripts/start-project-worktree.sh
set -e

PROJECT_NAME="category-expansion"
BRANCH_NAME="feature/$PROJECT_NAME"
WORKTREE_PATH="../worktrees/$PROJECT_NAME"
WAVES=(1 2 3)  # Define your waves

# Setup worktree (standard setup - see Quick Start)
# ...

# Create wave execution context
cat > "$WORKTREE_PATH/.claude-context.md" << 'CONTEXT'
# Project: Category System Expansion

## Execution Strategy
Single worktree, sequential waves (dependencies between waves)

## Waves
- Wave 1: SMI-1676 - Add Integrations category
- Wave 2: SMI-1677, SMI-1678 - Expand rules
- Wave 3: SMI-1679, SMI-1680 - Migration and validation

## Dependency Chain
Wave 1 → Wave 2 → Wave 3 (each depends on previous)

## Commands
```bash
# Execute each wave in sequence
./claude-flow swarm --config .claude/hive-mind/category-wave-1.yaml
./claude-flow swarm --config .claude/hive-mind/category-wave-2.yaml
./claude-flow swarm --config .claude/hive-mind/category-wave-3.yaml
```

## Completion
- [ ] All waves executed
- [ ] Tests passing
- [ ] Single PR created and merged
CONTEXT

echo "Worktree ready: $WORKTREE_PATH"
echo "Execute waves sequentially - see .claude-context.md"
```

### Multiple Worktrees Pattern (Independent Waves)

Use when waves are completely independent and can run in parallel.

**Example: Feature Bundle (no dependencies)**
```
Wave 1: Dark mode UI (frontend only)
Wave 2: API rate limiting (backend only)
Wave 3: Documentation refresh (docs only)
```

**Setup:**
```bash
# Create separate worktrees for each wave
git worktree add ../worktrees/dark-mode -b feature/dark-mode
git worktree add ../worktrees/rate-limiting -b feature/rate-limiting
git worktree add ../worktrees/docs-refresh -b feature/docs-refresh

# Run in parallel (separate terminal sessions)
# Terminal 1:
cd ../worktrees/dark-mode && ./claude-flow swarm --config ...

# Terminal 2:
cd ../worktrees/rate-limiting && ./claude-flow swarm --config ...

# Terminal 3:
cd ../worktrees/docs-refresh && ./claude-flow swarm --config ...

# Merge PRs in any order (no conflicts expected)
```

**Coordination for Multiple Worktrees:**

Before creating multiple worktrees, use the **staggered exports strategy** (see Conflict Prevention section) to prevent merge conflicts in shared files.

### Resource Considerations

| Environment | Recommended Strategy | Max Parallel Agents |
|-------------|---------------------|---------------------|
| MacBook (laptop profile) | Single worktree | 2-3 |
| Workstation | 1-2 worktrees | 4-6 |
| Server/CI | Multiple worktrees | 8+ |

**Memory Rule of Thumb:**
- Each Claude agent: ~300-500MB RAM
- Each worktree with Docker: ~200MB additional
- Safe limit: (Available RAM - 4GB) / 500MB = max parallel agents

### Integration with Wave-Planner

When using the wave-planner skill, it will analyze dependencies and recommend a strategy:

```
/wave-planner "Category System Expansion"

Claude: Analyzing 5 issues for dependencies...

Found SEQUENTIAL dependency pattern:
  SMI-1676 (schema) → SMI-1677/1678 (rules) → SMI-1679 (migration) → SMI-1680 (validate)

Recommended: Single worktree for all waves

Options:
A) Single worktree (recommended for this dependency pattern)
B) Multiple worktrees (not recommended - would cause conflicts)
C) Execute in current directory (no worktree isolation)
```

### Hive Config with Worktree Context

When wave-planner generates hive configs, they can include worktree execution context:

```yaml
# .claude/hive-mind/category-wave-1.yaml
name: "Category Expansion Wave 1"

execution:
  strategy: single-worktree
  worktree: ../worktrees/category-expansion
  branch: feature/category-expansion

  # Sequential wave indicator
  wave: 1
  total_waves: 3
  depends_on: null  # First wave

  # PR strategy
  merge_strategy: single-pr  # All waves → one PR
  pr_title: "feat: Category system expansion (SMI-1675)"

agents:
  - type: coder
    issues: [SMI-1676]
```

## Prerequisites

- Git 2.20+ (for worktree support)
- This repository cloned locally
- Understanding of the monorepo structure
- Git-crypt installed and key available (if repo uses encrypted files)
- Varlock configured for secret management (optional but recommended)

## Quick Start

### Creating a New Worktree

```bash
# 1. Ensure you're on main and up-to-date
cd /Users/williamsmith/Documents/GitHub/Smith-Horn/skillsmith
git checkout main && git pull origin main

# 2. If repo uses git-crypt, unlock BEFORE creating worktree
varlock run -- sh -c 'git-crypt unlock "${GIT_CRYPT_KEY_PATH/#\~/$HOME}"'

# 3. Create worktree directory (if not exists)
mkdir -p ../worktrees

# 4. Create worktree for your feature
git worktree add ../worktrees/feature-name -b feature/feature-name

# 5. Navigate to worktree
cd ../worktrees/feature-name

# 6. Verify encrypted files are readable (if applicable)
head -3 docs/architecture/standards.md
```

### Before Starting Work

**CRITICAL**: Check the shared files registry before modifying:

```bash
# Files that commonly cause merge conflicts:
cat << 'EOF'
SHARED FILES - Coordinate before modifying:
- packages/core/src/index.ts (exports)
- packages/core/package.json (dependencies)
- packages/mcp-server/src/index.ts (server exports)
- package.json (root dependencies)
- tsconfig.json (compiler options)
EOF
```

---

## Conflict Prevention Strategy

### The Problem We Solve

When multiple worktrees modify `packages/core/src/index.ts` to add exports, sequential merging causes conflict cascades:

```
Worktree A: adds session exports → merged first ✓
Worktree B: adds benchmark exports → CONFLICT (missing session exports)
Worktree C: adds webhook exports → CONFLICT (missing both)
```

### The Solution: Staggered Exports

**BEFORE creating worktrees**, add stub exports to main:

```typescript
// packages/core/src/index.ts - Add stubs FIRST

// Session (SMI-XXX) - to be implemented
// export * from './session/index.js'

// Benchmarks (SMI-XXX) - to be implemented
// export * from './benchmarks/index.js'

// Webhooks (SMI-XXX) - to be implemented
// export * from './webhooks/index.js'
```

Then each worktree only:
1. Creates its own `src/[feature]/` directory
2. Creates its own `src/[feature]/index.ts`
3. Uncomments its single line in the main index.ts

**Result**: No conflicts because each worktree touches a different line!

---

## Step-by-Step Workflow

### Phase 1: Planning (Before Creating Worktrees)

```bash
# 1. List all planned features
echo "Planned features for this phase:"
echo "- Feature A (SMI-XXX)"
echo "- Feature B (SMI-XXX)"
echo "- Feature C (SMI-XXX)"

# 2. Create stub exports in main
git checkout main
# Edit packages/core/src/index.ts to add commented export stubs

# 3. Commit the stubs
git add packages/core/src/index.ts
git commit -m "chore: add export stubs for Phase X features"
git push origin main

# 4. Create worktree launch scripts (IMPORTANT: Do this during planning!)
# See "Worktree Launch Script Template" below
```

#### Worktree Launch Script Template

**Create launch scripts during planning, not after.** Use this template for each worktree:

```bash
# scripts/start-phaseX-worktree.sh
#!/bin/bash
set -e

WORKTREE_NAME="phaseX-feature-name"
BRANCH_NAME="feature/phaseX-feature-name"
WORKTREE_PATH="../worktrees/$WORKTREE_NAME"
MAIN_REPO="$(pwd)"

echo "Setting up $WORKTREE_NAME worktree..."

# Ensure git-crypt is unlocked in main repo BEFORE creating worktree
if [ -f .gitattributes ] && grep -q "git-crypt" .gitattributes; then
    if git-crypt status docs/ 2>/dev/null | head -1 | grep -q "encrypted:"; then
        echo "Unlocking git-crypt..."
        varlock run -- sh -c 'git-crypt unlock "${GIT_CRYPT_KEY_PATH/#\~/$HOME}"'
    fi
fi

# Create worktree if it doesn't exist
if [ ! -d "$WORKTREE_PATH" ]; then
    git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
fi

cd "$WORKTREE_PATH"

# Sync with main
git fetch origin main
git rebase origin/main || true

# Verify encrypted files are readable
if [ -f docs/architecture/standards.md ]; then
    if head -1 docs/architecture/standards.md | grep -q "^#"; then
        echo "Git-crypt: Unlocked"
    else
        echo "WARNING: Encrypted files may not be readable"
    fi
fi

# Start Docker if needed (for projects using Docker)
if command -v docker &> /dev/null && [ -f docker-compose.yml ]; then
    docker compose --profile dev up -d 2>/dev/null || true
fi

# Create context file for Claude session continuity
cat > .claude-context.md << 'CONTEXT'
# Phase X: Feature Name

## Objective
[Brief description of what this worktree accomplishes]

## Linear Issues
- SMI-XXX: [Description]
- SMI-XXX: [Description]

## Key Files to Modify
- path/to/file1.ts
- path/to/file2.ts

## Completion Criteria
- [ ] Implementation complete
- [ ] Tests passing
- [ ] PR created and merged
CONTEXT

echo ""
echo "Worktree ready at: $WORKTREE_PATH"
echo "Run 'cd $WORKTREE_PATH && claude' to start"
```

Save scripts to `scripts/start-phaseX-*.sh` and make executable with `chmod +x`.

### Phase 2: Creating Worktrees

```bash
# For each feature:
FEATURE="session"  # Change per feature
ISSUE="SMI-641"    # Change per feature

# Create worktree
git worktree add ../worktrees/phase-2c-$FEATURE -b phase-2c-$FEATURE

# Navigate
cd ../worktrees/phase-2c-$FEATURE

# Verify starting point
git log --oneline -1
```

### Phase 3: Development (In Each Worktree)

```bash
# Start of session - always rebase first
git fetch origin main
git rebase origin/main

# Do your work...
# - Create src/[feature]/ directory
# - Implement feature
# - Write tests
# - Uncomment YOUR export line in index.ts

# End of session - commit
git add -A
git commit -m "feat($FEATURE): implement feature ($ISSUE)"
```

### Phase 4: Merging (Sequential, Rebase-First)

```bash
# After first worktree is ready:

# 1. In main repo, merge first PR
git checkout main
git pull origin main
gh pr merge <PR_NUMBER>

# 2. In ALL other worktrees, rebase immediately
cd ../worktrees/phase-2c-other-feature
git fetch origin main
git rebase origin/main
# Resolve any conflicts NOW while context is fresh

# 3. Repeat for each subsequent PR
```

### Phase 5: Cleanup

```bash
# After all PRs merged:
cd /Users/williamsmith/Documents/GitHub/Claude-Skill-Discovery/skillsmith

# Remove worktrees
git worktree remove ../worktrees/phase-2c-session
git worktree remove ../worktrees/phase-2c-perf
git worktree remove ../worktrees/phase-2c-webhooks

# Prune stale worktree references
git worktree prune

# Verify cleanup
git worktree list
```

---

## Worktree Directory Structure

```
/Users/williamsmith/Documents/GitHub/Claude-Skill-Discovery/
├── skillsmith/                    # Main repository
│   ├── .git/                      # Git directory (shared)
│   ├── packages/
│   └── ...
└── worktrees/                     # Worktree container (gitignored)
    ├── phase-2c-session/          # Feature worktree
    │   ├── packages/
    │   └── ...
    ├── phase-2c-perf/             # Feature worktree
    └── phase-2c-webhooks/         # Feature worktree
```

**Important**: The `worktrees/` directory should be:
- Outside the main repo directory
- Added to global gitignore (`~/.gitignore_global`)

---

## Coordination Protocol

### For Multi-Session Development

When running multiple Claude sessions in different worktrees:

#### Session Start Checklist

```bash
# 1. Announce your worktree
echo "Starting work in worktree: $(git worktree list | grep $(pwd))"

# 2. Check for recent changes to shared files
git fetch origin main
git log origin/main --oneline -5 -- packages/core/src/index.ts

# 3. Rebase if needed
git rebase origin/main
```

#### Before Modifying Shared Files

```bash
# Check if another session recently modified the file
git log origin/main --oneline -3 -- packages/core/src/index.ts

# If changes exist, rebase first
git fetch origin main && git rebase origin/main
```

#### Session End Checklist

```bash
# 1. Commit all changes
git add -A && git status

# 2. Push to remote (for PR)
git push origin $(git branch --show-current)

# 3. Notify other sessions to rebase
echo "Pushed changes. Other worktrees should: git fetch && git rebase origin/main"
```

---

## Git-Crypt Considerations

If your repository uses git-crypt for encrypted files (e.g., `docs/`, `.claude/hive-mind/`), worktrees require special handling.

### Key Principle: Unlock Main Repo First

**Git-crypt state is inherited by worktrees.** You must unlock in the main repository BEFORE creating worktrees:

```bash
# 1. Unlock in main repo FIRST
cd /Users/williamsmith/Documents/GitHub/Smith-Horn/skillsmith
varlock run -- sh -c 'git-crypt unlock "${GIT_CRYPT_KEY_PATH/#\~/$HOME}"'

# 2. Verify unlocked (should show plaintext, not binary)
head -5 docs/architecture/standards.md

# 3. THEN create worktree
git worktree add ../worktrees/my-feature -b feature/my-feature

# 4. Worktree inherits unlocked state automatically
cd ../worktrees/my-feature
head -5 docs/architecture/standards.md  # Should also be plaintext
```

### Checking Git-Crypt Status

```bash
# In main repo or any worktree:
git-crypt status docs/ | head -5

# If you see "encrypted:" prefix, files are locked
# If you see "not encrypted:", files are readable
```

### Common Patterns

#### Pattern 1: Encrypted Docs Not Readable in Worktree

**Symptom**: Files in `docs/` or `.claude/hive-mind/` show binary content
**Cause**: Main repo was not unlocked before worktree creation
**Solution**:

```bash
# Go to main repo
cd /path/to/main/repo

# Unlock
varlock run -- sh -c 'git-crypt unlock "${GIT_CRYPT_KEY_PATH/#\~/$HOME}"'

# The worktree should now see decrypted files
cd ../worktrees/my-feature
cat docs/architecture/standards.md  # Now readable
```

#### Pattern 2: CI Linting Fails on Encrypted Files

**Symptom**: ESLint or Prettier fails in CI on encrypted TypeScript/Markdown files
**Cause**: CI doesn't have git-crypt key, so files remain binary
**Solution**:
1. Add encrypted directories to `.prettierignore`
2. Add encrypted patterns to ESLint ignores in `eslint.config.js`
3. See [CI Doctor skill](../ci-doctor/SKILL.md) for detection

```bash
# .prettierignore
docs/
.claude/hive-mind/

# eslint.config.js (flat config)
const globalIgnores = {
  ignores: [
    'docs/**/*.ts',
    // ... other patterns
  ],
}
```

#### Pattern 3: Files Show Encrypted After .gitattributes Change

**Symptom**: Changed `.gitattributes` to exclude files from encryption, but they still show as binary
**Cause**: Changing patterns doesn't auto-decrypt existing files
**Solution**:

```bash
# Force git to re-apply filters
git rm --cached <file>
git add <file>

# Or for directories:
git rm -r --cached docs/templates/
git add docs/templates/

# Verify
git-crypt status docs/templates/
```

### Docker Volume Mounts

**Important**: Docker containers mount from specific paths. Ensure your Docker setup mounts from the worktree, not just the main repo:

```bash
# Check what's actually mounted
docker inspect skillsmith-dev-1 | grep -A5 '"Mounts"'

# If pointing to main repo path, changes in worktree won't be visible
# Solution: Restart Docker from within the worktree directory:
cd ../worktrees/my-feature
docker compose --profile dev down
docker compose --profile dev up -d
```

### Worktree Launch Script with Git-Crypt

Add this to your worktree launch script:

```bash
#!/bin/bash
set -e

MAIN_REPO="/Users/williamsmith/Documents/GitHub/Smith-Horn/skillsmith"
WORKTREE_PATH="../worktrees/$1"

# Ensure git-crypt is unlocked in main repo
if git-crypt status docs/ 2>/dev/null | grep -q "encrypted:"; then
  echo "Unlocking git-crypt in main repo..."
  cd "$MAIN_REPO"
  varlock run -- sh -c 'git-crypt unlock "${GIT_CRYPT_KEY_PATH/#\~/$HOME}"'
fi

# Now create/navigate to worktree
cd "$WORKTREE_PATH" 2>/dev/null || {
  cd "$MAIN_REPO"
  git worktree add "$WORKTREE_PATH" -b "$2"
  cd "$WORKTREE_PATH"
}

# Verify encrypted files are readable
if head -1 docs/architecture/standards.md 2>/dev/null | grep -q "^#"; then
  echo "Git-crypt: Unlocked (docs readable)"
else
  echo "WARNING: Encrypted files may not be readable"
fi
```

---

## Handling Merge Conflicts

### If Conflicts Occur During Rebase

```bash
# 1. See which files conflict
git status

# 2. For index.ts conflicts, combine all exports
# Open the file and ensure ALL exports from both versions are present

# 3. Mark resolved
git add packages/core/src/index.ts

# 4. Continue rebase
git rebase --continue
```

### Cherry-Pick Recovery (Last Resort)

If worktree is too far behind and rebasing is painful:

```bash
# 1. Note your unique commits
git log --oneline origin/main..HEAD

# 2. Create clean branch from current main
git checkout main && git pull
git checkout -b phase-2c-feature-clean

# 3. Cherry-pick your commits
git cherry-pick <commit1> <commit2>

# 4. Resolve conflicts during cherry-pick
# Then create new PR from clean branch
```

---

## Scripts

The skill includes helper scripts in `scripts/`:

| Script | Purpose |
|--------|---------|
| `worktree-create.sh` | Create a new worktree with branch |
| `worktree-status.sh` | Show status of all worktrees |
| `worktree-sync.sh` | Sync all worktrees with main |
| `worktree-cleanup.sh` | Clean up merged worktrees |
| `generate-launch-script.sh` | Generate Claude Code launch script |

### Generating Launch Scripts for Parallel Claude Sessions

Use `generate-launch-script.sh` to create terminal scripts that:
1. Navigate to the worktree
2. Sync with origin/main
3. Check Docker container health
4. Display the task prompt
5. Launch Claude Code

```bash
# With prompt file
./scripts/generate-launch-script.sh ../worktrees/smi-619 SMI-619 "CI/CD Docker" prompt.md

# With inline prompt
echo "Configure CI/CD pipeline with Docker" | \
  ./scripts/generate-launch-script.sh ../worktrees/smi-619 SMI-619 "CI/CD Docker"
```

### Key Learning: Claude Code Invocation

**WRONG** (causes "requires valid session ID" error):
```bash
claude --resume "Execute task..."  # --resume expects a UUID, not a prompt!
```

**CORRECT** (display prompt, then launch interactive claude):
```bash
cat << 'PROMPT'
================================================================================
SMI-XXX: Task Title
================================================================================

## IMPORTANT: Use Docker Skill
Run /docker before executing any npm commands.

[Task details...]

## When Done
1. Commit with conventional commit message
2. Push to remote
3. Create PR
================================================================================
PROMPT

claude
```

### Docker Container Health Check

Include this in launch scripts when the project uses Docker:

```bash
# Check if Docker container is running
if ! docker ps --filter name=skillsmith-dev-1 --format "{{.Status}}" | grep -q "Up"; then
  echo "Starting Docker container..."
  docker compose --profile dev up -d
  sleep 3
fi
```

### scripts/worktree-create.sh

```bash
./scripts/worktree-create.sh <feature-name> [issue-id] [base-branch]

# Examples:
./scripts/worktree-create.sh session SMI-641
./scripts/worktree-create.sh webhooks SMI-645 main
./scripts/worktree-create.sh hotfix-auth
```

### scripts/worktree-sync.sh

Syncs all worktrees with origin/main via rebase:

```bash
./scripts/worktree-sync.sh [--dry-run]
```

### scripts/worktree-status.sh

Shows status of all worktrees with behind/ahead counts:

```bash
./scripts/worktree-status.sh [--verbose]
```

### scripts/worktree-cleanup.sh

Removes worktrees that have been merged:

```bash
./scripts/worktree-cleanup.sh [--all] [--force] [worktree-name]
```

---

## Troubleshooting

### Issue: "fatal: 'path' is already checked out"

**Cause**: Trying to create worktree for branch that's already checked out
**Solution**:
```bash
# Check where it's checked out
git worktree list

# Either use that worktree or create new branch
git worktree add ../worktrees/new-name -b new-branch-name
```

### Issue: Cannot delete branch used by worktree

**Cause**: Branch is still associated with a worktree
**Solution**:
```bash
# Remove the worktree first
git worktree remove ../worktrees/feature-name

# Then delete the branch
git branch -d feature-name
```

### Issue: Stale worktree references

**Cause**: Worktree directory was deleted manually
**Solution**:
```bash
git worktree prune
```

### Issue: Massive conflicts in index.ts

**Cause**: Didn't use staggered exports strategy
**Solution**: Use cherry-pick recovery (see above)

### Issue: Encrypted files showing binary in worktree

**Cause**: Main repo was not unlocked before creating the worktree
**Solution**:
```bash
# Go to main repo and unlock
cd /path/to/main/repo
varlock run -- sh -c 'git-crypt unlock "${GIT_CRYPT_KEY_PATH/#\~/$HOME}"'

# Worktree will now inherit unlocked state
cd ../worktrees/my-feature
cat docs/architecture/standards.md  # Should be readable
```

### Issue: Git-crypt unlock succeeds but files still encrypted

**Cause**: Git smudge filter not triggered for existing files
**Solution**:
```bash
# Force re-checkout of encrypted files
git checkout -- docs/

# Or manually apply smudge filter
for f in docs/**/*.md; do
  cat "$f" | git-crypt smudge > "/tmp/$(basename $f)"
  mv "/tmp/$(basename $f)" "$f"
done
```

### Issue: ESLint/Prettier failing in CI on encrypted files

**Cause**: CI environment doesn't have git-crypt key, files remain binary
**Solution**:
1. Add encrypted directories to `.prettierignore`
2. Add encrypted patterns to ESLint config ignores
3. See [CI Doctor skill](../ci-doctor/SKILL.md) for automated detection

### Issue: Docker changes not visible in worktree

**Cause**: Docker container mounted from main repo path, not worktree path
**Solution**:
```bash
# Check current mounts
docker inspect skillsmith-dev-1 | grep -A5 '"Source"'

# Restart Docker from worktree directory
cd ../worktrees/my-feature
docker compose --profile dev down
docker compose --profile dev up -d
```

---

## Best Practices Summary

1. **Always start from fresh main**: `git checkout main && git pull`
2. **Unlock git-crypt before creating worktrees** (if repo uses encryption)
3. **Add export stubs before creating worktrees**
4. **Rebase frequently**: After each merge to main
5. **One feature per worktree**: Keep changes isolated
6. **Merge in order of completion**: Rebase remaining after each merge
7. **Clean up promptly**: Remove worktrees after merge
8. **Verify Docker mounts**: Ensure container mounts from correct worktree path

---

## Related Resources

- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree)
- [obra/superpowers](https://github.com/obra/superpowers) - Original inspiration
- [Claude Code Worktree Pattern](https://github.com/anthropics/claude-code/issues/1052)

---

## Changelog

### v1.1.0 (2026-01-22)
- **New**: Wave-aware worktree strategy selection
- Added decision framework for single vs. multiple worktrees
- Added dependency pattern detection guidance
- Integration points with wave-planner skill
- Hive config worktree context examples
- Resource considerations by environment (laptop/workstation/server)
- Launch script template for sequential wave execution

### v1.0.0 (2025-12)
- Initial release
- Smart worktree creation with export stubs
- Rebase-first workflow
- Git-crypt integration
- Multi-session coordination protocol

---

**Created**: December 2025
**Updated**: January 2026
**Scope**: Internal - Smith-Horn/skillsmith repository
**Maintainer**: Project team
**Related**: [wave-planner](~/.claude/skills/wave-planner/SKILL.md), [hive-mind](.claude/skills/hive-mind/SKILL.md)
