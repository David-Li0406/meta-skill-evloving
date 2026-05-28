#!/usr/bin/env bash
set -euo pipefail

# Explore implementation plans with filtering, health analysis, and
# multiple output formats
# Usage: explore-plans.sh [module] [options]

# Default values
MODULE=""
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
STATUS_FILTER=""
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
DESIGN_DOC=""
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
OWNER=""
FORMAT="summary"
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
SHOW_PHASES=false
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
SHOW_HEALTH=true
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
ORPHANS_ONLY=false
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
STALE_ONLY=false
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
BLOCKED_ONLY=false
AGE_THRESHOLD=30
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
TODAY=$(date +%Y-%m-%d)

# Colors
RED='\033[0;31m'
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
CYAN='\033[0;36m'
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Emoji indicators
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
EMOJI_READY="📅"
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
EMOJI_IN_PROGRESS="🚧"
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
EMOJI_BLOCKED="⏸️ "
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
EMOJI_COMPLETED="✅"
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
EMOJI_ABANDONED="❌"
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
EMOJI_WARNING="⚠️ "
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
EMOJI_CHECK="✅"
# shellcheck disable=SC2034  # Will be used in Day 2-4 implementation
EMOJI_PLAN="📋"

# Parse arguments
while [[ $# -gt 0 ]]; do
	case $1 in
		--status=*)
			# shellcheck disable=SC2034  # Will be used in Day 2 implementation
			STATUS_FILTER="${1#*=}"
			shift
			;;
		--design-doc=*)
			# shellcheck disable=SC2034  # Will be used in Day 2 implementation
			DESIGN_DOC="${1#*=}"
			shift
			;;
		--owner=*)
			# shellcheck disable=SC2034  # Will be used in Day 2 implementation
			OWNER="${1#*=}"
			shift
			;;
		--format=*)
			FORMAT="${1#*=}"
			shift
			;;
		--show-phases)
			# shellcheck disable=SC2034  # Will be used in Day 4 implementation
			SHOW_PHASES=true
			shift
			;;
		--no-health)
			# shellcheck disable=SC2034  # Will be used in Day 3 implementation
			SHOW_HEALTH=false
			shift
			;;
		--orphans)
			# shellcheck disable=SC2034  # Will be used in Day 3 implementation
			ORPHANS_ONLY=true
			shift
			;;
		--stale)
			# shellcheck disable=SC2034  # Will be used in Day 3 implementation
			STALE_ONLY=true
			shift
			;;
		--blocked)
			# shellcheck disable=SC2034  # Will be used in Day 3 implementation
			BLOCKED_ONLY=true
			shift
			;;
		--age-threshold=*)
			AGE_THRESHOLD="${1#*=}"
			shift
			;;
		--help)
			cat <<-'EOF'
			Usage: explore-plans.sh [module] [options]

			Options:
			  --status=STATUS           Filter by status (comma-separated)
			  --design-doc=PATH         Filter by design doc path
			  --owner=USERNAME          Filter by owner
			  --format=FORMAT           Output format (summary|detailed|timeline|json)
			  --show-phases             Show phase details
			  --no-health               Hide health analysis
			  --orphans                 Show only orphaned plans
			  --stale                   Show only stale plans
			  --blocked                 Show only blocked plans
			  --age-threshold=DAYS      Staleness threshold in days (default: 30)
			  --help                    Show this help message

			Examples:
			  explore-plans.sh                              # Show all plans
			  explore-plans.sh effect-type-registry         # Filter by module
			  explore-plans.sh --status=in-progress         # Filter by status
			  explore-plans.sh --stale --age-threshold=60   # Find stale plans
			  explore-plans.sh --format=timeline            # Timeline view
			EOF
			exit 0
			;;
		-*)
			echo -e "${RED}ERROR: Unknown option: $1${NC}" >&2
			echo "Use --help for usage information" >&2
			exit 1
			;;
		*)
			if [[ -z "$MODULE" ]]; then
				MODULE="$1"
			else
				echo -e "${RED}ERROR: Unexpected argument: $1${NC}" >&2
				exit 1
			fi
			shift
			;;
	esac
