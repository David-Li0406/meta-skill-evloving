---
name: testing-patterns
description: Use this skill when writing tests, implementing TDD, creating mocks, or discussing test coverage and testing strategies.
---

# Testing Patterns

Universal testing patterns that apply across languages and frameworks. This skill covers test writing patterns, TDD workflows, and mocking strategies.

## Test-Driven Development (TDD)

### The TDD Cycle

```
Red → Green → Refactor
```

1. **Red**: Write a failing test.
2. **Green**: Write minimal code to pass the test.
3. **Refactor**: Improve the code while keeping tests passing.

### TDD Example (Pseudocode)

```
# Step 1: Red - Write failing test
test "add returns sum of two numbers":
    assert add(2, 3) == 5  # Fails - function doesn't exist

# Step 2: Green - Minimal implementation
function add(a, b):
    return 5  # Passes, but not generalized

# Step 3: Refactor - Proper implementation
function add(a, b):
    return a + b  # Correct implementation
```

## Test Structure

### Arrange-Act-Assert (AAA)

```
test "user can log in with valid credentials":
    # Arrange - Set up test conditions
    user = create_test_user(email="test@example.com", password="secret")

    # Act - Perform the action
    result = login(email="test@example.com", password="secret")

    # Assert - Verify the outcome
    assert result.success == true
    assert result.user.email == "test@example.com"
```

### Given-When-Then (BDD Style)

```
test "authenticated user can access dashboard":
    # Given a logged-in user
    user = login_as_test_user()

    # When they access the dashboard
    response = get_dashboard(user)

    # Then they see their data
    assert response.status == 200
    assert response.contains(user.name)
```

## Principles of Testing

- **Test behaviour, not implementation**: Tests should survive refactoring.
- **One assertion per concept**: Each test proves one thing clearly.
- **Fast and deterministic**: No flaky tests, no slow I/O in unit tests.
- **Readable as documentation**: Test names describe the behaviour.

## Mocking Patterns

### When to Mock

Mock when:
- External services (APIs, databases).
- Slow operations.
- Non-deterministic behavior (time, random).
- Side effects (emails, payments).

Don't mock:
- The thing you're testing.
- Simple value objects.
- When a real implementation is easy.

### Mock Types

#### Stub
Returns predetermined values:
```
stub_api.get_user = returns({ id: 1, name: "Test" })
```

#### Spy
Records calls for verification:
```
spy_logger = spy(logger)
do_something()
assert spy_logger.called_with("Something happened")
```

#### Fake
Working implementation with shortcuts:
```
fake_db = InMemoryDatabase()  # Real behavior, no persistence
```

## Test Categories

### Unit Tests
- Test one function/method in isolation.
- Fast (milliseconds).
- Mock dependencies.

### Integration Tests
- Test components working together.
- Use real dependencies where practical.
- Slower (seconds).

### End-to-End Tests
- Test full user flows.
- Real browser/client.
- Slowest (minutes).

## Testing Pyramid

```
         /\
        /  \  E2E (few)
       /────\
      /      \  Integration (some)
     /────────\
    /          \  Unit (many)
   /────────────\
```

## Quick Checklist

Before completing a feature:
- [ ] Happy path tested.
- [ ] Error cases tested.
- [ ] Edge cases tested.
- [ ] All tests pass.
- [ ] No flaky tests introduced.

## Coverage Guidance

- **Line coverage**: Aim for 80%+ on critical paths.
- **Branch coverage**: All if/else branches exercised.
- **Don't chase 100%**: Diminishing returns after ~85%.
- **Coverage ≠ quality**: You can have 100% coverage and miss bugs.

## Fixing Flaky Tests

If a test is flaky:
1. Identify the source of non-determinism (time, random, async, order).
2. Fix the root cause; don't add retries or sleeps.
3. Common fixes: mock time, seed random, await properly, isolate state.

## Output

- Tests added/modified (with file paths).
- Coverage change (if measurable).
- What behaviours are now protected.
- Any gaps that need follow-up tests.