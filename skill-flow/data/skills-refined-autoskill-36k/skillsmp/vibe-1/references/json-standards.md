# JSON/JSONL Standards Catalog - Vibe Canonical Reference

**Version:** 1.0.0
**Last Updated:** 2026-01-21
**Purpose:** Canonical JSON/JSONL standards for vibe skill validation

---

## Table of Contents

1. [JSON Formatting](#json-formatting)
2. [JSONL Format](#jsonl-format)
3. [Beads JSONL Schema](#beads-jsonl-schema)
4. [Configuration Files](#configuration-files)
5. [JSON Schema](#json-schema)
6. [Tooling](#tooling)
7. [Compliance Assessment](#compliance-assessment)

---

## JSON Formatting

### Standard Format

```json
{
  "name": "example",
  "version": "1.0.0",
  "config": {
    "timeout": 30,
    "retries": 3,
    "enabled": true
  },
  "items": [
    "first",
    "second",
    "third"
  ]
}
```

### Formatting Rules

| Rule | Example | Why |
|------|---------|-----|
| 2-space indent | `  "key": "value"` | Readability |
| Double quotes only | `"key"` not `'key'` | JSON spec |
| No trailing commas | `["a", "b"]` | JSON spec |
| Trailing newline | File ends with `\n` | POSIX, git diffs |
| UTF-8 encoding | Always | Compatibility |

### Key Naming Conventions

| Convention | Use For | Example |
|------------|---------|---------|
| `camelCase` | JavaScript/TypeScript | `"apiVersion"` |
| `snake_case` | Python, beads | `"issue_type"` |
| `kebab-case` | Avoid | - |
| `UPPER_CASE` | Environment vars | `"DATABASE_URL"` |

**Rule:** Be consistent within a file. Match ecosystem convention.

---

## JSONL Format

### What is JSONL?

JSON Lines: one valid JSON object per line, newline-delimited.

```jsonl
{"id": "abc-123", "status": "open", "title": "First issue"}
{"id": "abc-124", "status": "closed", "title": "Second issue"}
{"id": "abc-125", "status": "open", "title": "Third issue"}
```

### When to Use

| Use JSONL | Use JSON |
|-----------|----------|
| Append-only data | Single config |
| Streaming ingestion | Nested data |
| Line-by-line processing | Small datasets |
| Beads issues | API responses |
| Large datasets | Human-edited |

### JSONL Rules

| Rule | Rationale |
|------|-----------|
| One object per line | Enables grep/head/tail |
| No trailing comma | Each line is complete |
| No array wrapper | Not `[{...}, {...}]` |
| Newline after last | Append-friendly |
| UTF-8, no BOM | Compatibility |

### Processing JSONL

```bash
# Count records
wc -l issues.jsonl

# Filter by field
jq -c 'select(.status == "open")' issues.jsonl

# Extract field
jq -r '.title' issues.jsonl

# Pretty-print one record
head -1 issues.jsonl | jq .

# Append new record
echo '{"id": "new", "status": "open"}' >> issues.jsonl

# Convert JSON array to JSONL
jq -c '.[]' array.json > data.jsonl

# Convert JSONL to JSON array
jq -s '.' data.jsonl > array.json
```

---

## Beads JSONL Schema

### Issue Record Schema

```json
{
  "id": "prefix-xxxx",
  "title": "Issue title",
  "status": "open",
  "priority": 2,
  "issue_type": "task",
  "owner": "user@example.com",
  "created_at": "2026-01-15T08:18:34.317984-05:00",
  "created_by": "User Name",
  "updated_at": "2026-01-15T08:42:39.253689-05:00",
  "closed_at": null,
  "close_reason": null,
  "dependencies": []
}
```

### Field Reference

| Field | Type | Required | Values |
|-------|------|----------|--------|
| `id` | string | Yes | `prefix-xxxx` |
| `title` | string | Yes | Brief description |
| `status` | string | Yes | `open`, `in_progress`, `closed` |
| `priority` | integer | Yes | 0-4 (0=critical) |
| `issue_type` | string | Yes | `task`, `bug`, `feature`, `epic` |
| `owner` | string | No | Email address |
| `created_at` | string | Yes | ISO 8601 |
| `updated_at` | string | Yes | ISO 8601 |
| `closed_at` | string | No | ISO 8601 or null |
| `dependencies` | array | No | Dependency objects |

### Dependency Object

```json
{
  "issue_id": "prefix-child",
  "depends_on_id": "prefix-parent",
  "type": "parent-child",
  "created_at": "2026-01-15T08:19:32.440350-05:00"
}
```

---

## Configuration Files

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "strict": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

### package.json

```json
{
  "name": "package-name",
  "version": "1.0.0",
  "description": "Brief description",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint ."
  },
  "dependencies": {},
  "devDependencies": {}
}
```

### VS Code settings.json

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true
}
```

---

## JSON Schema

### Defining Schemas

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/config.schema.json",
  "title": "Configuration",
  "type": "object",
  "required": ["name", "version"],
  "properties": {
    "name": {
      "type": "string",
      "description": "Project name",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "enabled": {
      "type": "boolean",
      "default": true
    }
  },
  "additionalProperties": false
}
```

### Schema Validation

```bash
# Using ajv-cli
npx ajv validate -s schema.json -d config.json

# Using Python jsonschema
python -c "
import json
from jsonschema import validate
with open('schema.json') as s, open('config.json') as c:
    validate(json.load(c), json.load(s))
"
```

---

## Tooling

### Formatting

```bash
# jq - Format and validate
jq . config.json > formatted.json

# Prettier - Format with config
npx prettier --write '**/*.json'

# Python - Format
python -m json.tool config.json
```

### Validation

```bash
# jq - Check valid JSON
jq empty config.json && echo "Valid"

# Python - Check valid JSON
python -c "import json; json.load(open('config.json'))"

# Node - Check valid JSON
node -e "require('./config.json')"
```

### Editor Configuration

**.editorconfig:**
```ini
[*.json]
indent_style = space
indent_size = 2
insert_final_newline = true
charset = utf-8

[*.jsonl]
indent_style = space
indent_size = 0
insert_final_newline = true
```

**.prettierrc:**
```json
{
  "tabWidth": 2,
  "useTabs": false,
  "trailingComma": "none",
  "singleQuote": false
}
```

---

## Compliance Assessment

**Use letter grades + evidence, NOT numeric scores.**

### Assessment Categories

| Category | Evidence Required |
|----------|------------------|
| **Formatting** | jq validation, indentation, newlines |
| **Schema** | Validation errors, required fields |
| **Key Naming** | Consistency check |
| **JSONL Integrity** | Line count = record count |

### Grading Scale

| Grade | Criteria |
|-------|----------|
| A+ | All files validate, 2-space, UTF-8, schema valid |
| A | Valid JSON, consistent formatting |
| A- | Minor formatting inconsistencies |
| B | Valid but poorly formatted |
| C | Parse errors |

### Validation Commands

```bash
# Validate JSON
find . -name '*.json' -exec jq empty {} \; 2>&1 | grep -c "parse error"
# Should be 0

# Check indentation
jq . config.json | head -5

# JSONL: validate line count
wc -l data.jsonl
jq -c '.' data.jsonl | wc -l
# Should match

# JSONL: validate each line
while IFS= read -r line; do echo "$line" | jq empty; done < data.jsonl
```

### Example Assessment

```markdown
## JSON/JSONL Standards Compliance

| Category | Grade | Evidence |
|----------|-------|----------|
| Formatting | A+ | 18/18 validate, 2-space |
| Schema | A+ | 1247/1247 records pass |
| Key Naming | A | Consistent snake_case |
| JSONL | A+ | Line count matches |
| **OVERALL** | **A+** | **0 findings** |
```

---

## Additional Resources

- [JSON Spec](https://www.json.org/)
- [JSON Lines](https://jsonlines.org/)
- [JSON Schema](https://json-schema.org/)
- [jq Manual](https://stedolan.github.io/jq/manual/)

---

**Related:** Quick reference in Tier 1 `json.md`
