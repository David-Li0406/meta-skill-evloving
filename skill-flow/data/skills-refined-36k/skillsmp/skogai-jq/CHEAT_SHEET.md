# jq-transforms Cheat Sheet

Quick reference for using jq-transforms. Path: `~/skogix/todo/jq-transforms/`

## Usage Pattern

```bash
jq -f <transform-path>/transform.jq [--arg key val] [--argjson key json] input.json
```

## Transform Index

### CRUD Operations

| Transform | Args | Example |
|-----------|------|---------|
| `crud-get` | `path`, `default?` | `--arg path "user.name" --arg default "unknown"` |
| `crud-set` | `path`, `value` | `--arg path "user.age" --arg value "30"` |
| `crud-delete` | `path` | `--arg path "user.old_field"` |
| `crud-has` | `path` | `--arg path "user.email"` |
| `crud-merge` | `source_path`, `target_path` | `--arg source_path "updates" --arg target_path "user"` |
| `crud-query` | `array_field`, `field`, `value` | `--arg array_field "users" --arg field "active" --arg value "true"` |

### Array Operations

| Transform | Args | Example |
|-----------|------|---------|
| `array-filter` | `array_field`, `field`, `value` | `--arg array_field "items" --arg field "status" --arg value "active"` |
| `array-map` | `array_field`, `field` | `--arg array_field "items" --arg field "name"` |
| `array-reduce` | `array_field`, `op`, `field?` | `--arg array_field "prices" --arg op "sum"` |
| `array-unique` | `array_field` | `--arg array_field "items"` |
| `array-flatten` | `array_field`, `depth?` | `--arg array_field "nested" --arg depth "1"` |
| `array-append` | `array_field`, `value` | `--arg array_field "items" --arg value "new"` |
| `array-prepend` | `array_field`, `value` | `--arg array_field "items" --arg value "first"` |
| `array-chunk` | `array_field`, `size` | `--arg array_field "items" --arg size "10"` |

### String Operations

| Transform | Args | Example |
|-----------|------|---------|
| `string-split` | `field`, `separator` | `--arg field "text" --arg separator ","` |
| `string-join` | `array_field`, `separator` | `--arg array_field "words" --arg separator " "` |
| `string-replace` | `field`, `pattern`, `replacement` | `--arg field "text" --arg pattern "old" --arg replacement "new"` |
| `string-match` | `field`, `pattern` | `--arg field "text" --arg pattern "^[a-z]+$"` |
| `string-trim` | `field` | `--arg field "text"` |
| `string-truncate` | `field`, `length` | `--arg field "text" --arg length "100"` |

### Extraction

| Transform | Args | Example |
|-----------|------|---------|
| `extract-urls` | `field` | `--arg field "content"` |
| `extract-code-blocks` | `field` | `--arg field "markdown"` |
| `extract-mentions` | `field` | `--arg field "message"` |
| `extract-first-line` | `field` | `--arg field "text"` |
| `extract-role-content` | `array_field`, `role` | `--arg array_field "messages" --arg role "user"` |

### Filtering

| Transform | Args | Example |
|-----------|------|---------|
| `filter-by-pattern` | `array_field`, `field`, `pattern` | `--arg array_field "users" --arg field "email" --arg pattern ".*@example.com"` |
| `filter-by-role` | `array_field`, `role` | `--arg array_field "messages" --arg role "assistant"` |
| `filter-by-date-range` | `array_field`, `field`, `start`, `end` | `--arg array_field "events" --arg field "date" --arg start "2024-01-01"` |

### Validation

| Transform | Args | Example |
|-----------|------|---------|
| `validate-required` | `fields` (comma-sep) | `--arg fields "name,email,age"` |
| `validate-types` | `field_types` (JSON) | `--argjson field_types '{"age":"number","name":"string"}'` |
| `validate-range` | `field`, `min`, `max` | `--arg field "age" --arg min "0" --arg max "120"` |
| `validate-format` | `field`, `format` | `--arg field "email" --arg format "email"` |
| `schema-validation` | `schema` (JSON) | `--argjson schema '{"type":"object","required":["name"]}'` |

