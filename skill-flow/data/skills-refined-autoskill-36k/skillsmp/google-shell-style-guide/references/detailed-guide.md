# Google Shell Style Guide - Complete Reference

This document contains the comprehensive Google Shell Style Guide for bash/shell scripting.

## When to Use Shell

### Appropriate Use Cases
- Small utilities and simple wrapper scripts
- Where shell's natural strengths apply (file manipulation, command chaining)
- Scripts under ~100 lines with straightforward logic

### When to Use Another Language
- Complex data structures needed
- Performance-critical operations
- Cross-platform requirements beyond POSIX
- Scripts exceeding 100 lines of logic

## File Structure

### Header Template
```bash
#!/bin/bash
#
# Script name: script_name.sh
# Description: Brief description of what the script does
# Usage: script_name.sh [options] <arguments>
```

### Section Order
1. Shebang and file header
2. Source statements
3. Constants and readonly variables
4. Global variables
5. Functions
6. Main code (in `main()` function for multi-function scripts)

## Formatting

### Indentation
- Use exactly 2 spaces (never tabs)
- Indent case patterns and their commands
- Align continuation lines sensibly

### Line Length
- Maximum 80 characters
- Break long commands at natural boundaries
- Use backslash continuation for readability

### Pipelines
```bash
# Short pipeline - single line
command1 | command2 | command3

# Long pipeline - break before |
command_with_long_name \
  | second_command \
  | third_command

# Very complex - use process substitution
diff <(command1) <(command2)
```

### Loops and Conditionals

```bash
# for loops
for file in "${files[@]}"; do
  process "${file}"
done

# while with read
while IFS= read -r line; do
  process "${line}"
done < "${input_file}"

# if statements - compact form
if [[ -n "${var}" ]]; then
  do_something
fi

# if statements - complex conditions
if [[ "${status}" == "active" ]] \
    && [[ -f "${config_file}" ]] \
    && check_prerequisites; then
  proceed_with_action
fi
```

### Case Statements
```bash
case "${option}" in
  -v|--verbose)
    verbose=true
    ;;
  -h|--help)
    show_help
    exit 0
    ;;
  --)
    shift
    break
    ;;
  -*)
    err "Unknown option: ${option}"
    exit 1
    ;;
  *)
    # Default case - positional argument
    args+=("${option}")
    ;;
esac
```

## Variables

### Naming Conventions
- **Local variables**: `lowercase_with_underscores`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Environment variables**: `UPPERCASE_WITH_UNDERSCORES`
- **Loop variables**: Short names okay (`i`, `file`, `line`)

### Declaration
```bash
# Constants (readonly)
readonly CONFIG_FILE="/etc/myapp/config"
readonly -a VALID_OPTIONS=("option1" "option2" "option3")

# Variables with defaults
: "${DEBUG:=false}"
: "${LOG_LEVEL:=info}"

# Local variables in functions
local result=""
local -r MAX_RETRIES=3
local -i count=0
local -a items=()
```

### Quoting Rules

**Always quote:**
- Variables in any context: `"${var}"`
- Command substitutions: `"$(command)"`
- Strings with special characters: `"hello world"`

**Don't quote:**
- Integer assignments: `count=0`
- Arithmetic contexts: `(( count++ ))`
- Pattern matching (intentional): `case $var in pattern*)`

```bash
# Correct quoting
local file_path="${base_dir}/${file_name}"
if [[ -f "${file_path}" ]]; then
  content="$(cat "${file_path}")"
fi

# Array expansion - always quote
for item in "${array[@]}"; do
  process "${item}"
done
```

### Parameter Expansion
```bash
# Default values
"${var:-default}"      # Use default if unset or empty
"${var:=default}"      # Set and use default if unset or empty
"${var:+alternate}"    # Use alternate if set and non-empty
"${var:?error msg}"    # Exit with error if unset or empty

# String manipulation
"${var#pattern}"       # Remove shortest prefix match
"${var##pattern}"      # Remove longest prefix match
"${var%pattern}"       # Remove shortest suffix match
"${var%%pattern}"      # Remove longest suffix match
"${var/old/new}"       # Replace first occurrence
"${var//old/new}"      # Replace all occurrences

# Length and substrings
"${#var}"              # String length
"${var:offset:length}" # Substring extraction
```

## Arrays

### Declaration and Assignment
```bash
# Indexed arrays
declare -a files=()
files=("file1.txt" "file2.txt" "file3.txt")
files+=("file4.txt")

# Associative arrays (bash 4+)
declare -A config
config["key1"]="value1"
config["key2"]="value2"
```

### Array Operations
```bash
# Length
echo "${#array[@]}"

# All elements (quoted)
echo "${array[@]}"

# All indices
echo "${!array[@]}"

# Specific element
echo "${array[0]}"

# Slice
echo "${array[@]:1:3}"  # Elements 1, 2, 3

# Iteration
for element in "${array[@]}"; do
  process "${element}"
done
```

## Functions

### Definition Style
```bash
# Preferred - no 'function' keyword
my_function() {
  local arg1="$1"
  local arg2="$2"

  # Function body
}

# Also acceptable
function my_function() {
  # Function body
}
```

### Argument Handling
```bash
process_files() {
  if [[ $# -lt 1 ]]; then
    err "Usage: process_files <file> [file...]"
    return 1
  fi

  local file
  for file in "$@"; do
    if [[ ! -f "${file}" ]]; then
      err "File not found: ${file}"
      continue
    fi
    # Process file
  done
}
```

### Return Values
```bash
# Status code (0-255)
validate_input() {
  if [[ -z "$1" ]]; then
    return 1
  fi
  return 0
}

# Data via stdout
get_config_value() {
  local key="$1"
  grep "^${key}=" "${CONFIG_FILE}" | cut -d= -f2
}

# Usage
if value="$(get_config_value "setting")"; then
  echo "Found: ${value}"
fi
```

