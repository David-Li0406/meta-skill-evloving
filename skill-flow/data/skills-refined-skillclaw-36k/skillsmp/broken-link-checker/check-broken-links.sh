#!/bin/bash
#
# Broken Link Checker for Markdown Files
# Checks internal links and anchor links in markdown files
#

set -euo pipefail

# Calculate project root from script location
PROJECT_ROOT="$(cd "$(dirname "$0")/../../../" && pwd)"

# Default options
TARGET_PATH="$PROJECT_ROOT"
VERBOSE=false

# Counters
TOTAL_LINKS=0
VALID_LINKS=0
BROKEN_LINKS=0
SKIPPED_LINKS=0

# Arrays for results
declare -a BROKEN_RESULTS=()

# Colors (only if terminal supports it)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --path)
            TARGET_PATH="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --path <dir>       Specify directory to check (default: project root)"
            echo "  --verbose, -v      Show detailed progress"
            echo "  --help, -h         Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Convert to absolute path if relative
if [[ ! "$TARGET_PATH" = /* ]]; then
    TARGET_PATH="$PROJECT_ROOT/$TARGET_PATH"
fi

# Print header
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Broken Link Checker                                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Find all markdown files (excluding hidden directories and node_modules)
# Note: .conductor exclusion is skipped when running from within .conductor workspace
if [[ "$TARGET_PATH" == *"/.conductor/"* ]]; then
    MARKDOWN_FILES=$(find "$TARGET_PATH" -name "*.md" \
        -not -path "*/node_modules/*" \
        -not -path "*/.git/*" \
        -not -path "*/dist/*" \
        2>/dev/null | sort)
else
    MARKDOWN_FILES=$(find "$TARGET_PATH" -name "*.md" \
        -not -path "*/node_modules/*" \
        -not -path "*/.git/*" \
        -not -path "*/dist/*" \
        -not -path "*/.conductor/*" \
        2>/dev/null | sort)
fi

if [ -n "$MARKDOWN_FILES" ]; then
    FILE_COUNT=$(echo "$MARKDOWN_FILES" | wc -l | tr -d ' ')
else
    FILE_COUNT=0
fi
echo "📁 검사 대상: ${FILE_COUNT}개 마크다운 파일"
echo ""
echo "──────────────────────────────────────────────────────────────────"
echo ""

START_TIME=$(date +%s)

# Function to convert heading to GitHub anchor ID
# GitHub's anchor generation rules:
# 1. Convert to lowercase
# 2. Remove characters that are not alphanumeric, spaces, hyphens, or underscores
# 3. Replace spaces with hyphens
# 4. Keep underscores as-is (they become part of the anchor)
# Note: Using perl for Unicode support (Korean characters) to avoid locale issues
heading_to_anchor() {
    local heading="$1"
    # Use perl for proper Unicode handling (Korean characters)
    # Perl's \p{L} matches any Unicode letter, including Korean
    echo "$heading" | \
        perl -CSD -Mutf8 -ne 'use utf8; binmode(STDOUT, ":utf8"); chomp; $_ = lc($_); s/[^\p{L}\p{N} _-]//g; s/ /-/g; print "$_\n"'
}

# Function to extract headings from a markdown file
extract_headings() {
    local file="$1"
    grep -E "^#{1,6} " "$file" 2>/dev/null | \
        sed 's/^#* //' | \
        while read -r heading; do
            heading_to_anchor "$heading"
        done
}

# Function to check if an internal link is valid
check_internal_link() {
    local source_file="$1"
    local link="$2"
    local source_dir=$(dirname "$source_file")

    # Handle anchor-only links
    if [[ "$link" =~ ^# ]]; then
        local anchor="${link#\#}"
        local anchors=$(extract_headings "$source_file")
        if echo "$anchors" | grep -qx "$anchor"; then
            return 0
        else
            return 1
        fi
    fi

    # Separate path and anchor
    local path="${link%%#*}"
    local anchor=""
    if [[ "$link" =~ \# ]]; then
        anchor="${link#*#}"
    fi

    # Resolve relative path
    local resolved_path
    if [[ "$path" = /* ]]; then
        resolved_path="$PROJECT_ROOT$path"
    else
        resolved_path="$source_dir/$path"
    fi

    # Normalize path
    resolved_path=$(cd "$(dirname "$resolved_path")" 2>/dev/null && pwd)/$(basename "$resolved_path") 2>/dev/null || echo ""

    # Check file existence
    if [[ -z "$resolved_path" ]] || [[ ! -e "$resolved_path" ]]; then
        return 1
    fi

    # Check anchor if present
    if [[ -n "$anchor" ]] && [[ -f "$resolved_path" ]]; then
        local anchors=$(extract_headings "$resolved_path")
        if ! echo "$anchors" | grep -qx "$anchor"; then
            return 2  # File exists but anchor not found
        fi
    fi

    return 0
}

# Extract and check links from each file
for file in $MARKDOWN_FILES; do
    [[ -z "$file" ]] && continue

    relative_file="${file#$PROJECT_ROOT/}"

    if [ "$VERBOSE" = true ]; then
        echo "🔍 검사 중: $relative_file"
    fi

    # Extract markdown links: [text](url)
    while IFS= read -r match_line; do
        [[ -z "$match_line" ]] && continue

        # Parse line number and link
        line_num="${match_line%%:*}"
        full_match="${match_line#*:}"

        # Extract URL from [text](url)
        link=$(echo "$full_match" | sed 's/.*](\([^)]*\)).*/\1/')
        [[ -z "$link" ]] && continue

        TOTAL_LINKS=$((TOTAL_LINKS + 1))

        # Determine link type
        if [[ "$link" =~ ^https?:// ]] || [[ "$link" =~ ^(mailto:|tel:) ]]; then
            # External URL - skip
            SKIPPED_LINKS=$((SKIPPED_LINKS + 1))
            continue
        elif [[ "$link" =~ ^# ]]; then
            # Anchor link within same file
            if check_internal_link "$file" "$link"; then
                VALID_LINKS=$((VALID_LINKS + 1))
            else
                BROKEN_LINKS=$((BROKEN_LINKS + 1))
                BROKEN_RESULTS+=("📄 ${relative_file}:${line_num}|   └─ ${link} (앵커 없음)")
            fi
        else
            # Internal relative link
            if check_internal_link "$file" "$link"; then
                VALID_LINKS=$((VALID_LINKS + 1))
            else
                result=$?
                if [[ $result -eq 2 ]]; then
                    BROKEN_LINKS=$((BROKEN_LINKS + 1))
                    BROKEN_RESULTS+=("📄 ${relative_file}:${line_num}|   └─ ${link} (앵커 없음)")
                else
                    BROKEN_LINKS=$((BROKEN_LINKS + 1))
                    BROKEN_RESULTS+=("📄 ${relative_file}:${line_num}|   └─ ${link} (파일 없음)")
                fi
            fi
        fi
    done < <(grep -n -oE '\[[^]]+\]\([^)]+\)' "$file" 2>/dev/null || true)

    # Also check reference-style links: [text][ref] and [ref]: url
    # Using grep -n to get line numbers directly (performance optimization)
    while IFS=':' read -r line_num ref_line; do
        [[ -z "$ref_line" ]] && continue

        # Extract URL from [ref]: url "title" or [ref]: <url>
        # Handles both <url> and plain url formats
        ref_url_part=$(echo "$ref_line" | sed -E 's/^\s*\[[^]]+\]:\s*(<[^>]+>|[^ ]+).*/\1/')
        ref_url=$(echo "$ref_url_part" | sed 's/^<//; s/>$//') # Strip < >
        [[ -z "$ref_url" ]] && continue

        TOTAL_LINKS=$((TOTAL_LINKS + 1))

        if [[ "$ref_url" =~ ^https?:// ]] || [[ "$ref_url" =~ ^(mailto:|tel:) ]]; then
            # External URL - skip
            SKIPPED_LINKS=$((SKIPPED_LINKS + 1))
            continue
        elif [[ "$ref_url" =~ ^# ]]; then
            # Anchor link within same file
            if check_internal_link "$file" "$ref_url"; then
                VALID_LINKS=$((VALID_LINKS + 1))
            else
                BROKEN_LINKS=$((BROKEN_LINKS + 1))
                BROKEN_RESULTS+=("📄 ${relative_file}:${line_num}|   └─ ${ref_url} (앵커 없음)")
            fi
        else
            # Internal relative link
            if check_internal_link "$file" "$ref_url"; then
                VALID_LINKS=$((VALID_LINKS + 1))
            else
                result=$?
                if [[ $result -eq 2 ]]; then
                    BROKEN_LINKS=$((BROKEN_LINKS + 1))
                    BROKEN_RESULTS+=("📄 ${relative_file}:${line_num}|   └─ ${ref_url} (앵커 없음)")
                else
                    BROKEN_LINKS=$((BROKEN_LINKS + 1))
                    BROKEN_RESULTS+=("📄 ${relative_file}:${line_num}|   └─ ${ref_url} (파일 없음)")
                fi
            fi
        fi
    done < <(grep -n -E '^\[.*\]: ' "$file" 2>/dev/null || true)
done

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

# Print results
if [ ${#BROKEN_RESULTS[@]} -gt 0 ]; then
    echo -e "${RED}❌ 깨진 링크 발견: ${BROKEN_LINKS}개${NC}"
    echo ""

    for result in "${BROKEN_RESULTS[@]}"; do
        file_info="${result%%|*}"
        link_info="${result#*|}"
        echo "$file_info"
        echo "$link_info"
        echo ""
    done
else
    echo -e "${GREEN}✅ 깨진 링크가 없습니다!${NC}"
    echo ""
fi

echo "──────────────────────────────────────────────────────────────────"
echo ""
echo -e "${GREEN}✅ 정상 링크: ${VALID_LINKS}개${NC}"
echo -e "${RED}❌ 깨진 링크: ${BROKEN_LINKS}개${NC}"
if [ $SKIPPED_LINKS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  스킵됨: ${SKIPPED_LINKS}개${NC}"
fi
echo ""
echo "총 검사 시간: ${ELAPSED}초"

# Exit with error if broken links found
if [ $BROKEN_LINKS -gt 0 ]; then
    exit 1
fi

exit 0
