# jq-transforms

Schema-driven JSON transformation library for AI agents.

## Overview

A library of JSON transformations with clear input/output contracts designed to make JSON manipulation discoverable, understandable, and composable for AI agents.

## Philosophy

This library is built **for AI agents**, not humans. Each transformation:
- Has a clear schema (input/output contract)
- Is tested directly
- Is minimal and readable
- Can be understood by reading the schema
- Can be composed with other transformations
- Can be verified by running tests

See [vision.md](../../todo/jq-transforms/vision.md) for full project philosophy.

## Installation

Requires `jq` (version 1.6+):

```bash
# Check if jq is installed
jq --version

# Install on macOS
brew install jq

# Install on Ubuntu/Debian
apt-get install jq
```

## Available Transformations

### CRUD Operations

#### crud-get
Get value at a nested path with optional default.

**Usage:**
```bash
jq -f crud-get/transform.jq --arg path "user.name" input.json
jq -f crud-get/transform.jq --arg path "user.email" --arg default "unknown" input.json
```

**Example:**
```bash
echo '{"user":{"name":"skogix"}}' | jq -f crud-get/transform.jq --arg path "user.name"
# Output: "skogix"
```

#### crud-set
Set value at a nested path, creating intermediate objects as needed.

**Usage:**
```bash
jq -f crud-set/transform.jq --arg path "user.name" --arg value "newname" input.json
```

**Example:**
```bash
echo '{}' | jq -f crud-set/transform.jq --arg path "user.profile.age" --arg value "30"
# Output: {"user":{"profile":{"age":"30"}}}
```

#### crud-delete
Delete value at a nested path.

**Usage:**
```bash
jq -f crud-delete/transform.jq --arg path "user.email" input.json
```

**Example:**
```bash
echo '{"user":{"name":"skogix","email":"test@example.com"}}' | \
  jq -f crud-delete/transform.jq --arg path "user.email"
# Output: {"user":{"name":"skogix"}}
```

## Composition

Transformations can be chained via pipes:

```bash
# Get value, modify it externally, set it back
cat input.json | \
  jq -f crud-get/transform.jq --arg path "user.name" | \
  # ... some processing ... | \
  jq -f crud-set/transform.jq --arg path "user.name" --arg value "$(cat -)"
```

```bash
# Extract, transform, and delete
cat config.json | \
  jq -f crud-get/transform.jq --arg path "database.host" > old-host.txt && \
cat config.json | \
  jq -f crud-set/transform.jq --arg path "database.host" --arg value "new-host" | \
  jq -f crud-delete/transform.jq --arg path "database.old_host" > new-config.json
```

## Schema Format

Each transformation has a `schema.json` file with:

```json
{
  "name": "transformation-name",
  "description": "What it does",
  "version": "1.0.0",
  "input": {
    "type": "object",
    "description": "Input shape"
  },
  "args": {
    "arg_name": {
      "type": "string",
      "required": true,
      "description": "What this argument does"
    }
  },
  "output": {
    "type": "object",
    "description": "Output shape"
  },
  "examples": [...],
  "tags": ["category", "keywords"]
}
```

## Testing

Each transformation has its own test suite:

```bash
# Run specific transformation tests
./crud-get/test.sh

# Run all tests
./test-all.sh
```

## Directory Structure

```
jq-transforms/
├── README.md              # This file
├── test-all.sh           # Run all tests
├── crud-get/
│   ├── transform.jq      # The transformation
│   ├── schema.json       # Input/output contract
│   ├── test.sh          # Test suite
│   └── test-input-*.json # Test fixtures
├── crud-set/
│   └── ...
└── crud-delete/
    └── ...
```

## Adding New Transformations

1. Create a new directory with the transformation name
2. Create `transform.jq` with the jq code
3. Create `schema.json` with the contract
4. Create `test.sh` with test cases
5. Create test input files as needed
6. Run `./test-all.sh` to verify

See existing transformations for examples.

## Design Principles

1. **Schema-driven**: Every transformation has input/output/args schema
2. **Test-first**: Tests show usage and verify behavior
3. **Minimal**: Less code, fewer bugs, easier to understand
4. **Composable**: Transformations chain via pipes
5. **Direct**: No wrappers hiding what actually runs
6. **Isolated**: Each transformation is self-contained

## Use Cases

- **Structured I/O**: Ensure consistent JSON shapes across projects
- **Config Management**: Update nested configuration values
- **Data Transformation**: Normalize data from different sources
- **API Response Handling**: Extract and transform API responses
- **Log Processing**: Filter and aggregate JSON logs

## Future Transformations

See [backlog.md](../../todo/jq-transforms/backlog.md) for planned transformations including:
- Array operations (map, filter, reduce)
- String operations (split, join, replace)
- Validation operations (schema, type, format)
- Aggregation operations (group-by, sort-by, count)

## Resources

- [jq Manual](https://jqlang.github.io/jq/manual/)
- [jq Patterns](../../todo/jq-transforms/patterns.md)
- [Examples](../../todo/jq-transforms/examples.md)
- [Vision](../../todo/jq-transforms/vision.md)

## License

Part of the SkogAI project.
