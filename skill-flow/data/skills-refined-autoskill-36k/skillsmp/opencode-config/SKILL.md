---
name: opencode-config
description: >
  Manage OpenCode configuration - skills, agents, commands, rules, profiles,
  and MCP servers. Triggers: creating skills, editing config files, setting up
  profiles, adding slash commands, configuring agents, or troubleshooting
  OpenCode setup issues.
license: MIT
compatibility: opencode
---

# OpenCode Configuration Skill

Manage and customize OpenCode configuration including skills, agents, commands, rules, and profiles.

## When This Skill MUST Be Used

**ALWAYS invoke this skill when the user's request involves ANY of these:**

- Creating or editing skills, agents, commands, or rules
- Configuring profiles (base, personal, work)
- Setting up MCP servers
- Editing `opencode.json` configuration
- Troubleshooting OpenCode configuration issues

**If editing any file in `~/.config/opencode*/`, use this skill.**

## Critical Safety Rules

**NEVER:**
- Edit files in `~/.config/opencode*/` directly - edit source in `~/.dotfiles/` instead
- Delete configuration without user confirmation
- Put secrets in configuration files (use `{env:VAR}` substitution)

**ALWAYS:**
- Edit source files in `~/.dotfiles/config/opencode*/` (symlinks point there)
- Create symlinks after adding new components
- Test components after creating them

## Quick Reference

