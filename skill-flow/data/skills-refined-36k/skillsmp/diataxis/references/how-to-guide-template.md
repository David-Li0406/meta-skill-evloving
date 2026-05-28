# How-to Guide Template

**Purpose**: Solve a specific, real-world problem. User is competent and wants to get work done.

**Key Characteristics**:
- Addresses a specific goal or problem
- Assumes competence (links to Tutorials if needed)
- Action-focused, no digression
- Practical and adaptable to variations
- Omits unnecessary details

## Structure

```markdown
# How to [Achieve specific outcome]

This guide shows you how to [outcome] when [situation/context].

## When to use this guide

[Who should use this and what problem it solves]

Example: "Use this if you need to migrate your database to a new server 
while minimizing downtime."

## Before you start

[Minimal prerequisites]
- [Access or permission]
- [Tool or service]
- [Basic knowledge]

## Context

[Brief explanation of why this matters, if helpful. Keep it short.]

## Steps

### [Subtask 1: Clear verb]

[Practical directions addressing the user's goal]

```
[Command or action]
```

### [Subtask 2: Clear verb]

[Continue with next subtask]

## Troubleshooting

**Problem: [Common issue]**
Solution: [How to fix it]

**Problem: [Another issue]**
Solution: [How to fix it]

## Variations

If you need to [alternative goal], instead do X instead of Y at step 2.

## Related guides

- [How-to Guide] for similar task
- [How-to Guide] for related task
- [Reference] for complete options

## See also

- [Explanation] for "why this approach"
- [Tutorial] for learning this skill from scratch
```

## Language Patterns

Use these patterns consistently throughout your how-to guide:

| Pattern | Example |
|---------|---------|
| **This guide shows you how to…** | "This guide shows you how to configure single sign-on with OAuth2." |
| **If you want X, do Y** | "If you want to run tests in parallel, add the `--workers=4` flag." |
| **To achieve W, follow these steps** | "To minimize downtime, follow these steps:" |
| **When you encounter [situation]** | "When you encounter a timeout, increase the connection timeout to 30s." |
| **Refer to the X reference for full options** | "Refer to the configuration reference for all available settings." |

## Key Principles to Remember

✓ **Address real-world complexity** — Handle common variations and edge cases

✓ **Omit the unnecessary** — Practical usability over completeness

✓ **Assume competence** — Link to tutorials for foundational skills

✓ **Provide executable instructions** — Every step works; it's a contract

✓ **Describe a logical sequence** — Steps flow in a natural, thinking-driven order

✓ **Seek flow** — Minimize context switching; guide user thinking

✓ **Pay attention to naming** — Title must say exactly what the guide shows

## Example

See [examples.md](examples.md#example-2-how-to-guide) for a complete working example: "How to migrate a PostgreSQL database with zero downtime"
