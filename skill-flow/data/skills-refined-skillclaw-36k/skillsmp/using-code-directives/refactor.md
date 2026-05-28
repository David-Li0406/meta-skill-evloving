# @refactor Directive

## Purpose

`@refactor` directives specify code improvements needed through refactoring. After completing the refactoring, the directive is always removed.

## Syntax

```javascript
// @refactor: Extract this logic into a separate function

/* @refactor
 This function is doing too much:
 - Split into smaller functions
 - Extract validation logic
 - Separate data fetching from processing
*/

# @refactor: Use list comprehension instead of loop
```

**Format:**
- Short form: `// @refactor: Brief instruction`
- Long form: Multi-line with detailed refactoring plan

## Step-by-Step Procedure

### 1. Read Full Context

**Understand the current code:**
- What does it do now?
- Why does it need refactoring?
- What are the smells or issues?
- What dependencies exist?

**Read surrounding code:**
- How is this function/class used?
- What tests exist?
- What patterns are used elsewhere in the codebase?

### 2. Plan the Refactoring

**Based on the directive, identify:**
- Specific transformations needed
- Which patterns to apply
- Breaking changes (if any)
- Test updates required

**Common refactoring patterns:**
- Extract function/method
- Extract variable/constant
- Rename for clarity
- Replace conditional with polymorphism
- Simplify complex expression
- Remove duplication
- Introduce parameter object
- Split large function/class

### 3. Execute the Refactoring

**Follow these principles:**
- Make one change at a time
- Keep tests passing (or update them)
- Preserve behavior (refactoring shouldn't change logic)
- Improve readability and maintainability
- Follow existing code style

**If tests exist:**
- Run tests before refactoring
- Make small incremental changes
- Run tests after each change
- Fix any failures immediately

**If no tests exist:**
- Consider adding tests first
- Or be extra careful to preserve behavior
- Manually verify functionality

### 4. Remove the Directive

**After completing the refactoring:**
- Remove the `@refactor` comment completely
- The refactored code should be self-documenting
- Add inline comments only if logic is complex

**Always remove - never keep `@refactor` comments after completion.**

## Examples

### Example 1: Extract Function

**Before:**
```javascript
// @refactor: Extract validation logic into separate function
function createUser(data) {
  // Validation
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.name || data.name.length < 2) {
    throw new Error('Invalid name');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Invalid password');
  }

  // User creation
  return {
    id: generateId(),
    email: data.email,
    name: data.name,
    passwordHash: hashPassword(data.password),
    createdAt: new Date(),
  };
}
```

**After:**
```javascript
function validateUserData(data) {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.name || data.name.length < 2) {
    throw new Error('Invalid name');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Invalid password');
  }
}

function createUser(data) {
  validateUserData(data);

  return {
    id: generateId(),
    email: data.email,
    name: data.name,
    passwordHash: hashPassword(data.password),
    createdAt: new Date(),
  };
}
```

**Directive removed, code is cleaner and more testable.**

### Example 2: Simplify Complex Expression

**Before:**
```python
# @refactor: Simplify this conditional logic
def calculate_discount(user, cart):
    if (user.is_premium and cart.total > 100) or \
       (user.is_premium and user.loyalty_points > 500) or \
       (not user.is_premium and cart.total > 500):
        return 0.15
    elif (user.is_premium and cart.total > 50) or \
         (not user.is_premium and cart.total > 200):
        return 0.10
    else:
        return 0.0
```

**After:**
```python
def calculate_discount(user, cart):
    if user.is_premium:
        if cart.total > 100 or user.loyalty_points > 500:
            return 0.15
        elif cart.total > 50:
            return 0.10
    else:
        if cart.total > 500:
            return 0.15
        elif cart.total > 200:
            return 0.10

    return 0.0
```

**Directive removed, logic is clearer with better structure.**

### Example 3: Remove Duplication

**Before:**
```typescript
/* @refactor
 These two functions are nearly identical - extract common logic
*/
async function fetchUserPosts(userId: number) {
  const response = await fetch(`/api/users/${userId}/posts`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

async function fetchUserComments(userId: number) {
  const response = await fetch(`/api/users/${userId}/comments`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}
```

**After:**
```typescript
async function fetchUserResource(userId: number, resource: string) {
  const response = await fetch(`/api/users/${userId}/${resource}`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

async function fetchUserPosts(userId: number) {
  return fetchUserResource(userId, 'posts');
}

async function fetchUserComments(userId: number) {
  return fetchUserResource(userId, 'comments');
}
```

**Directive removed, duplication eliminated with reusable helper.**

### Example 4: Rename for Clarity

**Before:**
```rust
// @refactor: Rename variables to be more descriptive
fn process(d: &str) -> Vec<i32> {
    let mut r = Vec::new();
    for p in d.split(',') {
        if let Ok(n) = p.trim().parse::<i32>() {
            r.push(n);
        }
    }
    r
}
```

**After:**
```rust
fn parse_comma_separated_numbers(data: &str) -> Vec<i32> {
    let mut numbers = Vec::new();
    for part in data.split(',') {
        if let Ok(number) = part.trim().parse::<i32>() {
            numbers.push(number);
        }
    }
    numbers
}
```

**Directive removed, code is self-documenting with clear names.**

## Decision Tree

```
@refactor directive found
  ↓
Read full context and current code
  ↓
Tests exist?
  YES → Run tests to establish baseline
  NO → Note: be extra careful
  ↓
Identify refactoring pattern(s)
  ↓
Execute refactoring incrementally
  ↓
Tests exist?
  YES → Run tests, fix any failures
  NO → Manually verify behavior
  ↓
Remove @refactor directive completely
```

## Common Mistakes

### ❌ Changing behavior during refactoring
```javascript
// ❌ BAD: Refactoring + behavior change
// Old: Returns null on error
// New: Throws exception on error
```
✅ Fix: Refactoring should preserve behavior. Behavior changes are separate tasks.

### ❌ Keeping the @refactor comment after completion
```javascript
// ❌ BAD
// @refactor: Extract validation [DONE]
function createUser(data) {
  validateUserData(data);
  // ...
}
```
✅ Fix: Always remove @refactor directives when done.

### ❌ Over-refactoring
```javascript
// ❌ BAD: Created 5 tiny functions for 10 lines of code
function validateEmail() { ... }
function validateEmailFormat() { ... }
function validateEmailDomain() { ... }
function checkEmailNotEmpty() { ... }
function verifyEmailStructure() { ... }
```
✅ Fix: Refactor to improve clarity, not to maximize function count.

### ❌ Refactoring without tests or verification
```python
# ❌ BAD: Changed complex logic without verification
# Changed implementation details but didn't verify it still works
```
✅ Fix: Run tests or manually verify behavior is preserved.

## When to Skip or Defer

**Skip refactoring if:**
- You don't understand the current code well enough
- Tests are failing for unrelated reasons
- The code is scheduled for deletion soon
- Breaking changes would require extensive updates

**Ask user if:**
- Refactoring would require breaking API changes
- Multiple approaches are equally valid
- Unclear which pattern fits best

**In these cases, ask user whether to proceed or defer the refactoring.**

## Why Always Remove?

**@refactor directives are one-time actions:**
- Once refactored, the code should be clean
- Keeping the directive creates confusion (is it done or not?)
- The refactored code is the documentation

**If more refactoring is needed later:**
- Add a new @refactor directive when the need arises
- Don't accumulate old completed directives
