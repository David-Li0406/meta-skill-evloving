---
name: schema-meta
description: Validate that a JSON Schema is well-formed and conforms to the JSON Schema specification. Use when the user asks to check if a schema is valid, verify schema syntax, validate schema structure, or check a JSON Schema file for errors.
---

# Validate JSON Schema (Meta-Validation)

Validate that a JSON Schema document is itself a valid schema according to the JSON Schema specification.

## Usage

```bash
npx tsx scripts/meta-validate.ts <schema-file> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `schema-file` | Yes | Path to the JSON Schema file to validate |

### Options

| Option | Description |
|--------|-------------|
| `--draft=VERSION` | JSON Schema draft version (draft-04, draft-06, draft-07, 2019-09, 2020-12). Default: auto-detect |
| `--strict` | Enable strict mode (additional validation rules) |
| `--verbose` | Show detailed validation information |

### Output

Valid schema:
```
Valid JSON Schema (draft-2020-12)
  Keywords: 5
  Definitions: 2
```

Invalid schema:
```
Invalid JSON Schema
  Error: "type" must be a string or array
  Path: /properties/name/type
```

## Script Execution

```bash
npx tsx scripts/meta-validate.ts schema.json
npx tsx scripts/meta-validate.ts schema.json --draft=draft-07
npx tsx scripts/meta-validate.ts schema.json --strict --verbose
```

Run from the json-schema plugin directory: `~/.claude/plugins/cache/json-schema/`

## Draft Version Detection

The script auto-detects the JSON Schema draft version from:
1. The `$schema` keyword in the document
2. Falls back to draft-2020-12 if not specified

Supported drafts:
- `draft-04` - JSON Schema Draft 4
- `draft-06` - JSON Schema Draft 6
- `draft-07` - JSON Schema Draft 7
- `2019-09` - JSON Schema Draft 2019-09
- `2020-12` - JSON Schema Draft 2020-12 (default)

## Strict Mode

When `--strict` is enabled, additional validations are performed:
- Disallow unknown keywords
- Require `$schema` declaration
- Validate format assertions by default

## Related Skills

- Use `schema-validate` to validate JSON data against a schema
- Use `schema-check` to validate a JSON file against its embedded `$schema`
