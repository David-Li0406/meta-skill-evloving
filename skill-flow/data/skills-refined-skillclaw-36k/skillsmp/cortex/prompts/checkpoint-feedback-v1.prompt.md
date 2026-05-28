# Checkpoint Feedback Prompt v1

## Purpose

Analyze **user messages** in a turn segment to detect quality signals about the prior response.
We want to know if the user accepted the response, corrected it, or expressed frustration.

## Input

- A turn segment containing one or more **User** messages (and possibly Assistant text)

## Task

For each user message, extract:

1. sentiment: positive / neutral / negative
2. correction: did the user correct the assistant?
3. frustration: did the user express annoyance?
4. praise: explicit positive feedback?
5. confusion: did the user seem confused?
6. acceptance: did the user accept/confirm the result?
7. evidence: 1–2 short quotes supporting labels

Also compute aggregates:
- positive_streak, negative_streak
- correction_count, frustration_count, praise_count
- quality_score (0–1) and quality_band (good/neutral/bad)

## Output Format (JSON)

```json
{
  "feedback": [
    {
      "message_index": 1,
      "sentiment": "positive",
      "correction": false,
      "frustration": false,
      "praise": true,
      "confusion": false,
      "acceptance": true,
      "evidence": ["Perfect, thanks."]
    }
  ],
  "aggregate": {
    "positive_streak": 2,
    "negative_streak": 0,
    "correction_count": 0,
    "frustration_count": 0,
    "praise_count": 1,
    "quality_score": 0.92,
    "quality_band": "good"
  }
}
```

## Rules

- Output **valid JSON only**
- Be conservative: only flag correction/frustration when clearly present
- Evidence quotes must be exact snippets from user messages
- Always include **all fields** shown in the output format (no omissions)
- If a field is unknown, still include it with a sensible default:
  - sentiment: "neutral"
  - correction/frustration/praise/confusion/acceptance: false
  - evidence: []
- Always include the aggregate block (even if all counts are zero)

---

## Feedback Input

{{{segment_text}}}
