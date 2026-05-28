#!/bin/bash
# Environment loader for non-interactive shells
# Extracts and sources only the export statements from ~/.bashrc
#
# Usage:
#   source ~/.config/opencode/skill/research/scripts/load_env.sh
#
# This script helps load environment variables when running Python scripts
# from non-interactive shells (e.g., AI agents).

if [ -f ~/.bashrc ]; then
    # Extract export statements and source them in current shell
    eval "$(grep -E '^[[:space:]]*export[[:space:]]+' ~/.bashrc)"
    
    # Also source the env script that's referenced in bashrc
    if [ -f "$HOME/.local/bin/env" ]; then
        source "$HOME/.local/bin/env"
    fi
fi
