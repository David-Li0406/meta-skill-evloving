# Test Strategist - Validations

## Weak Assertion - toBeTruthy

### **Id**
weak-assertion-truthy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - expect\(.*\)\.toBeTruthy\(\)
  - expect\(.*\)\.toBeDefined\(\)
  - expect\(.*\)\.not\.toBeNull\(\)
  - expect\(.*\)\.not\.toBeUndefined\(\)
### **Message**
Weak assertion proves existence, not correctness. Assert on specific values.
### **Fix Action**
Replace with specific assertion: expect(result.total).toBe(100) instead of expect(result).toBeTruthy()
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Test Without Assertion

### **Id**
no-assertion-test
### **Severity**
error
### **Type**
regex
### **Pattern**
  - it\(['"][^'"]+['"]\s*,\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{[^}]*\}\s*\)
### **Message**
Test has no assertions. Either add expect() calls or remove the test.
### **Fix Action**
Add assertions that verify the expected behavior, not just that code runs.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js
### **Exceptions**
  - expect\(
  - assert\(
  - should\.

## Hardcoded Future Date

### **Id**
hardcoded-future-date
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new Date\(['"]202[5-9]
  - new Date\(['"]203
  - Date\.parse\(['"]202[5-9]
### **Message**
Hardcoded future date will cause test failures when that date passes.
### **Fix Action**
Use relative dates or freeze time: jest.useFakeTimers(); jest.setSystemTime(new Date('2024-01-15'));
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Sleep/Delay in Test

### **Id**
sleep-in-test
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await\s+new\s+Promise.*setTimeout
  - await\s+sleep\(
  - await\s+delay\(
  - setTimeout\([^,]+,\s*\d{4,}\)
### **Message**
Fixed delays make tests slow and flaky. Wait for conditions instead.
### **Fix Action**
Use waitFor or polling: await waitFor(() => expect(element).toBeVisible());
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Testing Implementation Details

### **Id**
test-implementation-detail
### **Severity**
info
### **Type**
regex
### **Pattern**
  - expect\(.*\.mock\.calls
  - toHaveBeenCalledWith\([^)]*SELECT
  - toHaveBeenCalledWith\([^)]*INSERT
  - expect\(.*\.innerHTML\)
### **Message**
Testing implementation details makes tests brittle. Test behavior instead.
### **Fix Action**
Test outputs and side effects, not internal method calls or DOM structure.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Excessive Mocking

### **Id**
excessive-mocking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - jest\.mock\([^)]+\)[\s\S]*jest\.mock\([^)]+\)[\s\S]*jest\.mock\([^)]+\)[\s\S]*jest\.mock
  - vi\.mock\([^)]+\)[\s\S]*vi\.mock\([^)]+\)[\s\S]*vi\.mock\([^)]+\)[\s\S]*vi\.mock
### **Message**
Many mocks suggest testing mocks, not code. Consider integration test.
### **Fix Action**
Use real dependencies where practical. Mock only external systems.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Shared State Between Tests

### **Id**
shared-test-state
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - beforeAll\([^)]*\{[^}]*insert
  - beforeAll\([^)]*\{[^}]*create
  - let\s+\w+\s*;[\s\S]*beforeEach[\s\S]*=\s*[^;]+;[\s\S]*it\(
### **Message**
Shared state causes test pollution. Each test should set up its own data.
### **Fix Action**
Move setup to beforeEach or inside each test. Use unique IDs per test.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Only Happy Path Testing

### **Id**
only-happy-path
### **Severity**
info
### **Type**
regex
### **Pattern**
  - describe\([^)]+\)[^]*it\(['"].*(?:success|works|valid|correct)
### **Message**
Test file may only cover happy path. Consider edge cases and error paths.
### **Fix Action**
Add tests for: empty input, null/undefined, invalid data, error conditions.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js
### **Exceptions**
  - error|fail|invalid|empty|null|undefined|reject|throw

## Unclear Test Name

### **Id**
test-naming-unclear
### **Severity**
info
### **Type**
regex
### **Pattern**
  - it\(['"]test\s
  - it\(['"]should\s+work
  - it\(['"]works\s*['"]
  - it\(['"]test\d+
### **Message**
Test name doesn't describe behavior. Name should explain what and when.
### **Fix Action**
Use format: 'returns X when Y' or 'throws error when invalid input'
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Random Data Without Seed

### **Id**
random-data-unseeded
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Math\.random\(\)
  - faker\.
  - chance\.
### **Message**
Random data without seed causes flaky tests. Set seed for reproducibility.
### **Fix Action**
Seed random generator: faker.seed(12345); or use fixed test data.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js
### **Exceptions**
  - \.seed\(

## Commented Out Test

### **Id**
commented-test
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\s*it\(
  - //\s*test\(
  - //\s*describe\(
  - /\*[\s\S]*it\([\s\S]*\*/
### **Message**
Commented-out test is dead code. Delete or fix it.
### **Fix Action**
Either fix the test and uncomment, or delete entirely.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Skipped Test Without Reason

### **Id**
skip-without-reason
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.skip\(\)
  - xit\(
  - xdescribe\(
  - it\.skip\(['"][^'"]+['"]\s*,
### **Message**
Skipped test without explanation. Add TODO comment or remove.
### **Fix Action**
Add comment explaining why: it.skip('reason: waiting for API fix', ...)
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js
### **Exceptions**
  - TODO|FIXME|BUG|ISSUE

## Console Statement in Test

### **Id**
console-in-test
### **Severity**
info
### **Type**
regex
### **Pattern**
  - console\.log\(
  - console\.debug\(
### **Message**
Console statements in tests create noise. Remove debug output.
### **Fix Action**
Remove console statements or use test framework's debug utilities.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Network Call in Unit Test

### **Id**
network-call-in-unit-test
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fetch\(['"]http
  - axios\.[a-z]+\(['"]http
  - request\(['"]http
### **Message**
Real network call in test creates flakiness. Mock external calls.
### **Fix Action**
Mock HTTP layer: jest.mock('axios'); or use MSW for integration tests.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js
### **Exceptions**
  - nock\(
  - msw
  - mock

## Test File Too Long

### **Id**
long-test-file
### **Severity**
info
### **Type**
regex
### **Pattern**
  - describe\([\s\S]{15000,}
### **Message**
Very long test file. Consider splitting by feature or scenario.
### **Fix Action**
Split into focused test files: user.create.test.ts, user.delete.test.ts
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Too Many Assertions

### **Id**
single-assertion-per-test-violation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - expect\([^)]+\)[^;]*;[\s\S]*expect\([^)]+\)[^;]*;[\s\S]*expect\([^)]+\)[^;]*;[\s\S]*expect\([^)]+\)[^;]*;[\s\S]*expect\([^)]+\)[^;]*;
### **Message**
Many assertions in one test. Consider splitting for clearer failure messages.
### **Fix Action**
Split into multiple tests, each verifying one behavior.
### **Applies To**
  - **/*.test.ts
  - **/*.test.tsx
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js