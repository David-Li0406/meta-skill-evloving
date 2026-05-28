---
name: tdd-workflow
description: Use this skill when engaging in test-driven development (TDD), refactoring code, or writing tests to ensure code quality and maintainability.
---

# TDD Workflow - 测试驱动开发

This skill outlines the test-driven development (TDD) process, emphasizing the red-green-refactor cycle to maintain code quality.

## Core Cycle: RED-GREEN-REFACTOR

```
┌─────────┐    ┌─────────┐    ┌─────────┐
│   RED   │ -> │  GREEN  │ -> │ REFACTOR│
│ Write a │    │ Make the│    │ Optimize│
│ failing  │    │ test pass│    │ the code│
└─────────┘    └─────────┘    └─────────┘
     │                              │
     └──────────────┬───────────────┘
                    │
                    ▼
              Repeat Cycle
```

### Step 1: RED (Write a Failing Test)

- Write a test that must fail.
- The test should describe the desired **behavior**, not the implementation.
- Ensure the reason for failure is correct (not a syntax error).

```javascript
// ❌ Incorrect: Write code first
function add(a, b) { return a + b; }
test('add works', () => {});  // No assertion

// ✅ Correct: Write the test first
test('add returns sum of two numbers', () => {
  expect(add(2, 3)).toBe(5);
});
// Run: The test fails (add does not exist)
```

### Step 2: GREEN (Make the Test Pass)

- Write the **minimum** code necessary to make the test pass.
- Avoid writing code beyond what is required for the test.
- **Ugly code is allowed**; the goal is to pass the test.

```javascript
// Quickly make the test pass (even if ugly)
function add(a, b) {
  return 5;  // Hardcoded, but the test passes
}
```

### Step 3: REFACTOR (Optimize the Code)

- Once the test passes, optimize the implementation.
- **Keep the tests passing**.
- Extract functions, eliminate duplication, and improve naming.

```javascript
// Refactor to the correct implementation
function add(a, b) {
  return a + b;
}
// The test still passes ✅
```

---

## Testing Principles

### 1. One Test Validates One Thing

```javascript
// ❌ Incorrect: Testing multiple behaviors
test('user operations', () => {
  user.setName('Alice');
  expect(user.name).toBe('Alice');
  user.save();
  expect(user.id).toBeDefined();
});

// ✅ Correct: Separate tests
test('setName updates name', () => {
  user.setName('Alice');
  expect(user.name).toBe('Alice');
});

test('save assigns id', () => {
  user.save();
  expect(user.id).toBeDefined();
});
```

### 2. Test Behavior, Not Implementation

```javascript
// ❌ Incorrect: Testing internal implementation
test('uses cache', () => {
  expect(user.cache.get).toHaveBeenCalled();
});

// ✅ Correct: Test observable behavior
test('returns cached data without fetch', () => {
  const first = user.getData();
  const second = user.getData();
  expect(second).toEqual(first);
  expect(fetch).not.toHaveBeenCalled();
});
```

### 3. Use Given-When-Then Structure

```javascript
test('user can withdraw funds', () => {
  // Given: Account has 100
  account.balance = 100;

  // When: Withdraw 30
  account.withdraw(30);

  // Then: Balance is 70
  expect(account.balance).toBe(70);
});
```

---

## Refactoring Safety Net

### Pre-refactoring Checklist

- [ ] All tests pass
- [ ] Current test coverage is sufficient
- [ ] Refactoring goals are clear

### Rules During Refactoring

1. **Small Steps**: Change one thing at a time.
2. **Frequent Testing**: Test immediately after each change.
3. **Stop on Failure**: Do not continue modifying code when tests fail.

```bash
# Safe refactoring process
npm test                    # 1. Confirm tests pass
# Make small changes
npm test                    # 2. Confirm again
# Continue or roll back
```

### Coverage Requirement

- All new features, bug fixes, and refactoring must achieve **80% or higher test coverage**.

## Testing Types

### 1. Unit Tests
```rust
#[test]
fn test_validate_formula_name() {
    assert!(validate_formula_name("测试配方").is_ok());
    assert!(validate_formula_name("").is_err());
}
```

### 2. Integration Tests
```rust
#[tokio::test]
async fn test_create_formula_integration() {
    let pool = setup_test_db().await;
    let repo = FormulaRepository::new(Arc::new(pool));

    let dto = CreateFormulaDto {
        name: "测试配方".to_string(),
        species_code: "PIG".to_string(),
    };

    let result = repo.create(dto).await;
    // Add assertions here
}
```