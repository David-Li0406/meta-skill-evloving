#!/bin/bash
set -euo pipefail

# Scan dependencies from all package managers across 8 languages
#
# Usage:
#   bash scan-dependencies.sh [project_root]
#   bash scan-dependencies.sh  # Uses current directory
#
# Output: JSON to stdout

PROJECT_ROOT="${1:-.}"
cd "$PROJECT_ROOT"

# Check if jq is available
if ! command -v jq &>/dev/null; then
    echo "Warning: jq not found, JSON output may be malformed" >&2
    HAS_JQ=false
else
    HAS_JQ=true
fi

# Initialize dependencies object
declare -A DEPS

# Parse Python dependencies
parse_python() {
    local deps=()

    # requirements.txt
    if [ -f "requirements.txt" ]; then
        while IFS= read -r line; do
            # Skip comments and empty lines
            [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
            # Extract package name (before ==, >=, <=, [, etc.)
            pkg=$(echo "$line" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1 | cut -d'[' -f1 | tr -d ' ')
            [[ -n "$pkg" && "$pkg" != "-e" ]] && deps+=("\"$pkg\"")
        done < requirements.txt
    fi

    # pyproject.toml (simple parsing)
    if [ -f "pyproject.toml" ]; then
        # Extract dependencies section
        sed -n '/^\[tool.poetry.dependencies\]/,/^\[/p' pyproject.toml | \
            grep '=' | grep -v '^\[' | cut -d'=' -f1 | tr -d ' "' | \
            while read -r pkg; do
                [[ "$pkg" != "python" ]] && deps+=("\"$pkg\"")
            done
    fi

    # Output as JSON array
    if [ ${#deps[@]} -gt 0 ]; then
        echo "\"Python\": [$(IFS=,; echo "${deps[*]}")],"
    fi
}

# Parse Rust dependencies
parse_rust() {
    local deps=()

    if [ -f "Cargo.toml" ]; then
        # Parse [dependencies] section
        sed -n '/^\[dependencies\]/,/^\[/p' Cargo.toml | \
            grep -E '^[a-zA-Z0-9_-]+ = ' | cut -d'=' -f1 | tr -d ' ' | \
            while read -r pkg; do
                deps+=("\"$pkg\"")
            done

        # Also check [workspace.dependencies] if workspace
        if grep -q '^\[workspace.dependencies\]' Cargo.toml; then
            sed -n '/^\[workspace.dependencies\]/,/^\[/p' Cargo.toml | \
                grep -E '^[a-zA-Z0-9_-]+ = ' | cut -d'=' -f1 | tr -d ' ' | \
                while read -r pkg; do
                    deps+=("\"$pkg\"")
                done
        fi
    fi

    if [ ${#deps[@]} -gt 0 ]; then
        echo "\"Rust\": [$(IFS=,; echo "${deps[*]}")],"
    fi
}

# Parse Go dependencies
parse_go() {
    local deps=()

    if [ -f "go.mod" ]; then
        # Parse require statements (single line and block)
        {
            # Single line requires
            grep '^[[:space:]]*require ' go.mod | grep -v '// indirect' | awk '{print $2}'

            # Block requires
            sed -n '/^require (/,/^)/p' go.mod | \
                grep -v 'require (' | grep -v '^)' | grep -v '// indirect' | awk '{print $1}'
        } | sort -u | while read -r pkg; do
            deps+=("\"$pkg\"")
        done
    fi

    if [ ${#deps[@]} -gt 0 ]; then
        echo "\"Go\": [$(IFS=,; echo "${deps[*]}")],"
    fi
}

# Parse Julia dependencies
parse_julia() {
    local deps=()

    if [ -f "Project.toml" ]; then
        # Parse [deps] section
        sed -n '/^\[deps\]/,/^\[/p' Project.toml | \
            grep '=' | grep -v '^\[' | cut -d'=' -f1 | tr -d ' "' | \
            while read -r pkg; do
                deps+=("\"$pkg\"")
            done
    fi

    if [ ${#deps[@]} -gt 0 ]; then
        echo "\"Julia\": [$(IFS=,; echo "${deps[*]}")],"
    fi
}

# Parse Elixir dependencies
parse_elixir() {
    local deps=()

    if [ -f "mix.exs" ]; then
        # Extract from deps function (fragile, but works for common cases)
        sed -n '/defp deps do/,/^  end$/p' mix.exs | \
            grep '{:' | cut -d'{' -f2 | cut -d',' -f1 | tr -d ': ' | \
            while read -r pkg; do
                deps+=("\"$pkg\"")
            done
    fi

    if [ ${#deps[@]} -gt 0 ]; then
        echo "\"Elixir\": [$(IFS=,; echo "${deps[*]}")],"
    fi
}

# Parse C++ dependencies (limited - CMake only)
parse_cpp() {
    local deps=()

    if [ -f "CMakeLists.txt" ]; then
        # find_package statements
        grep 'find_package(' CMakeLists.txt | \
            sed 's/find_package(//' | sed 's/ .*//' | sed 's/)//' | \
            while read -r pkg; do
                [[ -n "$pkg" ]] && deps+=("\"$pkg\"")
            done

        # FetchContent declarations
        grep 'FetchContent_Declare(' CMakeLists.txt -A 1 | \
            grep -v 'FetchContent_Declare' | grep -v 'GIT_REPOSITORY' | grep -v ')' | tr -d ' ' | \
            while read -r pkg; do
                [[ -n "$pkg" ]] && deps+=("\"$pkg\"")
            done
    fi

    if [ ${#deps[@]} -gt 0 ]; then
        echo "\"C++\": [$(IFS=,; echo "${deps[*]}")],"
    fi
}

# Parse Zig dependencies (experimental)
parse_zig() {
    local deps=()

    if [ -f "build.zig" ]; then
        # b.dependency() calls
        grep 'b.dependency(' build.zig | \
            sed 's/.*b.dependency("//' | cut -d'"' -f1 | \
            while read -r pkg; do
                [[ -n "$pkg" ]] && deps+=("\"$pkg\"")
            done
    fi

    if [ ${#deps[@]} -gt 0 ]; then
        echo "\"Zig\": [$(IFS=,; echo "${deps[*]}")],"
    fi
}

# Parse JavaScript/TypeScript dependencies
parse_javascript() {
    local deps=()

    if [ -f "package.json" ]; then
        if $HAS_JQ; then
            # Use jq for robust parsing
            {
                jq -r '.dependencies | keys[]' package.json 2>/dev/null || true
                jq -r '.devDependencies | keys[]' package.json 2>/dev/null || true
            } | sort -u | while read -r pkg; do
                deps+=("\"$pkg\"")
            done
        else
            # Fallback: grep-based (fragile)
            {
                grep -A 1000 '"dependencies"' package.json | grep -B 1000 '^  }' | \
                    grep '"' | cut -d'"' -f2 | grep -v '^dependencies$' || true
                grep -A 1000 '"devDependencies"' package.json | grep -B 1000 '^  }' | \
                    grep '"' | cut -d'"' -f2 | grep -v '^devDependencies$' || true
            } | sort -u | while read -r pkg; do
                deps+=("\"$pkg\"")
            done
        fi
    fi

    if [ ${#deps[@]} -gt 0 ]; then
        echo "\"JavaScript\": [$(IFS=,; echo "${deps[*]}")],"
    fi
}

# Main execution
{
    echo "{"
    parse_python
    parse_rust
    parse_go
    parse_julia
    parse_elixir
    parse_cpp
    parse_zig
    parse_javascript
    echo "  \"_generated\": true"
    echo "}"
} | if $HAS_JQ; then
    # Validate and pretty-print with jq
    jq '.'
else
    # Output as-is without jq
    cat
fi
