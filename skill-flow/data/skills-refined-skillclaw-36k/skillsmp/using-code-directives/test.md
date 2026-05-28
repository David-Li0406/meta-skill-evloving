# @test Directive

## Purpose

`@test` directives specify test requirements for code. After implementing the test, the directive is always removed.

## Syntax

```javascript
// @test: Should handle empty input gracefully

/* @test
 Test cases needed:
 - Valid email returns true
 - Invalid format returns false
 - Empty string returns false
 - Null/undefined throws error
*/

# @test: Add test for edge case with negative numbers
```

**Format:**
- Short form: `// @test: Brief test requirement`
- Long form: Multi-line with test case list

## Step-by-Step Procedure

### 1. Read Full Context

**Understand what needs testing:**
- What function/class needs tests?
- What behavior should be verified?
- What edge cases exist?
- What test framework is used?

**Check existing tests:**
- Is there a test file already?
- What patterns are used?
- What test utilities are available?

### 2. Decide on Test Approach

**Choose based on directive location:**

#### Case A: Directive next to implementation
```javascript
function validateEmail(email) {
  // @test: Valid email returns true, invalid returns false
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```
**Approach:** Write unit test in test file

#### Case B: Directive in test file
```javascript
// tests/validation.test.js
describe('validateEmail', () => {
  // @test: Add test case for international domains (.co.uk, .com.au)
  it('validates standard email', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });
});
```
**Approach:** Add test case to existing suite

#### Case C: Directive describes missing test coverage
```python
# @test: Need integration test for database connection retry logic
class DatabaseConnection:
    def connect(self):
        # ...retry logic...
```
**Approach:** Create new integration test file if needed

### 3. Write the Test

**Write test for the code:**
1. Understand current behavior (read the implementation)
2. Write test cases that verify behavior
3. Cover edge cases and error conditions
4. Ensure test is comprehensive

