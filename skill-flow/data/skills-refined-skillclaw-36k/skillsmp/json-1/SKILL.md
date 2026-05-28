---
name: json
description: Parse, validate, transform, and manipulate JSON data. Use for JSON operations, schema validation, and data transformation.
allowed-tools: Read, Write, Bash
---

# JSON Processing Skill

Work with JSON data efficiently.

## 1. Parse and Query

**Using jq:**
```bash
# Pretty print
cat data.json | jq '.'

# Select field
cat data.json | jq '.users[0].name'

# Filter arrays
cat data.json | jq '.users[] | select(.age > 18)'

# Map transformation
cat data.json | jq '.users[] | {name, email}'

# Count elements
cat data.json | jq '.users | length'
```

## 2. Validate JSON

**Python:**
```python
import json
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number", "minimum": 0}
    },
    "required": ["name", "age"]
}

data = {"name": "John", "age": 30}
jsonschema.validate(instance=data, schema=schema)
```

## 3. Transform JSON

**jq transformations:**
```bash
# Rename keys
jq '.users[] | {fullName: .name, emailAddress: .email}'

# Flatten nested structure
jq '[.users[] | {name, city: .address.city}]'

# Group by
jq 'group_by(.category) | map({category: .[0].category, items: .})'

# Merge objects
jq '. + {newField: "value"}'
```

## 4. Convert Formats

**JSON to CSV:**
```bash
jq -r '.[] | [.name, .email, .age] | @csv' data.json > output.csv
```

**JSON to YAML:**
```bash
python -c "import json, yaml; print(yaml.dump(json.load(open('data.json'))))"
```

## When to Use This Skill

Use `/json` for JSON parsing, validation, transformation, and conversion tasks.
