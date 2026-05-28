---
name: clean-code-reviewer
description: Review code for Clean Code principles focusing on meaningful variable names, function length, and redundant comments. Use when the user requests code review with /review-code command, asks to check code quality, or wants to ensure code follows Clean Code principles. Supports JavaScript, Python, and Java with language-specific rules.
---

# Clean Code Reviewer

Review code for adherence to Clean Code principles with focus on practical improvements.

## Quick Start

When triggered by `/review-code`, analyze the current file or provided code and generate a concise report identifying Clean Code violations.

## Review Process

Follow this workflow:

1. **Identify the language** - Determine the programming language to apply appropriate rules
2. **Check variable naming** - Flag unclear, abbreviated, or misleading names
3. **Assess function length** - Identify functions exceeding recommended limits
4. **Evaluate comments** - Find redundant comments that repeat what code already says
5. **Generate report** - List issues in a concise format

## Variable Naming Review

Check for:
- Single letter names (except loop counters i, j, k)
- Unclear abbreviations (e.g., `d`, `tmp`, `val`)
- Non-descriptive names (e.g., `data`, `info`, `obj`)
- Names that don't reveal intent (e.g., `flag`, `check`)
- Misleading names that don't match actual purpose

**Good examples:**
- `userAge` not `a`
- `isAuthenticated` not `flag`
- `customerOrders` not `list`

## Function Length Review

Language-specific line count guidelines (excluding blank lines and braces):

- **JavaScript/TypeScript**: 20 lines
- **Python**: 20 lines
- **Java**: 25 lines

Flag functions exceeding these limits. Functions doing multiple things should be split into smaller, focused functions.

## Redundant Comments Review

Identify comments that:
- Repeat what the code clearly states
- Explain obvious operations
- Are outdated or misleading
- Could be replaced by better naming

**Redundant examples:**
```javascript
// Increment counter
counter++;

// Loop through users
for (const user of users) {
```

**Valuable comments explain WHY, not WHAT:**
```javascript
// Using exponential backoff to avoid API rate limits
await retry(apiCall, { maxAttempts: 3 });
```

## Language-Specific Rules

For detailed language-specific conventions:

- **JavaScript/TypeScript**: See [javascript.md](references/language-specific/javascript.md)
- **Python**: See [python.md](references/language-specific/python.md)
- **Java**: See [java.md](references/language-specific/java.md)

Load these files only when reviewing code in that specific language.

## Report Format

Generate a concise report listing issues found:

```
Clean Code Review Results:

Variable Naming Issues:
- Line 12: 'd' -> Use descriptive name like 'deliveryDate'
- Line 25: 'tmp' -> Rename to indicate purpose like 'sortedUsers'

Function Length Issues:
- calculateTotal() (lines 45-78): 34 lines -> Split into smaller functions

Redundant Comments:
- Line 10: "// Set name" -> Remove, code is self-explanatory
- Line 52: "// Return result" -> Remove obvious comment

Summary: 5 issues found (2 naming, 1 length, 2 comments)
```

Keep the report focused and actionable. Only list actual violations found.
