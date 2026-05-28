# Implementation Specification for jq-transforms

This document provides the exact pattern for implementing new transformations in this library.

## Overview

Each transformation follows a strict pattern:
- `<name>/transform.jq` - The jq transformation code
- `<name>/schema.json` - Input/output/args schema
- `<name>/test.sh` - Test suite (5+ test cases)
- `<name>/test-input-*.json` - Test input fixtures

## Directory Structure Pattern

```
transformation-name/
├── transform.jq          # The transformation logic
├── schema.json          # Schema definition
├── test.sh             # Test suite
├── test-input-1.json   # Test fixture 1
├── test-input-2.json   # Test fixture 2
└── test-input-3.json   # Test fixture 3 (etc.)
```

## 1. transform.jq Pattern

### Header Comments
```jq
# [Brief description]
# Usage: jq -f <name>/transform.jq --arg arg1 "value" [--arg arg2 "value"] input.json
#
# Arguments:
#   arg1: description of arg1
#   arg2: description of arg2 (optional)
#
# Input: description of expected input
# Output: description of output
```

### Code Structure
```jq
# Example from crud-get:
($path | split(".")) as $keys |
getpath($keys) as $value |

if $value != null then
  $value
elif ($ARGS.named.default // "") != "" then
  $ARGS.named.default
else
  null
end
```

### Key Patterns
- Use `$ARGS.named.argname` to access arguments
- Use `split(".")` for dot-separated paths
- Use `getpath()` and `setpath()` for nested access
- Handle null/missing values gracefully
- Keep transformations simple (5-20 lines max)

## 2. schema.json Pattern

### Complete Example (crud-get)
```json
{
  "name": "transformation-name",
  "description": "One-line description of what it does",
  "version": "1.0.0",
  "input": {
    "type": "object",
    "description": "Description of expected input"
  },
  "args": {
    "required_arg": {
      "type": "string",
      "required": true,
      "description": "What this argument does"
    },
    "optional_arg": {
      "type": "string",
      "required": false,
      "description": "What this optional argument does"
    }
  },
  "output": {
    "type": ["string", "number", "boolean", "object", "array", "null"],
    "description": "What the transformation returns"
  },
  "examples": [
    {
      "description": "Example use case",
      "input": {"key": "value"},
      "args": {"arg": "value"},
      "output": "expected result"
    }
  ],
  "tags": ["category", "keywords"]
}
```

### Schema Rules
- `name`: Use kebab-case matching directory name
- `version`: Always start at "1.0.0"
- `input.type`: Usually "object" or "array"
- `args`: Define ALL arguments (required + optional)
- `output.type`: Can be array of types if multiple possible
- `examples`: At least 3 examples showing different use cases
- `tags`: Include category (crud/array/string/etc) + descriptive keywords

## 3. test.sh Pattern

### Complete Example Structure
```bash
#!/usr/bin/env bash
set -euo pipefail

# Test <transformation-name> transformation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing <transformation-name> transformation..."

# Test 1: [Description]
echo -n "Test 1: [Description]... "
result=$(jq -f "$TRANSFORM" --arg arg1 "value1" "$SCRIPT_DIR/test-input-1.json")
expected='"expected-value"'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# Test 2: [Description]
echo -n "Test 2: [Description]... "
result=$(jq -f "$TRANSFORM" --arg arg1 "value2" "$SCRIPT_DIR/test-input-2.json")
expected='42'
if [[ "$result" == "$expected" ]]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $expected"
    echo "  Got: $result"
    exit 1
fi

# ... more tests ...

echo "All <transformation-name> tests passed!"
```

### Test Rules
- Minimum 5 test cases
- Use `jq -c` for compact output when comparing objects/arrays
- Test happy path (2-3 tests)
- Test edge cases (null, empty, missing fields)
- Test error cases if applicable
- Each test exits with 1 on failure
- Clear descriptive test names

### Common Test Patterns

**Testing string output:**
```bash
result=$(jq -f "$TRANSFORM" --arg path "user.name" "$SCRIPT_DIR/test-input.json")
expected='"skogix"'
```

