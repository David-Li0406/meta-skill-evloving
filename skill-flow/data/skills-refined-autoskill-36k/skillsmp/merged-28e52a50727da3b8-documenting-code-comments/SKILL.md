---
name: documenting-code-comments
description: Use this skill when auditing, cleaning up, or improving inline code documentation by following best practices for writing self-documenting code and effective comments.
---

# Code Comment Guidelines

## Core Philosophy

**The best comment is the one you didn't need to write.**

Self-documenting code reduces maintenance burden and prevents comment drift. Clear naming and structure can significantly reduce onboarding time.

### Writing Style Guidelines

**Tone:** Be direct, practical, and clear. Write in a natural and relaxed tone, avoiding corporate buzzwords, overly formal language, and excessive enthusiasm.

### Hierarchy of Documentation

1. **Make code self-documenting** (naming, structure, types)
2. **Use type systems** to document contracts
3. **Add comments only for WHY**, never for WHAT

## Refactoring: Preserve Existing Comments

**This skill's guidance applies to writing new code. When refactoring existing code, preserve comments.**

### Never Remove

- Comments explaining WHY something exists
- Comments warning about gotchas or edge cases
- Comments referencing external context (tickets, specs, RFCs)
- Comments documenting non-obvious business logic

### Update When Necessary

- If refactoring changes behavior the comment describes, update the comment.
- If refactoring makes a workaround obsolete, update or remove it.
- Add to existing comments if refactoring introduces new context.

### Only Remove When

- The comment is demonstrably incorrect.
- The comment documents code you're deleting entirely.
- The refactoring eliminates the "why."

## When NOT to Write Comments

### Never Comment the Obvious

```javascript
const name = user.name; // Get the user's name
items.forEach(item => process(item)); // Loop through items
```

### Never Duplicate Type Information

```javascript
/** @param {string} email - The email string to validate */
function validateEmail(email: string): boolean {}
```

### Never Leave Stale Comments

```javascript
// Returns user's full name
const getEmail = () => user.email;
```

## When TO Write Comments

### 1. Explain WHY, Not WHAT

```javascript
// Use exponential backoff - service rate-limits after 3 rapid failures
const backoffMs = Math.pow(2, attempts) * 1000;
```

### 2. Warn About Gotchas and Edge Cases

```javascript
// IMPORTANT: Assumes UTC - local timezone causes date drift
const dayStart = new Date(date.setHours(0, 0, 0, 0));
```

### 3. Reference External Context

```javascript
// Workaround for Safari flexbox bug (JIRA-1234)
display: '-webkit-flex';
```

### 4. Document Performance Decisions

```javascript
// Map for O(1) lookup - benchmarked 3x faster than array.find() at n>100
const userMap = new Map(users.map(u => [u.id, u]));
```

### 5. Complex Business Logic

```javascript
// Discount applies only to orders >$100 AND first-time customers
if (orderTotal > 100 && customer.orderCount === 0) {
```

## Comment Formatting Standards

### Single-line Comments

```javascript
// Sentence case, no period for fragments
// Full sentences get periods.
```

### JSDoc/TSDoc for Public APIs

Only when behavior isn't obvious from signature:

```typescript
/**
Validates email format and checks domain blacklist.
  @throws {ValidationError} If format invalid or domain blacklisted
  @example
    validateEmail('user@example.com'); // OK
    validateEmail('spam@blocked.com'); // throws
*/
function validateEmail(email: string): void {}
```

### TODO Format

```javascript
// TODO(JIRA-567): Replace with batch API when available Q1 2025
```

## Refactor Before Commenting

| Instead of commenting...      | Refactor to...                                      |
| ----------------------------- | --------------------------------------------------- |
| `// Get active users`         | `const activeUsers = users.filter(u => u.isActive)` |
| `// Check if admin`           | `const isAdmin = user.role === 'admin'`             |
| `// 86400000 ms = 1 day`      | `const ONE_DAY_MS = 24 * 60 * 60 * 1000`            |
| `// Handle error case`        | Extract to `handleAuthError(err)` function          |
| `// Calculate total with tax` | `const totalWithTax = calculateTotalWithTax(items)` |

## Audit Checklist

When reviewing code comments:

1. **Necessity**: For new code, can it be self-documenting? For existing code, is this comment still accurate?
2. **Accuracy**: Does comment match current code behavior?
3. **Value**: Does it explain WHY, not WHAT?
4. **Freshness**: Is it still relevant?
5. **Actionability**: If TODO, does it have a ticket reference?

## Language-Specific Patterns

### TypeScript/JavaScript

- Prefer TypeScript types over JSDoc type annotations.
- Use `@deprecated` JSDoc tag for deprecated APIs.
- Document thrown errors in JSDoc when not obvious.

### Go

- Follow effective Go: first sentence is function name + verb.
- Document exported functions; unexported can be brief.

### Python

- Use docstrings for modules, classes, functions.
- Follow Google or NumPy docstring format consistently.
- Type hints reduce need for parameter documentation.