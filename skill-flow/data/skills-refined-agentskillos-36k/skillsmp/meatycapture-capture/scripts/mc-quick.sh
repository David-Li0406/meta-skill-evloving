#!/usr/bin/env bash
set -e

# Temp file cleanup trap
TEMP_JSON=""
cleanup() {
  if [[ -n "$TEMP_JSON" && -f "$TEMP_JSON" ]]; then
    rm -f "$TEMP_JSON"
  fi
}
trap cleanup EXIT INT TERM

# Environment variable defaults
MC_PROJECT="${MC_PROJECT:-skillmeat}"
MC_PRIORITY="${MC_PRIORITY:-medium}"
MC_STATUS="${MC_STATUS:-triage}"

# Valid types
VALID_TYPES=("enhancement" "bug" "idea" "task" "question")

# Usage function
show_usage() {
  cat << EOF
Usage: mc-quick.sh TYPE DOMAIN SUBDOMAIN "Title" "Problem" "Goal" [additional notes...]

Positional Arguments:
  TYPE        One of: enhancement, bug, idea, task, question
  DOMAIN      Primary domain (comma-separated for multiple)
  SUBDOMAIN   Subdomain/component (comma-separated for multiple)
  TITLE       Short title for the capture
  PROBLEM     Description of the problem
  GOAL        Description of the desired outcome

Optional Arguments:
  [notes...]  Additional notes (each arg becomes a separate note)

Environment Variables:
  MC_PROJECT  Project name (default: skillmeat)
  MC_PRIORITY Priority level (default: medium)
  MC_STATUS   Status (default: triage)

Examples:
  mc-quick.sh enhancement web "deployments,modal" \\
    "Implement Remove button" \\
    "Button shows not implemented" \\
    "Full removal with filesystem toggle"

  MC_PRIORITY=high mc-quick.sh bug api validation \\
    "Fix auth timeout" \\
    "Sessions expire too quickly" \\
    "Extend session TTL to 24 hours"

EOF
  exit 1
}

# Check for help flag
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  show_usage
fi

# Validate minimum argument count
if [[ $# -lt 6 ]]; then
  echo "❌ Error: Minimum 6 arguments required" >&2
  echo "" >&2
  show_usage
fi

# Parse positional arguments
TYPE="$1"
DOMAIN="$2"
SUBDOMAIN="$3"
TITLE="$4"
PROBLEM="$5"
GOAL="$6"
shift 6

# Validate TYPE
type_valid=false
for valid_type in "${VALID_TYPES[@]}"; do
  if [[ "$TYPE" == "$valid_type" ]]; then
    type_valid=true
    break
  fi
done

if [[ "$type_valid" == false ]]; then
  echo "❌ Error: TYPE must be one of: ${VALID_TYPES[*]}" >&2
  exit 1
fi

# Smart auto-tagging: split comma-separated values and merge
build_tags() {
  local tags=()

  # Split DOMAIN on commas
  IFS=',' read -ra domain_parts <<< "$DOMAIN"
  for part in "${domain_parts[@]}"; do
    # Trim whitespace
    part=$(echo "$part" | xargs)
    if [[ -n "$part" ]]; then
      tags+=("\"$part\"")
    fi
  done

  # Split SUBDOMAIN on commas
  IFS=',' read -ra subdomain_parts <<< "$SUBDOMAIN"
  for part in "${subdomain_parts[@]}"; do
    # Trim whitespace
    part=$(echo "$part" | xargs)
    if [[ -n "$part" ]]; then
      tags+=("\"$part\"")
    fi
  done

  # Join with commas
  local IFS=','
  echo "${tags[*]}"
}

TAGS=$(build_tags)

# Build notes array
build_notes() {
  local notes=()

  # Add Problem and Goal
  notes+=("\"Problem: $PROBLEM\"")
  notes+=("\"Goal: $GOAL\"")

  # Add any additional notes
  for note in "$@"; do
    notes+=("\"$note\"")
  done

  # Join with commas
  local IFS=','
  echo "${notes[*]}"
}

NOTES=$(build_notes "$@")

# Build domain array from comma-separated string
build_domain_array() {
  local input="$1"
  local parts=()
  IFS=',' read -ra split_parts <<< "$input"
  for part in "${split_parts[@]}"; do
    part=$(echo "$part" | xargs)
    if [[ -n "$part" ]]; then
      parts+=("\"$part\"")
    fi
  done
  local IFS=','
  echo "${parts[*]}"
}

DOMAIN_ARRAY=$(build_domain_array "$DOMAIN")
SUBDOMAIN_ARRAY=$(build_domain_array "$SUBDOMAIN")

# Build JSON structure (wrapped in project/items format for meatycapture)
JSON_PAYLOAD=$(cat << EOF
{
  "project": "$MC_PROJECT",
  "items": [{
    "title": "$TITLE",
    "type": "$TYPE",
    "domain": [$DOMAIN_ARRAY],
    "subdomain": [$SUBDOMAIN_ARRAY],
    "priority": "$MC_PRIORITY",
    "status": "$MC_STATUS",
    "tags": [$TAGS],
    "notes": [$NOTES]
  }]
}
EOF
)

# Write to temp file (workaround for stdin bug)
TEMP_JSON=$(mktemp)
echo "$JSON_PAYLOAD" > "$TEMP_JSON"

# Call meatycapture with temp file
if meatycapture log create "$TEMP_JSON" --json; then
  echo "✓ Capture successful" >&2
  exit 0
else
  echo "❌ Capture failed" >&2
  exit 1
fi
