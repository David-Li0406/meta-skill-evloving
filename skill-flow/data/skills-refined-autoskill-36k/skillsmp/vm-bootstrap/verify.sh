#!/usr/bin/env bash
# vm-bootstrap/verify.sh - Linux VM Bootstrap Verification
#
# Usage: ./verify.sh [check|install|strict]
#   check   - Warn-only, never modifies (default)
#   install - Prompt before each install
#   strict  - Exit non-zero on first missing required tool

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

MODE="${1:-check}"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
REQUIRED_MISSING=0
OPTIONAL_MISSING=0

# ============================================================================
# Helper Functions
# ============================================================================

info() { echo -e "${BLUE}ℹ${NC} $*"; }
success() { echo -e "${GREEN}✓${NC} $*"; }
warn() { echo -e "${YELLOW}⚠${NC} $*"; }
error() { echo -e "${RED}✗${NC} $*"; }

check_os() {
    if [[ "$(uname -s)" != "Linux" ]]; then
        error "This skill is Linux-only. Detected: $(uname -s)"
        error "For macOS, use standard Homebrew-based setup."
        exit 1
    fi
    success "OS: Linux ($(uname -r))"
}

check_dirty_repo() {
    if [[ -d .git ]]; then
        if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
            if [[ "$MODE" == "check" ]]; then
                warn "Git repo has uncommitted changes (continuing in check mode)"
            else
                error "Git repo has uncommitted changes"
                error "In $MODE mode, please either:"
                error "  1. Commit or stash your changes first"
                error "  2. Use 'check' mode instead"
                exit 1
            fi
        fi
    fi
}

# Check command exists
check_cmd() {
    local cmd="$1"
    command -v "$cmd" >/dev/null 2>&1
}

# Check command with version output
verify_required() {
    local name="$1"
    local check_cmd="$2"
    
    if eval "$check_cmd" >/dev/null 2>&1; then
        local version
        version=$(eval "$check_cmd" 2>&1 | head -1)
        success "$name: $version"
        return 0
    else
        ((REQUIRED_MISSING++))
        error "$name: NOT FOUND"
        if [[ "$MODE" == "strict" ]]; then
            error "Strict mode: exiting on missing required tool"
            exit 1
        fi
        return 1
    fi
}

verify_optional() {
    local name="$1"
    local check_cmd="$2"
    
    if eval "$check_cmd" >/dev/null 2>&1; then
        local version
        version=$(eval "$check_cmd" 2>&1 | head -1)
        success "$name: $version"
        return 0
    else
        ((OPTIONAL_MISSING++))
        warn "$name: not found (optional)"
        return 1
    fi
}

# mise-wrapped command check
verify_mise_tool() {
    local name="$1"
    local tool="$2"
    local version_flag="${3:---version}"
    
    if check_cmd mise && mise exec -- "$tool" "$version_flag" >/dev/null 2>&1; then
        local version
        version=$(mise exec -- "$tool" "$version_flag" 2>&1 | head -1)
        success "$name (mise): $version"
        return 0
    elif check_cmd "$tool"; then
        local version
        version=$("$tool" "$version_flag" 2>&1 | head -1)
        success "$name (system): $version"
        return 0
    else
        ((REQUIRED_MISSING++))
        error "$name: NOT FOUND"
        if [[ "$MODE" == "strict" ]]; then
            error "Strict mode: exiting on missing required tool"
            exit 1
        fi
        return 1
    fi
}

verify_gh_auth() {
    if check_cmd gh; then
        if gh auth status >/dev/null 2>&1; then
            success "gh auth: authenticated"
        else
            warn "gh auth: not authenticated (run 'gh auth login')"
        fi
    fi
}

verify_railway_cli_version() {
    if ! check_cmd railway; then
        return 1
    fi

    local version
    version=$(railway --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "0.0.0")

    if [[ "$version" == "0.0.0" ]]; then
        warn "Railway CLI version check failed"
        return 1
    fi

    # Minimum version for GraphQL API support
    local min_version="3.0.0"

    # Simple version comparison
    if [[ "$version" < "$min_version" ]]; then
        warn "Railway CLI $version < $min_version (GraphQL API requires >= $min_version)"
        warn "  Update: mise use -g railway@latest"
        return 1
    fi

    success "Railway CLI version: $version (>= $min_version)"
    return 0
}

verify_railway_auth() {
    if ! check_cmd railway; then
        return 1
    fi

    if railway status >/dev/null 2>&1; then
        success "Railway auth: authenticated"
        return 0
    else
        warn "Railway auth: not authenticated (run 'railway login')"
        return 1
    fi
}

verify_skills_mount() {
    local skills_path="$HOME/.agent/skills"
    if [[ -L "$skills_path" ]]; then
        local target
        target=$(readlink "$skills_path")
        if [[ -d "$target" ]]; then
            success "~/.agent/skills: $target"
        else
            warn "~/.agent/skills: symlink exists but target missing ($target)"
        fi
    elif [[ -d "$skills_path" ]]; then
        success "~/.agent/skills: directory exists"
    else
        warn "~/.agent/skills: not mounted (run: ln -sfn ~/agent-skills ~/.agent/skills)"
    fi
}

# ============================================================================
# Main
# ============================================================================

main() {
    echo "======================================"
    echo " Linux VM Bootstrap Verification"
    echo " Mode: $MODE"
    echo "======================================"
    echo ""
    
    # OS Check
    info "Checking OS..."
    check_os
    
    # Dirty repo check (if in a git repo)
    if [[ -d .git ]]; then
        check_dirty_repo
    fi
    
    echo ""
    info "Checking required tools..."
    echo ""
    
    # System tools (apt-installed)
    verify_required "git" "git --version"
    verify_required "curl" "curl --version"
    verify_required "jq" "jq --version"
    verify_required "rg (ripgrep)" "rg --version"
    verify_required "tmux" "tmux -V"
    
    echo ""
    
    # Toolchain manager
    verify_required "mise" "mise --version"
    
    echo ""
    
    # Language runtimes (prefer mise-wrapped)
    verify_mise_tool "python" "python" "--version"
    verify_required "poetry" "poetry --version"
    verify_mise_tool "node" "node" "--version"
    verify_mise_tool "pnpm" "pnpm" "--version"
    
    echo ""
    
    # CLI tools
    verify_required "gh (GitHub CLI)" "gh --version"
    verify_gh_auth

    echo ""

    # Railway (version + auth specific checks)
    verify_mise_tool "railway" "railway" "--version"
    verify_railway_cli_version
    verify_railway_auth

    verify_required "bd (Beads)" "bd --version"
    
    echo ""
    
    # Skills mount
    verify_skills_mount
    
    echo ""
    info "Checking optional tools..."
    echo ""
    
    verify_optional "docker" "docker --version"
    verify_optional "tailscale" "tailscale version"
    verify_optional "bv (Beads Viewer)" "bv --version"
    verify_optional "playwright" "mise exec -- playwright --version"
    
    echo ""
    echo "======================================"
    echo " Summary"
    echo "======================================"
    
    if [[ $REQUIRED_MISSING -eq 0 ]]; then
        success "All required tools present"
    else
        error "$REQUIRED_MISSING required tools missing"
    fi
    
    if [[ $OPTIONAL_MISSING -gt 0 ]]; then
        warn "$OPTIONAL_MISSING optional tools not installed"
    fi
    
    echo ""
    
    # Exit code
    if [[ "$MODE" == "strict" && $REQUIRED_MISSING -gt 0 ]]; then
        exit 1
    fi
    
    exit 0
}

main "$@"
