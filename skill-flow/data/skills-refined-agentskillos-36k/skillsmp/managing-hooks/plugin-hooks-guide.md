# Plugin Hooks Comprehensive Guide

Plugin hooks enable Claude Code plugins to provide distributed hook functionality that integrates with user and project hooks.

## Overview

### What Are Plugin Hooks?

Plugin hooks are hooks defined by plugins (enabled Claude Code extensions) that automatically merge with user and project hooks. They enable:

- **Automatic Integration**: Hooks activate when plugin is enabled
- **Distributed Configuration**: Hooks defined with plugin code
- **Composition**: Multiple plugins' hooks work together
- **Plugin-Relative Paths**: Use `${CLAUDE_PLUGIN_ROOT}` for scripts

### Architecture

```
User Hooks (~/.claude/settings.json)
    ↓
Project Hooks (.claude/settings.json)
    ↓
Plugin Hooks (enabled plugins)
    ↓
Final Hook Configuration (merged)
```

All hooks execute in parallel on matching events.

### Key Differences from User/Project Hooks

| Aspect | User Hooks | Project Hooks | Plugin Hooks |
|--------|---|---|---|
| **Location** | `~/.claude/settings.json` | `.claude/settings.json` | `plugin.json` or custom path |
| **Scope** | All projects | One project | When plugin enabled |
| **Merging** | Single source | Overrides user | Adds to user + project |
| **Control** | User manages | Project team manages | Plugin provides |
| **Paths** | Absolute or relative | Project-relative | Plugin-relative (`${CLAUDE_PLUGIN_ROOT}`) |
| **Execution** | Always active | In project only | When plugin enabled |

## Plugin Hook Structure

### Directory Organization

Typical plugin with hooks:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── hooks/
│   ├── hooks.json               # Hook definitions
│   ├── scripts/
│   │   ├── validate.py
│   │   └── format.sh
│   └── templates/
│       └── hook-template.json
├── skills/
│   └── my-skill/
└── README.md
```

### Plugin Hook Configuration Files

**Option 1: hooks/hooks.json**

```json
{
  "description": "My plugin provides automatic code formatting",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/format.sh"
          }
        ]
      }
    ]
  }
}
```

**Option 2: Custom path in plugin.json**

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "hooks": "./my-custom-hooks-path/config.json"
}
```

### Plugin Manifest Integration

Define hooks in `plugin.json`:

```json
{
  "name": "formatting-plugin",
  "version": "1.0.0",
  "description": "Automatic code formatting for multiple languages",
  "hooks": [
    {
      "description": "Auto-format Python with Black",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-python.sh"
              }
            ]
          }
        ]
      }
    }
  ]
}
```

## Environment Variables for Plugin Hooks

### Available Variables

**${CLAUDE_PLUGIN_ROOT}**:
- Absolute path to plugin directory
- Used for plugin-relative paths
- Always available in plugin hooks

**${CLAUDE_PROJECT_DIR}**:
- Absolute path to project root
- Project where hook is running
- Available in all hook types

**All Standard Environment Variables**:
- `PATH`, `HOME`, `USER`, etc.
- System environment variables
- Available in command hooks only (not prompt hooks)

### Usage Examples

**Python Script with Logging**:
```bash
#!/bin/bash
PLUGIN_HOME="${CLAUDE_PLUGIN_ROOT}"
LOG_FILE="${CLAUDE_PROJECT_DIR}/.claude/plugin-logs/format.log"

mkdir -p "$(dirname "$LOG_FILE")"
echo "$(date): Formatting executed" >> "$LOG_FILE"

python3 "${PLUGIN_HOME}/scripts/formatter.py"
```

**Using CLAUDE_PROJECT_DIR in Python**:
```python
import os

plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
project_dir = os.environ.get('CLAUDE_PROJECT_DIR')

config_file = os.path.join(plugin_root, 'config.json')
output_dir = os.path.join(project_dir, '.claude', 'outputs')
```

## Hook Merging and Execution

### How Hooks Merge

When multiple hooks match the same event:

1. **Collection Phase**: Gather all matching hooks from:
   - User settings
   - Project settings
   - All enabled plugins

2. **Merge Phase**: Combine into single hook list for event

