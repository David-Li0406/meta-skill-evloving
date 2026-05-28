---
name: install
description: Install Claude tools from this repository to global or project locations
allowed-tools: AskUserQuestion, Bash(python*), Read, Glob
argument-hint: [list]
---

# Install Skill

Discovers and installs Claude tools (skills, agents, commands) from this repository.

## Quick Reference

| Command | Action |
|---------|--------|
| `/install` | Interactive installation wizard |
| `/install list` | Show available tools |

## Workflow

### Step 1: Discover Available Tools

Run the discovery script:
```bash
python {SKILL_DIR}/install.py --list
```

This shows all tools in the repository with their components:
- **skills/** - Skill definitions with optional scripts/, references/, assets/
- **agents/** - Agent definition markdown files
- **commands/** - Legacy command markdown files

### Step 2: Gather User Choices

Use AskUserQuestion to get:

1. **Target location:**
   - Global (`~/.claude/`) - Available in all projects
   - Project (`.claude/`) - Only available in current project

2. **Installation mode:**
   - Copy - Files are copied (portable, independent)
   - Symlink - Links to source (updates automatically, requires repo access)

3. **Tools to install:**
   - Present discovered tools as multi-select checkboxes

### Step 3: Execute Installation

Run the installation with user choices:
```bash
python {SKILL_DIR}/install.py --install --target <global|project> --mode <copy|symlink> --tools <tool1,tool2,...>
```

### Step 4: Report Results

Show the user what was installed:
- Skills installed to `{target}/skills/{tool_name}/`
- Agents installed to `{target}/agents/` (flat)
- Commands installed to `{target}/commands/` (flat)

## Installation Mapping

| Source | Destination |
|--------|-------------|
| `{tool}/skills/` (entire tree) | `{target}/skills/{tool}/` |
| `{tool}/agents/*.md` | `{target}/agents/` (flat) |
| `{tool}/commands/*.md` | `{target}/commands/` (flat) |

## Example Session

```
User: /install

Claude: Let me discover available tools...

[Runs: python install.py --list]

Available tools:
  brainstorming/ [skills, agents]
  scribe/ [skills with scripts]
  viz/ [skills with scripts]
  duckdb_sql/ [skills]

[Uses AskUserQuestion for target, mode, and tool selection]

User selects: Global, Symlink, brainstorming + viz

Claude: Installing...

[Runs: python install.py --install --target global --mode symlink --tools brainstorming,viz]

Installation complete!
  Linked skills/brainstorming/ -> /path/to/repo/brainstorming/skills
  Linked skills/viz/ -> /path/to/repo/viz/skills
  Linked agents/pragmatic-explorer.md
  Linked agents/creative-challenger.md
  Linked agents/devils-advocate.md
```

## Handling "list" Argument

If the user runs `/install list`, skip the interactive workflow and just display the tool list:
```bash
python {SKILL_DIR}/install.py --list
```

## Notes

- Symlink mode requires the repository to remain accessible
- Copy mode creates independent copies that won't auto-update
- Existing installations are replaced (no merge)
- The skill directory structure is preserved (SKILL.md, scripts/, references/, assets/)
