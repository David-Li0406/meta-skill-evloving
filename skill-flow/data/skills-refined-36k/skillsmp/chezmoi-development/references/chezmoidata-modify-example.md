# Real-World Example: Claude Code Marketplace Configuration

This is a complete, working example of using `.chezmoidata/` and `run_onchange_after_` scripts to manage Claude Code's `settings.json` without overwriting user preferences.

## The Problem

Need to configure Claude Code marketplace settings in dotfiles, but:
- Can't overwrite user's existing `~/.claude/settings.json`
- Must enforce required marketplace configuration
- Must handle fresh installs (no existing settings file)
- Must handle existing installations (preserve user settings)

## The Solution

Use `.chezmoidata/` to store configuration data, and a `run_onchange_after_` script to merge it into existing settings.

### File Structure

```
~/.local/share/chezmoi/
├── .chezmoidata/
│   └── claude.yaml                              # Configuration data
├── modify_dot_claude/
│   └── settings.json.tmpl                       # Merge script
└── .chezmoiscripts/
    └── run_before_00_setup-claude.sh.tmpl       # Ensure directory exists
```

### 1. Configuration Data (.chezmoidata/claude.yaml)

```yaml
---
# Claude Code marketplace configuration
# This data is merged into ~/.claude/settings.json via run_onchange_after_ script

marketplace:
  extraKnownMarketplaces:
    fx-cc:
      source:
        source: git
        url: git@github.com:fx/cc.git

settings:
  includeCoAuthoredBy: false
  enableAllProjectMcpServers: true
```

### 2. Merge Script (.chezmoiscripts/run_onchange_after_update-claude-settings.sh.tmpl)

```bash
{{- if .include_defaults -}}
#!/bin/bash
# Update ~/.claude/settings.json with marketplace configuration
# Works with both real directories and symlinks

set -e

# Ensure ~/.claude exists (as directory or symlink)
if [ ! -e "$HOME/.claude" ]; then
    mkdir -p "$HOME/.claude"
fi

SETTINGS_FILE="$HOME/.claude/settings.json"

# Read existing settings or start with empty object
if [ -f "$SETTINGS_FILE" ]; then
    existing=$(cat "$SETTINGS_FILE")
else
    existing='{}'
fi

# Our required settings from .chezmoidata/claude.yaml
required_settings='{{ .settings | toJson }}'
marketplace_config='{{ .marketplace | toJson }}'

# Merge: existing settings + our required settings + marketplace config
# Our settings take precedence (using * operator for recursive merge)
result=$(echo "$existing" | jq --argjson required "$required_settings" \
                                --argjson marketplace "$marketplace_config" \
                                '. * $required * $marketplace')

# Write the merged result
echo "$result" > "$SETTINGS_FILE"

echo "✓ Updated $SETTINGS_FILE"
{{- end }}
```

**Why use `run_onchange_after_` instead of `modify_`?**
- The `modify_` approach requires chezmoi to manage `~/.claude` as a directory
- This conflicts with Coder workspaces where `~/.claude` is a symlink
- Using a `run_onchange_after_` script allows us to update files inside symlinked directories
- The script runs whenever `.chezmoidata/claude.yaml` changes (because the rendered script changes)

## How It Works

When `chezmoi apply` runs:

1. **Other setup scripts execute** (like `run_onchange_after_setup-shared-symlinks.sh`):
   - May create `~/.claude` as a symlink to `/shared/home/default/.claude` in Coder workspaces
   - Or it remains a regular directory

2. **run_onchange_after_update-claude-settings.sh** executes after:
   - Checks if `~/.claude` exists (as directory or symlink)
   - Reads current `~/.claude/settings.json` from disk (or defaults to `{}`)
   - Loads configuration from `.chezmoidata/claude.yaml`
   - Merges using `jq`: existing + required settings + marketplace config
   - Writes merged JSON back to `~/.claude/settings.json`
   - Works whether `~/.claude` is a real directory or a symlink!

## Example Scenarios

### Scenario 1: Fresh Install (no existing settings.json)

**Before:**
```
~/.claude/  # doesn't exist
```

**After:**
```json
{
  "includeCoAuthoredBy": false,
  "enableAllProjectMcpServers": true,
  "extraKnownMarketplaces": {
    "fx-cc": {
      "source": {
        "source": "git",
        "url": "git@github.com:fx/cc.git"
      }
    }
  }
}
```

### Scenario 2: Existing Installation (user has custom settings)

**Before:**
```json
{
  "alwaysThinkingEnabled": true,
  "someUserSetting": "user-value"
}
```

**After:**
```json
{
  "alwaysThinkingEnabled": true,
  "someUserSetting": "user-value",
  "includeCoAuthoredBy": false,
  "enableAllProjectMcpServers": true,
  "extraKnownMarketplaces": {
    "fx-cc": {
      "source": {
        "source": "git",
        "url": "git@github.com:fx/cc.git"
      }
    }
  }
}
```

User settings preserved, required config enforced!

### Scenario 3: Coder Workspace (symlinked ~/.claude)

**Before:**
```
~/.claude -> /shared/home/default/.claude  # symlink
/shared/home/default/.claude/settings.json:
{
  "userWorkspaceSetting": "value"
}
```

**After:**
```
~/.claude -> /shared/home/default/.claude  # symlink preserved!
/shared/home/default/.claude/settings.json:
{
  "userWorkspaceSetting": "value",
  "includeCoAuthoredBy": false,
  "enableAllProjectMcpServers": true,
  "extraKnownMarketplaces": {
    "fx-cc": {
      "source": {
        "source": "git",
        "url": "git@github.com:fx/cc.git"
      }
    }
  }
}
```

Symlink preserved, settings merged inside the symlinked directory!

## Testing

To test the merge logic manually:

```bash
# Simulate the jq merge
existing='{"alwaysThinkingEnabled":true}'
required_settings='{"includeCoAuthoredBy":false,"enableAllProjectMcpServers":true}'
marketplace_config='{"extraKnownMarketplaces":{"fx-cc":{"source":{"source":"git","url":"git@github.com:fx/cc.git"}}}}'

echo "$existing" | jq --argjson required "$required_settings" \
                       --argjson marketplace "$marketplace_config" \
                       '. * $required * $marketplace'
```

Output:
```json
{
  "alwaysThinkingEnabled": true,
  "includeCoAuthoredBy": false,
  "enableAllProjectMcpServers": true,
  "extraKnownMarketplaces": {
    "fx-cc": {
      "source": {
        "source": "git",
        "url": "git@github.com:fx/cc.git"
      }
    }
  }
}
```

## Key Takeaways

1. **`.chezmoidata/` for structured config** - Store configuration as YAML/JSON/TOML data
2. **`run_onchange_after_` scripts for merging** - Non-destructive updates to existing files (use `modify_` when not dealing with symlinks)
3. **`jq` for JSON merging** - Use `*` operator for recursive merge (right side wins)
4. **Template guards** - Use `{{ if .include_defaults -}}` to control when scripts run
5. **Prerequisite scripts** - Use `run_before_` to ensure dependencies exist
6. **Handle all cases** - Script must work for: no file, empty file, existing file with data
