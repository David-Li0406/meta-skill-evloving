# Test Architect - Validations

## Test Without Assertion

### **Id**
missing-assertion
### **Severity**
error
### **Type**
regex
### **Pattern**
  - def test_[^(]+\([^)]*\):[^}]+(?<!assert)$
  - it\(["'][^"']+["'],\s*\(\)\s*=>\s*\{[^}]+\}\)(?!.*expect)
### **Message**
Test function without assertion. Test always passes.
### **Fix Action**
Add assert or expect statement to verify behavior
### **Applies To**
  - **/test_*.py
  - **/*.test.ts
  - **/*.spec.ts

## Hardcoded Email/ID in Tests

### **Id**
hardcoded-test-data
### **Severity**
info
### **Type**
regex
### **Pattern**
  - test@example\.com
  - user_123
  - agent_test
### **Message**
Hardcoded test data may cause isolation issues.
### **Fix Action**
Use unique generated data: f'test_{uuid4().hex}@example.com'
### **Applies To**
  - **/test_*.py
  - **/*.test.ts
  - **/*.spec.ts

## Fixed Sleep in Async Test

### **Id**
sleep-in-test
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - asyncio\.sleep\([0-9]
  - time\.sleep\([0-9]
  - await.*delay\([0-9]
  - setTimeout.*[0-9]+\)
### **Message**
Fixed sleep causes flaky tests. Use condition-based waiting.
### **Fix Action**
Use await wait_for(condition) or polling with timeout
### **Applies To**
  - **/test_*.py
  - **/*.test.ts
  - **/*.spec.ts

## Async Call Not Awaited in Test

### **Id**
async-not-awaited
### **Severity**
error
### **Type**
regex
### **Pattern**
  - assert\s+\w+\(\)(?!.*await)
  - expect\(\w+\(\)\)\.to
### **Message**
Async call may not be awaited. Test may pass falsely.
### **Fix Action**
Add await: assert await function() or await expect()
### **Applies To**
  - **/test_*.py
  - **/*.test.ts

## Excessive Mocking

### **Id**
mock-overuse
### **Severity**
info
### **Type**
regex
### **Pattern**
  - @mock\.patch.*@mock\.patch.*@mock\.patch
  - jest\.mock.*jest\.mock.*jest\.mock
  - Mock\(\).*Mock\(\).*Mock\(\)
### **Message**
Multiple mocks may hide integration issues.
### **Fix Action**
Consider using fakes or integration tests for complex interactions
### **Applies To**
  - **/test_*.py
  - **/*.test.ts

## Async Function Test Missing Async

### **Id**
test-not-async
### **Severity**
error
### **Type**
regex
### **Pattern**
  - def test_.*await
  - function test.*await(?!.*async)
### **Message**
Test uses await but function is not async.
### **Fix Action**
Add async to function definition: async def test_...
### **Applies To**
  - **/test_*.py
  - **/*.test.ts

## Fixture Without Cleanup

### **Id**
no-fixture-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @pytest\.fixture(?!.*yield|.*return)
  - beforeEach(?!.*afterEach)
### **Message**
Fixture creates resources but may not clean up.
### **Fix Action**
Use yield and cleanup after: yield resource; cleanup()
### **Applies To**
  - **/test_*.py
  - **/conftest.py
  - **/*.test.ts

## Snapshot Test Without Filtering

### **Id**
snapshot-without-filter
### **Severity**
info
### **Type**
regex
### **Pattern**
  - assert_match\([^)]+\)(?!.*exclude)
  - toMatchSnapshot\(\)(?!.*omit)
### **Message**
Snapshot includes all fields. May break on irrelevant changes.
### **Fix Action**
Filter out timestamps, IDs: assert_match(data, exclude=['created_at'])
### **Applies To**
  - **/test_*.py
  - **/*.test.ts

## Test Depends on Other Test

### **Id**
test-order-dependency
### **Severity**
error
### **Type**
regex
### **Pattern**
  - test_[a-z]+.*test_[a-z]+
  - @pytest\.mark\.order
  - jest\..*runInBand
### **Message**
Tests may depend on execution order. Should be independent.
### **Fix Action**
Use fixtures for setup, each test should be self-contained
### **Applies To**
  - **/test_*.py
  - **/*.test.ts

## No Error Case Test

### **Id**
missing-error-test
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class Test\w+:(?!.*error|.*exception|.*fail|.*invalid)
  - describe\([^)]+\)(?!.*error|.*throw|.*reject)
### **Message**
Test class has no error/exception tests.
### **Fix Action**
Add tests for error cases: test_raises_on_invalid_input
### **Applies To**
  - **/test_*.py
  - **/*.test.ts

## Test Marked as Flaky/Retry

### **Id**
flaky-test-retry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @pytest\.mark\.flaky
  - @retry
  - jest\.retryTimes
### **Message**
Test marked as flaky. Should be fixed or removed.
### **Fix Action**
Fix underlying timing/isolation issue instead of retrying
### **Applies To**
  - **/test_*.py
  - **/*.test.ts

## Test File Too Large

### **Id**
large-test-file
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def test_.*def test_.*def test_.*def test_.*def test_.*def test_.*def test_.*def test_.*def test_.*def test_
### **Message**
Test file has many tests. Consider splitting by feature.
### **Fix Action**
Split into focused test files: test_create.py, test_update.py
### **Applies To**
  - **/test_*.py
  - **/*.test.ts