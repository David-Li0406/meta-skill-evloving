---
name: conversation-analysis
description: Use this skill when analyzing conversation patterns, identifying frustration or success signals, or when "analyze conversation", "what went wrong", or "patterns" are mentioned.
---

# Skill body

Signal extraction → pattern detection → behavioral insights.

## When to Use

- User requests conversation analysis
- Identifying frustration, success, or workflow patterns
- Extracting user preferences and requirements
- Understanding task evolution and iterations

**NOT for:** real-time monitoring, content generation, single message analysis

## Signal Taxonomy

| Type       | Subtype         | Indicators                                           |
|------------|------------------|-----------------------------------------------------|
| Success    | Explicit Praise   | "Perfect!", "Exactly what I needed", exclamation marks |
| Success    | Continuation      | "Now do the same for...", building on prior work    |
| Success    | Adoption          | User implements suggestion without modification      |
| Success    | Acceptance        | "Looks good", "Ship it", "Merge this"              |
| Frustration| Correction        | "No, I meant...", "That's wrong", "Do X instead"   |
| Frustration| Reversion         | User undoes agent changes, "Go back"                |
| Frustration| Repetition        | Same request 2+ times, escalating specificity       |
| Frustration| Explicit          | "This isn't working", "Why did you...", accusatory tone |
| Workflow   | Sequence          | "First...", "Then...", "Finally...", numbered lists |
| Workflow   | Transition        | "Now that X is done, let's Y", phase changes       |
| Workflow   | Tool Chain        | Recurring tool usage patterns (Read → Edit → Bash) |
| Workflow   | Context Switch    | Abrupt topic changes, no transition language        |
| Request    | Prohibition       | "Don't use X", "Never do Y", "Avoid Z"            |
| Request    | Requirement       | "Always check...", "Make sure to...", "You must..."|
| Request    | Preference        | "I prefer...", "It's better to...", comparative language |
| Request    | Conditional       | "If X then Y", "When A, do B", situational rules   |

## Confidence Levels

- **High (0.8–1.0):** Explicit keywords match taxonomy, no ambiguity, strong context
- **Medium (0.5–0.79):** Implicit signal, partial context, minor ambiguity
- **Low (0.2–0.49):** Ambiguous language, weak context, borderline classification

## Phases

Track with **maintain-tasks** skill for phase tracking. Phases advance only, never regress.

| Phase            | Trigger          | activeForm          |
|------------------|------------------|---------------------|
| Parse Input      | Session start     | "Parsing input"     |
| Extract Signals  | Scope validated    | "Extracting signals"|
| Detect Patterns   | Signals extracted  | "Detecting patterns"|