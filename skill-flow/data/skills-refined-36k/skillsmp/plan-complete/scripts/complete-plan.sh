#!/usr/bin/env bash
set -euo pipefail

# Complete a plan by updating design docs and removing the plan file
# Usage: complete-plan.sh <plan-name> [--outcome=success|partial|failed] [--dry-run] [--keep]

PLAN_NAME=""
OUTCOME="success"
DRY_RUN=false
KEEP_PLAN=false
TODAY=$(date +%Y-%m-%d)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
while [[ $# -gt 0 ]]; do
	case $1 in
		--outcome=*)
			OUTCOME="${1#*=}"
			shift
			;;
		--dry-run)
			DRY_RUN=true
			shift
			;;
		--keep)
			KEEP_PLAN=true
			shift
			;;
		*)
			if [[ -z "$PLAN_NAME" ]]; then
				PLAN_NAME="$1"
			else
				echo -e "${RED}ERROR: Unknown argument: $1${NC}" >&2
				exit 1
			fi
			shift
			;;
	esac
done

# Validate arguments
if [[ -z "$PLAN_NAME" ]]; then
	echo -e "${RED}ERROR: Plan name is required${NC}" >&2
	echo "Usage: complete-plan.sh <plan-name> [--outcome=success|partial|failed] [--dry-run] [--keep]" >&2
	exit 1
fi

# Validate outcome
if [[ ! "$OUTCOME" =~ ^(success|partial|failed)$ ]]; then
	echo -e "${RED}ERROR: Invalid outcome '$OUTCOME'${NC}" >&2
	echo "Valid values: success, partial, failed" >&2
	exit 1
fi

# Find plan file
PLAN_FILE=".claude/plans/${PLAN_NAME}.md"
if [[ ! -f "$PLAN_FILE" ]]; then
	echo -e "${RED}ERROR: Plan file not found: $PLAN_FILE${NC}" >&2
	exit 1
fi

echo -e "${BLUE}Completing plan: $PLAN_NAME${NC}"
echo ""

# Extract plan metadata
STATUS=$(grep "^status:" "$PLAN_FILE" | head -1 | awk '{print $2}')
PROGRESS=$(grep "^progress:" "$PLAN_FILE" | head -1 | awk '{print $2}')
TITLE=$(grep "^title:" "$PLAN_FILE" | head -1 | cut -d' ' -f2- | tr -d '"')

# Extract implements array
IMPLEMENTS=$(sed -n '/^implements:/,/^[a-z-]*:/p' "$PLAN_FILE" | grep "^  -" | sed 's/^  - //')

echo "Plan metadata:"
echo "  Title: $TITLE"
echo "  Status: $STATUS"
echo "  Progress: $PROGRESS%"
echo ""

# Validate completion requirements
ERRORS=0

if [[ "$STATUS" != "completed" ]]; then
	echo -e "${YELLOW}⚠  Status is '$STATUS' (expected 'completed')${NC}"
	ERRORS=$((ERRORS + 1))
fi

if [[ "$PROGRESS" != "100" ]]; then
	echo -e "${YELLOW}⚠  Progress is $PROGRESS% (expected 100%)${NC}"
	ERRORS=$((ERRORS + 1))
fi

if [[ -z "$IMPLEMENTS" ]]; then
	echo -e "${YELLOW}⚠  No design docs linked (implements field empty)${NC}"
	ERRORS=$((ERRORS + 1))
fi

if [[ $ERRORS -gt 0 ]]; then
	echo ""
	echo -e "${RED}✗ Plan does not meet completion requirements${NC}"
	echo "Fix these issues before completing the plan"
	exit 1
fi

echo -e "${GREEN}✓ Plan meets completion requirements${NC}"
echo ""

# Process each linked design doc
echo "Updating linked design docs:"
while IFS= read -r doc_path; do
	# Convert relative path to absolute
	DESIGN_DOC=".claude/design/${doc_path}"

	if [[ ! -f "$DESIGN_DOC" ]]; then
		echo -e "${RED}  ✗ Design doc not found: $doc_path${NC}"
		continue
	fi

	echo -e "${BLUE}  Processing: $doc_path${NC}"

	# Extract current status
	DOC_STATUS=$(grep "^status:" "$DESIGN_DOC" | head -1 | awk '{print $2}')
	echo "    Current status: $DOC_STATUS"

	if [[ "$DRY_RUN" == true ]]; then
		echo "    [DRY RUN] Would update:"
		echo "      - status: current"
		echo "      - last-synced: $TODAY"
		echo "      - Add completion metadata"
	else
		# Update status to current
		if [[ "$DOC_STATUS" != "current" ]]; then
			sed -i.bak "s/^status: .*/status: current/" "$DESIGN_DOC"
			echo -e "${GREEN}    ✓ Updated status to current${NC}"
		else
			echo -e "${GREEN}    ✓ Status already current${NC}"
		fi

		# Update last-synced
		sed -i.bak "s/^last-synced: .*/last-synced: $TODAY/" "$DESIGN_DOC"
		echo -e "${GREEN}    ✓ Updated last-synced to $TODAY${NC}"

		# Add completion metadata if not present
		if ! grep -q "completed-plans:" "$DESIGN_DOC"; then
			# Insert before end of frontmatter
			awk -v plan="$PLAN_NAME" -v date="$TODAY" -v outcome="$OUTCOME" '
				/^---$/ && NR > 1 {
					print "completed-plans:"
					print "  - name: \"" plan "\""
					print "    completed: \"" date "\""
					print "    outcome: \"" outcome "\""
				}
				{ print }
			' "$DESIGN_DOC" > "$DESIGN_DOC.tmp"
			mv "$DESIGN_DOC.tmp" "$DESIGN_DOC"
			echo -e "${GREEN}    ✓ Added completion metadata${NC}"
		else
			# Append to existing completed-plans array
			awk -v plan="$PLAN_NAME" -v date="$TODAY" -v outcome="$OUTCOME" '
				/^completed-plans:/ {
					print
					getline
					print
					print "  - name: \"" plan "\""
					print "    completed: \"" date "\""
					print "    outcome: \"" outcome "\""
					next
				}
				{ print }
			' "$DESIGN_DOC" > "$DESIGN_DOC.tmp"
			mv "$DESIGN_DOC.tmp" "$DESIGN_DOC"
			echo -e "${GREEN}    ✓ Appended completion metadata${NC}"
		fi

		# Remove backup
		rm -f "$DESIGN_DOC.bak"
	fi
	echo ""
done <<< "$IMPLEMENTS"

# Delete or keep plan file
if [[ "$KEEP_PLAN" == true ]]; then
	echo -e "${BLUE}Plan file kept (--keep specified): $PLAN_FILE${NC}"
elif [[ "$DRY_RUN" == true ]]; then
	echo -e "${YELLOW}[DRY RUN] Would delete plan file: $PLAN_FILE${NC}"
else
	rm "$PLAN_FILE"
	echo -e "${GREEN}✓ Deleted plan file: $PLAN_FILE${NC}"
fi

echo ""
echo -e "${GREEN}✓ Plan completion successful!${NC}"
echo ""
echo "Summary:"
echo "  Plan: $PLAN_NAME"
echo "  Outcome: $OUTCOME"
echo "  Design docs updated: $(echo "$IMPLEMENTS" | wc -l | tr -d ' ')"
if [[ "$KEEP_PLAN" == true ]]; then
	echo "  Plan file: Kept"
else
	echo "  Plan file: Deleted"
fi