## Command Substitution

### Modern Style
```bash
# Correct - $() syntax
current_date="$(date +%Y-%m-%d)"
file_count="$(find . -type f | wc -l)"

# Nested substitution (clean)
result="$(command1 "$(command2)")"

# Wrong - backticks (deprecated)
current_date=`date +%Y-%m-%d`  # Don't use
```

### Checking Results
```bash
# Capture and check
if ! output="$(command 2>&1)"; then
  err "Command failed: ${output}"
  return 1
fi

# Check specific status
command
local status=$?
if [[ ${status} -eq 2 ]]; then
  # Handle specific error
fi
```

## Conditionals

### Test Syntax
```bash
# Always use [[ ]] for tests
if [[ -f "${file}" ]]; then
  echo "File exists"
fi

# String comparison
if [[ "${str1}" == "${str2}" ]]; then
  echo "Equal"
fi

# Pattern matching (unquoted pattern)
if [[ "${filename}" == *.txt ]]; then
  echo "Text file"
fi

# Regex matching
if [[ "${email}" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
  echo "Valid email"
fi

# Numeric comparison - use (( ))
if (( count > 10 )); then
  echo "Count exceeds 10"
fi
```

### Compound Conditions
```bash
# AND
if [[ -f "${file}" ]] && [[ -r "${file}" ]]; then
  cat "${file}"
fi

# OR
if [[ -z "${var1}" ]] || [[ -z "${var2}" ]]; then
  err "Missing required variable"
fi

# NOT
if [[ ! -d "${dir}" ]]; then
  mkdir -p "${dir}"
fi
```

## Arithmetic

### Integer Arithmetic
```bash
# Use (( )) for arithmetic
(( count++ ))
(( total = a + b ))
(( remaining = total - used ))

# In assignments
local -i result=$(( a * b ))

# In conditions
if (( count >= limit )); then
  echo "Limit reached"
fi
```

### Floating Point
```bash
# Use bc or awk for floating point
result="$(echo "scale=2; 22/7" | bc)"
average="$(awk "BEGIN {printf \"%.2f\", ${sum}/${count}}")"
```

## Error Handling

### Exit Codes
- `0` - Success
- `1` - General errors
- `2` - Misuse of shell command
- `126` - Command not executable
- `127` - Command not found
- `128+n` - Terminated by signal n

### Error Reporting
```bash
# Standard error function
err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

# Fatal error function
die() {
  err "$@"
  exit 1
}

# Usage
if [[ ! -f "${config}" ]]; then
  die "Configuration file not found: ${config}"
fi
```

### Strict Mode
```bash
#!/bin/bash
set -euo pipefail

# -e: Exit on error
# -u: Error on undefined variables
# -o pipefail: Pipeline fails if any command fails
```

### Trap Handlers
```bash
# Cleanup on exit
cleanup() {
  local exit_code=$?
  rm -f "${tmp_file:-}"
  exit "${exit_code}"
}
trap cleanup EXIT

# Handle specific signals
handle_interrupt() {
  err "Interrupted"
  exit 130
}
trap handle_interrupt INT TERM
```

## Temporary Files

### Safe Creation
```bash
# Create temp file
tmp_file="$(mktemp)" || die "Failed to create temp file"

# Create temp directory
tmp_dir="$(mktemp -d)" || die "Failed to create temp directory"

# With cleanup
cleanup() {
  rm -rf "${tmp_dir:-}"
}
trap cleanup EXIT
```

### Best Practices
- Always use `mktemp`
- Set cleanup traps
- Use restrictive permissions
- Never use predictable names

## Input Validation

### Argument Checking
```bash
main() {
  if [[ $# -lt 2 ]]; then
    err "Usage: $0 <input> <output>"
    exit 1
  fi

  local input="$1"
  local output="$2"

  if [[ ! -f "${input}" ]]; then
    die "Input file not found: ${input}"
  fi

  if [[ -e "${output}" ]] && [[ ! -w "${output}" ]]; then
    die "Cannot write to output: ${output}"
  fi
}
```

### Path Sanitization
```bash
# Validate path doesn't escape
validate_path() {
  local path="$1"
  local base_dir="$2"

  # Resolve to absolute path
  local resolved
  resolved="$(cd "${base_dir}" && realpath -m "${path}")"

  # Check it's within base
  if [[ "${resolved}" != "${base_dir}"/* ]]; then
    return 1
  fi
  return 0
}
```

## PIPESTATUS

### Checking Pipeline Status
```bash
# Individual command status in pipeline
command1 | command2 | command3
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
  err "command1 failed"
fi

# With set -o pipefail, entire pipeline fails
set -o pipefail
if ! command1 | command2; then
  err "Pipeline failed"
fi
```

## Main Function Pattern

```bash
#!/bin/bash
#
# Script description
#

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

err() {
  echo "[${SCRIPT_NAME}] ERROR: $*" >&2
}

usage() {
  cat <<EOF
Usage: ${SCRIPT_NAME} [options] <argument>

Options:
  -h, --help     Show this help message
  -v, --verbose  Enable verbose output

Arguments:
  argument       Description of argument
EOF
}

main() {
  local verbose=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--help)
        usage
        exit 0
        ;;
      -v|--verbose)
        verbose=true
        shift
        ;;
      --)
        shift
        break
        ;;
      -*)
        err "Unknown option: $1"
        usage
        exit 1
        ;;
      *)
        break
        ;;
    esac
  done

  if [[ $# -lt 1 ]]; then
    err "Missing required argument"
    usage
    exit 1
  fi

  # Main logic here
}

main "$@"
```
