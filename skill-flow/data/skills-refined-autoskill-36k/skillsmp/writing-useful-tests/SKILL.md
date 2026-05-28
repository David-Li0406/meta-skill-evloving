---
name: writing-useful-tests
description: Use when writing tests, reviewing test code, or discussing testing strategy. Covers TDD workflow, test structure, mocking strategy, property-based testing, and pytest patterns.
---

# Writing Useful Tests

## Overview

Tests exist to enable safe refactoring. A test that breaks when you refactor implementation (without changing behavior) is worse than no test. Write tests. Not too many. Mostly integration — they provide better confidence-to-cost ratios than unit tests alone. Test code deserves the same quality bar as production code.

## When to Use

- Writing new tests or test files
- Reviewing test code for quality
- Debugging flaky or brittle tests
- Deciding what level of test to write
- Setting up mocks or fixtures

## Core Pattern

### TDD Workflow

1. **Create test file with empty cases.** Stub out test function names describing expected behaviors before writing any implementation.
2. **Red phase.** Write the minimum test code to make one test fail. The failure message should clearly indicate what behavior is missing.
3. **Green phase.** Write the minimum implementation to make the test pass. Resist adding code beyond what the test requires.
4. **Refactor.** Clean up implementation while keeping tests green.
5. **Repeat.** Move to the next empty test case.

### Test Structure: Arrange, Act, Assert

```python
def test_registration_sends_email_to_provided_address():
    # Arrange
    email_service = FakeEmailService()
    user_service = UserService(email_service=email_service)

    # Act
    user_service.register(email="new@example.com")

    # Assert
    assert email_service.sent_to("new@example.com")
```

One behavior, one assertion, descriptive name. A separate test verifies subject line content.

### Test Pyramid

Favor integration tests when practical — they verify real behavior across boundaries:

| Level | When to Use |
|-------|-------------|
| Unit | Pure logic, fast feedback, complex branching |
| Integration | Database queries, API boundaries, file I/O — prefer these |
| E2E | Critical user journeys only; expensive to maintain |

If an integration test can verify the behavior with acceptable speed, prefer it over a unit test with extensive mocking.

## Property-Based Testing

Property-based testing generates random inputs to verify invariants rather than testing specific examples. Use it for serialization pairs, pure functions with clear contracts, validators, and normalizers.

### When to Use Property-Based Testing

| Use Property-Based | Use Example-Based |
|-------------------|-------------------|
| Encode/decode pairs, serialization | Specific user scenarios |
| Pure functions with mathematical properties | UI and integration flows |
| Validators and normalizers | Business logic with specific edge cases |
| Sorting, filtering, transformations | Code without obvious properties |

### Property Hierarchy (Strongest to Weakest)

| Property | Pattern | Example |
|----------|---------|---------|
| **Roundtrip** | `decode(encode(x)) == x` | JSON, base64, compression |
| **Idempotence** | `f(f(x)) == f(x)` | Normalization, formatting, deduplication |
| **Invariant** | Quantity preserved | Length, count, sum unchanged |
| **Commutativity** | `f(a,b) == f(b,a)` | Set operations, addition |
| **Oracle** | `new_impl(x) == reference(x)` | Refactoring verification |
| **Verifiability** | `is_sorted(sort(x))` | Easy-to-check outcomes |

### Example: Roundtrip Property

```python
from hypothesis import given
from hypothesis import strategies as st

@given(st.dictionaries(st.text(), st.integers()))
def test_json_roundtrip(data):
    # Roundtrip: decode(encode(x)) == x
    encoded = json.dumps(data)
    decoded = json.loads(encoded)
    assert decoded == data
```

### Example: Invariant Property

```python
@given(st.lists(st.integers()))
def test_sort_preserves_elements(xs):
    sorted_xs = sorted(xs)
    # Invariants: length preserved, elements preserved
    assert len(sorted_xs) == len(xs)
    assert sorted(sorted_xs) == sorted(xs)
```

