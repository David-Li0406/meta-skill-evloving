---
type: directory-documentation
directory: .claude/skills/initialize-repository
title: Initialize-Repository Meta-Skill
sibling_claude: CLAUDE.md
parent: null
children:
  - ARCHIVED/README.md
---

# Initialize-Repository Meta-Skill

**Phase 0 tool for bootstrapping new repositories with the workflow system.**

## Purpose

The initialize-repository meta-skill replicates the complete workflow system from a source repository to a new target repository. It provides an interactive Q&A system to configure what components get copied and how they're adapted.

## Quick Start

```bash
# Initialize new repository from current repo
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  . ../my-new-project

# Or with absolute paths
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  /path/to/source-repo /path/to/target-repo
```

## What It Does

1. **Validates** source repository has workflow system
2. **Asks questions** about target repository (purpose, tech stack, components)
3. **Copies** 8 workflow skills to target repository
4. **Adapts** documentation (README.md, CLAUDE.md, pyproject.toml)
5. **Creates** compliant directory structure (ARCHIVED/, planning/, specs/)
6. **Initializes git** with 3-branch structure (optional)
7. **Validates** created repository structure
8. **Reports** what was created and next steps

## Components Copied

**Always copied:**
- 8 workflow skills (.claude/skills/)
- Workflow documentation (WORKFLOW.md, CONTRIBUTING.md)
- Quality configurations (pyproject.toml, .gitignore)
- Adapted repository documentation (README.md, CLAUDE.md)

**Optionally copied:**
- Domain-specific content (src/, resources/)
- Sample tests (tests/)
- Container configs (Containerfile, podman-compose.yml)

## Token Efficiency

- **Manual setup:** ~3,500 tokens
- **Callable tool:** ~150 tokens
- **Savings:** ~3,350 tokens (96% reduction)

## When to Use

**For new repositories:**
- Starting a new project that needs the workflow system
- Creating template repository with workflow standards
- Bootstrapping multiple repositories with consistent workflow

**For existing repositories:**
- Migrating existing project to workflow system
- **⚠️ Important:** See [SKILL.md § Applying to Existing Repositories](SKILL.md#applying-to-existing-repositories) for detailed guidance
- Key files (README.md, CLAUDE.md, pyproject.toml) will be overwritten
- Use test-copy approach or careful backup/merge workflow

**NOT part of normal workflow phases (1-6).** This is Phase 0, run once per repository.

## After Initialization

Target repository will have:
- Complete workflow system ready to use
- Customized documentation
- Quality gates configured (≥80% coverage)
- Git branch structure (main, develop, contrib/<user>)
- Master workflow manifest (TODO.md)

Next steps:
1. `cd /path/to/new-repo`
2. `uv sync`
3. Start first feature with BMAD planning

## Documentation

- **[SKILL.md](SKILL.md)** - Complete documentation (558 lines)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code usage context (354 lines)
- **[scripts/initialize_repository.py](scripts/initialize_repository.py)** - Main script (993 lines)

## Version

v1.0.0 - Initial release

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Context for Claude Code
