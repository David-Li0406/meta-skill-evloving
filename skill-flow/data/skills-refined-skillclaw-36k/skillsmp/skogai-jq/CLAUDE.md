# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is this?

Schema-driven JSON transformation library built **for AI agents**. Each transformation is a standalone jq script with:
- Clear input/output contract (schema.json)
- Self-contained test suite (test.sh)
- Minimal, readable implementation (transform.jq)

Philosophy: Transformations should be **discoverable** (via schema), **verifiable** (via tests), and **composable** (via pipes).

## Commands

### Running Tests

```bash
# Run all tests (14 transformations, ~100+ test cases)
./test-all.sh

# Run specific transformation tests
./crud-get/test.sh
./array-filter/test.sh

# Test individual transformation manually
echo '{"user":{"name":"skogix"}}' | jq -f crud-get/transform.jq --arg path "user.name"
```

### Development Workflow

```bash
# 1. Create new transformation directory
mkdir transformation-name

# 2. Implement following the pattern in IMPLEMENTATION_SPEC.md
#    - transformation-name/transform.jq
#    - transformation-name/schema.json
#    - transformation-name/test.sh
#    - transformation-name/test-input-*.json

# 3. Run tests to verify
chmod +x transformation-name/test.sh
./transformation-name/test.sh

# 4. Verify integration with all tests
./test-all.sh
```

## Architecture

### File Structure Pattern

Every transformation follows this exact structure:

```
transformation-name/
├── transform.jq          # jq script (5-40 lines, pure jq)
├── schema.json           # Input/output/args contract
├── test.sh              # Bash test suite (8-17 tests minimum)
└── test-input-*.json    # Test fixtures (one per test case)
```

### Categories of Transformations

**CRUD Operations** (crud-*): Path-based object manipulation
- `crud-get`, `crud-set`, `crud-delete`, `crud-has`, `crud-merge`, `crud-query`

**Array Operations** (array-*): Array transformations
- `array-filter`, `array-map`, `array-reduce`, `array-unique`, `array-flatten`

**String Operations** (string-*): String manipulation
- `string-split`, `string-join`

**Object Operations**: Field selection
- `pick-fields`

### How Transformations Work

1. **Input**: Receive JSON object via stdin
2. **Args**: Accept arguments via `--arg name value` (accessed as `$ARGS.named.name`)
3. **Transform**: Apply jq logic using `getpath()`/`setpath()` for nested access
4. **Output**: Return transformed JSON to stdout

Key pattern: Use `($path | split(".")) as $keys | getpath($keys)` for dot-separated paths.

## Critical Implementation Requirements

**From IMPLEMENTATION_SPEC.md - MUST FOLLOW:**

### Test Coverage (90%+ required)

Every transformation MUST test:

1. **Happy path** (2-3 tests): Basic functionality, nested paths, variations
2. **Falsy values** (CRITICAL): `null`, `false`, `0`, `""`, `[]`, `{}`
3. **Type safety**: Non-existent paths, wrong types, missing fields
4. **Boundary conditions**: Empty input, single element, edge cases
5. **All JSON types**: strings, numbers, booleans, null, arrays, objects
6. **Error cases**: Malformed args, type mismatches, missing keys

**Minimum 8-10 tests per transformation.**

### Common jq Pitfalls to Avoid

1. **`// fallback` with falsy values**:
   ```jq
   # WRONG - breaks for null/false
   ($value | fromjson? // $value)

   # RIGHT - use try-catch
   try ($value | fromjson) catch $value
   ```

2. **`!= null` for existence checks**:
   ```jq
   # WRONG - confuses "exists" with "non-null"
   getpath($keys) != null

   # RIGHT - use has() for existence
   reduce $keys[1:] as $k (has($keys[0]); if . then has($k) else false end)
   ```

3. **Type checking before array operations**:
   ```jq
   # WRONG - crashes if not array
   .items | map(...)

   # RIGHT - check type first
   if (.items | type) == "array" then .items | map(...) else [] end
   ```

### transform.jq Header Template

```jq
# [Brief description]
# Usage: jq -f <name>/transform.jq --arg arg1 "value" input.json
#
# Arguments:
#   arg1: description
#
# Input: description of expected input
# Output: description of output
```

### schema.json Required Fields

- `name`: kebab-case matching directory
- `description`: One-line what-it-does
- `version`: "1.0.0" for new transformations
- `input`: Type and description
- `args`: ALL arguments (required + optional)
- `output`: Type(s) and description
- `examples`: Minimum 3 examples
- `tags`: Category + keywords

### test.sh Structure

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSFORM="$SCRIPT_DIR/transform.jq"

echo "Testing <name> transformation..."

# Test N: [Description]
echo -n "Test N: [Description]... "
result=$(jq -c -f "$TRANSFORM" --arg path "x" "$SCRIPT_DIR/test-input-N.json")
expected='{"expected":"output"}'
[[ "$result" == "$expected" ]] && echo "PASS" || {
    echo "FAIL (expected: $expected, got: $result)"; exit 1;
}

echo "All <name> tests passed!"
```

**Note**: Use `-c` for compact output, `-S` if key order matters.

## Using Existing Transformations as Reference

**Best examples to study:**

- **crud-has**: Shows proper existence checking with `has()`
- **array-filter**: Demonstrates `try-catch` for JSON parsing (avoids `//` pitfall)
- **array-map**: Shows type checking before array operations
- **crud-merge**: Complex recursive function with proper key merging
- **array-flatten**: Depth-controlled recursion with `reduce`

## Known Bugs Fixed (Learn from these)

1. **array-filter** (commit b42ebe5): Used `fromjson? // $value` which broke on null/false values → Fixed with `try-catch`
2. **array-map** (commit b42ebe5): No type checking before `map()` → Added array type check
3. **crud-has** (commit b42ebe5): Used `getpath() != null` which confused existence with non-null → Fixed with `has()`
4. **crud-merge** (commit 6a0c634): Used `+` operator which doesn't merge recursively → Rewrote to merge all keys
5. **array-flatten** (commit fe19adb): Used `add` which fails on mixed types → Changed to `reduce` pattern

## Design Principles

1. **No wrappers**: Direct jq invocation, no abstraction hiding behavior
2. **Self-contained**: Each transformation is isolated, no dependencies
3. **Test-driven**: Tests show usage and verify correctness
4. **Minimal code**: Fewer lines = fewer bugs, easier to understand
5. **Composable**: Chain transformations via Unix pipes
6. **Schema-first**: Contract defines interface, implementation follows

## Related Documentation

- **IMPLEMENTATION_SPEC.md**: Complete implementation guide with all patterns
- **README.md**: User-facing documentation and usage examples
- **USAGE_EXAMPLES.md**: Real-world usage scenarios
- **../../todo/jq-transforms/**: Vision, backlog, patterns, proposals
