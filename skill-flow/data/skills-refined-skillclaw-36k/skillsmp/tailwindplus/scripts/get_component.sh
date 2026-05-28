#!/bin/bash
set -euo pipefail

# Get TailwindPlus component code
# Usage: ./get_component.sh <json_file> <full_name> -f <framework> -v <version> -m <mode>

usage() {
    cat << EOF
Usage: $(basename "$0") <json_file> <full_name> -f <framework> -v <version> -m <mode>

Arguments:
  json_file    Path to TailwindPlus JSON data file
  full_name    Full dotted path (e.g., "Application UI.Forms.Input Groups.Simple")
  -f, --framework   html, react, or vue
  -v, --version     3 or 4 (Tailwind CSS version)
  -m, --mode        light, dark, system, or none (eCommerce only)

Examples:
  $(basename "$0") /path/to/data.json "Application UI.Forms.Input Groups.Simple" -f html -v 4 -m light
  $(basename "$0") /path/to/data.json "Ecommerce.Components.Product Overviews.With image gallery" -f react -v 4 -m none
EOF
    exit 1
}

# Parse arguments
if [[ $# -lt 2 ]]; then
    usage
fi

DATA_FILE="$1"
shift
FULL_NAME="$1"
shift

FRAMEWORK=""
VERSION=""
MODE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--framework) FRAMEWORK="$2"; shift 2 ;;
        -v|--version) VERSION="$2"; shift 2 ;;
        -m|--mode) MODE="$2"; shift 2 ;;
        -h|--help) usage ;;
        -*) echo "Unknown option: $1" >&2; usage ;;
        *) echo "Unexpected argument: $1" >&2; usage ;;
    esac
done

# Validate required arguments
if [[ ! -f "$DATA_FILE" ]]; then
    echo "Error: File not found: $DATA_FILE" >&2
    exit 1
fi

[[ -z "$FRAMEWORK" ]] && { echo "Error: -f/--framework is required" >&2; usage; }
[[ -z "$VERSION" ]] && { echo "Error: -v/--version is required" >&2; usage; }
[[ -z "$MODE" ]] && { echo "Error: -m/--mode is required" >&2; usage; }

# Validate framework
case "$FRAMEWORK" in
    html|react|vue) ;;
    *) echo "Error: framework must be html, react, or vue" >&2; exit 1 ;;
esac

# Validate version
case "$VERSION" in
    3|4) ;;
    *) echo "Error: version must be 3 or 4" >&2; exit 1 ;;
esac

# Validate mode
case "$MODE" in
    light|dark|system|none) ;;
    *) echo "Error: mode must be light, dark, system, or none" >&2; exit 1 ;;
esac

# Mode validation based on component category
if [[ "$FULL_NAME" == Ecommerce* ]] || [[ "$FULL_NAME" == eCommerce* ]]; then
    if [[ "$MODE" != "none" ]]; then
        echo "Error: eCommerce component '$FULL_NAME' must use mode='none'. Got mode='$MODE'." >&2
        echo "eCommerce components only support mode='none'." >&2
        exit 1
    fi
else
    if [[ "$MODE" == "none" ]]; then
        echo "Error: Component '$FULL_NAME' cannot use mode='none'. Got mode='$MODE'." >&2
        echo "Application UI and Marketing components support modes: 'light', 'dark', 'system'." >&2
        exit 1
    fi
fi

# Get component using jq
result=$(jq -r --arg name "$FULL_NAME" --arg fw "$FRAMEWORK" --arg ver "$VERSION" --arg mode "$MODE" '
  # Convert dotted path to array and navigate
  ($name | split(".")) as $path |
  (reduce $path[] as $key (.tailwindplus; .[$key] // null)) as $component |

  if $component == null then
    "ERROR: Component not found: \($name)"
  elif ($component | has("snippets") | not) then
    "ERROR: \($name) is not a component (no snippets found)"
  else
    # Find matching snippet
    (
      $component.snippets |
      map(select(
        .name == $fw and
        (.version | tostring) == $ver and
        (if .mode == null then "none" else .mode end) == $mode
      ))
    ) as $matches |

    if ($matches | length) == 0 then
      # Provide helpful error with available options
      (
        $component.snippets |
        map("\(.name)/v\(.version)/\(if .mode == null then "none" else .mode end)") |
        unique |
        sort |
        join(", ")
      ) as $available |
      "ERROR: No snippet found for \($fw)/v\($ver)/\($mode)\nAvailable combinations: \($available)"
    else
      $matches[0] |
      "# Component: \($name)",
      "# Framework: \(.name)",
      "# Tailwind Version: \(.version)",
      "# Mode: \(if .mode == null then "none" else .mode end)",
      "# Language: \(.language)",
      "# Supports Dark Mode: \(.supportsDarkMode)",
      "------------------------------------------------------------",
      .code
    end
  end
' "$DATA_FILE")

# Check for errors
if [[ "$result" == ERROR:* ]]; then
    echo "$result" >&2
    exit 1
fi

echo "$result"
