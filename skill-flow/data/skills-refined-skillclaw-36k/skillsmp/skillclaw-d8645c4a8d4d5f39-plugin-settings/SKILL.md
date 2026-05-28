---
name: plugin-settings
description: Use this skill when you need to manage plugin configurations, including storing user-configurable settings in `.local.md` files with YAML frontmatter.
---

# Plugin Settings Pattern for Claude Code Plugins

## Overview

Plugins can store user-configurable settings and state in `.claude/plugin-name.local.md` files within the project directory. This pattern uses YAML frontmatter for structured configuration and markdown content for prompts or additional context.

**Key characteristics:**

- **File location:** `.claude/plugin-name.local.md` in project root
- **Structure:** YAML frontmatter + markdown body
- **Purpose:** Per-project plugin configuration and state
- **Usage:** Read from hooks, commands, and agents
- **Lifecycle:** User-managed (not in git, should be in `.gitignore`)

## File Structure

### Basic Template

```markdown
---
enabled: true
setting1: value1
setting2: value2
numeric_setting: 42
list_setting: ["item1", "item2"]
---

# Additional Context

This markdown body can contain:

- Task descriptions
- Additional instructions
- Prompts to feed back to Claude
- Documentation or notes
```

### Example: Plugin State File

**.claude/my-plugin.local.md:**

```markdown
---
enabled: true
strict_mode: false
max_retries: 3
notification_level: info
coordinator_session: team-leader
---

# Plugin Configuration

This plugin is configured for standard validation mode.
Contact @team-lead with questions.
```

## Reading Settings Files

### From Hooks (Bash Scripts)

**Pattern: Check existence and parse frontmatter**

```bash
#!/bin/bash
set -euo pipefail

# Define state file path
STATE_FILE=".claude/my-plugin.local.md"

# Quick exit if file doesn't exist
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0  # Plugin not configured, skip
fi

# Parse YAML frontmatter (between --- markers)
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")

# Extract individual fields
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
STRICT_MODE=$(echo "$FRONTMATTER" | grep '^strict_mode:' | sed 's/strict_mode: *//')

# Check if enabled
if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Disabled
fi

# Use configuration in hook logic
```