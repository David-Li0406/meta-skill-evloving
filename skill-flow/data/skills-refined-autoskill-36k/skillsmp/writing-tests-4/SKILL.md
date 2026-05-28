---
name: writing-tests 
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
---

# Test Desiderata 2.0 - Properties of Valuable Tests

## Purpose

Guide the writing of high-quality individual tests by understanding which properties matter and how to achieve them.

## When to Use This Skill

- Writing new tests
- Evaluating whether a test is well-written
- Reviewing test code in pull requests
- Improving existing tests
- Making trade-off decisions when writing tests
- Debugging why tests are hard to maintain or unreliable

## Core Philosophy

**Not all tests need all properties.** Think of test properties as sliders, not checkboxes. The key is understanding which properties matter most for your specific test and making conscious trade-offs.

**Every property has a cost.** Optimize for the properties that deliver the most value for your test suite's goals.

## Four Macro Goals (Test Suite Level)

Every test suite should aim to achieve these four macro properties:

### 1. Predict Success in Production

The suite tells you if your software will work in production before you deploy it.

**How tests support this:**

- Cover critical paths and edge cases
- Test realistic scenarios
- Verify both functional behavior and non-functional qualities

### 2. Fast Feedback

Developers get results in seconds or minutes, not hours.

**How tests support this:**

- Run quickly (unit tests in ms, integration in seconds)
- Run in any order
- Can run in parallel
- Use minimal test data

### 3. Support Ongoing Code Design Changes

Tests enable refactoring and evolution without breaking.

**How tests support this:**

- Test behavior, not implementation
- Remain relevant as code changes
- Provide design pressure toward better code
- Stay organized and easy to locate

### 4. Minimize Total Cost of Ownership

Tests are cheap to write, run, and maintain over time.

**How tests support this:**

- Automated and deterministic
- Easy to read, write, and update
- Fast to diagnose failures
- Resilient to non-breaking changes

## Individual Test Properties

For each property below, we show:

- What it means
- Why it matters (which macro goal it serves)
- How to achieve it
- Trade-offs to consider

### Properties for "Predict Success in Production"

#### Sensitive to Behavior

**What:** Test fails when behavior changes in a way users care about. Test passes when behavior is correct.

**Why:** This is the fundamental purpose of a test - catch real problems.

**How to achieve:**

```python
# Good - tests observable behavior
def test_order_total_includes_tax():
    order = Order(items=[Item(price=100)])
    total = order.calculate_total(tax_rate=0.1)
    assert total == 110  # User-visible result

# Bad - tests implementation details
def test_order_calls_tax_calculator():
    order = Order(items=[Item(price=100)])
    with mock.patch('tax_calculator') as mock_calc:
        order.calculate_total(tax_rate=0.1)
        mock_calc.assert_called_once()  # Testing how, not what
```

**Trade-offs:**

- More behavioral = less tied to implementation = more maintainable
- Too high-level behavioral tests = slower, harder to pinpoint failures

### Properties for "Fast Feedback"

#### Minimal Data

**What:** Test uses the smallest amount of data needed to verify the behavior.

**Why:** Less data = faster tests, easier to understand, simpler to maintain.

**How to achieve:**

```python
# Good - minimal data
def test_user_can_update_email():
    user = User(id=1, email="old@example.com")
    user.update_email("new@example.com")
    assert user.email == "new@example.com"

# Bad - excessive data
def test_user_can_update_email():
    user = User(
        id=1,
        email="old@example.com",
        name="Alice Smith",
        address="123 Main St",
        phone="555-1234",
        created_at=datetime(2020, 1, 1),
        preferences={"theme": "dark", "language": "en"},
        # ... 20 more fields
    )
    user.update_email("new@example.com")
    assert user.email == "new@example.com"
```

**Trade-offs:**

- Too minimal = might miss requirements about what fields are needed
- Realistic data fixtures can improve test readability

#### Run in Any Order (Isolated)

**What:** Test produces same result regardless of which other tests run before/after it.

**Why:** Enables running subset of tests, parallel execution, and reliable results.

**How to achieve:**

