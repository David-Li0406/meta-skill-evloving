---
type: directory-documentation
directory: .claude/skills/workflow-utilities
title: Workflow Utilities
sibling_claude: CLAUDE.md
parent: null
children:
  - ARCHIVED/README.md
---

# Workflow Utilities

> **Shared utilities for all workflow skills - file operations, TODO management, VCS abstraction, and documentation tools**

Workflow Utilities provides reusable utilities for common workflow tasks used across all skills. It includes file deprecation, directory structure creation, TODO file updates, workflow lifecycle management, VCS abstraction, and documentation maintenance tools.

## Features

- ✅ **File deprecation** - Archive old files (never delete directly)
- ✅ **Directory standards** - Create compliant directory structure
- ✅ **TODO file updates** - Atomic YAML frontmatter updates
- ✅ **Workflow lifecycle** - Register/archive workflows in TODO.md manifest
- ✅ **VCS abstraction** - Unified interface for GitHub/Azure DevOps
- ✅ **Documentation tools** - Version validation, skill creation, doc sync
- ✅ **Archive management** - List and extract archived files

## Quick Start

### Deprecate Files (Never Delete)

```bash
# Archive old files with timestamp
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO_feature_*.md \
  old-auth-flow \
  src/old_auth.py tests/test_old_auth.py

# Creates: ARCHIVED/20251103T143000Z_old-auth-flow.zip
```

### Create Standard Directory

```bash
# Create directory with CLAUDE.md, README.md, ARCHIVED/
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  planning/auth-system
```

### Update TODO Task Status

```bash
# Mark task as complete
python .claude/skills/workflow-utilities/scripts/todo_updater.py \
  TODO_feature_*.md \
  impl_003 \
  complete \
  35  # context usage %
```

### Workflow Lifecycle Management

```bash
# Register new workflow in TODO.md manifest
python .claude/skills/workflow-utilities/scripts/workflow_registrar.py \
  TODO_feature_20251103T143000Z_auth.md \
  feature \
  auth-system \
  --title "User Authentication System"

# Archive completed workflow
python .claude/skills/workflow-utilities/scripts/workflow_archiver.py \
  TODO_feature_20251103T143000Z_auth.md \
  --summary "Implemented OAuth2 authentication" \
  --version "1.6.0"

# Sync TODO.md with filesystem (recovery)
python .claude/skills/workflow-utilities/scripts/sync_manifest.py
```

## Scripts Reference

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `deprecate_files.py` | Archive deprecated files | When replacing old implementations |
| `directory_structure.py` | Create standard directory structure | When creating planning/, specs/ directories |
| `todo_updater.py` | Update task status in TODO files | When marking tasks complete |
| `archive_manager.py` | List and extract archives | When inspecting/recovering archived files |
| `workflow_registrar.py` | Register workflow in TODO.md | Phase 1/2 (after creating TODO file) |
| `workflow_archiver.py` | Archive workflow in TODO.md | Phase 4.4 (after PR merged) |
| `sync_manifest.py` | Sync TODO.md with filesystem | Recovery/verification |
| `validate_versions.py` | Validate version consistency | Before committing skill changes |
| `create_skill.py` | Create new skill with official docs | When adding new skills (rare) |
| `sync_skill_docs.py` | Semi-automated doc sync | After modifying a skill |

## VCS Abstraction Layer

**Unified interface for GitHub and Azure DevOps:**

```python
from vcs.provider import detect_from_remote, VCSProvider
from vcs.github_adapter import GitHubAdapter
from vcs.azure_adapter import AzureDevOpsAdapter

# Auto-detect provider
provider = detect_from_remote()

if provider == VCSProvider.GITHUB:
    adapter = GitHubAdapter()
elif provider == VCSProvider.AZURE_DEVOPS:
    adapter = AzureDevOpsAdapter()

# Create PR (unified interface)
pr_url = adapter.create_pr(
    title="feat: auth system (v1.6.0)",
    body="PR body",
    source_branch="feature/20251103T143000Z_auth",
    target_branch="contrib/stharrold"
)
```