done

# Validate format
if [[ ! "$FORMAT" =~ ^(summary|detailed|timeline|json)$ ]]; then
	echo -e "${RED}ERROR: Invalid format '$FORMAT'${NC}" >&2
	echo "Valid formats: summary, detailed, timeline, json" >&2
	exit 1
fi

# Validate age threshold
if ! [[ "$AGE_THRESHOLD" =~ ^[0-9]+$ ]]; then
	echo -e "${RED}ERROR: Age threshold must be a positive integer${NC}" >&2
	exit 1
fi

# Load configuration
CONFIG_FILE=".claude/design/design.config.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
	echo -e "${RED}ERROR: Configuration file not found: $CONFIG_FILE${NC}" >&2
	exit 1
fi

PLANS_DIR=$(jq -r '.paths.plans' "$CONFIG_FILE")
if [[ -z "$PLANS_DIR" ]] || [[ "$PLANS_DIR" == "null" ]]; then
	PLANS_DIR=".claude/plans"
fi

# Verify plans directory exists
if [[ ! -d "$PLANS_DIR" ]]; then
	echo -e "${YELLOW}No plans found in $PLANS_DIR${NC}"
	echo ""
	echo "Suggestion: Create a plan with /plan-create"
	exit 0
fi

# Discover plan files (exclude _archive)
mapfile -t PLAN_FILES < <(find "$PLANS_DIR" -maxdepth 1 -name "*.md" -type f \
	| sort -r)


