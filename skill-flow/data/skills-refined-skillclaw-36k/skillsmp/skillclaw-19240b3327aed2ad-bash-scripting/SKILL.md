---
name: bash-scripting
description: Use this skill when you need to write, test, or develop Bash scripts, including unit testing, error handling, and argument parsing.
---

# Bash Scripting

This skill encompasses best practices for writing, testing, and developing Bash scripts, including frameworks for testing, error handling, and argument parsing.

## Script Foundation

Every script should start with the essential header:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

**set options explained:**

- `-e` - Exit immediately on command failure.
- `-u` - Treat unset variables as errors.
- `-o pipefail` - Pipeline fails if any command fails.

## Script Metadata Pattern

```bash
SCRIPT_NAME=$(basename "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_NAME SCRIPT_DIR
```

## Error Handling

Implement trap-based error handling for robust scripts:

```bash
handle_error() {
    local line="${1}"
    local exit_code="${2:-1}"
    printf '%s\n' "Error on line ${line}" >&2
    exit "${exit_code}"
}

trap 'handle_error ${LINENO} $?' ERR

cleanup() {
    # Cleanup logic here
    rm -f "${TEMP_FILE:-}"
}

trap cleanup EXIT
```

## Argument Parsing

Standard argument parsing template:

```bash
usage() {
    cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS] <argument>

Options:
    -h, --help      Show this help message
    -v, --version   Show version information
    -d, --debug     Enable debug mode
    -f, --file      Specify input file

Examples:
    ${SCRIPT_NAME} file.txt
    ${SCRIPT_NAME} --debug file.txt
EOF
}

main() {
    local debug=0
    local input_file=""

    while [[ $# -gt 0 ]]; do
        case "${1}" in
            -h|--help) usage; exit 0 ;;
            -v|--version) printf '%s version %s\n' "${SCRIPT_NAME}" "${SCRIPT_VERSION}"; exit 0 ;;
            -d|--debug) debug=1; set -x; shift ;;
            -f|--file) input_file="${2}"; shift 2 ;;
            -*) printf 'Unknown option: %s\n' "${1}" >&2; usage; exit 1 ;;
            *) break ;;
        esac
    done

    # Validate required arguments
    if [[ $# -lt 1 ]]; then
        printf 'Missing required argument\n' >&2
        usage
        exit 1
    fi

    # Main logic here
}

main "$@"
```

## Testing Frameworks

### Framework Selection

| Framework     | Strengths                     | Best For                      |
| ------------- | ----------------------------- | ----------------------------- |
| **shunit2**   | xUnit style, simple, portable | Unit tests, function testing  |
| **shellspec** | BDD style, modern, extensive  | Behavior specs, full projects |

### shunit2 Installation

```bash
# Download directly
curl -L https://github.com/kward/shunit2/raw/master/shunit2 -o shunit2

# Or via package manager
apt install shunit2
brew install shunit2
```

### Basic Test Structure

```bash
#!/usr/bin/env bash

# Source the script being tested
source ./my_script.sh

# Test functions start with test
test_addition() {
    result=$(add 2 3)
    assertEquals "2 + 3 should equal 5" "5" "$result"
}

# Load shunit2
source shunit2
```

### shunit2 Assertions

```bash
# Equality
assertEquals [message] expected actual
assertNotEquals [message] unexpected actual

# Null/Empty
assertNull [message] value
assertNotNull [message] value

# Boolean/Status
assertTrue [message] condition
assertFalse [message] condition
```