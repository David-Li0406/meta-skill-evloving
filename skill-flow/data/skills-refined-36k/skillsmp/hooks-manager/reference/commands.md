# Hooks Manager Command Reference

Complete reference for all hooks-manager skill commands.

## Configuration Format

### Plugin Hooks (PRISM)

PRISM uses plugin-level hooks configured in `hooks/hooks.json` at the plugin root:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/path/to/script.py",
            "description": "What this hook does",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**Critical Requirements:**
- ✅ Use `${CLAUDE_PLUGIN_ROOT}` for all plugin paths (not relative paths)
- ✅ Nest hooks under event names as keys
- ✅ Each matcher gets its own object with a `hooks` array
- ✅ Each hook needs `type: "command"` property

**Example (PRISM's current configuration)**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/enforce-story-context.py",
            "description": "Ensure workflow commands have required story context"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/track-current-story.py",
            "description": "Track story file as current workflow context"
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/validate-required-sections.py",
            "description": "Verify all required PRISM sections exist"
          }
        ]
      }
    ]
  }
}
```

### User-Level Hooks

User and project-level hooks use the same format in `~/.claude/settings.json` or `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python /absolute/path/to/hook.py"
          }
        ]
      }
    ]
  }
}
```

**Note:** User hooks don't have `${CLAUDE_PLUGIN_ROOT}` - use absolute paths.

### Schema Reference

```typescript
{
  hooks: {
    [EventName: string]: Array<{
      matcher: string;              // "Bash", "Edit|Write", "*"
      hooks: Array<{
        type: "command";             // Hook type (always "command")
        command: string;             // Shell command to execute
        description?: string;        // Optional description
        timeout?: number;            // Optional timeout (default: 60s)
      }>;
    }>;
  };
}
```

**Available Event Names:**
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool completion
- `UserPromptSubmit` - Before AI processes prompt
- `SessionStart` - Session begins/resumes
- `SessionEnd` - Session terminates
- `Stop` - Claude finishes responding
- `SubagentStop` - Subagent completes
- `PreCompact` - Before memory compaction
- `Notification` - Claude sends notification

**Matcher Patterns:**
- Exact: `"Bash"`, `"Edit"`, `"Write"`
- Multiple: `"Edit|Write"`, `"Read|Glob|Grep"`
- All tools: `"*"`
- MCP tools: `"mcp__server__tool"`

**Exit Codes:**
- `0`: Success (allow operation)
- `2`: Blocking error (blocks operation, feeds stderr to Claude)
- Other: Non-blocking error (stderr shown to user)

## Command Categories

- [Hook Management](#hook-management)
- [Testing & Debugging](#testing--debugging)
- [Examples & Reference](#examples--reference)
- [Integration](#integration)

---

## Hook Management

### `list-hooks`

**Purpose**: Display all configured hooks with their events and matchers

**Usage**: `*list-hooks`

**Output**:
```
📋 Configured Hooks:

User Hooks (~/.claude/settings.json):
  1. bash-logger (PreToolUse, Bash)
     Command: python hooks/log-bash.py

  2. auto-format (PostToolUse, Edit|Write)
     Command: prettier --write ${file_path}

Project Hooks (.claude/settings.json):
  3. validate-story (PreToolUse, Edit)
     Command: python hooks/validate-story.py

Total: 3 hooks (2 user, 1 project)
```

**Options**:
- `*list-hooks --user` - Show only user-level hooks
- `*list-hooks --project` - Show only project-level hooks
- `*list-hooks --event PreToolUse` - Filter by event type

---

### `create-hook`

**Purpose**: Create new hook with guided interactive setup

**Usage**: `*create-hook`

**Process**:
1. Select event type (PreToolUse, PostToolUse, etc.)
2. Choose matcher pattern (tool name or *)
3. Enter command to execute
4. Add description
5. Select configuration location (user or project)

**Example**:
```
*create-hook

→ Select event type:
  1. PreToolUse (can block operations)
  2. PostToolUse (after operations complete)
  ...

Choice: 1

