#!/bin/bash
# Frontis - FrontMatter Search & Schema Viewer
#
# Usage:
#   frontis search <field> <value> [path]    Search documents by FrontMatter
#   frontis show <file> [file...]            Show frontmatter of file(s)
#   frontis schema <type>                    View schema definition
#   frontis schema --list                    List available schemas
#
# Supports both Markdown (.md) and YAML (.yaml) files

set -e

# Source common functions
source "$(dirname "$0")/../_common.sh"

# Check project initialization
check_project_initialized

COMMAND="$1"
SCHEMA_DIR="$BLUEPRINT_DATA_DIR/front-matters"

# === SEARCH ===
do_search() {
  local field="$1"
  local value="$2"
  local search_path="${3:-.}"

  if [ -z "$field" ] || [ -z "$value" ]; then
    echo "Usage: frontis search <field> <value> [path]"
    echo ""
    echo "Examples:"
    echo "  blueprint.sh frontis search type spec"
    echo "  blueprint.sh frontis search status ready blueprint/specs/"
    echo "  blueprint.sh frontis search spec-type lib blueprint/specs/lib/"
    exit 1
  fi

  # Check if search path exists
  if [ ! -d "$search_path" ]; then
    error "Search path not found: $search_path"
    exit 1
  fi

  local found=0
  # Search both .md and .yaml files
  while IFS= read -r file; do
    frontmatter=$(get_frontmatter "$file")
    if echo "$frontmatter" | grep -q "^${field}: *${value}"; then
      echo "$file"
      found=1
    fi
  done < <(find "$search_path" \( -name "*.md" -o -name "*.yaml" \) -type f 2>/dev/null)

  if [ "$found" -eq 0 ]; then
    info "No documents found with ${field}: ${value} in ${search_path}"
  fi
}

# === SHOW ===
do_show() {
  if [ $# -eq 0 ]; then
    echo "Usage: frontis show <file> [file...]"
    echo ""
    echo "Examples:"
    echo "  blueprint.sh frontis show blueprint/discussions/001.md"
    echo "  blueprint.sh frontis show blueprint/specs/lib/prompt/spec.yaml"
    exit 1
  fi

  for file in "$@"; do
    if [ ! -f "$file" ]; then
      echo "=== $file ==="
      echo "File not found"
      echo ""
      continue
    fi

    echo "=== $file ==="
    if [[ "$file" == *.yaml ]]; then
      # YAML: show entire file (it's all structured data)
      cat "$file" 2>/dev/null
    else
      # Markdown: show frontmatter block only
      awk '/^---$/{if(++c==2){print "---"; exit}}{if(c)print}' "$file" 2>/dev/null
    fi
    echo ""
  done
}

# === SCHEMA ===
do_schema() {
  local type="$1"

  # --list: Show available schemas
  if [ "$type" = "--list" ] || [ "$type" = "-l" ]; then
    if [ ! -d "$SCHEMA_DIR" ]; then
      error "Schema directory not found: $SCHEMA_DIR"
      exit 1
    fi

    local found=0
    echo "Available schemas:"
    echo ""
    for file in "$SCHEMA_DIR"/*.schema.md; do
      if [ -f "$file" ]; then
        name=$(basename "$file" .schema.md)
        echo "  - $name"
        found=1
      fi
    done

    if [ "$found" -eq 0 ]; then
      echo "  (no schemas found)"
    fi
    exit 0
  fi

  # No type: show usage
  if [ -z "$type" ]; then
    echo "Usage: frontis schema <type>"
    echo "       frontis schema --list"
    echo ""
    echo "Examples:"
    echo "  blueprint.sh frontis schema spec"
    echo "  blueprint.sh frontis schema tokens"
    echo "  blueprint.sh frontis schema ast"
    exit 1
  fi

  # Show specific schema
  # "schema" type uses base.schema.md (avoids self-referential schema.schema.md)
  if [ "$type" = "schema" ]; then
    type="base"
  fi

  local schema_file="$SCHEMA_DIR/${type}.schema.md"

  if [ ! -f "$schema_file" ]; then
    echo "Schema not found: $type"
    echo ""
    echo "Available schemas:"
    for file in "$SCHEMA_DIR"/*.schema.md; do
      if [ -f "$file" ]; then
        name=$(basename "$file" .schema.md)
        echo "  - $name"
      fi
    done
    exit 1
  fi

  cat "$schema_file"
}

# === MAIN ===
case "$COMMAND" in
  search)
    shift
    do_search "$@"
    ;;
  show)
    shift
    do_show "$@"
    ;;
  schema)
    shift
    do_schema "$@"
    ;;
  *)
    echo "Frontis - FrontMatter Search & Schema Viewer"
    echo ""
    echo "Usage:"
    echo "  frontis search <field> <value> [path]    Search by FrontMatter"
    echo "  frontis show <file> [file...]            Show frontmatter"
    echo "  frontis schema <type>                    View schema"
    echo "  frontis schema --list                    List schemas"
    echo ""
    echo "Supported file types: .md, .yaml"
    echo ""
    echo "Examples:"
    echo "  blueprint.sh frontis search type spec"
    echo "  blueprint.sh frontis search status ready blueprint/specs/"
    echo "  blueprint.sh frontis show blueprint/specs/lib/prompt/spec.yaml"
    echo "  blueprint.sh frontis schema spec"
    exit 1
    ;;
esac
