---
name: strategic-compaction
description: Use this skill to suggest context compression at logical breakpoints during development sessions to optimize efficiency.
---

# Strategic Compaction Skill

This skill is designed to suggest context compression at appropriate times, enhancing session efficiency.

## Trigger Conditions

- Tool usage reaches a threshold
- Transitioning from research/exploration to implementation
- Completion of a milestone
- Finalization of plans

## Importance of Strategic Compaction

### Issues with Automatic Compression

- Can occur at any point, often mid-task
- May lose important context
- Disrupts thought continuity

### Advantages of Strategic Compaction

- Compresses at logical phase boundaries
- Retains key decisions and context
- Compresses after exploration and before execution
- Compresses after milestone completion

## Timing for Compression

### Suitable Times for Compression

```
1. Completion of exploration/research, ready to start implementation
2. Plans finalized, ready for execution
3. Completion of a functional module
4. Resolution of a complex issue
5. Completion of code review feedback
6. Context usage rate > 70%
```

### Unsuitable Times for Compression

```
1. During debugging
2. Multi-file modifications incomplete
3. Fixing failed tests
4. Important decision discussions ongoing
5. Midway through complex logic implementation
```

## Pre-Compression Checklist

```markdown
## Pre-Compression Confirmation

- [ ] Current task status recorded in progress.md
- [ ] Key decisions documented
- [ ] Pending assumptions noted
- [ ] Unfinished code changes saved
- [ ] Next steps clearly defined

## Compression Content

- Current progress
- Key decisions and reasons
- Pending items
- Next tasks
```

## Usage

### Manual Trigger

```
/compact
```

### Automatic Suggestions

The system will prompt to consider compression when:

1. **Tool usage reaches a threshold** (default 50 times)
2. **At regular intervals** (default reminder every 25 tool usages)

## Configuration

### Threshold Configuration

```bash
# Environment variable
export COMPACT_THRESHOLD=50  # Initial reminder tool usage count
```

### Hook Configuration

In `settings.local.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash skills/strategic-compact/suggest-compact.sh"
          }
        ],
        "description": "Suggest compression at logical intervals"
      }
    ]
  }
}
```

## Compression Summary Template

Ensure the following information is included during compression:

```markdown
## Session Summary

### Completed Tasks

1. [Task 1 description]
2. [Task 2 description]

### Key Decisions

| Decision | Reason | Confidence |
| ------- | ------ | -------- |
| [Decision 1] | [Reason] | High/Medium/Low |

### Current Status

- Progress: [Percentage or Stage]
- Blockers: [If any]

### Pending Items

- [ ] [Pending item 1]
- [ ] [Pending item 2]

### Next Steps

[Clearly defined next task]
```

## Best Practices

1. **Phase Boundary Compression** - Transitioning from exploration to implementation, design to coding
2. **Record Before Compression** - Update progress.md first
3. **Clarify Next Steps** - Include next steps in the compression summary
4. **Avoid Mid-Task Compression** - Refrain from compressing during complex tasks
5. **Monitor Context Rate** - Consider compression when exceeding 70% context usage
6. **Retain Key Decisions** - Bring important decisions into the new context
7. **Label Pending Items** - Clearly mark uncertain content

---

**Remember**: The timing of good compression is more important than the compression itself. Compress at logical breakpoints to maintain thought continuity.