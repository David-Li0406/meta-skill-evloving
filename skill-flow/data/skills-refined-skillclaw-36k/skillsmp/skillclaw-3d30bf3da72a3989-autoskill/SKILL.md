---
name: autoskill
description: Use this skill when the user asks to "learn from this session", "update skills", or "remember this pattern". It analyzes coding sessions to detect corrections and preferences, proposing targeted improvements to the Skills used during the session.
---

# Skill body

This skill analyzes coding sessions to extract durable preferences from corrections and approvals, then proposes targeted updates to Skills that were active during the session. It acts as a learning mechanism across sessions, ensuring the system improves based on feedback.

## When to activate

Trigger on explicit requests:
- "autoskill", "learn from this session", "update skills from these corrections"
- "remember this pattern", "make sure you do X next time"

Do NOT activate for one-off corrections or when the user declines skill modifications.

## Signal detection

Scan the session for:

**Corrections** (highest value)
- "No, use X instead of Y"
- "We always do it this way"
- "Don't do X in this codebase"

**Repeated patterns** (high value)
- Same feedback given 2+ times
- Consistent naming/structure choices across multiple files

**Approvals** (supporting evidence)
- "Yes, that's right"
- "Perfect, keep doing it this way"

**Ignore:**
- Context-specific one-offs ("use X here" without "always")
- Ambiguous feedback
- Contradictory signals (ask for clarification instead)

## Signal quality filter

Before proposing any change, ask:
1. Was this correction repeated, or stated as a general rule?
2. Would this apply to future sessions, or just this task?
3. Is it specific enough to be actionable?
4. Is this **new information** I wouldn't already know?

Only propose changes that pass all four.

### What counts as "new information"

**Worth capturing:**
- Project-specific conventions ("we use `cn()` not `clsx()` here")
- Custom component/utility locations ("buttons are in `@/components/ui`")
- Team preferences that differ from defaults ("we prefer explicit returns")
- Domain-specific terminology or patterns
- Non-obvious architectural decisions ("auth logic lives in middleware, not components")
- Integrations and API quirks specific to this stack

**NOT worth capturing:**
- Context-specific one-offs without broader applicability
- Feedback that contradicts established patterns without clarification

## Session scope

By default, analyze only the **current session** (from SessionStart to now). This ensures fresh, relevant feedback without noise from old sessions.

To analyze patterns across multiple sessions, the user must explicitly request: "analyze my last 5 sessions" or "look for patterns across this week".

## Where to apply changes

Distinguish between skill-specific behavior and project-wide conventions:

**Update Skills when:**
- Signal relates to how a specific skill should behave
- Preference affects skill trigger conditions or outputs
- Pattern is about the skill's decision-making process

**Update project documentation when:**
- Project-wide conventions (naming, file structure, architecture)
- Tool/library preferences that span multiple skills
- Team style preferences (spacing, comments, error handling)
- Domain-specific terminology used across the codebase