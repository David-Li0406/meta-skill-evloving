---
name: hooks-knowledge
description: "Knowledge base for event-driven automation in .claude/ configuration. Teaches project-first hooks architecture with templates, security patterns, and guardrails for local project protection. Do not use for plugin-level configuration."
user-invocable: true
---

# Hooks Knowledge Base

Reference library for creating project-scoped hooks automation and guardrails in `.claude/` configuration. Contains templates, security patterns, and best practices for protecting and automating your local project.

## 🚨 MANDATORY: Read BEFORE Creating Hooks

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] Official Hooks Guide**: https://code.claude.com/docs/en/hooks
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before any hook creation or modification
  - **Content**: Hook events, configuration, prompt-based vs command hooks
  - **Cache**: 15 minutes minimum

- **[MUST READ] Security Guide**: https://code.claude.com/docs/en/security
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before implementing any hook with security implications
  - **Content**: Security best practices, input validation, path safety
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** without understanding hook events and types
- **MUST validate** security requirements before implementation
- **REQUIRED** to understand event-driven automation patterns

## Core Philosophy: Project-First Hooks

**This skill teaches the "Project Scaffolding & Guardrails" approach:**

1. **Zero Active Hooks in Toolkit**: The toolkit contains NO active hooks for users
2. **Templates, Not Execution**: Provides templates and patterns, not active configuration
3. **Project-Local Configuration**: All hooks belong in user's `.claude/` directory
4. **Component-Scoped First**: Prefer hooks in skill/agent frontmatter over global hooks
5. **Fail Fast Principle**: Use command hooks with `exit 2` for immediate blocking
6. **User Empowerment**: Users create their own guardrails, toolkit guides them

## Quick Reference

**Hooks** automate your local project through event-driven guardrails and validation.

**Use Hooks For**:
- **Guardrails**: Prevent dangerous operations (e.g., `.env` modification)
- **Validation**: Validate file operations before execution
- **Project Automation**: Initialize development environment
- **Quality Gates**: Ensure code meets project standards
- **Session Management**: Persist development decisions
- **Security**: Block unauthorized actions

**Project-First Approach**:
- **Local Configuration**: All hooks in your `.claude/hooks.json`
- **Component-Scoped**: Hooks in skill/agent frontmatter (preferred)
- **Fail Fast**: Use `exit 2` to block dangerous operations
- **Templates**: Use provided templates, customize for your project

## Project-Scoped Hook Configuration

**Two Levels for Your Local Project**:

### 1. Global Hooks (`.claude/hooks.json`)
**Target**: `${CLAUDE_PROJECT_DIR}/.claude/hooks.json`

Use for project-wide automation and infrastructure guardrails:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "validate-write.sh"
      }]
    }]
  }
}
```

**Create in your project:**
```bash
mkdir -p .claude
cat > .claude/hooks.json << 'EOF'
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "validate-file.sh"
      }]
    }]
  }
}
EOF
```

### 2. Component-Scoped Hooks (Skill/Agent Frontmatter)
**Target**: `hooks:` block in YAML frontmatter

Use for skill-specific validation and security:

```yaml
---
name: deploy-skill
description: "Deploys application"
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "run-tests.sh"
---
```

**Best Practice**: Prefer component-scoped hooks to avoid "always-on" noise. Only use global hooks for project-wide guardrails.

**Configuration Location**: Your project's `.claude/hooks.json` (global) or inline frontmatter (component-scoped)

## Hook Events

### Complete Event List (12 Events)

| Event | Trigger | Best For |
|-------|---------|----------|
| `SessionStart` | Session begins/resumes | Session initialization, environment setup |
| `UserPromptSubmit` | User submits prompt | Prompt validation, logging |
| `PreToolUse` | Before tool execution | Validation, security checks |
| `PermissionRequest` | Permission dialog appears | Custom permission logic |
| `PostToolUse` | After tool succeeds | Logging, cleanup, metrics |
| `PostToolUseFailure` | After tool fails | Error handling, recovery |
| `SubagentStart` | Spawning subagent | Subagent configuration |
| `SubagentStop` | Subagent finishes | Cleanup, result processing |
| `Stop` | Claude finishes responding | Final validation, state save |
| `PreCompact` | Before context compaction | State persistence |
| `Setup` | Repository setup/maintenance | One-time initialization |
| `SessionEnd` | Session terminates | Session cleanup |
| `Notification` | Claude Code sends notifications | Notification filtering |

---

## Common Guardrail Patterns

### Protection Hook (Fail Fast)
**Block dangerous file operations:**

```json
{
  "PreToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "command",
      "command": "guard-env-files.sh"
    }]
  }]
}
```

**Script Example** (`guard-env-files.sh`):
```bash
#!/bin/bash
FILE_PATH="$1"
if [[ "$FILE_PATH" == *".env"* ]]; then
  echo "❌ BLOCKED: Writing to .env files requires explicit approval"
  exit 2
