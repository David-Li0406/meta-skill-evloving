#!/bin/bash
# Forma - Template Viewer & Copier
#
# Usage:
#   forma list                    List available templates
#   forma show <name>             Show template content
#   forma copy <name> <target>    Copy template to target (Context-saving)
#
# Templates are stored in blueprint/templates/*.template.md

set -e

# Source common functions
source "$(dirname "$0")/../_common.sh"

# Check project initialization
check_project_initialized

COMMAND="$1"
TEMPLATE_DIR="$BLUEPRINT_DATA_DIR/templates"

# === LIST ===
do_list() {
  if [ ! -d "$TEMPLATE_DIR" ]; then
    error "Template directory not found: $TEMPLATE_DIR"
    exit 1
  fi

  local found=0
  echo "Available templates:"
  echo ""

  for file in "$TEMPLATE_DIR"/*.template.md; do
    if [ -f "$file" ]; then
      name=$(basename "$file" .template.md)
      echo "  - $name"
      found=1
    fi
  done

  if [ "$found" -eq 0 ]; then
    echo "  (no templates found)"
  fi
}

# === SHOW ===
do_show() {
  local name="$1"

  if [ -z "$name" ]; then
    echo "Usage: forma show <name>"
    echo ""
    echo "Examples:"
    echo "  blueprint.sh forma show plan"
    echo "  blueprint.sh forma show brief"
    echo "  blueprint.sh forma show lib-spec"
    echo ""
    echo "Run 'blueprint.sh forma list' to see available templates."
    exit 1
  fi

  local template_file="$TEMPLATE_DIR/${name}.template.md"

  if [ ! -f "$template_file" ]; then
    error "Template not found: $name"
    echo ""
    echo "Available templates:"
    for file in "$TEMPLATE_DIR"/*.template.md; do
      if [ -f "$file" ]; then
        n=$(basename "$file" .template.md)
        echo "  - $n"
      fi
    done
    exit 1
  fi

  cat "$template_file"
}

# === COPY ===
do_copy() {
  local name="$1"
  local target="$2"

  if [ -z "$name" ] || [ -z "$target" ]; then
    echo "Usage: forma copy <template> <target>"
    echo ""
    echo "Examples:"
    echo "  blueprint.sh forma copy plan blueprint/plans/001-feature/"
    echo "  blueprint.sh forma copy brief blueprint/plans/001-feature/my-brief.md"
    echo ""
    echo "If target is a directory (ends with / or exists), file is named after template."
    echo "If target is a file path, that exact path is used."
    exit 1
  fi

  local template_file="$TEMPLATE_DIR/${name}.template.md"

  if [ ! -f "$template_file" ]; then
    error "Template not found: $name"
    echo ""
    echo "Available templates:"
    for file in "$TEMPLATE_DIR"/*.template.md; do
      if [ -f "$file" ]; then
        n=$(basename "$file" .template.md)
        echo "  - $n"
      fi
    done
    exit 1
  fi

  # Determine output path
  local output_file
  if [[ "$target" == */ ]] || [ -d "$target" ]; then
    # Target is directory → use template name
    mkdir -p "$target"
    output_file="${target%/}/${name}.md"
  else
    # Target is file path
    mkdir -p "$(dirname "$target")"
    output_file="$target"
  fi

  # Copy template
  cp "$template_file" "$output_file"
  echo "Created: $output_file"
}

# === MAIN ===
case "$COMMAND" in
  list)
    do_list
    ;;
  show)
    shift
    do_show "$@"
    ;;
  copy)
    shift
    do_copy "$@"
    ;;
  *)
    echo "Forma - Template Viewer & Copier"
    echo ""
    echo "Usage:"
    echo "  forma list                    List available templates"
    echo "  forma show <name>             Show template content"
    echo "  forma copy <name> <target>    Copy template to target"
    echo ""
    echo "Examples:"
    echo "  blueprint.sh forma list"
    echo "  blueprint.sh forma show plan"
    echo "  blueprint.sh forma copy plan blueprint/plans/001-feature/"
    exit 1
    ;;
esac