→ Select matcher:
  1. Bash (bash commands only)
  2. Edit|Write (file edits and writes)
  3. * (all tools)
  4. Custom pattern

Choice: 1

→ Enter command:
Command: python hooks/my-validation.py

→ Description:
Description: Validate bash commands before execution

→ Save to:
  1. User settings (global)
  2. Project settings (this project only)

Choice: 2

✅ Hook created: my-validation
   Saved to: .claude/settings.json
```

**Advanced Usage**:
- `*create-hook --template [name]` - Start from example template
- `*create-hook --quick` - Skip interactive prompts (use defaults)

---

### `edit-hook {name}`

**Purpose**: Modify existing hook configuration

**Usage**: `*edit-hook my-validation`

**Opens interactive editor**:
```
Editing hook: my-validation

Current configuration:
  Event: PreToolUse
  Matcher: Bash
  Command: python hooks/my-validation.py
  Description: Validate bash commands

What would you like to edit?
  1. Event type
  2. Matcher
  3. Command
  4. Description
  5. Enable/Disable
  6. Save changes
  7. Cancel
```

**Direct Edit**:
```
*edit-hook my-validation --command "python3 hooks/new-validator.py"
*edit-hook my-validation --matcher "Edit|Write"
*edit-hook my-validation --disable
```

---

### `delete-hook {name}`

**Purpose**: Remove hook from configuration

**Usage**: `*delete-hook my-validation`

**Confirmation**:
```
⚠️  Are you sure you want to delete hook: my-validation?
   Event: PreToolUse
   Matcher: Bash
   Command: python hooks/my-validation.py

   This action cannot be undone.

   Type 'yes' to confirm: yes

✅ Hook deleted: my-validation
```

**Force delete** (no confirmation):
```
*delete-hook my-validation --force
```

---

### `enable-hook {name}`

**Purpose**: Enable a disabled hook

**Usage**: `*enable-hook my-validation`

**Output**:
```
✅ Hook enabled: my-validation
   Will execute on: PreToolUse (Bash)
```

---

### `disable-hook {name}`

**Purpose**: Disable hook without deleting it

**Usage**: `*disable-hook my-validation`

**Output**:
```
✅ Hook disabled: my-validation
   Configuration preserved (can be re-enabled)
```

---

## Testing & Debugging

### `test-hook {name}`

**Purpose**: Test hook execution with sample input

**Usage**: `*test-hook my-validation`

**Process**:
1. Generates sample tool input JSON
2. Executes hook command
3. Captures stdout, stderr, exit code
4. Displays results

**Output**:
```
🧪 Testing hook: my-validation

Sample input:
{
  "tool_input": {
    "command": "git push --force",
    "description": "Force push to remote"
  }
}

Executing: python hooks/my-validation.py

Exit code: 2 (BLOCKED)
Stdout:
Stderr: ❌ ERROR: Force push not allowed on main branch

✅ Test complete
   Hook correctly blocks dangerous operation
```

**Custom test input**:
```
*test-hook my-validation --input sample.json
```

---

### `debug-hook {name}`

**Purpose**: Show hook execution logs and debugging information

**Usage**: `*debug-hook my-validation`

**Output**:
```
🔍 Debug information for: my-validation

Configuration:
  Location: .claude/settings.json
  Event: PreToolUse
  Matcher: Bash
  Command: python hooks/my-validation.py
  Status: Enabled

Recent executions (last 10):
  1. 2025-10-24 15:30:45 - EXIT:2 - Blocked: force push
  2. 2025-10-24 15:28:12 - EXIT:0 - Allowed: normal command
  3. 2025-10-24 15:25:33 - EXIT:2 - Blocked: rm -rf /
  ...

Common issues:
  ✓ Command is executable
  ✓ Configuration syntax valid
  ✓ Matcher pattern valid
  ! Hook has blocked 30% of recent executions (review threshold?)
```

---

### `validate-config`

**Purpose**: Check hooks configuration syntax for all settings files

**Usage**: `*validate-config`

**Output**:
```
✅ Validating hook configurations...

~/.claude/settings.json:
  ✅ Valid JSON syntax
  ✅ 2 hooks configured
  ✅ All matchers valid
  ✅ All commands exist

