#!/usr/bin/env bash

set -euo pipefail

function print_help() {
	echo "Usage: extract-issue-from-current-branch.sh [options]"
	echo
	echo "Extract Linear issue ID from current git branch name."
	echo
	echo "Options:"
	echo
	echo "  --help    Show this help message and exit."
}

# Parse arguments
while [[ $# -gt 0 ]]; do
	case "$1" in
	--help)
		print_help
		exit 0
		;;
	*)
		echo "Error: Unknown option: $1" >&2
		echo >&2
		print_help >&2
		exit 1
		;;
	esac
done

# Get current branch name
branch=$(git branch --show-current)

# Extract Linear issue ID (two or more letters, followed by dash and number)
issue_id=$(echo "$branch" | grep -oE "^[A-Za-z]+-[0-9]+" || true)

if [[ -n "$issue_id" ]]; then
	echo "$issue_id"
fi
