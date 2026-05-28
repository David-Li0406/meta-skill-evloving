---
name: bash
description: Defensive Bash scripting patterns for reliable automation. Use when writing shell scripts.
---

# Bash

## Strict Mode

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

# -E: ERR traps inherited by functions
# -e: exit on error
# -u: error on undefined variables
# -o pipefail: pipe fails if any command fails
```

## Error Handling

```bash
# Trap for cleanup
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Error handler with line number
error_handler() {
    echo "Error on line $1" >&2
    exit 1
}
trap 'error_handler $LINENO' ERR

# Check command exists
require_cmd() {
    command -v "$1" >/dev/null 2>&1 || {
        echo "Required command not found: $1" >&2
        exit 1
    }
}
require_cmd jq
require_cmd curl
```

## Variable Safety

```bash
# Required variable with error message
: "${REQUIRED_VAR:?Error: REQUIRED_VAR not set}"

# Default value
: "${OPTIONAL_VAR:=default_value}"

# Always quote variables
echo "$FILE_PATH"
rm -rf "${DIR:?}/"  # Prevents rm -rf /
```

## Argument Parsing

```bash
usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS] <arg>

Options:
    -h, --help      Show this help
    -v, --verbose   Verbose output
    -f, --file      Input file
EOF
    exit 1
}

VERBOSE=false
FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help) usage ;;
        -v|--verbose) VERBOSE=true; shift ;;
        -f|--file) FILE="$2"; shift 2 ;;
        -*) echo "Unknown option: $1" >&2; usage ;;
        *) ARGS+=("$1"); shift ;;
    esac
done
```

## Logging

```bash
readonly LOG_FILE="/var/log/script.log"

log() {
    local level="$1"; shift
    echo "[$(date -Iseconds)] [$level] $*" | tee -a "$LOG_FILE"
}

info()  { log INFO "$@"; }
warn()  { log WARN "$@"; }
error() { log ERROR "$@" >&2; }
debug() { [[ "${DEBUG:-false}" == "true" ]] && log DEBUG "$@"; }
```

## Idempotency

```bash
# Check before create
[[ -d "$DIR" ]] || mkdir -p "$DIR"

# Check before download
[[ -f "$FILE" ]] || curl -o "$FILE" "$URL"

# Atomic file write
tmp=$(mktemp)
generate_config > "$tmp"
mv "$tmp" "$CONFIG_FILE"
```

## Best Practices

- Always use `#!/usr/bin/env bash`
- Quote all variables: `"$var"`
- Use `[[` over `[` for conditionals
- Use `$(command)` over backticks
- Use `readonly` for constants
- Use `local` in functions
- Prefer absolute paths
- Use `mktemp` for temp files
- Run shellcheck on all scripts
