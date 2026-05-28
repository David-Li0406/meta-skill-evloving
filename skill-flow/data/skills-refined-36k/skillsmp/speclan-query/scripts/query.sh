#!/bin/bash
#
# SPECLAN Query Script
# Query SPECLAN entities with flexible filtering and JSON output
#
# Usage: ./query.sh [OPTIONS] [speclan-dir]
#
# Entity naming: {G|F|R|CR|S|AC|T}-{ID}-{slug}
# The filename/dirname is the source of truth for ID and slug.
#
# Exit codes: 0 = success, 1 = error

set -e
set -o pipefail

# Configuration
DEFAULT_SPECLAN_DIR="./speclan"

# Global variables (avoiding zsh reserved words)
entity_type=""
filter_status_value=""
parent_id=""
full_mode=false
speclan_dir=""

# Print usage
usage() {
  cat << 'EOF'
Usage: query.sh [OPTIONS] [speclan-dir]

Query SPECLAN entities with flexible filtering and JSON output.

Options:
  -t, --type TYPE              Entity type to query (required)
                               Values: goal, feature, requirement, scenario,
                                       acceptance-criterion, test, change-request, all
  -s, --filter-status STATUS   Filter by status (reads frontmatter)
                               Values: draft, review, approved, in-development,
                                       under-test, released, deprecated
  -p, --parent ID              Filter by parent ID (e.g., F-1234)
  -f, --full                   Include title and status in output (reads frontmatter)
  -h, --help                   Show this help

Arguments:
  speclan-dir                  Path to speclan directory (default: ./speclan)

Output:
  JSON array of entities to stdout

Examples:
  query.sh --type feature
  query.sh --type feature --full
  query.sh --type feature --filter-status approved
  query.sh --type requirement --parent F-1049
  query.sh --type all ./speclan

EOF
  exit 1
}

# Parse command-line arguments
parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -t|--type)
        if [[ -z "$2" || "$2" == -* ]]; then
          echo "ERROR: --type requires an argument" >&2
          usage
        fi
        entity_type="$2"
        shift 2
        ;;
      -s|--filter-status)
        if [[ -z "$2" || "$2" == -* ]]; then
          echo "ERROR: --filter-status requires an argument" >&2
          usage
        fi
        filter_status_value="$2"
        shift 2
        ;;
      -p|--parent)
        if [[ -z "$2" || "$2" == -* ]]; then
          echo "ERROR: --parent requires an argument" >&2
          usage
        fi
        parent_id="$2"
        shift 2
        ;;
      -f|--full)
        full_mode=true
        shift
        ;;
      -h|--help)
        usage
        ;;
      -*)
        echo "ERROR: Unknown option: $1" >&2
        usage
        ;;
      *)
        if [[ -n "$speclan_dir" ]]; then
          echo "ERROR: Multiple speclan-dir arguments provided" >&2
          usage
        fi
        speclan_dir="$1"
        shift
        ;;
    esac
  done

  # Set defaults
  [[ -z "$speclan_dir" ]] && speclan_dir="$DEFAULT_SPECLAN_DIR"

  # Validate required options
  if [[ -z "$entity_type" ]]; then
    echo "ERROR: --type is required" >&2
    usage
  fi
}

# Get find pattern for entity type
# Returns: pattern:search_subdir
get_entity_config() {
  local etype="$1"

  case "$etype" in
    goal)
      echo "G-*.md:goals"
      ;;
    feature)
      echo "F-*.md:features"
      ;;
    requirement)
      echo "R-*.md:features"
      ;;
    scenario)
      echo "S-*.md:features"
      ;;
    acceptance-criterion)
      echo "AC-*.md:features"
      ;;
    test)
      echo "T-*.md:features"
      ;;
    change-request)
      echo "CR-*.md:."
      ;;
    all)
      echo "*.md:."
      ;;
    *)
      return 1
      ;;
  esac
}

# Infer entity type from ID prefix
get_type_from_id() {
  local id="$1"

  case "$id" in
    G-*) echo "goal" ;;
    F-*) echo "feature" ;;
    R-*) echo "requirement" ;;
    CR-*) echo "change-request" ;;
    S-*) echo "scenario" ;;
    AC-*) echo "acceptance-criterion" ;;
    T-*) echo "test" ;;
    *) echo "unknown" ;;
  esac
}

