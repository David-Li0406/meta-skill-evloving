# Qa Engineering - Validations

## Hardcoded Wait in Tests

### **Id**
qa-hardcoded-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - waitForTimeout\\(\\d+
  - sleep\\(\\d+
  - setTimeout.*\\d{3,}
  - \\.delay\\(\\d+
### **Message**
Hardcoded wait in test. Use condition-based waits instead.
### **Fix Action**
Replace with waitForSelector, waitForResponse, or waitForCondition
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js
  - *.e2e.ts
  - *.e2e.js

## Skipped Test Without Ticket

### **Id**
qa-skipped-test
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - test\\.skip\\([^)]*\\)(?!.*JIRA|.*TODO|.*#\\d+)
  - it\\.skip\\([^)]*\\)(?!.*JIRA|.*TODO|.*#\\d+)
  - xit\\([^)]*\\)(?!.*JIRA|.*TODO|.*#\\d+)
  - xdescribe\\([^)]*\\)(?!.*JIRA|.*TODO|.*#\\d+)
### **Message**
Skipped test without tracking ticket. Skipped tests should have a JIRA/issue reference.
### **Fix Action**
Add tracking ticket or delete the test: test.skip('reason - JIRA-123')
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Shared Global Test Data

### **Id**
qa-shared-test-data
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - beforeAll.*insert|create
  - global\\.[a-zA-Z]+\\s*=.*test
  - let\\s+shared[A-Z]
### **Message**
Shared test data detected. Each test should create its own data for isolation.
### **Fix Action**
Move data creation to beforeEach and cleanup to afterEach
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Console Error Suppression

### **Id**
qa-console-error-suppressed
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\\.error.*=.*jest\\.fn\\(\\)
  - spyOn.*console.*error.*mockImplementation\\(\\s*\\)
  - console\\.error.*=.*\\(\\)\\s*=>
### **Message**
Console errors suppressed without assertion. Consider failing tests on console errors.
### **Fix Action**
Use mockImplementation that throws or assert on call count
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Test Without Assertion

### **Id**
qa-no-assertion
### **Severity**
error
### **Type**
regex
### **Pattern**
  - test\\([^)]*,\\s*(?:async\\s*)?\\([^)]*\\)\\s*=>\\s*\\{[^}]*\\}\\s*\\)(?![\\s\\S]*expect)
  - it\\([^)]*,\\s*(?:async\\s*)?\\([^)]*\\)\\s*=>\\s*\\{[^}]*\\}\\s*\\)(?![\\s\\S]*expect)
### **Message**
Test has no assertion. Every test must verify expected outcomes.
### **Fix Action**
Add expect() assertions to verify the test outcome
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Focused Test (only) Committed

### **Id**
qa-only-test
### **Severity**
error
### **Type**
regex
### **Pattern**
  - test\\.only\\(
  - it\\.only\\(
  - describe\\.only\\(
  - fit\\(
  - fdescribe\\(
### **Message**
.only test committed. This will skip other tests in CI.
### **Fix Action**
Remove .only before committing
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## TODO in Test Without Ticket

### **Id**
qa-todo-test
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\\s*TODO(?!.*JIRA|.*#\\d+)
  - //\\s*FIXME(?!.*JIRA|.*#\\d+)
### **Message**
TODO/FIXME in test code without ticket reference.
### **Fix Action**
Create tracking ticket and reference it: // TODO: JIRA-123
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Excessive Mocking

### **Id**
qa-mock-all-dependencies
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - jest\\.mock\\([^)]*\\)\\s*jest\\.mock\\([^)]*\\)\\s*jest\\.mock
### **Message**
Many dependencies mocked. Consider integration testing instead.
### **Fix Action**
Reduce mocks or use integration tests for better confidence
### **Applies To**
  - *.test.ts
  - *.test.js

## Snapshot Without Descriptive Name

### **Id**
qa-snapshot-no-name
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - toMatchSnapshot\\(\\)
  - toMatchInlineSnapshot\\(\\)
### **Message**
Snapshot without descriptive name. Add a name for clarity.
### **Fix Action**
Add name: toMatchSnapshot('component renders correctly')
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.test.tsx
  - *.test.jsx

## Flaky Test Retry Pattern

### **Id**
qa-flaky-retry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - retry\\s*:\\s*[3-9]
  - retries\\s*:\\s*[3-9]
  - \\.retries\\(\\s*[3-9]
### **Message**
High retry count suggests flaky test. Fix the root cause.
### **Fix Action**
Investigate and fix flakiness instead of adding retries
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js
  - playwright.config.*
  - jest.config.*

## Testing Implementation Details

### **Id**
qa-test-implementation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - expect\\(.*\\._
  - expect\\(.*\\.private
  - toHaveBeenCalledWith.*internal
### **Message**
Testing private/internal implementation. Test behavior, not implementation.
### **Fix Action**
Test public API and outcomes instead of internal methods
### **Applies To**
  - *.test.ts
  - *.test.js

## Missing Test Cleanup

### **Id**
qa-no-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - beforeEach(?![\\s\\S]*afterEach)
  - addEventListener(?![\\s\\S]*removeEventListener)
  - setInterval(?![\\s\\S]*clearInterval)
### **Message**
Setup without corresponding cleanup. Add afterEach for proper isolation.
### **Fix Action**
Add afterEach to clean up test state
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Magic Number Timeout

### **Id**
qa-magic-number-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - timeout:\\s*\\d{4,}
  - waitFor.*\\d{4,}
### **Message**
Magic number timeout. Use named constants for clarity.
### **Fix Action**
Define constant: const ASYNC_TIMEOUT = 5000
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js