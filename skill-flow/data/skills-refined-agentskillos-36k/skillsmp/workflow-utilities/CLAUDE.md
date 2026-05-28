---
type: claude-context
directory: .claude/skills/workflow-utilities
purpose: Workflow Utilities provides **shared utilities** for all workflow skills. It includes file deprecation, directory structure creation, CLAUDE.md hierarchy management, VCS abstraction (GitHub/Azure DevOps), documentation maintenance tools, and version validation. All other skills depend on workflow-utilities for consistent file operations.
parent: null
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - scripts/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - bmad-planner
  - speckit-author
  - quality-enforcer
  - git-workflow-manager
  - initialize-repository
  - agentdb-state-manager
---

# Claude Code Context: workflow-utilities

## Purpose

Workflow Utilities provides **shared utilities** for all workflow skills. It includes file deprecation, directory structure creation, CLAUDE.md hierarchy management, VCS abstraction (GitHub/Azure DevOps), documentation maintenance tools, and version validation. All other skills depend on workflow-utilities for consistent file operations.

> **Note**: As of v5.12.0, workflow state tracking has migrated from TODO_*.md files to AgentDB (DuckDB). See `agentdb-state-manager` for the new system. The TODO-related scripts (todo_updater.py, workflow_registrar.py, workflow_archiver.py, sync_manifest.py) have been moved to ARCHIVED/.

## Directory Structure

```
.claude/skills/workflow-utilities/
├── scripts/                        # Active utilities
│   ├── archive_manager.py          # List and extract archives
│   ├── container_utils.py          # Container detection utilities
│   ├── create_skill.py             # Create new skills
│   ├── deprecate_files.py          # Archive deprecated files
│   ├── directory_structure.py      # Create standard directory structure
│   ├── generate_claude_md.py       # Generate missing CLAUDE.md files
│   ├── sync_skill_docs.py          # Documentation sync
│   ├── update_claude_md_refs.py    # Update CLAUDE.md children refs
│   ├── update_claude_references.py # Update CLAUDE.md references
│   ├── validate_versions.py        # Validate version consistency
│   ├── workflow_progress.py        # Workflow progress tracking
│   ├── worktree_context.py         # Worktree state isolation
│   ├── vcs/                        # VCS abstraction layer
│   │   ├── provider.py             # VCS provider detection
│   │   ├── github_adapter.py       # GitHub CLI adapter
│   │   ├── azure_adapter.py        # Azure DevOps adapter
│   │   └── ...
│   └── __init__.py
├── SKILL.md                        # Complete skill documentation
├── CLAUDE.md                       # This file
├── README.md                       # Human-readable overview
├── CHANGELOG.md                    # Version history
└── ARCHIVED/                       # Deprecated scripts
    ├── todo_updater.py             # [DEPRECATED] TODO file updates
    ├── workflow_registrar.py       # [DEPRECATED] TODO.md registration
    ├── workflow_archiver.py        # [DEPRECATED] TODO.md archiving
    ├── sync_manifest.py            # [DEPRECATED] TODO.md sync
    ├── CLAUDE.md
    └── README.md
```

## Key Scripts

### deprecate_files.py

**Purpose:** Archive deprecated files with timestamp into ARCHIVED/ directory (never delete files directly)

**When to use:** When replacing old implementations, removing obsolete files, or deprecating unused code

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  <description> <file1> [file2 ...]
```

**Example:**
```bash
# Deprecate old authentication implementation
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  old-auth-flow \
  src/old_auth.py \
  tests/test_old_auth.py
```

**What it does:**
1. Validates all files to deprecate exist
2. Creates zip archive: `ARCHIVED/<timestamp>_<description>.zip`
3. Moves original files to archive
4. Removes original files from filesystem

**Key features:**
- Preserves file history (no deletion)
- Timestamped archives for traceability
- Validates all files before archiving
- Atomic operation (all or nothing)

---

### directory_structure.py

**Purpose:** Create standard directory structure with required files (CLAUDE.md, README.md, ARCHIVED/)

**When to use:** When creating new directories (planning/, specs/, etc.) to ensure compliance with directory standards

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  <directory>
```

