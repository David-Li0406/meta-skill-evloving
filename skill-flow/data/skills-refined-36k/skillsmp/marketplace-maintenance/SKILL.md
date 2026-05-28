---
name: marketplace-maintenance
description: Maintain the Claude Code plugin marketplace - create plugins, add skills, bump versions, update registry. Use when creating new plugins, adding skills/agents/commands to plugins, updating versions, or managing the marketplace registry.
---

# Marketplace Maintenance

## Repository Structure

```
claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json       # Plugin registry (lists all plugins)
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json    # Plugin metadata (name, version, description)
│       ├── CLAUDE.md          # Plugin documentation
│       ├── skills/            # Skill definitions
│       │   └── <skill-name>/
│       │       └── SKILL.md
│       ├── agents/            # Agent definitions
│       │   └── <agent-name>.md
│       ├── commands/          # Slash commands
│       │   └── <command>.md
│       └── scripts/           # Utility scripts
│           └── <script>.sh
└── scripts/
    └── bump-version.sh        # Version management script
```

## Creating a New Plugin

### 1. Create directory structure

```bash
mkdir -p plugins/<plugin-name>/.claude-plugin
mkdir -p plugins/<plugin-name>/skills
mkdir -p plugins/<plugin-name>/agents
mkdir -p plugins/<plugin-name>/commands
```

### 2. Create plugin.json

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "<Brief description>",
  "author": {
    "name": "hanibalsk",
    "url": "https://github.com/hanibalsk"
  },
  "repository": "https://github.com/hanibalsk/claude-marketplace",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

### 3. Create CLAUDE.md

Document the plugin with:
- Overview description
- Skills table (if any)
- Agents table (if any)
- Commands table (if any)
- Usage examples

### 4. Add to marketplace.json

Add entry to `.claude-plugin/marketplace.json` plugins array:

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "<Brief description>",
  "source": "./plugins/<plugin-name>",
  "author": {
    "name": "hanibalsk",
    "url": "https://github.com/hanibalsk"
  },
  "keywords": ["keyword1", "keyword2"]
}
```

## Adding Skills

### Skill file structure

`plugins/<plugin>/skills/<skill-name>/SKILL.md`:

```markdown
---
name: <skill-name>
description: <When to use this skill - triggers on keywords/contexts>
---

# Skill Title

## Content

<Skill content - commands, templates, workflows, etc.>
```

### After adding skills

1. Update plugin's CLAUDE.md with new skill in table
2. Bump version: `./scripts/bump-version.sh <plugin> minor`

## Adding Agents

`plugins/<plugin>/agents/<agent-name>.md`:

```markdown
---
name: <agent-name>
description: <Agent purpose>
model: sonnet  # optional: sonnet, opus, haiku
---

# Agent instructions

<Agent system prompt and behavior>
```

## Adding Commands

`plugins/<plugin>/commands/<command>.md`:

```markdown
---
name: <command>
description: <What the command does>
---

# Command instructions

<What to do when command is invoked>
```

## Version Management

### Bump version script

```bash
# Explicit version
./scripts/bump-version.sh <plugin-name> 1.2.0

# Increment types
./scripts/bump-version.sh <plugin-name> patch  # 1.1.0 → 1.1.1
./scripts/bump-version.sh <plugin-name> minor  # 1.1.0 → 1.2.0
./scripts/bump-version.sh <plugin-name> major  # 1.1.0 → 2.0.0
```

Updates both `plugin.json` and `marketplace.json` automatically.

### When to bump

- **patch**: Bug fixes, typos, minor improvements
- **minor**: New skills, agents, commands added
- **major**: Breaking changes, major restructuring

## Commit Conventions

```bash
# New plugin
git commit -m "feat: add <plugin-name> plugin with <brief description>"

# New skill/agent/command
git commit -m "feat(<plugin>): add <skill/agent/command> for <purpose>"

# Version bump
git commit -m "chore(<plugin>): bump version to X.Y.Z"

# Updates/fixes
git commit -m "fix(<plugin>): <what was fixed>"
```

## Checklist: New Plugin

- [ ] Create plugin directory structure
- [ ] Create `.claude-plugin/plugin.json`
- [ ] Create `CLAUDE.md` with documentation
- [ ] Add skills/agents/commands
- [ ] Add to `marketplace.json`
- [ ] Commit with descriptive message

## Checklist: Add Skills from ZIP

1. Extract ZIP to temp directory
2. Read SKILL.md files to understand content
3. Create skill directories in plugin
4. Copy SKILL.md files
5. Update plugin's CLAUDE.md
6. Bump version (minor)
7. Update marketplace.json version
8. Commit changes
