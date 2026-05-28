# Changelog - git-workflow-manager

All notable changes to the Git Workflow Manager skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Enhanced worktree cleanup with validation

## [5.2.0] - 2025-11-09

### Added
- **Pre-PR rebase in backmerge_release.py** - Ensures clean, linear git history
  - Added `rebase_release_branch()` function to rebase release branch onto target before PR
  - Eliminates "branch out-of-date" warnings in GitHub/Azure DevOps UI
  - Prevents merge commits in back-merge PRs (maintains linear history)
  - Automatic conflict detection with helpful resolution instructions
  - Uses `--force-with-lease` for safe force push after rebase

### Changed
- **backmerge_release.py** - Now rebases before creating PR (Step 3 added to workflow)
  - Updated main() workflow: validate → check clean → rebase → create PR
  - Updated docstring with rebase requirements and rationale
  - Updated WORKFLOW.md to document pre-PR rebase pattern

### Fixed
- **Back-merge PRs no longer require merge commits** - Identified during v1.9.0 release (PR #127)
  - Previous behavior: Created PR without rebasing, causing "branch out-of-date" warnings
  - New behavior: Rebases first, then creates PR with clean linear history

## [5.1.0] - 2025-11-08

### Added
- `generate_work_items_from_pr.py` - Generate work-items from unresolved PR conversations
  - Extracts unresolved conversations from GitHub PRs (GraphQL API) or Azure DevOps PRs (CLI)
  - Creates separate work-items (GitHub issues or Azure DevOps tasks) for each conversation
  - Work-item slug pattern: `pr-{pr_number}-issue-{sequence}` (e.g., pr-94-issue-1)
  - Supports both GitHub and Azure DevOps workflows
  - Enables PR approval while tracking feedback as separate feature work
  - Compatible with all issue trackers (GitHub Issues, Azure DevOps Work Items)

### Removed
- `handle_pr_feedback.py` - Removed iterative PR feedback implementation (Option B)
  - Replaced with work-item generation approach (Option A) for better tracker compatibility
  - Work-item generation enables cleaner separation of concerns and broader VCS support

### Changed
- Updated SKILL.md with comprehensive work-item generation documentation
- Updated CLAUDE.md with Phase 4 PR feedback workflow examples
- Added decision tree for simple fixes vs. work-item generation

### Token Efficiency
- No additional token cost (pure git/VCS CLI operations)
- Work-item generation script handles PR analysis without consuming context

## [5.0.0] - 2025-10-23

### Added
- `create_worktree.py` - Feature/hotfix/release worktree creation
- `create_release.py` - Release branch creation from develop
- `tag_release.py` - Tag release on main after PR merge
- `backmerge_release.py` - Back-merge release to develop
- `cleanup_release.py` - Cleanup release branch after completion
- `daily_rebase.py` - Rebase contrib branch onto develop
- `semantic_version.py` - Automatic version calculation

### Changed
- Git operations now use standalone scripts
- Worktree creation creates TODO files automatically
- Semantic versioning based on change analysis

### Token Efficiency
- Scripts handle git operations without consuming context
- No token impact (pure git operations)

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[../../CHANGELOG.md](../../CHANGELOG.md)** - Repository-wide changelog
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