```python
# Good - isolated
def test_create_user():
    db = create_test_database()  # Fresh state each time
    user = User(email="test@example.com")
    db.save(user)
    assert db.count_users() == 1
    db.cleanup()  # Clean up after yourself

# Bad - depends on other tests
_test_user = None  # Shared state!

def test_create_user():
    global _test_user
    _test_user = User(email="test@example.com")
    db.save(_test_user)

def test_delete_user():  # Depends on test_create_user running first!
    global _test_user
    db.delete(_test_user)
```

**Trade-offs:**

- Perfect isolation = more setup code
- Some shared fixtures are OK if truly read-only

#### Run in Parallel

**What:** Can run multiple copies of the test simultaneously without interference.

**Why:** Enables fast test suite execution through parallelization.

**How to achieve:**

- Use unique database schemas/tables per test
- Use random ports for servers
- Don't share file system state
- Use test-specific queue names

**Trade-offs:**

- Requires more infrastructure
- Some integration tests can't be parallelized (limited resources)

### Properties for "Minimize Cost of Ownership"

#### Automated

**What:** Test runs without human intervention. No manual steps.

**Why:** Humans are slow, make mistakes, and don't like repetitive work.

**How to achieve:**

- All setup in code, no manual configuration
- Assertions handled by test framework
- Runs in CI pipeline
- No "check the logs to see if it passed"

**Trade-offs:**

- Initial setup time
- Some exploratory testing still valuable

#### Deterministic

**What:** Given the same code, test always produces the same result (pass or fail).

**Why:** Flaky tests destroy confidence and waste debugging time.

**How to achieve:**

```python
# Good - deterministic
def test_calculate_age():
    birth_date = datetime(1990, 1, 1)
    reference_date = datetime(2020, 1, 1)
    age = calculate_age(birth_date, reference_date)
    assert age == 30

# Bad - non-deterministic
def test_calculate_age():
    birth_date = datetime(1990, 1, 1)
    age = calculate_age(birth_date)  # Uses current date - changes daily!
    assert age > 0  # Weak assertion
```

**Common sources of non-determinism:**

- Current time/date without mocking
- Random values without seeding
- Network calls without stubbing
- Race conditions in async code
- Floating point arithmetic

**Trade-offs:**

- Mocking time/randomness adds complexity
- Sometimes acceptable in specific test types (chaos testing)

#### Diagnosable (Specific)

**What:** When test fails, you immediately know what went wrong and where to look.

**Why:** Reduces debugging time, speeds up fixes.

**How to achieve:**

```python
# Good - specific, diagnosable failure
def test_discount_code_SUMMER20_gives_20_percent_off():
    product = Product(price=100)
    order = Order(items=[product], discount_code="SUMMER20")

    assert order.discount_amount == 20
    assert order.total == 80

# Bad - vague failure
def test_order_processing():
    # ... 50 lines of setup ...
    result = process_order(complex_order_data)
    assert result.success == True  # Which part failed?
```

**Techniques:**

- Descriptive test names
- Clear assertion messages
- One logical assertion per test
- Avoid generic assertions like `assert x` or `assert result.success`

**Trade-offs:**

- More specific = more tests
- Balance with maintainability

#### Easy to Read

**What:** Anyone can understand what the test does and why, quickly.

**Why:** Code is read more than written. Others need to maintain your tests.

**How to achieve:**

```python
# Good - readable
def test_premium_user_gets_free_shipping():
    user = create_premium_user()
    order = Order(items=[Item(price=10)])

    shipping_cost = calculate_shipping(order, user)

    assert shipping_cost == 0

# Bad - unclear
def test_calc():
    u = User(premium=True)
    o = Order(items=[Item(10)])
    sc = calc_ship(o, u)
    assert sc == 0
```

**Readability practices:**

