#!/bin/bash
# Core version manager - technology agnostic
# Handles: tag parsing, semver calculation, version bumping

set -euo pipefail

# === CONFIGURATION ===
BASE_VERSION="${BASE_VERSION:-1.0}"
TAG_PREFIX="${TAG_PREFIX:-v}"

# === CORE FUNCTIONS ===

get_latest_version() {
    local prefix="${1:-$TAG_PREFIX}"
    git tag -l "${prefix}*" 2>/dev/null |
        sed "s/^${prefix}//" |
        sort -V |
        tail -1 || echo "0.0.0"
}

bump_version() {
    local version="$1"
    local bump_type="${2:-patch}"

    IFS='.' read -r major minor patch <<< "$version"
    major="${major:-0}"; minor="${minor:-0}"; patch="${patch:-0}"

    case "$bump_type" in
        major) major=$((major + 1)); minor=0; patch=0 ;;
        minor) minor=$((minor + 1)); patch=0 ;;
        patch) patch=$((patch + 1)) ;;
    esac

    echo "${major}.${minor}.${patch}"
}

generate_version() {
    local bump_type="${1:-patch}"
    local latest
    latest=$(get_latest_version)

    if [[ "$latest" == "0.0.0" ]]; then
        echo "${BASE_VERSION}.0"
    else
        bump_version "$latest" "$bump_type"
    fi
}

output_version() {
    local version="$1"
    local is_prerelease="${2:-false}"

    if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
        echo "version=$version" >> "$GITHUB_OUTPUT"
        echo "is-prerelease=$is_prerelease" >> "$GITHUB_OUTPUT"
        echo "tag=${TAG_PREFIX}${version}" >> "$GITHUB_OUTPUT"
    fi

    echo "$version"
}

main() {
    local command="${1:-generate}"
    local arg="${2:-patch}"

    case "$command" in
        generate) output_version "$(generate_version "$arg")" "false" ;;
        latest)   get_latest_version ;;
        bump)     bump_version "$(get_latest_version)" "$arg" ;;
        *)        echo "Usage: $0 {generate|latest|bump} [patch|minor|major]" >&2; exit 1 ;;
    esac
}

main "$@"
