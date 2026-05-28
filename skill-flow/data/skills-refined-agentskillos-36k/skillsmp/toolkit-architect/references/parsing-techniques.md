# Parsing Techniques

## Table of Contents

- [Overview](#overview)
- [Technique Comparison](#technique-comparison)
- [Method 1: Basic sed/awk Parsing](#method-1-basic-sedawk-parsing)
- [Method 2: yq Parser (Recommended)](#method-2-yq-parser-recommended)
- [Method 3: Python Parser](#method-3-python-parser)
- [Method 4: jq for JSON Workflows](#method-4-jq-for-json-workflows)
- [Comparison Examples](#comparison-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Performance Benchmarks](#performance-benchmarks)
- [Conclusion](#conclusion)

## Overview

This guide covers comprehensive techniques for parsing YAML frontmatter and markdown content from `.local.md` files. Choose the appropriate technique based on your requirements.

## Technique Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| sed/awk | No dependencies | Fragile | Simple fields |
| yq | Robust, handles complex YAML | Requires installation | Production use |
| Python | Full YAML support, types | Python dependency | Complex validation |
| jq | JSON-native | YAML → JSON conversion needed | JSON-heavy workflows |

## Method 1: Basic sed/awk Parsing

### Extract Frontmatter

```bash
#!/bin/bash
# Extract everything between --- markers
extract_frontmatter() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        echo "" >&2
        return 1
    fi

    sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$file"
}

# Usage
FRONTMATTER=$(extract_frontmatter "$STATE_FILE")
```

### Read String Fields

```bash
#!/bin/bash
read_string_field() {
    local frontmatter="$1"
    local field="$2"

    echo "$frontmatter" | grep "^${field}:" | \
        sed "s/^${field}: *//" | \
        sed 's/^"\(.*\)"$/\1/' | \
        sed "s/^'\(.*\)'$/\1/" | \
        xargs
}

# Usage
MODE=$(read_string_field "$FRONTMATTER" "mode")
```

### Read Boolean Fields

```bash
#!/bin/bash
read_boolean_field() {
    local frontmatter="$1"
    local field="$2"

    local value
    value=$(echo "$frontmatter" | grep "^${field}:" | \
        sed "s/^${field}: *//" | \
        tr -d '[:space:]')

    case "$value" in
        true|True|TRUE|1|yes|Yes|YES)
            echo "true"
            return 0
            ;;
        false|False|FALSE|0|no|No|NO|"")
            echo "false"
            return 0
            ;;
        *)
            echo "false"
            echo "⚠️ Invalid boolean value for '$field': '$value'" >&2
            return 1
            ;;
    esac
}

# Usage
ENABLED=$(read_boolean_field "$FRONTMATTER" "enabled")
```

### Read Numeric Fields

```bash
#!/bin/bash
read_numeric_field() {
    local frontmatter="$1"
    local field="$2"

    local value
    value=$(echo "$frontmatter" | grep "^${field}:" | \
        sed "s/^${field}: *//" | \
        xargs)

    # Validate it's numeric
    if ! [[ "$value" =~ ^[0-9]+$ ]] && ! [[ "$value" =~ ^[0-9]+\.[0-9]+$ ]]; then
        echo "0" >&2
        echo "⚠️ Invalid numeric value for '$field': '$value'" >&2
        return 1
    fi

    echo "$value"
}

# Usage
MAX_RETRIES=$(read_numeric_field "$FRONTMATTER" "max_retries")
```

### Read Array Fields

```bash
#!/bin/bash
read_array_field() {
    local frontmatter="$1"
    local field="$2"

    local line
    line=$(echo "$frontmatter" | grep "^${field}:")

    if [[ -z "$line" ]]; then
        echo ""
        return 0
    fi

    # Extract array content
    local array_content
    array_content=$(echo "$line" | sed "s/^${field}: *\[//" | sed 's/\]//')

    # Split by comma and clean up
    local items=()
    IFS=',' read -ra items <<< "$array_content"

    local result=""
    for item in "${items[@]}"; do
        # Remove quotes and whitespace
        local cleaned
        cleaned=$(echo "$item" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//' | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/")
        result="${result}${cleaned}"$'\n'
    done

    echo -n "$result"
}

# Usage
TAGS=$(read_array_field "$FRONTMATTER" "tags")
# Parse newline-separated tags
IFS=$'\n' read -rd '' -a TAG_ARRAY <<< "$TAGS"
```

### Read Markdown Body

```bash
#!/bin/bash
extract_markdown_body() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        echo ""
        return 1
    fi

    # Get everything after second ---
    awk '/^---$/{i++; next} i>=2' "$file"
}

# Usage
BODY=$(extract_markdown_body "$STATE_FILE")
```

## Method 2: yq Parser (Recommended)

### Installation

```bash
# macOS
brew install yq

# Ubuntu/Debian
sudo add-apt-repository ppa:rmescandon/yq
sudo apt update && sudo apt install yq

# Using pip
pip install yq
```

### Basic Field Reading

```bash
#!/bin/bash
STATE_FILE=".claude/my-plugin.local.md"

# Read simple field
ENABLED=$(yq eval '.enabled' "$STATE_FILE")

# Read with default
MODE=$(yq eval '.mode // "standard"' "$STATE_FILE")

# Read nested field
VALIDATION_LEVEL=$(yq eval '.settings.validation_level' "$STATE_FILE")
```

### Reading Arrays

```bash
#!/bin/bash
# Read all array items
EXTENSIONS=$(yq eval '.allowed_extensions[]' "$STATE_FILE")

# Read specific array item
FIRST_EXTENSION=$(yq eval '.allowed_extensions[0]' "$STATE_FILE")

# Array length
NUM_EXTENSIONS=$(yq eval '.allowed_extensions | length' "$STATE_FILE")
```

### Reading Complex Structures

```bash
#!/bin/bash
# Read entire section as JSON
SETTINGS_JSON=$(yq eval '.settings' "$STATE_FILE")

# Check if field exists
if [[ "$(yq eval '.custom_field // empty' "$STATE_FILE")" != "empty" ]]; then
    CUSTOM_FIELD=$(yq eval '.custom_field' "$STATE_FILE")
fi

# Conditional reading
MODE=$(yq eval 'if .mode then .mode else "standard" end' "$STATE_FILE")
```

### Array to Bash Array

```bash
#!/bin/bash
# Convert YAML array to bash array
IFS=$'\n' read -rd '' -a EXTENSIONS <<< "$(yq eval -r '.allowed_extensions[]' "$STATE_FILE")"

# Usage
for ext in "${EXTENSIONS[@]}"; do
    echo "Extension: $ext"
done
```

### Error Handling with yq

```bash
#!/bin/bash
safe_yq_eval() {
    local expression="$1"
    local default="$2"

    local result
    result=$(yq eval "$expression" "$STATE_FILE" 2>/dev/null)

    if [[ $? -eq 0 ]] && [[ -n "$result" ]] && [[ "$result" != "null" ]]; then
        echo "$result"
    else
        echo "$default"
    fi
}

# Usage
ENABLED=$(safe_yq_eval '.enabled' "true")
```

## Method 3: Python Parser

### Basic Frontmatter Parser

```python
#!/usr/bin/env python3
import yaml
import sys
from typing import Dict, Any, Tuple

def parse_frontmatter(file_path: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter and markdown body."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return {}, ""

    if not content.startswith('---'):
        return {}, content

    try:
        _, frontmatter_str, body = content.split('---', 2)
        config = yaml.safe_load(frontmatter_str) or {}
        return config, body.strip()
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}", file=sys.stderr)
        return {}, body.strip()

def get_nested_value(config: Dict[str, Any], path: str, default=None):
    """Get nested value using dot notation."""
    keys = path.split('.')
    value = config

    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default

    return value

# Usage
config, body = parse_frontmatter('.claude/my-plugin.local.md')
enabled = config.get('enabled', True)
mode = config.get('mode', 'standard')
validation_level = get_nested_value(config, 'settings.validation_level', 'standard')
```

### Advanced Python Parser with Types

```python
#!/usr/bin/env python3
import yaml
import sys
from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass, field

@dataclass
class PluginConfig:
    version: str = "2.0.0"
    enabled: bool = True
    mode: str = "standard"
    max_retries: int = 3
    settings: Dict[str, Any] = field(default_factory=dict)
    environment: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    _raw_config: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_file(cls, file_path: str) -> 'PluginConfig':
        """Load configuration from file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            if not content.startswith('---'):
                return cls()

            _, frontmatter_str, _ = content.split('---', 2)
            raw_config = yaml.safe_load(frontmatter_str) or {}

            return cls(
                version=raw_config.get('version', '2.0.0'),
                enabled=raw_config.get('enabled', True),
                mode=raw_config.get('mode', 'standard'),
                max_retries=raw_config.get('max_retries', 3),
                settings=raw_config.get('settings', {}),
                environment=raw_config.get('environment', {}),
                tags=raw_config.get('tags', []),
                _raw_config=raw_config
            )
        except Exception as e:
            print(f"Error loading config: {e}", file=sys.stderr)
            return cls()

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation."""
        return get_nested_value(self._raw_config, key, default)

    def is_enabled(self) -> bool:
        """Check if plugin is enabled."""
        return self.enabled

# Usage
config = PluginConfig.from_file('.claude/my-plugin.local.md')

if config.is_enabled():
    print(f"Plugin enabled in {config.mode} mode")
    print(f"Max retries: {config.max_retries}")
    print(f"Settings: {config.settings}")
```

### Python with Validation

```python
#!/usr/bin/env python3
import yaml
import sys
from typing import Any, Dict, List, Union

class ConfigValidator:
    """Validate configuration settings."""
    
    VALID_MODES = ['strict', 'standard', 'lenient']
    VALID_NOTIFICATION_LEVELS = ['debug', 'info', 'warning', 'error']
    
    @staticmethod
    def validate(config: Dict[str, Any]) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Check enabled
        if 'enabled' in config and not isinstance(config['enabled'], bool):
            errors.append("Field 'enabled' must be boolean")
        
        # Check mode
        if 'mode' in config:
            if config['mode'] not in ConfigValidator.VALID_MODES:
                errors.append(f"Field 'mode' must be one of: {', '.join(ConfigValidator.VALID_MODES)}")
        
        # Check max_retries
        if 'max_retries' in config:
            if not isinstance(config['max_retries'], int) or config['max_retries'] < 0 or config['max_retries'] > 10:
                errors.append("Field 'max_retries' must be integer between 0 and 10")
        
        # Check notification_level
        if 'notification_level' in config:
            if config['notification_level'] not in ConfigValidator.VALID_NOTIFICATION_LEVELS:
                errors.append(f"Field 'notification_level' must be one of: {', '.join(ConfigValidator.VALID_NOTIFICATION_LEVELS)}")
        
        return errors
    
    @staticmethod
    def validate_and_report(config: Dict[str, Any]) -> bool:
        """Validate and report errors."""
        errors = ConfigValidator.validate(config)
        
        if errors:
            print("Configuration errors:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            return False
        
        return True

# Usage
config, _ = parse_frontmatter('.claude/my-plugin.local.md')

if not ConfigValidator.validate_and_report(config):
    sys.exit(1)

print("Configuration is valid")
```

## Method 4: jq for JSON Workflows

### Convert YAML to JSON

```bash
#!/bin/bin
# Convert YAML to JSON for jq processing
CONFIG_JSON=$(yq eval -o=json '.' "$STATE_FILE")

# Read field using jq
ENABLED=$(echo "$CONFIG_JSON" | jq -r '.enabled')
MODE=$(echo "$CONFIG_JSON" | jq -r '.mode // "standard"')
```

### Complex Queries with jq

```bash
#!/bin/bash
# Get all settings keys
SETTINGS_KEYS=$(echo "$CONFIG_JSON" | jq -r '.settings | keys[]')

# Check if any extension matches
HAS_TS=$(echo "$CONFIG_JSON" | jq -r '.allowed_extensions[] | select(. == ".ts")')
if [[ -n "$HAS_TS" ]]; then
    echo "TypeScript files allowed"
fi

# Conditional value
NOTIFICATION_LEVEL=$(echo "$CONFIG_JSON" | jq -r 'if .notification_level then .notification_level else "info" end')
```

## Comparison Examples

### Same Operation, Different Methods

**Read boolean field:**

```bash
# Method: sed
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

# Method: yq
ENABLED=$(yq eval '.enabled' "$STATE_FILE")

# Method: Python
ENABLED=config.get('enabled', True)
```

**Read array field:**

```bash
# Method: sed
EXTENSIONS=$(echo "$FRONTMATTER" | grep '^allowed_extensions:')

# Method: yq
IFS=$'\n' read -rd '' -a EXTENSIONS <<< "$(yq eval -r '.allowed_extensions[]' "$STATE_FILE")"

# Method: Python
EXTENSIONS=config.get('allowed_extensions', [])
```

## Best Practices

### Choose the Right Method

1. **Simple fields, no dependencies**: Use sed/awk
2. **Production, robust parsing**: Use yq
3. **Complex validation, type safety**: Use Python
4. **JSON-heavy workflows**: Use jq

### Error Handling

```bash
#!/bin/bash
robust_parse() {
    local method="$1"
    
    case "$method" in
        yq)
            if ! command -v yq &> /dev/null; then
                echo "❌ yq not installed, falling back to sed" >&2
                method="sed"
            fi
            ;;
        python)
            if ! command -v python3 &> /dev/null; then
                echo "❌ Python3 not installed, falling back to sed" >&2
                method="sed"
            fi
            ;;
    esac
    
    # Proceed with selected method
}
```

### Performance Considerations

```bash
# Good: Read all fields at once
FRONTMATTER=$(extract_frontmatter "$STATE_FILE")
ENABLED=$(read_boolean_field "$FRONTMATTER" "enabled")
MODE=$(read_string_field "$FRONTMATTER" "mode")

# Bad: Multiple file reads
ENABLED=$(yq eval '.enabled' "$STATE_FILE")
MODE=$(yq eval '.mode' "$STATE_FILE")  # Second file read
```

### Shell Safety

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Quote variables
echo "$VALUE"  # Good
echo $VALUE   # Bad - word splitting

# Use arrays for lists
IFS=$'\n' read -rd '' -a ARRAY <<< "$VALUE"
for item in "${ARRAY[@]}"; do  # Good
    echo "$item"
done
```

## Troubleshooting

### Common Parsing Issues

**Issue: Quoted values with special characters**

```bash
# Problem
VALUE=$(read_string_field "$FRONTMATTER" "pattern")
# Input: pattern: "[a-z]+"
# Result: [a-z]+ (brackets interpreted by shell)

# Solution
VALUE=$(read_string_field "$FRONTMATTER" "pattern")
# In usage, quote: echo "$VALUE"
```

**Issue: Arrays with mixed types**

```bash
# YAML
items: ["string", 123, true]

# sed approach - fragile
# yq approach - handles correctly
ITEMS=$(yq eval -r '.items[]' "$STATE_FILE")

# Python approach - best
ITEMS=config.get('items', [])
```

**Issue: Nested objects**

```bash
# YAML
settings:
  database:
    host: localhost
    port: 5432

# sed approach - very difficult
# yq approach - easy
HOST=$(yq eval '.settings.database.host' "$STATE_FILE")

# Python approach - easy
HOST=config.get('settings', {}).get('database', {}).get('host', 'localhost')
```

### Debugging Parsing

```bash
#!/bin/bash
debug_parse() {
    echo "=== Debug Output ===" >&2
    echo "File: $STATE_FILE" >&2
    echo "Exists: $([[ -f "$STATE_FILE" ]] && echo "yes" || echo "no")" >&2
    
    echo "Frontmatter:" >&2
    extract_frontmatter "$STATE_FILE" >&2
    
    echo "YAML parse (yq):" >&2
    yq eval '.' "$STATE_FILE" >&2
}
```

## Performance Benchmarks

### Large Files

**sed**: ~1ms for simple fields
**yq**: ~50ms (robust, worth it)
**Python**: ~100ms (full-featured)

### Many Fields

```bash
# Efficient: Parse once
FRONTMATTER=$(extract_frontmatter "$STATE_FILE")
ENABLED=$(read_boolean_field "$FRONTMATTER" "enabled")
MODE=$(read_string_field "$FRONTMATTER" "mode")

# Inefficient: Parse repeatedly
ENABLED=$(yq eval '.enabled' "$STATE_FILE")
MODE=$(yq eval '.mode' "$STATE_FILE")
```

## Conclusion

For most use cases, **yq is recommended**:
- Robust YAML parsing
- Handles edge cases
- Easy to use
- Well-maintained

For complex validation or type safety, use **Python**.

For simple scripts with minimal dependencies, use **sed/awk**.

For JSON-heavy workflows, use **jq** after converting YAML.
