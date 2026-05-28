---
name: foundational-patterns
description: Use this skill to implement common logging and testing patterns for observable and reliable applications.
---

# Foundational Patterns

This skill covers essential logging and testing practices to enhance application observability and reliability.

## Logging Patterns

### Rules

- Use structured logging (key-value pairs, not interpolated strings).
- Include request/correlation IDs in all log entries.
- Log at appropriate levels (DEBUG, INFO, WARN, ERROR).
- Include enough context to debug issues without the code.
- Avoid logging sensitive information (passwords, tokens, PII).

### Pitfalls

- Logging sensitive data (passwords, API keys, PII).
- Inconsistent log levels across the codebase.
- Missing correlation IDs in distributed systems.
- Logging at inappropriate levels (DEBUG in production, ERROR for non-errors).

### Example

```rust
// Structured logging with tracing
use tracing::{info, error, instrument};

#[instrument(skip(password))]
fn authenticate(user_id: &str, password: &str) -> Result<Token> {
    info!(user_id, "authentication attempt");

    match verify_credentials(user_id, password) {
        Ok(token) => {
            info!(user_id, "authentication successful");
            Ok(token)
        }
        Err(e) => {
            error!(user_id, error = %e, "authentication failed");
            Err(e)
        }
    }
}
```

## Testing Patterns

### Rules

- Write tests for happy paths and error cases.
- Test edge cases and boundary conditions.
- Each test should test one thing.
- Tests should be deterministic and repeatable.
- Use descriptive test names that explain the scenario.

### Checklist

- [ ] Happy path is covered.
- [ ] Error cases are tested.
- [ ] Edge cases are identified and tested.
- [ ] Tests are independent and can run in any order.
- [ ] Test data is isolated per test.
- [ ] No flaky tests in the suite.

### Pitfalls

- Testing implementation details instead of behavior.
- Not testing error paths.
- Shared mutable state between tests.
- Tests that depend on execution order.