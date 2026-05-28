---
name: gate-validation-tests
description: Use this skill to validate the quality and structure of integration and unit tests in your project.
---

# Skill body

### Gate Validation Tests

**Purpose:** Validate the quality of integration and unit tests, ensuring proper structure, test data management, and mocking strategies.

**STOP AND CHECK:**

```bash
# 1. Test files exist
if ! ls test/{integration,unit}/*Test.ts 2>/dev/null | head -1 > /dev/null; then
  echo "❌ Gate Validation FAILED: No test files found"
  echo "   Create test/{integration,unit}/{Resource}ProducerTest.ts"
  exit 1
fi

INTEGRATION_TEST_FILE_COUNT=$(ls test/integration/*Test.ts 2>/dev/null | wc -l)
UNIT_TEST_FILE_COUNT=$(ls test/unit/*Test.ts 2>/dev/null | wc -l)
echo "✅ Found $INTEGRATION_TEST_FILE_COUNT integration test file(s) and $UNIT_TEST_FILE_COUNT unit test file(s)"

# 2. Test suites exist with proper structure
for dir in integration unit; do
  DESCRIBE_COUNT=$(grep -h "^describe(" test/$dir/*.ts 2>/dev/null | wc -l)
  if [ "$DESCRIBE_COUNT" -lt 1 ]; then
    echo "❌ Gate Validation FAILED: No describe blocks found in $dir tests"
    exit 1
  fi
  echo "✅ Found $DESCRIBE_COUNT describe block(s) in $dir tests"
done

# 3. Multiple test cases (3+ per operation)
for dir in integration unit; do
  IT_COUNT=$(grep -h "^\s*it(" test/$dir/*.ts 2>/dev/null | wc -l)
  if [ "$IT_COUNT" -lt 3 ]; then
    echo "❌ Gate Validation FAILED: Insufficient test cases in $dir tests (found $IT_COUNT, need 3+)"
    exit 1
  fi
  echo "✅ Found $IT_COUNT test case(s) in $dir tests"
done

# 4. Integration tests: NO hardcoded test values
echo "Checking for hardcoded test values in integration tests..."
HARDCODED_IDS=$(grep -h -n -E "(const|let|var) [a-zA-Z_][a-zA-Z0-9_]*[Ii]d = ['\"][0-9a-zA-Z_-]+['\"]" test/integration/*.ts 2>/dev/null || true)

if [ -n "$HARDCODED_IDS" ]; then
  echo "❌ Gate Validation FAILED: Hardcoded test values found in integration tests"
  echo "   ALL test values must be in .env and imported from Common.ts"
  exit 1
fi
echo "✅ No hardcoded test values in integration tests"

# 5. Unit tests: ONLY nock used for HTTP mocking
if ! grep -h "from ['\"]nock['\"]" test/unit/*.ts 2>/dev/null | head -1 > /dev/null; then
  echo "❌ Gate Validation FAILED: nock not imported in unit tests"
  echo "   Unit tests MUST use nock for HTTP mocking"
  exit 1
fi
echo "✅ nock imported for HTTP mocking in unit tests"

# 6. Verify Common.ts exists and is properly structured
for dir in integration unit; do
  if [ ! -f "test/$dir/Common.ts" ]; then
    echo "❌ Gate Validation FAILED: test/$dir/Common.ts missing"
    echo "   Create Common.ts with necessary helpers"
    exit 1
  fi
done
echo "✅ Common.ts exists for both integration and unit tests"
```