# Proposal Formatting Templates

This document provides templates and formatting guidelines for presenting reflect proposals to users.

## Basic Format

```
┌─ Skill Reflection: [skill-name] ───────────────────┐
│                                                    │
│ Signals: X corrections, Y successes                │
│                                                    │
│ Proposed changes:                                  │
│                                                    │
│ [emoji] [LEVEL] [action]: "[description]"          │
│                                                    │
│ Commit: "[skill]: [summary]"                       │
│                                                    │
└────────────────────────────────────────────────────┘

Apply these changes? [Y/n] or describe tweaks
```

## Simplified Format (Recommended)

Use this more concise format to reduce tokens:

```
Skill Reflection: [skill-name]

Signals: X corrections, Y successes

Proposed changes:
🔴 HIGH: [action] - "[description]"
🟡 MED:  [action] - "[description]"
🔵 LOW:  [action] - "[description]"

Commit: "[skill]: [summary]"

Apply? [Y/n] or describe tweaks
```

## Confidence Levels & Emojis

| Level | Emoji | ANSI Code | Color | Use When |
|-------|-------|-----------|-------|----------|
| HIGH  | 🔴    | `\033[1;31m` | Bold Red #FF6B6B | User explicitly corrected (direct evidence) |
| MED   | 🟡    | `\033[1;33m` | Bold Yellow #FFE066 | Strong pattern observed (good evidence) |
| LOW   | 🔵    | `\033[1;36m` | Bold Cyan #6BC5FF | Weak signal or uncertain (accumulate over time) |

**Reset color**: `\033[0m`

### ANSI Code Usage

```bash
echo -e "\033[1;31mHIGH\033[0m: Add constraint"  # Red
echo -e "\033[1;33mMED\033[0m: Add preference"   # Yellow
echo -e "\033[1;36mLOW\033[0m: Note for review"  # Cyan
```

## Action Types

| Action | When to Use | Example |
|--------|-------------|---------|
| **Add constraint** | User explicitly said "never do X" | Add to NEVER section: "Don't use gradients" |
| **Add preference** | User consistently prefers X over Y | Add to PREFER section: "Use CSS Grid for layouts" |
| **Update guideline** | Existing guideline needs refinement | Change "use dark colors" to "use #000 for dark backgrounds" |
| **Remove outdated** | Guideline no longer applies | Remove "prefer class components" (React Hooks now standard) |
| **Add edge case** | Scenario skill didn't handle | Add to EDGE CASES: "Handle keyboard navigation" |
| **Clarify ambiguity** | Existing text unclear | Change "be accessible" to "ensure WCAG AA 4.5:1 contrast" |

## Confidence Level Guidelines

### When to use HIGH (🔴):
- User said "no, don't do that"
- User explicitly corrected output
- User stated clear constraint: "Never use..."
- Direct evidence of wrong approach

**Example**:
```
🔴 HIGH: Add constraint - "Never use gradients unless explicitly requested"
```

### When to use MED (🟡):
- User approved but suggested improvement
- Pattern observed in 2+ instances
- User expressed preference: "I prefer..."
- Good evidence but not absolute

**Example**:
```
🟡 MED: Add preference - "Prefer CSS Grid over Flexbox for card layouts"
```

### When to use LOW (🔵):
- Single observation, not yet pattern
- Uncertain interpretation
- Edge case that might be one-off
- Needs more sessions to confirm

**Example**:
```
🔵 LOW: Note for review - "User may prefer darker color palette"
```

## Commit Message Format

```
[skill-name]: [concise summary]
```

**Examples:**
- `frontend-design: no gradients, use #000 for dark backgrounds`
- `code-reviewer: add Python type hint checking`
- `api-client: handle connection timeout edge case`

**Guidelines:**
- Keep under 72 characters
- Use imperative mood ("add", not "added")
- Focus on "what" not "why" (details in skill file itself)
- Comma-separate multiple changes

## Full Example

```
Skill Reflection: frontend-design

Signals: 2 corrections, 3 successes

Proposed changes:
🔴 HIGH: Add constraint - "Never use gradients unless explicitly requested"
🔴 HIGH: Update guideline - "Dark backgrounds must use #000, not #1a1a1a"
🟡 MED: Add preference - "Prefer CSS Grid over Flexbox for card layouts"

Commit: "frontend-design: no gradients, #000 dark, prefer Grid"

Apply? [Y/n] or describe tweaks
```

## Accessibility Notes

- All colors meet WCAG AA 4.5:1 contrast ratio on dark backgrounds
- Emojis supplement color (not replace) for colorblind users
- Avoid green/red combinations
- Use bold for emphasis, not just color

## Token Optimization Tips

1. **Use simplified format** (not boxed format) - saves ~50 tokens
2. **Omit ANSI codes** in low-token environments - emojis sufficient
3. **Abbreviate when listing many changes** - "Add 3 constraints" instead of listing each
4. **Reference this file** instead of including guidelines in every proposal
