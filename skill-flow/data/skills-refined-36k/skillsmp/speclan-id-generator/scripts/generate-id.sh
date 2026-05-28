#!/bin/bash
#
# SPECLAN ID Generator
# Generate unique random IDs for SPECLAN entities with collision detection
#
# Usage: ./generate-id.sh <entity-type> [count] [speclan-dir]
#
# Entity types: goal, feature, requirement, change-request, scenario,
#               acceptance-criterion, test
#
# Output: Unique ID(s) to stdout, one per line
# Exit codes: 0 = success, 1 = error

# Configuration
MAX_ATTEMPTS=100

# Track generated IDs within this session to avoid duplicates
GENERATED_IDS=""

# Print usage
usage() {
  cat << EOF
Usage: $(basename "$0") <entity-type> [count] [speclan-dir]

Generate unique random ID(s) for SPECLAN entities.

Entity types:
  goal                 G-### (3 digits, 100-999)
  feature              F-#### (4 digits, 1000-9999)
  requirement          R-#### (4 digits, 1000-9999)
  change-request       CR-#### (4 digits, 1000-9999)
  scenario             S-#### (4 digits, 1000-9999)
  acceptance-criterion AC-#### (4 digits, 1000-9999)
  test                 T-#### (4 digits, 1000-9999)

Arguments:
  entity-type   Required. One of the types listed above.
  count         Optional. Number of IDs to generate (default: 1)
  speclan-dir   Optional. Path to speclan directory (default: ./speclan)

Output:
  Prints unique ID(s) to stdout, one per line

Examples:
  $(basename "$0") feature              # Single feature ID
  $(basename "$0") requirement 5        # 5 requirement IDs
  $(basename "$0") feature 3 ./speclan  # 3 feature IDs with custom path
EOF
  exit 1
}

# Get entity configuration: prefix, digits, range_min, range_max
get_entity_config() {
  local entity_type="$1"

  case "$entity_type" in
    goal)
      echo "G-:3:100:999"
      ;;
    feature)
      echo "F-:4:1000:9999"
      ;;
    requirement)
      echo "R-:4:1000:9999"
      ;;
    change-request)
      echo "CR-:4:1000:9999"
      ;;
    scenario)
      echo "S-:4:1000:9999"
      ;;
    acceptance-criterion)
      echo "AC-:4:1000:9999"
      ;;
    test)
      echo "T-:4:1000:9999"
      ;;
    *)
      echo ""
      ;;
  esac
}

# Check if ID exists in filenames
check_filename_collision() {
  local id="$1"
  local speclan_dir="$2"

  # Search for files starting with the ID
  if find "$speclan_dir" -name "${id}-*" -o -name "${id}.md" 2>/dev/null | grep -q .; then
    return 0  # Collision found
  fi
  return 1  # No collision
}

# Check if ID exists in frontmatter
check_frontmatter_collision() {
  local id="$1"
  local speclan_dir="$2"

  # Search for id: <ID> in frontmatter
  if grep -r "^id: ${id}$" "$speclan_dir" 2>/dev/null | grep -q .; then
    return 0  # Collision found
  fi
  return 1  # No collision
}

# Check if ID was already generated in this session
check_session_collision() {
  local id="$1"

  if echo "$GENERATED_IDS" | grep -q "^${id}$"; then
    return 0  # Collision found
  fi
  return 1  # No collision
}

# Check for any collision (filesystem + session)
collision_exists() {
  local id="$1"
  local speclan_dir="$2"

  # Check session-generated IDs first (fast)
  check_session_collision "$id" && return 0

  # Check filesystem if directory exists
  if [ -d "$speclan_dir" ]; then
    check_filename_collision "$id" "$speclan_dir" && return 0
    check_frontmatter_collision "$id" "$speclan_dir" && return 0
  fi

  return 1
}

# Generate random number in range
random_in_range() {
  local min="$1"
  local max="$2"
  local range=$((max - min + 1))
  echo $((RANDOM % range + min))
}

# Generate a single unique ID
generate_unique_id() {
  local entity_type="$1"
  local speclan_dir="$2"

  # Get entity configuration
  local config
  config=$(get_entity_config "$entity_type")

  if [ -z "$config" ]; then
    echo "ERROR: Unknown entity type: $entity_type" >&2
    return 1
  fi

  # Parse configuration (prefix:digits:range_min:range_max)
  local prefix digits range_min range_max
  prefix=$(echo "$config" | cut -d: -f1)
  digits=$(echo "$config" | cut -d: -f2)
  range_min=$(echo "$config" | cut -d: -f3)
  range_max=$(echo "$config" | cut -d: -f4)

  # Generate format string for printf
  local format_str
  if [ "$digits" -eq 3 ]; then
    format_str="%03d"
  else
    format_str="%04d"
  fi

  # Try to generate unique ID
  local attempt
  for attempt in $(seq 1 $MAX_ATTEMPTS); do
    # Generate random number in range
    local num
    num=$(random_in_range "$range_min" "$range_max")

    # Format ID
    local id
    id=$(printf "${prefix}${format_str}" "$num")

    # Check for collision
    if ! collision_exists "$id" "$speclan_dir"; then
      # Track this ID in the session
      GENERATED_IDS="${GENERATED_IDS}${id}
"
      echo "$id"
      return 0
    fi
  done

  echo "ERROR: Could not generate unique ID after $MAX_ATTEMPTS attempts" >&2
  echo "HINT: The ID space may be nearly full for entity type: $entity_type" >&2
  return 1
}

# Generate multiple unique IDs
generate_multiple_ids() {
  local entity_type="$1"
  local count="$2"
  local speclan_dir="$3"

  local i
  for i in $(seq 1 "$count"); do
    if ! generate_unique_id "$entity_type" "$speclan_dir"; then
      echo "ERROR: Failed to generate ID $i of $count" >&2
      return 1
    fi
  done

  return 0
}

# Main
main() {
  # Check arguments
  if [ $# -lt 1 ]; then
    echo "ERROR: Missing entity-type argument" >&2
    usage
  fi

  local entity_type="$1"
  local count="${2:-1}"
  local speclan_dir="${3:-./speclan}"

  # Check if second arg is a number (count) or a path (speclan-dir)
  if [ $# -eq 2 ]; then
    if [[ "$2" =~ ^[0-9]+$ ]]; then
      count="$2"
      speclan_dir="./speclan"
    else
      count="1"
      speclan_dir="$2"
    fi
  fi

  # Validate entity type
  local config
  config=$(get_entity_config "$entity_type")

  if [ -z "$config" ]; then
    echo "ERROR: Invalid entity type: $entity_type" >&2
    echo "" >&2
    echo "Valid types: goal, feature, requirement, change-request, scenario, acceptance-criterion, test" >&2
    exit 1
  fi

  # Validate count
  if ! [[ "$count" =~ ^[0-9]+$ ]] || [ "$count" -lt 1 ]; then
    echo "ERROR: Count must be a positive integer: $count" >&2
    exit 1
  fi

  # Generate and output the ID(s)
  generate_multiple_ids "$entity_type" "$count" "$speclan_dir"
}

main "$@"