**Example:**
```bash
# Create planning directory with standard structure
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  planning/auth-system
```

**What it does:**
1. Creates directory if it doesn't exist
2. Creates `CLAUDE.md` with template
3. Creates `README.md` with template
4. Creates `ARCHIVED/` subdirectory
5. Creates `ARCHIVED/CLAUDE.md` and `ARCHIVED/README.md`

**Key features:**
- Enforces directory standards consistently
- Idempotent (safe to run multiple times)
- Template-based file creation
- Nested ARCHIVED/ structure

---

### archive_manager.py

**Purpose:** List and extract archived files from ARCHIVED/ directory

**When to use:** When inspecting archived files, recovering deprecated files, or auditing archives

**Invocation:**
```bash
# List archives in ARCHIVED/
python .claude/skills/workflow-utilities/scripts/archive_manager.py list [directory]

# Extract archive to output directory
python .claude/skills/workflow-utilities/scripts/archive_manager.py \
  extract <archive> [output_dir]
```

**Examples:**
```bash
# List all archives
python .claude/skills/workflow-utilities/scripts/archive_manager.py list

# List archives in specific directory
python .claude/skills/workflow-utilities/scripts/archive_manager.py list planning/auth-system

# Extract archive
python .claude/skills/workflow-utilities/scripts/archive_manager.py \
  extract ARCHIVED/20251103T143000Z_old-auth-flow.zip \
  restored/
```

**What it does:**
1. **List mode:** Scans ARCHIVED/ for .zip files, prints archive names and contents
2. **Extract mode:** Extracts archive to output directory (default: `restored/`)

**Key features:**
- Validates archive exists
- Lists archive contents before extraction
- Preserves directory structure on extraction
- Safe extraction (validates zip integrity)

---

### validate_versions.py

**Purpose:** Validate version consistency across SKILL.md and WORKFLOW.md files

**When to use:** Before committing skill changes, before releases, when updating documentation

**Invocation:**
```bash
# Validate all versions
python .claude/skills/workflow-utilities/scripts/validate_versions.py

# Show detailed version information
python .claude/skills/workflow-utilities/scripts/validate_versions.py --verbose

# Attempt auto-fix (use with caution)
python .claude/skills/workflow-utilities/scripts/validate_versions.py --fix
```

**What it does:**
1. Validates all SKILL.md files have valid semantic version in YAML frontmatter
2. Validates WORKFLOW.md has valid version
3. Checks WORKFLOW.md phase descriptions reference correct skill versions
4. Reports inconsistencies

**Key features:**
- Semantic versioning validation (`MAJOR.MINOR.PATCH`)
- Cross-file consistency checks
- Verbose mode for detailed reporting
- Exit code indicates success (0) or failure (1)

---

### create_skill.py

**Purpose:** Create new workflow skill with official Claude Code documentation validation

**When to use:** When adding new skills to workflow system (rare - only 9 skills exist)

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/create_skill.py <skill-name>
```

**Example:**
```bash
# Create new skill
python .claude/skills/workflow-utilities/scripts/create_skill.py my-new-skill
```

**What it does:**
1. Asks configuration questions (purpose, phase, integration)
2. Fetches official Claude Code skill documentation
3. Compares local workflow patterns with official patterns
4. Alerts user if discrepancies exist (with citations)
5. Generates all required files (SKILL.md, CLAUDE.md, README.md, CHANGELOG.md)
6. Creates scripts/ directory with __init__.py
7. Creates ARCHIVED/ with documentation
8. Commits changes to current branch

**Key features:**
- Official docs integration (fetches from docs.claude.com)
- Pattern comparison (local vs official)
- Discrepancy alerts with citations
- Complete file generation
- Automated commit

---

### sync_skill_docs.py

**Purpose:** Semi-automated documentation sync tool for skill updates

**When to use:** After modifying a skill, to propagate changes across all related documentation

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \
  <skill-name> <new-version>
```

**Example:**
```bash
# Sync documentation after updating bmad-planner
python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \
  bmad-planner 5.2.0
```

