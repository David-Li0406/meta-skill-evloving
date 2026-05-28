---
name: schema-check
description: Validate a JSON file against the schema referenced in its $schema property. Use when the user asks to check JSON against its own schema, validate self-describing JSON, auto-validate JSON files, or verify JSON with embedded schema reference.
---

# Validate JSON Against Embedded $schema

Validate a JSON file against the schema referenced in its `$schema` property. This is useful for self-describing JSON documents that declare their own schema.

## Usage

```bash
npx tsx scripts/check.ts <json-file> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `json-file` | Yes | Path to the JSON file with `$schema` property |

### Options

| Option | Description |
|--------|-------------|
| `--all-errors` | Report all errors, not just the first |
| `--no-cache` | Bypass cache when fetching remote schemas |
| `--strict` | Enable strict mode validation |
| `--verbose` | Show detailed validation output |
| `--format` | Output format: text (default), json |

### Output

Valid JSON:
```
Valid
  Schema: https://json-schema.org/draft/2020-12/schema
  File: my-schema.json
```

Invalid JSON:
```
Invalid (2 errors)
  Schema: ./schemas/config.schema.json
  1. /settings/timeout: must be number
  2. /settings/retries: must be >= 0
```

No schema reference:
```
Error: No $schema property found in config.json
  Hint: Use schema-validate to validate against a specific schema
```

## Script Execution

```bash
npx tsx scripts/check.ts config.json
npx tsx scripts/check.ts config.json --all-errors
npx tsx scripts/check.ts config.json --no-cache --verbose
```

Run from the json-schema plugin directory: `~/.claude/plugins/cache/json-schema/`

## Schema Resolution

The `$schema` property can reference:

1. **Remote URLs** - Fetched and cached (24h TTL)
   ```json
   { "$schema": "https://json-schema.org/draft/2020-12/schema" }
   ```

2. **Local file paths** - Resolved relative to the JSON file
   ```json
   { "$schema": "./schemas/config.schema.json" }
   ```

3. **Absolute paths**
   ```json
   { "$schema": "/Users/joe/schemas/config.schema.json" }
   ```

## Common $schema Values

| Schema URI | Description |
|------------|-------------|
| `https://json-schema.org/draft/2020-12/schema` | JSON Schema Draft 2020-12 |
| `https://json-schema.org/draft/2019-09/schema` | JSON Schema Draft 2019-09 |
| `http://json-schema.org/draft-07/schema#` | JSON Schema Draft 7 |
| `http://json-schema.org/draft-06/schema#` | JSON Schema Draft 6 |
| `http://json-schema.org/draft-04/schema#` | JSON Schema Draft 4 |

## Caching

Remote schemas are cached for 24 hours using the OS temporary directory. Use `--no-cache` to bypass caching and fetch fresh schemas.

## Related Skills

- Use `schema-meta` to validate that a schema is well-formed
- Use `schema-validate` to validate JSON against an arbitrary schema file
