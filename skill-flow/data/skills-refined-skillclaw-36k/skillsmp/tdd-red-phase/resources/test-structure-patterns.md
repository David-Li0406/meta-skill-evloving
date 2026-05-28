# Test Structure Patterns
**Version:** {{VERSION}}

Patterns for organizing and structuring tests in the RED phase of TDD.

---

## Arrange-Act-Assert (AAA)

The most common test structure pattern. Each test has three distinct sections.

### Structure

```python
def test_user_creation():
    # Arrange - Set up test data and conditions
    email = "test@example.com"
    name = "Test User"

    # Act - Execute the code being tested
    user = create_user(email, name)

    # Assert - Verify the expected outcome
    assert user.email == email
    assert user.name == name
```

### Guidelines
- **Arrange:** Minimal setup needed for this specific test
- **Act:** Single action being tested (usually one line)
- **Assert:** Clear verification of expected behavior

### Benefits
- Easy to read and understand
- Clear separation of concerns
- Identifies what's being tested

---

## Given-When-Then (GWT)

BDD-style structure that reads like a specification.

### Structure

```python
def test_authenticated_user_can_view_profile():
    # Given - Preconditions
    user = create_authenticated_user()

    # When - Action taken
    response = view_profile(user)

    # Then - Expected outcome
    assert response.status == 200
    assert response.data["name"] == user.name
```

### When to Use
- Tests that describe business behavior
- Acceptance tests
- When non-developers need to understand tests

### Mapping to AAA
| Given | → | Arrange |
| When | → | Act |
| Then | → | Assert |

---

## Test Naming Conventions

### Pattern: `test_[unit]_[scenario]_[expected]`

```python
# Good names
test_user_with_invalid_email_raises_error
test_cart_with_items_calculates_total
test_login_with_wrong_password_fails

# Bad names
test_user()
test_1()
test_it_works()
```

### Alternative: `should_[expected]_when_[scenario]`

```python
should_raise_error_when_email_invalid
should_calculate_total_when_cart_has_items
should_fail_when_password_wrong
```

### Naming Guidelines

| Do | Don't |
|----|-------|
| Describe the behavior | Use generic names |
| Include the condition | Use numbers/abbreviations |
| State expected outcome | Say "test" in the name |
| Be specific | Be vague |

---

## Test File Organization

### One Test Class Per Unit

```
tests/
├── test_user.py          # User model tests
├── test_order.py         # Order model tests
├── test_payment.py       # Payment service tests
└── test_api_users.py     # User API endpoint tests
```

### Group by Feature

```
tests/
├── authentication/
│   ├── test_login.py
│   ├── test_logout.py
│   └── test_registration.py
├── orders/
│   ├── test_create_order.py
│   └── test_cancel_order.py
```

---

## Test Suite Structure

### Within a Test File

```python
class TestUserCreation:
    """Tests for user creation functionality"""

    def test_creates_user_with_valid_data(self):
        ...

    def test_raises_error_with_invalid_email(self):
        ...

    def test_raises_error_with_duplicate_email(self):
        ...


class TestUserAuthentication:
    """Tests for user authentication"""

    def test_authenticates_with_correct_password(self):
        ...

    def test_fails_with_wrong_password(self):
        ...
```

### Grouping Principles
- Group related tests together
- One concept per test class
- Shared setup in fixtures/setUp

---

## Quick Reference

| Pattern | Use When |
|---------|----------|
| AAA | Default choice, most tests |
| GWT | BDD, business-focused tests |
| One class per unit | Unit tests |
| Group by feature | Integration/E2E tests |

### Test Name Formula
```
test_[what]_[condition]_[result]
```

### File Name Formula
```
test_[module_or_feature].py
```
