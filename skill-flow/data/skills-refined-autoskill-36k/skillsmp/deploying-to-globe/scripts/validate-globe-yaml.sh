#!/usr/bin/env bash
# Validates globe.yaml configuration
# Usage: bash validate-globe-yaml.sh [path/to/globe.yaml]
#
# This script performs local validation without external dependencies.
# For full schema validation, use: https://globe.dev/globe.schema.json

set -e

GLOBE_YAML="${1:-globe.yaml}"

# Colors (disabled if not terminal)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    NC=''
fi

error() {
    echo -e "${RED}✗ $1${NC}" >&2
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Check if file exists
if [ ! -f "$GLOBE_YAML" ]; then
    error "File not found: $GLOBE_YAML"
    exit 1
fi

ERRORS=0

# Basic YAML syntax check (works without dependencies)
# Check for tabs (YAML doesn't allow tabs for indentation)
if grep -q $'\t' "$GLOBE_YAML"; then
    error "YAML syntax: tabs found (use spaces for indentation)"
    ERRORS=$((ERRORS + 1))
fi

# Check for common YAML issues (missing space after colon, excluding URLs and empty values)
# This is a simple heuristic, not a full YAML parser
if grep -E '^[a-zA-Z_][a-zA-Z0-9_]*:[^ [:space:]]' "$GLOBE_YAML" | grep -vE '://' | grep -q .; then
    error "YAML syntax: possible missing space after colon"
    ERRORS=$((ERRORS + 1))
fi

# Extract values using grep/sed (no external deps)
get_value() {
    grep -E "^${1}:" "$GLOBE_YAML" 2>/dev/null | sed "s/^${1}:[[:space:]]*//" | tr -d '"' | tr -d "'" || true
}

get_nested_value() {
    # Simple nested value extraction: parent.child
    local parent="$1"
    local child="$2"
    sed -n "/^${parent}:/,/^[^ ]/p" "$GLOBE_YAML" 2>/dev/null | grep -E "^[[:space:]]+${child}:" | sed "s/.*${child}:[[:space:]]*//" | tr -d '"' | tr -d "'" | head -1 || true
}

# Validate preset type
PRESET_TYPE=$(get_nested_value "build" "type" | head -1)
if [ -n "$PRESET_TYPE" ]; then
    VALID_PRESETS="dart_frog jaspr jaspr_static flutter flutter_server serverpod shelf"
    if ! echo "$VALID_PRESETS" | grep -qw "$PRESET_TYPE"; then
        error "Invalid preset type: '$PRESET_TYPE'"
        echo "  Valid presets: $VALID_PRESETS" >&2
        ERRORS=$((ERRORS + 1))
    fi
fi

# Validate cron jobs
if grep -q "^crons:" "$GLOBE_YAML"; then
    # Extract cron IDs
    CRON_IDS=$(grep -E "^[[:space:]]+-?[[:space:]]*id:" "$GLOBE_YAML" | sed 's/.*id:[[:space:]]*//' | tr -d '"' | tr -d "'")

    for CRON_ID in $CRON_IDS; do
        # Check ID format: 1-50 chars, alphanumeric + underscores
        if ! echo "$CRON_ID" | grep -qE '^[a-zA-Z0-9_]{1,50}$'; then
            error "Invalid cron id: '$CRON_ID' (must be 1-50 chars, alphanumeric + underscores)"
            ERRORS=$((ERRORS + 1))
        fi
    done

    # Check for required cron fields
    CRON_COUNT=$(grep -cE "^[[:space:]]+-[[:space:]]*id:" "$GLOBE_YAML" 2>/dev/null || echo "0")
    SCHEDULE_COUNT=$(grep -cE "^[[:space:]]+schedule:" "$GLOBE_YAML" 2>/dev/null || echo "0")
    PATH_COUNT=$(grep -cE "^[[:space:]]+path:" "$GLOBE_YAML" 2>/dev/null || echo "0")

    if [ "$CRON_COUNT" != "$SCHEDULE_COUNT" ]; then
        error "Cron jobs: some crons missing 'schedule' field"
        ERRORS=$((ERRORS + 1))
    fi

    if [ "$CRON_COUNT" != "$PATH_COUNT" ]; then
        error "Cron jobs: some crons missing 'path' field"
        ERRORS=$((ERRORS + 1))
    fi
fi

# Validate preferred_regions
if grep -q "^preferred_regions:" "$GLOBE_YAML"; then
    VALID_REGIONS="africa-south1 asia-east1 asia-east2 asia-northeast1 asia-northeast2 asia-northeast3 asia-south1 asia-south2 asia-southeast1 asia-southeast2 australia-southeast1 australia-southeast2 europe-central2 europe-north1 europe-southwest1 europe-west1 europe-west2 europe-west3 europe-west4 europe-west6 europe-west8 europe-west9 europe-west10 europe-west12 me-central1 me-central2 me-west1 northamerica-northeast1 northamerica-northeast2 northamerica-south1 southamerica-east1 southamerica-west1 us-central1 us-east1 us-east4 us-east5 us-south1 us-west1 us-west2 us-west4"

    # Extract regions from the list
    REGIONS=$(sed -n '/^preferred_regions:/,/^[^ ]/p' "$GLOBE_YAML" | grep -E "^[[:space:]]+-" | sed 's/.*-[[:space:]]*//' | tr -d '"' | tr -d "'")

    for REGION in $REGIONS; do
        if ! echo "$VALID_REGIONS" | grep -qw "$REGION"; then
            error "Invalid preferred_region: '$REGION'"
            ERRORS=$((ERRORS + 1))
        fi
    done
fi

# Validate entrypoint exists (if specified and file path looks local)
ENTRYPOINT=$(get_value "entrypoint")
if [ -n "$ENTRYPOINT" ] && [[ "$ENTRYPOINT" == *.dart ]]; then
    if [ ! -f "$ENTRYPOINT" ]; then
        # Only warn, don't error - file might exist in different context
        echo "Warning: entrypoint '$ENTRYPOINT' not found in current directory" >&2
    fi
fi

# Summary
if [ $ERRORS -eq 0 ]; then
    success "globe.yaml validation passed"
    exit 0
else
    error "Validation failed with $ERRORS error(s)"
    exit 1
fi
