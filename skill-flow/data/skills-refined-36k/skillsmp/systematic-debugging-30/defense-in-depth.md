# Defense in Depth

## Overview

After finding and fixing a root cause, add validation at multiple layers to prevent similar issues.

## The Pattern

```
Layer 1: Input Validation
    ↓
Layer 2: Business Logic Validation
    ↓
Layer 3: Data Access Validation
    ↓
Layer 4: Database Constraints
```

## When to Apply

Apply AFTER you've:
1. Found the root cause
2. Fixed it at the source
3. Want to prevent similar issues

## Example: User Data Flow

```typescript
// Layer 1: API Input
app.post('/users', (req, res) => {
  const { email } = req.body;
  if (!email || !isValidEmail(email)) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  // proceed...
});

// Layer 2: Service Layer
class UserService {
  async createUser(email: string) {
    if (!email) {
      throw new ValidationError('Email required');
    }
    // proceed...
  }
}

// Layer 3: Repository Layer
class UserRepository {
  async insert(user: User) {
    if (!user.email) {
      throw new DataError('Cannot insert user without email');
    }
    // proceed...
  }
}

// Layer 4: Database
-- CREATE TABLE users (
--   email TEXT NOT NULL UNIQUE
-- );
```

## Benefits

1. **Fail Fast**: Catch issues at the earliest possible point
2. **Clear Errors**: Each layer gives specific error messages
3. **Redundancy**: If one layer is bypassed, others still protect
4. **Debugging**: Easy to see WHERE validation failed

## Important Notes

- Defense in depth is NOT a substitute for finding root cause
- Apply AFTER fixing the source issue
- Each layer should have appropriate error messages
- Don't add so many checks that code becomes unreadable

## Anti-Pattern

```typescript
// BAD: Checks everywhere without understanding
if (data && data.user && data.user.email && isValidEmail(data.user.email)) {
  // This masks issues instead of preventing them
}
```

## Good Pattern

```typescript
// GOOD: Validation at appropriate layers with clear errors
function validateUserInput(input: unknown): UserInput {
  if (!input || typeof input !== 'object') {
    throw new ValidationError('Invalid input format');
  }
  if (!('email' in input) || typeof input.email !== 'string') {
    throw new ValidationError('Email is required');
  }
  // Return typed, validated object
  return input as UserInput;
}
```
