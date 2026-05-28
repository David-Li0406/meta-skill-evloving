---
name: error-recovery
description: Handle Claude Code errors gracefully - error types, recovery, prevention
version: 1.0.0
author: Claude Code SDK
tags: [errors, recovery, handling, prevention]
---

# Error Recovery

Handle Claude Code errors gracefully with systematic recovery strategies and prevention techniques.

## Quick Reference

| Error Category | Common Causes | Quick Fix |
|----------------|---------------|-----------|
| API Errors | Rate limits, overload, auth | Wait, retry, check credentials |
| Tool Errors | Permissions, missing files | Check permissions, validate paths |
| Context Errors | Token overflow, corruption | `/compact` or `/clear` |
| MCP Errors | Server disconnect, timeout | Restart server, check logs |
| Hook Errors | JSON syntax, script failure | Validate JSON, test script |

## Error Message Anatomy

Claude Code error messages follow a consistent pattern:

```
[Error Category] [Specific Error]: [Description]
  at [Location/Context]
  Cause: [Root cause if known]
  Suggestion: [Recommended action]
```

### Reading Error Messages

| Part | What It Tells You | Action |
|------|-------------------|--------|
| Category | Type of error (API, Tool, etc.) | Determines recovery approach |
| Specific Error | Exact error code/name | Look up in error reference |
| Description | Human-readable explanation | Understand what went wrong |
| Location | Where error occurred | Identify failing component |
| Cause | Why it happened | Fix root cause |
| Suggestion | Recommended fix | Try suggested action first |

## Common Error Patterns

### API Errors

| Error | Meaning | Recovery |
|-------|---------|----------|
| `rate_limit_error` | Too many requests | Wait 60s, reduce frequency |
| `overloaded_error` | API at capacity | Wait 30-60s, retry |
| `context_length_exceeded` | Too many tokens | `/compact` or split request |
| `authentication_error` | Invalid/expired token | `claude auth login` |
| `invalid_request_error` | Malformed request | Check input format |
| `api_error` | Server-side issue | Retry with backoff |

### Tool Errors

| Error | Meaning | Recovery |
|-------|---------|----------|
| `permission_denied` | Tool not allowed | `/permissions`, allow tool |
| `file_not_found` | Path doesn't exist | Verify path, check working dir |
| `directory_not_found` | Dir doesn't exist | Create directory first |
| `read_error` | Can't read file | Check permissions, encoding |
| `write_error` | Can't write file | Check permissions, disk space |
| `command_failed` | Bash command error | Check exit code, stderr |
| `timeout` | Operation too slow | Increase timeout, simplify |

### Context Errors

| Error | Meaning | Recovery |
|-------|---------|----------|
| `context_overflow` | Token limit reached | `/compact` or `/clear` |
| `memory_limit` | Too much in memory | Clear memory banks |
| `session_expired` | Session timed out | Start new session |
| `state_corruption` | Session state invalid | `/clear`, restart |

## Recovery Workflow

### Step 1: Identify Error Type

```
Error occurred
    |
    +-- API Error?
    |   +-- Yes --> See API recovery
    |   +-- No --> Continue
    |
    +-- Tool Error?
    |   +-- Yes --> See Tool recovery
    |   +-- No --> Continue
    |
    +-- Context Error?
    |   +-- Yes --> See Context recovery
    |   +-- No --> Continue
    |
    +-- Unknown?
        +-- Check debug output
        +-- Use /bug to report
```

### Step 2: Apply Recovery Strategy

**For API Errors:**
1. Wait for rate limit window (60s typical)
2. Retry with exponential backoff
3. If persistent, check credentials

**For Tool Errors:**
1. Check `/permissions`
2. Validate inputs (paths, arguments)
3. Check file/directory exists

**For Context Errors:**
1. Run `/compact` to reduce context
2. If severe, use `/clear`
3. Start fresh if corrupted

### Step 3: Verify Recovery

```bash
# Check system health
claude doctor

# Verify specific component
/permissions  # Tool permissions
/mcp          # MCP servers
/hooks        # Hook status
```

## Quick Recovery Commands

| Situation | Command |
|-----------|---------|
| Context too large | `/compact` |
| Session corrupted | `/clear` |
| Need to restart | `Ctrl+C`, restart `claude` |
| Check health | `claude doctor` |
| Debug mode | `claude --debug` |
| Verbose logging | `ANTHROPIC_LOG=debug claude` |

## Retry Patterns

### Simple Retry

For transient errors (rate limits, overload):

```
1. Wait initial delay (1s)
2. Retry operation
3. If fails, double delay (2s, 4s, 8s...)
4. Max 5 retries or 60s total
5. If still failing, escalate
```

### Backoff with Jitter

For high-contention scenarios:

```
delay = min(cap, base * 2^attempt) + random(0, 1000ms)
```

- Base: 1000ms
- Cap: 60000ms
- Jitter: 0-1000ms random

### Circuit Breaker

For persistent failures:

```
If 3 failures in 60s:
    Open circuit (stop trying)
    Wait 5 minutes
    Try once (half-open)
    If success: close circuit
    If failure: keep open
```

## Error Prevention Checklist

Before operations:
- [ ] Validate file paths exist
- [ ] Check permissions are granted
- [ ] Verify network connectivity
- [ ] Ensure context has headroom
- [ ] Test hooks work correctly

During operations:
- [ ] Watch for warning signs
- [ ] Monitor context size
- [ ] Handle errors gracefully
- [ ] Log important state

After errors:
- [ ] Document what happened
- [ ] Fix root cause
- [ ] Add prevention measures
- [ ] Test fix works

## Reference Files

| File | Contents |
|------|----------|
| [ERROR-TYPES.md](./ERROR-TYPES.md) | Comprehensive error reference |
| [RECOVERY-PATTERNS.md](./RECOVERY-PATTERNS.md) | Recovery strategies and patterns |
| [PREVENTION.md](./PREVENTION.md) | Error prevention techniques |

## Common Scenarios

### Scenario: Rate Limited

**Symptom:** `rate_limit_error` after many requests

**Solution:**
1. Wait 60 seconds
2. Reduce request frequency
3. Batch operations when possible

### Scenario: Context Overflow

**Symptom:** `context_length_exceeded` error

**Solution:**
1. Run `/compact` to summarize context
2. If still too large, `/clear` and restart
3. Use smaller file reads (with offset/limit)

### Scenario: Tool Permission Denied

**Symptom:** Tool blocked by permissions

**Solution:**
1. Run `/permissions`
2. Allow the specific tool
3. Or add to settings.json for persistence

### Scenario: MCP Server Disconnected

**Symptom:** MCP tools return errors

**Solution:**
1. Check `/mcp` for server status
2. Restart MCP server if needed
3. Verify `.mcp.json` configuration

## Best Practices

1. **Fail Fast**: Validate early, fail before expensive operations
2. **Graceful Degradation**: Have fallbacks for non-critical features
3. **Clear Errors**: Provide actionable error messages
4. **Log Everything**: Enable debug mode when troubleshooting
5. **Test Recovery**: Verify recovery procedures work before you need them

## When to Escalate

Use `/bug` command when:
- Error persists after recovery attempts
- Error message is unclear or missing
- Behavior contradicts documentation
- Reproducible crash occurs

Include in report:
- Claude Code version
- Error message (full text)
- Steps to reproduce
- Debug output
