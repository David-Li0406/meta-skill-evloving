---
name: code-review
description: Structured code review workflow for quality and consistency
license: MIT
---

# Code Review Skill

Use this skill when reviewing code changes for quality, consistency, and best practices.

## When to Use

- Reviewing pull requests
- Pair programming sessions
- Pre-merge code checks
- Learning from others' code
- Self-review before committing

## Review Process

### 1. Understand Context

Before reviewing code:
- Read the PR description/ticket
- Understand the goal of the change
- Check if there are related PRs

### 2. High-Level Review

Ask these questions:
- Does this solve the stated problem?
- Is the approach reasonable?
- Are there simpler alternatives?
- Does it fit the existing architecture?

### 3. Detailed Review

#### Code Quality

```typescript
// ❌ Bad: Unclear naming
const d = new Date();
const x = users.filter(u => u.a > d);

// ✅ Good: Self-documenting
const now = new Date();
const activeUsers = users.filter(user => user.lastActiveAt > now);
```

```typescript
// ❌ Bad: Magic numbers
if (retries > 3) { ... }
setTimeout(fn, 86400000);

// ✅ Good: Named constants
const MAX_RETRIES = 3;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (retries > MAX_RETRIES) { ... }
setTimeout(fn, ONE_DAY_MS);
```

#### Function Design

```typescript
// ❌ Bad: Function does too many things
function processUser(user) {
  // Validate (20 lines)
  // Transform (15 lines)
  // Save (10 lines)
  // Send email (15 lines)
  // Log (5 lines)
}

// ✅ Good: Single responsibility
function processUser(user) {
  validateUser(user);
  const transformed = transformUser(user);
  await saveUser(transformed);
  await notifyUser(transformed);
  logUserCreation(transformed);
}
```

#### Error Handling

```typescript
// ❌ Bad: Silent failure
try {
  await riskyOperation();
} catch (e) {
  // nothing
}

// ✅ Good: Proper error handling
try {
  await riskyOperation();
} catch (error) {
  logger.error('Operation failed', { error, context });
  throw new AppError('Operation failed', { cause: error });
}
```

#### Type Safety

```typescript
// ❌ Bad: Type assertions hiding issues
const user = data as User;
const value = (obj as any).property;

// ✅ Good: Type guards and validation
function isUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'id' in data &&
    'email' in data
  );
}

if (isUser(data)) {
  // data is safely typed as User
}
```

### 4. Check Tests

```typescript
// Tests should exist for:
// - Happy path
// - Edge cases
// - Error conditions

describe('calculateDiscount', () => {
  it('should apply 10% for orders over $100', () => { ... });
  it('should return 0 for orders under $50', () => { ... });
  it('should throw for negative amounts', () => { ... });
  it('should handle zero amount', () => { ... });
});
```

### 5. Security Check

- [ ] Input validation on user data
- [ ] No secrets in code
- [ ] SQL queries are parameterized
- [ ] User output is escaped
- [ ] Authentication/authorization verified

## Feedback Guidelines

### Be Specific

```markdown
// ❌ Bad feedback
"This code is confusing"

// ✅ Good feedback
"The variable `d` on line 45 is unclear. Consider renaming to 
`createdDate` to match the domain terminology."
```

### Explain Why

```markdown
// ❌ Bad feedback
"Don't use `any` here"

// ✅ Good feedback
"Using `any` here disables type checking for `processData`.
Consider using `unknown` with a type guard, or define a 
specific interface for the expected data shape."
```

### Suggest Solutions

```markdown
// ❌ Bad feedback
"This function is too long"

// ✅ Good feedback
"This function is 80 lines and handles validation, transformation,
and persistence. Consider extracting into smaller functions:

```typescript
function processOrder(order: Order) {
  validateOrder(order);
  const enriched = enrichOrder(order);
  return saveOrder(enriched);
}
```"
```

### Use the Right Tone

| Instead of | Use |
|------------|-----|
| "You should..." | "Consider..." |
| "This is wrong" | "This might cause..." |
| "Why did you..." | "What do you think about..." |
| "You forgot to..." | "We might want to add..." |

## Comment Categories

Use prefixes for clarity:

| Prefix | Meaning | Action Required |
|--------|---------|-----------------|
| `blocking:` | Must fix before merge | Yes |
| `suggestion:` | Improvement idea | No |
| `question:` | Need clarification | Answer needed |
| `nit:` | Minor style preference | No |
| `praise:` | Good work! | None |

### Examples

```markdown
blocking: This endpoint is missing authentication. Add the 
`authenticate` middleware before the handler.

suggestion: Consider extracting this validation logic into a 
shared `validateEmail` function since it's used in 3 places.

question: I'm not familiar with this library. What's the benefit 
over the standard approach we've been using?

nit: Our style guide prefers `const` over `let` when the variable 
isn't reassigned.

praise: Nice use of the builder pattern here! This makes the 
configuration much more readable.
```

## Review Checklist

### Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs

### Code Quality
- [ ] Code is readable and self-documenting
- [ ] No unnecessary complexity
- [ ] No code duplication
- [ ] Follows project conventions

### Testing
- [ ] Tests exist and are meaningful
- [ ] Tests cover happy path and errors
- [ ] Tests are not flaky
- [ ] Coverage is adequate

### Performance
- [ ] No obvious performance issues
- [ ] Expensive operations are optimized
- [ ] Database queries are efficient

### Security
- [ ] Input is validated
- [ ] Output is escaped
- [ ] Auth is checked
- [ ] No secrets exposed

## Review Output Template

```markdown
## Code Review: PR #123

### Summary
[Brief overview of what was reviewed]

### Blocking Issues 🔴
1. [Issue requiring fix before merge]

### Suggestions 💡
1. [Improvement idea]
2. [Another idea]

### Questions ❓
1. [Clarification needed]

### Positive Notes ✅
- [What was done well]

### Verdict
- [ ] Approved
- [x] Request changes
- [ ] Comment only
```
