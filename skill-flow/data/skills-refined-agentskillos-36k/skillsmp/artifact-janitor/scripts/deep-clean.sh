#!/bin/bash

# artifact-janitor: Deep Clean Script (2026 Edition)
# A robust utility to reclaim disk space by removing build artifacts and caches.

set -e

# --- Configuration ---
TARGETS=(
    "node_modules"
    ".next"
    ".turbo"
    ".cache"
    "dist"
    "build"
    ".angular"
    "out"
    ".vercel"
    ".netlify"
    "tsconfig.tsbuildinfo"
    "*.log"
    ".DS_Store"
    "coverage"
    ".nyc_output"
    "vendor"
)

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# --- Functions ---

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dry_run() {
    if [[ "$DRY_RUN" == "true" ]]; then
        return 0 # True
    else
        return 1 # False
    fi
}

# --- Execution ---

DRY_RUN=false
FORCE=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=true ;;
        --force) FORCE=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

log_info "Starting deep clean in $(pwd)..."

if check_dry_run; then
    log_warn "DRY RUN MODE: No files will be deleted."
fi

TOTAL_SIZE=0

for target in "${TARGETS[@]}"; do
    # Find all occurrences of the target
    # Use -prune to avoid entering directories that are already targets
    FOUND=$(find . -name "$target" -prune 2>/dev/null)
    
    if [[ -n "$FOUND" ]]; then
        while IFS= read -r path; do
            if [[ -e "$path" ]]; then
                SIZE=$(du -sk "$path" | cut -f1)
                TOTAL_SIZE=$((TOTAL_SIZE + SIZE))
                
                if check_dry_run; then
                    echo "Would remove: $path ($(du -sh "$path" | cut -f1))"
                else
                    log_info "Removing: $path ($(du -sh "$path" | cut -f1))"
                    rm -rf "$path"
                fi
            fi
        done <<< "$FOUND"
    fi
done

# Human readable total size
HUMAN_SIZE=$(echo "$TOTAL_SIZE" | awk '{
    if ($1 >= 1048576) printf "%.2f GB", $1/1048576;
    else if ($1 >= 1024) printf "%.2f MB", $1/1024;
    else printf "%d KB", $1;
}')

if check_dry_run; then
    log_info "Total space that would be reclaimed: $HUMAN_SIZE"
else
    log_info "Successfully reclaimed $HUMAN_SIZE of disk space."
    log_info "Remember to run 'bun install' or 'pnpm install' to restore dependencies if needed."
fi