**What it does:**
1. Updates SKILL.md version in frontmatter
2. Identifies affected sections in WORKFLOW.md
3. Prompts for CHANGELOG entry
4. Creates git commit with proper format
5. Optionally archives previous version

**Key features:**
- Semi-automated (prompts for manual input)
- Updates multiple files consistently
- Enforces semantic versioning
- Proper commit message format

---

### VCS Abstraction Layer (vcs/)

**Purpose:** Provide unified interface for GitHub and Azure DevOps operations (PR creation, issue management)

**When to use:** When creating PRs, managing issues, or working with VCS providers

**Key files:**
- **provider.py** - Auto-detects VCS provider from git remote URL
- **base_adapter.py** - Defines base adapter interface
- **github_adapter.py** - GitHub CLI (gh) adapter
- **azure_adapter.py** - Azure DevOps CLI (az) adapter
- **config.py** - VCS configuration

**Example usage (from git-workflow-manager):**
```python
from .vcs.provider import detect_from_remote
from .vcs.github_adapter import GitHubAdapter
from .vcs.azure_adapter import AzureDevOpsAdapter

# Auto-detect provider
provider = detect_from_remote()

if provider == VCSProvider.GITHUB:
    adapter = GitHubAdapter()
elif provider == VCSProvider.AZURE_DEVOPS:
    adapter = AzureDevOpsAdapter()

# Create PR (unified interface)
pr_url = adapter.create_pr(
    title="feat: auth system (v1.6.0)",
    body="PR body content",
    source_branch="feature/20251103T143000Z_auth",
    target_branch="contrib/stharrold"
)
```

**Key features:**
- Auto-detection from git remote
- Unified interface (GitHub/Azure DevOps)
- CLI-based operations (gh/az)
- Error handling with helpful messages

---

## Usage by Claude Code

### File Deprecation

**Context:** User wants to replace old implementation with new one

**User says:**
- "Replace old auth with new implementation"
- "Deprecate old files"
- "Remove old code"

**Claude Code should:**
```python
import subprocess

# Deprecate old files (NEVER delete directly)
result = subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/deprecate_files.py',
    'old-auth-flow',
    'src/old_auth.py',
    'tests/test_old_auth.py'
], check=True)

print("✓ Old files archived to ARCHIVED/<timestamp>_old-auth-flow.zip")
```

---

### Creating Standard Directories

**Context:** User wants to create new planning or specs directory

**User says:**
- "Create planning directory"
- "Set up specs folder"
- "Make new directory for X"

**Claude Code should:**
```python
import subprocess

# Create directory with standard structure
result = subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/directory_structure.py',
    'planning/auth-system'
], check=True)

# Now directory has: CLAUDE.md, README.md, ARCHIVED/
```

---

### Documentation Maintenance

**Context:** User updated a skill, need to sync documentation

**User says:**
- "Updated bmad-planner to v5.2.0"
- "Sync documentation"
- "Validate versions"

**Claude Code should:**
```python
import subprocess

# Validate version consistency
result = subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/validate_versions.py',
    '--verbose'
], check=False)

if result.returncode != 0:
    print("✗ Version inconsistencies found")
    # Show errors and prompt user

# Sync skill documentation
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/sync_skill_docs.py',
    'bmad-planner',
    '5.2.0'
], check=True)
```

---

### VCS Operations (PR Creation)

**Context:** User wants to create PR, need to detect VCS provider

**User says:**
- "Create PR"
- "Open pull request"

**Claude Code should:**
```python
from pathlib import Path
import sys

# Add vcs module to path
vcs_path = Path('.claude/skills/workflow-utilities/scripts')
sys.path.insert(0, str(vcs_path))

from vcs.provider import detect_from_remote, VCSProvider
from vcs.github_adapter import GitHubAdapter
from vcs.azure_adapter import AzureDevOpsAdapter

# Auto-detect provider
provider = detect_from_remote()

if provider == VCSProvider.GITHUB:
    adapter = GitHubAdapter()
    pr_url = adapter.create_pr(
        title="feat: auth system (v1.6.0)",
        body="PR body",
        source_branch="feature/20251103T143000Z_auth",
        target_branch="contrib/stharrold"
    )
elif provider == VCSProvider.AZURE_DEVOPS:
    adapter = AzureDevOpsAdapter()
    pr_url = adapter.create_pr(
        title="feat: auth system (v1.6.0)",
        body="PR body",
        source_branch="feature/20251103T143000Z_auth",
        target_branch="contrib/stharrold"
    )

print(f"✓ PR created: {pr_url}")
```

