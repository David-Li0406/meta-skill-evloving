---
name: Configure Powerline Status Line
description: This skill should be used when the user asks to "configure powerline", "set up status line", "use my default status line", "configure powerline as usual", "change the powerline theme", "update status line settings", or mentions powerline configuration. Provides comprehensive guidance for creating and managing .claude/.claude-powerline.json configuration and integrating it with Claude Code settings.
version: 0.1.0
---

# Configure Powerline Status Line

## Purpose

Configure Claude Code's status line using the powerline package. Create or update `.claude/.claude-powerline.json` with user preferences and integrate it into `.claude/settings.local.json`. Handle everything from applying default configurations to customizing specific segments, themes, and layouts based on natural language requests.

## When to Use

Activate when users want to:
- Set up powerline for the first time
- Apply default powerline configuration
- Customize status line segments (directory, git, metrics, context, etc.)
- Change themes or styles
- Modify line layouts
- Ask about available powerline options

## Configuration Workflow

Follow this safe, confirmable workflow for all configuration changes:

### 1. Understand User Intent

Parse the user's request to determine:
- **Default application**: Phrases like "use my default", "configure as usual", "set up powerline" → apply default configuration
- **Specific customization**: Parse what segments, theme, style, or layout changes requested
- **Information request**: "what themes are available", "what segments can I show" → consult references

### 2. Read Existing Configuration

Always check current state before making changes:

```bash
# Check if .claude directory exists
if [ ! -d ".claude" ]; then
    mkdir -p .claude
fi

# Read existing powerline config if present
if [ -f ".claude/.claude-powerline.json" ]; then
    cat .claude/.claude-powerline.json
fi

# Read existing settings if present
if [ -f ".claude/settings.local.json" ]; then
    cat .claude/settings.local.json
fi
```

### 3. Create Backup Files

Before any modifications, create backups with `.backup` extension:

```bash
# Backup powerline config if exists
if [ -f ".claude/.claude-powerline.json" ]; then
    cp .claude/.claude-powerline.json .claude/.claude-powerline.json.backup
fi

# Backup settings if exists
if [ -f ".claude/settings.local.json" ]; then
    cp .claude/settings.local.json .claude/settings.local.json.backup
fi
```

### 4. Validate Existing Files

If files exist, verify they contain valid JSON:

```bash
# Validate powerline config
if [ -f ".claude/.claude-powerline.json" ]; then
    if ! jq empty .claude/.claude-powerline.json 2>/dev/null; then
        echo "ERROR: .claude/.claude-powerline.json contains invalid JSON"
        exit 1
    fi
fi

# Validate settings
if [ -f ".claude/settings.local.json" ]; then
    if ! jq empty .claude/settings.local.json 2>/dev/null; then
        echo "ERROR: .claude/settings.local.json contains invalid JSON"
        exit 1
    fi
fi
```

**On validation failure**: Abort and ask user to fix the malformed JSON before proceeding.

### 5. Build New Configuration

Create the new powerline configuration based on user request:

**For default configuration request:**
- Use the default template (see Default Configuration section)
- Theme: "tokyo-night"
- Style: "powerline"

**For customization request:**
- Start with existing configuration or default if none exists
- Modify only the requested values
- Preserve all other settings
- Validate segment configurations against available options (see `references/segments.md`)

**For theme/style changes:**
- Preserve all segment and line configurations
- Update only theme or style properties
- Validate theme names against available themes (see `references/themes-and-styles.md`)

### 6. Write New Configuration

Write the new `.claude/.claude-powerline.json`:

```bash
# Write new powerline config
echo '{...}' | jq '.' > .claude/.claude-powerline.json
```

Update `.claude/settings.local.json` to include statusLine configuration:

```bash
# If settings.local.json doesn't exist, create it
if [ ! -f ".claude/settings.local.json" ]; then
    echo '{}' > .claude/settings.local.json
fi

# Merge statusLine configuration
jq '. + {
  "statusLine": {
    "type": "command",
    "command": "npx -y @owloops/claude-powerline@latest --config=.claude/.claude-powerline.json"
  }
}' .claude/settings.local.json > .claude/settings.local.json.tmp
mv .claude/settings.local.json.tmp .claude/settings.local.json
```

**Critical**: Only modify the `statusLine` key. Preserve all other settings in the file.

### 7. Confirm with User

After writing new configuration, ask for confirmation:

```
I've updated your powerline configuration with the following changes:
[Describe what changed]

The new configuration:
- Theme: tokyo-night
- Style: powerline
- Segments: [list enabled segments]

Do the changes work as expected?
```

### 8. Cleanup Based on Response

**If user confirms changes work:**
```bash
# Remove backup files
rm -f .claude/.claude-powerline.json.backup
rm -f .claude/settings.local.json.backup
```

**If user says changes don't work or wants to revert:**
```bash
# Restore from backups
if [ -f ".claude/.claude-powerline.json.backup" ]; then
    mv .claude/.claude-powerline.json.backup .claude/.claude-powerline.json
fi
if [ -f ".claude/settings.local.json.backup" ]; then
    mv .claude/settings.local.json.backup .claude/settings.local.json
fi

# Delete any remaining backup files
rm -f .claude/.claude-powerline.json.backup
rm -f .claude/settings.local.json.backup
```

