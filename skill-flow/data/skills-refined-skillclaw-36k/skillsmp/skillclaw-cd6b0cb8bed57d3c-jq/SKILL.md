---
name: jq
description: Use this skill when you need to filter, transform, and manipulate JSON data from the command line.
---

# jq — JSON Processor

## Installation

**macOS / Linux (Homebrew):**
```bash
brew install jq
```

**All platforms:** See [jqlang.org/download](https://jqlang.org/download/) for packages, binaries, and build instructions.

## Basic Usage

```bash
# Pretty-print JSON
jq '.' file.json

# Filter specific field
jq '.fieldName' file.json

# Filter array element by index
jq '.[index]' file.json

# Output all elements from arrays
jq '.[*]' file.json

# Parse from stdin
cat file.json | jq '.fieldName'

# Load JSON from URL
curl -s "http://example.com/file.json" | jq '.fieldName'
```

## Filtering & Transformation

```bash
# Select multiple fields
jq '{field1: .field1, field2: .field2}' file.json

# Query nested data
jq '.outerField.innerField' file.json

# Filter by condition
jq 'select(.fieldName == "value")' file.json

# Modify field value
jq '.fieldName = "newValue"' file.json

# Delete a field
jq 'del(.fieldName)' file.json
```

## Array Operations

```bash
# Count elements
jq '.arrayName | length' file.json

# Apply function to each element
jq '.arrayName[] | .fieldName' file.json

# First element
jq '.[0]' file.json

# First element's key
jq '.[0].key_name' file.json
```

## Advanced Operations

```bash
# Concatenate fields
jq '.field1 + " " + .field2' file.json

# Group by field
jq 'group_by(.fieldName)' file.json

# Sort by field
jq 'sort_by(.fieldName)' file.json

# Find unique values
jq 'unique' file.json

# Print keys and values
jq 'to_entries | .[] | "\(.key): \(.value)"' file.json

# Combine two JSON files
jq -s '.[0] + .[1]' file1.json file2.json

# Compact output (no whitespace)
jq -c '.' file.json
```