---
type: claude-context
directory: .claude/skills/git-workflow-manager
purpose: Git Workflow Manager provides **automated git operations** for the git-flow + GitHub-flow hybrid workflow with worktrees. It handles branch creation, worktree management, commits, PRs, semantic versioning, and daily rebase operations. All operations are designed to work with the isolated worktree development pattern and VCS provider abstraction (GitHub/Azure DevOps).
parent: null
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - scripts/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - speckit-author
  - quality-enforcer
  - workflow-utilities
  - bmad-planner
  - agentdb-state-manager
---

# Claude Code Context: git-workflow-manager

## Purpose

Git Workflow Manager provides **automated git operations** for the git-flow + GitHub-flow hybrid workflow with worktrees. It handles branch creation, worktree management, commits, PRs, semantic versioning, and daily rebase operations. All operations are designed to work with the isolated worktree development pattern and VCS provider abstraction (GitHub/Azure DevOps).

> **Note**: As of v5.12.0, workflow state tracking has migrated from TODO_*.md files to AgentDB (DuckDB). Some scripts in this skill (create_worktree.py, cleanup_feature.py) still reference TODO files but will be updated in a future release. See `agentdb-state-manager` for the current state tracking system.

## Directory Structure

```
.claude/skills/git-workflow-manager/
├── scripts/                      # Git operation automation
│   ├── create_worktree.py        # Create feature/release/hotfix worktrees (Phase 2)
│   ├── cleanup_feature.py        # Atomic cleanup: archive TODO + delete worktree + delete branches (Phase 4)
│   ├── daily_rebase.py          # Rebase contrib onto develop (daily maintenance)
│   ├── semantic_version.py       # Calculate semantic version from changes (Phase 3)
│   ├── create_release.py         # Create release branch from develop (Phase 5)
│   ├── tag_release.py            # Tag release on main after merge (Phase 5)
│   ├── backmerge_workflow.py     # Backmerge workflow orchestrator (Step 7)
│   ├── cleanup_release.py        # Cleanup release branch after completion (Phase 5)
│   └── __init__.py               # Package initialization
├── templates/                    # (none - no template files)
├── SKILL.md                      # Complete skill documentation
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
├── CHANGELOG.md                  # Version history
└── ARCHIVED/                     # Deprecated files
    ├── backmerge_release.py      # [DEPRECATED] Replaced by backmerge_workflow.py
    ├── CLAUDE.md
    └── README.md
```

## Key Scripts

### create_worktree.py

**Purpose:** Create isolated worktree for feature/release/hotfix development with automatic TODO file creation

**When to use:** Phase 2 (Implementation) - after BMAD planning (optional), before SpecKit

**Invocation:**
```bash
# Feature worktree from contrib branch
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature <slug> contrib/<gh-user>

# Release worktree from develop
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  release <version> develop

# Hotfix worktree from main
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  hotfix <slug> main
```

**Examples:**
```bash
# Feature: Create feature/20251104T143000Z_auth-system from contrib/stharrold
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature auth-system contrib/stharrold

# Release: Create release/v1.6.0 from develop
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  release v1.6.0 develop

# Hotfix: Create hotfix/20251104T150000Z_security-patch from main
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  hotfix security-patch main
```

**What it does:**
1. Validates workflow type (feature/release/hotfix) and slug format
2. Generates timestamp in compact ISO8601 format (YYYYMMDDTHHMMSSZ)
3. Creates branch: `<type>/<timestamp>_<slug>` or `release/<version>`
4. Creates worktree directory: `../german_<type>_<slug>/`
5. Creates TODO file: `TODO_<type>_<timestamp>_<slug>.md` in **main repo**
6. Initializes TODO with YAML frontmatter and basic structure
7. Prints worktree path and instructions

**Key features:**
- Timestamp format avoids shell escaping issues (no colons/hyphens)
- TODO file stored in main repo (not worktree) for persistence
- Validates base branch exists
- Creates compliant directory structure
- Error handling with cleanup on failure

