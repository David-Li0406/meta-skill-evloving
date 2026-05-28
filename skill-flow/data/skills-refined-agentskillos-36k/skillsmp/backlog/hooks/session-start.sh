#!/bin/bash

# Backlog SessionStart Hook
# Detects if Claude is starting in a git worktree and suggests loading context

set -euo pipefail

# Check if we're in a git repo at all
if ! git rev-parse --git-dir &>/dev/null; then
    exit 0
fi

# Function to verify submodules are functional
verify_submodules() {
    if [ ! -f ".gitmodules" ]; then
        return 0  # No submodules
    fi

    while IFS= read -r subpath; do
        if [ -d "$subpath" ] && ! git -C "$subpath" rev-parse --git-dir &>/dev/null 2>&1; then
            return 1  # Found a broken submodule
        fi
    done < <(grep "path = " .gitmodules 2>/dev/null | sed 's/.*path = //')

    return 0  # All submodules OK
}

# Method 3: Use git worktree list to detect if we're in a worktree
# This is the most reliable approach as it queries git's authoritative worktree list
is_secondary_worktree() {
    local current_dir
    current_dir=$(pwd -P)  # Canonical path

    # Get the main worktree (first line of git worktree list)
    local main_worktree
    main_worktree=$(git worktree list | head -1 | awk '{print $1}')

    # Check if current directory is in the worktree list but not the main one
    if git worktree list | grep -q "^${current_dir} "; then
        if [[ "$current_dir" != "$main_worktree" ]]; then
            return 0  # We are in a secondary worktree
        fi
    fi

    return 1  # Not in a secondary worktree
}

# Get worktree branch name
get_worktree_branch() {
    git branch --show-current 2>/dev/null || echo "unknown"
}

# Try to extract task info from branch name or PROMPT.md
get_task_info() {
    local branch="$1"
    local task_id=""
    local task_title=""

    # Try to find task ID from PROMPT.md
    if [[ -f "PROMPT.md" ]]; then
        # Look for **Task:** MKT-001 or similar pattern
        task_id=$(grep -oE '\*\*Task:\*\* [A-Z]+-[0-9]+' PROMPT.md 2>/dev/null | head -1 | sed 's/\*\*Task:\*\* //' || echo "")

        # Try to get title from the same line
        if [[ -n "$task_id" ]]; then
            task_title=$(grep "^\*\*Task:\*\*" PROMPT.md 2>/dev/null | head -1 | sed 's/.*\*\*Task:\*\* [A-Z]*-[0-9]* - //' | sed 's/\*\*$//' || echo "")
        fi
    fi

    # If no task ID found, try to infer from branch name
    if [[ -z "$task_id" ]] && [[ "$branch" == feature/* ]]; then
        local feature_name="${branch#feature/}"
        echo "Feature: $feature_name"
        return
    fi

    if [[ -n "$task_id" ]]; then
        if [[ -n "$task_title" ]]; then
            echo "$task_id - $task_title"
        else
            echo "$task_id"
        fi
    fi
}

# Main logic
if is_secondary_worktree; then
    BRANCH=$(get_worktree_branch)
    TASK_INFO=$(get_task_info "$BRANCH")

    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo " WORKTREE DETECTED"
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    echo "Branch: $BRANCH"

    if [[ -n "$TASK_INFO" ]]; then
        echo "Task:   $TASK_INFO"
    fi

    echo ""

    # Check for context files and instruct Claude to begin work
    if [[ -f "PROMPT.md" ]]; then
        echo "Context files:"
        echo "  - PROMPT.md (task instructions)"

        # Check for PROGRESS.md
        if [[ -f "PROGRESS.md" ]]; then
            echo "  - PROGRESS.md (prior work log)"
        fi

        # Check for task directory files
        if [[ -d "tasks" ]]; then
            for f in TASK.md PROGRESS.md REVIEW.md; do
                if find tasks -name "$f" -print -quit 2>/dev/null | grep -q .; then
                    echo "  - tasks/*/$f"
                fi
            done
        fi

        # Check for broken submodules before starting work
        if ! verify_submodules; then
            echo ""
            echo "═══════════════════════════════════════════════════════════════════"
            echo " ⚠️  SUBMODULE ISSUE DETECTED"
            echo "═══════════════════════════════════════════════════════════════════"
            echo ""
            echo "Some submodules are not properly initialized in this worktree."
            echo "Git commands may fail in submodule directories."
            echo ""
            echo "INSTRUCTION: Before starting work, run:"
            echo "  git submodule update --init --recursive"
            echo ""
            echo "If that fails, output:"
            echo "  <promise>TASK_BLOCKED: Submodules broken, needs reinitialization</promise>"
            echo ""
            echo "═══════════════════════════════════════════════════════════════════"
        else
            echo ""
            echo "═══════════════════════════════════════════════════════════════════"
            echo ""
            echo "INSTRUCTION: You are in an agent worktree. Read PROMPT.md now and"
            echo "begin working on the task immediately. If PROGRESS.md exists, review"
            echo "it first to continue from where you left off. Do not wait for user"
            echo "input - start the task autonomously."
            echo ""
        fi
    else
        echo "No PROMPT.md found in this worktree."
        echo "This may be a manually created worktree."
    fi

    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
fi

exit 0