fi
exit 0
```

### Quality Gate Hook
**Validate code before deployment:**

```yaml
---
name: deploy-skill
description: "Deploys application"
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "run-tests.sh"
---
```

### Session Persistence Hook
**Remember development decisions:**

```json
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "save-decisions.sh"
    }]
  }]
}
```

**Reference**: [Session Persistence Pattern](references/session-persistence.md)

---

### 1. SessionStart
**Trigger**: Session begins or resumes (matchers: startup, resume, clear, compact)

**Use For**:
- Session initialization
- Environment variable persistence via `CLAUDE_ENV_FILE`
- Context setup
- Resource allocation

**Example**:
```json
{
  "SessionStart": [{
    "matcher": "startup|resume",
    "hooks": [{
      "type": "command",
      "command": "setup-session.sh"
    }]
  }]
}
```

### 2. UserPromptSubmit
**Trigger**: User submits a prompt

**Use For**:
- Prompt validation
- User intent logging
- Prompt preprocessing

**Example**:
```json
{
  "UserPromptSubmit": [{
    "hooks": [{
      "type": "command",
      "command": "validate-prompt.sh \"$PROMPT\""
    }]
  }]
}
```

### 3. PreToolUse
**Trigger**: Before tool execution

**Use For**:
- Validation before execution
- Security checks
- Path safety verification
- Permission checks

**Example**:
```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "prompt",
      "prompt": "Validate this file operation is safe."
    }]
  }]
}
```

### 4. PermissionRequest
**Trigger**: Permission dialog appears

**Use For**:
- Custom permission logic
- Security validation
- Access control
- Compliance checks

**Example**:
```json
{
  "PermissionRequest": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "prompt",
      "prompt": "Evaluate if this command should be allowed."
    }]
  }]
}
```

### 5. PostToolUse
**Trigger**: After tool succeeds

**Use For**:
- Logging successful operations
- Cleanup after execution
- Metrics collection
- Result validation

**Example**:
```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "log-success.sh $TOOL_NAME"
    }]
  }]
}
```

### 6. PostToolUseFailure
**Trigger**: After tool fails

**Use For**:
- Error logging
- Recovery actions
- Fallback mechanisms
- Error notifications

**Example**:
```json
{
  "PostToolUseFailure": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "handle-error.sh $ERROR_TYPE"
    }]
  }]
}
```

### 7. SubagentStart
**Trigger**: When spawning a subagent

**Use For**:
- Subagent configuration
- Context injection
- Subagent-specific setup

**Example**:
```json
{
  "SubagentStart": [{
    "hooks": [{
      "type": "command",
      "command": "configure-subagent.sh $SUBAGENT_NAME"
    }]
  }]
}
```

### 8. SubagentStop
**Trigger**: When subagent finishes

**Use For**:
- Subagent cleanup
- Result processing
- Output collection

**Example**:
```json
{
  "SubagentStop": [{
    "hooks": [{
      "type": "prompt",
      "prompt": "Review subagent output for quality."
    }]
  }]
}
```

### 9. Stop
**Trigger**: Claude finishes responding

**Use For**:
- Final validation
- State persistence (use with PreCompact)
- Resource release
- Quality checks

**Example**:
```json
{
  "Stop": [{
    "hooks": [{
      "type": "prompt",
      "prompt": "Review the response for quality and completeness."
    }]
  }]
}
```

### 10. PreCompact
**Trigger**: Before context compaction

**Use For**:
- State persistence before compaction
- Memory optimization
- Critical data save

**Matchers**: `manual` (user-initiated), `auto` (system-triggered)

**Example**:
```json
{
  "PreCompact": [{
    "matcher": "auto",
    "hooks": [{
      "type": "command",
      "command": "save-state.sh"
    }]
  }]
}
```

### 11. Setup
**Trigger**: Repository setup/maintenance

**Use For**:
- One-time initialization
- Dependency installation
- Configuration setup

**Note**: Distinct from SessionStart - Setup runs once, SessionStart runs every session.

**Example**:
```json
{
  "Setup": [{
    "hooks": [{
      "type": "command",
      "command": "install-dependencies.sh"
    }]
  }]
}
```

### 12. SessionEnd
**Trigger**: Session terminates

**Use For**:
- Session cleanup
- Resource deallocation
- Session summary

**Anti-Pattern**: Don't use for state save (use Stop + PreCompact instead).

**Example**:
```json
{
  "SessionEnd": [{
    "hooks": [{
      "type": "command",
      "command": "cleanup-session.sh"
    }]
  }]
}
```

### 13. Notification
**Trigger**: Claude Code sends notifications

**Use For**:
- Notification filtering
- Custom notification handling
- Alert routing

**Type Matchers**: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`

