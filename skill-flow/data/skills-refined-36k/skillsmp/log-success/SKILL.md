---
name: log-success
description: Use when something works unusually well during agentic coding - fast completion, first-try success, elegant solution, minimal intervention needed, or new technique paid off.
---

# Log Success

Log agentic coding wins to understand **WHY things worked** and build repeatable patterns.

**Core principle:** Success patterns are as valuable as failure patterns. Capture what went RIGHT before you forget.

## Success Categories

| Category | Indicators |
|----------|------------|
| **Prompt Excellence** | Clear constraints, right abstraction, good structure |
| **Context Management** | Fresh context, lean CLAUDE.md, just-in-time info |
| **Harness Configuration** | Right agent type, effective parallelization, good validation |
| **Technique Applied** | New tip worked, pattern reuse, good tool usage |

## Interview Process

Ask 4-6 **specific** questions about what happened:

- "What about the prompt setup made it work so smoothly?"
- "What context did you provide upfront that prevented back-and-forth?"
- "Did you /clear recently? How much context was in the window?"
- "Was there something different about how you structured this?"
- "Could you do this again with the same approach?"
- "Is this worth adding to CLAUDE.md?"

## Required Captures

1. **Triggering prompt** - exact, verbatim
2. **Primary success category** - pick ONE
3. **Key ingredient** - the ONE thing that made the difference
4. **Reproducibility** - can this become standard practice?
5. **One-line lesson** - actionable insight to apply again

## Logging

- **Directory:** `~/agents/logs/successes/`
- **Format:** `success-YYYY-MM-DD-NNN.md`
- **Template:** See `template.md` in this skill directory

Consider adding successful patterns to CLAUDE.md if broadly applicable.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague logs | Be specific about what worked |
| Credit only Claude | Focus on what USER did right |
| Skip the prompt | Capture exact prompt for reference |
| Forget reproducibility | Ask if pattern should become standard |
