# Color and emoji definitions
declare -A colors=(
    [green]=$'\033[0;32m'
    [red]=$'\033[0;31m'
    [yellow]=$'\033[1;33m'
    [blue]=$'\033[0;34m'
    [reset]=$'\033[0m'
)

declare -A emojis=(
    [success]='✅'
    [error]='❌'
    [warning]='⚠️'
    [info]='ℹ️'
    [debug]='🐛'
)

# Logging functions
print_success() { printf '%b %b%b%b\n' "${emojis[success]}" "${colors[green]}" "$*" "${colors[reset]}"; }
print_error() { printf '%b %b%b%b\n' "${emojis[error]}" "${colors[red]}" "$*" "${colors[reset]}" >&2; }
print_warning() { printf '%b %b%b%b\n' "${emojis[warning]}" "${colors[yellow]}" "$*" "${colors[reset]}"; }
print_debug() { printf '%b %b%b%b\n' "${emojis[debug]}" "${colors[blue]}" "$*" "${colors[reset]}"; }
print_info() { printf '%b %b\n' "${emojis[info]}" "$*"; }

# Utility functions
command_exists() { command -v "$1" >/dev/null 2>&1; }