**Test quality checklist:**
- [ ] Test has clear name describing what it verifies
- [ ] Test is isolated (doesn't depend on other tests)
- [ ] Test covers the specified requirement
- [ ] Test uses appropriate assertions
- [ ] Test follows project conventions

### 4. Run the Test

**Verify test works:**
```bash
# Run specific test file
npm test -- validation.test.js
pytest tests/test_validation.py
cargo test validation
```

**Ensure:**
- Test passes when behavior is correct
- Test fails when behavior is broken (verify by temporarily breaking code)

### 5. Remove the Directive

**After test is implemented and passing:**
- Remove the `@test` comment completely
- The test file is the documentation
- Don't keep completed `@test` directives

## Examples

### Example 1: Add Unit Test

**Before:**
```typescript
// src/utils/validation.ts
export function isValidEmail(email: string): boolean {
  // @test: Should validate standard email formats
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

**Process:**
1. Check for test file: `tests/utils/validation.test.ts`
2. Determine test framework: Jest (based on other tests)
3. Write test cases

**After:**
```typescript
// src/utils/validation.ts (directive removed)
export function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// tests/utils/validation.test.ts (new file or added to existing)
import { isValidEmail } from '../../src/utils/validation';

describe('isValidEmail', () => {
  it('validates standard email formats', () => {
    expect(isValidEmail('user@example.com')).toBe(true);
    expect(isValidEmail('name.surname@company.co.uk')).toBe(true);
  });

  it('rejects invalid formats', () => {
    expect(isValidEmail('notanemail')).toBe(false);
    expect(isValidEmail('@example.com')).toBe(false);
    expect(isValidEmail('user@')).toBe(false);
  });

  it('handles empty string', () => {
    expect(isValidEmail('')).toBe(false);
  });
});
```

### Example 2: Add Edge Case Test

**Before:**
```python
# tests/test_parser.py
def test_parse_numbers():
    assert parse_numbers("1,2,3") == [1, 2, 3]
    # @test: Add test for negative numbers and decimals
```

**After:**
```python
# tests/test_parser.py (directive removed)
def test_parse_numbers():
    assert parse_numbers("1,2,3") == [1, 2, 3]

def test_parse_negative_numbers():
    assert parse_numbers("-1,-2,-3") == [-1, -2, -3]

def test_parse_decimal_numbers():
    assert parse_numbers("1.5,2.5,3.5") == [1.5, 2.5, 3.5]
```

### Example 3: Integration Test

**Before:**
```rust
// @test: Integration test for retry logic with mock server
impl ApiClient {
    async fn fetch_with_retry(&self, url: &str) -> Result<Response> {
        // ...retry logic...
    }
}
```

**After:**
```rust
// Implementation (directive removed)
impl ApiClient {
    async fn fetch_with_retry(&self, url: &str) -> Result<Response> {
        // ...retry logic...
    }
}

// tests/integration_test.rs (new test)
#[tokio::test]
async fn test_fetch_with_retry_logic() {
    let mock_server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/api/data"))
        .respond_with(ResponseTemplate::new(503)) // First attempt fails
        .expect(1)
        .mount(&mock_server)
        .await;

    Mock::given(method("GET"))
        .and(path("/api/data"))
        .respond_with(ResponseTemplate::new(200)) // Second attempt succeeds
        .expect(1)
        .mount(&mock_server)
        .await;

    let client = ApiClient::new();
    let result = client.fetch_with_retry(&format!("{}/api/data", &mock_server.uri())).await;

    assert!(result.is_ok());
}
```

### Example 4: Multiple Test Cases

**Before:**
```javascript
/* @test
 Test cases needed:
 - Returns user when found
 - Returns null when not found
 - Throws error on invalid ID format
 - Caches result on second call
*/
async function getUser(id) {
  // ...implementation...
}
```

**After:**
```javascript
// Implementation (directive removed)
async function getUser(id) {
  // ...implementation...
}

// tests/user.test.js
describe('getUser', () => {
  it('returns user when found', async () => {
    const user = await getUser('user-123');
    expect(user).toEqual({ id: 'user-123', name: 'Test User' });
  });

  it('returns null when not found', async () => {
    const user = await getUser('nonexistent');
    expect(user).toBeNull();
  });

  it('throws error on invalid ID format', async () => {
    await expect(getUser('')).rejects.toThrow('Invalid ID');
    await expect(getUser(null)).rejects.toThrow('Invalid ID');
  });

  it('caches result on second call', async () => {
    const fetchSpy = jest.spyOn(api, 'fetch');

    await getUser('user-123'); // First call
    await getUser('user-123'); // Second call

    expect(fetchSpy).toHaveBeenCalledTimes(1); // Only fetched once
  });
});
```

## Decision Tree

```
@test directive found
  ↓
Test file exists for this code?
  YES → Add to existing test suite
  NO → Create new test file
  ↓
Write test(s) for the code following project conventions
  ↓
Run tests
  ↓
All tests pass?
  NO → Fix implementation or test
  YES → Remove @test directive
```

## Common Mistakes

### ❌ Removing directive before test is written
```javascript
// ❌ BAD: Directive removed but no test exists
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```
✅ Fix: Write test, then remove directive.

### ❌ Writing weak tests that always pass
```javascript
// ❌ BAD: Test doesn't actually verify behavior
it('validates email', () => {
  expect(validateEmail).toBeDefined();
});
```
✅ Fix: Write meaningful assertions that verify actual behavior.

### ❌ Keeping @test directive after test is added
```python
# ❌ BAD
# @test: Test edge cases [DONE]
def validate_email(email):
    ...
```
✅ Fix: Always remove @test directives when tests are implemented.

### ❌ Not running the test
```rust
// ❌ BAD: Wrote test but never ran it to verify it works
```
✅ Fix: Always run tests and verify they pass.

## When to Ask for Clarification

**Ask user if:**
- Test framework/tools are unclear from codebase
- Multiple test approaches are valid (unit vs integration)
- Test requires external dependencies (database, API)
- Directive is ambiguous about what to test

## Why Always Remove?

**@test directives are one-time actions:**
- Once test exists, the test file is the documentation
- Keeping directive creates confusion (is test written or not?)
- Test code is self-documenting

**If more tests are needed later:**
- Add a new @test directive when the need arises
- Don't accumulate old completed directives