| Component | Location (in dotfiles) | Docs |
|-----------|------------------------|------|
| Main config | `opencode.json` | [Config](https://opencode.ai/docs/config/) |
| Global instructions | `AGENTS.md` | [Rules](https://opencode.ai/docs/rules/) |
| Skills | `skills/<name>/SKILL.md` | [Skills](https://opencode.ai/docs/skills/) |
| Agents | `agents/<name>.md` | [Agents](https://opencode.ai/docs/agents/) |
| Commands | `commands/<name>.md` | [Commands](https://opencode.ai/docs/commands/) |
| Rules | `rules/<category>/*.md` | [Rules](https://opencode.ai/docs/rules/) |
| Custom Tools | `tools/<name>.ts` | [Custom Tools](https://opencode.ai/docs/custom-tools/) |
| Plugins | `plugins/<name>.ts` | [Plugins](https://opencode.ai/docs/plugins/) |
| MCP Servers | `opencode.json` → `mcp` | [MCP](https://opencode.ai/docs/mcp-servers/) |
| Themes | `themes/<name>.json` | [Themes](https://opencode.ai/docs/themes/) |

---

# Profile System

## Architecture

```
~/.dotfiles/config/                    # SOURCE OF TRUTH (version controlled)
├── opencode/                          # Base profile - shared by ALL profiles
│   ├── opencode.json
│   ├── AGENTS.md
│   ├── skills/
│   ├── agents/
│   ├── commands/
│   └── rules/
│
├── opencode-d3fvxl/                   # Personal profile
│   ├── opencode.json
│   └── skills/                        # + agents/, commands/, rules/ as needed
│
└── opencode-efg/                      # Work profile
    ├── opencode.json
    └── skills/

~/.config/opencode*/                   # RUNTIME (symlinks + local files)
├── opencode.json -> ~/.dotfiles/...   # Symlinked files
├── AGENTS.md -> ~/.dotfiles/...
├── skills/
│   └── <name>/
│       └── SKILL.md -> ~/.dotfiles/...
├── agents/
│   └── <name>.md -> ~/.dotfiles/...
├── package.json, bun.lock             # Local (not in dotfiles)
└── node_modules/                      # Local
```

## Current Profiles

| Profile | Launch | Skills |
|---------|--------|--------|
| Base | `opencode` | Language idioms, testing, code-review, verification |
| d3fvxl | `oc d3fvxl` | + github, yandex |
| EFG | `oc efg` | + glab, jira, gcp |

## Adding a New Profile

```bash
# 1. Create dotfiles structure
mkdir -p ~/.dotfiles/config/opencode-<name>/{skills,agents,commands,rules}
cat > ~/.dotfiles/config/opencode-<name>/opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json"
}
EOF

# 2. Create runtime directory structure
mkdir -p ~/.config/opencode-<name>/{skills,agents,commands,rules}

# 3. Symlink config files
ln -s ~/.dotfiles/config/opencode-<name>/opencode.json ~/.config/opencode-<name>/

# 4. Add to PROFILE_GH_USERS in ~/.bashrc
declare -A PROFILE_GH_USERS=(
  [d3fvxl]="d3fvxl"
  [efg]="m-bovtunov_eslfg"
  [<name>]="<github-username>"  # Add new profile
)

# 5. Use with: oc <name>
```

**Note:** Each profile is isolated - they don't inherit from base. Symlink individual components from base if you want to share them.

The `switch` function in `.bashrc` handles:
- GitHub auth switching (`gh auth switch`)
- Copilot config symlink (`~/.copilot`)
- OpenCode config dir (`OPENCODE_CONFIG_DIR`)

---

# Creating Components

## Naming Convention

Skills, agents, and commands follow the pattern `<language>-<name>` for language-specific components:

| Language | Prefix | Examples |
|----------|--------|----------|
| Go | `go-` | `go-idioms`, `go-test`, `go-code-reviewer`, `/go-review` |
| Rust | `rust-` | `rust-idioms`, `rust-test` |
| Python | `python-` | `python-idioms`, `python-test` |

Language-agnostic components have no prefix: `doot`, `docker-best-practices`, `opencode-config`

## Where to Put Components

| Shared (all profiles) | Profile-specific |
|-----------------------|------------------|
| `~/.dotfiles/config/opencode/` | `~/.dotfiles/config/opencode-<profile>/` |
| Language idioms, testing, code review | Company tools, personal cloud |

## Skills

Create `skills/<name>/SKILL.md`:

```markdown
---
name: skill-name
description: >
  Brief description. Triggers: keyword1, keyword2, tool-name.
---

# Skill Name

## When This Skill MUST Be Used

- Trigger condition 1
- Trigger condition 2

## Critical Safety Rules

**NEVER:** dangerous actions
**ALWAYS:** required practices

## Quick Reference

| Task | Command |
|------|---------|
| Task 1 | `command` |
```

**Requirements:**
- `name`: 1-64 chars, lowercase alphanumeric with hyphens, must match directory name
- `description`: 1-1024 chars, include trigger keywords

**After creating:** `mkdir -p ~/.config/.../skills/<name> && ln -s ~/.dotfiles/.../skills/<name>/SKILL.md ~/.config/.../skills/<name>/`

## Agents

Create `agents/<name>.md`:

```markdown
---
description: What this agent does
mode: subagent
model: anthropic/claude-sonnet-4-5
tools:
  write: false
  edit: false
permission:
  bash: ask
---

You are a specialized agent for...
```

**Key options:** `description` (required), `mode` (primary/subagent), `model`, `temperature`, `maxSteps`, `tools`, `permission`, `hidden`

## Commands

Create `commands/<name>.md`:

```markdown
---
description: Brief description shown in command list
agent: build
---

Run task with $ARGUMENTS.
Include output: !`git status`
Reference file: @src/main.go
```

**Placeholders:** `$ARGUMENTS`, `$1`/`$2`, `` !`command` ``, `@filename`

## Rules

Rules are always loaded via `instructions` in `opencode.json`.

**Important:** Globs don't work with symlinked files. Use explicit absolute paths:

```json
{
  "instructions": [
    "/home/d3fvxl/.config/opencode/rules/programming-principles.md",
    "/home/d3fvxl/.config/opencode/rules/git-workflow.md"
  ]
}
```

**Rules vs Skills:**
- **Rules**: Always loaded, foundational guidelines (programming principles, git workflow)
- **Skills**: On-demand knowledge, loaded when triggered (language-specific patterns, tool usage)

---

# opencode.json Essentials

```json
{
  "$schema": "https://opencode.ai/config.json",
  "theme": "system",
  "model": "anthropic/claude-sonnet-4-5",
  "instructions": [
    "/home/d3fvxl/.config/opencode/rules/programming-principles.md",
    "/home/d3fvxl/.config/opencode/rules/git-workflow.md"
  ],
  "permission": {
    "edit": "allow",
    "bash": "ask"
  },
  "mcp": {
    "server-name": {
      "type": "local",
      "command": ["npx", "-y", "mcp-package"]
    }
  }
}
```

**Variable substitution:** `{env:VAR_NAME}`, `{file:path/to/file}`

For full schema, see [Config docs](https://opencode.ai/docs/config/).

---

# Symlink Checklist

After creating any component in dotfiles:

```bash
# Skills (need directory)
mkdir -p ~/.config/opencode/skills/<name>
ln -s ~/.dotfiles/config/opencode/skills/<name>/SKILL.md \
      ~/.config/opencode/skills/<name>/SKILL.md

# Agents, Commands, Rules (direct files)
ln -s ~/.dotfiles/config/opencode/agents/<name>.md \
      ~/.config/opencode/agents/<name>.md
```

---

# Troubleshooting

| Issue | Fix |
|-------|-----|
| Skill not loading | Check `skills/<name>/SKILL.md` exists, symlink valid |
| Command not found | Add `description` in frontmatter |
| Rules not applied | Use explicit absolute paths in `instructions` (globs don't work with symlinks) |
| Changes not appearing | Edit in `~/.dotfiles/`, not `~/.config/` |
| Profile not loading | Check `OPENCODE_CONFIG_DIR` env var |

---

# Decision Framework

When deciding how to implement a configuration change:

1. **Is it foundational knowledge needed in every session?**
   → Add as a **rule** (via `instructions` in opencode.json)
   - Examples: programming principles, git workflow, security basics

2. **Is it on-demand knowledge for specific tasks?**
   → Create a **skill** (in `skills/<name>/SKILL.md`)
   - Examples: language idioms, testing patterns, tool-specific guides

3. **Is it a reusable prompt template?**
   → Create a **command** (in `commands/<name>.md`)
   - Examples: `/go-review`

4. **Is it a specialized autonomous workflow?**
   → Create an **agent** (in `agents/<name>.md`)
   - Examples: `go-code-reviewer`

5. **Is it external tool integration?**
   → Configure **MCP server** (in `opencode.json` → `mcp`)
   - Examples: database access, API integrations

6. **Is it shared across all profiles?**
   → Put in `~/.dotfiles/config/opencode/`

7. **Is it profile-specific?**
   → Put in `~/.dotfiles/config/opencode-<profile>/`

---

# Example Requests

| User Request | Action |
|--------------|--------|
| "Create a skill for Rust" | Create `skills/rust-idioms/SKILL.md` with frontmatter and content |
| "Add a /deploy command" | Create `commands/deploy.md` with description and template |
| "Set up GitHub MCP server" | Add to `mcp` section in `opencode.json` |
| "My skill isn't loading" | Check symlink: `ls -la ~/.config/opencode/skills/<name>/` |
| "Add a code review agent" | Create `agents/code-reviewer.md` with mode, tools, prompt |
| "Rules aren't being applied" | Check `instructions` uses absolute paths, not globs with symlinks |
| "Create a new work profile" | Follow "Adding a New Profile" steps |
| "Share a skill between profiles" | Symlink from base profile to other profile's skills dir |

---

# Additional Features

For less common features, see official documentation:

| Feature | Documentation |
|---------|---------------|
| Custom Tools (TypeScript) | [Custom Tools](https://opencode.ai/docs/custom-tools/) |
| Plugins (event hooks) | [Plugins](https://opencode.ai/docs/plugins/) |
| Remote MCP with OAuth | [MCP Servers](https://opencode.ai/docs/mcp-servers/) |
| Custom Themes | [Themes](https://opencode.ai/docs/themes/) |
| Formatters | [Formatters](https://opencode.ai/docs/formatters/) |
| Keybinds | [Keybinds](https://opencode.ai/docs/keybinds/) |
| Permissions | [Permissions](https://opencode.ai/docs/permissions/) |
| LSP Integration | [LSP Servers](https://opencode.ai/docs/lsp/) |
| Provider Configuration | [Providers](https://opencode.ai/docs/providers/) |