**Supports:**
- GitHub (via `gh` CLI)
- Azure DevOps (via `az` CLI)
- Auto-detection from git remote URL

## Directory Standards

All directories created by workflow-utilities follow standard structure:

```
directory/
├── CLAUDE.md      # Context for Claude Code
├── README.md      # Human-readable documentation
└── ARCHIVED/      # Deprecated files (except if directory IS archived)
    ├── CLAUDE.md
    └── README.md
```

**Enforced by:** `directory_structure.py`

## Best Practices

**File deprecation:**
- ❌ Never delete files directly
- ✅ Always use `deprecate_files.py` to archive

**Directory creation:**
- ❌ Don't manually create directories
- ✅ Use `directory_structure.py` for consistency

**TODO updates:**
- ❌ Don't manually edit TODO YAML frontmatter
- ✅ Use `todo_updater.py` for atomic updates

**Workflow lifecycle:**
- ❌ Don't manually update TODO.md manifest
- ✅ Use `workflow_registrar.py` and `workflow_archiver.py`

**Documentation maintenance:**
- ❌ Don't update versions without validation
- ✅ Use `validate_versions.py` before committing
- ✅ Use `sync_skill_docs.py` after skill changes

**VCS operations:**
- ❌ Don't hardcode GitHub-specific commands
- ✅ Use VCS abstraction layer for portability

## Integration with Other Skills

**All skills depend on workflow-utilities:**

- **bmad-planner:** Uses `directory_structure.py`, `workflow_registrar.py`
- **speckit-author:** Uses `directory_structure.py`, `todo_updater.py`
- **quality-enforcer:** Uses `todo_updater.py` for quality gates
- **git-workflow-manager:** Uses VCS abstraction, workflow lifecycle tools
- **workflow-orchestrator:** Uses workflow lifecycle, context management
- **initialize-repository:** Uses `directory_structure.py`, `create_skill.py` patterns

## Examples

### Complete Workflow Lifecycle

```bash
# Phase 1: Register workflow after BMAD planning
python .claude/skills/workflow-utilities/scripts/workflow_registrar.py \
  TODO_feature_20251103T143000Z_auth.md \
  feature auth-system --title "User Authentication"

# Phase 2-3: Update tasks during implementation
python .claude/skills/workflow-utilities/scripts/todo_updater.py \
  TODO_feature_20251103T143000Z_auth.md impl_001 complete

# Phase 4.4: Archive after PR merged
python .claude/skills/workflow-utilities/scripts/workflow_archiver.py \
  TODO_feature_20251103T143000Z_auth.md \
  --summary "Implemented OAuth2" --version "1.6.0"
```

### Documentation Maintenance

```bash
# Validate version consistency
python .claude/skills/workflow-utilities/scripts/validate_versions.py --verbose

# Sync documentation after skill update
python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \
  bmad-planner 5.2.0
```

## Constants and Rationale

| Constant | Value | Rationale |
|----------|-------|-----------|
| ARCHIVED/ directory | All deprecated files | Preserve history, enable recovery |
| Timestamp format | `YYYYMMDDTHHMMSSZ` | Sortable, parseable, no shell escaping |
| TODO.md manifest | YAML frontmatter | Single source of truth, machine-readable |
| VCS abstraction | Unified interface | Portability, maintainability |

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete technical documentation
- **[CLAUDE.md](CLAUDE.md)** - Claude Code integration guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

**See also:**
- [WORKFLOW.md](../../WORKFLOW.md) - Complete workflow guide
- [UPDATE_CHECKLIST.md](../../.claude/skills/UPDATE_CHECKLIST.md) - Skill update checklist

## Contributing

This skill is part of the workflow system. To update:

1. Modify scripts in `scripts/`
2. Update version in `SKILL.md` frontmatter
3. Document changes in `CHANGELOG.md`
4. Run validation: `python .claude/skills/workflow-utilities/scripts/validate_versions.py`
5. Sync documentation: `python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py workflow-utilities <version>`

## License

Part of the german repository workflow system.
