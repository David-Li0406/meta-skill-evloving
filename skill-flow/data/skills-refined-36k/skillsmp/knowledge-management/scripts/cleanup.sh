#!/bin/bash
# Retention Policy Cleanup Script for Knowledge Management
# Cleans up old auto-captured files with optional archiving
#
# Usage: ./cleanup.sh [options]
# Options:
#   --days N         Retention period in days (default: 30)
#   --archive        Archive old files before deletion
#   --dry-run        Preview what would be deleted without making changes
#   --target DIR     Target directory (default: docs/auto-captured)
#   --all            Clean all targets (auto-captured, learnings with status:draft)
#   -h, --help       Show this help message

set -euo pipefail

# Default configuration
RETENTION_DAYS=30
ARCHIVE_ENABLED=false
DRY_RUN=false
TARGET_DIR=""
CLEAN_ALL=false
PROJECT_ROOT="${PROJECT_ROOT:-.}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Help message
show_help() {
    cat << EOF
Retention Policy Cleanup Script

Usage: ./cleanup.sh [options]

Options:
  --days N         Retention period in days (default: 30)
  --archive        Archive old files before deletion
  --dry-run        Preview what would be deleted without making changes
  --target DIR     Target directory relative to project root
                   (default: docs/auto-captured)
  --all            Clean all targets:
                   - docs/auto-captured (all files)
                   - docs/learnings (only status:draft files)
  -h, --help       Show this help message

Examples:
  ./cleanup.sh --dry-run                    # Preview with defaults
  ./cleanup.sh --days 7 --archive           # Archive & delete files older than 7 days
  ./cleanup.sh --all --days 14 --dry-run    # Preview all targets, 14 days retention
  ./cleanup.sh --target docs/learnings      # Clean specific directory

Configuration:
  Set PROJECT_ROOT environment variable to specify project location
  Current: $PROJECT_ROOT

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --days)
            if [[ -z "${2:-}" ]]; then
                echo -e "${RED}Error: --days requires an argument.${NC}"
                show_help
                exit 1
            fi

            if ! [[ "$2" =~ ^[0-9]+$ ]]; then
                echo -e "${RED}Error: --days value must be a positive integer. Got: '$2'${NC}"
                show_help
                exit 1
            fi

            if [[ "$2" -le 0 ]]; then
                echo -e "${RED}Error: --days value must be greater than zero. Got: '$2'${NC}"
                show_help
                exit 1
            fi

            RETENTION_DAYS="$2"
            shift 2
            ;;
        --archive)
            ARCHIVE_ENABLED=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --target)
            TARGET_DIR="${2:-}"
            shift 2
            ;;
        --all)
            CLEAN_ALL=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Validate PROJECT_ROOT
if [[ ! -d "$PROJECT_ROOT" ]]; then
    echo -e "${RED}Error: PROJECT_ROOT '$PROJECT_ROOT' does not exist${NC}"
    exit 1
fi

# Set timezone
TZ='Asia/Bangkok'
export TZ

# Calculate cutoff date
CUTOFF_DATE=$(date -v-${RETENTION_DAYS}d '+%Y-%m-%d' 2>/dev/null || date -d "-${RETENTION_DAYS} days" '+%Y-%m-%d')

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           Retention Policy Cleanup                         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "📅 Retention: ${GREEN}$RETENTION_DAYS days${NC}"
echo -e "📆 Cutoff date: ${GREEN}$CUTOFF_DATE${NC}"
echo -e "📦 Archive: ${GREEN}$ARCHIVE_ENABLED${NC}"
echo -e "🔍 Dry run: ${GREEN}$DRY_RUN${NC}"
echo ""

# Convert a YYYY-MM-DD date string to a Unix timestamp (seconds since epoch)
date_to_ts() {
    local date_str="$1"
    local ts

    # Try BSD/macOS date syntax first
    if ts=$(date -j -f '%Y-%m-%d' "$date_str" +%s 2>/dev/null); then
        echo "$ts"
        return 0
    fi

    # Fallback to GNU date syntax
    if ts=$(date -d "$date_str" +%s 2>/dev/null); then
        echo "$ts"
        return 0
    fi

    # If parsing fails, return empty and non-zero status
    return 1
}

# Function to get file date from path (YYYY-MM/DD format)
get_file_date() {
    local filepath="$1"
    # Extract YYYY-MM/DD from path
    local year_month day

    year_month=$(echo "$filepath" | grep -oE '[0-9]{4}-[0-9]{2}' | tail -1) || true
    day=$(echo "$filepath" | grep -oE '/[0-9]{2}/' | tail -1 | tr -d '/') || true

    if [[ -n "$year_month" && -n "$day" ]]; then
        echo "${year_month}-${day}"
    else
        # Fallback to file modification time
        stat -f '%Sm' -t '%Y-%m-%d' "$filepath" 2>/dev/null || stat -c '%y' "$filepath" 2>/dev/null | cut -d' ' -f1 || true
    fi
}

# Function to check if file is older than cutoff
is_old_file() {
    local filepath="$1"
    local file_date file_ts cutoff_ts

    file_date=$(get_file_date "$filepath")

    if [[ -z "$file_date" ]]; then
        return 1  # Can't determine date, don't delete
    fi

    # Convert dates to timestamps for reliable comparison
    if ! file_ts=$(date_to_ts "$file_date"); then
        return 1  # Can't parse file date, don't delete
    fi
    if ! cutoff_ts=$(date_to_ts "$CUTOFF_DATE"); then
        return 1  # Can't parse cutoff date, don't delete
    fi

    # Compare timestamps
    if (( file_ts < cutoff_ts )); then
        return 0  # File is old
    else
        return 1  # File is recent
    fi
}

