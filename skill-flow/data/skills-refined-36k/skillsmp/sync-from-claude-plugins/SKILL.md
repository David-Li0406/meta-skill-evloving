---
name: sync-from-claude-plugins
description: Fetch claude-code-plugins repo and convert plugins to OpenCode format. Usage: /sync-from-claude-plugins [plugin-names...] (default: all available plugins)
---

# Sync Claude Code Plugins to OpenCode

Convert Claude Code plugins to OpenCode format.

**Source of truth**: `references/CONVERSION_GUIDE.md` contains ALL conversion rules. Read it first and refer back during conversion.

## Arguments

- `$ARGUMENTS`: Plugin names and flags (space-separated). If no plugins specified, discovers and converts ALL plugins.

### Flags

- `--reasoning-effort[=LEVEL]`: Add `reasoningEffort` to agent frontmatter (`low`/`medium`/`high`/`xhigh`, default: `medium`)

## Workflow

### 1. Read Conversion Guide

**FIRST**: Read `references/CONVERSION_GUIDE.md` completely.

### 2. Locate Source Repo

```bash
REPO=""
for dir in ~/Documents/Projects/claude-code-plugins ~/Lemonade/claude-code-plugins /tmp/claude-code-plugins; do
  [ -d "$dir" ] && cd "$dir" && git pull origin main && REPO="$dir" && break
done
[ -z "$REPO" ] && git clone https://github.com/doodledood/claude-code-plugins.git /tmp/claude-code-plugins && REPO=/tmp/claude-code-plugins
```

### 3. Discover Plugins

```bash
PLUGINS=""
for dir in "$REPO"/claude-plugins/*/; do
  [ -d "$dir" ] || continue
  [ -f "$dir/.claude-plugin/plugin.json" ] && PLUGINS="$PLUGINS $(basename "$dir")"
done
```

If `$ARGUMENTS` provided, use those instead.

### 4. Bulk Copy

```bash
SCRIPTS="${CLAUDE_SKILL_ROOT}/scripts"
for PLUGIN in $PLUGINS; do
  "$SCRIPTS/bulk_copy.sh" "$REPO" "$PLUGIN"
done
```

### 5. Transform Files

```bash
python3 "${CLAUDE_SKILL_ROOT}/scripts/transform.py" "./*"
```

If `--reasoning-effort` flag: add `reasoningEffort: <level>` after `mode:` in all `agent/*.md` files.

### 6. Convert Hooks

For each plugin with `.hooks-reference/` directory:

1. **Read** `.hooks-reference/plugin.json` for hook configuration
2. **Read** Python files in `.hooks-reference/` to understand logic
3. **Generate** `plugin/hooks.ts` following CONVERSION_GUIDE.md "Converting Hooks" section
4. **Cleanup**: `rm -rf "$PLUGIN/.hooks-reference"`

### 7. Create package.json

Per CONVERSION_GUIDE.md "Plugin Manifest Conversion" section.

### 8. Create README.md

List commands, agents, skills for each plugin.

### 9. Final Validation

Validate **ALL files** (do not sample) against `references/CONVERSION_GUIDE.md`:
- Use the "Migration Checklist" section as your checklist
- Check every command, agent, skill, and hooks.ts file
- Fix any issues found

## Output

```
<plugin>/
├── package.json
├── README.md
├── command/*.md
├── agent/*.md
├── skill/*/SKILL.md
└── plugin/hooks.ts
```

## Installation

```bash
./install.sh                    # All plugins
./install.sh vibe-workflow      # Specific plugin
```