**Testing number output:**
```bash
result=$(jq -f "$TRANSFORM" --arg path "age" "$SCRIPT_DIR/test-input.json")
expected='30'
```

**Testing object/array output (use -c for compact):**
```bash
result=$(jq -c -f "$TRANSFORM" "$SCRIPT_DIR/test-input.json")
expected='{"key":"value"}'
```

**Testing null output:**
```bash
result=$(jq -f "$TRANSFORM" --arg path "missing" "$SCRIPT_DIR/test-input.json")
expected='null'
```

## 4. Test Input Files Pattern

### test-input-1.json (Happy path)
```json
{
  "user": {
    "name": "skogix",
    "profile": {
      "age": 30
    }
  }
}
```

### test-input-2.json (Edge case - missing fields)
```json
{
  "user": {
    "name": "test"
  }
}
```

### test-input-3.json (Edge case - arrays)
```json
{
  "data": {
    "items": [1, 2, 3]
  }
}
```

## 5. Testing Your Implementation

### Run individual transformation tests
```bash
cd /home/skogix/dev/skogix/src/jq-transforms
./transformation-name/test.sh
```

### Run all tests
```bash
./test-all.sh
```

Tests MUST pass before considering the transformation complete.

## 6. Common Transformation Patterns

### CRUD Operations
- **Get**: `getpath($keys)` with default handling
- **Set**: `setpath($keys; $value)`
- **Delete**: `delpaths([$keys])`
- **Has**: `getpath($keys) != null` or `has($key)`

### Array Operations
- **Filter**: `.array | map(select(.condition))`
- **Map**: `.array | map(.transformation)`
- **Reduce**: `.array | reduce .[] as $item (init; operation)`

### String Operations
- **Split**: `split($delimiter)`
- **Join**: `join($delimiter)`
- **Replace**: `gsub($pattern; $replacement)`

### Validation
- **Type check**: `if (.field | type) == "string" then ... end`
- **Required**: `if .field == null then error("required") else .field end`
- **Range**: `if .num >= $min and .num <= $max then ... end`

## 7. Common Mistakes to Avoid

❌ **Don't hardcode values in transform.jq**
```jq
setpath(["user", "name"]; "hardcoded")  # WRONG
```

✅ **Use arguments**
```jq
($path | split(".")) as $keys | setpath($keys; $value)  # CORRECT
```

❌ **Don't skip test cases**
```bash
# Only 1-2 tests  # WRONG
```

✅ **Write comprehensive tests**
```bash
# Minimum 5 tests covering happy path + edge cases  # CORRECT
```

❌ **Don't make tests with unclear expectations**
```bash
result=$(jq -f "$TRANSFORM" input.json)
# What should result be?  # WRONG
```

✅ **Always specify expected output**
```bash
result=$(jq -f "$TRANSFORM" input.json)
expected='{"clear":"expectation"}'  # CORRECT
```

## 8. Implementation Checklist

- [ ] Create directory `<name>/`
- [ ] Write `transform.jq` with header comments
- [ ] Create `schema.json` with all required fields
- [ ] Create 3+ test input files (`test-input-*.json`)
- [ ] Write `test.sh` with 5+ test cases
- [ ] Make `test.sh` executable (`chmod +x test.sh`)
- [ ] Run individual tests: `./test.sh`
- [ ] Run all tests: `../test-all.sh`
- [ ] Verify all tests pass (exit code 0)

## 9. Reference Implementations

See these working examples:
- `crud-get/` - Simple get with optional default
- `crud-set/` - Set value creating intermediate paths
- `crud-delete/` - Delete value at path

Study these to understand the exact pattern.

## 10. Integration

The `test-all.sh` script automatically discovers and runs all `*/test.sh` files. No need to modify it when adding new transformations.

---

# CRITICAL: Comprehensive Testing Requirements

## The Problem We're Solving

Initial implementations often have **60-70% test coverage gaps** with critical bugs hidden in edge cases. This section defines mandatory testing requirements to achieve **90%+ coverage**.

## Mandatory Test Coverage Checklist