- Use Arrange-Act-Assert structure
- Descriptive variable names
- Helper functions for complex setup (but don't hide the test logic)
- Comments only when truly necessary

**Trade-offs:**

- Some duplication is OK for readability
- Don't over-abstract

#### Easy to Update

**What:** When requirements change, updating the test is straightforward.

**Why:** Requirements change frequently. Tests must evolve with them.

**How to achieve:**

- Avoid brittle selectors (CSS classes that change)
- Use test data builders for complex objects
- Centralize test data creation
- Test high-level behavior, not low-level details

```python
# Good - easy to update
def test_user_registration_flow():
    user_data = build_valid_user()  # Centralized builder
    response = register_user(user_data)
    assert response.success == True

# Bad - hard to update
def test_user_registration_flow():
    # If we add a required field, this breaks everywhere
    response = register_user({
        "email": "test@example.com",
        "password": "secret123",
        "name": "Alice"
    })
    assert response.success == True
```

**Trade-offs:**

- Abstractions help but can obscure test logic
- Need balance between DRY and clarity

#### Easy to Write

**What:** Writing a new test doesn't require extensive setup or boilerplate.

**Why:** Low friction = more tests written = better coverage.

**How to achieve:**

- Good test frameworks and tooling
- Reusable test fixtures
- Test data builders
- Clear examples to copy from

**Trade-offs:**

- Too easy = might write unnecessary tests
- Some complex tests are worth the effort

#### Insensitive to Code Structure

**What:** Test doesn't break when you refactor (change internal structure without changing behavior).

**Why:** Tests should enable refactoring, not prevent it.

**How to achieve:**

```python
# Good - structure insensitive
def test_user_can_login():
    response = login("alice@example.com", "password123")
    assert response.success == True
    assert response.user_id is not None

# Bad - structure sensitive
def test_user_can_login():
    # Breaks if we rename LoginService or change its internals
    service = LoginService()
    validator = PasswordValidator()
    authenticator = Authenticator()

    assert service.validator == validator
    assert service.authenticate_internal("alice", "password123")
```

**Key principle:** Test through public APIs, not private implementation.

**Trade-offs:**

- Black-box testing = less granular failure information
- Sometimes need to test components individually

### Properties for "Support Ongoing Code Design"

#### Composable

**What:** Can test different dimensions of variability separately and combine them.

**Why:** Reduces test count. If you have 4 payment methods and 5 shipping options, you need 9 tests, not 20.

**How to achieve:**

```python
# Good - composable
def test_credit_card_payment_succeeds():
    payment = process_payment(amount=100, method="credit_card")
    assert payment.success == True

def test_express_shipping_costs_extra():
    cost = calculate_shipping(method="express")
    assert cost == 20

# Combined coverage: credit_card + express tested separately,
# not every combination

# Bad - all combinations
def test_credit_card_with_express_shipping(): ...
def test_credit_card_with_standard_shipping(): ...
def test_paypal_with_express_shipping(): ...
def test_paypal_with_standard_shipping(): ...
# 20 tests for 4 × 5 combinations!
```

**Trade-offs:**

- Need at least one test of the integrated flow
- Some combinations might have special behavior

#### Documents Intent

**What:** Test serves as documentation of how the system should behave.

**Why:** Tests are always up-to-date documentation (unlike docs that go stale).

**How to achieve:**

- Use business domain language in test names
- Write test cases that reflect user stories
- Group related tests together
- Include examples of edge cases

```python
# Good - documents intent
class TestShoppingCart:
    def test_new_cart_is_empty(self):
        cart = ShoppingCart()
        assert cart.item_count == 0

    def test_adding_item_increases_count(self):
        cart = ShoppingCart()
        cart.add(Item("Book"))
        assert cart.item_count == 1

    def test_cannot_checkout_empty_cart(self):
        cart = ShoppingCart()
        with pytest.raises(EmptyCartError):
            cart.checkout()
```

**Trade-offs:**

- More documentation-like = sometimes more verbose
- Balance clarity with conciseness

#### Durable

**What:** Test remains valuable throughout the product's lifetime. Doesn't become obsolete quickly.

**Why:** Tests are an investment. Want long-term ROI.

**How to achieve:**

- Test stable business rules, not temporary implementation
- Focus on behavior users rely on
- Avoid testing framework internals
- Test at appropriate level of abstraction

**Trade-offs:**

- Some tests for temporary features are OK
- Delete tests when features are removed

#### Necessary (Guide Development)

**What:** Test guides implementation choices. Failing test = missing implementation.

**Why:** Tests should add value, not just check boxes. Each test should prevent or catch a real bug.

**How to achieve:**

- Practice TDD: write test first, it guides the code
- If you can't think of why a test would fail, don't write it
- Delete tests that never fail (except regression tests)

**Trade-offs:**

- Some regression tests are necessary even if rarely fail
- Documentation tests have value beyond catching bugs

#### Organized (Easy to Locate)

**What:** Given a piece of code, you can easily find its tests. Given a test, you can find the code it tests.

**Why:** Speeds up understanding and maintenance.

**How to achieve:**

- Mirror production structure in test structure
- One test file per production file (or logical module)
- Group tests by feature/behavior
- Consistent naming: `test_[production_file].py` or `[ProductionClass]Test.java`

```
src/
  user/
    authentication.py
    profile.py
tests/
  user/
    test_authentication.py
    test_profile.py
```

**Trade-offs:**

- Strict mirroring can be limiting
- Some integration tests span multiple modules

#### Positive Design Pressure

**What:** Writing the test pushes you toward better design decisions.

**Why:** Good design emerges from testability requirements.

**How to achieve (TDD):**

1. Write test first
2. Notice when test is hard to write
3. Simplify design to make test easier
4. Implement to make test pass

**Design improvements from test pressure:**

- Hard to construct object → Use builder or factory
- Many dependencies → Break into smaller classes
- Hard to test method → Extract to separate class
- Brittle test → Improve encapsulation

**Trade-offs:**

- Requires discipline (TDD)
- Can over-engineer if you're not careful

## Making Trade-offs

**Key insight:** You cannot maximize all properties. Some conflict:

**Fast vs Realistic:**

- Mocking makes tests faster but less realistic
- Choose based on test level (unit = fast, E2E = realistic)

**Isolated vs Integrated:**

- Perfect isolation = simpler but less realistic
- Some integration = slower but more confident

**Specific vs Maintainable:**

- Very specific = many tests = harder to maintain
- More general = fewer tests = less precise debugging

### Decision Framework

**For each test, ask:**

1. **What macro goal does this test serve most?**

   - Predict production success → Emphasize behavioral sensitivity
   - Fast feedback → Emphasize speed and isolation
   - Support design → Emphasize structure insensitivity
   - Low cost → Emphasize readability and simplicity

2. **What properties am I willing to sacrifice?**

   - E2E test → Sacrifice speed for realism
   - Unit test → Sacrifice realism for speed and isolation

3. **Is this test pulling its weight?**
   - Does it catch real bugs?
   - Does it guide development?
   - Is it worth the maintenance cost?

## Red Flags: Tests That Need Improvement

**Flaky test (non-deterministic):**

- Fix the root cause (timing, randomness, external dependency)
- If unfixable, delete it (better no test than unreliable test)

**Slow test at wrong level:**

- Can you test this with a unit test instead?
- Are you testing too many combinations?

**Breaks with every refactor (structure sensitive):**

- Test behavior through public API
- Reduce mocking of internal components

**Hard to understand (not readable):**

- Simplify setup
- Use Arrange-Act-Assert
- Better naming
- Extract helper functions

**Passes but catches no bugs (not necessary):**

- Delete it
- Or failing test = you found gap in implementation

## Quick Evaluation Checklist

When reviewing a test, check:

**Macro goal alignment:**

- [ ] Does this test serve a clear macro goal?
- [ ] Is it at the right level (unit/integration/E2E)?

**Critical properties:**

- [ ] Automated?
- [ ] Deterministic?
- [ ] Easy to read?
- [ ] Tests behavior, not implementation?

**Good enough:**

- [ ] Makes conscious trade-offs (not trying to be perfect)?
- [ ] Worth the maintenance cost?
- [ ] Would you want to debug this when it fails?

## Summary

Great tests are the result of understanding:

1. **What you're optimizing for** (four macro goals)
2. **Which properties matter most** for this specific test
3. **Which trade-offs you're making** consciously

No test is perfect. Aim for "good enough to support your team's velocity and confidence while minimizing maintenance burden."

**The real skill:** Knowing which properties to prioritize for each test based on its purpose and level in your test pyramid.
