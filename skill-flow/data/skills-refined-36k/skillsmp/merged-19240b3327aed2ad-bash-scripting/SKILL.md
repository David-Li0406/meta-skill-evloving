---
name: bash-scripting
description: Use this skill when you need to develop, test, or implement Bash scripts, including writing functions, handling errors, and unit testing.
---

# Bash Scripting

This skill encompasses best practices for Bash script development, including error handling, argument parsing, and testing frameworks like shunit2 and shellspec.

## Script Foundation

Every script should start with the essential header:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

**set options explained:**

- `-e` - Exit immediately on command failure
- `-u` - Treat unset variables as errors
- `-o pipefail` - Pipeline fails if any command fails

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

## Variable Best Practices

**Always use curly braces and quote variables:**

```bash
# Correct
"${variable}"
"${array[@]}"

# Incorrect
$variable
${array[*]}  # Use [@] for proper iteration
```

**Use readonly for constants:**

```bash
readonly CONFIG_FILE="/etc/app/config"
readonly -a VALID_OPTIONS=("opt1" "opt2" "opt3")
```

## Testing Frameworks

### shunit2

#### Installation

```bash
# Download directly
curl -L https://github.com/kward/shunit2/raw/master/shunit2 -o shunit2

# Or via package manager
apt install shunit2
brew install shunit2
```

#### Basic Test Structure

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

### shellspec

#### Installation

```bash
# Via curl
curl -fsSL https://git.io/shellspec | sh

# Via Homebrew
brew install shellspec
```

#### Basic Spec Structure

```bash
# spec/functions_spec.sh

Describe 'calculate_sum'
  Include lib/functions.sh

  It 'returns 0 for no arguments'
    When call calculate_sum
    The output should eq "0"
    The status should be success
  End
End
```

## Best Practices

1. **One assertion per test** when practical.
2. **Descriptive test names** explaining what's tested.
3. **Isolate tests** - no dependencies between tests.
4. **Test edge cases** - empty input, special characters, large data.
5. **Clean up resources** in tearDown.
6. **Mock external commands** - don't test curl, test your logic.
7. **Test exit codes** not just output.

## Additional Resources

For detailed patterns and examples, consider reviewing the following:

- **[bash_example_file.sh](./references/bash_example_file.sh)** - Complete script template
- **[bash_example_includes.bash](./references/bash_example_includes.bash)** - Reusable utility functions
- **[pure-bash-bible-strings.md](./references/pure-bash-bible-strings.md)** - String manipulation patterns
- **[pure-bash-bible-arrays.md](./references/pure-bash-bible-arrays.md)** - Array operations
- **[pure-bash-bible-files.md](./references/pure-bash-bible-files.md)** - File handling patterns
- **[pure-bash-bible-variables.md](./references/pure-bash-bible-variables.md)** - Parameter expansion reference