**Example**:
```json
{
  "Notification": [{
    "matcher": "permission_prompt",
    "hooks": [{
      "type": "command",
      "command": "handle-permission.sh"
    }]
  }]
}
```

## Hook Types

### Prompt Hooks (LLM-Based)
**Use For**: Stop, SubagentStop events only

Prompt hooks use Haiku (fast LLM) for LLM-based evaluation. The model evaluates the prompt and makes decisions.

**Best For**:
- Quality validation (Stop/SubagentStop)
- Content review
- Decision-making requiring judgment

**Example**:
```json
{
  "Stop": [{
    "hooks": [{
      "type": "prompt",
      "prompt": "Review this response for quality, clarity, and completeness. Flag any issues."
    }]
  }]
}
```

**⚠️ Important**: Prompt hooks ONLY work for Stop and SubagentStop events. For all other events, use command hooks.

### Command Hooks (Bash-Based)
**Use For**: All events (faster, deterministic)

Command hooks execute external bash commands/scripts. They're fast, deterministic, and work with every event type.

**Best For**:
- Validation rules
- Security checks
- Logging
- State persistence
- File operations

**Example**:
```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "validate-file.sh \"$FILE_PATH\""
    }]
  }]
}
```

**Exit Codes**:
- `0`: Success (stdout shown in verbose mode, except UserPromptSubmit/SessionStart where it's added to context)
- `1`: Non-blocking error (logged but doesn't block operation)
- `2`: Blocking error (stderr shown to Claude, operation blocked)

**Security**: Always quote variables: `"$VAR"` not `$VAR`

## Configuration

### Create Hooks Directory
```bash
mkdir -p hooks
```

### Create hooks.json
```json
{
  "hooks": {
    "EventName": [{
      "matcher": "ToolName",
      "hooks": [{
        "type": "prompt|command",
        "prompt|command": "..."
      }]
    }]
  }
}
```

### Add to Plugin
```json
{
  "name": "my-plugin",
  "hooks": {
    "PreToolUse": [...]
  }
}
```

## Component-Scoped Hooks (Recommended)

**Overview**: Skills and agents can define hooks in their frontmatter (YAML header). These hooks are only active during that component's execution.

**Best For**: Component-specific validation, security checks, and quality gates

**Supported Events**: PreToolUse, PostToolUse, Stop

**Example (Skill Frontmatter)**:
```yaml
---
name: deploy-skill
description: "Deploys application to production"
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "run-tests.sh"
  Stop:
    - hooks:
        - type: "prompt"
          prompt: "Review deployment quality and rollback plan."
---
```

**Example (Agent Frontmatter)**:
```yaml
---
name: code-auditor
description: "Audits code for security issues"
hooks:
  PostToolUse:
    - matcher: "Grep"
      hooks:
        - type: "command"
          command: "validate-findings.sh"
---
```

**Scoping Hierarchy** (precedence order):
1. **Component-scoped** (highest): Active only during component execution, auto-cleanup
2. **Project-level** (recommended): Global hooks in `.claude/hooks.json`
3. **User-level** (lowest): Organizational policies

**Best Practice**:
- ✅ **Prefer component-scoped hooks** to avoid "always-on" noise
- ✅ Use for skill-specific validation and security
- ✅ Block dangerous operations with `exit 2`
- ❌ **Avoid** plugin-level hooks (not project-scoped)

**Anti-Pattern**: SessionStart hooks that only echo/print without functional behavior (cosmetic noise).

## Security Guardrails

### Path Safety (Fail Fast)
**Block dangerous file operations in your project:**

```json
{
  "PreToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "command",
      "command": "guard-sensitive-paths.sh"
    }]
  }]
}
```

**Script Template** (`guard-sensitive-paths.sh`):
```bash
#!/bin/bash
FILE_PATH="$1"

# Block sensitive files
if [[ "$FILE_PATH" =~ \.env$ ]] || [[ "$FILE_PATH" =~ \.aws/credentials$ ]]; then
  echo "❌ BLOCKED: Sensitive file modification requires explicit approval"
  exit 2
fi

# Block deletion of important directories
if [[ "$FILE_PATH" =~ node_modules/ ]] || [[ "$FILE_PATH" =~ .git/ ]]; then
  echo "❌ BLOCKED: Protected directory modification"
  exit 2
fi

exit 0
```

### Input Validation (Quality Gates)
**Validate operations before execution:**

```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "validate-command.sh"
    }]
  }]
}
```

**Script Template** (`validate-command.sh`):
```bash
#!/bin/bash
COMMAND="$1"

# Block dangerous commands
if [[ "$COMMAND" =~ rm[[:space:]]+-rf ]] || [[ "$COMMAND" =~ sudo.*rm ]]; then
  echo "❌ BLOCKED: Dangerous deletion command"
  exit 2
fi

exit 0
```

## Implementation for Your Project

### Step 1: Identify Your Need
**What guardrail do you need?**
- Block dangerous operations? → PreToolUse + `exit 2`
- Validate before deployment? → PreToolUse + command hook
- Remember decisions? → Stop + state save
- Quality gate? → Stop + prompt hook

### Step 2: Choose Scope
**Component-scoped (Recommended)**:
```yaml
---
name: my-skill
description: "My skill"
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: "command"
          command: "validate.sh"
---
```

**Global (Project-wide)**:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "validate.sh"
      }]
    }]
  }
}
```

### Step 3: Create Hook Configuration
**For your project**:
```bash
# Create hooks directory
mkdir -p .claude

