# JQ TRANSFORMATIONS

Schema-driven JSON transformation library built **for AI agents**.

## OVERVIEW

50+ standalone jq scripts with clear contracts. Transformations are **discoverable** (via schema), **verifiable** (via tests), **composable** (via pipes).

## STRUCTURE

```
scripts/jq/
├── crud-get/         # Get value at path
├── crud-set/         # Set value at path
├── crud-delete/      # Delete value at path
├── crud-has/         # Check path existence
├── crud-merge/       # Deep merge objects
├── crud-query/       # Query/filter arrays
├── array-*/          # Array operations (filter, map, reduce, unique, flatten)
├── string-*/         # String operations (split, join, trim, replace)
├── validate-*/       # Validation helpers
├── to-*/             # Type conversions
└── test-all.sh       # Run all 139 tests
```

**Each transformation:**
```
<name>/
├── transform.jq      # jq script (5-40 lines)
├── schema.json       # Input/output contract
├── test.sh          # Test suite (8-17 tests)
└── test-input-*.json # Test fixtures
```

## WHERE TO LOOK

| Task | File | Usage |
|------|------|-------|
| Get nested value | `crud-get/transform.jq` | `--arg path "user.name"` |
| Set nested value | `crud-set/transform.jq` | `--arg path "x" --arg value "y"` |
| Filter array | `array-filter/transform.jq` | `--arg condition ".age > 18"` |
| Validate type | `validate-types/transform.jq` | `--arg field "email" --arg type "string"` |

## CONVENTIONS

**Invocation Pattern:**
```bash
echo '{"user":{"name":"skogix"}}' | jq -f crud-get/transform.jq --arg path "user.name"
```

**Path Syntax:** Dot-separated for nested access
```bash
--arg path "user.profile.settings.theme"
```

**Composability:**
```bash
cat input.json | \
  jq -f crud-get/transform.jq --arg path "items" | \
  jq -f array-filter/transform.jq --arg condition ".active == true"
```

**Test Output Format:**
```
Test N: [Description]... PASS
```

## ANTI-PATTERNS

| DO NOT | Use Instead |
|--------|-------------|
| `// fallback` with falsy values | `try ($value \| fromjson) catch $value` |
| `!= null` for existence | `has()` function |
| Array ops without type check | `if (.items \| type) == "array" then` |
| Assume strings only | Test all JSON types |

## COMMANDS

```bash
# Run all tests
./test-all.sh

# Run specific transformation
./crud-get/test.sh

# Manual test
echo '{"a":{"b":1}}' | jq -f crud-get/transform.jq --arg path "a.b"
```

## NOTES

**Test Requirements:** Minimum 8-10 tests per transformation covering:
- Happy path (2-3 tests)
- Falsy values: `null`, `false`, `0`, `""`, `[]`, `{}`
- Non-existent paths
- All JSON types

**schema.json Required Fields:**
- `name`, `description`, `version`
- `input`, `args`, `output`
- `examples` (minimum 3)
- `tags`