---

### cleanup_feature.py

**Purpose:** Atomically archive TODO and cleanup feature worktree in correct order: Archive TODO → Delete worktree → Delete branches

**When to use:** Phase 4 (Integration) - after PR merged to contrib

**⚠️ CRITICAL:** This script prevents orphaned TODO files by enforcing proper cleanup ordering. Manual cleanup is error-prone and NOT recommended.

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py \
  <slug> \
  --summary "Completion summary" \
  --version "X.Y.Z"
```

**Examples:**
```bash
# Cleanup feature
python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py \
  auth-system \
  --summary "Implemented user authentication with JWT tokens" \
  --version "1.5.0"

# Cleanup issue fix
python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py \
  issue-243-todo-status \
  --summary "Updated TODO file to reflect completion" \
  --version "1.13.0"

# Cleanup with project-specific worktree pattern
python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py \
  auth-system \
  --summary "Implemented user authentication" \
  --version "1.5.0" \
  --project-name german
```

**What it does:**
1. **Finds TODO file:** Searches for `TODO_feature_*_{slug}.md` in main repo
2. **Finds worktree:** Searches for `../feature_{slug}/` or `../{project}_feature_{slug}/`
3. **Finds branch:** Searches for `feature/*_{slug}` branch
4. **Archives TODO:** Calls `workflow_archiver.py` (MUST succeed before proceeding)
5. **Deletes worktree:** Removes worktree directory (only if archive succeeded)
6. **Deletes branches:** Removes local and remote branches (only if worktree deletion succeeded)

**Key features:**
- **Atomic operation:** Either everything succeeds or nothing changes (safe to retry)
- **Correct ordering:** Cannot delete worktree without archiving TODO first
- **Error handling:** If TODO archive fails, worktree/branches NOT deleted (safe state)
- **Single command:** Replaces 4 separate manual commands
- **Clear feedback:** Emojis and progress indicators for each step

**Why atomic cleanup:**
- Prevents orphaned TODO files (main repo cleanup issue)
- Prevents confusion about workflow state
- Safe rollback on errors (idempotent)
- Single source of truth for cleanup logic

**Failure modes:**
- **TODO not found:** Script fails immediately, nothing deleted
- **Archive fails:** Script exits, worktree/branches preserved (safe to retry)
- **Worktree deletion fails:** TODO archived, but worktree remains (manual cleanup instructions provided)
- **Branch deletion fails:** TODO archived, worktree deleted, but branches remain (manual cleanup instructions provided)

---

### daily_rebase.py

**Purpose:** Rebase contrib branch onto develop to stay current with integration branch

**When to use:** Daily maintenance, before starting new work, before creating PR

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/<gh-user>
```

**Example:**
```bash
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/stharrold
```

**What it does:**
1. Validates branch starts with `contrib/`
2. Checks for uncommitted changes (fails if dirty)
3. Checks out contrib branch
4. Fetches from origin
5. Rebases onto origin/develop
6. Force pushes with `--force-with-lease` (safe force push)

**Key features:**
- Safe force push: `--force-with-lease` prevents overwriting others' work
- Validates clean working tree before rebase
- Comprehensive error handling
- Target branch: `origin/develop` (documented rationale)

---

### semantic_version.py

**Purpose:** Calculate semantic version automatically based on code changes

**When to use:** Phase 3 (Quality Gates) - after implementation, before PR

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  <base-branch> <current-version>
```

**Example:**
```bash
# From feature branch, compare to develop, current version v1.5.0
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.5.0

# Output: 1.6.0 (if new features detected)
```

**What it does:**
1. Compares changed files between current branch and base branch
2. Analyzes changes using semver rules:
   - **MAJOR** (X.0.0): Breaking changes (API changes, removed features)
   - **MINOR** (1.X.0): New features (new files in src/, new endpoints)
   - **PATCH** (1.5.X): Bug fixes, refactoring, docs, tests
3. Calculates next version from current version + change type
4. Outputs new version (e.g., `1.6.0`)

**Key features:**
- Automatic version calculation (no manual decisions)
- File-based change analysis
- Semantic versioning compliance
- Used by quality-enforcer to update TODO frontmatter

---

### create_release.py

**Purpose:** Create release branch from develop for final QA and release preparation

**When to use:** Phase 5 (Release) - when develop is ready for production

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  <version> <base-branch>
```

**Example:**
```bash
# Create release/v1.6.0 from develop
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  v1.6.0 develop
```

**What it does:**
1. Validates version format (vX.Y.Z)
2. Creates branch: `release/<version>` from base branch
3. Creates TODO file: `TODO_release_<timestamp>_<version-slug>.md`
4. Initializes TODO with YAML frontmatter
5. Prints instructions for next steps

**Key features:**
- Version format validation (semantic versioning)
- TODO file tracking for release workflow
- Prevents duplicate release branches

---

### tag_release.py

**Purpose:** Tag release on main branch after PR merge

**When to use:** Phase 5 (Release) - after merging release PR to main

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  <version> <branch>
```

**Example:**
```bash
# Tag v1.6.0 on main branch
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  v1.6.0 main
```

**What it does:**
1. Validates version format (vX.Y.Z)
2. Checks out specified branch (usually main)
3. Creates annotated git tag: `<version>`
4. Pushes tag to origin
5. Updates CHANGELOG.md (if exists)

**Key features:**
- Annotated tags (includes message)
- Version validation
- Automatic CHANGELOG updates

---

### backmerge_workflow.py

**Purpose:** Orchestrate backmerge of release changes to develop (Step 7)

**When to use:** Step 7 (/7_backmerge) - after tagging release on main

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py <step>
```

**Available steps:**
- `pr-develop` - Create PR from release branch to develop
- `rebase-contrib` - Rebase contrib on updated develop
- `cleanup-release` - Delete release branch
- `full` - Run all steps in sequence
- `status` - Show current backmerge status

**Example:**
```bash
# Create PR from release to develop
python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop

# After PR merged, rebase contrib
python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py rebase-contrib

# Cleanup release branch
python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py cleanup-release
```

**What it does:**
1. Creates PR from release branch to develop
2. (Manual) User merges PR in GitHub UI
3. Rebases contrib branch on updated develop
4. Deletes release branch

**Key features:**
- Uses release branch directly (no separate backmerge branch)
- Returns to editable branch (contrib) at end
- Handles merge conflicts gracefully
- Idempotent (safe to re-run)

---

### cleanup_release.py

**Purpose:** Delete release branch after successful completion

**When to use:** Phase 5 (Release) - after back-merge completes

**Invocation:**
```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  <version>
```

**Example:**
```bash
# Delete release/v1.6.0 locally and remotely
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  v1.6.0
```

**What it does:**
1. Validates release is tagged and merged
2. Deletes local branch: `release/<version>`
3. Deletes remote branch: `origin/release/<version>`
4. Archives TODO file to ARCHIVED/

**Key features:**
- Safety checks (tag must exist, branch must be merged)
- Cleans up both local and remote branches
- Archives release TODO file

---

## Usage by Claude Code

### Phase 2: Create Feature Worktree

**Context:** User wants to start implementing a feature

**User says:**
- "Create feature worktree for auth system"
- "Start working on new feature"
- "Begin implementation"

**Claude Code should:**
```python
import subprocess

# Call create_worktree.py
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/create_worktree.py',
    'feature',
    'auth-system',  # slug
    'contrib/stharrold'  # base branch
], check=True)

# After worktree created, move to SpecKit (Phase 2.3)
```

---

### Daily Maintenance: Rebase Contrib

**Context:** User starts new session or before creating PR

**User says:**
- "Rebase my branch"
- "Update contrib branch"
- "Sync with develop"

**Claude Code should:**
```python
import subprocess

# Call daily_rebase.py
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/daily_rebase.py',
    'contrib/stharrold'
], check=True)
```

---

### Phase 3: Calculate Version

**Context:** Implementation complete, need semantic version for PR

**User says:**
- "What version should this be?"
- "Calculate semantic version"
- "Run quality gates"

**Claude Code should:**
```python
import subprocess

# Call semantic_version.py
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/semantic_version.py',
    'develop',  # base branch
    'v1.5.0'    # current version
], capture_output=True, text=True, check=True)

new_version = result.stdout.strip()  # e.g., "1.6.0"

# Use new_version in TODO file, PR title, etc.
```

---

### Phase 4: Handle PR Feedback via Work-Items

**Context:** PR reviewed, has unresolved conversations requiring follow-up work

**User says:**
- "Generate work-items from PR feedback"
- "Create issues for PR #94 conversations"
- "Extract unresolved PR comments"

**Claude Code should:**
```python
import subprocess

# Call generate_work_items_from_pr.py
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/generate_work_items_from_pr.py',
    '94'  # PR number
], capture_output=True, text=True, check=True)

# Script outputs work-item URLs and slugs
# Example output:
# ✓ Found 3 unresolved conversations
# ✓ Created work-item: pr-94-issue-1 (https://github.com/user/repo/issues/123)
# ✓ Created work-item: pr-94-issue-2 (https://github.com/user/repo/issues/124)
# ✓ Created work-item: pr-94-issue-3 (https://github.com/user/repo/issues/125)

# For each work-item, create feature worktree
work_items = ['pr-94-issue-1', 'pr-94-issue-2', 'pr-94-issue-3']
for slug in work_items:
    # User approves PR in web portal first
    # Then create worktree for each work-item
    subprocess.run([
        'python',
        '.claude/skills/git-workflow-manager/scripts/create_worktree.py',
        'feature',
        slug,
        'contrib/stharrold'
    ], check=True)
```

**Complete PR Feedback Workflow:**
```python
import subprocess

# Step 1: Feature branch merged to contrib via PR
# (User merges PR #94 in GitHub/Azure DevOps UI)

# Step 2: Generate work-items from unresolved conversations
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/generate_work_items_from_pr.py',
    '94'
], capture_output=True, text=True, check=True)

# Step 3: For first work-item, create feature worktree
subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/create_worktree.py',
    'feature',
    'pr-94-issue-1',
    'contrib/stharrold'
], check=True)

# Step 4: Implement fix in worktree
# (SpecKit, implementation, quality gates)

# Step 5: Create PR: feature/YYYYMMDDTHHMMSSZ_pr-94-issue-1 → contrib/stharrold
# Step 6: User merges PR in web portal
# Step 7: Repeat steps 3-6 for remaining work-items

# Step 8: After all work-items resolved, approve original PR in web portal
```

**Integration with GitHub:**
```python
import subprocess
import json

# For GitHub repositories
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/generate_work_items_from_pr.py',
    '94'
], capture_output=True, text=True, check=True)

# Creates GitHub issues with:
# - Label: "pr-feedback"
# - Label: "pr-94"
# - Title: "PR #94 feedback: {conversation summary}"
# - Body: Full conversation with file/line context
# - Links to original PR

# Check created issues
issues = subprocess.run([
    'gh', 'issue', 'list',
    '--label', 'pr-94',
    '--json', 'number,title,url'
], capture_output=True, text=True, check=True)

issue_list = json.loads(issues.stdout)
# [{'number': 123, 'title': 'PR #94 feedback: ...', 'url': '...'}, ...]
```

**Integration with Azure DevOps:**
```python
import subprocess
import json

# For Azure DevOps repositories
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/generate_work_items_from_pr.py',
    '94'
], capture_output=True, text=True, check=True)

# Creates Azure DevOps tasks with:
# - Type: Task
# - Tags: "pr-feedback", "pr-94"
# - Title: "PR #94 feedback: {thread subject}"
# - Description: Full thread content with file context
# - Relations: Links to PR URL

# Check created work-items
work_items = subprocess.run([
    'az', 'boards', 'work-item', 'list',
    '--query', "[?fields.'System.Tags' contains 'pr-94']",
    '--output', 'json'
], capture_output=True, text=True, check=True)

item_list = json.loads(work_items.stdout)
# [{'id': 456, 'fields': {'System.Title': 'PR #94 feedback: ...'}, ...}, ...]
```

---

### Phase 5: Release Workflow

**Context:** Develop ready for production release

**User says:**
- "Create release"
- "Prepare v1.6.0 for production"
- "Start release process"

**Claude Code should execute sequence:**
```python
import subprocess

# Step 1: Create release branch
subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/create_release.py',
    'v1.6.0',
    'develop'
], check=True)

# Step 2: User performs QA, updates docs in release branch

# Step 3: User creates PR (release/v1.6.0 → main) and merges in GitHub UI

# Step 4: Tag release on main
subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/tag_release.py',
    'v1.6.0',
    'main'
], check=True)

# Step 5: Back-merge to develop
subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/backmerge_release.py',
    'v1.6.0',
    'develop'
], check=True)

# Step 6: Cleanup release branch
subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/cleanup_release.py',
    'v1.6.0'
], check=True)
```

---

## Integration with Other Skills

**workflow-orchestrator:**
- Orchestrator calls create_worktree.py at Phase 2 start
- Orchestrator calls semantic_version.py at Phase 3
- Orchestrator calls daily_rebase.py as needed

**speckit-author:**
- SpecKit runs in worktrees created by create_worktree.py
- SpecKit reads TODO file created by create_worktree.py

**quality-enforcer:**
- Quality enforcer calls semantic_version.py to calculate version
- Updates TODO frontmatter with semantic_version result

**workflow-utilities:**
- Uses workflow_archiver.py to archive TODO files
- Uses vcs abstraction for PR creation (gh/az cli)

**bmad-planner:**
- BMAD planning happens before create_worktree.py
- Worktree references ../planning/<slug>/ for context

---

## Git-Flow + GitHub-Flow Hybrid

This skill implements a hybrid workflow:

**Git-Flow elements:**
- Long-lived branches: main, develop, contrib/<user>
- Feature branches from contrib
- Release branches from develop
- Hotfix branches from main

**GitHub-Flow elements:**
- PRs for all merges
- Short-lived feature branches
- Continuous integration via develop
- Worktree isolation

**Worktree pattern:**
- Feature work happens in isolated worktrees
- TODO files stored in main repo (persistent)
- Clean separation between main repo and worktrees

---

## Constants and Rationale

**TIMESTAMP_FORMAT:** `YYYYMMDDTHHMMSSZ` (compact ISO8601)
- **Rationale:** No colons/hyphens avoids shell escaping issues. Remains intact when branch names are parsed by underscores.

**VALID_WORKFLOW_TYPES:** `['feature', 'release', 'hotfix']`
- **Rationale:** Supports all workflow phases with clear naming

**TARGET_BRANCH:** `origin/develop`
- **Rationale:** Integration branch for all contributions. All contrib branches rebase onto develop.

**Force push safety:** `--force-with-lease`
- **Rationale:** Only force-pushes if remote hasn't changed since last fetch. Prevents accidental overwrites.

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[WORKFLOW.md](../../WORKFLOW.md)** - Complete 6-phase workflow guide

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived files

## Related Skills

- **workflow-orchestrator** - Calls git-workflow-manager scripts
- **speckit-author** - Runs in worktrees created by this skill
- **quality-enforcer** - Uses semantic_version.py
- **workflow-utilities** - Provides VCS abstraction and TODO utilities
- **bmad-planner** - Planning happens before worktree creation