.claude/settings.json:
  ✅ Valid JSON syntax
  ✅ 1 hook configured
  ⚠️  Warning: Hook 'my-validation' command not found: python hooks/my-validation.py

.claude/settings.local.json:
  ℹ️  File not found (optional)

Overall: 3 hooks, 1 warning, 0 errors
```

**Fix issues**:
```
*validate-config --fix
```

---

## Examples & Reference

### `hook-examples`

**Purpose**: Browse pre-built hook patterns for common use cases

**Usage**: `*hook-examples`

**Categories**:
```
📚 Hook Examples Library

1. Logging & Auditing
   - bash-command-logger
   - file-change-tracker
   - workflow-auditor

2. Validation & Safety
   - file-protection
   - git-safety
   - syntax-validator

3. Automation
   - auto-formatter
   - auto-tester
   - auto-commit

4. Notifications
   - desktop-alerts
   - slack-integration
   - completion-notifier

Select category or search:
```

**View example**:
```
*hook-examples bash-command-logger

Name: bash-command-logger
Category: Logging & Auditing
Description: Log all bash commands to file for audit trail

Configuration:
  Event: PreToolUse
  Matcher: Bash
  Command: jq -r '"\(.tool_input.command) - \(.tool_input.description)"' >> ~/.claude/bash-log.txt

Usage: Tracks every bash command with timestamp
Security: Low risk (read-only logging)
Dependencies: jq

Install: *install-example bash-command-logger
```

---

### `event-types`

**Purpose**: List all hook event types with detailed information

**Usage**: `*event-types`

**Output**:
```
📋 Hook Event Types

PreToolUse
  Timing: Before tool execution
  Can Block: YES ✅
  Use Cases: Validation, access control, logging
  Example: Block dangerous git operations

PostToolUse
  Timing: After tool completion
  Can Block: NO ❌
  Use Cases: Formatting, testing, cleanup
  Example: Run prettier on edited files

UserPromptSubmit
  Timing: Before AI processing
  Can Block: YES ✅
  Use Cases: Input validation, preprocessing
  Example: Check for sensitive data in prompts

... (all 9 events)
```

**Filter by capability**:
```
*event-types --can-block
*event-types --for-validation
```

---

### `security-guide`

**Purpose**: Display hook security best practices and review checklist

**Usage**: `*security-guide`

**Output**:
```
🔒 Hook Security Guide

CRITICAL SECURITY PRINCIPLES:

1. Review Before Use
   ⚠️  NEVER run hooks from untrusted sources
   ✅  Always inspect hook code before installation

2. Least Privilege
   ⚠️  Hooks run with YOUR user credentials
   ✅  Limit hook permissions to minimum required

3. Data Protection
   ⚠️  Malicious hooks can exfiltrate data
   ✅  Review all network operations in hooks

4. Version Control
   ✅  Commit project hooks to git
   ✅  Track changes with meaningful commits

5. Testing
   ✅  Test in safe environment first
   ✅  Use *test-hook before deployment

SECURITY CHECKLIST:

□ Hook code reviewed by team
□ No hardcoded credentials
□ No untrusted network calls
□ Error handling prevents crashes
□ Logging doesn't expose secrets
□ Exit codes correctly implemented
□ Command injection prevented
□ File permissions validated

Run: *validate-security [hook-name] for automated checks
```

---

## Integration

### `install-example {name}`

**Purpose**: Install pre-built hook from examples library

**Usage**: `*install-example bash-command-logger`

**Process**:
1. Downloads hook configuration from library
2. Validates dependencies are available
3. Prompts for installation location
4. Installs and tests hook

**Output**:
```
📦 Installing: bash-command-logger

Checking dependencies...
  ✅ jq found

Configuration:
  Event: PreToolUse
  Matcher: Bash
  Command: jq -r '"\(.tool_input.command)"' >> ~/.claude/bash-log.txt

Install to:
  1. User settings (all projects)
  2. Project settings (this project only)

Choice: 1

Installing...
✅ Hook installed successfully

