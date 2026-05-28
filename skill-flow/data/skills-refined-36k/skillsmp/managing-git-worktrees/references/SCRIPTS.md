# Worktree Automation Scripts

## Table of Contents
- [Quick Worktree Creation](#quick-worktree-creation)
- [Automated Cleanup](#automated-cleanup)
- [Batch Operations](#batch-operations)
- [Status and Monitoring](#status-and-monitoring)
- [Advanced Workflows](#advanced-workflows)

## Quick Worktree Creation

### Script: create-worktree.sh

Creates a worktree with automatic naming and dependency installation.

**Usage:**
```bash
./scripts/create-worktree.sh <branch-name>
```

**Script:**
```bash
#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

if [ -z "$1" ]; then
    echo -e "${RED}Usage: $0 <branch-name>${NC}"
    echo "Example: $0 feature/search"
    exit 1
fi

BRANCH=$1
PROJECT=$(basename "$(git rev-parse --show-toplevel)")
WORKTREE_PATH="../${PROJECT}-${BRANCH//\//-}"

echo -e "${YELLOW}Creating worktree...${NC}"
echo "Branch: $BRANCH"
echo "Path: $WORKTREE_PATH"

# Check if worktree already exists
if [ -d "$WORKTREE_PATH" ]; then
    echo -e "${RED}Error: Directory already exists: $WORKTREE_PATH${NC}"
    exit 1
fi

# Create worktree
git worktree add -b "$BRANCH" "$WORKTREE_PATH"

# Navigate to worktree
cd "$WORKTREE_PATH"

echo -e "${YELLOW}Installing dependencies...${NC}"
npm install

echo -e "${YELLOW}Running tests...${NC}"
npm test

echo ""
echo -e "${GREEN}Worktree created successfully!${NC}"
echo ""
echo "Next steps:"
echo "  cd $WORKTREE_PATH"
echo "  # Start coding!"
echo ""
echo "When done:"
echo "  git checkout main"
echo "  git merge $BRANCH"
echo "  git worktree remove $WORKTREE_PATH"
```

**Installation:**
```bash
# Claude can create this script
cat > scripts/create-worktree.sh << 'EOF'
[script content above]
EOF

chmod +x scripts/create-worktree.sh
```

**Example Usage:**
```bash
./scripts/create-worktree.sh feature/search
# Creates: ../my-project-feature-search
```

## Automated Cleanup

### Script: cleanup-worktrees.sh

Interactive cleanup script for removing merged worktrees and branches.

**Script:**
```bash
#!/bin/bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Git Worktree Cleanup ===${NC}"
echo ""

# Show current worktrees
echo -e "${YELLOW}Current worktrees:${NC}"
git worktree list
echo ""

# Prune stale worktrees
echo -e "${YELLOW}Checking for stale worktrees...${NC}"
git worktree prune --verbose
echo ""

# Show merged branches
MAIN_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
echo -e "${YELLOW}Merged branches (safe to delete):${NC}"
MERGED_BRANCHES=$(git branch --merged "$MAIN_BRANCH" | grep -v "^\*" | grep -v "$MAIN_BRANCH" || true)

if [ -z "$MERGED_BRANCHES" ]; then
    echo "No merged branches found."
else
    echo "$MERGED_BRANCHES"
    echo ""

    read -p "Delete merged branches? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "$MERGED_BRANCHES" | xargs -r git branch -d
        echo -e "${GREEN}Merged branches deleted.${NC}"
    else
        echo "Skipped branch deletion."
    fi
fi

echo ""

# Check for worktrees with uncommitted changes
echo -e "${YELLOW}Checking for uncommitted changes in worktrees...${NC}"
git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2 | while read wt; do
    if [ -d "$wt" ]; then
        cd "$wt"
        if ! git diff-index --quiet HEAD -- 2>/dev/null; then
            echo -e "${RED}✗ $wt has uncommitted changes${NC}"
        else
            echo -e "${GREEN}✓ $wt is clean${NC}"
        fi
    fi
done

echo ""
echo -e "${GREEN}Cleanup complete!${NC}"
```

**Installation:**
```bash
cat > scripts/cleanup-worktrees.sh << 'EOF'
[script content above]
EOF

chmod +x scripts/cleanup-worktrees.sh
```

**Usage:**
```bash
./scripts/cleanup-worktrees.sh
```

## Batch Operations

### Create Multiple Worktrees

Create several worktrees at once from a list.

**Script:**
```bash
#!/bin/bash
set -e

# List of branches to create worktrees for
BRANCHES=(
    "feature/search"
    "feature/api-search"
    "fix/metadata-parsing"
)

PROJECT=$(basename "$(git rev-parse --show-toplevel)")

for BRANCH in "${BRANCHES[@]}"; do
    WORKTREE_PATH="../${PROJECT}-${BRANCH//\//-}"

    echo "Creating worktree for: $BRANCH"
    git worktree add -b "$BRANCH" "$WORKTREE_PATH"

    echo "Installing dependencies..."
    cd "$WORKTREE_PATH" && npm install && cd -

    echo "✓ Created: $WORKTREE_PATH"
    echo ""
done

echo "All worktrees created successfully!"
git worktree list
```

**Usage:**
```bash
# Edit BRANCHES array in script, then run:
./scripts/create-multiple-worktrees.sh
```

### Remove All Worktrees

Remove all worktrees except the main one.

**Script:**
```bash
#!/bin/bash
set -e

MAIN_WORKTREE=$(git rev-parse --show-toplevel)

echo "Main worktree: $MAIN_WORKTREE"
echo ""
echo "Worktrees to remove:"

git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2 | while read wt; do
    if [[ "$wt" != "$MAIN_WORKTREE" ]]; then
        echo "  - $wt"
    fi
done

echo ""
read -p "Remove all worktrees except main? (y/N) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2 | while read wt; do
        if [[ "$wt" != "$MAIN_WORKTREE" ]]; then
            echo "Removing: $wt"
            git worktree remove "$wt" || git worktree remove --force "$wt"
        fi
    done
    echo "All worktrees removed."
else
    echo "Cancelled."
fi
```

## Status and Monitoring

### Check All Worktrees Status

View git status across all worktrees.

**Script:**
```bash
#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== Worktree Status ==="
echo ""

git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2 | while read wt; do
    if [ -d "$wt" ]; then
        echo -e "${YELLOW}=== $(basename $wt) ===${NC}"
        echo "Path: $wt"
        cd "$wt"

        # Show branch
        BRANCH=$(git branch --show-current)
        echo "Branch: $BRANCH"

        # Show status
        STATUS=$(git status -s)
        if [ -z "$STATUS" ]; then
            echo -e "${GREEN}Status: Clean${NC}"
        else
            echo "Status: Modified"
            git status -s | head -10
        fi

        # Show last commit
        echo "Last commit: $(git log -1 --oneline)"
        echo ""
    fi
done
```

**Usage:**
```bash
./scripts/worktree-status.sh
```

### Disk Space Report

Show disk space used by each worktree.

**Script:**
```bash
#!/bin/bash

echo "=== Worktree Disk Usage ==="
echo ""

TOTAL=0

git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2 | while read wt; do
    if [ -d "$wt" ]; then
        SIZE=$(du -sh "$wt" | cut -f1)
        echo "$SIZE  $(basename $wt)"

        # Also show node_modules size if it exists
        if [ -d "$wt/node_modules" ]; then
            NM_SIZE=$(du -sh "$wt/node_modules" | cut -f1)
            echo "  ↳ node_modules: $NM_SIZE"
        fi
    fi
done

echo ""
echo "Tip: Run 'npm prune' in each worktree to remove unused dependencies"
```

## Advanced Workflows

### Sync All Worktrees with Main

Update all worktrees by merging the latest main branch.

**Script:**
```bash
#!/bin/bash
set -e

MAIN_BRANCH="main"

echo "Syncing all worktrees with $MAIN_BRANCH..."
echo ""

# First, update main branch
MAIN_WORKTREE=$(git rev-parse --show-toplevel)
cd "$MAIN_WORKTREE"
git checkout "$MAIN_BRANCH"
git pull origin "$MAIN_BRANCH"

echo "✓ Main branch updated"
echo ""

# Sync each worktree
git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2 | while read wt; do
    if [[ "$wt" != "$MAIN_WORKTREE" ]]; then
        echo "Syncing: $(basename $wt)"
        cd "$wt"

        BRANCH=$(git branch --show-current)

        # Check for uncommitted changes
        if ! git diff-index --quiet HEAD --; then
            echo "  ⚠ Uncommitted changes - skipping"
            continue
        fi

        # Merge main
        if git merge "$MAIN_BRANCH" --no-edit; then
            echo "  ✓ Merged $MAIN_BRANCH into $BRANCH"
        else
            echo "  ✗ Merge conflict - manual resolution needed"
        fi
        echo ""
    fi
done

echo "Sync complete!"
```

### Run Tests in All Worktrees

Execute tests across all worktrees to verify everything works.

**Script:**
```bash
#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== Running tests in all worktrees ==="
echo ""

FAILED=()

git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2 | while read wt; do
    if [ -d "$wt" ]; then
        echo -e "${YELLOW}Testing: $(basename $wt)${NC}"
        cd "$wt"

        if npm test 2>&1 | grep -q "passing"; then
            echo -e "${GREEN}✓ Tests passed${NC}"
        else
            echo -e "${RED}✗ Tests failed${NC}"
            FAILED+=("$(basename $wt)")
        fi
        echo ""
    fi
done

if [ ${#FAILED[@]} -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
else
    echo -e "${RED}Tests failed in:${NC}"
    printf '%s\n' "${FAILED[@]}"
    exit 1
fi
```

### PR Review Workflow

Automated setup for reviewing pull requests.

**Script:**
```bash
#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <pr-number>"
    echo "Example: $0 123"
    exit 1
fi

PR_NUMBER=$1
PROJECT=$(basename "$(git rev-parse --show-toplevel)")
WORKTREE_PATH="../${PROJECT}-pr-${PR_NUMBER}"

echo "Setting up PR #$PR_NUMBER for review..."

# Fetch PR
git fetch origin "pull/${PR_NUMBER}/head:pr-${PR_NUMBER}"

# Create worktree
git worktree add "$WORKTREE_PATH" "pr-${PR_NUMBER}"

# Setup environment
cd "$WORKTREE_PATH"
npm install

echo ""
echo "PR #$PR_NUMBER ready for review at: $WORKTREE_PATH"
echo ""
echo "Review checklist:"
echo "  npm run lint    # Check code style"
echo "  npm test        # Run tests"
echo "  npm run build   # Test build"
echo ""
echo "View changes:"
echo "  git log main..pr-${PR_NUMBER}"
echo "  git diff main...pr-${PR_NUMBER}"
echo ""
echo "After review:"
echo "  cd ../$(basename $(git rev-parse --show-toplevel))"
echo "  git worktree remove $WORKTREE_PATH"
echo "  git branch -d pr-${PR_NUMBER}"
```

**Usage:**
```bash
./scripts/review-pr.sh 123
```

## Script Management

### Installing All Scripts

Create all scripts at once:

**When user requests worktree automation scripts, Claude should:**

1. Ask which scripts the user wants
2. Create `scripts/` directory if it doesn't exist
3. Create requested scripts with proper permissions
4. Provide usage examples

**Example:**
```bash
# Create scripts directory
mkdir -p scripts

# Create script
cat > scripts/create-worktree.sh << 'EOF'
[script content]
EOF

chmod +x scripts/create-worktree.sh
```

### Best Practices for Scripts

1. **Error handling**: Use `set -e` to exit on errors
2. **User confirmation**: Ask before destructive operations
3. **Colored output**: Use colors for better readability
4. **Documentation**: Include usage examples in comments
5. **Validation**: Check inputs and preconditions
6. **Safety**: Never force operations without confirmation

## Advanced: Shared Dependencies Strategy

**Warning: Use with caution and only when disk space is critical**

### Symlink node_modules (Advanced)

```bash
#!/bin/bash
set -e

MAIN_WORKTREE=$(git rev-parse --show-toplevel)
WORKTREE_PATH=$1

if [ -z "$WORKTREE_PATH" ]; then
    echo "Usage: $0 <worktree-path>"
    exit 1
fi

echo "⚠ Warning: This creates a symlink to shared node_modules"
echo "Changes to package.json will affect all worktrees"
read -p "Continue? (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

cd "$WORKTREE_PATH"

# Remove existing node_modules if present
rm -rf node_modules

# Create symlink to main worktree's node_modules
ln -s "${MAIN_WORKTREE}/node_modules" node_modules

echo "✓ Linked node_modules from main worktree"
echo ""
echo "Caveat: Changes to package.json require:"
echo "  cd $MAIN_WORKTREE && npm install"
```

**Only suggest this script if user explicitly mentions disk space concerns.**

## Resources

All scripts should be:
- Executable: `chmod +x scripts/*.sh`
- Version controlled: Add to git repository
- Documented: Include comments explaining usage
- Safe: Confirm before destructive operations

For project-specific customization, modify the scripts to match your workflow.
