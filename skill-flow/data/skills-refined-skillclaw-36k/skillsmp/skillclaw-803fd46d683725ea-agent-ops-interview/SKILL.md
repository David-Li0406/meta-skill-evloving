---
name: agent-ops-interview
description: Use this skill when you need to conduct structured interviews with users, asking one question at a time to gather their decisions and preferences.
---

# Interview workflow

## Purpose

Gather user decisions, preferences, or clarifications through a structured one-question-at-a-time process. This prevents overwhelming the user and ensures each answer is properly understood before moving on.

## Rules (strict)

1. **One question per message.** Never batch multiple questions.
2. **Present clear options.** Each question should have labeled options (A, B, C) or a clear format for the expected answer.
3. **Explain briefly.** Give just enough context for the user to decide—not a wall of text.
4. **Record immediately.** After each answer, note it in `.agent/focus.md` or a working document before asking the next question.
5. **Allow escape.** User can say "skip", "defer", "use your recommendation", or "stop interview".
6. **Summarize at end.** When all questions are answered, present a summary for confirmation.

## Interview state tracking

Track in `.agent/focus.md` under "Doing now":

```markdown
## Doing now

Interview: [topic]
- Q1: [question summary] → [answer or pending]
- Q2: [question summary] → [answer or pending]
- ...
```

## Procedure

1. **Setup**: List all questions internally (do not show to user yet).
2. **Ask Q1**: Present one question with options.
3. **Wait**: Do not proceed until user responds.
4. **Record**: Update focus.md with the answer.
5. **Ask Q2**: Repeat until all questions answered or user stops.
6. **Summarize**: Present all answers for confirmation.
7. **Proceed**: Use confirmed answers to continue the workflow.

## Handling special responses

| User says | Action |
|-----------|--------|
| "skip" | Mark as SKIPPED, move to next question |
| "defer" | Mark as DEFERRED, move to next question |
| "use your recommendation" | Apply the agent's recommended default, note it |
| "stop" / "pause" | End interview, save progress, can resume later |
| "go back" | Re-ask the previous question |
| unclear answer | Ask a brief clarifying follow-up (still counts as same question) |

## Question Quality Standards

### Good Questions

- **Specific to context** — Ensure questions are relevant to the user's situation and needs.