Testing hook...
✅ Test passed

Next steps:
  - Run *test-hook bash-command-logger to verify
  - Check ~/.claude/bash-log.txt for logged commands
```

**Force install** (skip prompts):
```
*install-example bash-command-logger --user --force
```

---

### `export-hooks`

**Purpose**: Export hooks to shareable JSON file

**Usage**: `*export-hooks`

**Output**:
```
📤 Exporting hooks...

Source: .claude/settings.json

Hooks to export:
  ✓ validate-story (PreToolUse)
  ✓ auto-format (PostToolUse)

Export location: hooks-export.json

✅ Exported 2 hooks to hooks-export.json

Share with team:
  git add hooks-export.json
  git commit -m "Add project hooks"
```

**Options**:
```
*export-hooks --output my-hooks.json
*export-hooks --user  # Export only user hooks
*export-hooks --project  # Export only project hooks
```

---

### `import-hooks {file}`

**Purpose**: Import hooks from JSON file

**Usage**: `*import-hooks hooks-export.json`

**Process**:
1. Validates JSON file syntax
2. Checks for conflicts with existing hooks
3. Prompts for conflict resolution
4. Imports hooks to specified location

**Output**:
```
📥 Importing hooks from: hooks-export.json

Found 2 hooks:
  1. validate-story (PreToolUse)
  2. auto-format (PostToolUse)

Checking for conflicts...
  ⚠️  Hook 'validate-story' already exists

Conflict resolution:
  1. Skip (keep existing)
  2. Overwrite (replace with imported)
  3. Rename (keep both)

Choice for 'validate-story': 3
New name: validate-story-imported

Import to:
  1. User settings
  2. Project settings

Choice: 2

Importing...
  ✅ validate-story-imported
  ✅ auto-format

✅ Imported 2 hooks to .claude/settings.json

Run *list-hooks to see all hooks
```

---

## Command Shortcuts

| Full Command | Shortcut | Notes |
|-------------|----------|-------|
| `*list-hooks` | `*lh` | List all hooks |
| `*create-hook` | `*ch` | Create new hook |
| `*test-hook {name}` | `*th {name}` | Test hook |
| `*hook-examples` | `*hx` | Browse examples |

---

## Advanced Usage

### Chaining Commands

```bash
# Create, test, and enable in one flow
*create-hook && *test-hook my-hook && *enable-hook my-hook

# Export and commit hooks
*export-hooks --output team-hooks.json && git add team-hooks.json && git commit
```

### Filtering and Searching

```bash
# Find hooks by event type
*list-hooks --event PreToolUse

# Search examples by keyword
*hook-examples --search validation

# Show only enabled hooks
*list-hooks --enabled
```

### Batch Operations

```bash
# Disable all hooks temporarily
*disable-all-hooks

# Re-enable all hooks
*enable-all-hooks

# Delete all project hooks
*delete-hooks --project --confirm
```

---

## Troubleshooting

### Command Not Found

**Issue**: `*create-hook` not recognized

**Fix**:
1. Ensure hooks-manager skill is loaded
2. Try `*hooks` to see if skill is available
3. Reload skill: `/reload-skill hooks-manager`

### Hook Not Executing

**Issue**: Hook configured but not running

**Debug Steps**:
1. Run `*validate-config` to check syntax
2. Run `*test-hook {name}` to test execution
3. Check matcher matches the tool
4. Review Claude Code console for errors

### Permission Denied

**Issue**: Hook command fails with permission error

**Fix**:
1. Make script executable: `chmod +x hooks/script.py`
2. Check file permissions on settings file
3. Verify Python/command is in PATH

---

## Exit Codes

Hooks use exit codes to communicate results:

| Code | Meaning | Usage |
|------|---------|-------|
| 0 | Success / Allow | Operation proceeds normally |
| 1 | Error | Hook failed but operation may proceed |
| 2 | Block | Operation blocked (PreToolUse only) |
| >2 | Custom | Hook-specific error codes |

---

## Related Commands

- `/hooks` - Interactive hooks management UI
- `*help` - Show all available commands
- `*security-guide` - Security best practices

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
