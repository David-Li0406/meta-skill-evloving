#!/bin/bash

# Design Documentation Validation Script
# Validates frontmatter, structure, and cross-references
#
# Usage:
#   ./validate.sh [module|all]
#
# Examples:
#   ./validate.sh all
#   ./validate.sh effect-type-registry

ERRORS=0
WARNINGS=0
FILES_CHECKED=0

# Valid status values
VALID_STATUSES=("stub" "draft" "current" "needs-review" "archived")

echo "# Design Documentation Validation Report"
echo ""
echo "**Date:** $(date +%Y-%m-%d)"
echo "**Modules:** ${1:-all}"
echo ""

# Function to validate a single file
validate_file() {
	local file="$1"
	local module="$2"
	local allowed_categories="$3"

	FILES_CHECKED=$((FILES_CHECKED + 1))
	local file_errors=0
	local file_warnings=0

	# Extract frontmatter (between first two --- markers)
	local fm_start
	local fm_end
	fm_start=$(grep -n "^---$" "$file" | head -1 | cut -d: -f1)
	fm_end=$(grep -n "^---$" "$file" | head -2 | tail -1 | cut -d: -f1)

	if [ -z "$fm_start" ] || [ -z "$fm_end" ] || [ "$fm_start" -ge "$fm_end" ]; then
		echo "  - ❌ ERROR: Missing or invalid frontmatter structure"
		ERRORS=$((ERRORS + 1))
		file_errors=$((file_errors + 1))
		return
	fi

	local fm
	fm=$(sed -n "${fm_start},${fm_end}p" "$file")

	# Check required fields
	local required_fields=("status" "module" "category" "created" "updated" "last-synced" "completeness" "related" "dependencies")
	for field in "${required_fields[@]}"; do
		if ! echo "$fm" | grep -q "^${field}:"; then
			echo "  - ❌ ERROR: Missing required field '${field}'"
			ERRORS=$((ERRORS + 1))
			file_errors=$((file_errors + 1))
		fi
	done

	# Extract field values
	# shellcheck disable=SC2155
	local status=$(echo "$fm" | grep "^status:" | sed 's/status: *//' | tr -d '\r')
	# shellcheck disable=SC2155
	local module_val=$(echo "$fm" | grep "^module:" | sed 's/module: *//' | tr -d '\r')
	# shellcheck disable=SC2155
	local category=$(echo "$fm" | grep "^category:" | sed 's/category: *//' | tr -d '\r')
	# shellcheck disable=SC2155
	local created=$(echo "$fm" | grep "^created:" | sed 's/created: *//' | tr -d '\r')
	# shellcheck disable=SC2155
	local updated=$(echo "$fm" | grep "^updated:" | sed 's/updated: *//' | tr -d '\r')
	# shellcheck disable=SC2155
	local last_synced=$(echo "$fm" | grep "^last-synced:" | sed 's/last-synced: *//' | tr -d '\r')
	# shellcheck disable=SC2155
	local completeness=$(echo "$fm" | grep "^completeness:" | sed 's/completeness: *//' | tr -d '\r')

	# Validate status
	if [ -n "$status" ]; then
		local valid=0
		for valid_status in "${VALID_STATUSES[@]}"; do
			if [ "$status" = "$valid_status" ]; then
				valid=1
				break
			fi
		done
		if [ $valid -eq 0 ]; then
			echo "  - ❌ ERROR: Invalid status '${status}' (expected: stub, draft, current, needs-review, or archived)"
			ERRORS=$((ERRORS + 1))
			file_errors=$((file_errors + 1))
		fi
	fi

	# Validate module matches
	if [ -n "$module_val" ] && [ "$module_val" != "$module" ]; then
		echo "  - ⚠️  WARNING: Module field '${module_val}' doesn't match directory '${module}'"
		WARNINGS=$((WARNINGS + 1))
		file_warnings=$((file_warnings + 1))
	fi

	# Validate category is allowed
	if [ -n "$category" ] && [ -n "$allowed_categories" ]; then
		if ! echo "$allowed_categories" | grep -q "\"$category\""; then
			echo "  - ❌ ERROR: Category '${category}' not in allowed list: ${allowed_categories}"
			ERRORS=$((ERRORS + 1))
			file_errors=$((file_errors + 1))
		fi
	fi

	# Validate date formats (YYYY-MM-DD)
	local date_regex='^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
	if [ -n "$created" ] && ! [[ "$created" =~ $date_regex ]]; then
		echo "  - ❌ ERROR: Invalid date format for 'created': ${created} (expected YYYY-MM-DD)"
		ERRORS=$((ERRORS + 1))
		file_errors=$((file_errors + 1))
	fi
	if [ -n "$updated" ] && ! [[ "$updated" =~ $date_regex ]]; then
		echo "  - ❌ ERROR: Invalid date format for 'updated': ${updated} (expected YYYY-MM-DD)"
		ERRORS=$((ERRORS + 1))
		file_errors=$((file_errors + 1))
	fi
	if [ -n "$last_synced" ] && [ "$last_synced" != "never" ] && ! [[ "$last_synced" =~ $date_regex ]]; then
		echo "  - ❌ ERROR: Invalid date format for 'last-synced': ${last_synced} (expected YYYY-MM-DD or 'never')"
		ERRORS=$((ERRORS + 1))
		file_errors=$((file_errors + 1))
	fi

	# Validate completeness is 0-100
	if [ -n "$completeness" ]; then
		if ! [[ "$completeness" =~ ^[0-9]+$ ]] || [ "$completeness" -lt 0 ] || [ "$completeness" -gt 100 ]; then
			echo "  - ❌ ERROR: Invalid completeness: ${completeness} (expected 0-100)"
			ERRORS=$((ERRORS + 1))
			file_errors=$((file_errors + 1))
		fi
	fi

	# Validate status-completeness match
	if [ -n "$status" ] && [ -n "$completeness" ]; then
		case "$status" in
			"stub")
				if [ "$completeness" -gt 20 ]; then
					echo "  - ⚠️  WARNING: Status 'stub' but completeness ${completeness} > 20"
					WARNINGS=$((WARNINGS + 1))
					file_warnings=$((file_warnings + 1))
				fi
				;;
			"draft")
				if [ "$completeness" -le 20 ] || [ "$completeness" -gt 60 ]; then
					echo "  - ⚠️  WARNING: Status 'draft' but completeness ${completeness} outside 21-60 range"
					WARNINGS=$((WARNINGS + 1))
					file_warnings=$((file_warnings + 1))
				fi
				;;
			"current"|"needs-review")
				if [ "$completeness" -lt 61 ]; then
					echo "  - ⚠️  WARNING: Status '${status}' but completeness ${completeness} < 61"
					WARNINGS=$((WARNINGS + 1))
					file_warnings=$((file_warnings + 1))
				fi
				;;
		esac
	fi

	# Check for required sections
	local required_sections=("Overview" "Current State" "Rationale")
	for section in "${required_sections[@]}"; do
		if ! grep -q "^## ${section}" "$file"; then
			echo "  - ⚠️  WARNING: Missing recommended section '${section}'"
			WARNINGS=$((WARNINGS + 1))
			file_warnings=$((file_warnings + 1))
		fi
	done

	if [ $file_errors -eq 0 ] && [ $file_warnings -eq 0 ]; then
		echo "  ✅ PASS"
	elif [ $file_errors -eq 0 ]; then
		echo "  ⚠️  PASS with warnings"
	fi
}