3. **Execution Phase**: All hooks execute in parallel

**Example**:

User has: PostToolUse hook for Write (logging)
Project has: PostToolUse hook for Write (validation)
Plugin has: PostToolUse hook for Write (formatting)

**Result**: All three execute on Write operations

```
Write operation triggered
    ↓
All three hooks execute in parallel:
  - User hook: Logging
  - Project hook: Validation
  - Plugin hook: Formatting
    ↓
All complete (or one blocks)
```

### Execution Order

- **Parallel**: All hooks run simultaneously
- **No Guaranteed Order**: Don't rely on execution sequence
- **Independent**: Each hook's success/failure independent

**Design Implication**: Plugin hooks should be:
- Self-contained (don't depend on other hooks)
- Idempotent (safe to run multiple times)
- Non-blocking (unless they need to block)

### Blocking Behavior

When multiple hooks compete:

**Scenario**: User hook blocks, plugin hook allows
- User's block takes precedence
- Tool call is blocked
- Plugin can't override user decision

**Scenario**: Two plugins' hooks have different decisions
- First block wins (blocks execute first if any present)
- Deterministic: User setup not affected by plugin order

### Deduplication

Identical hooks from multiple sources:
- System automatically deduplicates
- Same command run once, not twice
- Reduces unnecessary overhead

## Plugin Hook Composition Patterns

### Pattern 1: Single-Purpose Hook

Plugin provides one focused hook:

```json
{
  "description": "Validates Python code style",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-python.py"
          }
        ]
      }
    ]
  }
}
```

**Characteristics**:
- Single event type
- Clear responsibility
- Easy to understand
- Composable with others

### Pattern 2: Multi-Event Hook

Plugin manages multiple related events:

```json
{
  "description": "Comprehensive code quality management",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{...}]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{...}]
      }
    ]
  }
}
```

**Characteristics**:
- Related functionality across events
- Coordinated behavior
- Still focused and clear

### Pattern 3: Conditional Hooks

Plugin provides different hooks based on context:

```json
{
  "description": "Language-specific formatters",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/auto-detect-and-format.sh"
          }
        ]
      }
    ]
  }
}
```

Script internally decides which formatter to use.

### Pattern 4: Templated Hooks

Plugin provides hook templates users can customize:

**In plugin**:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/setup.sh"
          }
        ]
      }
    ]
  }
}
```

Script created from template when plugin installed.

## Multi-Plugin Scenarios

### Scenario 1: Complementary Plugins

**Plugin A**: Formats code
**Plugin B**: Lints code

Both provide PostToolUse hooks on Write/Edit:
- Both execute independently
- No conflicts
- Complementary workflow

```
Edit file
  ↓
Plugin A: Format (makes code pretty)
Plugin B: Lint (checks for issues)
  ↓
Both hooks complete
```

### Scenario 2: Competing Plugins

**Plugin A**: Formats with Prettier
**Plugin B**: Formats with Black

Both PostToolUse hooks on Write/Edit:
- Both will execute
- Both modify the file
- Potential conflicts

**Solution**:
- Document incompatibility
- Use matchers to avoid overlap (e.g., `"Plugin A": "*.js"`, `"Plugin B": "*.py"`)
- Provide compatibility layer

### Scenario 3: Dependent Plugins

**Plugin A**: Validation (must run first)
**Plugin B**: Formatting (depends on validation)

Challenge: Hooks execute in parallel, no guaranteed order

**Solution Options**:

1. **Combine into single plugin hook**:
   Script validates then formats

2. **Use separate events**:
   - Plugin A: PreToolUse (validation)
   - Plugin B: PostToolUse (formatting)

3. **Disable conflicting plugin**:
   User disables Plugin B if using Plugin A

### Scenario 4: User Override of Plugin

User wants to customize plugin behavior:

**Plugin provides**: Default validation
**User provides**: Project-specific validation in `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/project-specific-validation.py"
          }
        ]
      }
    ]
  }
}
```

**Result**: Both hooks execute
- Plugin: Default validation
- User: Project-specific validation
- Layered protection

## Integration Patterns

### Pattern: Audit Trail with Plugins

Combine multiple plugins into audit system:

**Plugin A (Security)**: PreToolUse validates operations
**Plugin B (Compliance)**: PostToolUse logs operations
**Plugin C (Reporting)**: SessionEnd generates report

```
Session starts
  ↓