---

## Integration with Other Skills

**All skills depend on workflow-utilities:**

**bmad-planner:**
- Uses directory_structure.py to create planning/ directories
- May use deprecate_files.py to archive old planning

**speckit-author:**
- Uses directory_structure.py to create specs/ directories
- May use deprecate_files.py to archive old specs

**quality-enforcer:**
- Uses workflow_progress.py to track quality gate status

**git-workflow-manager:**
- Uses VCS abstraction layer for PR creation
- Uses worktree_context.py for worktree state isolation

**workflow-orchestrator:**
- Uses validate_versions.py to ensure consistency
- Uses workflow_progress.py for phase tracking

**initialize-repository:**
- Uses directory_structure.py to create skill directories
- Uses create_skill.py patterns for new repository setup

**agentdb-state-manager:**
- Workflow state tracking (replaces TODO_*.md workflow)
- See `agentdb-state-manager` for current state tracking system

---

## Directory Standards

All directories created by workflow-utilities follow the standard structure:

```
directory/
├── CLAUDE.md      # Context for Claude Code
├── README.md      # Human-readable documentation
└── ARCHIVED/      # Deprecated files (except if directory IS archived)
    ├── CLAUDE.md
    └── README.md
```

**Enforced by:** directory_structure.py

---

## Best Practices

**File deprecation:**
- ❌ Never delete files directly
- ✅ Always use deprecate_files.py to archive

**Directory creation:**
- ❌ Don't manually create directories
- ✅ Use directory_structure.py for consistency

**CLAUDE.md hierarchy:**
- ❌ Don't manually create CLAUDE.md files
- ✅ Use generate_claude_md.py to create missing files
- ✅ Use update_claude_md_refs.py to update children references

**Workflow state tracking:**
- ❌ Don't use TODO_*.md files (deprecated)
- ✅ Use AgentDB via `agentdb-state-manager` scripts

**Documentation maintenance:**
- ❌ Don't update versions without validation
- ✅ Use validate_versions.py before committing
- ✅ Use sync_skill_docs.py after skill changes

**VCS operations:**
- ❌ Don't hardcode GitHub-specific commands
- ✅ Use VCS abstraction layer for portability

---

## Constants and Rationale

**ARCHIVED/ directory:** All deprecated files go here
- **Rationale:** Preserve file history, enable recovery, audit trail

**Timestamp format:** `YYYYMMDDTHHMMSSZ` (compact ISO8601)
- **Rationale:** Sortable, parseable, no shell escaping issues

**CLAUDE.md hierarchy:** Every directory has CLAUDE.md with parent/child refs
- **Rationale:** AI navigation, context inheritance, documentation consistency

**VCS abstraction:** Unified interface for GitHub/Azure DevOps
- **Rationale:** Portability, maintainability, future-proof

**Semantic versioning:** `MAJOR.MINOR.PATCH`
- **Rationale:** Industry standard, clear upgrade paths

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[UPDATE_CHECKLIST.md](../../UPDATE_CHECKLIST.md)** - Skill update checklist

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived files

## Related Skills

- **workflow-orchestrator** - Uses workflow utilities for phase tracking
- **bmad-planner** - Uses directory_structure.py for planning directories
- **speckit-author** - Uses directory_structure.py for specs directories
- **quality-enforcer** - Uses workflow_progress.py for gate status
- **git-workflow-manager** - Uses VCS abstraction, worktree_context.py
- **initialize-repository** - Uses directory_structure.py, create_skill.py
- **agentdb-state-manager** - Workflow state tracking (replaces TODO_*.md)
