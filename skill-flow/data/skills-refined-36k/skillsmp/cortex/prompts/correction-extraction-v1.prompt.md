# Correction Extraction Prompt v1

## Purpose

Extract instances where the user corrects AI assistant behavior. These corrections reveal how the user wants tasks done and become learning signals for future interactions.

## Input

- **Channel**: The AI platform (cursor, claude-code, codex, nexus, etc.)
- **Session Name**: The name/title of the AI session (for agent attribution)
- **User**: The owner of the cortex database
- **Messages**: An AI conversation session

## Task

Identify and extract ALL corrections, including:

1. **Direct corrections** — "No, do X instead", "That's wrong, it should be Y"
2. **Behavioral guidance** — "Don't do that", "Always do X when Y"
3. **Preference assertions** — "I prefer X", "Use Y format"
4. **Frustration signals** — "That's not what I asked", "You keep doing X"
5. **Clarifications that correct** — "What I meant was...", "To be clear, I want..."
6. **Implicit corrections** — User redoes something the AI did wrong

### Correction Categories

| Category | Examples |
|----------|----------|
| **output_format** | How to format responses, code style, structure |
| **task_approach** | How to approach problems, workflow, methodology |
| **content** | What to include/exclude, level of detail |
| **communication** | Tone, verbosity, explanation style |
| **tools** | Which tools to use/avoid, how to use them |
| **domain** | Domain-specific corrections (codebase, terminology) |

---

## Output Format

```json
{
  "extraction_metadata": {
    "channel": "cursor",
    "session_name": "nexus-cli-development",
    "user_name": "Tyler Brandt",
    "message_count": 80,
    "date_range": {
      "start": "2024-01-15T10:00:00Z",
      "end": "2024-01-15T14:30:00Z"
    }
  },
  "corrections": [
    {
      "category": "output_format",
      "what_was_wrong": "Assistant used paragraphs for summary",
      "correction": "Use bullet points, not paragraphs",
      "generalized_rule": "When summarizing, use bullet points instead of paragraphs",
      "memory_entry": "output_format: When summarizing, use bullet points instead of paragraphs",
      "evidence": "No, use bullet points instead. I don't want to read paragraphs.",
      "confidence": "high",
      "correction_type": "direct",
      "scope_hint": "user_general"
    },
    {
      "category": "task_approach",
      "what_was_wrong": "Assistant started implementing without confirming plan",
      "correction": "Show plan before implementing",
      "generalized_rule": "Before making changes, show the plan and get confirmation",
      "memory_entry": "task_approach: Before making changes, show the plan and get confirmation",
      "evidence": "Wait, hold on. Show me what you're going to do first.",
      "confidence": "high",
      "correction_type": "direct",
      "scope_hint": "user_general"
    },
    {
      "category": "tools",
      "what_was_wrong": "Assistant used rm to delete files",
      "correction": "Use trash instead of rm",
      "generalized_rule": "Use 'trash' command instead of 'rm' for file deletion",
      "memory_entry": "tools: Use 'trash' instead of 'rm' for file deletion",
      "evidence": "Don't use rm! Use trash so I can recover it.",
      "confidence": "high",
      "correction_type": "direct",
      "scope_hint": "workspace_specific"
    },
    {
      "category": "domain",
      "what_was_wrong": "Assistant misunderstood project structure",
      "correction": "Skills live in skills/, not plugins/",
      "generalized_rule": "In nexus, skill definitions are in skills/ directory",
      "memory_entry": "domain: In nexus, skill definitions are in skills/ directory",
      "evidence": "No, skills go in skills/, not plugins/. Look at the existing structure.",
      "confidence": "high",
      "correction_type": "clarification",
      "scope_hint": "workspace_specific"
    }
  ],
  "frustration_signals": [
    {
      "trigger": "Assistant kept making same mistake",
      "evidence": "You keep doing this. I've told you three times now.",
      "implied_rule": "Pay attention to previous corrections in the conversation"
    }
  ]
}
```

---

## Important Rules

1. **Focus on actionable corrections** — Things that can become rules for future behavior
2. **Include memory_entry** — A compact sentence suitable for MEMORY.md (prefix with category)
3. **Generalize when possible** — Turn specific corrections into general rules
4. **Quote exact evidence** — Include the user's actual words
5. **Track frustration** — Repeated corrections or frustration signals indicate high-priority learnings
6. **Confidence levels**:
   - **high**: Direct, explicit correction
   - **medium**: Clarification or implicit correction
   - **low**: Single subtle signal
7. **Correction types**:
   - `direct`: User explicitly says what's wrong and how to fix
   - `clarification`: User clarifies intent, implying previous understanding was wrong
   - `redo`: User redoes what assistant did, showing correct approach
   - `frustration`: User expresses frustration about repeated issue
8. **Context matters** — Note if correction is likely session-specific vs general
9. **Don't over-generalize** — Some corrections are one-off, not rules

---

## Scope Hints

Include a `scope_hint` for each correction to help with later categorization:

- `"agent_specific"`: This correction is specific to this type of task/session
- `"user_general"`: This is a general user preference
- `"workspace_specific"`: This is specific to this codebase/workspace

---

## Conversation
{{{segment_text}}}
