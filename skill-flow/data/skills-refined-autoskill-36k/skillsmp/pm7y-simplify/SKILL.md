---
name: pm7y-simplify
description: |
  Explicitly simplifies code by removing unnecessary abstractions, inlining single-use functions, reducing nesting, and applying YAGNI. Produces cleaner, more maintainable code.

  Use this skill when:
  - Code feels over-engineered or hard to follow
  - There are unnecessary abstractions or indirection
  - Functions are used only once and could be inlined
  - Nesting is deep and could be flattened
  - Code has speculative features that aren't needed
allowed-tools: Read, Edit, Glob, Grep
---

# Code Simplification Skill

Explicitly simplifies code by removing unnecessary complexity while preserving all existing behavior.

---

## Overview

This skill identifies and removes unnecessary complexity including:

- **Unnecessary abstractions** - Wrapper functions, unnecessary classes, over-generalized utilities
- **Single-use functions** - Functions called exactly once that could be inlined
- **Deep nesting** - Nested conditionals and loops that could be flattened
- **YAGNI violations** - Speculative features, unused parameters, premature configurability
- **Indirection** - Unnecessary delegation, pass-through functions, redundant layers

**Output:** Simpler code that does the same thing with less complexity.

**When to use:**

- After implementing a feature that feels over-engineered
- When inheriting code that's hard to understand
- Before a code review to catch unnecessary complexity
- When refactoring legacy code
- When code has grown organically and accumulated cruft

---

## Simplification Process

### Step 1: Identify the Target Code

If specific files/functions are provided, focus there. Otherwise:

```
# Find recently modified files
git diff --name-only HEAD~5

# Or find files with high complexity indicators
# (deep nesting, many small functions, lots of indirection)
```

Read the target code thoroughly before making changes.

### Step 2: Find Unnecessary Abstractions

**Wrapper functions that add no value:**
```
Pattern: Functions that just call another function with same/similar args
```

Before:
```typescript
function getUserById(id: string) {
  return fetchUser(id)
}

function fetchUser(id: string) {
  return api.get(`/users/${id}`)
}
```

After:
```typescript
function getUserById(id: string) {
  return api.get(`/users/${id}`)
}
```

**Over-generalized utilities:**

Before:
```typescript
function processItems<T>(items: T[], processor: (item: T) => T): T[] {
  return items.map(processor)
}

// Usage (only place it's called)
const processed = processItems(users, normalizeUser)
```

After:
```typescript
const processed = users.map(normalizeUser)
```

### Step 3: Inline Single-Use Functions

Search for function definitions and their usages:

```
# Find function definitions
Pattern: (function \w+|const \w+ = (\([^)]*\)|[^=]+) =>)

# Count usages of each function name
```

**Candidates for inlining:**
- Functions called exactly once
- Functions with 1-3 lines of code
- Functions that don't improve readability by having a name

Before:
```typescript
function formatDisplayName(user: User): string {
  return `${user.firstName} ${user.lastName}`
}

// Only usage
const displayName = formatDisplayName(currentUser)
```

After:
```typescript
const displayName = `${currentUser.firstName} ${currentUser.lastName}`
```

**Do NOT inline:**
- Functions with meaningful names that document intent
- Functions called in multiple places
- Functions that encapsulate complex logic
- Test helpers or mocks

### Step 4: Reduce Nesting

**Early returns instead of nested conditionals:**

Before:
```typescript
function processUser(user: User | null) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        return doSomething(user)
      } else {
        return null
      }
    } else {
      return null
    }
  } else {
    return null
  }
}
```

After:
```typescript
function processUser(user: User | null) {
  if (!user) return null
  if (!user.isActive) return null
  if (!user.hasPermission) return null
  return doSomething(user)
}
```

**Flatten nested loops where possible:**

Before:
```typescript
const results = []
for (const group of groups) {
  for (const item of group.items) {
    if (item.isValid) {
      results.push(item)
    }
  }
}
```

After:
```typescript
const results = groups.flatMap(g => g.items).filter(item => item.isValid)
```

### Step 5: Apply YAGNI (You Aren't Gonna Need It)

**Remove unused parameters:**

Before:
```typescript
function createUser(name: string, email: string, options?: { sendEmail?: boolean }) {
  // options is never used
  return { name, email }
}
```

After:
```typescript
function createUser(name: string, email: string) {
  return { name, email }
}
```

**Remove speculative features:**

Before:
```typescript
interface Config {
  apiUrl: string
  timeout?: number        // never set
  retryCount?: number     // never set
  customHeaders?: Record<string, string>  // never set
}
```

