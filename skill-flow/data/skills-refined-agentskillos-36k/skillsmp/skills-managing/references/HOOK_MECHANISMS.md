# Hook Mechanisms - Deep Dive

Technical deep dive into how activation hooks work in the skill system.

## Table of Contents

- [Activation Flow](#activation-flow)
- [Exit Code Behavior](#exit-code-behavior)
- [Session State Management](#session-state-management)
- [Performance Considerations](#performance-considerations)

---

## Activation Flow

### Execution Sequence

```
User submits prompt
    ↓
System reads registry.json
    ↓
Matches keywords + intent patterns
    ↓
Groups matches by priority
    ↓
Outputs skill suggestion
    ↓
Skill content loaded into context
    ↓
Agent processes with skill knowledge
```

### Key Points

- **Timing**: Skill matching happens BEFORE processing
- **Behavior**: Non-blocking, advisory suggestions
- **Purpose**: Load relevant domain knowledge

---

## Exit Code Behavior

### For Suggestion Hooks

- **Exit 0**: Allow (always use this)
- **stdout**: Becomes context for the Agent

### For Guard Hooks

- **Exit 0**: Allow operation
- **Exit 2**: Block operation with message
- **stdout**: Message shown to user

### Critical Rule

> Never exit with code 1 - this is reserved for errors and will cause unexpected behavior.

---

## Session State Management

### Purpose

Track which skills have been activated in a session to avoid redundant suggestions.

### Implementation

```
.agent/hooks/state/
├── session-{id}.json
└── activated-skills.json
```

### State Structure

```json
{
  "sessionId": "abc123",
  "activatedSkills": ["skill-a", "skill-b"],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Behavior

- First activation: Show full suggestion
- Repeat activation: Skip or show abbreviated
- Session end: Clear state

---

## Performance Considerations

### Target Metrics

- **Keyword matching**: < 50ms
- **Intent patterns**: < 100ms
- **File content patterns**: < 200ms

### Performance Bottlenecks

1. **Loading registry.json** (every check)
   - Solution: Cache in memory
   
2. **Reading file content**
   - Only when contentPatterns configured
   - Slow for large files
   
3. **Regex compilation**
   - Compile once, cache result
   - Avoid complex patterns

### Optimization Strategies

**Reduce patterns:**
- Use more specific patterns
- Combine similar patterns

**File path patterns:**
- More specific = fewer files to check
- Example: `src/services/**` better than `**/*`

**Content patterns:**
- Only add when truly necessary
- Simpler regex = faster matching

---

**Related Files:**
- [SKILL.md](../SKILL.md) - Main skill guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Debug hook issues
- [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md) - Configuration reference
