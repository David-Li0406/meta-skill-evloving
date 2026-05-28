# @implement Directive

## Purpose

`@implement` directives contain implementation instructions that you should execute immediately. After implementation, the directive comment is transformed into proper documentation or removed based on context.

## Syntax

```javascript
/* @implement
 [Implementation instructions go here]
 - Bullet points are common
 - Can span multiple lines
 - Describes what to build
*/
```

**Language-specific comment styles:**
- JavaScript/TypeScript: `/* @implement ... */` or `// @implement ...`
- Python: `# @implement ...` or `"""@implement ..."""`
- Rust/Go/Java: `// @implement ...` or `/* @implement ... */`
- Ruby: `# @implement ...`
- Any other: Use that language's comment syntax

## Step-by-Step Procedure

### 1. Read Full Context

**Before implementing, understand:**
- What does the surrounding code do?
- Where is this directive located? (in docblock, above function, standalone, inline)
- What existing patterns should you follow?
- Are there related functions/classes to reference?

**Location determines post-action:**
```javascript
/**
 * @implement
 * Add user authentication
 */
class UserService { }  // → In docblock

// @implement: Add user authentication
class UserService { }  // → Above signature

class UserService {
  // @implement: Add authentication here
}  // → Standalone inline
```

### 2. Execute Implementation

**Follow the instructions in the directive:**
- Implement exactly what's described
- Follow existing code patterns and style
- Add proper error handling
- Consider edge cases
- Write clean, maintainable code

**Don't over-engineer:**
- Only implement what's explicitly requested
- Don't add extra features "just in case"
- Keep it simple

### 3. Apply Post-Action Transformation

**The transformation depends on where the directive was located.**

#### Case A: Directive in Function/Class Docblock

**Original:**
```typescript
/**
 * @implement
 * Add a caching layer for user data:
 * - Cache user objects by ID in a Map
 * - Expire entries after 5 minutes
 * - Return cached data if available and fresh
 */
class UserService {
  async getUser(id: string): Promise<User> {
    // ... implementation added ...
  }
}
```

**Transform to proper documentation:**
```typescript
/**
 * User service with 5-minute caching layer.
 * Caches user objects by ID and expires stale entries automatically.
 */
class UserService {
  async getUser(id: string): Promise<User> {
    // ... implementation ...
  }
}
```

**Rules:**
- Describe *what* was implemented, not *how*
- Focus on user-facing behavior
- Use proper doc format (JSDoc, docstring, etc.)
- Remove implementation details (those belong in code/comments)

#### Case B: Directive Above Function Signature

**Original:**
```python
# @implement: Validate email format and domain
def validate_email(email: str) -> bool:
    pass
```

**Transform to docstring:**
```python
def validate_email(email: str) -> bool:
    """
    Validates email format and domain.

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    # ... implementation ...
```

**Rules:**
- Create proper function documentation
- Document parameters and return values
- Describe validation rules or behavior
- Remove the @implement directive entirely

#### Case C: Standalone Directive

**Original:**
```javascript
class AuthService {
  // @implement: Add token refresh logic here

  login(credentials) {
    // ...
  }
}
```

**After implementation, remove the directive:**
```javascript
class AuthService {
  refreshToken() {
    // Token refresh implementation
  }

  login(credentials) {
    // ...
  }
}
```

**Rules:**
- Remove directive comment completely
- The implementation is self-documenting
- Add inline comments only if logic is complex

#### Case D: Inline Implementation Detail

**Original:**
```rust
fn calculate_score(data: &Data) -> f64 {
    let base = data.value * 2.0;
    // @implement: Add bonus multiplier for premium users
    base
}
```

**After implementation:**
```rust
fn calculate_score(data: &Data) -> f64 {
    let base = data.value * 2.0;
    let multiplier = if data.is_premium { 1.5 } else { 1.0 };
    base * multiplier
}
```

**Rules:**
- Remove directive comment
- Code is self-explanatory
- Add comment only if multiplier logic is non-obvious

## Examples

### Example 1: Class Method Documentation

**Before:**
```typescript
class PaymentProcessor {
  /**
   * @implement
   * Process payment with retry logic:
   * - Try up to 3 times
   * - Exponential backoff (1s, 2s, 4s)
   * - Log failures
   * - Return success/failure status
   */
  async processPayment(amount: number): Promise<boolean> {
    throw new Error('Not implemented');
  }
}
```

**After:**
```typescript
class PaymentProcessor {
  /**
   * Processes payment with automatic retry on failure.
   * Retries up to 3 times with exponential backoff.
   *
   * @param amount - Payment amount in cents
   * @returns True if payment succeeded, false otherwise
   */
  async processPayment(amount: number): Promise<boolean> {
    // Implementation with retry logic...
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        await this.chargeCard(amount);
        return true;
      } catch (error) {
        this.logger.error('Payment failed', { attempt, error });
        if (attempt < 2) {
          await this.delay(Math.pow(2, attempt) * 1000);
        }
      }
    }
    return false;
  }
}
```

### Example 2: Utility Function

**Before:**
```python
# @implement: Parse ISO date string and return datetime object with timezone
def parse_date(date_str):
    pass
```

**After:**
```python
def parse_date(date_str: str) -> datetime:
    """Parses ISO 8601 date string with timezone information."""
    return datetime.fromisoformat(date_str)
```

### Example 3: Configuration Addition

**Before:**
```javascript
const config = {
  api: {
    baseUrl: 'https://api.example.com',
    timeout: 5000,
    // @implement: Add retry configuration
  }
};
```

**After:**
```javascript
const config = {
  api: {
    baseUrl: 'https://api.example.com',
    timeout: 5000,
    retry: {
      maxAttempts: 3,
      backoffMs: 1000,
    },
  }
};
```

## Decision Tree

```
@implement directive found
  ↓
Is it in a docblock (/** ... */ before function/class)?
  YES → Implement, then transform to proper documentation
  NO → Continue
  ↓
Is it directly above a function signature?
  YES → Implement, then create function docs
  NO → Continue
  ↓
Is it a standalone comment?
  YES → Implement, then remove comment entirely
```

## Common Mistakes

### ❌ Leaving @implement comment after implementation
```javascript
// ❌ BAD
/* @implement: Add caching */
async getUser(id) {
  return this.cache.get(id) || await this.fetchUser(id);
}
```

```javascript
// ✅ GOOD
async getUser(id) {
  return this.cache.get(id) || await this.fetchUser(id);
}
```

### ❌ Copying implementation details into documentation
```javascript
// ❌ BAD
/**
 * Uses a Map to cache users by ID.
 * Checks cache first with this.cache.get(id).
 * Falls back to this.fetchUser(id) if not found.
 */
```

```javascript
// ✅ GOOD
/**
 * Retrieves user by ID with caching.
 */
```

### ❌ Not following existing documentation patterns
Check how other functions in the same file are documented and follow that style.
