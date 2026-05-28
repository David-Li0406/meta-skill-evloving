---
name: gemini
description: Interact with Google's Gemini model via CLI. Use when needing a second opinion from another LLM, cross-validation, or leveraging Gemini's Google Search grounding. Supports multi-turn conversations with session management.
---

# Gemini CLI

## Commands

### New conversation (ask)

```bash
gemini "your prompt here" --output-format json 2>/dev/null
```

Response includes `session_id` for follow-up:
```json
{
  "session_id": "uuid-here",
  "response": "...",
  "stats": {...}
}
```

### Continue conversation (reply)

```bash
gemini --resume <session_id> -p "follow-up prompt" --output-format json 2>/dev/null
```

Context from previous turns is preserved.

## Examples

```bash
# Ask Gemini for code review
gemini "Review this function for potential bugs: $(cat src/utils.ts)" --output-format json 2>/dev/null | jq '{session_id, response}'

# Follow up on the same session
gemini --resume abc123-def456 -p "How would you refactor it?" --output-format json 2>/dev/null | jq '{session_id, response}'

# Leverage Google Search grounding
gemini "What are the latest changes in TypeScript 5.8?" --output-format json 2>/dev/null | jq '{session_id, response}'
```

## Notes

- Parse `session_id` from JSON response to enable reply
- Gemini automatically uses `google_web_search` when needed
- Image analysis: include file path in prompt, Gemini reads via `read_file`
