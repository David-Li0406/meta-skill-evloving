# Self-Preference Extraction Prompt v1

## Purpose

Extract the user's personal preferences from a conversation. These are statements about how the user likes things done, what they prefer, what they dislike, and their working style.

## Input

- **Channel**: The communication channel (iMessage, Gmail, Cursor, etc.)
- **User**: The owner of the cortex database (the person whose preferences we're extracting)
- **Messages**: A conversation chunk

## Task

Extract ALL preferences expressed by or about the user. Look for:

1. **Explicit preferences** — "I prefer...", "I like...", "I want..."
2. **Explicit dislikes** — "I hate...", "Don't...", "I don't like..."
3. **Corrections that reveal preferences** — "No, do it this way", "Actually, I'd rather..."
4. **Demonstrated patterns** — Consistent behaviors that indicate preference
5. **Style indicators** — How the user communicates, formats, responds

### Preference Categories

| Category | Examples |
|----------|----------|
| **formatting** | Bullet points vs paragraphs, markdown style, code style |
| **communication** | Tone (casual/formal), directness, level of detail |
| **workflow** | How they like to work, tools they prefer, processes |
| **feedback** | How they want to receive feedback, criticism style |
| **scheduling** | Time preferences, response timing, availability |
| **content** | Topics they engage with, things they avoid |

---

## Output Format

```json
{
  "extraction_metadata": {
    "channel": "cursor",
    "user_name": "Tyler Brandt",
    "message_count": 50,
    "date_range": {
      "start": "2024-01-01T00:00:00Z",
      "end": "2024-01-15T23:59:59Z"
    }
  },
  "preferences": [
    {
      "category": "formatting",
      "preference": "Prefers bullet points over paragraphs for summaries",
      "memory_entry": "formatting: Prefers bullet points over paragraphs for summaries",
      "evidence": "No, use bullet points instead",
      "confidence": "high",
      "source_type": "explicit_correction"
    },
    {
      "category": "communication",
      "preference": "Wants direct feedback without softening",
      "memory_entry": "communication: Wants direct feedback without softening",
      "evidence": "Just tell me straight, I don't need the fluff",
      "confidence": "high",
      "source_type": "explicit_statement"
    },
    {
      "category": "workflow",
      "preference": "Prefers to see the plan before implementation",
      "memory_entry": "workflow: Prefers to see the plan before implementation",
      "evidence": "Wait, let me see what you're going to do first",
      "confidence": "medium",
      "source_type": "demonstrated_pattern"
    }
  ]
}
```

---

## Important Rules

1. **Only extract USER's preferences** — Not preferences of other participants
2. **Include memory_entry** — A compact sentence suitable for MEMORY.md (prefix with category)
3. **Quote exact evidence** — Include the message text that supports the preference
4. **Be specific** — "prefers bullet points" is better than "prefers organized output"
5. **Confidence levels**:
   - **high**: Explicitly stated or directly corrected
   - **medium**: Strongly implied or demonstrated multiple times
   - **low**: Inferred from single instance
6. **Source types**:
   - `explicit_statement`: User directly states preference
   - `explicit_correction`: User corrects someone/something to their preference
   - `explicit_dislike`: User states what they don't want
   - `demonstrated_pattern`: Consistent behavior across messages
   - `inferred`: Single instance suggesting preference
7. **Don't over-extract** — Only include clear preferences, not every opinion
8. **Don't hallucinate** — Only extract what's actually in the messages

---

## Conversation
{{{segment_text}}}
