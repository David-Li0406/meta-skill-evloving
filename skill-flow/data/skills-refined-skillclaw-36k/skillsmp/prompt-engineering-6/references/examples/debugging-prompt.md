# Example: Debugging a Failing Prompt

How to diagnose and fix prompt issues.

## Scenario

Prompt produces inconsistent, verbose summaries.

## Original Prompt (Failing)

```
Summarize this article and make it good.
```

## Diagnosis

| Symptom | Root Cause |
|---------|------------|
| Output varies wildly in length | No length specification |
| Sometimes bullets, sometimes prose | No format defined |
| Misses key points | No priority guidance |
| "Good" is subjective | Vague quality criteria |

## Fixed Prompt

```xml
<task>
Summarize this article in exactly 3 bullet points.
</task>

<format>
Each bullet must:
- Start with strong action verb
- Be 15-25 words (not shorter, not longer)
- Cover one distinct insight (no overlap)
</format>

<priority>
Order bullets by importance:
1. Main finding or announcement
2. Key supporting evidence
3. Implication or next steps
</priority>

<constraints>
- No quotes from article
- No hedging ("might", "could", "seems")
- No meta-commentary ("This article discusses...")
</constraints>
```

## Changes Made

| Issue | Fix Applied |
|-------|-------------|
| No length | "exactly 3 bullet points" |
| Vague "good" | Specific criteria (verb, word count) |
| No format | Explicit structure with priorities |
| No focus | Priority order defined |
| Unpredictable | Added constraints for consistency |

## Debugging Checklist

When a prompt fails, check:

1. **Format specified?** → Add explicit structure
2. **Length bounded?** → Add word/bullet count
3. **Priorities clear?** → Define what matters most
4. **Constraints stated?** → Say what NOT to do
5. **Examples needed?** → Add few-shot if pattern-based
6. **Reasoning required?** → Add CoT structure
