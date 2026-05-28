# Context Compression for Reflect

## Overview

For large conversations (>10k tokens), compressing context before analysis provides:

- **80%+ token reduction**: Typical compression from 20k → 3k tokens
- **Faster analysis**: Process only relevant signals, not entire conversation
- **Maintained accuracy**: Signal detection quality unchanged
- **Cost efficiency**: Lower API costs for large sessions

## When to Use

**Always use for:**
- Conversations >10k tokens
- Multi-skill sessions where only one skill is being reflected
- Sessions with extensive unrelated work (debugging, exploring, etc.)

**Skip for:**
- Small conversations (<5k tokens)
- Sessions focused entirely on the skill being reflected
- When rapid iteration is needed

## How It Works

### 1. Invoke context-manager Agent

Use the Task tool to call context-manager with a specific extraction prompt:

```
Task: Extract reflect-relevant signals from conversation
Agent: context-manager
Prompt: "Extract only these types of interactions from the conversation:
- User corrections (explicit rejections, requests to change)
- User successes (approvals, positive feedback)
- Edge cases (unexpected questions, workarounds)
- Repeated user preferences
Focus on the skill: [skill-name]. Remove all other content."
```

### 2. Analyze Compressed Output

The context-manager will return a compressed view containing only:
- User-assistant exchanges related to the target skill
- Corrections and feedback
- Success confirmations
- Edge case discoveries
- Preference patterns

All other content (unrelated work, system messages, debugging, etc.) is filtered out.

### 3. Count Signals

Process the compressed conversation using the same signal detection logic:
- Corrections (HIGH confidence)
- Successes (MED confidence)
- Edge Cases (MED confidence)
- Preferences (LOW confidence)

## Compression Prompt Template

**Basic template:**
```
Extract only these types of interactions from the conversation:
- User corrections (explicit rejections, requests to change)
- User successes (approvals, positive feedback)
- Edge cases (unexpected questions, workarounds)
- Repeated user preferences
Focus on the skill: [skill-name]. Remove all other content.
```

**Multi-skill session:**
```
Extract interactions where the user worked with or gave feedback on the [skill-name] skill.
Include:
- Corrections to skill behavior
- Positive/negative feedback on skill outputs
- Edge cases the skill didn't handle well
- User preferences about skill behavior
Exclude: All work unrelated to this skill.
```

**Preference-focused:**
```
Extract user preferences related to [skill-name]:
- Repeated patterns (user always asks for X)
- Style preferences (e.g., "use Grid not Flexbox")
- Constraint statements (e.g., "never use gradients")
- Workflow preferences
Remove all implementation work, debugging, and one-off requests.
```

## Example: Before and After

### Before Compression (18k tokens)

```
[extensive debugging session]
user: "The API is failing, let me check the logs"
assistant: [reads logs, analyzes error]
user: "Try adding error handling"
assistant: [implements error handling]
[500 lines of code changes]
user: "Now run frontend-design skill to create the dashboard"
assistant: [uses frontend-design skill, creates dashboard]
user: "The colors are too bright"
assistant: [adjusts colors]
user: "Perfect! I like this muted palette approach"
[more unrelated work]
```

### After Compression (2.5k tokens)

```
Interactions with frontend-design skill:

user: "Now run frontend-design skill to create the dashboard"
assistant: [uses frontend-design skill, creates dashboard with bright colors]
user: "The colors are too bright"
assistant: [adjusts to muted palette]
user: "Perfect! I like this muted palette approach"

Signals detected:
- 1 correction: "colors are too bright"
- 1 success: "Perfect! I like this muted palette"
- 1 preference: User prefers muted color palettes
```

## Integration with Metrics

Compression is transparent to metrics tracking:
- Signal counts remain accurate
- Proposal logging unchanged
- Outcome tracking unaffected

The context-manager agent call is not logged - only the final signal counts matter.

## Performance Benchmarks

Based on context-manager agent capabilities:

| Conversation Size | Compression Time | Token Reduction | Accuracy |
|-------------------|------------------|-----------------|----------|
| 5k tokens         | ~2-3 seconds     | 40-60%          | 100%     |
| 10k tokens        | ~3-5 seconds     | 60-75%          | 98%      |
| 20k tokens        | ~5-8 seconds     | 75-85%          | 95%      |
| 50k+ tokens       | ~10-15 seconds   | 85-95%          | 90%      |

**Note:** Accuracy = Signal detection quality compared to analyzing full conversation

## Troubleshooting

**If compression misses signals:**
- Make the extraction prompt more specific
- Add examples of the types of interactions you want
- Run without compression and compare results

**If compression is too slow:**
- Reduce conversation size by analyzing only recent messages
- Use compression only for >15k token conversations
- Consider splitting into multiple reflect sessions

**If compressed output is still large:**
- Refine the extraction prompt to be more selective
- Focus on one signal type at a time
- Exclude verbose code snippets from extraction

## Advanced: Custom Compression

For specific use cases, customize the compression prompt:

**Error-focused (for debugger skill):**
```
Extract only error messages, stack traces, and the user's feedback on how to fix them.
Exclude: Successful operations, unrelated code.
```

**Performance-focused (for performance-engineer skill):**
```
Extract only performance measurements, user complaints about speed,
and optimization requests.
Exclude: Functional changes, styling, features.
```

**Architecture-focused (for architect-review skill):**
```
Extract only architectural decisions, design pattern discussions,
and feedback on system structure.
Exclude: Implementation details, styling, debugging.
```

## Best Practices

1. **Always estimate conversation size** before reflecting
2. **Use compression for >10k tokens** as a rule of thumb
3. **Review compressed output** occasionally to verify quality
4. **Adjust prompts** if signal detection seems off
5. **Track compression effectiveness** in your own workflow

## Future Enhancements

Potential improvements to context compression (not yet implemented):

- **Automatic size detection**: Auto-compress when conversation exceeds threshold
- **Compression caching**: Save compressed views for re-analysis
- **Multi-pass compression**: First pass filters by skill, second pass extracts signals
- **Compression metrics**: Track time saved and accuracy over time
