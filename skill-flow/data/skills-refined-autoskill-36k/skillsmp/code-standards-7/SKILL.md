---
name: code-standards
description: Baseline coding conventions for naming, formatting, and style
user-invocable: false
---

# Code Standards

Baseline conventions for all code. Apply universally unless overridden by project-specific conventions.

## Naming Conventions

### General Principles

- **Reveal intent:** Names answer why it exists, what it does, how it's used
- **Avoid mental mapping:** No abbreviations that require translation
- **Pronounceable:** You should be able to discuss the code verbally
- **Searchable:** Longer names in larger scopes

### By Type

| Type | Convention | Examples |
|------|------------|----------|
| Variables | camelCase, noun | `userId`, `orderTotal`, `isActive` |
| Functions | camelCase, verb | `getUserById`, `calculateTotal`, `validateInput` |
| Classes | PascalCase, noun | `UserService`, `OrderProcessor` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT` |
| Files | kebab-case | `user-service.ts`, `order-utils.py` |
| Directories | kebab-case | `api-handlers/`, `test-utils/` |

### Boolean Naming

Always prefix with `is`, `has`, `should`, `can`, `will`, or `did`:

```
✓ isActive, hasPermission, shouldRefresh, canEdit
✗ active, permission, refresh, edit
```

### Avoid

| Don't | Instead |
|-------|---------|
| Single letters (except loop `i`, `j`) | Full descriptive name |
| Abbreviations (`custId`) | `customerId` |
| Generic names (`data`, `list`) | `userData`, `orderList` |
| Negated booleans (`isNotDisabled`) | `isEnabled` |

---

## Formatting

### Spacing

- **Indentation:** 2 spaces (JS/TS/HTML) or 4 spaces (Python)
- **Max line length:** 100 characters
- **Trailing whitespace:** Never
- **Final newline:** Always

### Imports

Order: built-ins → external packages → internal modules → relative imports

Blank line between each group. Alphabetize within groups.

### Braces

- Opening brace on same line
- Always use braces, even for single-line bodies

```javascript
// Yes
if (condition) {
  doSomething();
}

// No
if (condition)
  doSomething();
```

---

## Comments

### When to Comment

| Do Comment | Don't Comment |
|------------|---------------|
| Why (intent, business reason) | What (code already says this) |
| Non-obvious gotchas | Obvious operations |
| Complex algorithms (summary) | Bad code to explain it |
| TODO with ticket reference | TODO without context |

### TODO Format

```javascript
// TODO(TICKET-123): Implement retry logic
// FIXME: Race condition when concurrent updates
```

---

## Patterns to Prefer

### Early Returns (Guard Clauses)

```javascript
// Yes - flat, clear
function process(order) {
  if (!order) return null;
  if (!order.items.length) return { error: 'Empty' };
  
  return calculateTotal(order);
}

// No - nested, hard to follow
function process(order) {
  if (order) {
    if (order.items.length) {
      return calculateTotal(order);
    }
  }
  return null;
}
```

### Explicit Over Clever

```javascript
// Yes - clear intent
const activeUsers = users.filter(user => user.isActive);
const names = activeUsers.map(user => user.name);

// No - clever but harder to debug/modify
const names = users.filter(u => u.isActive).map(u => u.name);
```

### Fail Fast

Validate inputs at the boundary:

```javascript
function createUser(data) {
  if (!data.email) throw new ValidationError('Email required');
  if (!isValidEmail(data.email)) throw new ValidationError('Invalid email');
  
  return saveUser(data);
}
```

---

## Patterns to Avoid

### Deep Nesting

Max 3 levels. If deeper, extract to functions.

### Magic Numbers & Strings

```javascript
// No
if (retryCount > 3) { ... }

// Yes
const MAX_RETRIES = 3;
if (retryCount > MAX_RETRIES) { ... }
```

### Boolean Parameters

```javascript
// No - what does 'true' mean?
createUser(data, true, false);

// Yes - options object
createUser(data, { sendWelcome: true, requireVerification: false });
```

### Catch-All Error Handling

```javascript
// No - swallows everything
try { doRiskyThing(); } catch (e) { }

// Yes - handle specific errors
try {
  doRiskyThing();
} catch (e) {
  if (e instanceof NetworkError) return retry();
  throw e;
}
```

---

## Language-Specific Details

For detailed language-specific standards:

- **JavaScript/TypeScript:** See `references/javascript.md`
- **Python:** See `references/python.md`
- **SQL:** See `references/sql.md`
- **Testing:** See `references/testing.md`
