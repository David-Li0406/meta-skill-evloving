---
type: directory-documentation
directory: .claude/skills/git-workflow-manager
title: Git Workflow Manager
sibling_claude: CLAUDE.md
parent: null
children:
  - ARCHIVED/README.md
---

# Git Workflow Manager

> **Automated git operations for the git-flow + GitHub-flow hybrid workflow with worktrees**

The Git Workflow Manager handles all git automation in the workflow system: branch creation, worktree management, commits, PRs, semantic versioning, and daily rebase operations. It implements a git-flow + GitHub-flow hybrid with isolated worktree development, designed for multi-contributor teams.

## Features

- ✅ **Automated worktree creation** - Isolated development environments per feature/release/hotfix
- ✅ **Semantic versioning** - Automatic version calculation from code changes (MAJOR.MINOR.PATCH)
- ✅ **Daily rebase automation** - Keep contrib branches current with develop using safe force push
- ✅ **Release workflow** - Complete release management (create, tag, back-merge, cleanup)
- ✅ **VCS abstraction** - Works with both GitHub and Azure DevOps
- ✅ **TODO file integration** - Tracks all operations in workflow manifest
- ✅ **Timestamp-based naming** - Avoid shell escaping issues with compact ISO8601 format

## Quick Start

### Prerequisites

```bash
# Ensure you're in a git repository
git status

# Have GitHub CLI or Azure DevOps CLI installed (for PR creation)
gh --version  # GitHub
az --version  # Azure DevOps
```

### Create Feature Worktree

```bash
# From main repo on contrib/<gh-user> branch
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature auth-system contrib/stharrold

# Output:
# ✓ Created worktree: ../german_feature_auth-system
# ✓ Created branch: feature/20251103T143000Z_auth-system
# ✓ Created TODO file: TODO_feature_20251103T143000Z_auth-system.md
#
# Next steps:
#   cd ../german_feature_auth-system
#   python .claude/skills/speckit-author/scripts/create_specifications.py \
#     feature auth-system stharrold --todo-file ../TODO_feature_*.md
```

### Daily Rebase (Keep Current)

```bash
# From main repo
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/stharrold

# Output:
# ✓ Rebased contrib/stharrold onto origin/develop
# ✓ Force pushed with --force-with-lease (safe)
```

### Calculate Semantic Version

```bash
# From feature worktree (after implementation complete)
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.5.0

# Output: 1.6.0
#
# Logic:
# - Breaking changes (API changes, removed features) → MAJOR bump
# - New features (new files, new endpoints) → MINOR bump
# - Bug fixes, refactoring, docs, tests → PATCH bump
```

### Create Release

```bash
# Step 1: Create release branch from develop
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  v1.6.0 develop

# Step 2: Perform final QA, update docs in release branch

# Step 3: Create PR (release/v1.6.0 → main) and merge in GitHub UI

# Step 4: Tag release on main
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  v1.6.0 main

# Step 5: Back-merge to develop
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  v1.6.0 develop

# Step 6: Cleanup release branch
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  v1.6.0
```

## Scripts Reference

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `create_worktree.py` | Create isolated worktree for feature/release/hotfix | Phase 2 (after planning) |
| `daily_rebase.py` | Rebase contrib branch onto develop | Daily maintenance, before PR |
| `semantic_version.py` | Calculate semantic version from changes | Phase 3 (after implementation) |
| `create_release.py` | Create release branch from develop | Phase 5 (when ready for production) |
| `tag_release.py` | Tag release on main after merge | Phase 5 (after release PR merged) |
| `backmerge_release.py` | Merge release back to develop | Phase 5 (keep develop in sync) |
| `cleanup_release.py` | Delete release branch after completion | Phase 5 (final cleanup) |

## Branch Structure

```
main                           ← Production (tagged vX.Y.Z)
  ↑                             ↑
release/vX.Y.Z                hotfix/vX.Y.Z-hotfix.N (worktree)
  ↑
develop                        ← Integration branch
  ↑
contrib/<gh-user>             ← Personal contribution (e.g., contrib/stharrold)
  ↑
feature/<timestamp>_<slug>    ← Isolated feature (worktree)
```

### Workflow Patterns

**Feature workflow:**
1. Main repo (contrib branch) → BMAD planning
2. Create feature worktree → SpecKit + Implementation
3. Quality gates → PR (feature → contrib)
4. Merge in GitHub UI → PR (contrib → develop)

**Release workflow:**
1. Develop ready → Create release branch
2. Final QA + docs → PR (release → main)
3. Tag on main → Back-merge to develop → Cleanup

**Hotfix workflow:**
1. Bug in production → Create hotfix worktree from main
2. Minimal fix → PR (hotfix → main)
3. Tag on main → Back-merge to develop

## Examples

### Create Hotfix Worktree

```bash
# Hotfix for production bug
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  hotfix security-patch main

# Output:
# ✓ Created worktree: ../german_hotfix_security-patch
# ✓ Created branch: hotfix/20251103T150000Z_security-patch
# ✓ Created TODO file: TODO_hotfix_20251103T150000Z_security-patch.md
```

