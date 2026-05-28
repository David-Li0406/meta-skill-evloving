---
name: python-naming
description: Python naming conventions for variables, constants, files, and directories
license: MIT
compatibility: opencode
metadata:
    related_coding_principles: For general coding standards, use skill `coding-principles`
    related_python_guidelines: For type annotations and style, use skill `python-guidelines`
---

# Python Naming Conventions

## What I Do

Provide Python naming conventions for variables, functions, classes, constants, files, and directories.

## Naming Rules

### Variables and Functions

```python
# Use snake_case for variables and functions
user_name = "alice"
input_data = get_input()

# Avoid single-letter names except for loop counters or math
for i in range(10):      # OK - loop counter
    x = coordinate[i]    # OK - mathematical variable

# Avoid generic names
# BAD: data, info, temp, x, y
# GOOD: user_data, config_info, temp_file, user_coordinates

# Avoid abbreviations unless widely recognized
# BAD: usr_nm, cfg, calc_val
# GOOD: user_name, config, calculated_value
```

### Classes

```python
# Use PascalCase for classes
class DataProcessor:
    pass

class ConfigurationError(Exception):
    pass
```

### Constants

```python
# Use UPPER_SNAKE_CASE for constants
MAX_BUFFER_SIZE = 1024
DEFAULT_TIMEOUT_SECONDS = 30

# Define magic numbers as constants
INPUT_FILE_ENCODING = "utf-8"
OUTPUT_DELIMITER = ","
```

### Files and Directories

```python
# Use _file suffix for filename variables
input_file: Path
output_file: Path

# Use _dir suffix for directory path variables
input_dir: Path
output_dir: Path

# NEVER mix these up
# BAD: input_file = Path("path/to/dir")       # Confusing
# BAD: output_dir = Path("file.txt")          # Confusing

# Use _path ONLY in rare exceptional cases when truly unclear
# Prefer _file or _dir instead
```

## When to Use Me

Use this skill when:

- Naming variables, functions, or classes
- Defining constants
- Creating file/directory path parameters
- Reviewing code for naming consistency

## Key Rules

1. **Clarity over brevity** - `user_input_path` > `uip`
2. **Consistent conventions** - Apply same pattern throughout
3. **Avoid magic values** - Use constants for repeated values
4. **Type hints required** - Always annotate types
5. **Domain-appropriate names** - Use context-relevant terminology
