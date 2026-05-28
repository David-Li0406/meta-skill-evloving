---
name: shell-script-quality-assurance
description: Use this skill when you need to lint, format, or improve the quality of shell scripts, ensuring adherence to best practices and style guidelines.
---

# Shell Script Quality Assurance

This skill provides comprehensive guidance for writing, linting, and formatting shell scripts, ensuring they adhere to best practices and style guidelines.

## Core Principles

1. **Consistency** - Follow established patterns within each script.
2. **Safety** - Quote variables, use `[[ ]]`, and check return values.
3. **Readability** - Use clear naming conventions and maintain a maximum line length of 80 characters.

## Quick Reference for Style

| Pattern | Use | Avoid |
|---------|-----|-------|
| Command substitution | `$(command)` | `` `command` `` |
| Conditionals | `[[ condition ]]` | `[ condition ]` |
| Variables | `"${var}"` | `$var` |
| Arrays | `"${array[@]}"` | `${array[*]}` |

## Formatting Rules

### Indentation
- Use 2 spaces (never tabs).
- Align case patterns with `esac`.

### Line Length
- Maximum 80 characters.
- Break long pipelines before `|`.
- Use backslash for line continuation.

## Linting with Shellcheck

### Installation

```bash
# Debian/Ubuntu
apt install shellcheck

# macOS
brew install shellcheck

# From source
cabal update && cabal install ShellCheck
```

### Basic Usage

```bash
# Check single file
shellcheck script.sh

# Check multiple files
shellcheck *.sh

# With specific shell dialect
shellcheck --shell=bash script.sh
```

### Common Shellcheck Codes

| Code   | Issue                                      | Fix                            |
| ------ | ------------------------------------------ | ------------------------------ |
| SC2086 | Double quote to prevent globbing/splitting | `"$var"`                       |
| SC2046 | Quote command substitution                 | `"$(cmd)"`                     |
| SC2006 | Use `$()` instead of backticks             | `$(cmd)`                       |
| SC2034 | Variable appears unused                    | Remove or export               |

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
- Use `return` for status codes (0-255).
- Use `echo` or global variable for data.
- Always check return values.

## Shellcheck Directives

```bash
# Disable for next line
# shellcheck disable=SC2086
echo $unquoted_var

# Specify shell dialect
# shellcheck shell=bash
```