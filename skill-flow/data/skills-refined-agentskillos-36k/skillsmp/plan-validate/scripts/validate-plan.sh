#!/usr/bin/env bash
set -euo pipefail

# validate-plan.sh - Validate plan document frontmatter
# Usage: ./validate-plan.sh <plan-file>

PLAN_FILE="${1:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Error counter
ERRORS=0

error() {
	echo -e "${RED}✗${NC} $1" >&2
	((ERRORS++))
}

warning() {
	echo -e "${YELLOW}⚠${NC} $1" >&2
}

success() {
	echo -e "${GREEN}✓${NC} $1"
}

# Check arguments
if [[ -z "$PLAN_FILE" ]]; then
	echo "Usage: $0 <plan-file>" >&2
	exit 1
fi

if [[ ! -f "$PLAN_FILE" ]]; then
	error "Plan file not found: $PLAN_FILE"
	exit 1
fi

echo "Validating plan: $PLAN_FILE"
echo

# Extract frontmatter (between first and second ---)
FRONTMATTER=$(awk '/^---$/{if(++count==2)exit;next}count==1' "$PLAN_FILE")

if [[ -z "$FRONTMATTER" ]]; then
	error "No frontmatter found (missing --- delimiters)"
	exit 1
fi

# Helper function to extract YAML field
get_field() {
	local field="$1"
	echo "$FRONTMATTER" | grep "^${field}:" | sed "s/^${field}: *//" | tr -d '"' | tr -d "'"
}

# Helper function to check if field exists
has_field() {
	local field="$1"
	echo "$FRONTMATTER" | grep -q "^${field}:"
}

# Validate required fields
echo "Checking required fields..."

REQUIRED_FIELDS=("name" "title" "created" "status" "progress")
for field in "${REQUIRED_FIELDS[@]}"; do
	if has_field "$field"; then
		success "Required field '$field' present"
	else
		error "Missing required field: $field"
	fi
done

# Validate field values
echo
echo "Validating field values..."

# Validate name (kebab-case)
if has_field "name"; then
	NAME=$(get_field "name")
	if [[ "$NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
		success "name: '$NAME' (valid kebab-case)"
	else
		error "name: '$NAME' (must be kebab-case: lowercase, hyphens only)"
	fi
fi

# Validate status
if has_field "status"; then
	STATUS=$(get_field "status")
	VALID_STATUSES=("ready" "in-progress" "blocked" "completed" "abandoned")
	if [[ " ${VALID_STATUSES[*]} " =~ \ ${STATUS}\  ]]; then
		success "status: '$STATUS' (valid)"
	else
		error "status: '$STATUS' (must be one of: ${VALID_STATUSES[*]})"
	fi
fi

# Validate progress
if has_field "progress"; then
	PROGRESS=$(get_field "progress")
	if [[ "$PROGRESS" =~ ^[0-9]+$ ]] && [[ "$PROGRESS" -ge 0 ]] && [[ "$PROGRESS" -le 100 ]]; then
		success "progress: $PROGRESS% (valid)"
	else
		error "progress: $PROGRESS (must be integer 0-100)"
	fi
fi

# Validate date format (YYYY-MM-DD)
validate_date() {
	local field="$1"
	if has_field "$field"; then
		local date
		date=$(get_field "$field")
		if [[ "$date" == "null" ]] || [[ -z "$date" ]]; then
			return 0
		fi
		if [[ "$date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
			success "$field: $date (valid format)"
		else
			error "$field: $date (must be YYYY-MM-DD)"
		fi
	fi
}

validate_date "created"
validate_date "updated"
validate_date "started"
validate_date "completed"
validate_date "archived"

# Validate status-progress alignment
if has_field "status" && has_field "progress"; then
	STATUS=$(get_field "status")
	PROGRESS=$(get_field "progress")

	case "$STATUS" in
		ready)
			if [[ "$PROGRESS" -eq 0 ]]; then
				success "Status '$STATUS' with progress $PROGRESS% (aligned)"
			else
				warning "Status 'ready' should have progress 0%, found $PROGRESS%"
			fi
			;;
		completed)
			if [[ "$PROGRESS" -eq 100 ]]; then
				success "Status '$STATUS' with progress $PROGRESS% (aligned)"
			else
				error "Status 'completed' must have progress 100%, found $PROGRESS%"
			fi
			;;
		in-progress|blocked)
			if [[ "$PROGRESS" -gt 0 ]] && [[ "$PROGRESS" -lt 100 ]]; then
				success "Status '$STATUS' with progress $PROGRESS% (aligned)"
			else
				warning "Status '$STATUS' should have progress 1-99%, found $PROGRESS%"
			fi
			;;
	esac
fi

# Check for completed requirements
if has_field "status"; then
	STATUS=$(get_field "status")
	if [[ "$STATUS" == "completed" ]]; then
		echo
		echo "Checking 'completed' status requirements..."

		if has_field "completed" && [[ -n "$(get_field "completed")" ]]; then
			success "completed date present"
		else
			error "Status 'completed' requires 'completed' date field"
		fi

		if has_field "outcome" && [[ -n "$(get_field "outcome")" ]]; then
			OUTCOME=$(get_field "outcome")
			VALID_OUTCOMES=("success" "partial" "failed")
			if [[ " ${VALID_OUTCOMES[*]} " =~ \ ${OUTCOME}\  ]]; then
				success "outcome: '$OUTCOME' (valid)"
			else
				error "outcome: '$OUTCOME' (must be one of: ${VALID_OUTCOMES[*]})"
			fi
		else
			error "Status 'completed' requires 'outcome' field"
		fi
	fi

	if [[ "$STATUS" == "abandoned" ]]; then
		echo
		echo "Checking 'abandoned' status requirements..."

		if has_field "completed" && [[ -n "$(get_field "completed")" ]]; then
			success "completed date present"
		else
			error "Status 'abandoned' requires 'completed' date field"
		fi

		if has_field "archival-reason" && [[ -n "$(get_field "archival-reason")" ]]; then
			success "archival-reason present"
		else
			error "Status 'abandoned' requires 'archival-reason' field"
		fi
	fi
fi

# Summary
echo
echo "----------------------------------------"
if [[ $ERRORS -eq 0 ]]; then
	success "Validation passed! No errors found."
	exit 0
else
	error "Validation failed with $ERRORS error(s)"
	exit 1
fi
