---
name: status
description: Show current inference-planz session status and configuration
allowed-tools: Read, Glob
user-invocable: true
---

# Inference Planz - Status

Display current plugin status, configuration, and session information.

## Status Check

Read and display the following information:

1. **Plugin Status**
   - Enabled/Disabled
   - Version
   - Debug mode status

2. **Configuration**
   - Read from settings file locations:
     - Project: `.claude/planz.config.json`
     - User: `~/.config/inference-planz/settings.json`
     - Plugin: `${CLAUDE_PLUGIN_ROOT}/settings.json`

3. **Session State** (if any active session)
   - Current stage in pipeline
   - Artifacts collected
   - Timing information

4. **Agent Configuration**
   - Research Agent: max_tokens, temperature
   - Survey Agent: question limits, option counts
   - Plan Agent: max_tokens, provisional branch setting

5. **Timeout Settings**
   - Per-agent timeouts
   - Total pipeline timeout

## Output Format

```
## Inference Planz Status

**Plugin**: inference-planz v1.0.0
**Status**: Enabled
**Debug Mode**: Off

### Configuration Source
Using: ~/.config/inference-planz/settings.json

### Agent Settings
| Agent | Max Tokens | Timeout |
|-------|------------|---------|
| Research | 4000 | 60s |
| Survey | N/A | 45s |
| Plan | 6000 | 60s |

### Survey Settings
- Questions: 5-10
- Options per question: 3-7
- Include "Other" option: Yes

### Fallback Settings
- Enabled: Yes
- Min survey questions on failure: 5
- Use heuristics on research failure: Yes

### Current Session
No active session

### Environment Overrides
- INFERENCE_PLANZ_ENABLED: (not set)
- INFERENCE_PLANZ_DEBUG: (not set)
- INFERENCE_PLANZ_TIMEOUT: (not set)
```

## Quick Actions

After viewing status, you can:
- `/inference-planz:configure` to modify settings
- `/inference-planz:run <prompt>` to start a new session
- `/inference-planz:help` for full documentation
