#!/bin/bash
#
# Render syntax-highlighted chunk summary
#
# Usage:
#   render-summary.sh [chunk_id]
#   render-summary.sh              # Current chunk
#   render-summary.sh chunk_phase_2_api

set -euo pipefail

CHUNKS_FILE="${CHUNKS_FILE:-.claude/.chunks.json}"

# Get chunk ID (use current if not specified)
if [ $# -eq 0 ]; then
  CHUNK_ID=$(jq -r '.current_chunk' "$CHUNKS_FILE")
else
  CHUNK_ID="$1"
fi

# Validate chunk exists
if ! jq -e ".chunks[] | select(.id == \"$CHUNK_ID\")" "$CHUNKS_FILE" >/dev/null; then
  echo "Error: Chunk not found: $CHUNK_ID" >&2
  exit 1
fi

# Extract chunk data
CHUNK_DATA=$(jq ".chunks[] | select(.id == \"$CHUNK_ID\")" "$CHUNKS_FILE")
CHUNK_NAME=$(echo "$CHUNK_DATA" | jq -r '.name')
CHUNK_DESC=$(echo "$CHUNK_DATA" | jq -r '.description')
CHUNK_STATUS=$(echo "$CHUNK_DATA" | jq -r '.status')
CHUNK_COMPLETION=$(echo "$CHUNK_DATA" | jq -r '.completion')
CHUNK_FILES=$(echo "$CHUNK_DATA" | jq -r '.files[]')
ENTRY_POINTS=$(echo "$CHUNK_DATA" | jq -r '.entry_points[]')
DEPENDENCIES=$(echo "$CHUNK_DATA" | jq -r '.dependencies[]')

# ANSI color codes
BOLD='\033[1m'
BLUE='\033[34m'
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
CYAN='\033[36m'
RESET='\033[0m'

# Status color
case "$CHUNK_STATUS" in
  completed)
    STATUS_COLOR="$GREEN"
    ;;
  in_progress)
    STATUS_COLOR="$YELLOW"
    ;;
  pending)
    STATUS_COLOR="$CYAN"
    ;;
  *)
    STATUS_COLOR="$RESET"
    ;;
esac

# Print header
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════${RESET}"
echo -e "${BOLD}${BLUE}  Chunk Summary${RESET}"
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════${RESET}"
echo ""

# Chunk metadata
echo -e "${BOLD}Name:${RESET} $CHUNK_NAME"
echo -e "${BOLD}ID:${RESET} $CHUNK_ID"
echo -e "${BOLD}Description:${RESET} $CHUNK_DESC"
echo -e "${BOLD}Status:${RESET} ${STATUS_COLOR}${CHUNK_STATUS}${RESET}"
echo -e "${BOLD}Completion:${RESET} ${CHUNK_COMPLETION}%"
echo ""

# Entry points
if [ -n "$ENTRY_POINTS" ]; then
  echo -e "${BOLD}${CYAN}Entry Points:${RESET}"
  echo "$ENTRY_POINTS" | while read -r file; do
    if [ -f "$file" ]; then
      echo -e "  ${GREEN}✓${RESET} $file"
    else
      echo -e "  ${RED}✗${RESET} $file ${RED}(missing)${RESET}"
    fi
  done
  echo ""
fi

# Dependencies
if [ -n "$DEPENDENCIES" ]; then
  echo -e "${BOLD}${CYAN}Dependencies:${RESET}"
  echo "$DEPENDENCIES" | while read -r dep_id; do
    dep_name=$(jq -r ".chunks[] | select(.id == \"$dep_id\") | .name" "$CHUNKS_FILE")
    dep_status=$(jq -r ".chunks[] | select(.id == \"$dep_id\") | .status" "$CHUNKS_FILE")

    case "$dep_status" in
      completed)
        echo -e "  ${GREEN}✓${RESET} $dep_name ${GREEN}($dep_status)${RESET}"
        ;;
      in_progress)
        echo -e "  ${YELLOW}⚠${RESET} $dep_name ${YELLOW}($dep_status)${RESET}"
        ;;
      *)
        echo -e "  ${RED}✗${RESET} $dep_name ${RED}($dep_status)${RESET}"
        ;;
    esac
  done
  echo ""
fi

# File statistics
TOTAL_FILES=$(echo "$CHUNK_FILES" | wc -l | tr -d ' ')
MISSING_FILES=$(echo "$CHUNK_FILES" | while read -r f; do [ ! -f "$f" ] && echo "$f"; done | wc -l | tr -d ' ')
EXISTING_FILES=$((TOTAL_FILES - MISSING_FILES))

echo -e "${BOLD}${CYAN}Files:${RESET} $EXISTING_FILES/$TOTAL_FILES exist"
echo ""

# List files with syntax highlighting indicators
echo -e "${BOLD}${CYAN}File Listing:${RESET}"
echo "$CHUNK_FILES" | while read -r file; do
  if [ ! -f "$file" ]; then
    echo -e "  ${RED}✗${RESET} $file ${RED}(missing)${RESET}"
    continue
  fi

  # Detect language from extension
  case "${file##*.}" in
    py)
      lang="${BLUE}Python${RESET}"
      ;;
    rs)
      lang="${YELLOW}Rust${RESET}"
      ;;
    go)
      lang="${CYAN}Go${RESET}"
      ;;
    jl)
      lang="${GREEN}Julia${RESET}"
      ;;
    ex|exs)
      lang="${RED}Elixir${RESET}"
      ;;
    js|jsx|ts|tsx)
      lang="${YELLOW}JavaScript${RESET}"
      ;;
    cpp|cc|h|hpp)
      lang="${BLUE}C++${RESET}"
      ;;
    zig)
      lang="${CYAN}Zig${RESET}"
      ;;
    *)
      lang="${RESET}Other${RESET}"
      ;;
  esac

  # File size
  size=$(du -h "$file" | cut -f1)

  # Last modified
  if [ "$(uname)" = "Darwin" ]; then
    mtime=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$file")
  else
    mtime=$(stat -c "%y" "$file" | cut -d' ' -f1-2 | cut -d. -f1)
  fi

  echo -e "  ${GREEN}✓${RESET} $file"
  echo -e "    ${BOLD}Language:${RESET} $lang  ${BOLD}Size:${RESET} $size  ${BOLD}Modified:${RESET} $mtime"
done

echo ""

# Show syntax-highlighted preview of entry points
if command -v bat >/dev/null 2>&1; then
  echo -e "${BOLD}${CYAN}Entry Point Previews:${RESET}"
  echo ""

  echo "$ENTRY_POINTS" | while read -r file; do
    if [ -f "$file" ]; then
      echo -e "${BOLD}$file:${RESET}"
      bat --style=plain --color=always --line-range=:30 "$file" 2>/dev/null || cat "$file" | head -30
      echo ""
    fi
  done
elif command -v pygmentize >/dev/null 2>&1; then
  echo -e "${BOLD}${CYAN}Entry Point Previews:${RESET}"
  echo ""

  echo "$ENTRY_POINTS" | while read -r file; do
    if [ -f "$file" ]; then
      echo -e "${BOLD}$file:${RESET}"
      head -30 "$file" | pygmentize -f terminal256 -l autodetect 2>/dev/null || head -30 "$file"
      echo ""
    fi
  done
else
  # No syntax highlighter available
  echo -e "${YELLOW}Tip: Install 'bat' or 'pygmentize' for syntax-highlighted previews${RESET}"
fi

# Footer
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════${RESET}"