After:
```typescript
interface Config {
  apiUrl: string
}
```

**Remove premature configurability:**

Before:
```typescript
function fetchData(url: string, method: 'GET' | 'POST' = 'GET') {
  // Always called with GET, POST never used
  return fetch(url, { method })
}
```

After:
```typescript
function fetchData(url: string) {
  return fetch(url)
}
```

### Step 6: Remove Indirection

**Pass-through functions:**

Before:
```typescript
class UserService {
  private repository: UserRepository

  getUser(id: string) {
    return this.repository.getUser(id)
  }

  saveUser(user: User) {
    return this.repository.saveUser(user)
  }
}
```

If `UserService` adds no logic, consider using `UserRepository` directly.

**Unnecessary delegation:**

Before:
```typescript
const handleClick = () => {
  onClick()
}

<button onClick={handleClick}>
```

After:
```typescript
<button onClick={onClick}>
```

### Step 7: Simplify Type Definitions

**Inline simple types:**

Before:
```typescript
type UserId = string
type UserName = string

interface User {
  id: UserId
  name: UserName
}
```

After (if aliases add no meaning):
```typescript
interface User {
  id: string
  name: string
}
```

**Remove redundant interfaces:**

Before:
```typescript
interface UserResponse {
  user: User
}

// Only used once, returned directly
function getUser(): UserResponse {
  return { user: fetchedUser }
}
```

After:
```typescript
function getUser(): { user: User } {
  return { user: fetchedUser }
}
```

---

## Output Format

After simplification, report changes:

```markdown
## Simplification Summary

### Changes Made

1. **Inlined `formatDisplayName`** (line 45)
   - Called only once, 1-line function
   - Before: `const name = formatDisplayName(user)`
   - After: `const name = \`${user.firstName} ${user.lastName}\``

2. **Flattened nested conditionals** (lines 78-95)
   - 4 levels of nesting reduced to sequential early returns

3. **Removed unused `options` parameter** from `createUser` (line 112)
   - Parameter was never used in function body

4. **Inlined `handleSubmit` wrapper** (line 156)
   - Just called `onSubmit()` with no additional logic

### Behavior Preserved

All existing functionality remains unchanged. Tests should pass without modification.

### Files Modified

- `src/components/UserForm.tsx`
- `src/utils/formatters.ts`
```

---

## Simplification Checklist

Before making changes:

- [ ] Read and understand the target code completely
- [ ] Identified functions called only once
- [ ] Identified unnecessary wrapper/delegation functions
- [ ] Found deeply nested code (3+ levels)
- [ ] Found unused parameters or options
- [ ] Found speculative features that aren't used
- [ ] Verified changes preserve behavior

After making changes:

- [ ] Each simplification maintains identical behavior
- [ ] No business logic was accidentally removed
- [ ] Code is more readable, not just shorter
- [ ] Changes are documented in summary

---

## Constraints

### DO:
- Preserve all existing behavior exactly
- Make one simplification at a time
- Verify each change before moving to the next
- Keep meaningful abstractions that aid understanding
- Inline only when it improves or maintains readability

### DO NOT:
- Change behavior in any way
- Remove code that's actually used (check thoroughly)
- Expand scope beyond simplification
- Add new features or functionality
- Refactor unrelated code
- Remove error handling or validation
- Remove meaningful type aliases that document intent
- Inline functions that will be called from multiple places in future (check git history for patterns)

---

## When NOT to Simplify

Some apparent complexity is justified:

**Keep abstractions when:**
- They provide meaningful names for concepts
- They're used in multiple places
- They encapsulate genuinely complex logic
- They provide extension points that are actually used
- They improve testability in a meaningful way

**Keep separate functions when:**
- The name documents important intent
- The logic might need to change independently
- They're used in tests as boundaries

**Keep indirection when:**
- It provides dependency injection for testing
- It's part of an established pattern in the codebase
- Removing it would require changes in many places

---

## Example Session

User: "Simplify this React component"

Discovery phase:
1. Read the component file
2. Identify: 3 single-use helper functions, 2 levels of unnecessary nesting, unused `className` prop

Simplification:
1. Inline `formatDate` (1 line, called once)
2. Inline `getStatusColor` (simple ternary, called once)
3. Keep `validateForm` (meaningful name, complex logic)
4. Flatten nested `if (user) { if (user.isActive) { ... } }`
5. Remove unused `className` prop from interface and destructuring

Result:
- 45 lines reduced to 32 lines
- 2 fewer functions to trace through
- Behavior unchanged
- More readable linear flow
