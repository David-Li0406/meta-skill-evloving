---
name: test-creation-validation
description: Use this skill when validating the creation of integration and unit tests, ensuring proper structure, mocking strategies, and adherence to best practices.
---

# Test Creation Validation

## Purpose
Validate the quality and structure of integration and unit tests, ensuring proper mocking strategies, coverage, and adherence to best practices.

### Integration Test Validation (Gate 4b)

**STOP AND CHECK:**
```bash
# 1. Integration test files exist
if ! ls test/integration/*Test.ts 2>/dev/null | head -1 > /dev/null; then
  echo "❌ Gate 4b FAILED: No integration test files found"
  echo "   Create test/integration/{Resource}ProducerTest.ts"
  exit 1
fi

# 2. Test suites exist with proper structure
DESCRIBE_COUNT=$(grep -h "^describe(" test/integration/*.ts 2>/dev/null | wc -l)
if [ "$DESCRIBE_COUNT" -lt 1 ]; then
  echo "❌ Gate 4b FAILED: No describe blocks found"
  exit 1
fi

# 3. Multiple test cases (3+ per operation)
IT_COUNT=$(grep -h "^\s*it(" test/integration/*.ts 2>/dev/null | wc -l)
if [ "$IT_COUNT" -lt 3 ]; then
  echo "❌ Gate 4b FAILED: Insufficient test cases (found $IT_COUNT, need 3+)"
  exit 1
fi

# 4. CRITICAL: NO hardcoded test values
HARDCODED_IDS=$(grep -h -n -E "(const|let|var) [a-zA-Z_][a-zA-Z0-9_]*[Ii]d = ['\"][0-9a-zA-Z_-]+['\"]" test/integration/*.ts 2>/dev/null | grep -v "Common.ts" || true)
if [ -n "$HARDCODED_IDS" ]; then
  echo "❌ Gate 4b FAILED: Hardcoded test values found"
  exit 1
fi

# 5. Verify Common.ts exists and exports test data
if [ ! -f "test/integration/Common.ts" ]; then
  echo "❌ Gate 4b FAILED: test/integration/Common.ts missing"
  exit 1
fi

# 6. Verify .env file exists
if [ ! -f ".env" ]; then
  echo "⚠️  WARNING: .env file missing"
fi

# 7. Verify tests import from Common.ts
TEST_FILES_WITHOUT_COMMON=$(grep -L "from.*['\"]\.\/Common['\"]" test/integration/*Test.ts 2>/dev/null || true)
if [ -n "$TEST_FILES_WITHOUT_COMMON" ]; then
  echo "⚠️  WARNING: Some test files don't import from Common.ts:"
fi

# 8. Verify tests check hasCredentials
if ! grep -r "hasCredentials()" test/integration/*.ts > /dev/null 2>&1; then
  echo "⚠️  WARNING: Tests should check hasCredentials() in before() hook"
fi

# 9. Check for debug logging (MANDATORY)
LOGGER_IMPORTS=$(grep -h -c "getLogger" test/integration/*Test.ts 2>/dev/null | awk '{s+=$1} END {print s}')
if [ "$LOGGER_IMPORTS" -lt 1 ]; then
  echo "❌ Gate 4b FAILED: No debug logging found in integration tests"
  exit 1
fi

# 10. Verify NO nock in integration tests (should use real API)
if grep -h "from ['\"]nock['\"]" test/integration/*.ts 2>/dev/null | head -1 > /dev/null; then
  echo "❌ Gate 4b FAILED: nock found in integration tests"
  exit 1
fi

# 11. Check test file naming convention
for file in test/integration/*Test.ts; do
  if [ -f "$file" ]; then
    basename=$(basename "$file")
    if [[ ! "$basename" =~ ^[A-Z][a-zA-Z]*Test\.ts$ ]] && [[ "$basename" != "Common.ts" ]]; then
      echo "⚠️  WARNING: Incorrect test file naming: $basename"
    fi
  fi
done

echo "✅ Gate 4b: Integration Test Creation - PASSED"
```

