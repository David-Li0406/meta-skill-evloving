---
name: "compact"
description: "Produces compact, high-signal output. Invoke when user asks for concise answers, quick status, or a short action checklist."
---

# Compact

## Purpose

Reduce verbosity while keeping correctness and key technical details.

## When to Invoke

- The user says: “Use skill `compact`”, “be concise”, “short answer”, “TL;DR”.
- You need to provide a fast status update with minimal prose.
- You’re outputting results that are mostly procedural (commands, checklist, verification steps).

## Output Rules

- Prefer 3–7 bullets total.
- Avoid background explanations unless asked.
- Include only:
  - What changed / what works
  - Where to look (file links) if relevant
  - What to do next (1–3 steps) if relevant
- No filler acknowledgements.

## Templates

### Status

- Done: <1–3 items>
- Verified: <commands/tests>
- Next: <1–3 steps>

### Change Summary

- Files: <key files>
- Behavior: <what user sees>
- Notes: <1–2 risks/limits>
