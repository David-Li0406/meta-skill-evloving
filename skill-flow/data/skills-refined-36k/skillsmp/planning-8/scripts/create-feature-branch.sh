#!/usr/bin/env bash
set -euo pipefail

function print_help() {
	echo "Usage: create-feature-branch.sh [options]"
	echo
	echo "Create or switch to a feature branch, with Git Town support."
	echo
	echo "Options:"
	echo
	echo "  --featureBranch <branch>    Name of the feature branch (required)."
	echo "  --baseBranch <branch>       Name of the base branch (required)."
	echo "  --help                      Show this help message and exit."
}

# Parse arguments
feature_branch=""
base_branch=""

while [[ $# -gt 0 ]]; do
	case "$1" in
	--help)
		print_help
		exit 0
		;;
	--featureBranch)
		feature_branch="$2"
		shift 2
		;;
	--baseBranch)
		base_branch="$2"
		shift 2
		;;
	*)
		echo "Error: Unknown option: $1" >&2
		echo >&2
		print_help >&2
		exit 1
		;;
	esac
done

# Validate required arguments
if [[ -z "$feature_branch" ]]; then
	echo "Error: --featureBranch is required" >&2
	echo >&2
	print_help >&2
	exit 1
fi

if [[ -z "$base_branch" ]]; then
	echo "Error: --baseBranch is required" >&2
	echo >&2
	print_help >&2
	exit 1
fi

# Check if working directory is clean
if ! git diff-index --quiet HEAD --; then
	echo "Error: Working directory is not clean. Please commit or stash your changes before switching branches." >&2
	exit 1
fi

# Check if branch already exists
if git show-ref --verify --quiet "refs/heads/$feature_branch"; then
	git switch "$feature_branch"
	exit 0
fi

# Check if repository is using Git Town
if [ -f "git-town.toml" ] || [ -f ".git-town.toml" ] || [ -f ".git-branches.toml" ]; then
	git switch "$base_branch"
	git town append "$feature_branch"
	exit 0
fi

# Use standard Git commands
git switch -c "$feature_branch" "$base_branch"