**EVERY transformation MUST test ALL of these categories:**

### ✅ 1. Happy Path (2-3 tests)
- [ ] Basic functionality with typical input
- [ ] Nested/deep paths (if applicable)
- [ ] Multiple variations of valid input

### ✅ 2. Edge Cases - Falsy Values (CRITICAL)
**These are the most commonly missed tests:**
- [ ] **null values** - Path exists but value is `null`
- [ ] **boolean false** - NOT the same as missing/null
- [ ] **number 0** - NOT the same as missing/null
- [ ] **empty string ""** - NOT the same as missing/null
- [ ] **empty array []** - NOT the same as missing
- [ ] **empty object {}** - NOT the same as missing

**Why:** The `//` operator and `!= null` checks treat these differently. You MUST test all falsy values explicitly.

### ✅ 3. Type Safety (CRITICAL)
- [ ] Non-existent paths/fields
- [ ] Wrong input type (string instead of object, etc.)
- [ ] Missing required fields
- [ ] Invalid argument values

**For array operations specifically:**
- [ ] Array field doesn't exist
- [ ] Array field is not an array (string, number, object)
- [ ] Array contains primitives (numbers, strings, booleans)
- [ ] Array contains mixed types (objects + primitives)
- [ ] Empty array

### ✅ 4. Boundary Conditions
- [ ] Empty input (`{}`, `[]`, `""`)
- [ ] Single element
- [ ] Very large input (if relevant)
- [ ] Delimiters at start/end (for string operations)
- [ ] Consecutive delimiters/separators

### ✅ 5. Data Type Coverage
Test with ALL JSON types:
- [ ] Strings (including empty)
- [ ] Numbers (including 0, negatives, decimals)
- [ ] Booleans (both true AND false)
- [ ] Null (explicit null value)
- [ ] Arrays (empty and populated)
- [ ] Objects (empty and populated)

### ✅ 6. Error Cases
- [ ] Malformed arguments
- [ ] Type mismatches
- [ ] Out-of-bounds access
- [ ] Missing intermediate keys in paths

---

## Common Testing Anti-Patterns (DON'T DO THIS)

### ❌ Anti-Pattern 1: Only Testing Happy Paths
```bash
# WRONG - Only tests when things work
Test 1: Extract name field... PASS
Test 2: Extract age field... PASS
Test 3: Extract with custom array... PASS
```

**Problem:** Doesn't test what happens with null, false, 0, missing fields, wrong types, etc.

**Right approach:** Add edge case tests for EVERY falsy value and type mismatch.

### ❌ Anti-Pattern 2: Assuming `!= null` Catches Everything
```jq
# WRONG - This has a semantic bug
getpath($keys) != null
```

**Problem:** Returns `false` for paths that exist but have `null` values. This confuses "path exists" with "value is non-null".

**Right approach:** If checking existence, use `has()`. If checking non-null, document it clearly.

### ❌ Anti-Pattern 3: Using `// fallback` Without Understanding Falsy Values
```jq
# WRONG - Breaks for null and false
($value | fromjson? // $value)
```

**Problem:** When `fromjson?` successfully parses `"null"` → `null` or `"false"` → `false`, the `//` operator treats them as falsy and uses the fallback string instead.

**Right approach:** Use `try-catch`:
```jq
try ($value | fromjson) catch $value
```

### ❌ Anti-Pattern 4: No Type Checking Before Operations
```jq
# WRONG - Crashes if not an array
.items | map(...)
```

**Problem:** If `items` is a string, number, or doesn't exist, `map()` crashes with cryptic error.

**Right approach:** Add type check:
```jq
if (.items | type) == "array" then
  .items | map(...)
else
  []
end
```

### ❌ Anti-Pattern 5: Testing Strings Only
```bash
# WRONG - Only tests string values
Test 1: Extract "alice"... PASS
Test 2: Extract "bob"... PASS
Test 3: Extract "charlie"... PASS
```

**Problem:** Doesn't test numbers, booleans, null, objects, arrays as values.

**Right approach:** Test extraction of ALL types.

