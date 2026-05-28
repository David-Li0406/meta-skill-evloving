---
name: defensive-bash-scripting
description: Use this skill when writing robust, production-grade Bash scripts for automation, CI/CD pipelines, and system utilities, ensuring safety and reliability through defensive programming techniques.
---

# Defensive Bash Scripting

This skill provides comprehensive guidance for writing production-ready Bash scripts using defensive programming techniques, error handling, and safety best practices to prevent common pitfalls and ensure reliability.

## Core Defensive Principles

### 1. Strict Mode

Enable Bash strict mode at the start of every script to catch errors early.

```bash
#!/bin/bash
set -Eeuo pipefail  # Exit on error, unset variables, pipe failures
```

### 2. Error Trapping and Cleanup

Implement proper cleanup on script exit or error.

```bash
trap 'echo "Error on line $LINENO"' ERR
trap 'echo "Cleaning up..."; rm -rf "$TMPDIR"' EXIT

TMPDIR=$(mktemp -d)
# Script code here
```

### 3. Variable Safety

Always quote variables to prevent word splitting and globbing issues.

```bash
# Wrong - unsafe
cp $source $dest

# Correct - safe
cp "$source" "$dest"

# Required variables - fail with message if unset
: "${REQUIRED_VAR:?REQUIRED_VAR is not set}"
```

### 4. Array Handling

Use arrays safely for complex data handling.

```bash
# Safe array iteration
declare -a items=("item 1" "item 2" "item 3")

for item in "${items[@]}"; do
    echo "Processing: $item"
done

# Reading output into array safely
mapfile -t lines < <(some_command)
```

### 5. Conditional Safety

Use `[[ ]]` for Bash-specific features, `[ ]` for POSIX.

```bash
# Bash - safer
if [[ -f "$file" && -r "$file" ]]; then
    content=$(<"$file")
fi

# POSIX - portable
if [ -f "$file" ] && [ -r "$file" ]; then
    content=$(cat "$file")
fi
```

## Essential Defensive Patterns

### 1. Strict Mode Template

```bash
#!/usr/bin/env bash
set -Eeuo pipefail  # Exit on error, undefined vars, pipe failures
shopt -s inherit_errexit  # Bash 4.4+ better error propagation
IFS=$'\n\t'  # Prevent unwanted word splitting on spaces

# Error trap with context
trap 'echo "Error at line $LINENO: exit $?" >&2' ERR

# Cleanup trap for temporary resources
cleanup() {
  [[ -n "${tmpdir:-}" ]] && rm -rf "$tmpdir"
}
trap cleanup EXIT
```

### 2. Safe Variable Handling

```bash
# Quote all variable expansions
cp "$source_file" "$dest_dir"

# Required variables with error messages
: "${REQUIRED_VAR:?not set or empty}"
```

### 3. Robust Argument Parsing

```bash
usage() {
  cat <<EOF
Usage: ${0##*/} [OPTIONS] <required-arg>

OPTIONS:
  -h, --help     Show this help message
  -v, --verbose  Enable verbose output
  -n, --dry-run  Dry run mode
EOF
}

# Parse arguments
while getopts "hvn-:" opt; do
  case "$opt" in
    h) usage; exit 0 ;;
    v) VERBOSE=1 ;;
    n) DRY_RUN=1 ;;
    -) # Long options
      case "$OPTARG" in
        help) usage; exit 0 ;;
        verbose) VERBOSE=1 ;;
        dry-run) DRY_RUN=1 ;;
        *) echo "Unknown option: --$OPTARG" >&2; exit 1 ;;
      esac
      ;;
    *) usage >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))
```

### 4. Safe Temporary Resources

```bash
# Create temp directory with cleanup
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

# Safe temp file creation
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT
```

### 5. Structured Logging

```bash
log() {
  local level="$1"; shift
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$timestamp] [$level] $SCRIPT_NAME: $*" >&2
}

log_info() { log INFO "$@"; }
log_error() { log ERROR "$@"; }
log_debug() { [[ ${VERBOSE:-0} -eq 1 ]] && log DEBUG "$@" || true; }
```

## Output Deliverables

When creating Bash scripts, provide:

1. **Production-ready script** with:
   - Strict mode enabled (`set -Eeuo pipefail`)
   - Comprehensive error handling and cleanup traps
   - Clear usage message (`--help`)
   - Proper argument parsing with `getopts`
   - Structured logging with log levels

2. **Test suite** (bats-core or shellspec):
   - Edge cases and error conditions
   - Mock external dependencies
   - TAP output format

3. **CI/CD configuration**:
   - ShellCheck static analysis
   - shfmt formatting validation
   - Automated testing with Bats

4. **Documentation**:
   - Usage examples in `--help`
   - Required dependencies and versions
   - Exit codes and error messages

5. **Static analysis config**:
   - `.shellcheckrc` with appropriate suppressions
   - `.editorconfig` for consistent formatting

## Tools & Commands

### Essential Tools
- **ShellCheck**: `shellcheck --enable=all script.sh`
- **shfmt**: `shfmt -i 2 -ci -bn -sr -kp script.sh`
- **bats-core**: `bats test/script.bats`

## Common Pitfalls to Avoid

Quick list:
- ❌ `for f in $(ls ...)` → ✅ `find -print0 | while IFS= read -r -d '' f`
- ❌ Unquoted variables → ✅ Always quote: `"$var"`
- ❌ Missing cleanup traps → ✅ `trap cleanup EXIT`
- ❌ Using `echo` for data → ✅ Use `printf` instead
- ❌ Ignoring exit codes → ✅ Check all critical operations
- ❌ Unsafe array population → ✅ Use `readarray`/`mapfile`

## References & Further Reading

### Style Guides & Best Practices
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) - Comprehensive style guide covering quoting, arrays, and when to use shell
- [Bash Pitfalls](https://mywiki.wooledge.org/BashPitfalls) - Catalog of common Bash mistakes and how to avoid them
- [Bash Hackers Wiki](https://wiki.bash-hackers.org/) - Comprehensive Bash documentation and advanced techniques