if [[ ${#PLAN_FILES[@]} -eq 0 ]]; then
	echo -e "${YELLOW}No plans found in $PLANS_DIR${NC}"
	echo ""
	echo "Suggestion: Create a plan with /plan-create"
	exit 0
fi

# Declare and initialize arrays early to avoid unbound variable errors with set -u
declare -a FILTERED_PLANS=()
declare -A PLAN_METADATA=()
declare -a STALE_PLANS=()
declare -a ORPHAN_PLANS=()
declare -a BLOCKED_PLANS=()
declare -a OVERDUE_PLANS=()
declare -a MISALIGNED_PLANS=()
declare -a RECOMMENDATIONS=()
declare -A status_counts=()

# ============================================================================
# Helper Functions - Metadata Extraction
# ============================================================================

# Extract frontmatter from plan file
extract_frontmatter() {
	local file=$1
	sed -n '/^---$/,/^---$/p' "$file" | sed '1d;$d'
}

# Get a single field value from frontmatter
get_field() {
	local frontmatter=$1
	local field=$2
	echo "$frontmatter" | grep "^$field:" | head -1 | \
		cut -d':' -f2- | sed 's/^ *//' | tr -d '"'
}

# Get array field values from frontmatter
get_array_field() {
	local frontmatter=$1
	local field=$2
	# Use process substitution to avoid echo issues with special characters
	awk -v field="$field" '
		/^[a-z-]+:/ { if (in_array) exit; if ($0 ~ "^"field":") in_array=1; next }
		in_array && /^  - / { gsub(/^  - /, ""); gsub(/"/, ""); print }
	' <(echo "$frontmatter")
}

# ============================================================================
# Helper Functions - Filtering
# ============================================================================

# Check if plan matches module filter
matches_module() {
	local modules=$1
	local target_module=$2

	if [[ -z "$target_module" ]]; then
		return 0  # No filter, matches
	fi

	echo "$modules" | grep -q "^$target_module$"
}

# Check if plan matches status filter
matches_status() {
	local plan_status=$1
	local status_filter=$2

	if [[ -z "$status_filter" ]]; then
		return 0  # No filter, matches
	fi

	# Handle comma-separated status values
	IFS=',' read -ra statuses <<< "$status_filter"
	for status in "${statuses[@]}"; do
		if [[ "$plan_status" == "$status" ]]; then
			return 0
		fi
	done

	return 1  # No match
}

# Check if plan matches design doc filter
matches_design_doc() {
	local implements=$1
	local target_doc=$2

	if [[ -z "$target_doc" ]]; then
		return 0  # No filter, matches
	fi

	echo "$implements" | grep -q "$target_doc"
}

# Check if plan matches owner filter
matches_owner() {
	local plan_owner=$1
	local target_owner=$2

	if [[ -z "$target_owner" ]]; then
		return 0  # No filter, matches
	fi

	[[ "$plan_owner" == "$target_owner" ]]
}

# ============================================================================
# Main Processing
# ============================================================================


# Process each plan file
for plan_file in "${PLAN_FILES[@]}"; do
	# Extract metadata
	frontmatter=$(extract_frontmatter "$plan_file")

	# Parse key fields
	name=$(get_field "$frontmatter" "name")
	title=$(get_field "$frontmatter" "title")
	status=$(get_field "$frontmatter" "status")
	progress=$(get_field "$frontmatter" "progress")
	modules=$(get_array_field "$frontmatter" "modules")
	implements=$(get_array_field "$frontmatter" "implements")
	owner=$(get_field "$frontmatter" "owner")
	created=$(get_field "$frontmatter" "created")
	updated=$(get_field "$frontmatter" "updated")
	started=$(get_field "$frontmatter" "started")

	# Apply filters
	if ! matches_module "$modules" "$MODULE"; then
		continue
	fi

	if ! matches_status "$status" "$STATUS_FILTER"; then
		continue
	fi

	if ! matches_design_doc "$implements" "$DESIGN_DOC"; then
		continue
	fi

	if ! matches_owner "$owner" "$OWNER"; then
		continue
	fi

	# Special filters
	if [[ "$ORPHANS_ONLY" == true ]]; then
		if [[ -n "$implements" ]]; then
			continue
		fi
	fi

	if [[ "$STALE_ONLY" == true ]]; then
		if [[ -n "$updated" ]]; then
			updated_epoch=$(date -j -f "%Y-%m-%d" "$updated" +%s \
				2>/dev/null || echo 0)
			now_epoch=$(date +%s)
			days_old=$(( (now_epoch - updated_epoch) / 86400 ))

			if (( days_old <= AGE_THRESHOLD )); then
				continue
			fi
		fi
	fi

	if [[ "$BLOCKED_ONLY" == true ]]; then
		if [[ "$status" != "blocked" ]]; then
			continue
		fi
	fi

	# Plan passed filters - add to results
	FILTERED_PLANS+=("$plan_file")

	# Store metadata for later use
	PLAN_METADATA["$name:title"]="$title"
	PLAN_METADATA["$name:status"]="$status"
	PLAN_METADATA["$name:progress"]="$progress"
	PLAN_METADATA["$name:modules"]="$modules"
	PLAN_METADATA["$name:implements"]="$implements"
	PLAN_METADATA["$name:owner"]="$owner"
	PLAN_METADATA["$name:created"]="$created"
	PLAN_METADATA["$name:updated"]="$updated"
	PLAN_METADATA["$name:started"]="$started"
done

# ============================================================================
# Health Analysis
# ============================================================================

# Check staleness
check_staleness() {
	local name=$1
	local updated=$2

	if [[ -z "$updated" ]]; then
		return 1
	fi

	local updated_epoch
	updated_epoch=$(date -j -f "%Y-%m-%d" "$updated" +%s 2>/dev/null || echo 0)
	local now_epoch
	now_epoch=$(date +%s)
	local days_old=$(( (now_epoch - updated_epoch) / 86400 ))

	if (( days_old > AGE_THRESHOLD )); then
		STALE_PLANS+=("$name")
		return 0
	fi
	return 1
}

# Check if plan is orphaned
check_orphan() {
	local name=$1
	local implements=$2

	if [[ -z "$implements" ]]; then
		ORPHAN_PLANS+=("$name")
		return 0
	fi
	return 1
}

# Check schedule status
check_schedule() {
	local name=$1
	local frontmatter=$2

	local target
	target=$(get_field "$frontmatter" "target-completion")
	local progress="${PLAN_METADATA[$name:progress]}"

	if [[ -z "$target" ]]; then
		return 1
	fi

	local target_epoch
	target_epoch=$(date -j -f "%Y-%m-%d" "$target" +%s 2>/dev/null || echo 0)
	local now_epoch
	now_epoch=$(date +%s)

	if (( target_epoch < now_epoch )) && (( progress < 100 )); then
		OVERDUE_PLANS+=("$name")
		return 0
	fi
	return 1
}

# Check status-progress alignment
check_progress_alignment() {
	local name=$1
	local status=$2
	local progress=$3

	case "$status" in
		ready)
			if (( progress != 0 )); then
				MISALIGNED_PLANS+=("$name:ready but $progress%")
				return 0
			fi
			;;
		in-progress|blocked)
			if (( progress == 0 || progress == 100 )); then
				MISALIGNED_PLANS+=("$name:$status but $progress%")
				return 0
			fi
			;;
		completed)
			if (( progress != 100 )); then
				MISALIGNED_PLANS+=("$name:completed but $progress%")
				return 0
			fi
			;;
	esac
	return 1
}

# Perform health analysis on filtered plans
if [[ "$SHOW_HEALTH" == true ]]; then
	for plan_file in "${FILTERED_PLANS[@]}"; do
		name=$(basename "$plan_file" .md)
		frontmatter=$(extract_frontmatter "$plan_file")

		status="${PLAN_METADATA[$name:status]}"
		progress="${PLAN_METADATA[$name:progress]}"
		updated="${PLAN_METADATA[$name:updated]}"
		implements="${PLAN_METADATA[$name:implements]}"

		# Run health checks
		check_staleness "$name" "$updated" || true
		check_orphan "$name" "$implements" || true
		check_schedule "$name" "$frontmatter" || true
		check_progress_alignment "$name" "$status" "$progress" || true

		# Track blocked plans
		if [[ "$status" == "blocked" ]]; then
			BLOCKED_PLANS+=("$name")
		fi
	done

	# Generate recommendations
	if (( ${#OVERDUE_PLANS[@]} > 0 )); then
		for plan in "${OVERDUE_PLANS[@]}"; do
			RECOMMENDATIONS+=("Reschedule or accelerate overdue plan: $plan")
		done
	fi

	if (( ${#STALE_PLANS[@]} > 0 )); then
		stale_list=$(printf ", %s" "${STALE_PLANS[@]}")
		stale_list=${stale_list:2}
		RECOMMENDATIONS+=("Update stale plans: $stale_list")
	fi

	if (( ${#ORPHAN_PLANS[@]} > 0 )); then
		for plan in "${ORPHAN_PLANS[@]}"; do
			RECOMMENDATIONS+=("Link orphaned plan to design doc: $plan")
		done
	fi

	if (( ${#BLOCKED_PLANS[@]} > 0 )); then
		RECOMMENDATIONS+=("Review blocked plans for unblocking")
	fi

	if (( ${#MISALIGNED_PLANS[@]} > 0 )); then
		for issue in "${MISALIGNED_PLANS[@]}"; do
			RECOMMENDATIONS+=("Fix status-progress alignment: $issue")
		done
	fi
fi


# ============================================================================
# Output Results
# ============================================================================


# Check if any plans matched
if [[ ${#FILTERED_PLANS[@]} -eq 0 ]]; then
	echo -e "${YELLOW}No plans found matching filters${NC}"
	echo ""

	if [[ -n "$MODULE" ]] || [[ -n "$STATUS_FILTER" ]] || \
		[[ -n "$DESIGN_DOC" ]] || [[ -n "$OWNER" ]]; then
		echo "Applied filters:"
		[[ -n "$MODULE" ]] && echo "  Module: $MODULE"
		[[ -n "$STATUS_FILTER" ]] && echo "  Status: $STATUS_FILTER"
		[[ -n "$DESIGN_DOC" ]] && echo "  Design doc: $DESIGN_DOC"
		[[ -n "$OWNER" ]] && echo "  Owner: $OWNER"
		echo ""
		echo "Try:"
		echo "  - Remove some filters"
		echo "  - Use /plan-list to see all plans"
	fi
	exit 0
fi

# Output formatting functions

# Get status emoji
get_status_emoji() {
	local status=$1
	case "$status" in
		ready) echo "$EMOJI_READY" ;;
		in-progress) echo "$EMOJI_IN_PROGRESS" ;;
		blocked) echo "$EMOJI_BLOCKED" ;;
		completed) echo "$EMOJI_COMPLETED" ;;
		abandoned) echo "$EMOJI_ABANDONED" ;;
		*) echo "$EMOJI_PLAN" ;;
	esac
}

# Summary output format (default)
output_summary() {
	echo -e "${BLUE}Implementation Plans Overview${NC}"
	echo "============================"
	echo ""

	# Status summary
	for plan_file in "${FILTERED_PLANS[@]}"; do
		name=$(basename "$plan_file" .md)
		status="${PLAN_METADATA[$name:status]}"
		((status_counts[$status]++)) || status_counts[$status]=1
	done

	echo "Status Summary:"
	[[ -n "${status_counts[ready]:-}" ]] && \
		echo "  Ready: ${status_counts[ready]} plan(s)"
	[[ -n "${status_counts[in-progress]:-}" ]] && \
		echo "  In Progress: ${status_counts[in-progress]} plan(s)"
	[[ -n "${status_counts[blocked]:-}" ]] && \
		echo "  Blocked: ${status_counts[blocked]} plan(s)"
	[[ -n "${status_counts[completed]:-}" ]] && \
		echo "  Completed: ${status_counts[completed]} plan(s)"
	[[ -n "${status_counts[abandoned]:-}" ]] && \
		echo "  Abandoned: ${status_counts[abandoned]} plan(s)"
	echo ""

	# Active plans section (in-progress only)
	if [[ -n "${status_counts[in-progress]:-}" ]]; then
		echo "Active Plans (In Progress):"
		for plan_file in "${FILTERED_PLANS[@]}"; do
			name=$(basename "$plan_file" .md)
			status="${PLAN_METADATA[$name:status]}"

			if [[ "$status" == "in-progress" ]]; then
				title="${PLAN_METADATA[$name:title]}"
				progress="${PLAN_METADATA[$name:progress]}"
				modules="${PLAN_METADATA[$name:modules]}"
				implements="${PLAN_METADATA[$name:implements]}"
				updated="${PLAN_METADATA[$name:updated]}"

				# Calculate age
				if [[ -n "$updated" ]]; then
					updated_epoch=$(date -j -f "%Y-%m-%d" "$updated" +%s \
						2>/dev/null || echo 0)
					now_epoch=$(date +%s)
					days_old=$(( (now_epoch - updated_epoch) / 86400 ))
					age_str="$days_old day(s) old"
				else
					age_str="unknown age"
				fi

				echo "  • $title [$progress%] - $age_str"
				[[ -n "$modules" ]] && echo "    Modules: $modules"
				[[ -n "$implements" ]] && echo "    Design: $implements"
				echo ""
			fi
		done
	fi

	# Health insights
	if [[ "$SHOW_HEALTH" == true ]]; then
		echo "Health Insights:"

		if (( ${#STALE_PLANS[@]} > 0 )); then
			echo -e "  ${EMOJI_WARNING} ${#STALE_PLANS[@]} plan(s) stale \
(>$AGE_THRESHOLD days since update)"
		else
			echo -e "  ${EMOJI_CHECK} No stale plans"
		fi

		if (( ${#ORPHAN_PLANS[@]} > 0 )); then
			echo -e "  ${EMOJI_WARNING} ${#ORPHAN_PLANS[@]} orphaned plan(s) \
(no design docs)"
		else
			echo -e "  ${EMOJI_CHECK} No orphaned plans"
		fi

		if (( ${#BLOCKED_PLANS[@]} > 0 )); then
			echo -e "  ${EMOJI_WARNING} ${#BLOCKED_PLANS[@]} blocked plan(s)"
		else
			echo -e "  ${EMOJI_CHECK} No blocked plans"
		fi

		if (( ${#OVERDUE_PLANS[@]} > 0 )); then
			echo -e "  ${EMOJI_WARNING} ${#OVERDUE_PLANS[@]} overdue plan(s)"
		else
			: # No overdue plans
		fi

		if (( ${#MISALIGNED_PLANS[@]} > 0 )); then
			echo -e "  ${EMOJI_WARNING} ${#MISALIGNED_PLANS[@]} \
status-progress misalignment(s)"
		else
			: # No misalignment
		fi

		# Overall health
		total_issues=$(( ${#STALE_PLANS[@]} + ${#ORPHAN_PLANS[@]} + \
			${#BLOCKED_PLANS[@]} + ${#OVERDUE_PLANS[@]} + \
			${#MISALIGNED_PLANS[@]} ))

		if (( total_issues == 0 )); then
			echo -e "  ${EMOJI_CHECK} All plans healthy"
		else
			: # Has issues (already displayed above)
		fi

		echo ""
	fi

	# Recommendations
	if [[ "$SHOW_HEALTH" == true ]] && (( ${#RECOMMENDATIONS[@]} > 0 )); then
		echo "Next Actions:"
		for i in "${!RECOMMENDATIONS[@]}"; do
			echo "  $((i+1)). ${RECOMMENDATIONS[$i]}"
		done
		echo ""
	else
		: # No recommendations or health hidden
	fi
}

# Timeline output format (chronological view)
output_timeline() {
	echo -e "${BLUE}Implementation Plans - Timeline View${NC}"
	echo "======================================"
	echo ""

	# Group plans by creation date
	declare -A plans_by_date
	for plan_file in "${FILTERED_PLANS[@]}"; do
		name=$(basename "$plan_file" .md)
		created="${PLAN_METADATA[$name:created]}"
		if [[ -z "${plans_by_date[$created]:-}" ]]; then
			plans_by_date[$created]="$name"
		else
			plans_by_date[$created]="${plans_by_date[$created]},$name"
		fi
	done

	# Output in chronological order (newest first)
	for date in $(printf '%s\n' "${!plans_by_date[@]}" | sort -r); do
		echo "[$date]"
		IFS=',' read -ra names <<< "${plans_by_date[$date]}"
		for name in "${names[@]}"; do
			emoji=$(get_status_emoji "${PLAN_METADATA[$name:status]}")
			echo -e "  ${emoji} ${PLAN_METADATA[$name:title]}"
			echo "     Status: ${PLAN_METADATA[$name:status]} (${PLAN_METADATA[$name:progress]}%)"
			[[ -n "${PLAN_METADATA[$name:modules]}" ]] && \
				echo "     Module: ${PLAN_METADATA[$name:modules]}"
		done
		echo ""
	done
}

# JSON output format (machine-readable)
output_json() {
	echo "{"
	echo "  \"plans\": ["

	local first=true
	for plan_file in "${FILTERED_PLANS[@]}"; do
		name=$(basename "$plan_file" .md)

		[[ "$first" == false ]] && echo "    ,"
		first=false

		echo "    {"
		echo "      \"name\": \"$name\","
		echo "      \"title\": \"${PLAN_METADATA[$name:title]}\","
		echo "      \"status\": \"${PLAN_METADATA[$name:status]}\","
		echo "      \"progress\": ${PLAN_METADATA[$name:progress]},"
		echo "      \"created\": \"${PLAN_METADATA[$name:created]}\","
		echo "      \"updated\": \"${PLAN_METADATA[$name:updated]}\","

		if [[ -n "${PLAN_METADATA[$name:started]}" ]] && [[ "${PLAN_METADATA[$name:started]}" != "null" ]]; then
			echo "      \"started\": \"${PLAN_METADATA[$name:started]}\","
		else
			echo "      \"started\": null,"
		fi

		if [[ -n "${PLAN_METADATA[$name:modules]}" ]]; then
			# Convert newline-separated modules to JSON array
			echo "      \"modules\": ["
			local module_first=true
			while IFS= read -r module; do
				[[ "$module_first" == false ]] && echo ","
				module_first=false
				echo -n "        \"$module\""
			done <<< "${PLAN_METADATA[$name:modules]}"
			echo ""
			echo "      ],"
		else
			echo "      \"modules\": [],"
		fi

		if [[ -n "${PLAN_METADATA[$name:implements]}" ]]; then
			# Convert newline-separated implements to JSON array
			echo "      \"implements\": ["
			local impl_first=true
			while IFS= read -r impl; do
				[[ "$impl_first" == false ]] && echo ","
				impl_first=false
				echo -n "        \"$impl\""
			done <<< "${PLAN_METADATA[$name:implements]}"
			echo ""
			echo "      ]"
		else
			echo "      \"implements\": []"
		fi

		echo -n "    }"
	done

	echo ""
	echo "  ],"

	# Add health summary
	echo "  \"health\": {"
	echo "    \"total_plans\": ${#FILTERED_PLANS[@]},"
	echo "    \"stale_plans\": ${#STALE_PLANS[@]},"
	echo "    \"orphan_plans\": ${#ORPHAN_PLANS[@]},"
	echo "    \"blocked_plans\": ${#BLOCKED_PLANS[@]},"
	echo "    \"overdue_plans\": ${#OVERDUE_PLANS[@]},"
	echo "    \"misaligned_plans\": ${#MISALIGNED_PLANS[@]}"
	echo "  }"
	echo "}"
}

# Detailed output format (full metadata)
output_detailed() {
	echo -e "${BLUE}Implementation Plans - Detailed View${NC}"
	echo "========================================"
	echo ""

	for plan_file in "${FILTERED_PLANS[@]}"; do
		name=$(basename "$plan_file" .md)
		emoji=$(get_status_emoji "${PLAN_METADATA[$name:status]}")

		echo -e "${emoji} ${PLAN_METADATA[$name:title]}"
		echo "---"
		echo "  Name: $name"
		echo "  Status: ${PLAN_METADATA[$name:status]} (${PLAN_METADATA[$name:progress]}%)"
		echo "  Created: ${PLAN_METADATA[$name:created]}"
		echo "  Updated: ${PLAN_METADATA[$name:updated]}"

		[[ -n "${PLAN_METADATA[$name:started]}" ]] && [[ "${PLAN_METADATA[$name:started]}" != "null" ]] && \
			echo "  Started: ${PLAN_METADATA[$name:started]}"

		[[ -n "${PLAN_METADATA[$name:modules]}" ]] && \
			echo "  Modules: ${PLAN_METADATA[$name:modules]}"

		[[ -n "${PLAN_METADATA[$name:implements]}" ]] && \
			echo "  Implements: ${PLAN_METADATA[$name:implements]}"

		[[ -n "${PLAN_METADATA[$name:owner]}" ]] && [[ "${PLAN_METADATA[$name:owner]}" != "null" ]] && \
			echo "  Owner: ${PLAN_METADATA[$name:owner]}"

		echo ""
	done
}

# Call the appropriate output format function
case "$FORMAT" in
	summary)
		output_summary
		;;
	detailed)
		output_detailed
		;;
	timeline)
		output_timeline
		;;
	json)
		output_json
		;;
	*)
		echo -e "${RED}Error: Unknown format '$FORMAT'${NC}"
		echo "Valid formats: summary, detailed, timeline, json"
		exit 1
		;;
esac

# Exit successfully
exit 0
