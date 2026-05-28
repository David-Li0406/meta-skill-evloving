---
name: log-error
description: Use when something goes wrong during agentic coding - hallucination, bug, ignored instruction, anti-pattern, context loss, or Claude getting stuck in a loop.
---

# Log Error

Log agentic coding failures to identify **USER mistakes** in prompting, context management, or harness configuration.

**Core principle:** The model is constant. The user's input is the variable. Focus on the variable.

## Error Categories

| Category | Symptoms |
|----------|----------|
| **Prompt Error** | Ambiguous, missing constraints, too verbose, implicit expectations |
| **Context Error** | Context rot, stale/missing context, didn't /clear |
| **Harness Error** | Wrong agent type, subagent context loss, no guardrails |
| **Meta Error** | Rushed implementation, assumed competence, skipped planning |

## Interview Process

Ask 5-8 **specific** questions about what happened:

- "Your prompt was X words. What were the 3 most important requirements?"
- "Did you specify what NOT to do?"
- "When did you last /clear? How full was context?"
- "What constraints were in your head but not in the prompt?"
- "Was this reference material or explicit requirements?"

**Be critical** - user is logging to learn, not to feel good.

## Required Captures

1. **Triggering prompt** - exact, verbatim
2. **Primary error category** - pick ONE
3. **The gap** - expected vs actual outcome
4. **Prevention** - specific action items for next time
5. **Pattern check** - seen this before? (habit to break)

## Logging

- **Directory:** `~/agents/logs/errors/`
- **Format:** `error-YYYY-MM-DD-NNN.md`
- **Template:** See `template.md` in this skill directory

After logging, user can double-escape to rewind conversation and continue working.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Generic questions | Ask about what ACTUALLY happened |
| Blaming model | Focus 80% on user error |
| Sanitizing logs | Be specific and honest |
| Vague prevention | Give actionable items |
