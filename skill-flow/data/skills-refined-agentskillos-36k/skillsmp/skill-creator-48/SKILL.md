---
name: skill-creator
description: Guidelines for generating new Agent Skills for the Cycle Navigator project. Use this when the user wants to create a new SKILL.md file for a specific component or workflow.
---

# Skill Creator

## Overview
This skill provides structured guidance for creating new Agent Skills that are consistent with the Cycle Navigator project's technical architecture, developer setup, and best practices.

## Required Frontmatter
Every generated skill must start with this exact YAML structure:
```yaml
---
name: lowercase-with-hyphens
description: A clear "Trigger" sentence (e.g., "Use this when...") so Copilot knows when to activate it.
---
```

- **name**: Must be lowercase with hyphens, no spaces. Examples: `skill-creator`, `macro-data-fetcher`, `celery-task-builder`
- **description**: Start with "Use this when..." to provide clear trigger conditions for skill discovery.

## Core Project Context to Include
Always reference these project-specific facts if relevant to the new skill:

- **Environment**: Fedora Linux using Podman/Docker Compose
- **Backend**: FastAPI (Python 3.11+), located in `backend/` directory
- **Database**: PostgreSQL 16 + TimescaleDB (⚠️ hypertables are **irreversible** - always verify before creating)
- **Workers**: Celery using the `backend.celery_app` module
- **Frontend**: Next.js + TypeScript, located in `web/` directory
- **Package Management**: `pyproject.toml` (Python), `package.json` (Node.js)

## Formatting Standards
- Use Markdown headers (`##`, `###`) for clear organization
- Provide example commands using the project's preferred tools:
  - `podman-compose` instead of generic `docker`
  - `pip` with `pyproject.toml` conventions
  - Terminal code blocks with clear explanations
- Include a **Safety/Verification** section for any skill involving:
  - Database schema changes
  - Code deployments
  - Celery task creation
  - Environment modifications

## Folder Structure
Place new skills in:
```
.github/skills/<skill-name>/
├── SKILL.md              # Main instructions (required)
├── examples.md           # Usage examples (optional but recommended)
├── scripts/              # Utility scripts (optional)
│   └── utility.py
```

## Skill Template

Use this as a starting point for new skills:

```markdown
---
name: your-skill-name
description: Brief description of functionality. Use this when [specific trigger or use case].
---

# Your Skill Name

## Overview
[1-2 sentence description of what this skill enables]

## When to Use This Skill
[Explain the trigger conditions clearly]

## Instructions
[Step-by-step guidance for Claude/Copilot to follow]

### Setup
[Any preliminary setup or environment checks]

### Implementation
[Detailed steps]

### Verification
[How to verify the task was completed successfully]

## Examples

### Example 1: [Specific scenario]
[Walkthrough of using the skill in this scenario]

## Safety/Verification
[Important warnings, irreversible operations, or validation steps]

## Troubleshooting
[Common issues and solutions specific to this project]
```

## Version Requirements

Ensure any skill you create acknowledges these project constraints:
- **Python**: 3.11 or higher
- **PostgreSQL**: 16
- **Node.js**: Check `web/package.json` for current LTS version
- **Podman/Docker**: Latest stable versions

## Testing Your Skill

Before finalizing a new skill:
1. **Syntax check**: Validate YAML frontmatter
2. **Context test**: Ensure instructions reference correct file paths and modules
3. **Tool verification**: Confirm any tools or scripts mentioned exist in the project
4. **Trigger clarity**: Verify the description clearly indicates when Copilot should activate this skill

## Examples of Well-Structured Skills

Reference these projects as examples:
- **Dev Agent Skills** (`/fvadicamo/dev-agent-skills`): Git, GitHub, Conventional Commits
- **Supabase Agent Skills** (`/supabase/agent-skills`): Database and API interactions
- **Vercel Agent Skills** (`/vercel-labs/agent-skills`): Deployment and infrastructure

## Tips for Success

- **Be specific**: Use exact module names (`backend.celery_app`, not just `celery`)
- **Include context**: Always mention whether a task affects frontend, backend, or both
- **Warn about irreversibility**: TimescaleDB hypertables, migrations, and schema changes need explicit warnings
- **Reference docs**: Link to [TECHNICAL_ARCHITECTURE.md](../../documents/TECHNICAL_ARCHITECTURE.md) and [DEVELOPER_SETUP.md](../../documents/DEVELOPER_SETUP.md) when relevant
- **Make it actionable**: Skills should enable users to complete tasks without leaving VS Code

## Skills Location

Store all new skills in: `.github/skills/<skill-name>/SKILL.md`

This follows the Agent Skills Standard and ensures consistent discovery by Claude Code and GitHub Copilot.