# Create hooks.json with your configuration
cat > .claude/hooks.json << 'EOF'
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "guard-files.sh"
      }]
    }]
  }
}
EOF
```

### Step 4: Test Guardrail
1. Create file that should be blocked
2. Verify hook blocks it
3. Test `exit 2` returns error correctly
4. Validate security pattern

## Examples: Project Guardrails

### 1. Environment File Protection
**Blocks accidental `.env` file modifications:**

```bash
# Create in your project: .claude/hooks.json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "guard-env.sh"
      }]
    }]
  }
}
```

```bash
# Create script: guard-env.sh
#!/bin/bash
FILE_PATH="$1"
if [[ "$FILE_PATH" == *".env"* ]]; then
  echo "❌ BLOCKED: .env files require explicit approval"
  exit 2
fi
exit 0
```

### 2. Deployment Quality Gate
**Validates tests before deployment:**

```yaml
---
name: deploy-to-prod
description: "Deploys to production"
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "run-tests.sh"
---
```

```bash
# Script: run-tests.sh
#!/bin/bash
echo "Running tests..."
npm test
if [ $? -ne 0 ]; then
  echo "❌ BLOCKED: Tests failed"
  exit 2
fi
exit 0
```

### 3. Session Persistence
**Remembers your development decisions:**

```bash
# Create: .claude/hooks.json
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "save-decisions.sh"
    }]
  }]
}
```

```bash
# Script: save-decisions.sh
#!/bin/bash
# Extract decisions from conversation and save to .claude/STATE.md
# See references/session-persistence.md for full implementation
```

## Best Practices: Project-First Approach

### DO ✅
- **Prefer component-scoped hooks** over global hooks
- Use `exit 2` to block dangerous operations immediately
- Validate all file paths before writes/edits
- Create scripts in your project's `.claude/scripts/` directory
- Test guardrails with intentionally dangerous operations
- Keep hooks fast (<10 seconds timeout)
- Document what each guardrail protects

### DON'T ❌
- **Don't create plugin-level hooks** (not project-scoped)
- Don't execute untrusted commands without validation
- Don't use hooks for cosmetic messages (SessionStart echo)
- Don't create conflicting hooks across components
- Don't ignore security warnings in your guardrails
- Don't use prompt hooks for non-Stop/SubagentStop events

### Project Configuration Checklist
- [ ] Created `.claude/hooks.json` for global guardrails
- [ ] Added hooks to skill frontmatter where needed
- [ ] All scripts in `.claude/scripts/` directory
- [ ] Tested blocking behavior with `exit 2`
- [ ] Validated path safety in PreToolUse hooks
- [ ] Documented guardrail purposes in README

## Troubleshooting

### Hook Not Triggering
1. Verify event name is correct
2. Check matcher syntax
3. Validate JSON format
4. Test with simple hook first

### Invalid JSON
1. Use JSON validator
2. Check for trailing commas
3. Verify quotes are proper
4. Test syntax

### Security Errors
1. Review path safety
2. Check input validation
3. Verify command restrictions
4. Update security policies

## Detailed Examples

Complete hook configurations:
- PreToolUse validation
- PostToolUse logging
- Error recovery patterns

Advanced patterns:
- Multi-hook chains
- Conditional hooks
- State management

Error handling strategies:
- Graceful degradation
- Retry logic
- User feedback

## Session Persistence Pattern

**Purpose**: Memory persistence for plugin development decisions

**State File**: `${CLAUDE_PROJECT_DIR}/.claude/TOOLKIT_STATE.md`

**Use When**: Implementing hooks that save/load plugin development state (manifest decisions, naming conventions, validation issues)

**Implementation**: See [session-persistence.md](references/session-persistence.md) for:
- State schema specification
- Hook configuration (SessionStart/Stop/PreCompact)
- State extraction logic from transcripts
- Integration patterns with toolkit-architect

## Additional Resources

- **Hooks Guide**: https://code.claude.com/docs/en/hooks
- **Security Guide**: https://code.claude.com/docs/en/security
- **Plugin Structure**: https://code.claude.com/docs/en/plugins