# Parse filename to extract ID and slug
# Input: /path/to/F-1234-my-feature.md or /path/to/F-1234-my-feature/F-1234-my-feature.md
# Output: F-1234|my-feature
parse_filename() {
  local file="$1"
  local basename_no_ext
  basename_no_ext=$(basename "$file" .md)

  # Match pattern: PREFIX-DIGITS-slug
  # Examples: F-1234-slug, G-123-slug, CR-5678-slug, AC-9999-slug
  if [[ "$basename_no_ext" =~ ^([A-Z]+-[0-9]+)-(.+)$ ]]; then
    echo "${BASH_REMATCH[1]}|${BASH_REMATCH[2]}"
    return 0
  fi

  # Try simpler pattern for IDs without slug (shouldn't happen but handle gracefully)
  if [[ "$basename_no_ext" =~ ^([A-Z]+-[0-9]+)$ ]]; then
    echo "${BASH_REMATCH[1]}|"
    return 0
  fi

  return 1
}

# Extract field from YAML frontmatter
# Usage: get_frontmatter_field <file> <field>
get_frontmatter_field() {
  local file="$1"
  local field="$2"

  # Read between --- delimiters, extract field value
  # Handles both quoted and unquoted values
  awk -v field="$field" '
    BEGIN { in_fm = 0 }
    /^---$/ {
      if (in_fm) exit
      in_fm = 1
      next
    }
    in_fm && $0 ~ "^"field":" {
      sub("^"field":[ ]*", "")
      # Remove surrounding quotes if present
      gsub(/^["'\'']|["'\'']$/, "")
      print
      exit
    }
  ' "$file" 2>/dev/null
}

# Check if entity has specific parent
# Checks: feature, requirement, parentId, goals array
has_parent() {
  local file="$1"
  local pid="$2"

  # Also check if parent ID appears in file path (structural parent)
  if [[ "$file" == *"/$pid-"* ]]; then
    return 0
  fi

  # Check direct parent fields in frontmatter
  if grep -q "^feature: $pid$" "$file" 2>/dev/null; then
    return 0
  fi
  if grep -q "^feature: \"$pid\"$" "$file" 2>/dev/null; then
    return 0
  fi
  if grep -q "^requirement: $pid$" "$file" 2>/dev/null; then
    return 0
  fi
  if grep -q "^requirement: \"$pid\"$" "$file" 2>/dev/null; then
    return 0
  fi
  if grep -q "^parentId: $pid$" "$file" 2>/dev/null; then
    return 0
  fi
  if grep -q "^parentId: \"$pid\"$" "$file" 2>/dev/null; then
    return 0
  fi

  # Check array parent fields (goals)
  if grep -q "^  - $pid$" "$file" 2>/dev/null; then
    return 0
  fi
  if grep -q "^  - \"$pid\"$" "$file" 2>/dev/null; then
    return 0
  fi

  return 1
}

# Escape string for JSON
json_escape() {
  local str="$1"
  # Escape backslashes first, then quotes
  str="${str//\\/\\\\}"
  str="${str//\"/\\\"}"
  # Escape control characters
  str="${str//$'\n'/\\n}"
  str="${str//$'\r'/\\r}"
  str="${str//$'\t'/\\t}"
  echo "$str"
}

# Build JSON entry for an entity
build_json_entry() {
  local id="$1"
  local slug="$2"
  local etype="$3"
  local fpath="$4"
  local title="$5"
  local entity_status="$6"

  # Escape strings for JSON
  local slug_escaped=$(json_escape "$slug")
  local path_escaped=$(json_escape "$fpath")

  # Build minimal JSON
  local json="{\"id\":\"$id\",\"slug\":\"$slug_escaped\",\"type\":\"$etype\",\"path\":\"$path_escaped\""

  # Add full fields if available
  if [[ -n "$title" ]]; then
    local title_escaped=$(json_escape "$title")
    json="${json},\"title\":\"$title_escaped\""
  fi
  if [[ -n "$entity_status" ]]; then
    json="${json},\"status\":\"$entity_status\""
  fi

  json="${json}}"
  echo "$json"
}

