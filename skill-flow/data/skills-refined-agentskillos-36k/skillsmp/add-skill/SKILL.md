---
name: add-skill
description: This skill should be used when the user asks to "install a skill", "add skill from GitHub", "list available skills", "manage skills registry", or mentions "npx add-skill". Provides guidance for installing and tracking agent skills from git repositories.
---

# Add Skill

Install agent skills from any git repository using the `add-skill` CLI.

## When to Use

- Installing skills from GitHub or other git repositories
- Listing available skills from a repository before installation
- Managing skill installations across global and project scopes
- Tracking installed skills in a registry for updates

## Quick Start

### List Available Skills

```bash
npx add-skill vercel-labs/agent-skills --list
```

### Install a Skill

```bash
# Install globally (all projects)
npx add-skill vercel-labs/agent-browser --skill agent-browser --global

# Install to current project
npx add-skill vercel-labs/agent-browser --skill agent-browser
```

### Verify Installation

```bash
ls ~/.claude/skills/       # Global skills
ls .claude/skills/         # Project skills
```

## Source Formats

| Format | Example |
|--------|---------|
| GitHub shorthand | `vercel-labs/agent-skills` |
| Full GitHub URL | `https://github.com/vercel-labs/agent-skills` |
| Specific skill path | `vercel-labs/agent-skills/skills/skill-name` |
| GitLab URL | `https://gitlab.com/org/repo` |
| Any Git URL | `git@github.com:org/repo.git` |

## CLI Options

| Option | Description |
|--------|-------------|
| `-l, --list` | List available skills without installing |
| `-s, --skill <name>` | Install specific skill by name |
| `-g, --global` | Install to user directory (~/.claude/skills/) |
| `-a, --agent <agents...>` | Target specific agents (claude-code, cursor, etc.) |
| `-y, --yes` | Skip all confirmation prompts |
| `-h, --help` | Show help information |

## Installation Locations

| Scope | Path |
|-------|------|
| Project (default) | `.claude/skills/<name>/` |
| Global (`--global`) | `~/.claude/skills/<name>/` |

## Popular Skill Sources

| Source | Description |
|--------|-------------|
| `vercel-labs/agent-skills` | Vercel's curated skill collection |
| `vercel-labs/agent-browser` | Browser automation skill |

## Skill Registry

Track installed skills in a registry for long-term maintenance. After each installation, update the registry to enable batch updates later.

For detailed registry setup, format, and workflows, see **`references/registry.md`**.

### Quick Registry Update

```bash
# Set registry path
REGISTRY=~/.claude/skills/add-skill/registry.json  # Global

# Ensure directory exists
mkdir -p "$(dirname "$REGISTRY")"

# Initialize if needed
[ -f "$REGISTRY" ] || echo '{"$schema":"./registry.schema.json","version":"1.0","skills":{}}' > "$REGISTRY"

# Add skill entry
jq '.skills["agent-browser"] = {
  "source": "vercel-labs/agent-browser",
  "sourceUrl": "https://github.com/vercel-labs/agent-browser",
  "skillPath": "skills/agent-browser",
  "installedAt": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
} | .lastUpdated = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' \
"$REGISTRY" > tmp.json && mv tmp.json "$REGISTRY"
```

## Additional Resources

### Reference Files

- **`references/registry.md`** - Detailed registry setup, format, and maintenance workflows

### Schema Files

- **`registry.schema.json`** - JSON Schema for registry validation

## Notes

- The CLI auto-detects installed agents
- Skills are stored as `SKILL.md` files with YAML frontmatter
- Use `--global` for skills needed across all projects
- Use project-level for project-specific skills
