---
name: Google Shell Style Guide
description: This skill should be used when the user asks to "refactor shell script", "fix bash style", "review shell code", "apply Google style guide", "improve shell script", mentions "shellcheck", or discusses bash/shell coding standards and best practices.
allowed-tools: Read, Edit, Bash, Glob, Grep, mcp__plugin_serena_serena, mcp__plugin_serena_serena_*
---

# Google Shell Style Guide

Comprehensive guidance for writing shell scripts following Google's Shell Style Guide.

## Core Principles

1. **Consistency** - Follow established patterns within each script
2. **Safety** - Quote variables, use `[[ ]]`, check return values
3. **Readability** - 2-space indents, 80-char lines, clear naming

## Quick Reference

| Pattern | Use | Avoid |
|---------|-----|-------|
| Command substitution | `$(command)` | `` `command` `` |
| Conditionals | `[[ condition ]]` | `[ condition ]` |
| Arithmetic | `(( expression ))` | `$[ expression ]` |
| Variables | `"${var}"` | `$var` |
| Arrays | `"${array[@]}"` | `${array[*]}` |

## Formatting Rules

### Indentation
- Use 2 spaces (never tabs)
- Align case patterns with `esac`

### Line Length
- Maximum 80 characters
- Break long pipelines before `|`
- Use backslash for line continuation

### Control Structures

```bash
# if/then on same line
if [[ condition ]]; then
  command
elif [[ other ]]; then
  other_command
else
  fallback
fi

# while/do on same line
while [[ condition ]]; do
  command
done

# case alignment
case "${var}" in
  pattern1)
    command
    ;;
  pattern2)
    other
    ;;
esac
```

## Variable Handling

### Always Quote
```bash
# Correct
echo "${var}"
rm "${file}"

# Wrong - word splitting risk
echo $var
rm $file
```

### Use Braces
```bash
# Correct - clear boundaries
echo "${prefix}_suffix"

# Wrong - ambiguous
echo "$prefix_suffix"
```

### Arrays for Commands
```bash
# Correct - handles spaces safely
local -a args=(--flag "value with spaces")
command "${args[@]}"

# Wrong - breaks on spaces
local args="--flag value with spaces"
command $args
```

## Function Guidelines

### Naming and Declaration
```bash
# lowercase_with_underscores
process_file() {
  local input_file="$1"
  # ...
}
```

### Local Variables
```bash
my_function() {
  local result=""
  local -r CONSTANT="value"  # readonly local
  # ...
}
```

### Return Values
- Use `return` for status codes (0-255)
- Use `echo` or global variable for data
- Always check return values

```bash
if ! process_file "${input}"; then
  err "Processing failed"
  return 1
fi
```

## Error Handling

### Standard Error Function
```bash
err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}
```

### Strict Mode
```bash
#!/bin/bash
set -euo pipefail
```

### Cleanup with Traps
```bash
cleanup() {
  rm -f "${tmp_file:-}"
}
trap cleanup EXIT
```

## Issue Severity Classification

When reviewing shell scripts, classify issues by severity:

| Severity | Description | Examples |
|----------|-------------|----------|
| **Critical** | Security risks, data loss potential | Command injection, unquoted variables in `rm`, `eval` usage |
| **Important** | Correctness issues, portability problems | Missing error handling, bashisms in `/bin/sh` scripts |
| **Minor** | Style violations, readability issues | Inconsistent indentation, long lines |

## Anti-Patterns to Avoid

1. **Never use `eval`** - Command injection risk
2. **Never use aliases in scripts** - Use functions instead
3. **Avoid piping to `while`** - Creates subshell, loses variable changes
4. **Avoid `mapfile`/`readarray`** - Not available on macOS

## Additional Resources

For detailed patterns, edge cases, and comprehensive examples:

- **`references/detailed-guide.md`** - Complete style guide with all rules
- **`references/anti-patterns.md`** - Comprehensive anti-pattern catalog with fixes