### Unit Test Validation (Gate 4a)

**STOP AND CHECK:**
```bash
# 1. Unit test files exist
if ! ls test/unit/*Test.ts 2>/dev/null | head -1 > /dev/null; then
  echo "❌ Gate 4a FAILED: No unit test files found"
  echo "   Create test/unit/{Resource}ProducerTest.ts"
  exit 1
fi

# 2. Test suites exist with proper structure
DESCRIBE_COUNT=$(grep -h "^describe(" test/unit/*.ts 2>/dev/null | wc -l)
if [ "$DESCRIBE_COUNT" -lt 1 ]; then
  echo "❌ Gate 4a FAILED: No describe blocks found"
  exit 1
fi

# 3. Multiple test cases (3+ per operation)
IT_COUNT=$(grep -h "^\s*it(" test/unit/*.ts 2>/dev/null | wc -l)
if [ "$IT_COUNT" -lt 3 ]; then
  echo "❌ Gate 4a FAILED: Insufficient test cases (found $IT_COUNT, need 3+)"
  exit 1
fi

# 4. CRITICAL: ONLY nock used for HTTP mocking
if ! grep -h "from ['\"]nock['\"]" test/unit/*.ts 2>/dev/null | head -1 > /dev/null; then
  echo "❌ Gate 4a FAILED: nock not imported in unit tests"
  exit 1
fi

# 5. CRITICAL: No forbidden mocking libraries
FORBIDDEN_MOCKS=$(grep -h -E "jest\.mock|sinon|fetch-mock|msw" test/unit/*.ts 2>/dev/null || true)
if [ -n "$FORBIDDEN_MOCKS" ]; then
  echo "❌ Gate 4a FAILED: Forbidden mocking library detected"
  exit 1
fi

# 6. Verify Common.ts exists and is properly structured
if [ ! -f "test/unit/Common.ts" ]; then
  echo "❌ Gate 4a FAILED: test/unit/Common.ts missing"
  exit 1
fi

# 7. Verify error cases are tested
ERROR_TESTS=$(grep -h -i "error\|fail\|invalid\|unauthorized\|notfound\|404\|401" test/unit/*.ts 2>/dev/null | wc -l)
if [ "$ERROR_TESTS" -lt 1 ]; then
  echo "⚠️  WARNING: No error case tests found"
fi

# 8. Verify nock cleanup in tests
if ! grep -h "nock.cleanAll()" test/unit/*.ts > /dev/null 2>&1; then
  echo "⚠️  WARNING: No nock.cleanAll() found"
fi

# 9. Check test file naming convention
for file in test/unit/*Test.ts; do
  if [ -f "$file" ]; then
    basename=$(basename "$file")
    if [[ ! "$basename" =~ ^[A-Z][a-zA-Z]*Test\.ts$ ]] && [[ "$basename" != "Common.ts" ]]; then
      echo "⚠️  WARNING: Incorrect test file naming: $basename"
    fi
  fi
done

echo "✅ Gate 4a: Unit Test Creation - PASSED"
```

## Common Failures

### Hardcoded Test Values
Ensure all test values are sourced from environment variables or configuration files, not hardcoded in the test files.

### Forbidden Mocking Libraries
Only use `nock` for HTTP mocking in unit tests. Avoid using libraries like `jest.mock`, `sinon`, `fetch-mock`, or `msw`.

### Missing Error Case Tests
Ensure that tests cover various error scenarios, including unauthorized access, not found errors, and rate limits.

### Nock Cleanup
Always include `nock.cleanAll()` in your tests to prevent interference between tests.

## Related Rules
- **integration-test-patterns skill** ⭐ - All integration test patterns and examples
- **unit-test-patterns skill** ⭐ - All unit test patterns and examples
- **nock-patterns skill** ⭐ - HTTP mocking with nock (ONLY allowed library)
- **testing-core-rules skill** - General testing principles
- **failure-conditions skill** - Common failure conditions in tests

## Success Criteria
Both integration and unit test creation MUST meet ALL criteria outlined in the respective validation sections.