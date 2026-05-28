# Testing Automation - Validations

## Missing Await in Async Test

### **Id**
test-missing-await
### **Severity**
error
### **Type**
regex
### **Pattern**
  - it\([^)]+,\s*\(\)\s*=>\s*{\s*(?!.*await|return)[^}]*\.(then|catch|resolves|rejects)
  - test\([^)]+,\s*\(\)\s*=>\s*{\s*(?!.*await|return)[^}]*\.(then|catch|resolves|rejects)
### **Message**
Async operation in non-async test function. Test may complete before assertion.
### **Fix Action**
Add async keyword to test function and await the operation
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js
  - **/__tests__/**

## Hardcoded Timeout in Test

### **Id**
test-hardcoded-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - setTimeout.*\d{3,}
  - waitForTimeout\(\d+
  - sleep\(\d+
  - new Promise.*setTimeout.*\d+
  - await.*delay\(\d+
### **Message**
Hardcoded timeout may cause flaky tests. Use waitFor or fake timers instead.
### **Fix Action**
Replace with waitFor(() => expect(...)) or jest.useFakeTimers()
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js
  - **/__tests__/**

## Shared Mutable State Between Tests

### **Id**
test-shared-mutable-state
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^let\s+\w+\s*[;=]\s*\n(?!.*beforeEach)
  - ^var\s+\w+\s*[;=]\s*\n(?!.*beforeEach)
### **Message**
Variable declared outside test may cause test order dependencies.
### **Fix Action**
Initialize in beforeEach or within individual test
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Test Without Assertion

### **Id**
test-no-assertion
### **Severity**
error
### **Type**
regex
### **Pattern**
  - it\([^)]+,\s*(?:async\s*)?\([^)]*\)\s*=>\s*{\s*[^}]*}\s*\);?\s*$(?![^}]*expect)
### **Message**
Test function has no expect() assertion. Test will pass without verifying anything.
### **Fix Action**
Add expect() assertions to verify expected behavior
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Brittle E2E Selector

### **Id**
test-brittle-selector
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - nth-child\(\d+\)
  - :first-child
  - :last-child
  - \.css-[a-z0-9]+
  - \.MuiButton
  - \.MuiInput
  - \.ant-
  - \.chakra-
  - \[class\*=
### **Message**
Brittle selector will break on UI changes. Use data-testid or role selectors.
### **Fix Action**
Replace with [data-testid='...'] or getByRole/getByLabel
### **Applies To**
  - **/*.spec.ts
  - **/*.spec.js
  - **/e2e/**
  - **/cypress/**
  - **/playwright/**

## .only() Left in Test

### **Id**
test-only-left
### **Severity**
error
### **Type**
regex
### **Pattern**
  - describe\.only\(
  - it\.only\(
  - test\.only\(
  - fdescribe\(
  - fit\(
### **Message**
.only() left in test file. Other tests in this file will be skipped.
### **Fix Action**
Remove .only() before committing
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Skipped Test Without Reason

### **Id**
test-skip-no-reason
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - describe\.skip\([^,]+,(?![^)]*//)
  - it\.skip\([^,]+,(?![^)]*//)
  - test\.skip\([^,]+,(?![^)]*//)
  - xdescribe\([^,]+,(?![^)]*//)
  - xit\([^,]+,(?![^)]*//)
### **Message**
Test skipped without explanation. Add comment explaining why.
### **Fix Action**
Add // TODO: comment explaining why test is skipped
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Mock Not Restored After Test

### **Id**
test-mock-not-restored
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - jest\.spyOn(?![\\s\\S]*?mockRestore)
  - jest\.mock(?![\\s\\S]*?(resetAllMocks|restoreAllMocks|clearAllMocks))
  - sinon\.stub(?![\\s\\S]*?restore)
### **Message**
Mock may not be restored. Can affect other tests.
### **Fix Action**
Add afterEach(() => jest.restoreAllMocks()) or manually restore
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Console.log in Test File

### **Id**
test-console-log
### **Severity**
info
### **Type**
regex
### **Pattern**
  - console\.log\(
  - console\.debug\(
  - console\.info\(
### **Message**
Console statement in test file. Remove debugging artifacts.
### **Fix Action**
Remove console statements before committing
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Hardcoded Test Data

### **Id**
test-hardcoded-data
### **Severity**
info
### **Type**
regex
### **Pattern**
  - email.*=.*['"]test@example\.com['"]
  - email.*=.*['"]user@test\.com['"]
  - password.*=.*['"]password123['"]
  - password.*=.*['"]test123['"]
### **Message**
Hardcoded test data may cause conflicts. Use unique generated data.
### **Fix Action**
Use faker.js or UUID for unique test data
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Weak Boolean Assertion

### **Id**
test-expect-true-false
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - expect\(true\)\.toBe\(true\)
  - expect\(false\)\.toBe\(false\)
  - expect\(.*\)\.toBe\(true\)$
  - expect\(.*\)\.toBe\(false\)$
### **Message**
Weak assertion. Use specific matcher for clearer failure messages.
### **Fix Action**
Use toBeVisible(), toHaveLength(), toContain(), etc. instead
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Magic Numbers in Test

### **Id**
test-magic-number
### **Severity**
info
### **Type**
regex
### **Pattern**
  - expect\([^)]+\)\.toBe\(\d{4,}\)
  - expect\([^)]+\)\.toEqual\(\d{4,}\)
  - toHaveLength\(\d{3,}\)
### **Message**
Magic number in assertion. Define as named constant for clarity.
### **Fix Action**
Extract to const with descriptive name
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Testing Implementation Details

### **Id**
test-implementation-detail
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.state\(
  - \.instance\(\)
  - wrapper\.vm\.
  - component\._
  - spyOn.*_[a-zA-Z]+
### **Message**
Testing private/internal implementation. Test will break on refactoring.
### **Fix Action**
Test observable behavior instead of internal state
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Large Snapshot Test

### **Id**
test-large-snapshot
### **Severity**
info
### **Type**
regex
### **Pattern**
  - toMatchSnapshot\(\)$
### **Message**
Full component snapshot may be too large to review meaningfully.
### **Fix Action**
Use toMatchInlineSnapshot() for focused assertions or test behavior instead
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Empty Catch in Test

### **Id**
test-empty-catch
### **Severity**
error
### **Type**
regex
### **Pattern**
  - catch\s*\([^)]*\)\s*{\s*}
  - catch\s*\([^)]*\)\s*{\s*//[^}]*}
### **Message**
Empty catch block swallows errors. Test may pass when it shouldn't.
### **Fix Action**
Fail test on error or use toThrow() matcher
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## External API Call in Test

### **Id**
test-external-api-call
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fetch\s*\(\s*["']https?://
  - axios\.[a-z]+\s*\(\s*["']https?://
  - http[s]?://api\.
  - http[s]?://.*\.com/
### **Message**
Test calls external API. May be flaky and slow.
### **Fix Action**
Mock external calls with nock, msw, or jest.mock
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Database/Resource Not Cleaned Up

### **Id**
test-no-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - beforeAll.*insert|create(?![\\s\\S]*?afterAll.*delete|truncate)
  - beforeEach.*insert|create(?![\\s\\S]*?afterEach.*delete|truncate)
### **Message**
Test creates data but may not clean up. Can cause test pollution.
### **Fix Action**
Add afterEach cleanup or use transaction rollback
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Duplicate Test Name

### **Id**
test-duplicate-name
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (it|test)\(['"]([^'"]+)['"][\s\S]*?\1\(['"]\2['"]
### **Message**
Duplicate test name makes failures ambiguous in reports.
### **Fix Action**
Use unique, descriptive test names
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## TODO Test Without Implementation

### **Id**
test-todo-test
### **Severity**
info
### **Type**
regex
### **Pattern**
  - it\.todo\(
  - test\.todo\(
  - // TODO.*test
  - // FIXME.*test
### **Message**
Unimplemented test placeholder. Complete or remove.
### **Fix Action**
Implement the test or create an issue to track it
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Flaky Date/Time in Test

### **Id**
test-flaky-date
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new Date\(\)
  - Date\.now\(\)
  - moment\(\)
  - dayjs\(\)
### **Message**
Real current date/time causes flaky tests at midnight/year boundary.
### **Fix Action**
Use jest.useFakeTimers() or mock the date
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js

## Only Testing Happy Path

### **Id**
test-missing-error-case
### **Severity**
info
### **Type**
regex
### **Pattern**
  - describe\([^)]+\)\s*{\s*(?:[^}]*it\([^)]+,)(?![^}]*(?:error|fail|invalid|throw|reject))[^}]*}
### **Message**
Test suite only tests success case. Consider error scenarios.
### **Fix Action**
Add tests for error cases, edge cases, and invalid inputs
### **Applies To**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/*.spec.js