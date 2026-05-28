# Changelog - workflow-utilities

All notable changes to the Workflow Utilities skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- `sync_skill_docs.py` - Documentation sync automation

## [5.2.0] - 2025-11-08

### Added
- **VCS Adapter PR Feedback Methods:**
  - `fetch_pr_comments(pr_number)` - Fetch review comments from pull request
    - GitHub: Uses `gh pr view --json reviews,comments`
    - Azure DevOps: Uses `az repos pr show --query threads`
    - Returns unified comment format (author, body, file, line, timestamp)
  - `update_pr(pr_number, title, body)` - Update pull request title or description
    - GitHub: Uses `gh pr edit`
    - Azure DevOps: Uses `az repos pr update`
  - `get_pr_status(pr_number)` - Get pull request approval and merge status
    - GitHub: Uses `gh pr view --json state,mergeable,reviews`
    - Azure DevOps: Uses `az repos pr show --query status,mergeStatus`
    - Returns state, mergeable, approved, reviews_required

### Changed
- Updated `base_adapter.py` with three new abstract methods for PR feedback
- Updated `github_adapter.py` with GitHub-specific PR feedback implementations
- Updated `azure_adapter.py` with Azure DevOps-specific PR feedback implementations
- Updated SKILL.md with comprehensive VCS abstraction documentation
- Extended VCS abstraction beyond PR creation to full PR lifecycle management

### Integration
- Used by `git-workflow-manager/scripts/generate_work_items_from_pr.py`
- Enables work-item generation from unresolved PR conversations
- Supports both GitHub Issues and Azure DevOps Work Items

### Token Efficiency
- No additional token cost (pure CLI operations)
- Unified interface reduces context needed for VCS-specific operations

## [5.1.0] - 2025-11-03

### Added
- **Workflow lifecycle management scripts:**
  - `workflow_registrar.py` - Register workflows in TODO.md active list
  - `workflow_archiver.py` - Archive workflows and update TODO.md manifest
  - `sync_manifest.py` - Rebuild TODO.md from filesystem state
- TODO.md master manifest management capabilities
- Phase 4.3 workflow archival automation

### Changed
- Extended scope from "file utilities" to "workflow lifecycle utilities"
- Updated SKILL.md with workflow management documentation
- Added workflow lifecycle usage examples

### Fixed
- Gap: Phase 4.3 archival had no implementation (now workflow_archiver.py)
- Gap: TODO.md workflows.active[] never updated (now workflow_registrar.py)
- Gap: No recovery mechanism for TODO.md (now sync_manifest.py)

## [5.0.0] - 2025-10-23

### Added
- `deprecate_files.py` - File deprecation with timestamped archives
- `archive_manager.py` - Archive management (list, extract)
- `todo_updater.py` - TODO file manifest management
- `directory_structure.py` - Compliant directory creation

### Changed
- All utilities follow consistent error handling patterns
- Shared constants and validation logic

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[../../CHANGELOG.md](../../CHANGELOG.md)** - Repository-wide changelog
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
