# @todo Directive

## Purpose

`@todo` directives mark task items that need to be completed. After completing the task, the directive is always removed.

## Syntax

```javascript
// @todo: Add error handling

/* @todo
 Improvements needed:
 - Add input validation
 - Improve error messages
 - Add logging
*/

# @todo: Optimize this query - currently N+1
```

**Format:**
- Short form: `// @todo: Brief task description`
- Long form: Multi-line with task list
- Can include context or urgency markers

## Step-by-Step Procedure

### 1. Read the Todo Item

**Understand what needs to be done:**
- What is the specific task?
- Why is it needed?
- What's the priority or urgency?
- Are there dependencies?

**Check context:**
- Where is the todo located?
- What code does it relate to?
- Is there related code elsewhere?

### 2. Assess Scope

**Determine if you should do it now:**

#### Do it now if:
- Task is clear and well-defined
- Small effort (< 30 minutes)
- Blocks other work
- Easy to complete

#### Ask user if:
- Task is large or complex
- Unclear how to implement
- Requires architectural decisions
- Might break existing code
- Priority is uncertain

#### Defer if:
- Explicitly marked as "later" or "future"
- Depends on incomplete work
- Outside current scope
- User indicates low priority

### 3. Complete the Task

**Execute the todo item:**
- Follow existing code patterns
- Maintain code quality
- Add tests if needed
- Update documentation if needed

**Keep it focused:**
- Only do what the todo specifies
- Don't add extra features
- Don't refactor unrelated code

### 4. Remove the Directive

**After completing the task:**
- Remove the `@todo` comment completely
- The completed work is the documentation
- Don't mark as "DONE" - remove it

**Always remove completed todos.**

## Examples

### Example 1: Add Error Handling

**Before:**
```javascript
async function fetchUserData(userId) {
  // @todo: Add error handling for network failures
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}
```

**After:**
```javascript
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
  } catch (error) {
    console.error('Failed to fetch user data:', error);
    throw error;
  }
}
```

**Directive removed after error handling added.**

### Example 2: Add Input Validation

**Before:**
```python
def create_user(name, email):
    # @todo: Validate inputs before creating user
    return User(name=name, email=email)
```

**After:**
```python
def create_user(name, email):
    if not name or len(name) < 2:
        raise ValueError("Name must be at least 2 characters")
    if not email or '@' not in email:
        raise ValueError("Invalid email address")

    return User(name=name, email=email)
```

**Directive removed after validation added.**

### Example 3: Performance Optimization

**Before:**
```rust
// @todo: Optimize - this creates unnecessary allocations
fn process_items(items: &[Item]) -> Vec<String> {
    let mut results = Vec::new();
    for item in items {
        results.push(item.name.clone());
    }
    results
}
```

**After:**
```rust
fn process_items(items: &[Item]) -> Vec<String> {
    items.iter()
        .map(|item| item.name.clone())
        .collect()
}
```

**Directive removed after optimization.**

### Example 4: Multiple Tasks

**Before:**
```typescript
class UserService {
  /* @todo
   - Add caching
   - Add retry logic
   - Add request timeout
  */
  async getUser(id: string): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    return response.json();
  }
}
```

**After:**
```typescript
class UserService {
  private cache = new Map<string, User>();

  async getUser(id: string): Promise<User> {
    // Check cache
    if (this.cache.has(id)) {
      return this.cache.get(id)!;
    }

    // Fetch with timeout and retry
    const response = await this.fetchWithRetry(`/api/users/${id}`, {
      timeout: 5000,
      maxRetries: 3,
    });

    const user = await response.json();
    this.cache.set(id, user);
    return user;
  }

  private async fetchWithRetry(url: string, options: FetchOptions): Promise<Response> {
    // ...retry implementation...
  }
}
```

**Directive removed after all three tasks completed.**

## Decision Tree

```
@todo directive found
  ↓
Is task clear and well-defined?
  NO → Ask user for clarification
  YES → Continue
  ↓
Is task small and quick?
  YES → Do it now
  NO → Ask user if should do now or defer
  ↓
Complete the task
  ↓
Remove @todo directive completely
```

## Common Mistakes

### ❌ Marking todo as done instead of removing
```javascript
// ❌ BAD
// @todo: Add validation [DONE]
// @todo: Add validation ✓
// @todo: Add validation - COMPLETED
```
✅ Fix: Remove the comment entirely.

### ❌ Leaving todos indefinitely
```python
# ❌ BAD: Todo from 2 years ago still in code
# @todo: Add caching (2023-01-15)
def get_user(id):
    ...
```
✅ Fix: Either complete the todo or ask user if it's still needed.

### ❌ Adding more todos while completing one
```javascript
// ❌ BAD
// Original: @todo: Add error handling
// After: Added error handling but also added logging, caching, retry logic
```
✅ Fix: Only complete what the todo specifies.

### ❌ Completing unclear todos without asking
```typescript
// @todo: Fix this
// ❌ What needs fixing? Don't guess.
```
✅ Fix: Ask user what needs to be fixed.

## When to Ask User

**Ask for clarification if:**
- Todo is vague ("Fix this", "Make better", "Improve")
- Multiple valid approaches exist
- Todo is large or complex
- Priority is unclear
- Todo conflicts with current code design

**Example questions:**
- "This todo says 'add caching' - should I use in-memory caching or Redis?"
- "Should I complete this todo now or defer it?"
- "This todo is unclear - what specifically needs fixing?"

## Urgency Markers

**Some todos include urgency markers:**

```javascript
// @todo: URGENT - Fix memory leak
// @todo: FIXME - Broken on IE11
// @todo: HACK - Temporary workaround, replace with proper solution
// @todo: NOTE - Consider using library instead
```

**Handle based on marker:**
- `URGENT`, `FIXME` → High priority, do now
- `HACK` → Indicates temporary code that needs replacing
- `NOTE` → Informational, may not need action

## Deferring Todos

**If user says to defer:**
- Leave the @todo comment in place
- Don't mark as "deferred" or "later" - it's already a todo
- Let user manage todo priority

**If todo is no longer needed:**
- Remove the @todo comment entirely
- User changed their mind → it's not a task anymore

## Why Always Remove When Done?

**@todo directives are pending work:**
- Once done, there's no pending work
- Keeping creates confusion (is it done or not?)
- Accumulating completed todos clutters code
- The completed work is self-documenting

**Completed todos don't provide value - remove them.**

## Special Cases

### Todo in Comments for Future Readers

**Sometimes developers leave notes for the future:**

```javascript
// Future optimization: Could use binary search here if list is sorted
function findItem(list, target) {
  return list.find(item => item.id === target);
}
```

**This is NOT a @todo directive - it's a design note:**
- No action required now
- Informational only
- Leave it in place

**Only @todo directives should be treated as actionable tasks.**

### Todo with Date or Author

```python
# @todo (john, 2024-01-15): Migrate to new API
```

**Still a todo:**
- Date/author is just context
- Follow same process
- Remove entire comment when done

### Todo for Missing Feature

```rust
// @todo: Add support for authentication
// This will require implementing the Auth trait
```

**If it's a significant feature:**
1. Ask user if should implement now
2. If no, defer (leave todo in place)

## Quick Reference

| Situation | Action |
|-----------|--------|
| Todo is clear and small | Complete and remove |
| Todo is unclear | Ask user for clarification |
| Todo is large | Ask user if should do now |
| Todo is marked URGENT/FIXME | Complete now if possible |
| Todo says "later" or "future" | Defer (leave in place) |
| Todo is completed | Remove entirely |
