# Hook Lifecycle and Event Types

> **Pattern**: Choose the right event for the right purpose
> **Use For**: Understanding when each hook type fires
> **Philosophy**: Event-driven automation aligned with session lifecycle

## Hook Lifecycle Overview

```
Session Lifecycle:
┌─────────────┐
│ SessionStart│ ← Initialize environment
└──────┬──────┘
       │
       ▼
┌─────────────┐
│User Submits │
│   Prompt    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ PreToolUse  │ ← Validate before execution
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Tool     │ ← Execute operation
│  Executes   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│PostToolUse  │ ← Process results
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Stop       │ ← Review quality, save state
└──────┬──────┘
       │
       ▼
┌─────────────┐
│PreCompact   │ ← Save before compaction
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ SessionEnd  │ ← Cleanup resources
└─────────────┘
```

## Event Categories

### Session Management Events

#### 1. SessionStart
**When**: Session begins, resumes, clears, or compacts
**Match**: `startup`, `resume`, `clear`, `compact`

**Use For**:
- Initialize project environment
- Check dependencies
- Load session state
- Set up development tools

**Example**:
```json
{
  "SessionStart": [{
    "matcher": "startup",
    "hooks": [{
      "type": "command",
      "command": "init-project.sh"
    }]
  }]
}
```

**Script Template** (`init-project.sh`):
```bash
#!/bin/bash
echo "🚀 Initializing project..."

# Check Node.js
if ! command -v node &> /dev/null; then
  echo "❌ Node.js not installed"
  exit 2
fi

# Install dependencies
if [ ! -d "node_modules" ]; then
  npm install
fi

# Validate environment
if [ ! -f ".env.example" ]; then
  echo "⚠️  Missing .env.example"
fi

echo "✅ Project initialized"
exit 0
```

#### 2. SessionEnd
**When**: Session terminates
**Use For**:
- Cleanup temporary files
- Close connections
- Final logging

**Example**:
```json
{
  "SessionEnd": [{
    "hooks": [{
      "type": "command",
      "command": "cleanup.sh"
    }]
  }]
}
```

**⚠️ Note**: Don't use for state save (use Stop + PreCompact instead).

### Tool Execution Events

#### 3. PreToolUse
**When**: Before tool execution
**Use For**:
- Validate inputs
- Security checks
- Path safety
- Permission checks

**Example**:
```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit|Read",
    "hooks": [{
      "type": "command",
      "command": "validate-file.sh"
    }]
  }]
}
```

#### 4. PostToolUse
**When**: After tool succeeds
**Use For**:
- Log operations
- Process results
- Cleanup
- Metrics

**Example**:
```json
{
  "PostToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "log-command.sh"
    }]
  }]
}
```

#### 5. PostToolUseFailure
**When**: After tool fails
**Use For**:
- Error logging
- Recovery actions
- Fallback mechanisms

**Example**:
```json
{
  "PostToolUseFailure": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "handle-error.sh"
    }]
  }]
}
```

### User Interaction Events

#### 6. UserPromptSubmit
**When**: User submits prompt
**Use For**:
- Prompt validation
- Logging
- Preprocessing

**Example**:
```json
{
  "UserPromptSubmit": [{
    "hooks": [{
      "type": "command",
      "command": "validate-prompt.sh"
    }]
  }]
}
```

#### 7. PermissionRequest
**When**: Permission dialog appears
**Use For**:
- Custom permission logic
- Security validation

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

### Subagent Events

#### 8. SubagentStart
**When**: Spawning subagent
**Use For**:
- Subagent configuration
- Context injection

**Example**:
```json
{
  "SubagentStart": [{
    "hooks": [{
      "type": "command",
      "command": "setup-subagent.sh"
    }]
  }]
}
```

#### 9. SubagentStop
**When**: Subagent finishes
**Use For**:
- Cleanup
- Result processing
- Quality review (with prompt hook)

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

### System Events

#### 10. Stop
**When**: Claude finishes responding
**Use For**:
- Final validation (command or prompt)
- State persistence
- Quality checks (prompt hook)

**Example**:
```json
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "save-state.sh"
    }]
  }]
}
```

#### 11. PreCompact
**When**: Before context compaction
**Match**: `manual` or `auto`
**Use For**:
- State persistence
- Memory optimization

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

#### 12. Setup
**When**: Repository setup/maintenance
**Use For**:
- One-time initialization
- Dependency installation

**Example**:
```json
{
  "Setup": [{
    "hooks": [{
      "type": "command",
      "command": "install-deps.sh"
    }]
  }]
}
```

**⚠️ Note**: Distinct from SessionStart - Setup runs once, SessionStart runs every session.

#### 13. Notification
**When**: Claude Code sends notifications
**Use For**:
- Notification filtering
- Custom handling

**Example**:
```json
{
  "Notification": [{
    "matcher": "permission_prompt",
    "hooks": [{
      "type": "command",
      "command": "handle-notification.sh"
    }]
  }]
}
```

## Choosing the Right Event

### Decision Tree

```
Need to validate before execution?
├─ Yes → PreToolUse
└─ No

Need to run after successful operation?
├─ Yes → PostToolUse
└─ No

Need to handle errors?
├─ Yes → PostToolUseFailure
└─ No

Need to review quality?
├─ Yes → Stop (prompt hook)
└─ No

Need to remember state?
├─ Yes → Stop + PreCompact
└─ No

Need to initialize environment?
├─ Yes → SessionStart
└─ No

Need to cleanup?
├─ Yes → SessionEnd
└─ Done
```

## Event Combinations

### Common Combinations

#### 1. Complete Validation Pipeline
```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "validate-command.sh"
    }]
  }],
  "PostToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "log-command.sh"
    }]
  }],
  "Stop": [{
    "hooks": [{
      "type": "prompt",
      "prompt": "Review execution quality."
    }]
  }]
}
```

#### 2. State Persistence
```json
{
  "SessionStart": [{
    "matcher": "startup|resume",
    "hooks": [{
      "type": "command",
      "command": "load-state.sh"
    }]
  }],
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "save-state.sh"
    }]
  }],
  "PreCompact": [{
    "matcher": "manual|auto",
    "hooks": [{
      "type": "command",
      "command": "save-state.sh"
    }]
  }]
}
```

#### 3. Security Guardrails
```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit|Bash",
    "hooks": [{
      "type": "command",
      "command": "security-check.sh"
    }]
  }]
}
```

## Anti-Patterns

### DON'T Use:
- **SessionEnd for state save** (use Stop + PreCompact)
- **SessionStart for one-time setup** (use Setup)
- **Prompt hooks for PreToolUse** (use command hooks)
- **Notification hooks for logging** (use PostToolUse)
- **Multiple hooks for same event** (combine logic)

## Performance Considerations

### Fast Events (< 1 second)
- PreToolUse
- PostToolUse
- PostToolUseFailure

### Moderate Events (1-5 seconds)
- SessionStart
- SessionEnd
- Stop (command)
- PreCompact

### Slow Events (5+ seconds)
- Stop (prompt)
- SubagentStop (prompt)
- Setup

**Best Practice**: Keep PreToolUse hooks as fast as possible (user is waiting).

## Reference

- **Hooks Guide**: https://code.claude.com/docs/en/hooks
- **Command Hooks**: [command-hooks.md](command-hooks.md)
- **Prompt Hooks**: [prompt-hooks.md](prompt-hooks.md)
- **Security Patterns**: [security-patterns.md](security-patterns.md)
- **Session Persistence**: [session-persistence.md](session-persistence.md)
