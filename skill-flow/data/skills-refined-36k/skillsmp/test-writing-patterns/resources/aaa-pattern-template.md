# AAA Pattern Template
**Version:** {{VERSION}}

Template and examples for the Arrange-Act-Assert test structure pattern.

## Basic AAA Template

```
test_[unit]_[scenario]_[expected]:
    // ===== ARRANGE =====
    [Set up test data and preconditions]
    [Create required objects]
    [Configure dependencies]

    // ===== ACT =====
    [Execute the behavior being tested]

    // ===== ASSERT =====
    [Verify the expected outcome]
    [Check side effects if applicable]
```

---

## Detailed AAA Sections

### ARRANGE Section

**Purpose:** Set up everything needed for the test

**Common activities:**
- Create test data
- Initialize objects under test
- Configure mocks/stubs
- Set up database state
- Create test fixtures
- Define expected values

**Guidelines:**
- Use explicit, meaningful test data
- Keep setup minimal (only what's needed)
- Make test data intention-revealing
- Avoid hidden dependencies

**Example (conceptual):**
```
ARRANGE:
    user_data = {name: "Alice", role: "admin"}
    expected_result = UserObject(name="Alice", role="admin", active=true)
    mock_database = create_mock()
    service = UserService(database=mock_database)
```

### ACT Section

**Purpose:** Execute the specific behavior being tested

**Characteristics:**
- Usually one line (or one logical action)
- Calls the function/method under test
- Captures result for assertion
- Should be obvious what's being tested

**Guidelines:**
- Keep it simple and focused
- One action per test
- Clearly captures return value or outcome
- Sometimes includes expected exception

**Example (conceptual):**
```
ACT:
    result = service.create_user(user_data)
```

### ASSERT Section

**Purpose:** Verify expected outcome occurred

**Common verifications:**
- Return value matches expectation
- Object state changed correctly
- Side effects occurred (or didn't)
- Exceptions thrown (or not)
- Mock interactions verified

**Guidelines:**
- Specific assertions (not generic "assert true")
- Include helpful failure messages
- Test observable behavior
- Assert on outcomes, not implementation

**Example (conceptual):**
```
ASSERT:
    assert result == expected_result
    assert mock_database.insert_called_with(user_data)
    assert result.active == true
```

---

## AAA Pattern Examples

### Example 1: Simple Function Test

```
test_add_function_with_positive_numbers_returns_sum:
    // ARRANGE
    a = 2
    b = 3
    expected = 5

    // ACT
    result = add(a, b)

    // ASSERT
    assert result == expected
```

### Example 2: Object Method Test

```
test_user_can_update_own_profile:
    // ARRANGE
    user = create_user(id=1, name="Alice")
    new_data = {name: "Alice Smith"}

    // ACT
    success = user.update_profile(new_data)

    // ASSERT
    assert success == true
    assert user.name == "Alice Smith"
```

### Example 3: API Endpoint Test

```
test_get_user_endpoint_returns_user_data:
    // ARRANGE
    user_id = 123
    expected_user = {id: 123, name: "Alice"}
    mock_db.set_user(user_id, expected_user)
    client = create_test_client()

    // ACT
    response = client.get(f"/users/{user_id}")

    // ASSERT
    assert response.status_code == 200
    assert response.json() == expected_user
```

### Example 4: Exception Testing

```
test_divide_by_zero_raises_exception:
    // ARRANGE
    numerator = 10
    denominator = 0

    // ACT & ASSERT (combined for exception testing)
    assert_raises(DivisionByZeroError):
        divide(numerator, denominator)
```

### Example 5: Mock Verification

```
test_send_email_calls_email_service:
    // ARRANGE
    mock_email_service = create_mock()
    notification_service = NotificationService(mock_email_service)
    user_email = "alice@example.com"
    message = "Welcome!"

    // ACT
    notification_service.send_welcome_email(user_email, message)

    // ASSERT
    mock_email_service.verify_called_once_with(
        to=user_email,
        subject="Welcome",
        body=message
    )
```

---

## AAA Pattern Variations

### Minimal AAA (Very Simple Tests)

```
test_is_even_with_even_number:
    result = is_even(4)  // Act inline
    assert result == true
```

**Use when:** Test is trivially simple, no setup needed

### Extended AAA (Complex Setup)

```
test_complex_workflow:
    // ARRANGE
    database = setup_test_database()
    seed_test_data(database)
    cache = setup_test_cache()
    config = load_test_config()
    service = create_service(database, cache, config)
    expected_outcome = calculate_expected_result()

    // ACT
    result = service.execute_complex_workflow()

    // ASSERT
    assert result.status == "success"
    assert result.data == expected_outcome
    verify_database_state(database)
    verify_cache_updated(cache)

    // CLEANUP (sometimes needed)
    database.close()
    cache.clear()
```

**Use when:** Setup is complex, multiple verifications needed

---

## Common AAA Mistakes

### Mistake 1: Mixing Act and Assert

**Wrong:**
```
result = function() // Act
assert result > 0   // Assert
another_result = other_function() // More Act?
assert another_result == true
```

**Right:**
```
// ACT
result = function()
another_result = other_function()

// ASSERT
assert result > 0
assert another_result == true
```

### Mistake 2: Too Much in Arrange

**Wrong:**
```
// ARRANGE (doing too much)
setup_database()
populate_users()
configure_cache()
initialize_services()
warm_up_connections()
pre_calculate_values()
// ... 50 more lines
```

**Right:**
- Extract to setup fixtures
- Use test data builders
- Keep only relevant setup in test

### Mistake 3: Multiple Acts

**Wrong:**
```
// ACT
result1 = do_thing_one()
result2 = do_thing_two()
result3 = do_thing_three()
```

**Right:**
- One test per action
- Split into three separate tests
- Each tests one behavior

---

## AAA Quick Reference

**ARRANGE:**
- What: Set up test conditions
- Goal: Prepare everything needed
- Keep: Minimal and clear

**ACT:**
- What: Execute behavior being tested
- Goal: One clear action
- Keep: Simple and obvious

**ASSERT:**
- What: Verify expected outcome
- Goal: Prove behavior correct
- Keep: Specific and meaningful

---

**Use AAA pattern for consistent, readable tests**
