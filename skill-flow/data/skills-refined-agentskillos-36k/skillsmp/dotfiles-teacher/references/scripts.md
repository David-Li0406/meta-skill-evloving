# Shell Script Best Practices

## Table of Contents

1. [Script Template](#script-template)
2. [Helper Functions](#helper-functions)
3. [Error Handling](#error-handling)
4. [Platform Detection](#platform-detection)
5. [Idempotency](#idempotency)

## Script Template

Every script should follow this structure:

```bash
#!/bin/bash
set -eu  # Exit on error, undefined vars

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

info "Starting <task>"
debugPlatformInfo

# Main logic here

success "<task> complete"
```

### Strict Mode Explained

- `set -e`: Exit immediately on command failure
- `set -u`: Treat unset variables as errors
- Avoid `set -o pipefail` unless needed (can cause issues with grep)

## Helper Functions

Centralize reusable functions in `common.sh`:

### Logging

```bash
info()    { echo -e "\033[0;34m[INFO]\033[0m $*"; }
success() { echo -e "\033[0;32m[SUCCESS]\033[0m $*"; }
warning() { echo -e "\033[0;33m[WARNING]\033[0m $*"; }
error()   { echo -e "\033[0;31m[ERROR]\033[0m $*" >&2; }
debug()   { [[ "${DEBUG:-}" == "1" ]] && echo -e "[DEBUG] $*"; }
```

### Path Resolution

```bash
getDotfilesDir() {
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    echo "$(cd "${script_dir}/../.." && pwd)"
}
```

### Safe Operations

```bash
safeDownload() {
    local url="$1" dest="$2" desc="${3:-file}"
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$url" -o "$dest"
    elif command -v wget >/dev/null 2>&1; then
        wget -q "$url" -O "$dest"
    else
        error "No download tool available"
        return 1
    fi
}
```

## Error Handling

### Graceful Failures

```bash
if ! some_command; then
    warning "some_command failed, continuing..."
fi

# Or with fallback
some_command || {
    warning "Fallback to alternative"
    alternative_command
}
```

### Required Commands

```bash
require_command() {
    command -v "$1" >/dev/null 2>&1 || {
        error "Required command not found: $1"
        exit 1
    }
}
```

## Platform Detection

```bash
isRunningOnMac()   { [[ "$(uname)" == "Darwin" ]]; }
isRunningOnLinux() { [[ "$(uname)" == "Linux" ]] && [[ -z "${WSL_DISTRO_NAME:-}" ]]; }
isRunningOnWSL()   { [[ -n "${WSL_DISTRO_NAME:-}" ]]; }
isRunningOnCI()    { [[ "${CI:-}" == "true" ]]; }

getLinuxDistro() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        echo "${ID:-unknown}"
    else
        echo "unknown"
    fi
}
```

### Platform-Specific Logic

```bash
if isRunningOnMac; then
    # macOS specific
    FONT_DIR="$HOME/Library/Fonts"
elif isRunningOnWSL; then
    # WSL specific
    installFontToWindows "$FONT_URL" "$FONT_NAME"
elif isRunningOnLinux; then
    # Linux specific
    case "$(getLinuxDistro)" in
        ubuntu|debian) apt-get install ... ;;
        fedora|rhel)   dnf install ... ;;
        arch)          pacman -S ... ;;
    esac
fi
```

## Idempotency

Scripts should be safe to run multiple times:

```bash
# Check before creating
if [[ ! -f "$TARGET" ]]; then
    cp "$SOURCE" "$TARGET"
    info "Created $TARGET"
else
    debug "$TARGET already exists"
fi

# Use force flags for symlinks
ln -fnsv "$SOURCE" "$TARGET"  # -f forces, -n treats symlink as file

# Check before installing
if ! isPackageInstalled "brew" "some-package"; then
    brew install some-package
fi
```
