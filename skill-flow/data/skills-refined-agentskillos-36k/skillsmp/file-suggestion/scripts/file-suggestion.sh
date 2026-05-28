#!/bin/bash
# Custom file suggestion script for Claude Code
# Uses rg + fzf for fuzzy matching and symlink support
#
# Prerequisites: ripgrep, jq, fzf
#   Ubuntu/Debian: sudo apt install ripgrep jq fzf
#   macOS: brew install ripgrep jq fzf
#
# Installation:
#   1. Copy to ~/.claude/file-suggestion.sh
#   2. chmod +x ~/.claude/file-suggestion.sh
#   3. Add to ~/.claude/settings.json:
#      "fileSuggestion": {
#        "type": "command",
#        "command": "~/.claude/file-suggestion.sh"
#      }

# Parse JSON input to get query (sanitize to prevent shell injection)
QUERY=$(jq -r '.query // ""' | tr -cd 'a-zA-Z0-9._/ -')

# Use project dir from env, fallback to pwd
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

# cd into project dir so rg outputs relative paths
cd "$PROJECT_DIR" || exit 1

{
  # Main search - respects .gitignore, includes hidden files, follows symlinks
  rg --files --follow --hidden . 2>/dev/null

  # Additional paths - include even if gitignored (uncomment and customize)
  # [ -e .notes ] && rg --files --follow --hidden --no-ignore-vcs .notes 2>/dev/null
  # [ -e vendor ] && rg --files --follow --hidden --no-ignore-vcs vendor 2>/dev/null
} | sort -u | fzf --filter "$QUERY" | head -15
