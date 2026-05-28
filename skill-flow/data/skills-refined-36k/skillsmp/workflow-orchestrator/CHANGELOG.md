# Changelog - workflow-orchestrator

All notable changes to the Workflow Orchestrator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Auto-detection of current workflow phase
- Resumable workflows after context checkpoints

## [5.1.0] - 2025-11-08

### Added
- **Phase 4.3: PR Feedback via Work-Items (Optional)**
  - Generate work-items from unresolved PR conversations
  - Decision tree for simple fixes vs. substantive changes requiring work-items
  - Workflow pattern: PR → generate work-items → approve PR → fix work-items in separate features
  - Compatible with GitHub Issues and Azure DevOps Work Items
- Updated workflow phase map with 8-step Phase 4 (was 5 steps)
  - 4.1: Create PR
  - 4.2: Reviewers add comments
  - 4.3: Generate work-items (optional)
  - 4.4: Approve PR
  - 4.5: Archive workflow
  - 4.6: Update BMAD (optional)
  - 4.7: Rebase contrib
  - 4.8: Create PR (contrib → develop)

### Changed
- Updated SKILL.md with work-item generation invocation and benefits
- Updated CLAUDE.md Workflow Phase Map with detailed Phase 4 steps
- Extended Phase 4 from integration-only to include PR feedback handling
- Added guidance on when to use work-item generation vs. direct fixes

### Integration
- Coordinates git-workflow-manager's generate_work_items_from_pr.py script
- Leverages workflow-utilities VCS abstraction layer
- Supports iterative work-item resolution (each work-item follows Phase 2-4)

### Documentation
- Added decision tree for PR feedback handling
- Documented work-item slug pattern: pr-{pr_number}-issue-{sequence}
- Clarified that work-item generation is optional (for substantive changes only)

## [5.0.0] - 2025-10-23

### Added
- Progressive skill loading architecture
- Phase-based skill coordination
- Context-aware skill selection (main repo vs worktree)
- User confirmation prompts before actions
- TODO file state management at 100K token checkpoint
- Templates for TODO, WORKFLOW.md, CLAUDE.md

### Changed
- Migrated from monolithic workflow to modular orchestration
- Skills loaded on-demand per phase (not all at once)

### Token Efficiency
- **Previous (monolith):** ~2,718 tokens all at once
- **New (orchestrator):** ~300 tokens initial, ~600-900 per phase
- **Savings:** Progressive loading reduces active context significantly

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[../../CHANGELOG.md](../../CHANGELOG.md)** - Repository-wide changelog
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
