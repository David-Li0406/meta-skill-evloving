---
name: writing-hooks
description: "Use when creating hooks for prompt interception, permission handling, or event-triggered automation with timeout and bypass handling."
---

# Writing Hooks

## Overview

Hooks intercept events (prompts, permissions, tool calls) to inject behavior. Good hooks are fast, have graceful failures, and define bypass conditions.

## When to Create

**Create a hook when:**
- Behavior should apply to ALL relevant events
- Pre-processing or validation is needed
- Automation can replace manual steps
- Skill activation should be automatic

**Don't create for:**
- Occasional interventions (use rules)
- Complex logic (use commands or skills)
- User-initiated workflows (use commands)

## Structure Template

```markdown
---
name: hook-name
type: [UserPromptSubmit | PermissionRequest | ToolExecution]
timeout_ms: [number]
---

# Hook Name

## Purpose
[What this hook accomplishes]

## Trigger Event
[Exact event type and conditions]

## Input Format
[JSON structure received]

## Processing Logic
[What the hook does]

## Output Format
[JSON structure returned or modification made]

## Timeout Handling
[What happens if hook exceeds timeout]

## Bypass Conditions
[When hook should be skipped]

## Error Handling
[Graceful failure behavior]
```

## Quality Checklist

- [ ] Hook type correctly identified
- [ ] Timeout is reasonable (< 5000ms for prompt hooks)
- [ ] Input/output JSON formats defined
- [ ] Bypass conditions explicit
- [ ] Error handling prevents blocking
- [ ] Graceful degradation (fails open, not closed)
- [ ] No side effects on main context
- [ ] Cross-platform if using scripts

## Testing Requirements

1. **Trigger test** - Hook fires on correct events
2. **Timeout test** - Behavior when timeout exceeded
3. **Bypass test** - Skipped when conditions met
4. **Error test** - Graceful failure on exceptions
5. **Performance test** - Stays within timeout
6. **Platform test** - Works on Windows/Mac/Linux

## Examples

**Good Hook (Skill Activation):**
```markdown
---
name: skill-activation
type: UserPromptSubmit
timeout_ms: 3000
---

## Purpose
Analyze prompts and recommend relevant skills.

## Trigger Event
Every UserPromptSubmit event.

## Input Format
{
  "session_id": "string",
  "prompt": "string"
}

## Processing Logic
1. Parse prompt for keywords
2. Match against skill-rules.json
3. Append skill recommendations to prompt

## Output Format
{
  "prompt": "original + skill recommendations"
}

## Timeout Handling
Return original prompt unchanged.

## Bypass Conditions
- Prompt starts with /command
- Prompt is < 5 characters

## Error Handling
Log error, return original prompt.
```

**Good Hook (Permission):**
```markdown
---
name: safe-permissions
type: PermissionRequest
timeout_ms: 5000
---

## Purpose
Auto-approve safe operations, block dangerous ones.

## Processing Logic
Tier 1 (fast approve): Read, Write, Glob, Grep
Tier 2 (fast deny): rm -rf /, force push main
Tier 3 (analyze): Everything else via LLM

## Bypass Conditions
- User in --dangerous mode
```

**Bad Hook:**
```markdown
---
name: helper-hook
---

Does helpful things when stuff happens.
```
(No type, no timeout, no error handling)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No timeout defined | Add reasonable timeout_ms |
| Fails closed | Fail open (return unchanged input) |
| No bypass conditions | Define when to skip |
| Platform-specific | Use cross-platform scripts |
| Side effects | Hooks should be pure/stateless |
| Too slow | Optimize or move logic elsewhere |