Each operation:
  - PreToolUse: Security check
  - Tool execution
  - PostToolUse: Compliance log
  ↓
Session ends
  ↓
SessionEnd: Generate report from logs
```

### Pattern: Layered Validation

Progressive validation through plugins:

**Plugin A (Syntax)**: Checks valid syntax
**Plugin B (Style)**: Checks code style
**Plugin C (Performance)**: Checks performance

All PostToolUse on Write/Edit:
- Each plugin checks different aspect
- User sees comprehensive validation

### Pattern: Template + Execution

Plugin provides template hooks:

**In plugin**: Template for SessionStart setup
**User**: Customizes template for project
**Result**: Plugin provides framework, user customizes

## Best Practices for Plugin Developers

### 1. Use ${CLAUDE_PLUGIN_ROOT} for All Paths

✅ **Good**:
```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
```

❌ **Bad**:
```bash
"/home/user/.claude/plugins/my-plugin/scripts/format.sh"
```

### 2. Provide Clear Hook Descriptions

```json
{
  "description": "Validates Python files with Black formatter and reports style issues",
  "hooks": {
    ...
  }
}
```

### 3. Make Hooks Independent

Each hook should work without assuming other hooks run:

```python
#!/usr/bin/env python3
# Don't assume previous hooks ran
# Don't require specific execution order
# Complete standalone
```

### 4. Handle Missing Dependencies Gracefully

```bash
#!/bin/bash
if ! command -v black &> /dev/null; then
  echo "Black not installed. Skipping format hook."
  exit 0  # Don't fail
fi

black "$file"
```

### 5. Use Appropriate Matchers

Be specific to avoid unexpected hook triggers:

✅ **Good**:
```json
{"matcher": "Write|Edit"}
```

❌ **Overly Broad**:
```json
{"matcher": "*"}  // Matches everything
```

### 6. Document Environment Setup

```
## Installation

This plugin requires:
- Python 3.8+
- Black >= 22.0

Install dependencies:
```bash
pip install black>=22.0
```
```

### 7. Provide Configuration Options

If plugin hooks are customizable:

```
## Configuration

Users can customize plugin behavior by creating `.claude/.plugin-config.json`:

```json
{
  "black-plugin": {
    "line-length": 88,
    "target-version": "py38"
  }
}
```

Load in hook script:
```bash
CONFIG_FILE="${CLAUDE_PROJECT_DIR}/.claude/.plugin-config.json"
# Load configuration
```
```

### 8. Log Appropriately

Use stderr for errors, stdout for information:

```bash
#!/bin/bash
# Log to file
LOG_FILE="${CLAUDE_PROJECT_DIR}/.claude/logs/plugin.log"
mkdir -p "$(dirname "$LOG_FILE")"

