# Response Format System

**Absolute minimum - only what's functionally necessary.**

---

## Format

```
📋 SUMMARY: [One sentence - stored in work items]

[Your response]
```

---

## What's Parsed

| Field | Hook | Storage |
|-------|------|---------|
| 📋 SUMMARY | `capture.ts` | `MEMORY/WORK/*/items/*.yaml` → `response_summary` |

---

## What Was Removed (Not Parsed)

- ~~Voice line~~ - Was for TTS/notifications (removed per user request)
- ~~📁 CAPTURE~~ - `isLearningCapture()` uses keyword detection, not this field
- ~~📖 STORY EXPLANATION~~ - Not parsed
- ~~⭐ RATE~~ - Rating hooks parse user messages, not AI output
- ~~🔍 ANALYSIS~~ - Only written to learning files if one is created
- ~~⚡ ACTIONS~~ - Only written to learning files if one is created
- ~~✅ RESULTS~~ - Only written to learning files if one is created
- ~~📊 STATUS~~ - Only checked for error keywords
- ~~➡️ NEXT~~ - Only written to learning files if one is created

---

## Example

```
📋 SUMMARY: Fixed authentication bug in login handler

Found missing null check on token validation. Added check before token use.
Updated unit tests. All 47 tests now passing. Ready for deployment.
```

---

**For user-specific customizations, see:** `USER/RESPONSEFORMAT.md`