### Type Checks (return boolean)

| Transform | Args | Example |
|-----------|------|---------|
| `is-timestamp` | `field` | `--arg field "created_at"` |
| `is-uuid` | `field` | `--arg field "id"` |
| `is-empty-string` | `field` | `--arg field "text"` |
| `has-url` | `field` | `--arg field "content"` |
| `has-code-block` | `field` | `--arg field "markdown"` |
| `has-field` | `path` | `--arg path "user.email"` |

### Type Conversions

| Transform | Args | Example |
|-----------|------|---------|
| `to-string` | `field` | `--arg field "value"` |
| `to-number` | `field` | `--arg field "value"` |
| `to-boolean` | `field` | `--arg field "value"` |
| `to-array` | `field` | `--arg field "value"` |
| `to-object` | `field` | `--arg field "value"` |

### Utilities

| Transform | Args | Example |
|-----------|------|---------|
| `pipe` | `steps` (JSON array) | `--argjson steps '[{"op":"set","path":"x","value":1}]'` |
| `pick-fields` | `fields` (comma-sep) | `--arg fields "name,email,age"` |
| `copy-field` | `source_path`, `target_path` | `--arg source_path "old" --arg target_path "new"` |
| `rename-field` | `old_path`, `new_path` | `--arg old_path "old_name" --arg new_path "new_name"` |
| `add-field` | `path`, `value` | `--arg path "new_field" --arg value "value"` |
| `remove-field` | `path` | `--arg path "field_to_remove"` |
| `count-by-field` | `array_field`, `field` | `--arg array_field "items" --arg field "category"` |
| `group-by-field` | `array_field`, `field` | `--arg array_field "items" --arg field "status"` |
| `sort-by-field` | `array_field`, `field`, `order?` | `--arg array_field "items" --arg field "name" --arg order "asc"` |
| `deduplicate-by-content` | `array_field` | `--arg array_field "items"` |
| `generate-message-id` | `strategy?`, `field?` | `--arg strategy "hash" --arg field "id"` |
| `generate-stats` | `array_field`, `field?` | `--arg array_field "numbers" --arg field "value"` |
| `format-message` | `template` | `--arg template "{role}: {content}"` |
| `normalize-timestamp` | `field` | `--arg field "created_at"` |

## Common Patterns

### Chain multiple transforms
```bash
cat data.json \
  | jq -f crud-get/transform.jq --arg path "users" \
  | jq -f array-filter/transform.jq --arg array_field "." --arg field "active" --arg value "true" \
  | jq -f array-map/transform.jq --arg array_field "." --arg field "email"
```

### Use pipe transform for complex pipelines
```bash
cat data.json | jq -f pipe/transform.jq --argjson steps '[
  {"op": "set", "path": "user.age", "value": 30},
  {"op": "set", "path": "user.active", "value": true},
  {"op": "delete", "path": "user.temp"}
]'
```

### Extract and process
```bash
cat messages.json \
  | jq -f extract-role-content/transform.jq --arg array_field "messages" --arg role "user" \
  | jq -f array-map/transform.jq --arg array_field "." --arg field "content"
```

## Quick Tips

1. **Use `-c` for compact output**: `jq -c -f transform.jq`
2. **Use `-S` for sorted keys**: `jq -S -f transform.jq`
3. **Boolean/number args**: `--argjson value "true"` not `--arg value "true"`
4. **Check schema**: `cat <transform>/schema.json` for full contract
5. **See examples**: `cat <transform>/test.sh` for real usage
6. **Path syntax**: Dots for nesting `"user.profile.name"`
7. **All transforms handle falsy values**: `null`, `false`, `0`, `""`, `[]`, `{}`