{
  echo "[$(date)] Processing: $1"
  # ... execution ...
  echo "[$(date)] Completed"
} >> "$LOG_FILE" 2>&1
```

### 9. Support Windows/Mac/Linux

- Use forward slashes in paths
- Don't assume bash (support sh)
- Test cross-platform

```bash
#!/bin/sh  # Not #!/bin/bash (more portable)
# Use portable commands
```

### 10. Provide Disable/Override Options

Document how users can:
- Disable plugin hooks
- Override plugin behavior
- Work around conflicts

## Creating Plugin Hooks Step-by-Step

### Step 1: Create Hook Configuration

In `my-plugin/hooks/hooks.json`:

```json
{
  "description": "Automatic Python code formatting with Black",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/format-python.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Step 2: Create Hook Script

In `my-plugin/hooks/scripts/format-python.sh`:

```bash
#!/bin/bash
set -e

# Load hook input
INPUT=$(cat)

# Extract file path
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)

# Only process Python files
if [[ ! "$FILE_PATH" == *.py ]]; then
  exit 0  # Not a Python file, skip
fi

# Check Black is installed
if ! command -v black &> /dev/null; then
  echo "Black formatter not found. Install with: pip install black" >&2
  exit 0  # Don't fail, just skip
fi

# Format the file
if black "$FILE_PATH" 2>/dev/null; then
  echo "✓ Formatted: $(basename "$FILE_PATH")"
  exit 0
else
  echo "⚠ Format failed: $(basename "$FILE_PATH")" >&2
  exit 0  # Don't block file editing
fi
```

### Step 3: Register in Plugin Manifest

In `my-plugin/.claude-plugin/plugin.json`:

```json
{
  "name": "python-formatter-plugin",
  "version": "1.0.0",
  "description": "Automatic Python code formatting with Black",
  "hooks": "hooks/hooks.json"
}
```

### Step 4: Test Hook Registration

When plugin is installed:

```bash
# User runs: /hooks command
# Should see: Python Formatter plugin hooks listed
```

### Step 5: Test Hook Execution

Create test Python file:

```python
def hello(  x,y  ):
    return x+y
```

Edit file in Claude Code. Hook should trigger after edit and format it.

## Troubleshooting Plugin Hooks

### Hooks Not Running

**Symptoms**: Plugin installed but hooks don't execute

**Debug**:
1. Verify plugin is enabled in Claude Code settings
2. Run `/hooks` command - should list plugin hooks
3. Restart Claude Code
4. Run `claude --debug` for detailed logs

### Hook Script Fails

**Symptoms**: Error when hook tries to run

**Solutions**:
1. Check script has execute permissions: `chmod +x script.sh`
2. Verify shebang line is correct: `#!/bin/bash`
3. Check `${CLAUDE_PLUGIN_ROOT}` expansion works
4. Test script independently

### Environment Variables Not Available

**Symptoms**: `$CLAUDE_PLUGIN_ROOT` not set

**Causes**:
- Prompt-based hooks (no access to env vars)
- Running outside Claude Code context

**Solution**:
- Use command hooks if you need env vars
- Use paths in prompt for prompt hooks

### Plugin Conflicts

**Symptoms**: Multiple plugins' hooks interfere

**Solutions**:
1. Use specific matchers (avoid overlapping)
2. Check plugin execution order
3. Document incompatibilities
4. Provide user override options

### Performance Issues

**Symptoms**: Claude Code is slow when plugin active

**Causes**:
- Hook runs on very frequent event (e.g., every PreToolUse)
- Hook script is slow or resource-intensive

**Solutions**:
1. Optimize script performance
2. Add selective matchers
3. Cache results if possible
4. Reduce hook frequency

## Security Considerations

### Plugin Hook Risks

⚠️ **Plugin hooks run automatically with user permissions**

**Potential Issues**:
- Malicious plugins could exfiltrate data
- Plugins could modify system files
- Plugins could execute arbitrary commands

### Security Best Practices

1. **Only enable trusted plugins**
   - Review plugin source code
   - Check plugin permissions in manifest
   - Verify plugin author/reputation

2. **Review plugin hooks**
   ```bash
   cat ~/.claude/plugins/plugin-name/hooks.json
   # Review what commands will execute
   ```

3. **Use allowed-tools restrictions**
   Plugin can restrict its own tool access

4. **Audit hook scripts**
   - Check for suspicious commands
   - Look for credential exfiltration
   - Verify error handling

5. **Disable suspicious hooks**
   Remove from hooks.json if uncertain

## Migration: From User Hooks to Plugin Hooks

When converting user hooks to plugin hooks:

### Step 1: Extract Functionality

Take user's `.claude/settings.json` hook:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [...]
      }
    ]
  }
}
```

### Step 2: Create Plugin Structure

Create plugin with same functionality:

```
my-plugin/
├── .claude-plugin/plugin.json
├── hooks/
│   ├── hooks.json
│   └── scripts/my-hook.sh
└── README.md
```

### Step 3: Reference from Plugin

Use `${CLAUDE_PLUGIN_ROOT}` in paths

### Step 4: User Installs Plugin

User enables plugin instead of manual hook config

### Step 5: Clean Up Manual Config

User can remove original hooks from `.claude/settings.json`

## See Also

- **SKILL.md**: Main hook skill overview
- **prompt-hooks-guide.md**: Prompt-based hooks
- **hook-schemas-reference.md**: Hook input/output schemas
- **script-examples.md**: Script implementation examples