### ❌ Anti-Pattern 6: Not Testing Type Mismatches
```bash
# MISSING - What if user passes wrong type?
# Missing test: What if items is a string not an array?
# Missing test: What if array contains numbers not objects?
```

**Problem:** Real-world data is messy. Type mismatches will happen.

**Right approach:** Add tests for common type mistakes users will make.

---

## Minimum Test Requirements by Category

### For CRUD Operations (get/set/delete/has)
**Minimum 8 tests:**
1. Basic nested path (happy path)
2. Deep nesting (3+ levels)
3. Non-existent path
4. Path with null value
5. Path with false value
6. Path with 0 value
7. Empty object input
8. Intermediate missing keys

### For Array Operations (map/filter/reduce)
**Minimum 10 tests:**
1. Basic array operation (happy path)
2. Empty array
3. Array field doesn't exist
4. Array field is not an array (type safety)
5. Array contains primitives
6. Array contains mixed types (objects + primitives)
7. Missing fields in array objects
8. Null values in fields
9. Boolean false in fields
10. Zero values in fields

### For String Operations (split/join/replace)
**Minimum 8 tests:**
1. Basic operation (happy path)
2. Empty string
3. Delimiter at start
4. Delimiter at end
5. Consecutive delimiters
6. Delimiter not found
7. Non-string value (returns null)
8. Multi-character delimiter (if applicable)

### For Object Operations (pick/merge/nest)
**Minimum 8 tests:**
1. Basic operation (happy path)
2. Missing fields
3. All fields missing
4. Empty object input
5. Boolean/null/zero values
6. Array values
7. Object values
8. Whitespace in arguments (if applicable)

---

## Real Bugs Found and How to Prevent Them

### Bug 1: array-filter couldn't filter null/false values
**Root cause:** Used `fromjson? // $value` which treats null/false as falsy
**How found:** No test for filtering null or false values
**Prevention:** ALWAYS test filtering/matching for null and false
**Test required:**
```bash
# Test: Filter for null values
input='{"items":[{"val":null},{"val":"test"}]}'
echo "$input" | jq -f transform.jq --arg field "val" --arg value "null"
expected='{"items":[{"val":null}]}'
```

### Bug 2: array-map crashed on non-array fields
**Root cause:** No type checking before `map()` operation
**How found:** No test for wrong input types
**Prevention:** ALWAYS test with wrong types (string instead of array, etc.)
**Test required:**
```bash
# Test: Non-array field gracefully returns empty array
input='{"items":"not-an-array"}'
echo "$input" | jq -f transform.jq --arg field "name"
expected='[]'
```

### Bug 3: crud-has returned false for existing paths with null values
**Root cause:** Checked `getpath() != null` instead of key existence
**How found:** No test for paths with null values
**Prevention:** ALWAYS test "path exists with null value"
**Test required:**
```bash
# Test: Path exists even if value is null
input='{"user":{"name":null}}'
echo "$input" | jq -f transform.jq --arg path "user.name"
expected='true'  # Key exists!
```

---

## Testing Workflow

1. **Write implementation**
2. **Run this checklist** - Mark each category tested
3. **Add minimum required tests** (8-10 based on category)
4. **Add edge case tests** for every falsy value
5. **Add type safety tests** for wrong input types
6. **Run tests** - All must pass
7. **Code review** - Verify coverage

---

## Test Coverage Self-Assessment

Before submitting, rate your tests:

**Happy Path Coverage:** ___ / 3 tests
**Falsy Value Coverage:** ___ / 6 tests (null, false, 0, "", [], {})
**Type Safety Coverage:** ___ / 4 tests (wrong types, missing fields, etc.)
**Boundary Conditions:** ___ / 3 tests (empty, single, edges)
**Data Type Coverage:** ___ / 6 types (string, number, boolean, null, array, object)

**Minimum acceptable:** 15 tests covering all categories
**Good coverage:** 20+ tests
**Excellent coverage:** 25+ tests with all edge cases

---

## When in Doubt, Add the Test

If you think "should I test this edge case?" → **YES, add the test.**

Better to have 30 passing tests than 10 tests with hidden bugs.
