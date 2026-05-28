---
name: gleam-testing
description: Guides Claude through testing Gleam applications with gleeunit. Use when writing unit tests, integration tests, or property-based tests. Always use let assert, NOT deprecated should module.
---

# Gleam Testing Skill

This skill guides Claude Code through testing Gleam applications.

## Primary Sources

1. **[Gleeunit Documentation](https://hexdocs.pm/gleeunit/)** - Test framework
2. **[Let Assert - Gleam Tour](https://tour.gleam.run/advanced-features/let-assert/)** - Assertion syntax
3. **[Testing Guide](https://abs0luty.github.io/gleam-tutorial/testing.html)** - Comprehensive testing
4. **[Test Timeouts](https://gearsco.de/blog/gleam-test-timeouts/)** - Timeout configuration
5. **[Birdie](https://hexdocs.pm/birdie/)** - Snapshot testing
6. **[Glacier](https://hexdocs.pm/glacier/)** - Interactive testing
7. **[QCheck](https://hexdocs.pm/gleam_qcheck/)** - Property-based testing
8. **[Gleamy Bench](https://hexdocs.pm/gleamy_bench/)** - Benchmarking

## Quick Reference

### Test Command
```bash
gleam test                    # Run all tests
gleam test --target erlang    # Erlang target only
gleam test --target javascript # JavaScript target only
```

### Test File Structure
```
project/
├── test/
│   ├── project_name_test.gleam    # Main test file
│   ├── feature_a_test.gleam       # Feature tests
│   └── feature_b_test.gleam
```

## Critical Rules

### Use `let assert` NOT `should` (MANDATORY)

The `gleeunit/should` module is **deprecated**.

See examples: [Testing Practices](../../rules/testing-practices.md)

### Test Function Naming (MANDATORY)

Functions ending in `_test` are automatically discovered and run.

```gleam
pub fn my_feature_test() {
  // Test implementation
}
```

See: [Gleeunit Documentation](https://hexdocs.pm/gleeunit/)

## Common Testing Patterns

### Unit Testing

```gleam
pub fn add_test() {
  let assert 5 = add(2, 3)
  let assert 0 = add(-1, 1)
}
```

### Testing Result Types

```gleam
pub fn parse_success_test() {
  let assert Ok(value) = parse("valid input")
  let assert expected_value = value
}

pub fn parse_failure_test() {
  let assert Error(Nil) = parse("invalid input")
}
```

### Testing Custom Types

```gleam
pub fn user_creation_test() {
  let user = create_user("alice@example.com")
  let assert Active(_, email) = user
  let assert "alice@example.com" = email
}
```

### Testing Error Variants

```gleam
pub fn error_handling_test() {
  let assert Error(NotFound(id)) = fetch_user("invalid-id")
  let assert "invalid-id" = id
}
```

## Advanced Testing

### Test Timeouts (Erlang Target)

For tests that need more than 5 seconds:

See: [Gleam Test Timeouts](https://gearsco.de/blog/gleam-test-timeouts/)

### Property-Based Testing

For testing properties that should hold for all inputs:

See: [gleam_qcheck Documentation](https://hexdocs.pm/gleam_qcheck/)

Example use cases:
- Testing that `reverse(reverse(list)) == list`
- Verifying encoding/decoding round-trips
- Checking mathematical properties

### Snapshot Testing

For testing rendered output:

See: [Birdie Documentation](https://hexdocs.pm/birdie/)

Use cases:
- HTML rendering
- JSON API responses
- Formatted text output

### Interactive Testing

For development workflows with fast feedback:

See: [Glacier Documentation](https://hexdocs.pm/glacier/)

## Testing Web Applications

### HTTP Request Testing

For Wisp applications:
See: [Wisp Testing](https://hexdocs.pm/wisp/)

### Database Testing

Patterns for testing with databases:
1. Use test databases
2. Wrap tests in transactions (rollback after)
3. Use fixtures for test data
4. Consider using SQLite in-memory for fast tests

### Mocking External Services

Gleam doesn't have built-in mocking. Patterns:
1. Dependency injection via function parameters
2. Test doubles (implement same type)
3. Behavior parameterization

## Testing OTP Applications

### Actor Testing

```gleam
import gleam/otp/actor

pub fn actor_behavior_test() {
  let assert Ok(actor.Started(subject, _)) = start_my_actor()

  // Test message handling
  let response = actor.call(subject, waiting: 100, sending: fn(s) { GetState(s) })
  let assert expected_state = response
}
```

See: [OTP Development](../skills/gleam-otp-development/SKILL.md)

### Supervision Testing

Test that supervisors:
- Start children correctly
- Restart children on failure
- Respect max restart limits

## Performance Testing

### Benchmarking

For performance measurements:

See: [gleamy_bench Documentation](https://hexdocs.pm/gleamy_bench/)

Use cases:
- Comparing algorithm implementations
- Measuring optimization impact
- Profiling hot code paths

## Test Organization

### Test Modules

Organize tests by feature or domain:
```
test/
├── auth_test.gleam        # Authentication tests
├── user_test.gleam        # User management
├── api_test.gleam         # API endpoints
└── integration_test.gleam # Integration tests
```

### Test Helpers

Create helper functions in test modules:
```gleam
// test/test_helpers.gleam
pub fn create_test_user() -> User {
  User(id: "test-id", email: "test@example.com")
}

pub fn with_database(test: fn(Connection) -> a) -> a {
  let assert Ok(conn) = setup_test_db()
  let result = test(conn)
  teardown_test_db(conn)
  result
}
```

## Cross-Platform Testing

Tests run on both Erlang and JavaScript targets by default. Be aware of platform differences:

- Test timeouts only work on Erlang
- Some external functions behave differently
- Platform-specific tests can use `@target` attribute

See: [External Functions](../../rules/external-functions.md)

## CI/CD Integration

### GitHub Actions

Example workflow:
```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: erlef/setup-beam@v1
        with:
          otp-version: "27.0"
          gleam-version: "1.10.0"
      - run: gleam deps download
      - run: gleam test
      - run: gleam format --check src test
```

See: [Writing Gleam - CI/CD](https://gleam.run/writing-gleam/)

## Test Coverage

Currently, Gleam doesn't have built-in coverage tools. Options:
1. Use Erlang's cover tool
2. Monitor test comprehensiveness manually
3. Focus on critical path coverage

## Common Testing Patterns

### Table-Driven Tests

```gleam
pub fn multiple_cases_test() {
  let cases = [
    #("input1", "output1"),
    #("input2", "output2"),
    #("input3", "output3"),
  ]

  list.each(cases, fn(case) {
    let #(input, expected) = case
    let assert expected = my_function(input)
  })
}
```

### Setup and Teardown

```gleam
pub fn test_with_setup() {
  // Setup
  let resource = create_resource()

  // Test
  let assert Ok(result) = use_resource(resource)

  // Teardown (using defer-like pattern)
  cleanup_resource(resource)
}
```

## Test Quality Guidelines

✅ **Good tests:**
- Test one thing
- Have clear names
- Are independent (no shared state)
- Are fast (when possible)
- Are deterministic

❌ **Avoid:**
- Testing implementation details
- Shared mutable state
- Flaky tests (timing-dependent)
- Tests that are hard to understand

---

**Remember**: Tests are documentation. Write them clearly and maintain them carefully.