# Query entities
query_entities() {
  local etype="$1"
  local sdir="$2"

  # Handle 'all' type specially - query each type
  if [[ "$etype" == "all" ]]; then
    local all_results=()
    local types=("goal" "feature" "requirement" "change-request" "scenario" "acceptance-criterion" "test")

    for t in "${types[@]}"; do
      local results
      if ! results=$(query_single_type "$t" "$sdir"); then
        echo "ERROR: Failed to query type: $t" >&2
        return 1
      fi
      # Extract entries from JSON array (strip [ and ])
      local entries
      entries=$(echo "$results" | sed '1d;$d' | sed 's/^  //')
      if [[ -n "$entries" && "$entries" != "" ]]; then
        all_results+=("$entries")
      fi
    done

    # Combine all results
    echo "["
    local first=true
    for entry_block in "${all_results[@]}"; do
      while IFS= read -r entry; do
        [[ -z "$entry" ]] && continue
        # Remove trailing comma if present
        entry="${entry%,}"
        if [[ "$first" == true ]]; then
          first=false
        else
          echo ","
        fi
        echo -n "  $entry"
      done <<< "$entry_block"
    done
    echo ""
    echo "]"
    return 0
  fi

  query_single_type "$etype" "$sdir"
}

# Query single entity type
query_single_type() {
  local etype="$1"
  local sdir="$2"

  # Get entity configuration
  local config
  config=$(get_entity_config "$etype")
  if [[ $? -ne 0 ]]; then
    echo "ERROR: Invalid entity type: $etype" >&2
    echo "Valid types: goal, feature, requirement, scenario, acceptance-criterion, test, change-request, all" >&2
    exit 1
  fi

  local pattern search_subdir
  pattern=$(echo "$config" | cut -d: -f1)
  search_subdir=$(echo "$config" | cut -d: -f2)

  # Build search path
  local search_path="$sdir"
  if [[ "$search_subdir" != "." ]]; then
    search_path="$sdir/$search_subdir"
  fi

  # Check if search path exists
  if [[ ! -d "$search_path" ]]; then
    # Empty result for non-existent subdirectory
    echo "[]"
    return 0
  fi

  # Find matching files
  local files
  files=$(find "$search_path" -name "$pattern" -type f 2>/dev/null | sort)

  # Determine if we need to read frontmatter
  local needs_frontmatter=false
  if [[ "$full_mode" == true ]] || [[ -n "$filter_status_value" ]] || [[ -n "$parent_id" ]]; then
    needs_frontmatter=true
  fi

  # Process files and build JSON entries
  local json_entries=()

  while IFS= read -r file; do
    [[ -z "$file" ]] && continue

    # Skip template files
    if [[ "$file" == *"/templates/"* ]]; then
      continue
    fi

    # Skip archived files
    if [[ "$file" == *"/_archived/"* ]]; then
      continue
    fi

    # Parse filename
    local parsed
    parsed=$(parse_filename "$file")
    if [[ $? -ne 0 ]]; then
      # Skip files that don't match pattern
      continue
    fi

    local id slug
    id=$(echo "$parsed" | cut -d'|' -f1)
    slug=$(echo "$parsed" | cut -d'|' -f2)

    # Infer type from ID if querying 'all'
    local file_type="$etype"
    if [[ "$etype" == "all" ]]; then
      file_type=$(get_type_from_id "$id")
    fi

    # Read frontmatter if needed
    local title="" entity_status=""
    if [[ "$needs_frontmatter" == true ]]; then
      entity_status=$(get_frontmatter_field "$file" "status")

      # Apply status filter
      if [[ -n "$filter_status_value" ]] && [[ "$entity_status" != "$filter_status_value" ]]; then
        continue
      fi

      # Apply parent filter
      if [[ -n "$parent_id" ]]; then
        if ! has_parent "$file" "$parent_id"; then
          continue
        fi
      fi

      # Get title if full mode
      if [[ "$full_mode" == true ]]; then
        title=$(get_frontmatter_field "$file" "title")
      fi
    fi

    # Build JSON entry
    local entry
    entry=$(build_json_entry "$id" "$slug" "$file_type" "$file" "$title" "$entity_status")
    json_entries+=("$entry")

  done <<< "$files"

  # Output JSON array
  echo "["
  local first=true
  for entry in "${json_entries[@]}"; do
    if [[ "$first" == true ]]; then
      first=false
    else
      echo ","
    fi
    echo -n "  $entry"
  done
  if [[ ${#json_entries[@]} -gt 0 ]]; then
    echo ""
  fi
  echo "]"
}

# Main
main() {
  parse_args "$@"

  # Validate speclan directory
  if [[ ! -d "$speclan_dir" ]]; then
    echo "ERROR: Speclan directory not found: $speclan_dir" >&2
    exit 1
  fi

  # Execute query
  query_entities "$entity_type" "$speclan_dir"
}

main "$@"
