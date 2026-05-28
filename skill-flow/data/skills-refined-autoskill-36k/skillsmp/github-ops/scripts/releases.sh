#!/usr/bin/env bash
#
# releases.sh - Release Operations for GitHub Ops Skill
# MCP Parity: list_releases, get_release, create_release, delete_release,
#             get_release_asset, upload_release_asset
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

LIMIT=30
JSON_OUTPUT=false
CONFIRM_DESTRUCTIVE=true

usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

Release Operations - GitHub MCP Server Parity

Actions:
  list              List releases
  view              View a release
  latest            View latest release
  create            Create a release
  delete            Delete a release
  download          Download release assets
  upload            Upload release asset

Common Options:
  --owner OWNER     Repository owner
  --repo REPO       Repository name
  --tag TAG         Release tag
  --title TITLE     Release title
  --notes NOTES     Release notes
  --file FILE       File to upload
  --pattern GLOB    Download pattern filter
  --limit N         Maximum results (default: 30)
  --draft           Create as draft
  --prerelease      Mark as prerelease
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") list --owner cli --repo cli --limit 5
  $(basename "$0") view --owner cli --repo cli --tag v2.86.0
  $(basename "$0") latest --owner cli --repo cli
  $(basename "$0") download --owner cli --repo cli --tag v2.86.0
EOF
    exit 0
}

error() { echo -e "${RED}Error: $1${NC}" >&2; exit 1; }
success() { echo -e "${GREEN}$1${NC}"; }
info() { echo -e "${BLUE}$1${NC}"; }

confirm() {
    if [[ "$CONFIRM_DESTRUCTIVE" == "true" ]]; then
        echo -e "${YELLOW}Warning: $1${NC}"
        read -p "Are you sure? (y/N) " -n 1 -r
        echo
        [[ ! $REPLY =~ ^[Yy]$ ]] && echo "Operation cancelled." && exit 2
    fi
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --owner) OWNER="$2"; shift 2 ;;
            --repo) REPO="$2"; shift 2 ;;
            --tag) TAG="$2"; shift 2 ;;
            --title) TITLE="$2"; shift 2 ;;
            --notes) NOTES="$2"; shift 2 ;;
            --file) FILE="$2"; shift 2 ;;
            --pattern) PATTERN="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --draft) DRAFT=true; shift ;;
            --prerelease) PRERELEASE=true; shift ;;
            --json) JSON_OUTPUT=true; shift ;;
            --no-confirm) CONFIRM_DESTRUCTIVE=false; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

action_list() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing releases for $OWNER/$REPO"
    gh release list --repo "$OWNER/$REPO" --limit "$LIMIT"
}

action_view() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${TAG:-}" ]] && error "Missing --tag"
    
    info "Fetching release: $TAG"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/releases/tags/$TAG"
    else
        gh release view "$TAG" --repo "$OWNER/$REPO"
    fi
}

action_latest() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Fetching latest release"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/releases/latest"
    else
        gh release view --repo "$OWNER/$REPO"
    fi
}

action_create() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${TAG:-}" ]] && error "Missing --tag"
    
    confirm "This will create release $TAG in $OWNER/$REPO"
    
    info "Creating release: $TAG"
    
    local cmd="gh release create $TAG --repo $OWNER/$REPO"
    [[ -n "${TITLE:-}" ]] && cmd="$cmd --title \"$TITLE\""
    [[ -n "${NOTES:-}" ]] && cmd="$cmd --notes \"$NOTES\""
    [[ "${DRAFT:-false}" == "true" ]] && cmd="$cmd --draft"
    [[ "${PRERELEASE:-false}" == "true" ]] && cmd="$cmd --prerelease"
    
    eval "$cmd"
    success "Release created"
}

action_delete() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${TAG:-}" ]] && error "Missing --tag"
    
    confirm "This will DELETE release $TAG from $OWNER/$REPO"
    
    info "Deleting release: $TAG"
    gh release delete "$TAG" --repo "$OWNER/$REPO" --yes
    success "Release deleted"
}

action_download() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${TAG:-}" ]] && error "Missing --tag"
    
    info "Downloading assets from release: $TAG"
    
    local cmd="gh release download $TAG --repo $OWNER/$REPO"
    [[ -n "${PATTERN:-}" ]] && cmd="$cmd --pattern \"$PATTERN\""
    
    eval "$cmd"
    success "Assets downloaded"
}

action_upload() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${TAG:-}" ]] && error "Missing --tag"
    [[ -z "${FILE:-}" ]] && error "Missing --file"
    
    confirm "This will upload $FILE to release $TAG"
    
    info "Uploading: $FILE"
    gh release upload "$TAG" "$FILE" --repo "$OWNER/$REPO"
    success "Asset uploaded"
}

main() {
    [[ $# -eq 0 ]] && usage
    local action="$1"; shift
    parse_args "$@"
    
    case "$action" in
        list) action_list ;;
        view) action_view ;;
        latest) action_latest ;;
        create) action_create ;;
        delete) action_delete ;;
        download) action_download ;;
        upload) action_upload ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action" ;;
    esac
}

main "$@"