# Validate modules based on argument
MODULE_ARG="${1:-all}"

if [ "$MODULE_ARG" = "all" ] || [ "$MODULE_ARG" = "effect-type-registry" ]; then
	echo "## effect-type-registry"
	echo ""
	CATEGORIES='["architecture", "observability", "performance"]'
	for file in .claude/design/effect-type-registry/*.md; do
		[ -f "$file" ] || continue
		echo "- **$(basename "$file")**"
		validate_file "$file" "effect-type-registry" "$CATEGORIES"
	done
	echo ""
fi

if [ "$MODULE_ARG" = "all" ] || [ "$MODULE_ARG" = "rspress-plugin-api-extractor" ]; then
	echo "## rspress-plugin-api-extractor"
	echo ""
	CATEGORIES='["architecture", "performance", "observability", "cross-linking", "import-generation", "source-mapping"]'
	for file in .claude/design/rspress-plugin-api-extractor/*.md; do
		[ -f "$file" ] || continue
		echo "- **$(basename "$file")**"
		validate_file "$file" "rspress-plugin-api-extractor" "$CATEGORIES"
	done
	echo ""
fi

if [ "$MODULE_ARG" = "all" ] || [ "$MODULE_ARG" = "design-doc-system" ]; then
	echo "## design-doc-system"
	echo ""
	CATEGORIES='["meta", "documentation", "architecture"]'
	for file in .claude/design/design-doc-system/*.md; do
		[ -f "$file" ] || continue
		echo "- **$(basename "$file")**"
		validate_file "$file" "design-doc-system" "$CATEGORIES"
	done
	echo ""
fi

# Summary
echo "---"
echo ""
echo "## Summary"
echo ""
echo "**Files validated:** ${FILES_CHECKED}"
echo "**Errors:** ${ERRORS}"
echo "**Warnings:** ${WARNINGS}"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
	echo "✅ **PASS** - All files valid!"
	exit 0
elif [ $ERRORS -eq 0 ]; then
	echo "⚠️  **PASS WITH WARNINGS** - No errors but ${WARNINGS} warning(s)"
	exit 0
else
	echo "❌ **FAIL** - ${ERRORS} error(s) found"
	exit 1
fi