### Property-Based Testing Anti-Patterns

- **Tautological assertions** — Testing that `f(x) == f(x)` proves nothing
- **Reimplementing the function** — If your property duplicates the implementation, you're not testing
- **Excessive filtering** — If most generated inputs are discarded, constrain the generator instead

## Mocking Strategy

**You don't hate mocks; you hate side-effects.** Mocking difficulty reveals where side-effects complicate your design.

### Managed vs Unmanaged Dependencies

| Type | Examples | Approach |
|------|----------|----------|
| Managed | Databases, filesystems, local services | Use real instances |
| Unmanaged | External APIs, payment processors, email | Mock these |

Communications with managed dependencies are implementation details. Communications with unmanaged dependencies are observable behavior worth testing.

### Don't Mock What You Don't Own

Create thin wrappers around third-party libraries. Mock your wrapper, not the library directly.

```python
# Good — mock your wrapper
class StripeClient:
    def charge(self, amount: int) -> ChargeResult: ...

def test_order_charges_correct_amount(mocker):
    mock_stripe = mocker.Mock(spec=StripeClient)
    mock_stripe.charge.return_value = ChargeResult(success=True)
    # test uses mock_stripe

# Bad — mocking stripe library internals directly
def test_order_charges(mocker):
    mocker.patch("stripe.Charge.create", ...)  # brittle to library changes
```

### Mocking Anti-Patterns

- **Testing mock behavior** — If you're asserting on mock return values, you're testing the mock
- **Incomplete mocks** — Mirror real API structure; downstream code will break on missing fields
- **Mock setup longer than test** — Consider integration testing with real components instead

## Test Isolation

Tests should not depend on execution order, but isolation does not require cleaning everything.

### What to Clean Up

Long-lived resources that cost money or block other tests:
- Cloud resources (VMs, storage, Databricks clusters/jobs)
- Kubernetes deployments, pods
- Background processes

Prefer using the product's own cleanup mechanisms when available.

### What's Fine to Leave

- Database records (use unique test IDs instead of pristine state)
- Logs and cached data that expires naturally
- Test artifacts in temp directories

```python
# Prevent order dependencies with unique IDs
test_id = f"test-{uuid.uuid4().hex[:8]}"
user = create_user(email=f"{test_id}@test.com")
```

## Red Flags

Warning signs that tests need attention:

- Mock setup longer than test logic
- Tests that break when you refactor (without changing behavior)
- Arbitrary timeouts without timing-related reasons
- Mocking everything to make a test pass
- Tests with unclear success criteria

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Testing implementation details | Breaks on refactor | Test observable behavior only |
| Multiple behaviors per test | Unclear which failed | One behavior, one assertion focus |
| Sloppy test code | Erodes trust | Same quality bar as production |
| Mocking managed dependencies | False confidence | Use real databases, filesystems |
| Skipping red phase | Test may never fail | Verify failure before implementing |

## Anti-Rationalizations

- "I'll add tests later" — You will not. TDD is faster than debugging untested code.
- "Mocking is too much work" — Difficulty mocking signals tight coupling. Fix the design.
- "I need a unit test for speed" — If the integration test is fast enough, prefer it for confidence.
- "Cleanup is too hard" — Use unique test IDs; you don't need pristine state.

## Supporting References

- [hypothesis-reference.md](hypothesis-reference.md) — Library-specific patterns for Hypothesis (Python)

## Summary

1. **TDD: empty cases → red → green.** Write test names first, fail one, implement until green.
2. **Test behavior, not implementation.** Assert outputs and side effects, never internal state.
3. **Prefer integration tests.** They verify real behavior; mock only unmanaged external dependencies.
4. **One behavior per test.** Descriptive name, single assertion focus, precise failure message.
5. **Use property-based testing for invariants.** Roundtrip, idempotence, and preservation properties catch edge cases you won't think of.
