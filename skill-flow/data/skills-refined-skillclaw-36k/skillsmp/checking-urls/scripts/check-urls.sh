#!/bin/bash

# URL Checker for Learn In Public Repository
# Validates internal and external URLs in markdown files

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
LOG_DIR="$REPO_ROOT/logs/url-checks"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG_FILE="$LOG_DIR/$DATE.log"
UNRESOLVED_FILE="$LOG_DIR/UNRESOLVED.md"

mkdir -p "$LOG_DIR"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL=0
VALID=0
INVALID=0
SKIPPED=0

# Arrays to track results
declare -a BROKEN_LINKS=()

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

check_internal_link() {
    local source_file="$1"
    local link="$2"
    local source_dir=$(dirname "$source_file")
    
    # Remove anchor if present
    local path_only="${link%%#*}"
    
    # Handle empty path (anchor-only link like #section)
    if [[ -z "$path_only" ]]; then
        return 0  # Skip anchor-only links for now
    fi
    
    # Resolve relative path
    local full_path
    if [[ "$path_only" == /* ]]; then
        full_path="$REPO_ROOT$path_only"
    else
        full_path="$source_dir/$path_only"
    fi
    
    # Normalize path
    full_path=$(cd "$(dirname "$full_path")" 2>/dev/null && echo "$(pwd)/$(basename "$full_path")" || echo "$full_path")
    
    if [[ -e "$full_path" ]]; then
        log "✓ VALID: $link (from $source_file)"
        ((VALID++))
        return 0
    else
        local rel_source="${source_file#$REPO_ROOT/}"
        log "✗ MISSING: $link (from $rel_source)"
        BROKEN_LINKS+=("$rel_source | $link | file not found")
        ((INVALID++))
        return 1
    fi
}

check_external_link() {
    local source_file="$1"
    local url="$2"
    
    # Skip certain URLs
    if [[ "$url" =~ ^mailto: ]] || [[ "$url" =~ ^javascript: ]]; then
        log "⊘ SKIPPED: $url (unsupported protocol)"
        ((SKIPPED++))
        return 0
    fi
    
    # Skip example/placeholder URLs
    if [[ "$url" =~ example\.com ]] || [[ "$url" =~ broken-link\.com ]] || [[ "$url" =~ placeholder ]] || [[ "$url" =~ localhost ]]; then
        log "⊘ SKIPPED: $url (example/placeholder URL)"
        ((SKIPPED++))
        return 0
    fi
    
    # Use curl with timeout and follow redirects
    local http_code
    http_code=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 10 --connect-timeout 5 "$url" 2>/dev/null || echo "000")
    
    local rel_source="${source_file#$REPO_ROOT/}"
    # 2xx/3xx = success, 429 = rate limited (URL exists), 403 = blocked but exists
    if [[ "$http_code" =~ ^[23] ]] || [[ "$http_code" == "429" ]] || [[ "$http_code" == "403" ]]; then
        log "✓ VALID: $url ($http_code)"
        ((VALID++))
        return 0
    else
        log "✗ INVALID: $url (HTTP $http_code from $rel_source)"
        BROKEN_LINKS+=("$rel_source | $url | HTTP $http_code")
        ((INVALID++))
        return 1
    fi
}

extract_urls() {
    local file="$1"
    
    # Extract markdown links [text](url) and bare URLs
    grep -oE '\[([^\]]+)\]\(([^)]+)\)' "$file" 2>/dev/null | sed -E 's/\[([^\]]+)\]\(([^)]+)\)/\2/' || true
    grep -oE 'https?://[^[:space:]<>"\)]+' "$file" 2>/dev/null || true
}

# Main execution
echo -e "${YELLOW}=== URL Check Started: $TIMESTAMP ===${NC}"
log "=== URL Check Started ==="

# Find all markdown files
while IFS= read -r -d '' file; do
    log "CHECKING: $file"
    
    while IFS= read -r url; do
        [[ -z "$url" ]] && continue
        ((TOTAL++))
        
        if [[ "$url" =~ ^https?:// ]]; then
            check_external_link "$file" "$url" || true
        else
            check_internal_link "$file" "$url" || true
        fi
    done < <(extract_urls "$file" | sort -u)
    
done < <(find "$REPO_ROOT" -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/logs/*" -print0)

# Summary
echo ""
echo -e "${YELLOW}=== Summary ===${NC}"
log "=== Summary ==="
log "Total URLs checked: $TOTAL"
log "Valid: $VALID"
log "Invalid: $INVALID"
log "Skipped: $SKIPPED"

# Update UNRESOLVED.md
{
    echo "# Unresolved URLs"
    echo ""
    echo "Last checked: $TIMESTAMP"
    echo ""
    if [[ ${#BROKEN_LINKS[@]} -eq 0 ]]; then
        echo "✅ All URLs are valid!"
    else
        echo "## Broken Links (${#BROKEN_LINKS[@]})"
        echo ""
        echo "| Source File | Broken URL | Status |"
        echo "|-------------|------------|--------|"
        for link in "${BROKEN_LINKS[@]}"; do
            echo "| $link |"
        done
    fi
} > "$UNRESOLVED_FILE"

# Output results
if [[ ${#BROKEN_LINKS[@]} -gt 0 ]]; then
    echo -e "${RED}=== BROKEN LINKS FOUND ===${NC}"
    echo ""
    printf "${RED}%-50s %-50s %s${NC}\n" "SOURCE" "BROKEN URL" "STATUS"
    printf "${RED}%-50s %-50s %s${NC}\n" "------" "----------" "------"
    for link in "${BROKEN_LINKS[@]}"; do
        IFS='|' read -r src url status <<< "$link"
        printf "${RED}%-50s %-50s %s${NC}\n" "$src" "$url" "$status"
    done
    echo ""
    echo -e "${YELLOW}See $UNRESOLVED_FILE for tracking${NC}"
    exit 1
else
    echo -e "${GREEN}✓ All $TOTAL URLs are valid!${NC}"
    exit 0
fi