### Create Release Worktree

```bash
# Release workflow
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  release v1.6.0 develop

# Output:
# ✓ Created worktree: ../german_release_v1.6.0
# ✓ Created branch: release/v1.6.0
# ✓ Created TODO file: TODO_release_20251103T160000Z_v1.6.0.md
```

### Timestamp Format

All branches use compact ISO8601 timestamps (`YYYYMMDDTHHMMSSZ`):

```bash
# Feature branch name
feature/20251103T143000Z_auth-system

# Rationale:
# - No colons/hyphens (avoids shell escaping issues)
# - Sortable chronologically
# - Parseable by underscores
# - Remains intact when parsed by scripts
```

### Semantic Versioning Examples

**Scenario 1: Bug fix**
```bash
# Changed: tests/test_auth.py (fixed test bug)
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.5.0

# Output: 1.5.1  (PATCH bump)
```

**Scenario 2: New feature**
```bash
# Changed: src/auth/oauth.py (new file - OAuth support)
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.5.1

# Output: 1.6.0  (MINOR bump)
```

**Scenario 3: Breaking change**
```bash
# Changed: src/api/routes.py (removed /old-endpoint)
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.6.0

# Output: 2.0.0  (MAJOR bump)
```

## Workflow Integration

### Phase 2: Implementation

```bash
# Create feature worktree after BMAD planning
cd ~/Code/german  # main repo
git checkout contrib/stharrold

python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature auth-system contrib/stharrold

# Move to worktree
cd ../german_feature_auth-system

# Create specifications
python .claude/skills/speckit-author/scripts/create_specifications.py \
  feature auth-system stharrold --todo-file ../TODO_feature_*.md

# Implement feature...
```

### Phase 3: Quality

```bash
# In feature worktree after implementation
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# If passed, calculate version
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.5.0

# Output: 1.6.0
```

### Phase 4: Integration

```bash
# Create PR: feature → contrib (done via GitHub/Azure DevOps UI)

# After merge, rebase contrib
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/stharrold

# Create PR: contrib → develop (done via UI)
```

### Phase 5: Release

```bash
# Create release
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  v1.6.0 develop

# QA + docs in release branch...

# Create PR: release → main (done via UI)

# After merge, tag and back-merge
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  v1.6.0 main

python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  v1.6.0 develop

python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  v1.6.0
```

## VCS Provider Support

Works with both GitHub and Azure DevOps via VCS abstraction layer:

```bash
# GitHub repository
# Auto-detects from: git@github.com:user/repo.git

# Azure DevOps repository
# Auto-detects from: git@ssh.dev.azure.com:v3/org/project/repo
```

**PR creation uses:**
- `gh pr create` for GitHub
- `az repos pr create` for Azure DevOps

## TODO File Integration

All git operations create or update TODO files in the main repository:

```bash
# After create_worktree.py
ls TODO_*.md
# TODO_feature_20251103T143000Z_auth-system.md

# TODO file tracks:
# - Workflow type (feature/release/hotfix)
# - Timestamp
# - Slug
# - Current phase
# - Task progress
# - Quality gates status
# - Semantic version
```

## Constants and Rationale

| Constant | Value | Rationale |
|----------|-------|-----------|
| TIMESTAMP_FORMAT | `YYYYMMDDTHHMMSSZ` | No colons/hyphens, sortable, parseable |
| VALID_WORKFLOW_TYPES | feature, release, hotfix | Covers all workflow phases |
| TARGET_BRANCH | `origin/develop` | Integration branch for all contributions |
| Force push safety | `--force-with-lease` | Only pushes if remote unchanged since last fetch |

## Troubleshooting

### Error: "Not in main repository"

```bash
✗ Error: Must run from main repository (not worktree)

Fix: cd to main repository before running script
```

### Error: "Branch already exists"

```bash
✗ Error: Branch feature/20251103T143000Z_auth already exists

Fix: Use different slug or delete existing branch:
  git branch -D feature/20251103T143000Z_auth
  git push origin --delete feature/20251103T143000Z_auth
```

### Error: "Force push failed (--force-with-lease)"

```bash
✗ Error: Force push rejected - remote changed since last fetch

Fix: Someone else pushed to this branch. Fetch and review:
  git fetch origin
  git log contrib/stharrold..origin/contrib/stharrold
  # If safe to overwrite:
  git push origin contrib/stharrold --force
```

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete technical documentation
- **[CLAUDE.md](CLAUDE.md)** - Claude Code integration guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

**See also:**
- [WORKFLOW.md](../../WORKFLOW.md) - Complete 6-phase workflow guide
- [workflow-utilities](../workflow-utilities/) - Shared utilities
- [quality-enforcer](../quality-enforcer/) - Quality gates

## Contributing

This skill is part of the workflow system. To update:

1. Modify scripts in `scripts/`
2. Update version in `SKILL.md` frontmatter
3. Document changes in `CHANGELOG.md`
4. Run validation: `python .claude/skills/workflow-utilities/scripts/validate_versions.py`
5. Sync documentation: `python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py git-workflow-manager <version>`

## License

Part of the german repository workflow system.