**Always ensure backup files are removed** regardless of outcome.

## Default Configuration

When user requests default configuration ("use my default", "configure powerline as usual", etc.), use this template:

```json
{
  "theme": "tokyo-night",
  "display": {
    "style": "powerline",
    "lines": [
      {
        "segments": {
          "directory": {
            "enabled": true,
            "style": "basename"
          },
          "git": {
            "enabled": true,
            "showSha": false,
            "showOperation": true,
            "showTimeSinceCommit": true,
            "showRepoName": true
          }
        }
      },
      {
        "segments": {
          "model": {
            "enabled": true
          },
          "metrics": {
            "enabled": true,
            "showResponseTime": false,
            "showLastResponseTime": false,
            "showDuration": false,
            "showMessageCount": true,
            "showLinesAdded": true,
            "showLinesRemoved": true
          },
          "block": {
            "enabled": true,
            "type": "tokens",
            "burnType": "tokens"
          },
          "context": {
            "enabled": true,
            "showPercentageOnly": true
          }
        }
      }
    ]
  }
}
```

## Parsing User Requests

### Common Request Patterns

**Minimal configurations:**
- "just show the directory and context" → Enable only directory and context segments
- "show only git status" → Enable only git segment
- "minimal status line" → Single line with directory only

**Layout requests:**
- "two lines" → Create configuration with two line objects
- "Directory on top then metrics below" → First line with directory, second with metrics
- "put everything on one line" → Single line object with all requested segments

**Segment customization:**
- "directory basename only" → Set `directory.style` to "basename"
- "show full path" → Set `directory.style` to "full"
- "show git SHA" → Set `git.showSha` to true
- "hide lines added/removed" → Set corresponding metrics flags to false

**Theme/style changes:**
- "change theme to rose-pine" → Update `theme` property only
- "use minimal style" → Update `display.style` only
- Both preserve all segment configurations

### Validation Logic

Before writing configuration, validate:

1. **Theme names**: Must match available themes (see `references/themes-and-styles.md`)
2. **Style names**: Must be "powerline", "minimal", or "capsule"
3. **Segment names**: Must match available segments (see `references/segments.md`)
4. **Segment properties**: Validate against segment-specific options
5. **Directory style**: Must be "full", "fish", or "basename"

**On validation failure**: Inform user of invalid value and suggest corrections.

## Preserving Existing Settings

Critical principle: **Only modify what user explicitly requests.**

### Powerline Configuration Preservation

When updating `.claude/.claude-powerline.json`:
- Changing theme → preserve display configuration
- Modifying segments → preserve theme, style, and other segments
- Updating one segment property → preserve all other properties of that segment
- Adding/removing lines → preserve segment configurations within unchanged lines

### Settings.local.json Preservation

When updating `.claude/settings.local.json`:
- Only modify the `statusLine` object
- Preserve all other keys (`attribution`, `model`, etc.)
- Use jq to merge rather than overwrite

Example merging logic:
```bash
# Read existing settings
EXISTING=$(cat .claude/settings.local.json)

# Merge with new statusLine
echo "$EXISTING" | jq '. + {
  "statusLine": {
    "type": "command",
    "command": "npx -y @owloops/claude-powerline@latest --config=.claude/.claude-powerline.json"
  }
}' > .claude/settings.local.json
```

## Examples

See `examples/` directory for complete working examples:
- **`examples/default.json`** - Default configuration
- **`examples/minimal.json`** - Minimal single-line configuration
- **`examples/two-lines.json`** - Two-line layout with separation
- **`examples/custom-theme.json`** - Custom theme application

## Additional Resources

### Reference Files

For detailed configuration options:
- **`references/segments.md`** - Complete segment reference with all configuration options
- **`references/themes-and-styles.md`** - Available themes and styles with descriptions

### User Information Requests

When users ask "what themes are available" or "what segments can I use":
1. Read the appropriate reference file
2. Present the information in a clear, organized format
3. Offer to apply any of the options

## Error Handling

### Directory Creation
If `.claude/` doesn't exist, create it automatically:
```bash
mkdir -p .claude
```

### File Creation
If configuration files don't exist, create them with valid JSON:
```bash
echo '{}' > .claude/settings.local.json
```

### Malformed JSON
If existing files contain invalid JSON:
1. Detect using `jq empty`
2. Abort the operation
3. Ask user to fix JSON manually before proceeding
4. Do NOT attempt automatic fixes

### Backup Recovery
If user wants to revert:
1. Restore both files from backups
2. Remove all backup files
3. Confirm restoration complete

## Notes

- Powerline requires Node.js/npm but runs via npx (auto-installs on first use)
- Configuration takes effect on next Claude Code session
- Use jq for all JSON operations to ensure validity
- Always preserve settings the user didn't explicitly request to change
- Backup workflow provides safety without cluttering the workspace