# Function to check if learnings file is draft status
is_draft_learning() {
    local filepath="$1"

    # Check for status: draft in frontmatter
    if head -20 "$filepath" 2>/dev/null | grep -qE '^status:\s*(draft|pending)'; then
        return 0
    fi

    # Check for Distilled marker (means it's been processed)
    # Limit search to first 50 lines for efficiency
    if head -50 "$filepath" 2>/dev/null | grep -q 'Distilled:'; then
        return 1  # Already distilled, don't delete
    fi

    return 1  # Default: don't delete
}

# Function to create archive
# Returns 0 on success, 1 on failure
create_archive() {
    local source_dir="$1"
    local archive_name="$2"
    local files=("${@:3}")

    if [[ ${#files[@]} -eq 0 ]]; then
        return 0
    fi

    local archive_dir="$PROJECT_ROOT/docs/archives"
    mkdir -p "$archive_dir"

    local archive_path="$archive_dir/${archive_name}.tar.gz"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "  ${YELLOW}[DRY-RUN]${NC} Would create archive: $archive_path"
        echo -e "  ${YELLOW}[DRY-RUN]${NC} Files to archive: ${#files[@]}"
        return 0
    else
        # Create archive with error handling
        if tar -czf "$archive_path" -C "$PROJECT_ROOT" "${files[@]/#$PROJECT_ROOT\//}" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} Created archive: $archive_path"
            return 0
        else
            echo -e "  ${RED}✗${NC} Failed to create archive: $archive_path" >&2
            return 1
        fi
    fi
}

# Function to process a target directory
process_directory() {
    local target="$1"
    local filter_draft="$2"  # true for learnings
    local full_path="$PROJECT_ROOT/$target"

    if [[ ! -d "$full_path" ]]; then
        echo -e "${YELLOW}⚠️  Directory not found: $target${NC}"
        return 0
    fi

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "📁 Processing: ${GREEN}$target${NC}"
    echo ""

    local old_files=()
    local total_size=0
    local file_count=0

    # Find markdown files
    while IFS= read -r -d '' file; do
        if is_old_file "$file"; then
            # For learnings, only delete draft files
            if [[ "$filter_draft" == "true" ]]; then
                if ! is_draft_learning "$file"; then
                    continue
                fi
            fi

            old_files+=("$file")
            file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
            total_size=$((total_size + file_size))
            file_count=$((file_count + 1))

            file_date=$(get_file_date "$file")
            relative_path="${file#$PROJECT_ROOT/}"
            echo -e "  ${RED}×${NC} $relative_path ${YELLOW}($file_date)${NC}"
        fi
    done < <(find "$full_path" -type f -name "*.md" -print0 2>/dev/null || true)

    # Summary for this target
    echo ""
    if [[ $file_count -eq 0 ]]; then
        echo -e "  ${GREEN}✓${NC} No old files found"
    else
        # Convert size to human readable
        local size_human
        if [[ $total_size -gt 1048576 ]]; then
            size_human="$((total_size / 1048576)) MB"
        elif [[ $total_size -gt 1024 ]]; then
            size_human="$((total_size / 1024)) KB"
        else
            size_human="$total_size bytes"
        fi

        echo -e "  📊 Files to delete: ${RED}$file_count${NC}"
        echo -e "  💾 Space to free: ${GREEN}$size_human${NC}"

        # Archive if enabled
        local archive_success=true
        if [[ "$ARCHIVE_ENABLED" == "true" && $file_count -gt 0 ]]; then
            archive_name="archive_${target//\//_}_$(date '+%Y%m%d_%H%M%S')"
            if ! create_archive "$full_path" "$archive_name" "${old_files[@]}"; then
                archive_success=false
                echo -e "  ${RED}⚠️  Skipping deletion due to archive failure${NC}"
            fi
        fi

        # Delete files only if archive succeeded (or archiving was disabled)
        if [[ "$archive_success" == "true" ]]; then
            if [[ "$DRY_RUN" == "true" ]]; then
                echo -e "  ${YELLOW}[DRY-RUN]${NC} Would delete $file_count files"
            else
                for file in "${old_files[@]}"; do
                    rm "$file"
                done
                echo -e "  ${GREEN}✓${NC} Deleted $file_count files"

                # Clean up empty directories
                find "$full_path" -type d -empty -delete 2>/dev/null || true
            fi
        fi
    fi

    echo ""
    return $file_count
}

# Main execution
TOTAL_DELETED=0

if [[ "$CLEAN_ALL" == "true" ]]; then
    # Process all targets
    process_directory "docs/auto-captured" "false" || true
    TOTAL_DELETED=$((TOTAL_DELETED + $?))

    process_directory "docs/learnings" "true" || true
    TOTAL_DELETED=$((TOTAL_DELETED + $?))

elif [[ -n "$TARGET_DIR" ]]; then
    # Process specific target
    process_directory "$TARGET_DIR" "false" || true
    TOTAL_DELETED=$?

else
    # Default: process auto-captured only
    process_directory "docs/auto-captured" "false" || true
    TOTAL_DELETED=$?
fi

# Final summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Cleanup Complete${NC}"
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}This was a dry run. No files were actually deleted.${NC}"
    echo -e "Run without ${YELLOW}--dry-run${NC} to perform actual cleanup."
fi

echo ""
echo "Next steps:"
echo "  • Review archives in docs/archives/ (if archiving was enabled)"
echo "  • Run /distill to extract patterns from remaining learnings"
echo "  • Adjust retention period if needed"
