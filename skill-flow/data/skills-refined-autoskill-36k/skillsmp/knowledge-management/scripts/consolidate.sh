#!/bin/bash
# Session Consolidation Script for Knowledge Management
# Merges related auto-captured session files into daily summaries
#
# Usage: ./consolidate.sh [options]
# Options:
#   --date YYYY-MM-DD    Target date (default: today)
#   --dry-run            Preview changes without writing (default)
#   --execute            Actually perform consolidation
#   --time-window N      Time proximity window in minutes (default: 30)
#   --overlap N          File overlap percentage threshold (default: 50)
#   -h, --help           Show help

set -euo pipefail

# Configuration
TZ='Asia/Bangkok'
export TZ
PROJECT_ROOT="${PROJECT_ROOT:-.}"
DRY_RUN=true
TARGET_DATE=""
TIME_WINDOW=30
OVERLAP_THRESHOLD=50

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Temp directory for intermediate data
TEMP_DIR=""
cleanup_temp() {
    # Safely remove temp directory only if it's under /tmp or /var/folders (macOS)
    if [[ -n "$TEMP_DIR" ]] && [[ -d "$TEMP_DIR" ]]; then
        if [[ "$TEMP_DIR" == /tmp/* ]] || [[ "$TEMP_DIR" == /var/folders/* ]]; then
            rm -r "$TEMP_DIR" 2>/dev/null || true
        fi
    fi
}
trap cleanup_temp EXIT

# Help message
show_help() {
    cat << EOF
Session Consolidation Script

Usage: ./consolidate.sh [options]

Options:
  --date YYYY-MM-DD    Target date (default: today)
  --dry-run            Preview changes without writing (default)
  --execute            Actually perform consolidation
  --time-window N      Time proximity window in minutes (default: 30)
  --overlap N          File overlap percentage threshold (default: 50)
  -h, --help           Show this help message

Examples:
  ./consolidate.sh --dry-run                    # Preview today's consolidation
  ./consolidate.sh --date 2026-01-13 --execute  # Consolidate specific date
  ./consolidate.sh --time-window 60             # Use 60-minute proximity window

Configuration:
  Set PROJECT_ROOT environment variable to specify project location
  Current: $PROJECT_ROOT

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --date)
            if [[ -z "${2:-}" ]]; then
                echo -e "${RED}Error: --date requires YYYY-MM-DD argument${NC}"
                exit 1
            fi
            if ! [[ "$2" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
                echo -e "${RED}Error: Invalid date format. Use YYYY-MM-DD${NC}"
                exit 1
            fi
            TARGET_DATE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --execute)
            DRY_RUN=false
            shift
            ;;
        --time-window)
            if [[ -z "${2:-}" ]] || ! [[ "$2" =~ ^[0-9]+$ ]]; then
                echo -e "${RED}Error: --time-window requires positive integer${NC}"
                exit 1
            fi
            TIME_WINDOW="$2"
            shift 2
            ;;
        --overlap)
            if [[ -z "${2:-}" ]] || ! [[ "$2" =~ ^[0-9]+$ ]]; then
                echo -e "${RED}Error: --overlap requires positive integer (0-100)${NC}"
                exit 1
            fi
            if [[ "$2" -gt 100 ]]; then
                echo -e "${RED}Error: --overlap must be 0-100${NC}"
                exit 1
            fi
            OVERLAP_THRESHOLD="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Default to today if no date specified
if [[ -z "$TARGET_DATE" ]]; then
    TARGET_DATE=$(date '+%Y-%m-%d')
fi

# Parse date components
YEAR_MONTH="${TARGET_DATE:0:7}"
DAY="${TARGET_DATE:8:2}"

# Target directory
TARGET_DIR="$PROJECT_ROOT/docs/auto-captured/$YEAR_MONTH/$DAY"
OUTPUT_FILE="$TARGET_DIR/daily-summary.md"

echo -e "${BLUE}=== Session Consolidation ===${NC}"
echo -e "Date: ${CYAN}$TARGET_DATE${NC}"
echo -e "Directory: ${CYAN}$TARGET_DIR${NC}"
echo -e "Mode: $([ "$DRY_RUN" = true ] && echo -e "${YELLOW}DRY-RUN${NC}" || echo -e "${GREEN}EXECUTE${NC}")"
echo ""

# Check if directory exists
if [[ ! -d "$TARGET_DIR" ]]; then
    echo -e "${YELLOW}No sessions found for $TARGET_DATE${NC}"
    echo -e "Directory does not exist: $TARGET_DIR"
    exit 0
fi

# Create temp directory for intermediate data
TEMP_DIR=$(mktemp -d)

# Find session files (exclude daily-summary.md)
SESSION_FILES=()
while IFS= read -r file; do
    [[ -n "$file" ]] && SESSION_FILES+=("$file")
done < <(find "$TARGET_DIR" -maxdepth 1 -name "*.md" ! -name "daily-summary.md" -type f 2>/dev/null | sort)

if [[ ${#SESSION_FILES[@]} -eq 0 ]]; then
    echo -e "${YELLOW}No session files found for $TARGET_DATE${NC}"
    exit 0
fi

echo -e "${GREEN}Found ${#SESSION_FILES[@]} session files${NC}"
echo ""

# Arrays for session data (simple arrays, indexed by position)
SESSION_IDS=()
SESSION_PATHS=()
SESSION_TIMES_MIN=()
SESSION_ISSUES_LIST=()
SESSION_FILES_LIST=()

# Extract YAML frontmatter value
extract_yaml_value() {
    local file="$1"
    local key="$2"
    sed -n '/^---$/,/^---$/p' "$file" | grep "^${key}:" | head -1 | sed "s/^${key}:[[:space:]]*//"
}

# Extract issue numbers from content
extract_issues() {
    local file="$1"
    # Use || true to prevent exit on no matches (grep returns 1 when no match)
    grep -oE '#[0-9]+|[A-Z]+-[0-9]+' "$file" 2>/dev/null | sort -u | tr '\n' ' ' | xargs || true
}

# Extract files changed section
extract_files_changed() {
    local file="$1"
    local in_section=false
    local files=""
    while IFS= read -r line; do
        if [[ "$line" =~ ^##.*[Ff]iles.*[Cc]hanged ]] || [[ "$line" =~ ^files_changed: ]]; then
            in_section=true
            continue
        fi
        if [[ "$in_section" = true ]]; then
            if [[ "$line" =~ ^## ]] || [[ "$line" =~ ^--- ]]; then
                break
            fi
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]* ]] || [[ "$line" =~ \.[a-z]+$ ]]; then
                local cleaned
                cleaned=$(echo "$line" | sed 's/^[[:space:]]*-[[:space:]]*//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
                if [[ -n "$cleaned" ]] && [[ "$cleaned" != '```' ]]; then
                    files="$files$cleaned "
                fi
            fi
        fi
    done < "$file"
    echo "$files" | xargs
}

# Convert HH.MM (or HH) to minutes since midnight
time_to_minutes() {
    local time="$1"
    local hours
    local minutes

    # Handle empty or unset time defensively
    if [[ -z "${time:-}" ]]; then
        echo 0
        return 0
    fi

    # If time contains a dot, split into hours and minutes, otherwise assume whole string is hours
    if [[ "$time" == *.* ]]; then
        hours="${time%%.*}"
        minutes="${time#*.}"
    else
        hours="$time"
        minutes="0"
    fi

    # Validate that hours and minutes are non-empty and numeric
    if [[ -z "$hours" || -z "$minutes" || ! "$hours" =~ ^[0-9]+$ || ! "$minutes" =~ ^[0-9]+$ ]]; then
        # Fallback to 0 minutes on malformed time to avoid arithmetic errors
        echo 0
        return 0
    fi

    hours=$((10#$hours))
    minutes=$((10#$minutes))
    echo $((hours * 60 + minutes))
}

# Parse all session files
echo -e "${BLUE}Parsing session files...${NC}"
for session_file in "${SESSION_FILES[@]}"; do
    filename=$(basename "$session_file")

    # Validate filename format: expect HH.MM_* (e.g., 09.30_topic.md)
    time_part="${filename%%_*}"
    if [[ "$filename" != *_* ]] || ! [[ "$time_part" =~ ^([01][0-9]|2[0-3])\.[0-5][0-9]$ ]]; then
        echo -e "${YELLOW}Skipping file with unexpected name format (expected HH.MM_*):${NC} $filename" >&2
        continue
    fi

    session_id="${filename%.md}"
    SESSION_IDS+=("$session_id")
    SESSION_PATHS+=("$session_file")

    # Extract time from filename (already validated above)
    SESSION_TIMES_MIN+=("$(time_to_minutes "$time_part")")

    # Extract issues and files
    issues=$(extract_issues "$session_file")
    files=$(extract_files_changed "$session_file")
    SESSION_ISSUES_LIST+=("$issues")
    SESSION_FILES_LIST+=("$files")

    echo -e "  ${CYAN}$session_id${NC}"
    echo -e "    Time: $time_part"
    [[ -n "$issues" ]] && echo -e "    Issues: $issues"
done
echo ""

# Grouping arrays
GROUP_IDS=()
GROUP_TYPES=()
GROUP_SESSIONS=()  # space-separated session indices
ASSIGNED=()        # -1 means not assigned, otherwise index into GROUP_IDS

# Initialize assigned array
for ((i=0; i<${#SESSION_IDS[@]}; i++)); do
    ASSIGNED+=(-1)
done

group_counter=0

# Calculate file overlap percentage
calc_overlap() {
    local files1="$1"
    local files2="$2"

    if [[ -z "$files1" ]] || [[ -z "$files2" ]]; then
        echo 0
        return
    fi

    # Convert to arrays safely (avoid glob expansion)
    local -a arr1
    local -a arr2
    read -ra arr1 <<< "$files1"
    read -ra arr2 <<< "$files2"
    local common=0

    for f1 in "${arr1[@]}"; do
        for f2 in "${arr2[@]}"; do
            if [[ "$f1" == "$f2" ]]; then
                ((common++))
                break
            fi
        done
    done

    local total1=${#arr1[@]}
    local total2=${#arr2[@]}
    local min_total=$((total1 < total2 ? total1 : total2))

    if [[ $min_total -eq 0 ]]; then
        echo 0
    else
        echo $((common * 100 / min_total))
    fi
}

echo -e "${BLUE}Grouping sessions...${NC}"

# Priority 1: Group by same issue
echo -e "  ${CYAN}Phase 1: Grouping by issue...${NC}"

# Collect all unique issues and their sessions
all_issues=""
for ((i=0; i<${#SESSION_IDS[@]}; i++)); do
    issues="${SESSION_ISSUES_LIST[$i]}"
    for issue in $issues; do
        all_issues="$all_issues$issue "
    done
done
unique_issues=$(echo "$all_issues" | tr ' ' '\n' | sort -u | xargs)

for issue in $unique_issues; do
    [[ -z "$issue" ]] && continue

    # Find all sessions with this issue
    matching_indices=""
    for ((i=0; i<${#SESSION_IDS[@]}; i++)); do
        if [[ " ${SESSION_ISSUES_LIST[$i]} " =~ " $issue " ]]; then
            matching_indices="$matching_indices$i "
        fi
    done

    # Count unassigned sessions
    unassigned_count=0
    unassigned_indices=""
    for idx in $matching_indices; do
        if [[ ${ASSIGNED[$idx]} -eq -1 ]]; then
            ((unassigned_count++))
            unassigned_indices="$unassigned_indices$idx "
        fi
    done

    # Only group if multiple unassigned sessions share the issue
    if [[ $unassigned_count -gt 1 ]]; then
        GROUP_IDS+=("issue_$issue")
        GROUP_TYPES+=("issue")
        GROUP_SESSIONS+=("$unassigned_indices")

        for idx in $unassigned_indices; do
            ASSIGNED[$idx]=$group_counter
        done

        echo -e "    Group: $issue -> $unassigned_count sessions"
        ((group_counter++))
    fi
done

# Priority 2: Group by file overlap
echo -e "  ${CYAN}Phase 2: Grouping by file overlap (>${OVERLAP_THRESHOLD}%)...${NC}"
for ((i=0; i<${#SESSION_IDS[@]}; i++)); do
    [[ ${ASSIGNED[$i]} -ne -1 ]] && continue

    similar_indices="$i"
    for ((j=i+1; j<${#SESSION_IDS[@]}; j++)); do
        [[ ${ASSIGNED[$j]} -ne -1 ]] && continue

        overlap=$(calc_overlap "${SESSION_FILES_LIST[$i]}" "${SESSION_FILES_LIST[$j]}")
        if [[ $overlap -ge $OVERLAP_THRESHOLD ]]; then
            similar_indices="$similar_indices $j"
        fi
    done

    # Count sessions in group
    count=$(echo "$similar_indices" | wc -w | xargs)
    if [[ $count -gt 1 ]]; then
        GROUP_IDS+=("files_$group_counter")
        GROUP_TYPES+=("files")
        GROUP_SESSIONS+=("$similar_indices")

        for idx in $similar_indices; do
            ASSIGNED[$idx]=$group_counter
        done

        echo -e "    Group: file overlap -> $count sessions"
        ((group_counter++))
    fi
done

# Priority 3: Group by time proximity
echo -e "  ${CYAN}Phase 3: Grouping by time proximity (${TIME_WINDOW} min)...${NC}"
for ((i=0; i<${#SESSION_IDS[@]}; i++)); do
    [[ ${ASSIGNED[$i]} -ne -1 ]] && continue

    time1=${SESSION_TIMES_MIN[$i]}
    nearby_indices="$i"

    for ((j=i+1; j<${#SESSION_IDS[@]}; j++)); do
        [[ ${ASSIGNED[$j]} -ne -1 ]] && continue

        time2=${SESSION_TIMES_MIN[$j]}
        diff=$((time2 > time1 ? time2 - time1 : time1 - time2))

        if [[ $diff -le $TIME_WINDOW ]]; then
            nearby_indices="$nearby_indices $j"
        fi
    done

    count=$(echo "$nearby_indices" | wc -w | xargs)
    if [[ $count -gt 1 ]]; then
        GROUP_IDS+=("time_$group_counter")
        GROUP_TYPES+=("time")
        GROUP_SESSIONS+=("$nearby_indices")

        for idx in $nearby_indices; do
            ASSIGNED[$idx]=$group_counter
        done

        echo -e "    Group: time proximity -> $count sessions"
        ((group_counter++))
    fi
done

echo ""

# Count statistics
total_sessions=${#SESSION_IDS[@]}
grouped_count=0
for ((i=0; i<${#SESSION_IDS[@]}; i++)); do
    [[ ${ASSIGNED[$i]} -ne -1 ]] && ((grouped_count++))
done
ungrouped_count=$((total_sessions - grouped_count))
groups_count=${#GROUP_IDS[@]}

echo -e "${BLUE}=== Consolidation Summary ===${NC}"
echo -e "Total sessions: ${CYAN}$total_sessions${NC}"
echo -e "Groups formed: ${CYAN}$groups_count${NC}"
echo -e "Sessions grouped: ${GREEN}$grouped_count${NC}"
echo -e "Ungrouped: ${YELLOW}$ungrouped_count${NC}"
echo ""

# Show groups
if [[ $groups_count -gt 0 ]]; then
    echo -e "${BLUE}Groups:${NC}"
    for ((g=0; g<${#GROUP_IDS[@]}; g++)); do
        gid="${GROUP_IDS[$g]}"
        gtype="${GROUP_TYPES[$g]}"
        gessions="${GROUP_SESSIONS[$g]}"
        count=$(echo "$gessions" | wc -w | xargs)
        echo -e "  ${CYAN}$gid${NC} ($gtype): $count sessions"
        for idx in $gessions; do
            echo -e "    - ${SESSION_IDS[$idx]}"
        done
    done
    echo ""
fi

# Show ungrouped
if [[ $ungrouped_count -gt 0 ]]; then
    echo -e "${YELLOW}Ungrouped sessions:${NC}"
    for ((i=0; i<${#SESSION_IDS[@]}; i++)); do
        [[ ${ASSIGNED[$i]} -eq -1 ]] && echo -e "  - ${SESSION_IDS[$i]}"
    done
    echo ""
fi

# Generate output if not dry-run
if [[ "$DRY_RUN" = false ]]; then
    echo -e "${GREEN}Generating daily-summary.md...${NC}"

    # Generate output
    {
        echo "---"
        echo "type: daily-summary"
        echo "status: consolidated"
        echo "date: $TARGET_DATE"
        echo "sessions_merged: $total_sessions"
        echo "groups_formed: $groups_count"
        echo "original_files:"
        for sid in "${SESSION_IDS[@]}"; do
            echo "  - ${sid}.md"
        done
        echo "generated_at: $(date '+%Y-%m-%d %H:%M:%S %Z')"
        echo "---"
        echo ""
        echo "# Daily Summary: $TARGET_DATE"
        echo ""
        echo "## Overview"
        echo ""
        echo "| Metric | Value |"
        echo "|--------|-------|"
        echo "| Date | $TARGET_DATE |"
        echo "| Sessions Merged | $total_sessions |"
        echo "| Groups Formed | $groups_count |"
        echo "| Ungrouped | $ungrouped_count |"
        echo ""
        echo "---"
        echo ""
    } > "$OUTPUT_FILE"

    # Add grouped sessions
    group_num=1
    for ((g=0; g<${#GROUP_IDS[@]}; g++)); do
        gid="${GROUP_IDS[$g]}"
        gtype="${GROUP_TYPES[$g]}"
        gessions="${GROUP_SESSIONS[$g]}"

        # Get time range
        first_time=""
        last_time=""
        for idx in $gessions; do
            sid="${SESSION_IDS[$idx]}"
            time_part="${sid%%_*}"
            [[ -z "$first_time" ]] && first_time="$time_part"
            last_time="$time_part"
        done

        # Determine group title
        case "$gtype" in
            issue)
                issue_num="${gid#issue_}"
                group_title="Task $issue_num"
                ;;
            files)
                group_title="Related Files Group"
                ;;
            time)
                group_title="Time-Proximate Sessions"
                ;;
        esac

        count=$(echo "$gessions" | wc -w | xargs)

        {
            echo "## Group $group_num: $group_title"
            echo ""
            echo "> $count sessions merged | $first_time - $last_time | Type: $gtype"
            echo ""
            echo "### Sessions Included"
            echo ""
            echo "| Time | Session ID |"
            echo "|------|------------|"
        } >> "$OUTPUT_FILE"

        for idx in $gessions; do
            sid="${SESSION_IDS[$idx]}"
            time_part="${sid%%_*}"
            echo "| $time_part | $sid |" >> "$OUTPUT_FILE"
        done

        {
            echo ""
            echo "### Combined Content"
            echo ""
        } >> "$OUTPUT_FILE"

        for idx in $gessions; do
            sid="${SESSION_IDS[$idx]}"
            session_file="${SESSION_PATHS[$idx]}"
            {
                echo "<details>"
                echo "<summary>$sid</summary>"
                echo ""
                # Skip frontmatter, include rest
                sed '1,/^---$/d; 1,/^---$/d' "$session_file"
                echo ""
                echo "</details>"
                echo ""
            } >> "$OUTPUT_FILE"
        done

        echo "---" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"

        ((group_num++))
    done

    # Add ungrouped sessions
    if [[ $ungrouped_count -gt 0 ]]; then
        echo "## Ungrouped Sessions" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"

        for ((i=0; i<${#SESSION_IDS[@]}; i++)); do
            if [[ ${ASSIGNED[$i]} -eq -1 ]]; then
                sid="${SESSION_IDS[$i]}"
                session_file="${SESSION_PATHS[$i]}"
                time_part="${sid%%_*}"

                {
                    echo "### $sid ($time_part)"
                    echo ""
                    # Skip frontmatter, include rest
                    sed '1,/^---$/d; 1,/^---$/d' "$session_file"
                    echo ""
                    echo "---"
                    echo ""
                } >> "$OUTPUT_FILE"
            fi
        done
    fi

    # Footer
    {
        echo ""
        echo "---"
        echo ""
        echo "*Generated by Session Consolidation Script*"
        echo "*Original session files preserved in this directory*"
    } >> "$OUTPUT_FILE"

    echo -e "${GREEN}Created: $OUTPUT_FILE${NC}"
else
    echo -e "${YELLOW}Dry-run complete. Use --execute to create daily-summary.md${NC}"
fi
