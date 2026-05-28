---
name: schema-validate
description: Validate JSON data against a JSON Schema. Use when the user asks to validate JSON against a schema, check if JSON conforms to a schema, test JSON data validity, or verify JSON structure matches a schema definition.
---

# Validate JSON Against Schema

Validate JSON data files against a JSON Schema definition.

## Usage

```bash
npx tsx scripts/validate.ts <json-file> --schema=<schema-file> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `json-file` | Yes | Path to the JSON file to validate |

### Options

| Option | Description |
|--------|-------------|
| `--schema=FILE` | Path to the JSON Schema file (required) |
| `--all-errors` | Report all errors, not just the first |
| `--strict` | Enable strict mode validation |
| `--verbose` | Show detailed validation output |
| `--format` | Output format: text (default), json |

### Output

Valid JSON:
```
Valid
  Schema: user-schema.json
  File: user.json
```

Invalid JSON:
```
Invalid (3 errors)
  1. /email: must match format "email"
  2. /age: must be >= 0
  3. /name: must be string
```

## Script Execution

```bash
npx tsx scripts/validate.ts data.json --schema=schema.json
npx tsx scripts/validate.ts data.json --schema=schema.json --all-errors
npx tsx scripts/validate.ts data.json --schema=schema.json --format=json
```

Run from the json-schema plugin directory: `~/.claude/plugins/cache/json-schema/`

## Batch Validation

Validate multiple files against the same schema using glob patterns:

```bash
# Validate all JSON files in a directory
for f in data/*.json; do npx tsx scripts/validate.ts "$f" --schema=schema.json; done
```

## JSON Output Format

When using `--format=json`:

```json
{
  "valid": false,
  "file": "user.json",
  "schema": "user-schema.json",
  "errors": [
    {
      "path": "/email",
      "message": "must match format \"email\"",
      "keyword": "format"
    }
  ]
}
```

## Error Messages

Common validation errors:
- `must be string` - Type mismatch
- `must match format "..."` - Format validation failed
- `must be >= N` / `must be <= N` - Number range violation
- `must NOT have additional properties` - Unknown property
- `must have required property '...'` - Missing required field
- `must match pattern "..."` - String pattern mismatch

## Related Skills

- Use `schema-meta` to validate that a schema is well-formed
- Use `schema-check` to validate a JSON file against its embedded `$schema`
